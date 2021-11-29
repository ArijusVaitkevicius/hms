from django.apps import AppConfig


class HospitalAppConfig(AppConfig):
    name = 'hospital_app'

    def ready(self):
        from .signals import create_profile, save_profile
