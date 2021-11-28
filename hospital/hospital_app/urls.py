from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("create", views.appointment_create_view, name="create_appointment"),
    path("receptionist_dashboard", views.ReceptionistDashboardListView.as_view(), name="receptionist_dashboard"),
]
