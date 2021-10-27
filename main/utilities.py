from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import CartOrder, CartOrderItems


def notify_vendor(orderaddress):
    from_email = settings.DEFAULT_EMAIL_FROM

 
    to_email = orderaddress.vendor
    subject = 'New order'
    text_content = 'You have a new order!'
    html_content = render_to_string('main/email_notify_vendor.html', {'order': orderaddress})

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

def notify_customer(items):
    from_email = settings.DEFAULT_EMAIL_FROM

    to_email = items.user.email
    subject = 'Order confirmation'
    text_content = 'Thank you for the order!'
    html_content = render_to_string('main/email_notify_customer.html', {'order': items})

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()