from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Reservation
from train.models import Ticket
from .serializers import ReservationSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


class ReservationCreateAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data["user"] = request.user.id

        ticket_id = data.pop("tickets")

        seat_number = data.pop("seat_number")

        if Reservation.objects.filter(
            tickets__id=ticket_id, seat_number=seat_number
        ).exists():
            return Response(
                {"error": "The selected seat is already reserved."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            ticket = Ticket.objects.get(id=ticket_id)
        except Ticket.DoesNotExist:
            return Response(
                {"error": "The selected ticket is not available."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        reservation_data = {
            "user": request.user.id,
            "tickets": ticket.id,
            "seat_number": seat_number,
            "number_of_tickets": data.get("number_of_tickets", 1),
        }

        serializer = ReservationSerializer(data=reservation_data)
        if serializer.is_valid():
            reservation = serializer.save()
            response_data = {**serializer.data, "total_price": reservation.total_price}

            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
