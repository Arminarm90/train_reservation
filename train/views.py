from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Ticket
from rest_framework.response import Response
from .serializers import TicketSerializer


class TicketListAPIView(APIView):
    def get(self, request):
        # Get query parameters from the request
        train_name = request.GET.get("train_name")
        origin = request.GET.get("origin")
        destination = request.GET.get("destination")
        # Filter tickets based on the search criteria
        tickets = Ticket.objects.all()
        if train_name:
            tickets = tickets.filter(schedule__train__name__icontains=train_name)
        if origin:
            tickets = tickets.filter(schedule__route__origin__name__icontains=origin)
        if destination:
            tickets = tickets.filter(
                schedule__route__destination__name__icontains=destination
            )
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data)
