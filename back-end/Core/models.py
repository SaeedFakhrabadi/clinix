from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.conf import settings
import uuid
from django.utils import timezone

class UserRoles(models.TextChoices):
    PATIENT = "PATIENT", "Patient"
    DOCTOR  = "DOCTOR",  "Doctor"
    ADMIN   = "ADMIN",   "Admin"

class UserManager(BaseUserManager):
    def create_user(self, username, email, phonenumber, password=None, role=UserRoles.PATIENT, **extra_fields):
        if not username:
            raise ValueError("Users must have a username")
        if not email:
            raise ValueError("Users must have an email")
        if not phonenumber:
            raise ValueError("Users must have a phone number")

        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            phonenumber=phonenumber,
            role=role,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, phonenumber, password=None, **extra_fields):
        extra_fields.setdefault('role', UserRoles.ADMIN)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('role') != UserRoles.ADMIN:
            raise ValueError("Superuser must have role=ADMIN")
        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(username, email, phonenumber, password, **extra_fields)
    
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    phonenumber = models.CharField(max_length=20, unique=True)

    role = models.CharField(
        max_length=20,
        choices=UserRoles.choices
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phonenumber']

    def __str__(self):
        return self.username

class WorkingHour(models.Model):
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': UserRoles.DOCTOR},
        related_name='working_hours'
    )
    day_of_week = models.IntegerField(
        choices=[(i, day) for i, day in enumerate(
            ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        )]
    )
    start_time  = models.TimeField()
    end_time    = models.TimeField()
    is_available = models.BooleanField(default=True)

class DoctorService(models.Model):
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': UserRoles.DOCTOR}
    )
    name = models.CharField(max_length=150)           # e.g. "Check-up", "Surgery consult"
    price = models.PositiveIntegerField()
    
class PasswordReset(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='password_resets'
    )
    verification_code = models.PositiveIntegerField()
    created_when = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_when']
        indexes = [
            models.Index(fields=['user', 'verification_code']),
        ]

    def __str__(self):
        return f"Reset for {self.user} - {self.verificationCode}"

    @property
    def is_expired(self):
        return timezone.now() > self.created_when + timezone.timedelta(minutes=2)

class Appointment(models.Model):

    class Status(models.TextChoices):
        PENDING   = "PENDING",   "Pending"
        CONFIRMED = "CONFIRMED", "Confirmed"
        CANCELED  = "CANCELED",  "Canceled"

    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="patient_appointments",
        limit_choices_to={'role': UserRoles.PATIENT},
    )

    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="doctor_appointments",
        limit_choices_to={'role': UserRoles.DOCTOR},
    )

    appointment_time = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient} → Dr. {self.doctor} at {self.appointment_time}"

class Payment(models.Model):
    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.CASCADE
    )
    amount = models.PositiveIntegerField()
    is_paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(null=True, blank=True)
