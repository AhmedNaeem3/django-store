from celery import shared_task
from django.core.mail import send_mail


@shared_task
def add_numbers(a, b):
    return a + b


@shared_task
def send_welcome_email(user_email, username):
    subject = "Welcome to Our Store!"

    message = (
        f"Hello {username},\n\n"
        "Welcome to our store! "
        "We're happy to have you with us."
    )

    send_mail(
        subject=subject,
        message=message,
        from_email=None,
        recipient_list=[user_email],
        fail_silently=False,
    )

    return f"Welcome email sent to {user_email}"
