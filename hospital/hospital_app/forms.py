from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField
from .models import CustomUser, Appointment, Profile, Prescription, PrescriptionLine, Drug
from django import forms
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from django.forms.widgets import DateInput

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['user_type'].widget.attrs['disabled'] = 'disabled'

    class Meta:
        model = CustomUser
        fields = ('email', 'user_type')


class CustomUserChangeForm(UserChangeForm):
    password = None

    class Meta:
        model = CustomUser
        fields = ('email',)


class PatientCustomUserChangeForm(UserChangeForm):
    password = None

    class Meta:
        model = CustomUser
        fields = ('email', 'my_doctor')


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo']
        widgets = {
            'date': DateInput(attrs={'type': 'birth_date'}),
        }


class DoctorProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'surname', 'phone', 'birth_date', 'address', 'photo', 'shift']
        widgets = {
            'birth_date': DateInput(attrs={'type': 'date'}),
        }


class PatientProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'surname', 'phone', 'birth_date', 'address', 'photo', 'blood_group']
        widgets = {
            'birth_date': DateInput(attrs={'type': 'date'}),
        }


def working_hours(timeslot):
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

    for t in time:
        one_tuple = (t, t)
        choices.append(one_tuple)

    return choices


class AppointmentForm(forms.ModelForm):
    timeslot = ''
    timestamp = ''
    doc = ''

    class Meta:
        model = Appointment
        fields = ['date', 'time', 'status', 'patient', 'doctor', 'complaint']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['time'] = forms.ChoiceField(choices=working_hours(self.timeslot))
            self.initial['time'] = self.timestamp[:5]
            self.fields['patient'].widget.attrs['disabled'] = 'disabled'
            self.fields['doctor'].widget.attrs['disabled'] = 'disabled'


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['patient', 'doctor', 'expiration', 'symptoms', 'diagnosis']
        widgets = {
            'expiration': DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(PrescriptionForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['patient'].widget.attrs['disabled'] = 'disabled'
            self.fields['doctor'].widget.attrs['disabled'] = 'disabled'


class PrescriptionLineForm(forms.ModelForm):
    class Meta:
        model = PrescriptionLine
        fields = ['prescription', 'drugs', 'qty']
        widgets = {'prescription': forms.HiddenInput()}


class DrugForm(forms.ModelForm):
    class Meta:
        model = Drug
        fields = ['name']
