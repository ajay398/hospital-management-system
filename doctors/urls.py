from django.urls import path

from .views import (
    create_slot,
    doctor_slots,
    delete_slot
)

urlpatterns = [

    path('create-slot/', create_slot, name='create_slot'),

    path('my-slots/', doctor_slots, name='doctor_slots'),

    path(
        'delete-slot/<int:slot_id>/',
        delete_slot,
        name='delete_slot'
    ),
]