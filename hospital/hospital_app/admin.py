from django.contrib import admin
from .models import User, Appointment, Drug, Prescription, PrescriptionLine


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('date', 'time', 'status', 'patient', 'doctor')
    list_filter = ('date', 'status', 'patient', 'doctor')


class PrescriptionLineInline(admin.TabularInline):
    model = PrescriptionLine
    extra = 0


class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('date', 'expiration', 'doctor', 'patient')
    inlines = [PrescriptionLineInline]


admin.site.register(User)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Drug)
admin.site.register(Prescription, PrescriptionAdmin)
admin.site.register(PrescriptionLine)
