'''Products app views'''
from django.shortcuts import render

def all_products(request):
    """View to return products page"""

    return render(request, 'products/products.html')
