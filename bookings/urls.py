from django.urls import path

from .views import (
    doctor_list,
    available_slots,
    book_slot,
    my_bookings
)

urlpatterns = [

    path('doctors/', doctor_list, name='doctor_list'),

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
]