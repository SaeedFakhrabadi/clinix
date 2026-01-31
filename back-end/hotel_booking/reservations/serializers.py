from rest_framework import serializers
from .models import Hotel, Room, Reservation

class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'

class RoomSerializer(serializers.ModelSerializer):
    hotel = serializers.PrimaryKeyRelatedField(queryset=Hotel.objects.all())
    hotel_name = serializers.CharField(source='hotel.name', read_only=True)

    class Meta:
        model = Room
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())
    room_number = serializers.CharField(source='room.room_number', read_only=True)
    hotel_name = serializers.CharField(source='room.hotel.name', read_only=True)

    class Meta:
        model = Reservation
        fields = '__all__'
