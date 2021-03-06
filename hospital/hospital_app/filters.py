import django_filters
from .models import *
from django.forms.widgets import DateInput


class AppointmentFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(label='Date from', widget=DateInput(attrs={'type': 'date'}),
                                           field_name='date', lookup_expr='gte')
    end_date = django_filters.DateFilter(label='Date to', widget=DateInput(attrs={'type': 'date'}), field_name='date',
                                         lookup_expr='lte')
    patient_email = django_filters.CharFilter(label='Patient email', field_name='patient__email',
                                              lookup_expr='icontains')
    doctor_email = django_filters.CharFilter(label='Doctor email', field_name='doctor__email', lookup_expr='icontains')

    class Meta:
        model = Appointment
        fields = ['status']
        exclude = ['complaint', 'date', 'time']


class MyAppointmentFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(label='Date from', widget=DateInput(attrs={'type': 'date'}),
                                           field_name='date', lookup_expr='gte')
    end_date = django_filters.DateFilter(label='Date to', widget=DateInput(attrs={'type': 'date'}), field_name='date',
                                         lookup_expr='lte')
    patient_email = django_filters.CharFilter(label='Patient email', field_name='patient__email',
                                              lookup_expr='icontains')
    patient_name = django_filters.CharFilter(label='Patient name', field_name='patient__profile__name',
                                             lookup_expr='icontains')
    patient_surname = django_filters.CharFilter(label='Patient surname', field_name='patient__profile__surname',
                                                lookup_expr='icontains')

    class Meta:
        model = Appointment
        fields = ['status']
        exclude = ['complaint', 'date', 'time']


class PatientFilter(django_filters.FilterSet):
    email = django_filters.CharFilter(label='Email', field_name='email', lookup_expr='icontains')
    name = django_filters.CharFilter(label='Name', field_name='profile__name', lookup_expr='icontains')
    surname = django_filters.CharFilter(label='Surname', field_name='profile__surname', lookup_expr='icontains')

    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'surname']


class DoctorFilter(django_filters.FilterSet):
    email = django_filters.CharFilter(label='Email', field_name='email', lookup_expr='icontains')
    name = django_filters.CharFilter(label='Name', field_name='profile__name', lookup_expr='icontains')
    surname = django_filters.CharFilter(label='Surname', field_name='profile__surname', lookup_expr='icontains')

    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'surname']


class DrugsFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(label='Drug name', field_name='name', lookup_expr='icontains')

    class Meta:
        model = Drug
        fields = ['name']
