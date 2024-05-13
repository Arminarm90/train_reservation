from django.contrib import admin
from .models import Station, Route, Schedule, Train, Ticket, Reservation

admin.site.register(Station)
admin.site.register(Route)
admin.site.register(Schedule)
admin.site.register(Train)
admin.site.register(Ticket)
admin.site.register(Reservation)
