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
    price = models.DecimalField(max_digits=10, decimal_places=2,default=1000.00)

    def __str__(self):
        return f"{self.schedule} - Seat: {self.seat_number}"


# class Reservation(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     tickets = models.ForeignKey(Ticket, on_delete=models.CASCADE)
#     number_of_tickets = models.IntegerField(default=1)  # Number of tickets in the reservation
#     total_price = models.DecimalField(max_digits=15, decimal_places=2, default=0)  # Total price of the reservation
#     status_choices = [('reserved', 'Reserved'), ('paid', 'Paid')]
#     status = models.CharField(max_length=10, choices=status_choices, default='reserved')

#     def calculate_total_price(self):
#         return sum(ticket.price for ticket in self.tickets.all()) * self.number_of_tickets

#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)  # Save the reservation first
#         self.total_price = self.calculate_total_price()  # Calculate total price after saving
#         super().save(*args, **kwargs)  # Save again to update the total price

#     def __str__(self):
#         return f"{self.user.email} - {self.status} - Total Price: {self.total_price}"