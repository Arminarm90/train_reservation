from django.db import models
from accounts.models import User


class Station(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Route(models.Model):
    origin = models.ForeignKey(
        Station, related_name="origin_routes", on_delete=models.CASCADE
    )
    destination = models.ForeignKey(
        Station, related_name="destination_routes", on_delete=models.CASCADE
    )
    distance = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.DurationField()

    def __str__(self):
        return f"{self.origin} to {self.destination}"


class Train(models.Model):
    train_number = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    capacity = models.IntegerField()

    def __str__(self):
        return self.name


class Schedule(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    def __str__(self):
        return f"{self.train} - {self.route} - {self.departure_time} to {self.arrival_time}"


class Ticket(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10)
    is_reserved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.schedule} - Seat: {self.seat_number}"


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tickets = models.ManyToManyField(Ticket)
    status_choices = [("reserved", "Reserved"), ("paid", "Paid")]
    status = models.CharField(max_length=10, choices=status_choices, default="reserved")

    def __str__(self):
        return f"{self.user.username} - {self.status}"
