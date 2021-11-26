from django.contrib import admin
from .models import User, Appointment, Drug, Prescription, PrescriptionLine

admin.site.register(User)
admin.site.register(Appointment)
admin.site.register(Drug)
admin.site.register(Prescription)
admin.site.register(PrescriptionLine)
