from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path("appointments", views.AppointmentsListView.as_view(), name="appointments"),
    path("appointments/<int:pk>/create", views.AppointmentCreateView.as_view(), name="create_appointment"),
    path("appointments/<int:pk>/update", views.AppointmentUpdateView.as_view(), name='update_appointment'),
    path("appointments/<int:pk>/delete", views.AppointmentDeleteView.as_view(), name='delete_appointment'),
    path("patients", views.PatientsListView.as_view(), name="patients"),
    path("patients/add", views.PatientCreateView.as_view(), name="add_patient"),
    path("patients/<int:pk>/update", views.patient_profile, name='update_patient'),
    path("patients/<int:pk>/delete", views.PatientDeleteView.as_view(), name='delete_patient'),
    path("doctors", views.DoctorsListView.as_view(), name="doctors"),
    path("doctors/add", views.DoctorCreateView.as_view(), name="add_doctor"),
    path("doctors/<int:pk>/update", views.doctor_profile, name='update_doctor'),
    path("doctors/<int:pk>/delete", views.DoctorDeleteView.as_view(), name='delete_doctor'),
]
