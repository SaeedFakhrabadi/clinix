import random

import django.contrib.auth
from rest_framework import viewsets, status
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.db import IntegrityError

from .models import DoctorProfile, PasswordReset, Reservation, User, Notification, UserRoles, Transaction
from .serializers import (
    LoginSerializer,
    RegisterSerializer,
    ForgetPasswordSerializer,
    ReservationSerializer,
    ResetPasswordSerializer,
    UserSerializer,
    DoctorListSerializer,
    DoctorDetailSerializer,
    ReservationCreateSerializer,
    CommentCreateSerializer, NotificationSerializer, TransactionHistorySerializer, TransactionCreateSerializer
)
from kavenegar import *

from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

User = django.contrib.auth.get_user_model()

def success_response(message, message_en, status_code=status.HTTP_200_OK, extra_data=None):
    data = {
        "message": message,
        "message_en": message_en,
    }
    if extra_data:
        data.update(extra_data)
    return Response(data, status=status_code)

def error_response(message, message_en, status_code=status.HTTP_400_BAD_REQUEST, extra_data=None):
    data = {
        "message": message,
        "message_en": message_en,
    }
    if extra_data:
        data.update(extra_data)
    return Response(data, status=status_code)

def is_email(value):
    try:
        validate_email(value)
        return True
    except ValidationError:
        return False

class AuthViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()

                # refresh = RefreshToken.for_user(user)

                return success_response(
                    message="ثبت‌نام با موفقیت انجام شد",
                    message_en="User registered successfully",
                    status_code=status.HTTP_201_CREATED,
                    extra_data={
                        "user": UserSerializer(user).data,
                    }
                    # extra_data={
                    #     "access_token": str(refresh.access_token),
                    # }
                )
            
            except IntegrityError as e:
                return error_response(
                    message="مشخصات وارد شده تکراری است!",
                    message_en="The entered information is duplicate!",
                    extra_data={
                        "detail": "شماره تلفن یا ایمیل قبلاً ثبت شده است.",
                        "detail_en": "Phone number or email is already registered.",
                        "db_error": str(e)
                    },
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            except Exception:
                return error_response(
                    message="خطایی در ثبت‌نام رخ داد",
                    message_en="An error occurred during registration",
                )
        
        return error_response(
            message="داده‌های ارسالی معتبر نمی‌باشند",
            message_en="Invalid input data",
            status_code=status.HTTP_400_BAD_REQUEST,
            extra_data={"errors": serializer.errors}
        )
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(
                message="داده‌های ارسالی ناقص یا نامعتبر است",
                message_en="Invalid or incomplete input data",
                extra_data={"errors": serializer.errors}
            )

        user = django.contrib.auth.authenticate(
            request,
            identifier=serializer.validated_data['identifier'],   # ← use identifier
            password=serializer.validated_data['password']
        )

        if user:
            # refresh = RefreshToken.for_user(user)
            return success_response(
                message="ورود با موفقیت انجام شد",
                message_en="Login successful",
                extra_data={
                    "user": UserSerializer(user).data,
                }
                # extra_data={
                #     "access_token": str(refresh.access_token),
                # }
            )

        return error_response(
            message="اطلاعات وارد شده صحیح نمی‌باشند!",
            message_en="Invalid credentials!",
            status_code=status.HTTP_401_UNAUTHORIZED,
            extra_data={
                "detail": "ایمیل یا شماره تلفن یا رمز عبور اشتباه است.",
                "detail_en": "Email/phonenumber or password is incorrect."
            }
        )

    @action(detail=False, methods=['post'])
    def forgot_password(self, request):
        serializer = ForgetPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(
                message="ایمیل نامعتبر است",
                message_en="Invalid email format",
                extra_data={"errors": serializer.errors}
            )
        
        identifier = serializer.validated_data['identifier']
        
        try:
            if is_email(identifier):
                user = User.objects.get(email=identifier)
                send_via = "email"
            else:
                user = User.objects.get(phonenumber=identifier)
                send_via = "sms"

            code = random.randint(100000, 999999)

            PasswordReset.objects.update_or_create(
                user=user,
                defaults={
                    "verificationCode": code,
                    "created_when": timezone.now()
                }
            )

            if send_via == "email":
                send_mail(
                    subject="کد بازنشانی رمز عبور",
                    message=f"کد بازنشانی شما: {code}\n\nاین کد ۲ دقیقه اعتبار دارد.",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                )

            else:
                api = KavenegarAPI(settings.KAVENEGAR_API_KEY)
                params = {
                    'sender': '2000660110', 'receptor': user.phonenumber,
                    'message': f"کد بازنشانی رمز عبور شما: {code}"
                }
                response = api.sms_send(params)
                print(response)

            return success_response(
                message="کد بازنشانی ارسال شد",
                message_en="Verification code sent",
            )
            
        except User.DoesNotExist:
            return error_response(
                message="کاربر یافت نشد",
                message_en="User with this email does not exist",
                status_code=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['post'])
    def reset_password(self, request):
        serializer = ResetPasswordSerializer(data=request.data)

        if not serializer.is_valid():
            return error_response(
                message="داده‌های ارسالی نامعتبر است",
                message_en="Invalid input",
                extra_data={"errors": serializer.errors}
            )
        
        verificationCode = serializer.validated_data['verificationCode']
        newPassword = serializer.validated_data['newPassword']
        
        try:
            password_reset = PasswordReset.objects.get(verificationCode=verificationCode)
            expiration_time = password_reset.created_when + timezone.timedelta(minutes=5)
            
            if timezone.now() > expiration_time:
                password_reset.delete()
                return error_response(
                    message="کد تایید منقضی شده است",
                    message_en="Reset link has expired",
                )
            
            user = password_reset.user
            user.set_password(newPassword)
            user.save()
            password_reset.delete()
            
            return success_response(
                message="رمز عبور با موفقیت تغییر یافت",
                message_en="Password reset successfully",
                extra_data={
                    "user": UserSerializer(user).data,
                }
            )
            
        except PasswordReset.DoesNotExist:
            return error_response(
                message="کد بازنشانی نامعتبر است",
                message_en="Invalid reset ID",
                status_code=status.HTTP_404_NOT_FOUND
            )

class DoctorsListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        doctors = DoctorProfile.objects.all()
        serializer = DoctorListSerializer(doctors, many=True)
        return Response(serializer.data)

class UserReservationsAPIView(APIView):
    permission_classes = [AllowAny]   # ← no login required (dev phase)

    def get(self, request, user_id):
        # 1. Get the user or return 404
        user = get_object_or_404(User, id=user_id)

        # 2. Get their reservations
        reservations = Reservation.objects.filter(patient=user).order_by('-start_reservation_hour')

        # 3. Serialize
        serializer = ReservationSerializer(reservations, many=True)

        # 4. Optional: enrich response with some user info
        return Response({
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "reservations_count": reservations.count(),
            "reservations": serializer.data
        })

class ReservationDeleteAPIView(APIView):
    permission_classes = [AllowAny]

    def delete(self, request, pk):
        # WARNING: allows anyone to delete any reservation!
        try:
            reservation = Reservation.objects.get(id=pk)
        except Reservation.DoesNotExist:
            return Response({"detail": "Not found"}, status=404)

        reservation.delete()
        return Response(status=204)

class ReservationCreateAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ReservationCreateSerializer(data=request.data)
        if serializer.is_valid():
            reservation = serializer.save()
            return success_response(
                message="نوبت با موفقیت ثبت شد",
                message_en="Reservation created successfully",
                status_code=status.HTTP_201_CREATED,
                extra_data={
                    "reservation_id": reservation.id,
                    "start": reservation.start_reservation_hour,
                    "end": reservation.end_reservation_hour
                }
            )
        return error_response(
            message="داده‌های ارسالی معتبر نیستند",
            message_en="Invalid data",
            extra_data={"errors": serializer.errors}
        )

class DoctorDetailAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        try:
            doctor = DoctorProfile.objects.get(pk=pk)
        except DoctorProfile.DoesNotExist:
            return Response({"detail": "Not found"}, status=404)

        serializer = DoctorDetailSerializer(doctor)
        return Response(serializer.data)

class CommentCreateAPIView(APIView):
    permission_classes = [AllowAny]   # ← change to IsAuthenticated later

    def post(self, request):
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            comment = serializer.save()
            return success_response(
                message="نظر با موفقیت ثبت شد",
                message_en="Comment created successfully",
                status_code=status.HTTP_201_CREATED,
                extra_data={
                    "comment_id": comment.id,
                    "score": comment.score,
                    "doctor_id": comment.doctor.doctor_profile.id
                }
            )
        return error_response(
            message="داده‌های ارسالی معتبر نیستند",
            message_en="Invalid input",
            status_code=status.HTTP_400_BAD_REQUEST,
            extra_data={"errors": serializer.errors}
        )

class NotificationsListAPIView(APIView):
    permission_classes = [AllowAny]  # ← change to IsAuthenticated later

    def get(self, request):
        user_id = request.query_params.get('user_id')
        doctor_id = request.query_params.get('doctor_id')

        if not user_id and not doctor_id:
            return error_response(
                message="حداقل یکی از user_id یا doctor_id باید ارسال شود",
                message_en="At least user_id or doctor_id is required",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        if user_id and doctor_id:
            return error_response(
                message="فقط یکی از user_id یا doctor_id مجاز است",
                message_en="Only one of user_id or doctor_id is allowed",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        queryset = Notification.objects.none()

        if user_id:
            try:
                user = User.objects.get(id=user_id)
                queryset = Notification.objects.filter(user=user)
            except User.DoesNotExist:
                return error_response(
                    message="کاربر یافت نشد",
                    message_en="User not found",
                    status_code=status.HTTP_404_NOT_FOUND
                )

        elif doctor_id:
            try:
                doctor = User.objects.get(id=doctor_id)
                if doctor.role != UserRoles.DOCTOR:
                    return error_response(
                        message="شناسه وارد شده پزشک نیست",
                        message_en="Provided ID is not a doctor",
                        status_code=status.HTTP_400_BAD_REQUEST
                    )
                queryset = Notification.objects.filter(doctor=doctor)
            except User.DoesNotExist:
                return error_response(
                    message="پزشک یافت نشد",
                    message_en="Doctor not found",
                    status_code=status.HTTP_404_NOT_FOUND
                )

        serializer = NotificationSerializer(queryset.order_by('-created_at'), many=True)

        return success_response(
            message="لیست اعلان‌ها با موفقیت دریافت شد",
            message_en="Notifications retrieved successfully",
            extra_data={"notifications": serializer.data}
        )

class TransactionCreateAPIView(APIView):
    permission_classes = [AllowAny]   # ← بعداً به IsAuthenticated تغییر دهید

    def post(self, request):
        serializer = TransactionCreateSerializer(data=request.data)
        if serializer.is_valid():
            transaction = serializer.save()
            return success_response(
                message="تراکنش با موفقیت ثبت شد",
                message_en="Transaction created successfully",
                status_code=status.HTTP_201_CREATED,
                extra_data={
                    "transaction_id": transaction.id,
                    "price": transaction.price,
                    "status": transaction.status,
                    "date": transaction.created_at.strftime("%Y-%m-%d %H:%M")
                }
            )
        return error_response(
            message="داده‌های ارسالی معتبر نیستند",
            message_en="Invalid data",
            extra_data={"errors": serializer.errors}
        )

class TransactionHistoryAPIView(APIView):
    permission_classes = [AllowAny]   # ← بعداً محدود کنید

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return error_response(
                message="کاربر یافت نشد",
                message_en="User not found",
                status_code=status.HTTP_404_NOT_FOUND
            )

        transactions = Transaction.objects.filter(user=user).order_by('-created_at')
        serializer = TransactionHistorySerializer(transactions, many=True)

        return success_response(
            message="تاریخچه تراکنش‌ها دریافت شد",
            message_en="Transaction history retrieved",
            extra_data={"transactions": serializer.data}
        )
