from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.permissions import AllowAny
from .views import (
    AuthViewSet,
    DoctorsListAPIView,
    DoctorDetailAPIView,
    ReservationCreateAPIView,
    UserReservationsAPIView,
    ReservationDeleteAPIView,
    EditProfileAPIView,
    CommentCreateAPIView, NotificationsListAPIView, TransactionCreateAPIView, TransactionHistoryAPIView,
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
    path('api/v1/', include([
        path('', router.get_api_root_view(), name='api-root'),
        path('', include(router.urls)),

        # Doctors
        path('doctors/', DoctorsListAPIView.as_view()),
        path('doctors/<int:pk>/', DoctorDetailAPIView.as_view()),

        # Reservations
        path('reservations/', UserReservationsAPIView.as_view(), name='user-reservations'),
        path('reservations/create/', ReservationCreateAPIView.as_view()), # POST
        path('reservations/delete/<int:pk>/', ReservationDeleteAPIView.as_view()), # DELETE

        # Comments
        path('comments/create/', CommentCreateAPIView.as_view()),

        # Notifications
        path('notifications/', NotificationsListAPIView.as_view(), name='notifications-list'),

        # Transactions
        path('transactions/create/', TransactionCreateAPIView.as_view(), name='transaction-create'), # POST
        path('transactions/history/', TransactionHistoryAPIView.as_view(), name='transaction-history'), # GET

        path('edit_profile/', EditProfileAPIView.as_view(), name='edit_profile'),

    ])),
]
