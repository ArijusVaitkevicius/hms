from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path("appointments", views.AppointmentsListView.as_view(), name="appointments"),
    path("my_appointments", views.MyAppointmentsListView.as_view(), name="my_appointments"),
    path('appointments/<int:pk>', views.AppointmentsDetailView.as_view(), name='appointment'),
    path("appointments/<int:pk>/create", views.AppointmentCreateView.as_view(), name="create_appointment"),
    path("appointments/<int:pk>/update", views.AppointmentUpdateView.as_view(), name='update_appointment'),
    path("appointments/<int:pk>/delete", views.AppointmentDeleteView.as_view(), name='delete_appointment'),
    path("patients", views.PatientsListView.as_view(), name="patients"),
    path("my_patients", views.MyPatientsListView.as_view(), name="my_patients"),
    path('patients/<int:pk>', views.PatientsDetailView.as_view(), name='patient'),
    path("patients/add", views.PatientCreateView.as_view(), name="add_patient"),
    path("patients/<int:pk>/update", views.patient_profile, name='update_patient'),
    path("patients/<int:pk>/delete", views.PatientDeleteView.as_view(), name='delete_patient'),
    path("doctors", views.DoctorsListView.as_view(), name="doctors"),
    path('doctors/<int:pk>', views.DoctorsDetailView.as_view(), name='doctor'),
    path("doctors/add", views.DoctorCreateView.as_view(), name="add_doctor"),
    path("doctors/<int:pk>/update", views.doctor_profile, name='update_doctor'),
    path("doctors/<int:pk>/delete", views.DoctorDeleteView.as_view(), name='delete_doctor'),
    path('prescriptions/<int:pk>', views.PrescriptionDetailView.as_view(), name='prescription'),
    path("prescriptions/<int:pk>/create", views.PrescriptionCreateView.as_view(), name="create_prescription"),
    path("prescriptions/<int:pk>/update", views.PrescriptionUpdateView.as_view(), name='update_prescription'),
    path("prescription_line/<int:pk>/delete", views.PrescriptionLineDeleteView.as_view(), name='delete_prescription_line'),
    path("drugs", views.DrugsListView.as_view(), name="drugs"),


    path("drugs/<int:pk>/delete", views.DrugDeleteView.as_view(), name='delete_drug'),
]
