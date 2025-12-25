from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, ProductCategory, Product, Order, OrderItem


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("is_employee",)
    list_filter = UserAdmin.list_filter + ("is_employee",)
    fieldsets = UserAdmin.fieldsets + (
        ("Additional info", {"fields": ("is_employee",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Additional info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "is_employee",
                )
            },
        ),
    )


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "category", "stock_quantity")
    search_fields = ("name",)
    list_filter = ("category",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created_at", "status")
    list_filter = ("status", "created_at")
    search_fields = ("user__username",)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "order__user", "product", "quantity", "order__status")
    list_filter = ("product",)
