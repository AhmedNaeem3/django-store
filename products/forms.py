from django import forms
from .models import Product
from .validators import validate_price_and_stock
from django.core.exceptions import ValidationError


class ProductForm(forms.ModelForm):
    # name = forms.CharField(max_length=100)
    # price = forms.DecimalField(min_value=0.01)
    # stock = forms.IntegerField(min_value=0)

    class Meta:
        model = Product
        fields = ["name", "price", "stock", "category"]

    def clean_name(self):
        name = self.cleaned_data["name"]

        if "test" in name.lower():
            raise forms.ValidationError("Product name cannot contain the word 'test'.")

        return name

    def clean(self):
        cleaned_data = super().clean()

        price = cleaned_data.get("price")
        stock = cleaned_data.get("stock")

        try:
            validate_price_and_stock(price, stock)
        except ValidationError as error:
            raise forms.ValidationError(error.messages)

        return cleaned_data
