from django.shortcuts import render, redirect
from .forms import AppointmentForm, CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Appointment, CustomUser, Profile
from .forms import CustomUserChangeForm, ProfileUpdateForm, DoctorProfileUpdateForm, PatientProfileUpdateForm, \
    PatientCustomUserChangeForm
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


@login_required
def doctor_profile(request, pk):
    user = User.objects.get(pk=pk)
    doc_profile = Profile.objects.get(user=user)
    if request.method == "POST":
        u_form = CustomUserChangeForm(request.POST, instance=user)
        p_form = DoctorProfileUpdateForm(request.POST, request.FILES, instance=doc_profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Profile updated")
            return redirect('doctors')
    else:
        u_form = CustomUserChangeForm(instance=user)
        p_form = DoctorProfileUpdateForm(instance=doc_profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        # 'user': user,
    }
    return render(request, 'update_profile.html', context)


@login_required
def patient_profile(request, pk):
    user = User.objects.get(pk=pk)
    pat_profile = Profile.objects.get(user=user)
    if request.method == "POST":
        u_form = PatientCustomUserChangeForm(request.POST, instance=user)
        p_form = PatientProfileUpdateForm(request.POST, request.FILES, instance=pat_profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Profile updated")
            return redirect('patients')
    else:
        u_form = PatientCustomUserChangeForm(instance=user)
        p_form = PatientProfileUpdateForm(instance=pat_profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        # 'user': user,
    }
    return render(request, 'update_profile.html', context)


# @login_required
# def create_appointment(request, pk):
#     user = User.objects.get(pk=pk)
#     if request.method == "POST":
#         form = AppointmentForm(request.POST, instance=user)
#         if form.is_valid():
#             form.save()
#             messages.success(request, f"Appointment created")
#             return redirect('patients')
#     else:
#         form = AppointmentForm(instance=user)
#
#     context = {
#         'u_form': form,
#     }
#     return render(request, 'create_appointment.html', context)


class AppointmentsListView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = 'appointments.html'
    context_object_name = 'appointments_list'
    paginate_by = 10
    ordering = 'date', 'time'
    queryset = Appointment.objects.filter(status='P')


class AppointmentsDetailView(LoginRequiredMixin, DetailView):
    model = Appointment
    template_name = 'appointment.html'


class AppointmentCreateView(LoginRequiredMixin, CreateView):
    model = Appointment
    success_url = "/appointments"
    template_name = 'create_appointment.html'
    form_class = AppointmentForm

    def get_initial(self):
        initial = super(AppointmentCreateView, self).get_initial()
        initial.update({'patient': User.objects.get(pk=self.kwargs['pk'])})
        initial.update({'doctor': User.objects.get(pk=self.kwargs['pk']).my_doctor})
        AppointmentForm.timeslot = User.objects.get(pk=self.kwargs['pk']).my_doctor.profile.shift

        return initial


class AppointmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Appointment
    success_url = "/appointments"
    template_name = 'update_appointment.html'
    form_class = AppointmentForm

    def get_initial(self):
        new_pk = str(Appointment.objects.get(pk=self.kwargs['pk']).patient.pk)
        initial = super(AppointmentUpdateView, self).get_initial()
        initial.update({'patient': User.objects.get(pk=new_pk)})
        initial.update({'doctor': User.objects.get(pk=new_pk).my_doctor})
        AppointmentForm.timeslot = User.objects.get(pk=new_pk).my_doctor.profile.shift

        return initial


class AppointmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Appointment
    success_url = "/appointments"
    template_name = 'delete_appointment.html'


class PatientsListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'patients.html'
    context_object_name = 'patients_list'
    paginate_by = 10
    queryset = User.objects.filter(user_type='P')


class PatientsDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'patient.html'


class PatientCreateView(LoginRequiredMixin, CreateView):
    model = CustomUser
    success_url = "/patients"
    template_name = 'add_patient.html'
    form_class = CustomUserCreationForm

    def get_initial(self):
        initial = super(PatientCreateView, self).get_initial()
        initial.update({'user_type': 'P'})

        return initial


class PatientDeleteView(LoginRequiredMixin, DeleteView):
    model = CustomUser
    success_url = "/patients"
    template_name = 'delete_patient.html'


class DoctorsListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'doctors.html'
    context_object_name = 'doctors_list'
    paginate_by = 10
    queryset = User.objects.filter(user_type='D')


class DoctorsDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'doctor.html'


class DoctorCreateView(LoginRequiredMixin, CreateView):
    model = CustomUser
    success_url = "/doctors"
    template_name = 'add_doctor.html'
    form_class = CustomUserCreationForm

    def get_initial(self):
        initial = super(DoctorCreateView, self).get_initial()
        initial.update({'user_type': 'D'})

        return initial


class DoctorDeleteView(LoginRequiredMixin, DeleteView):
    model = CustomUser
    success_url = "/doctors"
    template_name = 'delete_doctor.html'
