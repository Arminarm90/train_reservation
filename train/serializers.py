from .models import Station, Schedule, Route, Train, Ticket, User
from rest_framework import serializers

class TicketSerializer(serializers.ModelSerializer):
    train_name = serializers.CharField(source='schedule.train.name')
    train_type = serializers.CharField(source='schedule.train.type')
    origin = serializers.CharField(source='schedule.route.origin.name')
    destination = serializers.CharField(source='schedule.route.destination.name')
    capacity = serializers.IntegerField(source='schedule.train.capacity')
    duration = serializers.DurationField(source='schedule.route.duration')
    distance = serializers.DecimalField(max_digits=10, decimal_places=2, source='schedule.route.distance')
    price = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Ticket
        fields = ['id', 'train_name','train_type', 'origin', 'destination', 'capacity', 'duration', 'distance', 'price']