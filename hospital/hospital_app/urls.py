from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("appointments", views.AppointmentsListView.as_view(), name="appointments"),
    path("appointments/create", views.AppointmentCreateView.as_view(), name="create_appointment"),
    path("appointments/<int:pk>/update", views.AppointmentUpdateView.as_view(), name='appointment_update'),
    path("patients", views.PatientsListView.as_view(), name="patients"),
    path("patients/add", views.PatientCreateView.as_view(), name="add_patient"),
]
