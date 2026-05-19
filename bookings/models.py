from django.db import models

from accounts.models import User
from doctors.models import AvailabilitySlot


class Booking(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    slot = models.ForeignKey(
        AvailabilitySlot,
        on_delete=models.CASCADE
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return f"{self.patient.username} - {self.slot}"