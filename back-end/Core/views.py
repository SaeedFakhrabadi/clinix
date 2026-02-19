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
from rest_framework_simplejwt.tokens import RefreshToken

from .auth_utils import CookieAuthMixin

from .models import DoctorProfile, PasswordReset, Reservation, User, Notification, UserRoles, Transaction
from .serializers import (
    LoginSerializer,
    RegisterSerializer,
    ForgetPasswordSerializer,
    ResetPasswordSerializer,
    UserSerializer,
    DoctorListSerializer,
    DoctorDetailSerializer,
    ReservationCreateSerializer,
    CommentCreateSerializer, NotificationSerializer, TransactionHistorySerializer, TransactionCreateSerializer,
    DoctorReservationSerializer, PatientReservationSerializer
)
from kavenegar import *

from rest_framework.views import APIView
from rest_framework.response import Response

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

class AuthViewSet(viewsets.ViewSet, CookieAuthMixin):
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()

                # Create response
                response = success_response(
                    message="ثبت‌نام با موفقیت انجام شد",
                    message_en="User registered successfully",
                    status_code=status.HTTP_201_CREATED,
                    extra_data={
                        "user": UserSerializer(user).data,
                    }
                )

                # Set authentication cookies
                return self.set_auth_cookies(response, user)
            
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
            identifier=serializer.validated_data['identifier'],
            password=serializer.validated_data['password']
        )

        if user:
            user_data = UserSerializer(user).data

            if user.role == UserRoles.DOCTOR:
                try:
                    user_data['did'] = user.doctor_profile.id
                except DoctorProfile.DoesNotExist:
                    return error_response(
                        message="پروفایل دکتر در سیستم تعریف نشده است، به ادمین پیام دهید",
                        message_en="The doctor's profile is not defined in the system, send a message to the admin.",
                        status_code=status.HTTP_404_NOT_FOUND,
                    )

            response = success_response(
                message="ورود با موفقیت انجام شد",
                message_en="Login successful",
                extra_data={
                    "user": user_data
                }
            )

            return self.set_auth_cookies(response, user)

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
    def logout(self, request):
        """Logout user by clearing auth cookies."""
        response = success_response(
            message="با موفقیت خارج شدید",
            message_en="Logged out successfully"
        )
        return self.clear_auth_cookies(response)

    @action(detail=False, methods=['post'])
    def refresh_token(self, request):
        """Manually refresh access token."""
        refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            return error_response(
                message="نشانه یافت نشد",
                message_en="Token not found",
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        try:
            refresh = RefreshToken(refresh_token)
            new_access_token = str(refresh.access_token)

            response = success_response(
                message="نشانه با موفقیت به‌روزرسانی شد",
                message_en="Token refreshed successfully",
                extra_data={
                    "access_token": new_access_token
                }
            )

            # Set new access token cookie
            response.set_cookie(
                key='access_token',
                value=new_access_token,
                max_age=300,  # 5 minutes
                httponly=True,
                samesite='Lax',
                secure=not settings.DEBUG,
                path='/'
            )

            return response

        except Exception as e:
            return error_response(
                message="نشانه نامعتبر است",
                message_en="Invalid token",
                status_code=status.HTTP_401_UNAUTHORIZED
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
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.role == UserRoles.DOCTOR:
            reservations = Reservation.objects.filter(doctor=user).order_by('-start_reservation_hour')
            serializer = DoctorReservationSerializer(reservations, many=True)
        else:
            reservations = Reservation.objects.filter(patient=user).order_by('-start_reservation_hour')
            serializer = PatientReservationSerializer(reservations, many=True)

        return Response({
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "reservations_count": reservations.count(),
            "reservations": serializer.data
        })

class ReservationDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            reservation = Reservation.objects.get(id=pk)

            # Check if user owns this reservation
            if reservation.patient.id != request.user.id:
                return error_response(
                    message="شما اجازه حذف این نوبت را ندارید",
                    message_en="You don't have permission to delete this reservation",
                    status_code=status.HTTP_403_FORBIDDEN
                )
            doctor_profile = reservation.doctor.doctor_profile
            doctor_price = doctor_profile.price

            reservation.delete()

            return success_response(
                message="نوبت با موفقیت حذف گردید",
                message_en="reservation deleted successfully",
                status_code=status.HTTP_204_NO_CONTENT,
                extra_data={
                    "price": doctor_price,
                }
            )

        except Reservation.DoesNotExist:
            return Response({"detail": "Not found"}, status=404)

class ReservationCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print(f"Authenticated user in view: {request.user.id}")
        print(f"Request data: {request.data}")

        # Add user_id from authenticated user
        # data = request.data.copy()
        # data['user_id'] = request.user.id

        serializer = ReservationCreateSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            try:
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
            except ValidationError as e:
                return error_response(
                    message=str(e.message) if hasattr(e, 'message') else str(e.messages[0]),
                    message_en="Reservation conflict",
                    extra_data={"errors": e.messages if hasattr(e, 'messages') else [str(e)]}
                )

        print(f"Serializer errors: {serializer.errors}")  # Debug
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
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Add user_id from authenticated user
        data = request.data.copy()
        data['user_id'] = request.user.id

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
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Don't accept user_id or doctor_id parameters
        # Just return notifications for the authenticated user

        # For patients
        if request.user.role == UserRoles.PATIENT:
            notifications = Notification.objects.filter(user=request.user)

        # For doctors
        elif request.user.role == UserRoles.DOCTOR:
            notifications = Notification.objects.filter(doctor=request.user)

        else:
            notifications = Notification.objects.none()

        serializer = NotificationSerializer(notifications.order_by('-created_at'), many=True)

        return success_response(
            message="لیست اعلان‌ها با موفقیت دریافت شد",
            message_en="Notifications retrieved successfully",
            extra_data={"notifications": serializer.data}
        )

class TransactionCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Add user_id from authenticated user
        data = request.data.copy()
        data['user_id'] = request.user.id

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
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Get transaction history for the authenticated user
        """
        # Get transactions for the authenticated user
        transactions = Transaction.objects.filter(user=request.user).order_by('-created_at')
        serializer = TransactionHistorySerializer(transactions, many=True)

        return success_response(
            message="تاریخچه تراکنش‌ها دریافت شد",
            message_en="Transaction history retrieved",
            extra_data={
                "user_id": request.user.id,
                "transactions": serializer.data
            }
        )


