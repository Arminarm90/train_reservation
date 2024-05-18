
from django.core.mail import send_mail
from django.conf import settings

def send_reservation_email(user_email, reservation):
    subject = 'Your Reservation Confirmation'
    message = f'Dear {reservation.user.email},\n\n' \
              f'Thank you for your reservation. Here are the details:\n\n' \
              f'Ticket: {reservation.ticket.schedule}\n' \
              f'Seat Number: {reservation.seat_number}\n' \
              f'Number of Tickets: {reservation.number_of_tickets}\n' \
              f'Total Price: {reservation.total_price}\n' \
              f'Status: {reservation.status}\n\n' \
              f'We hope you enjoy your journey!\n' \
              f'Thank you!'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user_email]
    
    send_mail(subject, message, email_from, recipient_list)
