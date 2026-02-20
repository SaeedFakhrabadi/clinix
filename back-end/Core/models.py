from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.conf import settings
from django.utils import timezone
from django.db.models import Avg, Q
from django.core.exceptions import ValidationError
from zoneinfo import ZoneInfo
from django.core.exceptions import ObjectDoesNotExist

TEHRAN_TZ = ZoneInfo('Asia/Tehran')

class NotificationType(models.TextChoices):
    RESERVE = "RESERVE", "رزرو نوبت"
    CANCEL  = "CANCEL",  "لغو نوبت"

class UserRoles(models.TextChoices):
    PATIENT = "PATIENT", "Patient"
    DOCTOR  = "DOCTOR",  "Doctor"
    ADMIN   = "ADMIN",   "Admin"

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

class ComplaintStatus(models.TextChoices):
    PENDING  = 'PENDING',  'در انتظار بررسی'
    REVIEWED = 'REVIEWED', 'بررسی شده'
    RESOLVED = 'RESOLVED', 'حل شده'
    REJECTED = 'REJECTED', 'رد شده'

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

    @property
    def wallet_balance(self):
        try:
            wallet: 'Wallet' = self.wallet
            return wallet.balance
        except ObjectDoesNotExist:
            return 0

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
        verbose_name = "نوبت"
        verbose_name_plural = "نوبت‌ها"

    def _check_overlap(self, queryset):
        overlapping = queryset.filter(
            Q(start_reservation_hour__lt=self.end_reservation_hour) &
            Q(end_reservation_hour__gt=self.start_reservation_hour)
        )
        if self.pk:
            overlapping = overlapping.exclude(pk=self.pk)
        return overlapping.exists()

    def clean(self):
        if self.start_reservation_hour >= self.end_reservation_hour:
            raise ValidationError("Start time must be before end time.")

        doctor_profile = self.doctor.doctor_profile
        start_time = self.start_reservation_hour.astimezone(TEHRAN_TZ).time()
        end_time = self.end_reservation_hour.astimezone(TEHRAN_TZ).time()

        if not (doctor_profile.start_working_hour <= start_time and
                end_time <= doctor_profile.end_working_hour):
            raise ValidationError("Reservation time is outside doctor's working hours.")

        if self._check_overlap(Reservation.objects.filter(doctor=self.doctor)):
            raise ValidationError("This time slot is already booked.")

        if self._check_overlap(Reservation.objects.filter(patient=self.patient)):
            raise ValidationError("شما در این زمان نوبت دیگری دارید.")

    def save(self, *args, **kwargs):
        self.full_clean()
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            from .utils import notify_reservation_created
            notify_reservation_created(self)

    def delete(self, *args, cancelled_by=None, **kwargs):
        from .utils import notify_reservation_cancelled
        notify_reservation_cancelled(self, cancelled_by=cancelled_by or self.doctor)
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

class PaymentGateway(models.Model):
    name       = models.CharField(max_length=100, verbose_name="نام درگاه")
    code       = models.CharField(max_length=50, unique=True, verbose_name="کد درگاه")  # e.g. 'ZARINPAL', 'MELLAT'
    is_active  = models.BooleanField(default=True, verbose_name="فعال")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "درگاه پرداخت"
        verbose_name_plural = "درگاه‌های پرداخت"

    def __str__(self):
        return f"{self.name} ({'فعال' if self.is_active else 'غیرفعال'})"
