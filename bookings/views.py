from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from doctors.models import AvailabilitySlot
from accounts.models import User

from .models import Booking
from django.db import transaction
from .google_calendar import create_calendar_event


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
        is_booked=False
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
    slot=slot
)

    slot.is_booked = True
    slot.save()

    create_calendar_event(slot, request.user)

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