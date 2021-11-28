from django.shortcuts import render, redirect
from .forms import AppointmentForm
from django.contrib.auth.decorators import login_required
from .models import Appointment
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin


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


class ReceptionistDashboardListView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = 'receptionist_dashboard.html'
    context_object_name = 'appointments_list'
    paginate_by = 10
    ordering = 'date', 'time'


