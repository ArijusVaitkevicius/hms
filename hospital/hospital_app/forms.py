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


class AppointmentForm(forms.ModelForm):
    time_choices = [('select_time', 'select_time')]
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
            self.fields['time'] = forms.ChoiceField(choices=self.time_choices)
            # self.initial['time'] = self.timestamp[:5]
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
