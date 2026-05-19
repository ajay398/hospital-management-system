from django import forms
from .models import AvailabilitySlot


class AvailabilitySlotForm(forms.ModelForm):

    class Meta:

        model = AvailabilitySlot

        fields = ['date', 'start_time', 'end_time']