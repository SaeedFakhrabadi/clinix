from jdatetime import datetime as jdatetime
from zoneinfo import ZoneInfo
from .models import Notification
from django.db import models

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

class ComplaintStatus(models.TextChoices):
    PENDING  = 'PENDING',  'در انتظار بررسی'
    REVIEWED = 'REVIEWED', 'بررسی شده'
    RESOLVED = 'RESOLVED', 'حل شده'
    REJECTED = 'REJECTED', 'رد شده'

def _jalali_range(reservation):
    start = reservation.start_reservation_hour.astimezone(TEHRAN_TZ)
    end   = reservation.end_reservation_hour.astimezone(TEHRAN_TZ)
    date_str  = jdatetime.fromgregorian(datetime=start).strftime('%Y/%m/%d')
    start_str = start.strftime('%H:%M')
    end_str   = end.strftime('%H:%M')
    return date_str, start_str, end_str


def notify_reservation_created(reservation):
    date_str, start_str, end_str = _jalali_range(reservation)
    doctor_name   = reservation.doctor.username
    patient_name  = reservation.patient.username
    patient_phone = reservation.patient.phonenumber

    # Notify patient
    Notification.objects.create(
        user=reservation.patient,
        doctor=None,
        notification_type=NotificationType.RESERVE,
        message=(
            f"نوبت ساعت {start_str} تا {end_str} روز {date_str} "
            f"شما با دکتر {doctor_name} با موفقیت رزرو شد"
        )
    )

    # Notify doctor
    Notification.objects.create(
        user=None,
        doctor=reservation.doctor,
        notification_type=NotificationType.RESERVE,
        message=(
            f"نوبت ساعت {start_str} تا {end_str} روز {date_str} "
            f"توسط کاربر {patient_name} با شماره تلفن {patient_phone} رزرو شد"
        )
    )


def notify_reservation_cancelled(reservation, cancelled_by):
    date_str, start_str, end_str = _jalali_range(reservation)
    doctor_name   = reservation.doctor.username
    patient_name  = reservation.patient.username
    patient_phone = reservation.patient.phonenumber

    cancelled_by_patient = (cancelled_by.id == reservation.patient.id)

    # Notify patient
    canceller_for_patient = "شما" if cancelled_by_patient else f"دکتر {doctor_name}"
    Notification.objects.create(
        user=reservation.patient,
        doctor=None,
        notification_type=NotificationType.CANCEL,
        message=(
            f"نوبت ساعت {start_str} تا {end_str} روز {date_str} "
            f"شما با دکتر {doctor_name} توسط {canceller_for_patient} لغو شد"
        )
    )

    # Notify doctor
    canceller_for_doctor = "شما" if not cancelled_by_patient else f"کاربر {patient_name} با شماره تلفن {patient_phone}"
    Notification.objects.create(
        user=None,
        doctor=reservation.doctor,
        notification_type=NotificationType.CANCEL,
        message=(
            f"نوبت ساعت {start_str} تا {end_str} روز {date_str} "
            f"توسط {canceller_for_doctor} لغو شد"
        )
    )