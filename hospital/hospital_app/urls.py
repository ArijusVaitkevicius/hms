from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("receptionist_dashboard", views.ReceptionistDashboardListView.as_view(), name="receptionist_dashboard"),
    path("appointments/create", views.AppointmentCreateView.as_view(), name="create_appointment"),
    path("appointments/<int:pk>/update", views.AppointmentUpdateView.as_view(), name='appointment_update'),
]
