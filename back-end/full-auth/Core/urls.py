from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import AuthViewSet, UserViewSet, HomeAPIView

router = DefaultRouter()
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'users', UserViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/home/', HomeAPIView.as_view(), name='home-api'),
    path('api/auth/login/', AuthViewSet.as_view({'post': 'login'}), name='login-api'),
    path('api/auth/register/', AuthViewSet.as_view({'post': 'register'}), name='register-api'),
    path('api/auth/logout/', AuthViewSet.as_view({'post': 'logout'}), name='logout-api'),
    path('api/auth/forgot-password/', AuthViewSet.as_view({'post': 'forgot_password'}), name='forgot-password-api'),
    path('api/auth/reset-password/', AuthViewSet.as_view({'post': 'reset_password'}), name='reset-password-api'),
]
