from django.db import models
from django.conf import settings

from doctors.models import AvailabilitySlot


class Booking(models.Model):

    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    slot = models.OneToOneField(
        AvailabilitySlot,
        on_delete=models.CASCADE
    )

    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.username} booked {self.slot}"