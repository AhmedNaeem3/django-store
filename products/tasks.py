from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .models import Product


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


@shared_task
def send_daily_summary_email():
    total_users = User.objects.count()
    total_products = Product.objects.count()

    subject = "Daily Store Summary"

    message = (
        "Here is your daily store summary:\n\n"
        f"Total registered users: {total_users}\n"
        f"Total products: {total_products}\n"
    )

    send_mail(
        subject=subject,
        message=message,
        from_email=None,
        recipient_list=[settings.DEFAULT_FROM_EMAIL],
        fail_silently=False,
    )

    return f"Daily summary sent. " f"Users: {total_users}, Products: {total_products}"
