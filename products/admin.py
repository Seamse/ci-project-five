from django.contrib import admin
from .models import Product, Category


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'category',
        'name',
        'country',
        'vintage',
        'price',
        'rating',
        'image',
    )

    ordering = ('sku',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
