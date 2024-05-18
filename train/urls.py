from django.urls import path
from .views import TicketListAPIView, TicketDeleteAPIView

urlpatterns = [
    path('tickets/', TicketListAPIView.as_view(), name='ticket-list'),
    path('tickets/<int:pk>/', TicketDeleteAPIView.as_view(), name='ticket-delete'),

]
