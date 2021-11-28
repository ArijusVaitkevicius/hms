from django.shortcuts import render, redirect
from .forms import AppointmentForm
from django.contrib.auth.decorators import login_required
from .models import Appointment
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
User = get_user_model()


def home(request):
    return render(request, 'home.html')


class ReceptionistDashboardListView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = 'receptionist_dashboard.html'
    context_object_name = 'appointments_list'
    paginate_by = 10
    ordering = 'date', 'time'
    queryset = Appointment.objects.filter(status='P')


class AppointmentCreateView(LoginRequiredMixin, CreateView):
    model = Appointment
    success_url = "/receptionist_dashboard"
    template_name = 'create_appointment.html'
    form_class = AppointmentForm


class AppointmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Appointment
    success_url = "/receptionist_dashboard"
    template_name = 'update_appointment.html'
    form_class = AppointmentForm
