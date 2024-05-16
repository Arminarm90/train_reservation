from django.db import models
from train.models import Station, Schedule, Route, Ticket, Train
from accounts.models import User


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tickets = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    number_of_tickets = models.IntegerField(default=1)
    total_price = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    seat_number = models.CharField(max_length=10)
    status_choices = [("reserved", "Reserved"), ("paid", "Paid")]
    status = models.CharField(max_length=10, choices=status_choices, default="reserved")

    def save(self, *args, **kwargs):
        # Calculate total price
        self.total_price = self.number_of_tickets * self.tickets.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.email} - {self.seat_number} - {self.status} - Total Price: {self.total_price}"
