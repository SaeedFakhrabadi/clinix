from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.conf import settings
from django.db.models import Q
from django.utils import timezone
from django.db.models import Avg
from django.core.exceptions import ValidationError

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
    username = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phonenumber = models.CharField(max_length=20, unique=True)

    role = models.CharField(
        max_length=20,
        choices=UserRoles.choices
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now, editable=False)

    def get_full_name(self):
        return self.username  # or combine with other fields later

    def get_short_name(self):
        return self.username

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phonenumber']

    def __str__(self):
        return self.username

class DoctorProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': UserRoles.DOCTOR},
        related_name='doctor_profile'
    )

    field = models.CharField(max_length=150)
    location = models.CharField(max_length=255)
    experience = models.PositiveIntegerField(help_text="Years of experience")
    price = models.PositiveIntegerField()
    score = models.FloatField(default=0)

    start_working_hour = models.TimeField()
    end_working_hour = models.TimeField()

    def average_score_formatted(self):
        return f"{self.score:.1f}" if self.score else "بدون امتیاز"

    def __str__(self):
        return f"Dr. {self.user.username}"

class Reservation(models.Model):

    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='doctor_reservations',
        limit_choices_to={'role': UserRoles.DOCTOR}
    )

    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='patient_reservations',
        limit_choices_to={'role': UserRoles.PATIENT}
    )

    start_reservation_hour = models.DateTimeField()
    end_reservation_hour = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):

        # 1️⃣ start باید قبل از end باشد
        if self.start_reservation_hour >= self.end_reservation_hour:
            raise ValidationError("Start time must be before end time.")

        # 2️⃣ زمان در گذشته نباشد
        # if self.start_reservation_hour < timezone.now():
        #     raise ValidationError("Reservation time cannot be in the past.")

        # 3️⃣ داخل ساعات کاری دکتر باشد
        doctor_profile = self.doctor.doctor_profile

        start_time = self.start_reservation_hour.time()
        end_time = self.end_reservation_hour.time()

        if not (
            doctor_profile.start_working_hour <= start_time and
            end_time <= doctor_profile.end_working_hour
        ):
            raise ValidationError("Reservation time is outside doctor's working hours.")

        # 4️⃣ جلوگیری از overlap
        overlapping = Reservation.objects.filter(
            doctor=self.doctor
        ).filter(
            Q(start_reservation_hour__lt=self.end_reservation_hour) &
            Q(end_reservation_hour__gt=self.start_reservation_hour)
        )

        if self.pk:
            overlapping = overlapping.exclude(pk=self.pk)

        if overlapping.exists():
            raise ValidationError("This time slot is already booked.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.patient} → Dr.{self.doctor} ({self.start_reservation_hour})"

class Comment(models.Model):
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='doctor_comments',
        limit_choices_to={'role': UserRoles.DOCTOR}
    )

    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='patient_comments',
        limit_choices_to={'role': UserRoles.PATIENT}
    )

    # reservation = models.OneToOneField(
    #     Reservation,
    #     on_delete=models.CASCADE
    # )

    score = models.IntegerField()
    comment = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # جلوگیری از mismatch
        # if self.reservation.doctor != self.doctor:
        #     raise ValidationError("Reservation doctor mismatch.")

        # if self.reservation.patient != self.patient:
        #     raise ValidationError("Reservation patient mismatch.")

        if not (1 <= self.score <= 5):
            raise ValidationError("Score must be between 1 and 5.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

        # Update doctor score
        avg_score = Comment.objects.filter(
            doctor=self.doctor
        ).aggregate(avg=Avg('score'))['avg']

        profile = self.doctor.doctor_profile
        profile.score = avg_score or 0
        profile.save()

class PasswordReset(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='password_resets'
    )
    verificationCode = models.PositiveIntegerField()
    created_when = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_when']
        indexes = [
            models.Index(fields=['user', 'verificationCode']),
        ]

    def __str__(self):
        return f"Reset for {self.user} - {self.verificationCode}"

    @property
    def is_expired(self):
        return timezone.now() > self.created_when + timezone.timedelta(minutes=2)
    
