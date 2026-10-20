from django.core.exceptions import ValidationError


def validate_product_name(value):

    if len(value.strip()) < 3:
        raise ValidationError("Product name must contain at least 3 characters.")

    if "test" in value.lower():
        raise ValidationError("Product name cannot contain the word 'test'.")


def validate_price_and_stock(price, stock):
    if price is not None and stock is not None:
        if price > 1000 and stock == 0:
            raise ValidationError("An expensive product cannot have zero stock.")
