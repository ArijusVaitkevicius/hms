import simplejson as simplejson
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.views.generic.edit import FormMixin
import json
from .forms import AppointmentForm, CustomUserCreationForm, DrugForm
from django.contrib.auth.decorators import login_required
from .models import Appointment, CustomUser, Profile, Prescription, PrescriptionLine, Drug
from .forms import CustomUserChangeForm, ProfileUpdateForm, DoctorProfileUpdateForm, PatientProfileUpdateForm, \
    PatientCustomUserChangeForm, PrescriptionForm, PrescriptionLineForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.views.generic.list import MultipleObjectMixin
from .filters import AppointmentFilter, PatientFilter, DoctorFilter, MyAppointmentFilter, DrugsFilter
from datetime import date
from extra_views import InlineFormSetFactory, CreateWithInlinesView, UpdateWithInlinesView
from datetime import datetime, timedelta

User = get_user_model()


def home(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'R':
            appointments = Appointment.objects.all().order_by('-id')[:5]
            patients = User.objects.all().filter(user_type='P').order_by('-id')[:3]
            doctors = User.objects.all().filter(user_type='D').order_by('-id')[:3]

            context = {'appointments': appointments, 'patients': patients, 'doctors': doctors}

            return render(request, 'receptionist_home.html', context)

        elif request.user.user_type == 'D':
            completed_appointments = Appointment.objects.filter(status='C', doctor=request.user).order_by('-date',
                                                                                                          '-time')[:5]
            pending_appointments = Appointment.objects.filter(status='P', doctor=request.user,
                                                              date=date.today()).order_by('date', 'time')

            context = {'completed_appointments': completed_appointments, 'pending_appointments': pending_appointments}

            return render(request, 'doctor_home.html', context)

        elif request.user.user_type == 'P':
            return render(request, 'patient_home.html')

    else:
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


class AppointmentsListView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = 'appointments.html'

    def get_context_data(self, **kwargs):
        context = super(AppointmentsListView, self).get_context_data(**kwargs)
        appointments_list = Appointment.objects.all()
        my_filter = AppointmentFilter(self.request.GET, queryset=appointments_list)
        appointments_list = my_filter.qs
        context['my_filter'] = my_filter
        context['appointments_list'] = appointments_list

        return context


class MyAppointmentsListView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = 'appointments.html'

    def get_context_data(self, **kwargs):
        context = super(MyAppointmentsListView, self).get_context_data(**kwargs)
        appointments_list = Appointment.objects.filter(doctor=self.request.user).order_by('-date', '-time')
        my_filter = MyAppointmentFilter(self.request.GET, queryset=appointments_list)
        appointments_list = my_filter.qs
        context['my_filter'] = my_filter
        context['appointments_list'] = appointments_list

        return context


class AppointmentsDetailView(LoginRequiredMixin, DetailView):
    model = Appointment
    template_name = 'appointment.html'


def working_hours(timeslot, picked):
    if timeslot == '0':
        st = '08:00'
        en = '12:00'
    elif timeslot == '1':
        st = '10:00'
        en = '14:00'
    elif timeslot == '2':
        st = '12:00'
        en = '16:00'
    elif timeslot == '3':
        st = '14:00'
        en = '18:00'
    elif timeslot == '4':
        st = '16:00'
        en = '20:00'
    else:
        st = '00:00'
        en = '00:00'

    start = datetime.strptime(st, '%H:%M')
    end = datetime.strptime(en, '%H:%M')

    seq = [start]

    while seq[-1] < end:
        start = start + timedelta(minutes=30)
        seq.append(start)

    time = []

    for s in seq:
        corrected = datetime.strftime(s, '%m/%d/%Y %H:%M')
        time.append(corrected[-5:])

    choices = []

    new_picked = []

    for new in picked:
        new_picked.append(str(new))

    for t in time:
        if t not in picked:
            # one_tuple = (t, t)
            choices.append(t)
        else:
            continue

    return choices


def filter_times(request):
    if request.method == "POST":
        times = {}

        picked_time_dict = Appointment.objects.filter(doctor=User.objects.get(pk=request.POST['doctor']), date=request.POST['date']).values('time')

        picked_times = []

        for dct in picked_time_dict:
            picked_times.append(dct.get('time').strftime("%H:%M"))

        timeslot = User.objects.get(pk=request.POST['doctor']).profile.shift

        filtered_times = working_hours(timeslot, picked_times)
        filtered_times.reverse()

        for time in filtered_times:
            times[time] = time

        return HttpResponse(json.dumps(times), content_type='application/json')


class AppointmentCreateView(LoginRequiredMixin, CreateView):
    model = Appointment
    success_url = "/appointments"
    template_name = 'appointment_form.html'
    form_class = AppointmentForm

    def get_initial(self):
        initial = super(AppointmentCreateView, self).get_initial()
        initial.update({'patient': User.objects.get(pk=self.kwargs['pk'])})
        initial.update({'doctor': User.objects.get(pk=self.kwargs['pk']).my_doctor})

        return initial


class AppointmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Appointment
    success_url = "/appointments"
    template_name = 'appointment_form.html'
    form_class = AppointmentForm

    def get_initial(self):
        initial = super(AppointmentUpdateView, self).get_initial()
        initial.update({'patient': User.objects.get(pk=self.kwargs['pk'])})
        initial.update({'doctor': User.objects.get(pk=self.kwargs['pk']).my_doctor})

        AppointmentForm.timeslot = User.objects.get(pk=self.kwargs['pk']).my_doctor.profile.shift
        AppointmentForm.timestamp = str(Appointment.objects.get(pk=self.kwargs['pk']).time)

        return initial


class AppointmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Appointment
    success_url = "/appointments"
    template_name = 'delete_appointment.html'


class PatientsListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'patients.html'

    def get_context_data(self, **kwargs):
        context = super(PatientsListView, self).get_context_data(**kwargs)
        patients_list = User.objects.filter(user_type='P')
        my_filter = PatientFilter(self.request.GET, queryset=patients_list)
        patients_list = my_filter.qs
        context['my_filter'] = my_filter
        context['patients_list'] = patients_list

        return context


class MyPatientsListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'patients.html'

    def get_context_data(self, **kwargs):
        context = super(MyPatientsListView, self).get_context_data(**kwargs)
        patients_list = User.objects.filter(user_type='P', my_doctor=self.request.user)
        my_filter = PatientFilter(self.request.GET, queryset=patients_list)
        patients_list = my_filter.qs
        context['my_filter'] = my_filter
        context['patients_list'] = patients_list

        return context


class PatientsDetailView(LoginRequiredMixin, DetailView, MultipleObjectMixin):
    model = User
    template_name = 'patient.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        object_list = Prescription.objects.filter(patient=self.get_object()).order_by('-expiration', )
        context = super(PatientsDetailView, self).get_context_data(object_list=object_list, **kwargs)

        return context


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


    def get_context_data(self, **kwargs):
        context = super(DoctorsListView, self).get_context_data(**kwargs)
        doctors_list = User.objects.filter(user_type='D')
        my_filter = DoctorFilter(self.request.GET, queryset=doctors_list)
        doctors_list = my_filter.qs
        context['my_filter'] = my_filter
        context['doctors_list'] = doctors_list

        return context


class DoctorsDetailView(LoginRequiredMixin, DetailView, MultipleObjectMixin):
    model = User
    template_name = 'doctor.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        object_list = Appointment.objects.filter(doctor=self.get_object())
        context = super(DoctorsDetailView, self).get_context_data(object_list=object_list, **kwargs)

        return context


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


class PrescriptionInline(InlineFormSetFactory):
    model = PrescriptionLine
    fields = ['drugs', 'qty']


class PrescriptionDetailView(FormMixin, LoginRequiredMixin, DetailView):
    model = Prescription
    template_name = 'prescription.html'
    form_class = PrescriptionLineForm

    def get_success_url(self):
        return reverse('prescription', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        object_list = PrescriptionLine.objects.filter(prescription=self.get_object())
        context = super(PrescriptionDetailView, self).get_context_data(object_list=object_list, **kwargs)
        context['form'] = PrescriptionLineForm(initial={'prescription': self.object})

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.prescription = self.object
        form.save()
        return super(PrescriptionDetailView, self).form_valid(form)


class PrescriptionCreateView(LoginRequiredMixin, CreateWithInlinesView):
    model = Prescription
    inlines = [PrescriptionInline, ]
    template_name = 'prescription_form.html'
    form_class = PrescriptionForm

    def get_success_url(self):
        return reverse('prescription', kwargs={'pk': self.object.id})

    def get_initial(self):
        initial = super(PrescriptionCreateView, self).get_initial()
        initial.update({'patient': User.objects.get(pk=self.kwargs['pk'])})
        initial.update({'doctor': User.objects.get(pk=self.kwargs['pk']).my_doctor})

        return initial


class PrescriptionUpdateView(LoginRequiredMixin, UpdateWithInlinesView):
    model = Prescription
    inlines = [PrescriptionInline, ]
    template_name = 'prescription_form.html'
    form_class = PrescriptionForm

    def get_success_url(self):
        return reverse('prescription', kwargs={'pk': self.object.id})

    def get_initial(self):
        initial = super(PrescriptionUpdateView, self).get_initial()
        initial.update({'patient': User.objects.get(pk=self.kwargs['pk'])})
        initial.update({'doctor': User.objects.get(pk=self.kwargs['pk']).my_doctor})

        return initial


class PrescriptionLineDeleteView(LoginRequiredMixin, DeleteView):
    model = PrescriptionLine
    template_name = 'delete_prescription_line.html'

    def get_success_url(self):
        return reverse('prescription',
                       kwargs={'pk': PrescriptionLine.objects.get(pk=self.kwargs['pk']).prescription.pk})


class DrugsListView(LoginRequiredMixin, ListView, FormMixin):
    model = Drug
    template_name = 'drugs.html'
    form_class = DrugForm
    success_url = "/drugs"

    def get_context_data(self, **kwargs):
        context = super(DrugsListView, self).get_context_data(**kwargs)
        drugs_list = Drug.objects.all()
        my_filter = DrugsFilter(self.request.GET, queryset=drugs_list)
        drugs_list = my_filter.qs
        context['form'] = DrugForm
        context['my_filter'] = my_filter
        context['drugs_list'] = drugs_list

        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super(DrugsListView, self).form_valid(form)


class DrugDeleteView(LoginRequiredMixin, DeleteView):
    model = Drug
    template_name = 'delete_drug.html'
    success_url = "/drugs"
