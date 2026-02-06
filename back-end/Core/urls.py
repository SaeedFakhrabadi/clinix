from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthViewSet, HomeAPIView
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from rest_framework.permissions import AllowAny

# Custom router to allow anonymous access to root
class CustomRouter(DefaultRouter):
    def get_api_root_view(self, api_urls=None, **kwargs):
        view = super().get_api_root_view(api_urls=api_urls, **kwargs)
        view.cls.permission_classes = [AllowAny]
        return view

router = CustomRouter()
router.register(r'auth', AuthViewSet, basename='auth')

urlpatterns = [
    path('api/v1/', include([
        path('', router.get_api_root_view(), name='api-root'),
        path('', include(router.urls)),
        
        # Standard JWT endpoints
        path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    ])),
]
