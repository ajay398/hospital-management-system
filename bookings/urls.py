from django.urls import path

from .views import (
    doctor_list,
    available_slots,
    book_slot,
    my_bookings,
    pending_requests,
    approve_booking,
    reject_booking
)

urlpatterns = [

    path(
        'doctors/',
        doctor_list,
        name='doctor_list'
    ),

    path(
        'slots/<int:doctor_id>/',
        available_slots,
        name='available_slots'
    ),

    path(
        'book/<int:slot_id>/',
        book_slot,
        name='book_slot'
    ),

    path(
        'my-bookings/',
        my_bookings,
        name='my_bookings'
    ),

    path(
        'pending-requests/',
        pending_requests,
        name='pending_requests'
    ),

    path(
        'approve-booking/<int:booking_id>/',
        approve_booking,
        name='approve_booking'
    ),

    path(
        'reject-booking/<int:booking_id>/',
        reject_booking,
        name='reject_booking'
    ),
]