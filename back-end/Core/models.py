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
from jdatetime import datetime as jdatetime
from zoneinfo import ZoneInfo

TEHRAN_TZ = ZoneInfo('Asia/Tehran')

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
    REFUNDED = "REFUNDED", "بازپرداخت شده"

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

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربر‌ها"

    def __str__(self):
        return self.username

class Specialty(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="تخصص")
    description = models.TextField(blank=True, verbose_name="توضیحات")
    is_active = models.BooleanField(default=True, verbose_name="فعال")

    class Meta:
        verbose_name = "تخصص"
        verbose_name_plural = "تخصص‌ها"

    def __str__(self):
        return self.name

class DoctorProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': UserRoles.DOCTOR},
        related_name='doctor_profile'
    )

    specialty = models.ForeignKey(          # replaces field CharField
        Specialty,
        on_delete=models.SET_NULL,
        null=True,
        related_name='doctors',
        verbose_name="تخصص"
    )
    field = models.CharField(max_length=150, blank=True)  # keep for backward compat, populate from specialty
    location = models.CharField(max_length=255)
    experience = models.PositiveIntegerField(help_text="Years of experience")
    price = models.PositiveIntegerField()
    score = models.FloatField(default=0)
    start_working_hour = models.TimeField()
    end_working_hour = models.TimeField()

    class Meta:
        verbose_name = "دکتر"
        verbose_name_plural = "دکتر‌ها"

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

    class Meta:
        verbose_name = "رزرو"
        verbose_name_plural = "رزرو‌ها"

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

        # Check if doctor's time slot is already booked
        doctor_overlapping = Reservation.objects.filter(
            doctor=self.doctor
        ).filter(
            Q(start_reservation_hour__lt=self.end_reservation_hour) &
            Q(end_reservation_hour__gt=self.start_reservation_hour)
        )

        if self.pk:
            doctor_overlapping = doctor_overlapping.exclude(pk=self.pk)

        if doctor_overlapping.exists():
            raise ValidationError("This time slot is already booked.")

        # Check if patient already has an appointment at this time
        patient_overlapping = Reservation.objects.filter(
            patient=self.patient
        ).filter(
            Q(start_reservation_hour__lt=self.end_reservation_hour) &
            Q(end_reservation_hour__gt=self.start_reservation_hour)
        )

        if self.pk:
            patient_overlapping = patient_overlapping.exclude(pk=self.pk)

        if patient_overlapping.exists():
            raise ValidationError("شما در این زمان نوبت دیگری دارید.")

    def save(self, *args, **kwargs):
        self.full_clean()
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            # Convert to Tehran timezone and Jalali date
            start_tehran = self.start_reservation_hour.astimezone(TEHRAN_TZ)
            end_tehran = self.end_reservation_hour.astimezone(TEHRAN_TZ)
            jalali_date = jdatetime.fromgregorian(datetime=start_tehran).strftime('%Y/%m/%d')

            # Notify PATIENT
            Notification.objects.create(
                user=self.patient,
                doctor=None,
                notification_type=NotificationType.RESERVE,
                message=(
                    f"نوبت شما در ساعت {start_tehran.strftime('%H:%M')} تا "
                    f"{end_tehran.strftime('%H:%M')} در تاریخ "
                    f"{jalali_date} "
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
                    f"نوبت ساعت {start_tehran.strftime('%H:%M')} تا "
                    f"{end_tehran.strftime('%H:%M')} در تاریخ "
                    f"{jalali_date} "
                    f"را با شما رزرو کرد"
                )
            )

    def delete(self, *args, **kwargs):
        # Before delete → create cancel notifications
        # Convert to Tehran timezone and Jalali date
        start_tehran = self.start_reservation_hour.astimezone(TEHRAN_TZ)
        end_tehran = self.end_reservation_hour.astimezone(TEHRAN_TZ)
        jalali_date = jdatetime.fromgregorian(datetime=start_tehran).strftime('%Y/%m/%d')

        start_str = start_tehran.strftime('%H:%M')
        end_str = end_tehran.strftime('%H:%M')

        # Notify PATIENT
        Notification.objects.create(
            user=self.patient,
            doctor=None,
            notification_type=NotificationType.CANCEL,
            message=(
                f"نوبت شما در ساعت {start_str} تا {end_str} در تاریخ {jalali_date} "
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
                f"نوبت ساعت {start_str} تا {end_str} در تاریخ {jalali_date} "
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

    class Meta:
        verbose_name = "نظر"
        verbose_name_plural = "نظرات"

    def clean(self):
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
        verbose_name = "ریست پسورد"
        verbose_name_plural = "ریست پسوردها"
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
        verbose_name = "اعلان"
        verbose_name_plural = "اعلان‌ها"
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
        return f"{self.user} – {self.price:,} – {self.get_type_display()}"


class Wallet(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='wallet'
    )
    balance = models.PositiveIntegerField(default=0, verbose_name="موجودی")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "کیف پول"
        verbose_name_plural = "کیف پول‌ها"

    def deposit(self, amount):
        self.balance += amount
        self.save()

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("موجودی کافی نیست")
        self.balance -= amount
        self.save()

    def __str__(self):
        return f"{self.user.username} – {self.balance:,} تومان"

class ComplaintStatus(models.TextChoices):
    PENDING  = 'PENDING',  'در انتظار بررسی'
    REVIEWED = 'REVIEWED', 'بررسی شده'
    RESOLVED = 'RESOLVED', 'حل شده'
    REJECTED = 'REJECTED', 'رد شده'

class Complaint(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='complaints',
        verbose_name="کاربر"
    )
    subject = models.CharField(max_length=255, verbose_name="موضوع")
    message = models.TextField(verbose_name="متن شکایت")
    status = models.CharField(
        max_length=10,
        choices=ComplaintStatus.choices,
        default=ComplaintStatus.PENDING,
        verbose_name="وضعیت"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین بروزرسانی")
    admin_note = models.TextField(blank=True, verbose_name="یادداشت ادمین")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "شکایت"
        verbose_name_plural = "شکایات"

    def __str__(self):
        return f"{self.user.username} – {self.subject[:50]}"
