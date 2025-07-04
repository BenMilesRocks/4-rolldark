'''Cart app views'''
from django.shortcuts import render, redirect
from django.contrib import messages

from products.models import Product

def view_cart(request):
    '''Returns cart page'''
    return render(request, 'cart/cart.html')

def add_to_cart(request, item_id):
    '''Adds items to the cart'''

    # Fetch variables from page
    product = Product.objects.get(pk=item_id) #pylint: disable=E1101
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')

    # If cart exists in session fetches it, else create empty cart
    cart = request.session.get('cart', {})

    # Check if already in cart
    if item_id in list(cart.keys()):
        # If in cart, increment quantity
        cart[item_id] += quantity
    else:
        # If not, add new key to cart
        cart[item_id] = quantity
        messages.success(request, f'Added {product.name} to your cart')

    # Pushes cart back to session
    request.session['cart'] = cart

    # Redirect to last page visited
    return redirect(redirect_url)
