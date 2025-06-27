'''Products Admin.py'''
from django.contrib import admin
from .models import Product, Category

class ProductAdmin(admin.ModelAdmin):
    '''Admin class for Products'''
    list_display = (
        'sku',
        'name',
        'category',
        'price',
        'image'
    )

    ordering = ('sku',)

class CategoryAdmin(admin.ModelAdmin):
    '''Admin class for Categories'''
    list_display = (
        'friendly_name','name',        
    )

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
