from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator
from .validators import validate_product_name
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


# AbstractModel
class BaseProduct(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Product(BaseProduct):

    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("active", "Active"),
        ("archived", "Archived"),
    ]
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
    )

    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="products",
    )

    name = models.CharField(
        max_length=100,
        validators=[validate_product_name],
    )

    description = models.TextField(
        blank=True,
        help_text="Optional description of the product.",
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )

    stock = models.PositiveIntegerField(default=0)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="draft",
    )

    def __str__(self):
        return self.name

    def is_in_stock(self):
        return self.stock > 0

    def calculate_stock_value(self):
        return self.price * self.stock

    # It's main purpose is to provide a way to access a method as an attribute.
    @property
    def stock_value(self):
        return self.price * self.stock

    # It works with the class itself, and it can be called on the class without creating an instance. It can work all over the class.
    @classmethod
    def get_active_products(cls):
        return cls.objects.filter(status="active")

    # It works with the argument passed to the method, and it does not depend on the instance or class state. It is a utility function that can be called without creating an instance of the class.
    @staticmethod
    def is_valid_price(price):
        return price > 0

    def __repr__(self):
        return f"Product(id={self.pk}, name={self.name!r})"

    class Meta:
        ordering = ["price"]
        verbose_name = "Store Product"
        verbose_name_plural = "Store Products"
        db_table = "products"

        constraints = [
            models.UniqueConstraint(
                fields=["name"],
                name="unique_product_name",
            ),
        ]

        indexes = [
            models.Index(
                fields=["status"],
                name="product_status_idx",
            ),
        ]


class ProductDetail(models.Model):
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name="detail",
    )
    warranty_months = models.PositiveIntegerField(default=0)
    weight_kg = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0,
    )

    def __str__(self):
        return f"Details for {self.product.name}"


class ExpensiveProduct(Product):
    class Meta:
        proxy = True
        ordering = ["-price"]
        verbose_name = "Expensive Product"
        verbose_name_plural = "Expensive Products"


class ActivityLog(models.Model):
    action = models.CharField(max_length=255)

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
    )

    object_id = models.PositiveIntegerField()

    content_object = GenericForeignKey(
        "content_type",
        "object_id",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.action
