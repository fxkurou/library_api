from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_email_notification(email, subject, message):
    send_mail(
        subject,
        message,
        "noreply@library.com",
        [email],
        fail_silently=False,
    )
