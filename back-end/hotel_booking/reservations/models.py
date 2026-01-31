from django.db import models

class Hotel(models.Model):
    name = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    stars = models.IntegerField()

    def __str__(self):
        return f"{self.name} - {self.city}"


class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="rooms")
    room_number = models.IntegerField()
    capacity = models.IntegerField()
    price_per_night = models.IntegerField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Room {self.room_number} ({self.hotel.name})"


class Reservation(models.Model):
    customer_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    check_in = models.DateField()
    check_out = models.DateField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.customer_name} - Room {self.room.room_number}"

