'''Products app views'''
from django.shortcuts import render

from .models import Product

def all_products(request):
    """View to return products page"""

    products = Product.objects.all() # pylint: disable=E1101

    context = {
        'products':products,
    }

    return render(request, 'products/products.html', context)
