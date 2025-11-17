from django.contrib import admin
from .models import Product, Order, OrderItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "price")
    search_fields = ("name", "category")
    list_filter = ("category",)
    fields = ("name", "category", "price", "image_name")
    list_editable = ("price", "category")
    ordering = ("id",)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "total_quantity", "total_price", "created_at")
    list_filter = ("status", "created_at")
    inlines = [OrderItemInline]
    readonly_fields = ("total_quantity", "total_price", "created_at")
    fields = ("user", "status", "total_quantity", "total_price", "created_at")
