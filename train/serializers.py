from .models import Station, Schedule, Route, Train, Ticket, User
from rest_framework import serializers

class TicketSerializer(serializers.ModelSerializer):
        class Meta:
            model = Ticket
            fields = '__all__'