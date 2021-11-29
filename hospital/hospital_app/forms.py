from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Appointment
from django import forms
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    #
    # def __init__(self, *args, **kwargs):
    #     super(CustomUserCreationForm, self).__init__(*args, **kwargs)
    #     self.fields['user_type'].widget.attrs['disabled'] = 'disabled'

    class Meta:
        model = CustomUser
        fields = ('email', 'user_type')




class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)


def working_hours():
    start = datetime.strptime('08:00', '%H:%M')
    end = datetime.strptime('20:00', '%H:%M')
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


CHOICES = working_hours()


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['patient'].queryset = User.objects.filter(user_type="P")
            self.fields['doctor'].queryset = User.objects.filter(user_type="D")
            self.fields["date"].label = "Date (YYYY-MM-DD)"
            self.fields["time"] = forms.ChoiceField(choices=CHOICES)
