from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from rest_framework import viewsets
from .models import Hotel, Room, Reservation
from .serializers import HotelSerializer, RoomSerializer, ReservationSerializer

def hotels(request):
    myhotels = Hotel.objects.all().values()
    template = loader.get_template('hotel_list_view.html')
    context = {
        'myhotels': myhotels,
    }
    return HttpResponse(template.render(context, request))

def hotel_rooms(request, pk):
    hotel = Hotel.objects.get(pk=pk)
    rooms = hotel.rooms.all()
    return render(request, "hotel_list.html", {
        "hotel": hotel,
        "rooms": rooms
    })

def roomdetailview(request, id):
    myroom = Room.objects.get(id=id)
    template = loader.get_template('room_detail.html')
    context = {
        'myroom': myroom,
    }
    return HttpResponse(template.render(context, request))

class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def perform_create(self, serializer):
        reservation = serializer.save()
        room = reservation.room
        if room.is_available:
            room.is_available = False
            room.save()

def main(request):
    template = loader.get_template('main.html')
    return HttpResponse(template.render())

def testing(request):
  template = loader.get_template('template.html')
  context = {
    'fruits': ['Apple', 'Banana', 'Cherry'],   
  }
  return HttpResponse(template.render(context, request))
