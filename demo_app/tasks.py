import logging
from celery import shared_task
from django.core.mail import send_mail

logger = logging.getLogger(__name__)

@shared_task
def send_email_task(subject, message, recipient_list):
    logger.info(f"Received arguments - Subject: {subject}, Message: {message}, Recipients: {recipient_list}")
    send_mail(
        subject,
        message,
        'demoapp2345@gmail.com',  # Sender Email
        recipient_list,
        fail_silently=False,
    )
    return "Email Sent"
