from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price')
    search_fields = ('name', 'category')
    list_filter = ('category',)
    fields = ('name', 'category', 'price', 'image_name')
    list_editable = ('price', 'category')
    ordering = ('id',)
                  