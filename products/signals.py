from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product


@receiver(post_save, sender=Product)
def product_saved(sender, instance, created, **kwargs):
    if created:
        print(f"New product created: {instance.name}")
    else:
        print(f"Product updated: {instance.name}")
