from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils.timezone import now

from doctors.models import AvailabilitySlot
from accounts.models import User

from .models import Booking
from django.db import transaction

from .google_calendar import create_calendar_event
from accounts.email_service import send_email


@login_required
def doctor_list(request):

    if request.user.role != 'patient':
        return redirect('dashboard')

    doctors = User.objects.filter(role='doctor')

    return render(
        request,
        'bookings/doctor_list.html',
        {'doctors': doctors}
    )


@login_required
def available_slots(request, doctor_id):

    if request.user.role != 'patient':
        return redirect('dashboard')

    slots = AvailabilitySlot.objects.filter(
        doctor_id=doctor_id,
        is_booked=False,
        date__gte=now().date()
    ).order_by('date', 'start_time')

    doctor = User.objects.get(id=doctor_id)

    return render(
        request,
        'bookings/available_slots.html',
        {
            'slots': slots,
            'doctor': doctor
        }
    )


@login_required
@require_POST
@transaction.atomic
def book_slot(request, slot_id):

    if request.user.role != 'patient':
        return redirect('dashboard')

    slot = AvailabilitySlot.objects.select_for_update().get(
        id=slot_id
    )

    if slot.is_booked:

        return render(
            request,
            'bookings/already_booked.html'
        )

    Booking.objects.create(
        patient=request.user,
        slot=slot,
        status='pending'
    )

    send_email(
        request.user.email,
        "Appointment Request Submitted",
        f"""
Your appointment request has been submitted.

Doctor: Dr. {slot.doctor.username}

Date: {slot.date}

Time: {slot.start_time} - {slot.end_time}

Status: Pending Approval
"""
    )

    return redirect('my_bookings')


@login_required
def my_bookings(request):

    if request.user.role != 'patient':
        return redirect('dashboard')

    bookings = Booking.objects.filter(
        patient=request.user
    )

    return render(
        request,
        'bookings/my_bookings.html',
        {'bookings': bookings}
    )


@login_required
def pending_requests(request):

    if request.user.role != 'doctor':
        return redirect('dashboard')

    bookings = Booking.objects.filter(
        slot__doctor=request.user,
        status='pending'
    )

    return render(
        request,
        'bookings/pending_requests.html',
        {'bookings': bookings}
    )


@login_required
def approve_booking(request, booking_id):

    if request.user.role != 'doctor':
        return redirect('dashboard')

    booking = Booking.objects.get(id=booking_id)

    booking.status = 'approved'
    booking.save()

    booking.slot.is_booked = True
    booking.slot.save()

    create_calendar_event(
        booking.slot,
        booking.patient
    )

    send_email(
        booking.patient.email,
        "Appointment Approved",
        f"""
Your appointment has been approved.

Doctor: Dr. {booking.slot.doctor.username}

Date: {booking.slot.date}

Time: {booking.slot.start_time} - {booking.slot.end_time}
"""
    )

    return redirect('pending_requests')


@login_required
def reject_booking(request, booking_id):

    if request.user.role != 'doctor':
        return redirect('dashboard')

    booking = Booking.objects.get(id=booking_id)

    booking.status = 'rejected'
    booking.save()

    send_email(
        booking.patient.email,
        "Appointment Rejected",
        f"""
Your appointment request was rejected.

Doctor: Dr. {booking.slot.doctor.username}
"""
    )

    return redirect('pending_requests')