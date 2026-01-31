from django.contrib import admin
from .models import Hotel, Room, Reservation

@admin.register(Hotel)
class AdminHotels(admin.ModelAdmin):
    list_display = ("name", "city", "address", "stars")

@admin.register(Room)
class AdminRooms(admin.ModelAdmin):
    list_display = ("hotel", "room_number", "capacity", "price_per_night", "is_available")
    raw_id_fields = ("hotel",)

@admin.register(Reservation)
class AdminReservations(admin.ModelAdmin):
    list_display = ("customer_name", "phone_number", "check_in", "check_out", "room")
    search_fields = ("customer_name",)
    list_filter = ("room__hotel__name", "room__is_available")

