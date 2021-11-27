from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Appointment, Drug, Prescription, PrescriptionLine


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'user_type')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'user_type')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('date', 'time', 'status', 'patient', 'doctor')
    list_filter = ('date', 'status', 'patient', 'doctor')


class PrescriptionLineInline(admin.TabularInline):
    model = PrescriptionLine
    extra = 0


class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('date', 'expiration', 'doctor', 'patient')
    inlines = [PrescriptionLineInline]


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Drug)
admin.site.register(Prescription, PrescriptionAdmin)
admin.site.register(PrescriptionLine)
