from rest_framework import viewsets, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import PasswordReset
from .serializers import (
    LoginSerializer, 
    RegisterSerializer, 
    ForgetPasswordSerializer, 
    ResetPasswordSerializer,
    UserSerializer
)
from rest_framework.permissions import AllowAny, IsAuthenticated
import uuid

class AuthViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'User registered successfully',
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'message': 'Login successful',
                    'user': UserSerializer(user).data,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            else:
                return Response(
                    {'error': 'Invalid credentials'}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Logout successful'})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def forgot_password(self, request):
        serializer = ForgetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            
            try:
                user = User.objects.get(email=email)
                reset_id = str(uuid.uuid4())
                
                # Create or update password reset entry
                password_reset, created = PasswordReset.objects.update_or_create(
                    user=user,
                    defaults={'reset_id': reset_id, 'created_when': timezone.now()}
                )
                
                # Send email (configure your email settings first)
                reset_url = f"{settings.FRONTEND_URL}/reset-password/{reset_id}"
                send_mail(
                    'Password Reset Request',
                    f'Click the link to reset your password: {reset_url}',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                
                return Response({
                    'message': 'Password reset email sent',
                    'reset_id': reset_id
                })
                
            except User.DoesNotExist:
                return Response(
                    {'error': 'User with this email does not exist'},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def reset_password(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            reset_id = serializer.validated_data['reset_id']
            password = serializer.validated_data['password']
            
            try:
                password_reset = PasswordReset.objects.get(reset_id=reset_id)
                
                # Check if reset link has expired (10 minutes)
                expiration_time = password_reset.created_when + timezone.timedelta(minutes=10)
                if timezone.now() > expiration_time:
                    password_reset.delete()
                    return Response(
                        {'error': 'Reset link has expired'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # Update user password
                user = password_reset.user
                user.set_password(password)
                user.save()
                
                # Delete the used reset entry
                password_reset.delete()
                
                return Response({'message': 'Password reset successfully'})
                
            except PasswordReset.DoesNotExist:
                return Response(
                    {'error': 'Invalid reset ID'},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ModelViewSet):
    """
    For user management (admin only)
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

# API Views (alternative approach)
class HomeAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({
            'message': f'Welcome {request.user.username}',
            'user': UserSerializer(request.user).data
        })
    

