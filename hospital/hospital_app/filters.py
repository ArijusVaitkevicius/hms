import django_filters
from django_filters import DateFilter, CharFilter
from .models import *


class AppointmentFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name='date', lookup_expr='gte')
    end_date = DateFilter(field_name='date', lookup_expr='lte')
    patient_email = django_filters.CharFilter(field_name='patient__email', lookup_expr='icontains')
    doctor_email = django_filters.CharFilter(field_name='doctor__email', lookup_expr='icontains')

    class Meta:
        model = Appointment
        fields = ['status']
        exclude = ['complaint', 'date', 'time']

