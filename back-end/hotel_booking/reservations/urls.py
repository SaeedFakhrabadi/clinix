from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import HotelViewSet, RoomViewSet, ReservationViewSet

router = DefaultRouter()
router.register(r'hotels', HotelViewSet)
router.register(r'rooms', RoomViewSet)
router.register(r'reservations', ReservationViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.main, name='main'),
    path('admin/', admin.site.urls),
    path("hotels/", views.hotels, name="hotel-list"),
    path("hotels/<int:pk>/", views.hotel_rooms, name="hotel-rooms"),
    path("rooms/<int:pk>/", views.roomdetailview, name="room-detail"),
    path('testing/', views.testing, name='testing'),
]
