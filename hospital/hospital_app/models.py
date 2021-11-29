from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.contrib.auth import get_user_model
from PIL import Image


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email address', unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USER_CHOICES = [
        ('D', 'Doctor'),
        ('P', 'Patient'),
        ('R', 'Receptionist')
    ]

    user_type = models.CharField(choices=USER_CHOICES, max_length=1)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

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

    def __str__(self):
        return self.email


User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(default="default.png", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user} profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.photo.path)
        if img.height > 200 or img.width > 200:
            output_size = (200, 200)
            img.thumbnail(output_size)
            img.save(self.photo.path)


class Appointment(models.Model):
    date = models.DateField()
    time = models.TimeField()

    APPOINTMENT_STATUS = (
        ('P', 'Pending'),
        ('C', 'Completed'),
        ('X', 'Cancelled'),
    )

    status = models.CharField(choices=APPOINTMENT_STATUS, max_length=1, default='P')
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_appointment')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_appointment')

    def __str__(self):
        return f'{self.date} Doctor: {self.doctor} Patient: {self.patient}'

    class Meta:
        verbose_name = 'Appointment'
        verbose_name_plural = 'Appointments'


class Drug(models.Model):
    name = models.CharField('Name', max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Drug'
        verbose_name_plural = 'Drugs'


class Prescription(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_prescription')
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_prescription')
    date = models.DateField(auto_now_add=True)
    expiration = models.DateField('Expiration date', null=True, blank=True)
    symptoms = models.TextField('Symptoms', max_length=200)
    diagnosis = models.TextField('Diagnosis', max_length=1000)

    def __str__(self):
        return f'prescription id:{self.pk} for {self.patient}'

    class Meta:
        verbose_name = 'Prescription'
        verbose_name_plural = 'Prescriptions'


class PrescriptionLine(models.Model):
    prescription = models.ForeignKey(Prescription,
                                     on_delete=models.SET_NULL,
                                     null=True,
                                     related_name='prescription_line')
    drugs = models.ForeignKey(Drug, on_delete=models.SET_NULL, null=True, related_name='drug_line')
    qty = models.IntegerField('Quantity')

    def __str__(self):
        return f'line id:{self.pk} {self.prescription}'

    class Meta:
        verbose_name = 'Prescription line'
        verbose_name_plural = 'Prescription lines'
