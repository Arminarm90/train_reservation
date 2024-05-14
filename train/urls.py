from django.urls import path
from .views import TicketListAPIView

urlpatterns = [
    path('tickets/', TicketListAPIView.as_view(),'tickets')
]
