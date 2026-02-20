from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.utils import timezone
from django.db.models import Count, Sum
from .models import (
    User, UserRoles,
    DoctorProfile, Specialty,
    Reservation,
    Comment,
    PasswordReset,
    Transaction, TransactionStatus, Wallet
)


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('name', 'doctor_count', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    actions = ['activate', 'deactivate']

    def doctor_count(self, obj):
        return obj.doctors.count()
    doctor_count.short_description = "تعداد پزشکان"

    def activate(self, request, queryset):
        queryset.update(is_active=True)
    activate.short_description = "فعال‌سازی"

    def deactivate(self, request, queryset):
        queryset.update(is_active=False)
    deactivate.short_description = "غیرفعال‌سازی"


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        "email", "username", "phonenumber", "role_colored",
        "is_active", "is_staff", "is_superuser", "date_joined"
    )
    list_filter = ("role", "is_active", "is_staff", "is_superuser")
    search_fields = ("email", "username", "phonenumber")
    ordering = ("email",)
    readonly_fields = ("date_joined", "last_login")

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'phonenumber', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'phonenumber', 'password1', 'password2', 'role'),
        }),
    )

    def role_colored(self, obj):
        colors = {
            UserRoles.PATIENT: "blue",
            UserRoles.DOCTOR: "green",
            UserRoles.ADMIN: "red",
        }
        color = colors.get(obj.role, "gray")
        return format_html('<span style="color: {};">{}</span>', color, obj.get_role_display())
    role_colored.short_description = "نقش"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.exclude(is_superuser=True)
        return qs


@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = (
        "doctor_name", "specialty", "location", "experience",
        "price", "score_display", "working_hours", "reservation_count"
    )
    list_filter = ("specialty", "location")
    search_fields = ("user__username", "user__email", "specialty__name", "location")
    autocomplete_fields = ["user", "specialty"]

    fieldsets = (
        (None, {'fields': ('user',)}),
        ('اطلاعات حرفه‌ای', {'fields': ('specialty', 'experience', 'price', 'score', 'location')}),
        ('ساعات کاری', {'fields': ('start_working_hour', 'end_working_hour')}),
    )
    readonly_fields = ("score",)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            _reservation_count=Count('user__doctor_reservations')
        )

    def doctor_name(self, obj):
        return f"دکتر {obj.user.username}"
    doctor_name.short_description = "نام پزشک"

    def score_display(self, obj):
        return f"{obj.score:.1f}" if obj.score else "—"
    score_display.short_description = "امتیاز"

    def working_hours(self, obj):
        return f"{obj.start_working_hour.strftime('%H:%M')} – {obj.end_working_hour.strftime('%H:%M')}"
    working_hours.short_description = "ساعات کاری"

    def reservation_count(self, obj):
        return obj._reservation_count
    reservation_count.short_description = "تعداد نوبت‌ها"
    reservation_count.admin_order_field = '_reservation_count'


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        "patient_link", "doctor_link", "start_reservation_hour",
        "end_reservation_hour", "duration", "created_at", "is_future"
    )
    list_filter = ("start_reservation_hour",)
    search_fields = (
        "patient__username", "patient__email",
        "doctor__username", "doctor__email"
    )
    date_hierarchy = "start_reservation_hour"
    readonly_fields = ("created_at",)
    actions = ['cancel_reservations']

    def cancel_reservations(self, request, queryset):
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f"{count} نوبت لغو شد.")
    cancel_reservations.short_description = "لغو نوبت‌های انتخاب شده"

    def patient_link(self, obj):
        return format_html('<a href="/admin/accounts/user/{}/">{}</a>', obj.patient.id, obj.patient)
    patient_link.short_description = "بیمار"

    def doctor_link(self, obj):
        return format_html('<a href="/admin/accounts/doctorprofile/{}/">{}</a>', obj.doctor.doctor_profile.id, f"دکتر {obj.doctor}")
    doctor_link.short_description = "پزشک"

    def duration(self, obj):
        delta = obj.end_reservation_hour - obj.start_reservation_hour
        return f"{delta.total_seconds() // 60:.0f} دقیقه"
    duration.short_description = "مدت"

    def is_future(self, obj):
        return obj.start_reservation_hour > timezone.now()
    is_future.boolean = True
    is_future.short_description = "آینده"


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'price_formatted', 'type', 'method', 'status_colored', 'reservation', 'created_at')
    list_filter = ('status', 'type', 'method', 'created_at')
    search_fields = ('user__username', 'user__email')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)
    actions = ['mark_refunded']

    def __str__(self):
        return f"{self.user} – {self.price:,} – {self.get_type_display()}"

    def price_formatted(self, obj):
        return f"{obj.price:,} تومان"
    price_formatted.short_description = "مبلغ"

    def status_colored(self, obj):
        colors = {
            TransactionStatus.SUCCESS: "green",
            TransactionStatus.FAILED: "red",
            TransactionStatus.PENDING: "orange",
        }
        color = colors.get(obj.status, "gray")
        return format_html('<span style="color: {};">{}</span>', color, obj.get_status_display())
    status_colored.short_description = "وضعیت"

    def mark_refunded(self, request, queryset):
        queryset.update(status=TransactionStatus.REFUNDED)  # add REFUNDED to your choices if not there
    mark_refunded.short_description = "علامت‌گذاری به عنوان بازگشت وجه"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("doctor_link", "patient_link", "score", "short_comment", "created_at")
    list_filter = ("score", "created_at")
    search_fields = ("doctor__username", "patient__username", "comment")
    date_hierarchy = "created_at"
    readonly_fields = ("created_at",)

    def doctor_link(self, obj):
        return f"دکتر {obj.doctor.username}"
    doctor_link.short_description = "پزشک"

    def patient_link(self, obj):
        return obj.patient.username
    patient_link.short_description = "بیمار"

    def short_comment(self, obj):
        return (obj.comment[:60] + "...") if len(obj.comment) > 60 else obj.comment
    short_comment.short_description = "متن نظر"


@admin.register(PasswordReset)
class PasswordResetAdmin(admin.ModelAdmin):
    list_display = ("user", "verificationCode", "created_when", "is_expired")
    list_filter = ("created_when",)
    search_fields = ("user__email", "user__username", "verificationCode")
    date_hierarchy = "created_when"
    readonly_fields = ("created_when",)

    def is_expired(self, obj):
        return obj.is_expired
    is_expired.boolean = True

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance_formatted', 'updated_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('updated_at',)

    def balance_formatted(self, obj):
        return f"{obj.balance:,} تومان"
    balance_formatted.short_description = "موجودی"
