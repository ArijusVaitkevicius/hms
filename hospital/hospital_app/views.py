from django.shortcuts import render, redirect
from .forms import AppointmentForm, CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Appointment, CustomUser
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
User = get_user_model()


def home(request):
    return render(request, 'home.html')


class AppointmentsListView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = 'appointments.html'
    context_object_name = 'appointments_list'
    paginate_by = 10
    ordering = 'date', 'time'
    queryset = Appointment.objects.filter(status='P')


class AppointmentCreateView(LoginRequiredMixin, CreateView):
    model = Appointment
    success_url = "/appointments"
    template_name = 'create_appointment.html'
    form_class = AppointmentForm


class AppointmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Appointment
    success_url = "/appointments"
    template_name = 'update_appointment.html'
    form_class = AppointmentForm


class PatientsListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'patients.html'
    context_object_name = 'patients_list'
    paginate_by = 10
    queryset = User.objects.filter(user_type='P')


class PatientCreateView(LoginRequiredMixin, CreateView):
    model = CustomUser
    success_url = "/patients"
    template_name = 'add_patient.html'
    form_class = CustomUserCreationForm

    def get_initial(self):
        initial = super(PatientCreateView, self).get_initial()
        initial.update({'user_type': 'P'})

        return initial


