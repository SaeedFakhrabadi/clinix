from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import DoctorProfile, Comment, Reservation, UserRoles, Notification, TransactionType, TransactionMethod, \
    Transaction, TransactionStatus
from jdatetime import date as jdate
from datetime import datetime, timedelta
from django.utils import timezone

User = get_user_model()

class LocalDateTimeField(serializers.DateTimeField):
    def to_representation(self, value):
        if value is None:
            return None
        local_value = timezone.localtime(value)
        print("DEBUG: Converting", value, "→", local_value)
        return local_value.strftime('%Y-%m-%d %H:%M')

class RegisterSerializer(serializers.ModelSerializer):     
    password = serializers.CharField(
        write_only=True,
        # validators=[validate_password]
    )

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'phonenumber')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            phonenumber=validated_data['phonenumber'],
            password=validated_data['password'],
            role="PATIENT"
        )

class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        identifier = attrs.get('identifier')
        password = attrs.get('password')

        if not identifier or not password:
            raise serializers.ValidationError("Both identifier and password are required.")

        return attrs

class ForgetPasswordSerializer(serializers.Serializer):
    identifier = serializers.CharField(required=True)

class ResetPasswordSerializer(serializers.Serializer):
    verificationCode = serializers.IntegerField(required=True)
    newPassword = serializers.CharField(
        required=True,
        write_only=True,
        # validators=[validate_password],
        style={'input_type': 'password'}
    )

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'phonenumber',
            'role',
        )
        read_only_fields = ('id','role')

class DoctorListSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.username')

    class Meta:
        model = DoctorProfile
        fields = [
            'id',
            'name',
            'field',
            'location',
            'score',
            'price',
        ]

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='patient.username')

    class Meta:
        model = Comment
        fields = ['score', 'username', 'comment']
        read_only_fields = fields

# class ReservationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Reservation
#         fields = [
#             'id',
#             'patient',
#             'start_reservation_hour',
#             'end_reservation_hour'
#         ]
#         read_only_fields = ['patient']

class ReservationSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.username', read_only=True)
    # doctor_name = serializers.CharField(source='doctor.full_name', read_only=True)
    start_reservation_time = serializers.DateTimeField(
        source='start_reservation_hour',
        format='%Y-%m-%dT%H:%M:%SZ',
        read_only=True
    )
    is_past = serializers.SerializerMethodField()

    class Meta:
        model = Reservation
        fields = [
            'id',
            'doctor_name',
            'is_past',
            'start_reservation_time',
        ]

    def get_is_past(self, obj):
        return obj.start_reservation_hour < timezone.now()


class ReservationCreateSerializer(serializers.Serializer):
    doctor_id = serializers.IntegerField()
    time = serializers.CharField()

    def validate(self, data):
        # Get patient from request context (authenticated user)
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("User not authenticated")

        # Set patient from authenticated user
        data['patient'] = request.user

        # Parse time
        try:
            y, m, d, hour = map(int, data['time'].split('-'))
            jdt = jdate(y, m, d)
            greg = jdt.togregorian()

            naive_start = datetime.combine(greg, datetime.min.time().replace(hour=hour, minute=0, second=0))
            aware_start = timezone.make_aware(naive_start)

            data['start_reservation_hour'] = aware_start
            data['end_reservation_hour'] = aware_start + timedelta(hours=1)

        except Exception as e:
            raise serializers.ValidationError(f"فرمت زمان اشتباه است یا تاریخ معتبر نیست: {str(e)}")

        # Get doctor
        try:
            profile = DoctorProfile.objects.get(id=data['doctor_id'])
            data['doctor'] = profile.user
        except DoctorProfile.DoesNotExist:
            raise serializers.ValidationError("پزشک یافت نشد")

        return data

    def create(self, validated_data):
        return Reservation.objects.create(
            doctor=validated_data['doctor'],
            patient=validated_data['patient'],  # Now from request.user
            start_reservation_hour=validated_data['start_reservation_hour'],
            end_reservation_hour=validated_data['end_reservation_hour']
        )


# class ReservationCreateSerializer(serializers.Serializer):
#     doctor_id = serializers.IntegerField()
#     user_id   = serializers.IntegerField()
#     time      = serializers.CharField()
#
#     def validate(self, data):
#         try:
#             y, m, d, hour = map(int, data['time'].split('-'))
#             jdt = jdate(y, m, d)
#             greg = jdt.togregorian()
#
#             # Create naive datetime first
#             naive_start = datetime.combine(greg, datetime.min.time().replace(hour=hour, minute=0, second=0))
#
#             # Make it timezone-aware (uses settings.TIME_ZONE)
#             aware_start = timezone.make_aware(naive_start)
#
#             data['start_reservation_hour'] = aware_start
#             data['end_reservation_hour'] = aware_start + timedelta(hours=1)
#
#         except Exception as e:
#             raise serializers.ValidationError(f"فرمت زمان اشتباه است یا تاریخ معتبر نیست: {str(e)}")
#
#         # 2. Get doctor (from DoctorProfile.id → User)
#         try:
#             profile = DoctorProfile.objects.get(id=data['doctor_id'])
#             data['doctor'] = profile.user
#         except DoctorProfile.DoesNotExist:
#             raise serializers.ValidationError("پزشک یافت نشد")
#
#         # 3. Get patient
#         try:
#             data['patient'] = User.objects.get(id=data['user_id'])
#         except User.DoesNotExist:
#             raise serializers.ValidationError("کاربر یافت نشد")
#
#         return data
#
#     def create(self, validated_data):
#         return Reservation.objects.create(
#             doctor=validated_data['doctor'],
#             patient=validated_data['patient'],
#             start_reservation_hour=validated_data['start_reservation_hour'],
#             end_reservation_hour=validated_data['end_reservation_hour']
#         )

class DoctorDetailSerializer(serializers.ModelSerializer):
    did = serializers.IntegerField(source='id')
    name = serializers.CharField(source='user.username')

    start_working_hour = serializers.SerializerMethodField()
    end_working_hour   = serializers.SerializerMethodField()
    reserved_times     = serializers.SerializerMethodField()
    comments           = serializers.SerializerMethodField()

    class Meta:
        model = DoctorProfile
        fields = [
            'did', 'name', 'field', 'location', 'score', 'price',
            'experience', 'start_working_hour', 'end_working_hour',
            'reserved_times', 'comments'
        ]

    def get_start_working_hour(self, obj):
        return obj.start_working_hour.hour

    def get_end_working_hour(self, obj):
        return obj.end_working_hour.hour

    def get_reserved_times(self, obj):
        today = jdate.today()
        # شنبه هفته جاری (در jdatetime: weekday()=0 → شنبه)
        saturday = today - timedelta(days=today.weekday())

        reserved = {}
        for i in range(12):                                 # 0 تا 11
            day_jalali = saturday + timedelta(days=i)
            day_greg = day_jalali.togregorian()

            reservations = Reservation.objects.filter(
                doctor=obj.user,
                start_reservation_hour__date=day_greg
            )

            hours = [r.start_reservation_hour.hour for r in reservations]
            reserved[i] = sorted(set(hours))                # بدون تکرار و مرتب

        return reserved

    def get_comments(self, obj):
        comments = Comment.objects.filter(doctor=obj.user)
        return CommentSerializer(comments, many=True).data

class CommentCreateSerializer(serializers.Serializer):
    doctor_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    comment = serializers.CharField(
        max_length=1000,
        trim_whitespace=True,
        allow_blank=True,
        required=True
    )
    score = serializers.IntegerField(min_value=1, max_value=5)

    def validate(self, data):
        # Get doctor
        try:
            doctor_profile = DoctorProfile.objects.get(id=data['doctor_id'])
            data['doctor'] = doctor_profile.user
        except DoctorProfile.DoesNotExist:
            raise serializers.ValidationError({"doctor_id": "پزشک با این شناسه یافت نشد"})

        # Get patient
        try:
            patient = User.objects.get(id=data['user_id'])
            if patient.role != UserRoles.PATIENT:
                raise serializers.ValidationError({"user_id": "فقط بیماران می‌توانند نظر ثبت کنند"})
            data['patient'] = patient
        except User.DoesNotExist:
            raise serializers.ValidationError({"user_id": "کاربر یافت نشد"})

        return data

    def validate_comment(self, value):
        if value == "":
            return ""

        return value

    def create(self, validated_data):
        comment = Comment.objects.create(
            doctor=validated_data['doctor'],
            patient=validated_data['patient'],
            score=validated_data['score'],
            comment=validated_data.get('comment', '').strip()
        )

        return comment

class NotificationSerializer(serializers.ModelSerializer):
    created_at = LocalDateTimeField(source='created_at')
    class Meta:
        model = Notification
        fields = ['id', 'message', 'notification_type', 'is_read', 'created_at']
        read_only_fields = fields

class TransactionCreateSerializer(serializers.Serializer):
    price     = serializers.IntegerField(min_value=1000)   # حداقل مبلغ منطقی
    user_id   = serializers.IntegerField()
    type      = serializers.ChoiceField(choices=TransactionType.choices)
    method    = serializers.ChoiceField(choices=TransactionMethod.choices)

    def validate(self, data):
        try:
            user = User.objects.get(id=data['user_id'])
            data['user'] = user
        except User.DoesNotExist:
            raise serializers.ValidationError({"user_id": "کاربر یافت نشد"})

        return data

    def create(self, validated_data):
        transaction = Transaction.objects.create(
            user=validated_data['user'],
            price=validated_data['price'],
            type=validated_data['type'],
            method=validated_data['method'],
            status=TransactionStatus.SUCCESS,
        )
        return transaction

class TransactionHistorySerializer(serializers.ModelSerializer):
    date = LocalDateTimeField(source='created_at')

    class Meta:
        model = Transaction
        fields = ['price', 'status', 'date', 'method', 'type']
        read_only_fields = fields
