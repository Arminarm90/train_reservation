from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Reservation
from .utils import send_reservation_email
from train.models import Ticket
from .serializers import ReservationSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings
import simplejson as json
import requests

# zarinpal
# ? sandbox merchant
if settings.SANDBOX:
    sandbox = "sandbox"
else:
    sandbox = "www"

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = (
    f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
)
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"


amount = 1000  # Rial / Required
description = "Description"  # Required
phone = "YOUR_PHONE_NUMBER"  # Optional
# Important: need to edit for realy server.
CallbackURL = "http://127.0.0.1:8000/api/tickets/"


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
        # data for zarinpal

        serializer = ReservationSerializer(data=reservation_data)
        if serializer.is_valid():
            reservation = serializer.save()
            data_zarin = {
                "MerchantID": settings.MERCHANT,
                "Amount": reservation.total_price,
                "Description": description,
                "Email": request.user.email,
                "CallbackURL": CallbackURL,
            }
            data_zarin = json.dumps(data_zarin)
            headers = {
                "content-type": "application/json",
                "content-length": str(len(data)),
            }
            # zarinpal
            try:
                response = requests.post(
                    ZP_API_REQUEST, data=data_zarin, headers=headers, timeout=10
                )
                if response.status_code == 200:
                    response_data = response.json()
                    if response_data["Status"] == 100:
                        send_reservation_email(request.user.email, reservation)
                        return Response(
                            {
                                **serializer.data,
                                "total_price": reservation.total_price,
                                # "status": True,
                                "payment_url": ZP_API_STARTPAY
                                + str(response_data["Authority"]),
                                # "authority": response_data["Authority"],
                            },
                            status=status.HTTP_200_OK,
                        )
                    else:
                        return Response(
                            {"status": False, "code": str(response_data["Status"])},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
            except requests.exceptions.Timeout:
                return Response(
                    {"status": False, "code": "timeout"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            except requests.exceptions.ConnectionError:
                return Response(
                    {"status": False, "code": "connection error"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        authority = request.query_params.get("authority")
        if authority:
            data = {
                "MerchantID": settings.MERCHANT,
                "Amount": amount,
                "Authority": authority,
            }
            data = json.dumps(data)
            headers = {
                "content-type": "application/json",
                "content-length": str(len(data)),
            }
            response = requests.post(settings.ZP_API_VERIFY, data=data, headers=headers)
            if response.status_code == 200:
                response_data = response.json()
                if response_data["Status"] == 100:
                    return Response(
                        {"status": True, "RefID": response_data["RefID"]},
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        {"status": False, "code": str(response_data["Status"])},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"status": False, "code": "authority not provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )
