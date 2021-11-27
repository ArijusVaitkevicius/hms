from django.shortcuts import render, redirect
from .forms import AppointmentForm
from django.contrib.auth.decorators import login_required
from .models import Appointment


def home(request):
    return render(request, 'home.html')


@login_required(login_url='/login/')
def appointment_create_view(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.save()
            return redirect('receptionist_dashboard')
    else:
        form = AppointmentForm()
    return render(request, 'create_appointment.html', {'form': form})


@login_required(login_url='/login/')
def receptionist_dashboard(request):
    if request.method == "GET" and request.user.user_type == "R":
        context = {
            "totalApp": len(Appointment.objects.all()),
            "compApp": len(Appointment.objects.filter(status="C")),
            "pendApp": len(Appointment.objects.filter(status="P")),
            "app_list": Appointment.objects.all(),
        }
        return render(request, 'receptionist_dashboard.html', context=context)
