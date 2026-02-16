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

class NotificationType(models.TextChoices):
    RESERVE = "RESERVE", "رزرو نوبت"
    CANCEL  = "CANCEL",  "لغو نوبت"

class TransactionType(models.TextChoices):
    PAY    = "PAY",    "پرداخت"
    REFUND = "REFUND", "بازگشت وجه"

class TransactionMethod(models.TextChoices):
    BANK   = "BANK",   "درگاه بانکی"
    WALLET = "WALLET", "کیف پول"

class TransactionStatus(models.TextChoices):
    SUCCESS = "SUCCESS", "موفق"
    FAILED  = "FAILED",  "ناموفق"
    PENDING = "PENDING", "در انتظار"

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
        if self.start_reservation_hour >= self.end_reservation_hour:
            raise ValidationError("Start time must be before end time.")

        doctor_profile = self.doctor.doctor_profile

        start_time = self.start_reservation_hour.time()
        end_time = self.end_reservation_hour.time()

        if not (
            doctor_profile.start_working_hour <= start_time and
            end_time <= doctor_profile.end_working_hour
        ):
            raise ValidationError("Reservation time is outside doctor's working hours.")

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
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            # Notify PATIENT
            Notification.objects.create(
                user=self.patient,
                doctor=None,
                notification_type=NotificationType.RESERVE,
                message=(
                    f"نوبت شما در ساعت {self.start_reservation_hour.strftime('%H:%M')} تا "
                    f"{self.end_reservation_hour.strftime('%H:%M')} در تاریخ "
                    f"{self.start_reservation_hour.strftime('%Y-%m-%d')} "
                    f"با دکتر {self.doctor.username} با موفقیت رزرو شد"
                )
            )

            # Notify DOCTOR
            Notification.objects.create(
                user=None,
                doctor=self.doctor,
                notification_type=NotificationType.RESERVE,
                message=(
                    f"بیمار با شماره تلفن {self.patient.phonenumber} "
                    f"نوبت ساعت {self.start_reservation_hour.strftime('%H:%M')} تا "
                    f"{self.end_reservation_hour.strftime('%H:%M')} در تاریخ "
                    f"{self.start_reservation_hour.strftime('%Y-%m-%d')} "
                    f"را با شما رزرو کرد"
                )
            )

    def delete(self, *args, **kwargs):
        # Before delete → create cancel notifications
        start_str = self.start_reservation_hour.strftime('%H:%M')
        end_str = self.end_reservation_hour.strftime('%H:%M')
        date_str = self.start_reservation_hour.strftime('%Y-%m-%d')

        # Notify PATIENT
        Notification.objects.create(
            user=self.patient,
            doctor=None,
            notification_type=NotificationType.CANCEL,
            message=(
                f"نوبت شما در ساعت {start_str} تا {end_str} در تاریخ {date_str} "
                f"توسط دکتر {self.doctor.username} لغو شد"
            )
        )

        # Notify DOCTOR
        Notification.objects.create(
            user=None,
            doctor=self.doctor,
            notification_type=NotificationType.CANCEL,
            message=(
                f"بیمار با شماره تلفن {self.patient.phonenumber} "
                f"نوبت ساعت {start_str} تا {end_str} در تاریخ {date_str} "
                f"را لغو کرد"
            )
        )

        super().delete(*args, **kwargs)

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

    score = models.IntegerField()
    comment = models.TextField(
        blank=True,
        default=""
    )


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

class Notification(models.Model):
    user        = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications_as_user',
        null=True, blank=True,
        help_text="برای بیمار (اگر اعلان برای بیمار باشد)"
    )
    doctor      = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications_as_doctor',
        null=True, blank=True,
        help_text="برای پزشک (اگر اعلان برای پزشک باشد)"
    )
    notification_type = models.CharField(
        max_length=20,
        choices=NotificationType.choices
    )
    message     = models.TextField()
    is_read     = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['doctor', 'created_at']),
        ]

    def __str__(self):
        return f"{self.notification_type} - {self.created_at}"

class Transaction(models.Model):
    user        = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='transactions'
    )
    price       = models.PositiveIntegerField()
    type = models.CharField(
        max_length=10,
        choices=TransactionType.choices,
        verbose_name="نوع تراکنش"
    )
    method      = models.CharField(
        max_length=10,
        choices=TransactionMethod.choices,
        verbose_name="روش پرداخت"
    )
    status      = models.CharField(
        max_length=10,
        choices=TransactionStatus.choices,
        default=TransactionStatus.SUCCESS,
        verbose_name="وضعیت"
    )
    created_at  = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ تراکنش"
    )
    # optional: reference to reservation if payment is for appointment
    reservation = models.ForeignKey(
        'Reservation',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='transactions'
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "تراکنش"
        verbose_name_plural = "تراکنش‌ها"

    def __str__(self):
        return f"{self.user} – {self.price:,} – {self.get_transaction_type_display()}"
