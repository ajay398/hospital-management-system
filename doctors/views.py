from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import AvailabilitySlot
from .forms import AvailabilitySlotForm


@login_required
def create_slot(request):

    if request.user.role != 'doctor':
        return redirect('dashboard')

    if request.method == 'POST':

        form = AvailabilitySlotForm(request.POST)

        if form.is_valid():

            slot = form.save(commit=False)

            slot.doctor = request.user

            slot.save()

            return redirect('doctor_slots')

    else:

        form = AvailabilitySlotForm()

    return render(request, 'doctors/create_slot.html', {'form': form})


@login_required
def doctor_slots(request):

    if request.user.role != 'doctor':
        return redirect('dashboard')

    slots = AvailabilitySlot.objects.filter(
        doctor=request.user
    ).order_by('-date')

    return render(
        request,
        'doctors/doctor_slots.html',
        {'slots': slots}
    )


@login_required
def delete_slot(request, slot_id):

    if request.user.role != 'doctor':
        return redirect('dashboard')

    slot = AvailabilitySlot.objects.get(
        id=slot_id,
        doctor=request.user
    )

    slot.delete()

    return redirect('doctor_slots')