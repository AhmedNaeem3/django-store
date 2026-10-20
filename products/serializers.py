from rest_framework import serializers
from .models import Product
from .validators import validate_price_and_stock
from django.core.exceptions import ValidationError


class ProductSerializer(serializers.ModelSerializer):

    internal_note = serializers.CharField(write_only=True, required=False)

    # in_stock = serializers.SerializerMethodField()
    # def get_in_stock(self, obj):
    #     return obj.is_in_stock()

    # Calling function with source
    in_stock = serializers.BooleanField(source="is_in_stock", read_only=True)

    def validate(self, attrs):
        price = attrs.get("price", getattr(self.instance, "price", None))
        stock = attrs.get("stock", getattr(self.instance, "stock", None))

        try:
            validate_price_and_stock(price, stock)
        except ValidationError as error:
            raise serializers.ValidationError({"stock": error.messages})

        return attrs

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "stock",
            "category",
            "status",
            "tags",
            "in_stock",
            "internal_note",
        ]
        read_only_fields = ["id", "in_stock"]


# serializer = ProductSerializer(
#     data={
#         "name": "Wireless Mouse",
#         "price": "25.99",
#         "stock": 10,
#         "status": "active",
#         "category": 1,
#         "tags": [],
#     }
# )

# serializer.is_valid(raise_exception=True)
# product = serializer.save()


class ProductHyperlinkedSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = [
            "url",
            "name",
            "price",
            "stock",
            "category",
            "status",
            "tags",
        ]
