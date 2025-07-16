'''Checkout views.py'''
from django.shortcuts import render

def checkout(request):
    '''Returns checkout page'''
    return render(request, 'checkout/checkout.html')
