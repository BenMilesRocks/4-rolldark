'''Cart app views'''
from django.shortcuts import render

def view_cart(request):
    '''Returns cart page'''
    return render(request, 'cart/cart.html')
