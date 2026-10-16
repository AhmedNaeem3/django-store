from django.contrib import admin
from .models import Product, Category, Tag, ProductDetail, ActivityLog

# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = ["name", "price", "stock", "status", "category"]
    list_filter = ["status", "category"]
    search_fields = ["name", "description"]

    fieldsets = [
        (
            "Product Information",
            {
                "fields": ["name", "description"],
            },
        ),
        (
            "Pricing and Inventory",
            {
                "fields": ["price", "stock"],
            },
        ),
        (
            "Classification",
            {
                "fields": ["category", "tags", "status"],
            },
        ),
    ]

    @admin.action(description="Activate selected products")
    def activate_products(self, request, queryset):
        queryset.update(status="active")

    @admin.action(description="Archieved selected products")
    def archieved_products(self, request, queryset):
        queryset.update(status="archived")

    @admin.action(description="Draft selected products")
    def draft_products(self, request, queryset):
        queryset.update(status="draft")

    actions = [
        "activate_products",
        "archieved_products",
        "draft_products",
    ]


admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(ProductDetail)
admin.site.register(ActivityLog)
