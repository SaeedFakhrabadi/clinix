from django.contrib.auth import authenticate, get_user_model
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.db import IntegrityError

from .models import PasswordReset
from .serializers import (
    LoginSerializer,
    RegisterSerializer,
    ForgetPasswordSerializer,
    ResetPasswordSerializer,
    UserSerializer,
    MessageSerializer
)

import uuid

User = get_user_model()

def success_response(message_fa, message_en, code="success", status_code=status.HTTP_200_OK, extra_data=None):
    data = {
        "message": message_fa,
        "message_en": message_en,
        "code": code,
    }
    if extra_data:
        data.update(extra_data)
    return Response(data, status=status_code)


def error_response(message_fa, message_en, code="error", status_code=status.HTTP_400_BAD_REQUEST, extra_data=None):
    data = {
        "message": message_fa,
        "message_en": message_en,
        "code": code,
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

                refresh = RefreshToken.for_user(user)

                return success_response(
                    message_fa="ثبت‌نام با موفقیت انجام شد",
                    message_en="User registered successfully",
                    code="registration_success",
                    status_code=status.HTTP_201_CREATED,
                    extra_data={
                        "user": UserSerializer(user).data,
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    }
                )
            
            except IntegrityError as e:
                return error_response(
                    message_fa="مشخصات وارد شده تکراری است!",
                    message_en="The entered information is duplicate!",
                    code="duplicate_entry",
                    extra_data={
                        "detail": "شماره تلفن یا ایمیل قبلاً ثبت شده است.",
                        "detail_en": "Phone number or email is already registered.",
                        "db_error": str(e)
                    },
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            except Exception as e:
                # This should rarely happen now
                import traceback
                traceback.print_exc()  # ← print full stack trace to console
                return error_response(
                    message_fa="خطایی در ثبت‌نام رخ داد",
                    message_en="An error occurred during registration",
                    code="registration_failed"
                )
        
        return error_response(
            message_fa="داده‌های ارسالی معتبر نمی‌باشند",
            message_en="Invalid input data",
            code="validation_error",
            status_code=status.HTTP_400_BAD_REQUEST,
            extra_data={"errors": serializer.errors}
        )
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(
                message_fa="داده‌های ارسالی ناقص یا نامعتبر است",
                message_en="Invalid or incomplete input data",
                code="validation_error",
                extra_data={"errors": serializer.errors}
            )

        user = authenticate(
            request,
            identifier=serializer.validated_data['identifier'],   # ← use identifier
            password=serializer.validated_data['password']
        )

        if user:
            refresh = RefreshToken.for_user(user)
            return success_response(
                message_fa="ورود با موفقیت انجام شد",
                message_en="Login successful",
                code="login_success",
                extra_data={
                    "user": UserSerializer(user).data,
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            )

        return error_response(
            message_fa="اطلاعات وارد شده صحیح نمی‌باشند!",
            message_en="Invalid credentials!",
            code="invalid_credentials",
            status_code=status.HTTP_401_UNAUTHORIZED,
            extra_data={
                "detail": "ایمیل یا شماره تلفن یا رمز عبور اشتباه است.",
                "detail_en": "Email/phonenumber or password is incorrect."
            }
        )
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        refresh_token = request.data.get("refresh")
        
        if not refresh_token:
            return error_response(
                message_fa="توکن تازه‌سازی ارسال نشده است",
                message_en="Refresh token is required",
                code="missing_refresh_token",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            return success_response(
                message_fa="خروج با موفقیت انجام شد",
                message_en="Logout successful",
                code="logout_success"
            )
        
        except Exception as e:
            return error_response(
                message_fa="خطا در فرآیند خروج",
                message_en="Logout error",
                code="logout_failed",
                extra_data={"detail_en": str(e)},
                status_code=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['post'])
    def forgot_password(self, request):
        serializer = ForgetPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(
                message_fa="ایمیل نامعتبر است",
                message_en="Invalid email format",
                code="validation_error",
                extra_data={"errors": serializer.errors}
            )
        
        email = serializer.validated_data['email']
        
        try:
            user = User.objects.get(email=email)

            reset_id = uuid.uuid4()

            PasswordReset.objects.update_or_create(
                user=user,
                defaults={
                    "reset_id": reset_id,
                    "created_when": timezone.now()
                }
            )
            
            reset_url = f"{settings.FRONTEND_URL}/reset-password/{reset_id}"
            send_mail(
                subject='درخواست بازنشانی رمز عبور - Clinixs',
                message=f'سلام،\n\nبرای تغییر رمز عبور خود روی لینک زیر کلیک کنید:\n{reset_url}\n\nاین لینک ۱۰ دقیقه اعتبار دارد.\n\nبا احترام،\nتیم Clinixs',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )

            return success_response(
                message_fa="ایمیل بازنشانی رمز عبور ارسال شد",
                message_en="Password reset email sent",
                code="reset_email_sent"
            )
            
        except User.DoesNotExist:
            return error_response(
                message_fa="کاربری با این ایمیل یافت نشد",
                message_en="User with this email does not exist",
                code="user_not_found",
                status_code=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['post'])
    def reset_password(self, request):
        serializer = ResetPasswordSerializer(data=request.data)

        if not serializer.is_valid():
            return error_response(
                message_fa="داده‌های ارسالی نامعتبر است",
                message_en="Invalid input",
                code="validation_error",
                extra_data={"errors": serializer.errors}
            )
        
        reset_id = serializer.validated_data['reset_id']
        password = serializer.validated_data['password']
        
        try:
            password_reset = PasswordReset.objects.get(reset_id=reset_id)
            expiration_time = password_reset.created_when + timezone.timedelta(minutes=10)
            
            if timezone.now() > expiration_time:
                password_reset.delete()
                return error_response(
                    message_fa="لینک بازنشانی منقضی شده است",
                    message_en="Reset link has expired",
                    code="link_expired"
                )
            
            user = password_reset.user
            user.set_password(password)
            user.save()
            password_reset.delete()
            
            return success_response(
                message_fa="رمز عبور با موفقیت تغییر یافت",
                message_en="Password reset successfully",
                code="password_reset_success"
            )
            
        except PasswordReset.DoesNotExist:
            return error_response(
                message_fa="کد بازنشانی نامعتبر است",
                message_en="Invalid reset ID",
                code="invalid_reset_id",
                status_code=status.HTTP_404_NOT_FOUND
            )

class HomeAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return success_response(
            message_fa=f"خوش آمدید {request.user.username}",
            message_en=f"Welcome {request.user.username}",
            code="welcome",
            extra_data={"user": UserSerializer(request.user).data}
        )
