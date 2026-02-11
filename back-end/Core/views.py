import random

import django.contrib.auth
from rest_framework import viewsets, status
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.db import IntegrityError

from .models import DoctorProfile, PasswordReset, Reservation
from .serializers import (
    LoginSerializer,
    RegisterSerializer,
    ForgetPasswordSerializer,
    ReservationSerializer,
    ResetPasswordSerializer,
    UserSerializer,
    DoctorListSerializer,
    DoctorDetailSerializer,
    CommentSerializer
)
from kavenegar import *

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
            expiration_time = password_reset.created_when + timezone.timedelta(minutes=2)
            
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
            )
            
        except PasswordReset.DoesNotExist:
            return error_response(
                message="کد بازنشانی نامعتبر است",
                message_en="Invalid reset ID",
                status_code=status.HTTP_404_NOT_FOUND
            )

class HomeAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return success_response(
            message=f"خوش آمدید {request.user.username}",
            message_en=f"Welcome {request.user.username}",
            extra_data={"user": UserSerializer(request.user).data}
        )
    
class DoctorsListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        doctors = DoctorProfile.objects.all()
        serializer = DoctorListSerializer(doctors, many=True)
        return Response(serializer.data)

class DoctorDetailAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        try:
            doctor = DoctorProfile.objects.get(pk=pk)
        except DoctorProfile.DoesNotExist:
            return Response({"detail": "Not found"}, status=404)

        serializer = DoctorDetailSerializer(doctor)
        return Response(serializer.data)

class ReservationCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ReservationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(patient=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class UserReservationsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        reservations = Reservation.objects.filter(patient=request.user)
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)

class ReservationDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            reservation = Reservation.objects.get(pk=pk, patient=request.user)
        except Reservation.DoesNotExist:
            return Response({"detail": "Not found"}, status=404)

        reservation.delete()
        return Response(status=204)

class CommentCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(patient=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


def is_email(value):
    try:
        validate_email(value)
        return True
    except ValidationError:
        return False