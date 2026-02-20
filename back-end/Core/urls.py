from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.permissions import AllowAny
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    AuthViewSet,
    DoctorsListAPIView,
    DoctorDetailAPIView,
    ReservationCreateAPIView,
    UserReservationsAPIView,
    ReservationDeleteAPIView,
    EditProfileAPIView,
    CommentCreateAPIView, NotificationsListAPIView, TransactionCreateAPIView, TransactionHistoryAPIView,
    ComplaintAPIView, WalletBalanceAPIView, WalletDepositAPIView, WalletWithdrawAPIView,
)

# Custom router to allow anonymous access to root
class CustomRouter(DefaultRouter):
    def get_api_root_view(self, api_urls=None, **kwargs):
        view = super().get_api_root_view(api_urls=api_urls, **kwargs)
        view.cls.permission_classes = [AllowAny]
        return view

router = CustomRouter()
router.register(r'auth', AuthViewSet, basename='auth')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include([
        path('', router.get_api_root_view(), name='api-root'),
        path('', include(router.urls)),

        # Doctors
        path('doctors/', DoctorsListAPIView.as_view()),
        path('doctors/<int:pk>/', DoctorDetailAPIView.as_view()),

        # Reservations
        path('reservations/', UserReservationsAPIView.as_view(), name='user-reservations'),
        path('reservations/create/', ReservationCreateAPIView.as_view()),
        path('reservations/delete/<int:pk>/', ReservationDeleteAPIView.as_view()),

        # Comments
        path('comments/create/', CommentCreateAPIView.as_view()),

        # Notifications
        path('notifications/', NotificationsListAPIView.as_view(), name='notifications-list'),

        # Transactions
        path('transactions/create/', TransactionCreateAPIView.as_view(), name='transaction-create'),
        path('transactions/history/', TransactionHistoryAPIView.as_view(), name='transaction-history'),

        # Edit Profile
        path('edit_profile/', EditProfileAPIView.as_view(), name='edit_profile'),

        # Complaint
        path('complaint/', ComplaintAPIView.as_view(), name='complaint'),

        # Wallet
        path('wallet/balance/',  WalletBalanceAPIView.as_view(),  name='wallet-balance'),
        path('wallet/deposit/',  WalletDepositAPIView.as_view(),  name='wallet-deposit'),
        path('wallet/withdraw/', WalletWithdrawAPIView.as_view(), name='wallet-withdraw'),
    ])),
]

# Media files — must be OUTSIDE the include() block
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
