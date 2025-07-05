'''Dice Admin.py'''
from django.contrib import admin
from .models import Dice, Category

class DiceAdmin(admin.ModelAdmin):
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

admin.site.register(Dice, DiceAdmin)
admin.site.register(Category, CategoryAdmin)
