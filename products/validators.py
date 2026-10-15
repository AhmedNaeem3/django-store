from django.core.exceptions import ValidationError


def validate_product_name(value):
    if len(value.strip()) < 3:
        raise ValidationError("Product name must contain at least 3 characters.")
