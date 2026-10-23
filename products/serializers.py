from django.db import transaction
from rest_framework import serializers
from .validators import validate_price_and_stock
from django.core.exceptions import ValidationError
from .models import Product, Category, Tag, ProductDetail
from django.contrib.auth.models import User
from products.tasks import send_welcome_email


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDetail
        fields = ["warranty_months", "weight_kg"]


# class ProductNestedSerializer(serializers.ModelSerializer):
#     category = CategorySerializer(read_only=True)
#     tags = TagSerializer(many=True, read_only=True)
#     detail = ProductDetailSerializer(read_only=True)

#     class Meta:
#         model = Product
#         fields = [
#             "id",
#             "name",
#             "price",
#             "stock",
#             "category",
#             "tags",
#             "detail",
#         ]


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        read_only_fields = ["id"]

    @transaction.atomic
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        transaction.on_commit(
            lambda: send_welcome_email.delay(user.email, user.username)
        )
        return user


class ProductSerializer(serializers.ModelSerializer):

    category = CategorySerializer(read_only=True)
    # tags = TagSerializer(many=True, read_only=True)
    # detail = ProductDetailSerializer(read_only=True)
    internal_note = serializers.CharField(write_only=True, required=False)
    tags = serializers.SlugRelatedField(
        many=True,
        slug_field="name",
        queryset=Tag.objects.all(),
        required=False,
    )

    detail = ProductDetailSerializer(required=False)

    category_name = serializers.SlugRelatedField(
        slug_field="name",
        queryset=Category.objects.all(),
        source="category",
        write_only=True,
    )

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

    @transaction.atomic
    def create(self, validated_data):
        tags = validated_data.pop("tags", [])
        detail_data = validated_data.pop("detail", None)

        # Create the main product
        product = Product.objects.create(**validated_data)

        # Assign existing tags
        product.tags.set(tags)

        # Create related details if provided
        if detail_data is not None:
            ProductDetail.objects.create(
                product=product,
                **detail_data,
            )

        return product

    @transaction.atomic
    def update(self, instance, validated_data):
        tags = validated_data.pop("tags", None)
        detail_data = validated_data.pop("detail", None)

        # Update ordinary Product fields
        for field, value in validated_data.items():
            setattr(instance, field, value)

        instance.save()

        # Update tags only if supplied
        if tags is not None:
            instance.tags.set(tags)

        # Create or update ProductDetail if supplied
        if detail_data is not None:
            detail, _ = ProductDetail.objects.get_or_create(product=instance)

            for field, value in detail_data.items():
                setattr(detail, field, value)

            detail.save()

        return instance

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "stock",
            "category",
            "category_name",
            "tags",
            "detail",
            "status",
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
