from django.shortcuts import render, redirect
from .forms import AppointmentForm, CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Appointment, CustomUser
from .forms import CustomUserChangeForm, ProfileUpdateForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib import messages
User = get_user_model()


def home(request):
    return render(request, 'home.html')


@login_required
def profile(request):
    if request.method == "POST":
        u_form = CustomUserChangeForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Profile updated")
            return redirect('profile')
    else:
        u_form = CustomUserChangeForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'profile.html', context)


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


class DoctorsListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'doctors.html'
    context_object_name = 'doctors_list'
    paginate_by = 10
    queryset = User.objects.filter(user_type='D')


class DoctorCreateView(LoginRequiredMixin, CreateView):
    model = CustomUser
    success_url = "/doctors"
    template_name = 'add_doctor.html'
    form_class = CustomUserCreationForm

    def get_initial(self):
        initial = super(DoctorCreateView, self).get_initial()
        initial.update({'user_type': 'D'})

        return initial

