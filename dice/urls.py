"""URL configuration for Dice app"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_dice, name='dice'),
    path('<dice_id>', views.dice_detail, name='dice_detail')
]
