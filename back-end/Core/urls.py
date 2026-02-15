from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthViewSet, HomeAPIView
from rest_framework.permissions import AllowAny
from .views import (
    AuthViewSet,
    HomeAPIView,
    DoctorsListAPIView,
    DoctorDetailAPIView,
    ReservationCreateAPIView,
    UserReservationsAPIView,
    ReservationDeleteAPIView,
    CommentCreateAPIView,
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

        # Home
        path('home/', HomeAPIView.as_view()),

        # Doctors
        path('doctors/', DoctorsListAPIView.as_view()),
        path('doctors/<int:pk>/', DoctorDetailAPIView.as_view()),

        # Reservations
        # path('reservations/', UserReservationsAPIView.as_view()),        # GET

        path('reservations/<int:user_id>/', UserReservationsAPIView.as_view(), name='user-reservations'),

        path('reservations/create/', ReservationCreateAPIView.as_view()), # POST
        path('reservations/<int:pk>/', ReservationDeleteAPIView.as_view()), # DELETE

        # Comments
        path('comments/create/', CommentCreateAPIView.as_view()),
    ])),
]
