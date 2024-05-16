from rest_framework import serializers
from .models import Reservation
from train.models import Ticket


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ["user", "tickets", "seat_number", "number_of_tickets"]
