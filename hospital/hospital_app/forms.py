from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Appointment, Profile
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
    class Meta:
        model = CustomUser
        fields = ('email',)


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
        fields = ['name', 'surname', 'phone',  'birth_date', 'address', 'photo', 'shift']
        widgets = {
            'birth_date': DateInput(attrs={'type': 'date'}),
        }


class PatientProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'surname', 'phone',  'birth_date', 'address', 'photo', 'blood_group']
        widgets = {
            'birth_date': DateInput(attrs={'type': 'date'}),
        }


def working_hours(st, en):
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


# CHOICES = working_hours('08:00', '10:00')


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = '__all__'
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['patient'].queryset = User.objects.filter(user_type="P")
            self.fields['doctor'].queryset = User.objects.filter(user_type="D")
            self.fields["time"] = forms.ChoiceField(choices=working_hours('08:00', '12:00'))
