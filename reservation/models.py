from django.db import models
from train.models import Station, Schedule, Route, Ticket, Train
from accounts.models import User

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tickets = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    number_of_tickets = models.IntegerField(default=1)  # Number of tickets in the reservation
    total_price = models.DecimalField(max_digits=15, decimal_places=2, default=0)  # Total price of the reservation
    status_choices = [('reserved', 'Reserved'), ('paid', 'Paid')]
    status = models.CharField(max_length=10, choices=status_choices, default='reserved')

    def calculate_total_price(self):
        return sum(ticket.price for ticket in self.tickets.all()) * self.number_of_tickets

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the reservation first
        self.total_price = self.calculate_total_price()  # Calculate total price after saving
        super().save(*args, **kwargs)  # Save again to update the total price

    def __str__(self):
        return f"{self.user.email} - {self.status} - Total Price: {self.total_price}"
