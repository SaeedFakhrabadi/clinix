from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import (
    User, UserRoles,
    DoctorProfile,
    Reservation,
    Comment,
    PasswordReset
)

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
        (None, {
            'fields': ('email', 'password')
        }),
        ('Personal info', {
            'fields': ('username', 'phonenumber', 'role')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
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
            UserRoles.DOCTOR:  "green",
            UserRoles.ADMIN:   "red",
        }
        color = colors.get(obj.role, "gray")
        return format_html(
            '<span style="color: {};">{}</span>',
            color, obj.get_role_display()
        )
    role_colored.short_description = "نقش"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Optional: hide superusers from non-superuser admins
        if not request.user.is_superuser:
            return qs.exclude(is_superuser=True)
        return qs


@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = (
        "doctor_name", "field", "location", "experience",
        "price", "score_display", "working_hours"
    )
    list_filter = ("field",)
    search_fields = ("user__username", "user__email", "field", "location")
    autocomplete_fields = ["user"]

    fieldsets = (
        (None, {
            'fields': ('user',)
        }),
        ('اطلاعات حرفه‌ای', {
            'fields': ('field', 'experience', 'price', 'score', 'location')
        }),
        ('ساعات کاری', {
            'fields': ('start_working_hour', 'end_working_hour')
        }),
    )

    readonly_fields = ("score",)

    def doctor_name(self, obj):
        return f"دکتر {obj.user.username}"
    doctor_name.short_description = "نام پزشک"

    def score_display(self, obj):
        return f"{obj.score:.1f}" if obj.score else "—"
    score_display.short_description = "امتیاز"

    def working_hours(self, obj):
        return f"{obj.start_working_hour.strftime('%H:%M')} – {obj.end_working_hour.strftime('%H:%M')}"
    working_hours.short_description = "ساعات کاری"


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