from django import forms
from shop.models import Product, Order


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "price",
            "stock_quantity",
            "category",
        ]

class OrderStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["status"]
