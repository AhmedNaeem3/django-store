from django.core.management.base import BaseCommand
from products.models import Product


class Command(BaseCommand):
    help = "List all products in the database and filter them by status if provided."

    def add_arguments(self, parser):
        parser.add_argument(
            "--status",
            type=str,
            default=None,
            help="Filter products by status (active or draft)",
        )

    def handle(self, *args, **options):
        status = options["status"]

        products = Product.objects.all()

        if status:
            products = products.filter(status=status)

        if not products.exists():
            self.stdout.write("No products found.")
            return

        for product in products:
            self.stdout.write(
                f"{product.name} | "
                f"Price: {product.price} | "
                f"Stock: {product.stock} | "
                f"Status: {product.status}"
            )
