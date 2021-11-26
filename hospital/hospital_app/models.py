from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USER_CHOICES = [
        ('D', 'Doctor'),
        ('P', 'Patient'),
        ('R', 'Receptionist')
    ]

    user_type = models.CharField(choices=USER_CHOICES, max_length=1)

    def is_doctor(self):
        if self.user_type == 'D':
            return True
        else:
            return False

    def is_patient(self):
        if self.user_type == 'P':
            return True
        else:
            return False

    def is_receptionist(self):
        if self.user_type == 'R':
            return True
        else:
            return False

    class Meta:
        ordering = ('id',)


class Appointment(models.Model):
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

    APPOINTMENT_STATUS = (
        ('P', 'Pending'),
        ('C', 'Completed'),
        ('X', 'Cancelled'),
    )

    status = models.CharField(choices=APPOINTMENT_STATUS, max_length=1, default='P')
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor')

    class Meta:
        verbose_name = 'Appointment'
        verbose_name_plural = 'Appointments'


class Drug(models.Model):
    name = models.CharField('Name', max_length=200)

    class Meta:
        verbose_name = 'Drug'
        verbose_name_plural = 'Drugs'


class Prescription(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='doctor_prescription')
    patient = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='patient_prescription')
    date = models.DateField(auto_now_add=True)
    expiration = models.DateField('Expiration date', null=True, blank=True)
    symptoms = models.TextField('Symptoms', max_length=200)
    diagnosis = models.TextField('Diagnosis', max_length=1000)

    class Meta:
        verbose_name = 'Prescription'
        verbose_name_plural = 'Prescriptions'


class PrescriptionLine(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.SET_NULL, null=True)
    drugs = models.ForeignKey(Drug, on_delete=models.SET_NULL, null=True)
    qty = models.IntegerField('Quantity')

    class Meta:
        verbose_name = 'Prescription line'
        verbose_name_plural = 'Prescription lines'
