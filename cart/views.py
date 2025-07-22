'''Cart app views'''
from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from django.contrib import messages

from products.models import Product
from dice.models import Dice

def view_cart(request):
    '''Returns cart page'''
    return render(request, 'cart/cart.html')

def add_dice_to_cart(request, item_id):
    '''Adds Dice to the cart'''

    # Fetch variables from page
    product = Dice.objects.get(pk=item_id) #pylint: disable=E1101
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

    print(request.session['cart'])

    # Redirect to last page visited
    return redirect(redirect_url)

def add_game_to_cart(request, item_id):
    '''Adds Games to the cart, allowing custom formating specific to games'''

    # Fetch variables from page
    product = Product.objects.get(pk=item_id) #pylint: disable=E1101
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    if request.POST.get(f'option_{product}') == 'campaign_ticket':
        ticket_option = 'campaign_ticket'
    else:
        ticket_option = request.POST.get(f'option_{product}')

    # If cart exists in session fetches it, else create empty cart
    cart = request.session.get('cart', {})

    # Check if already in cart
    if item_id in list(cart.keys()):
        # If in cart, check if ticket option in cart
        if ticket_option in cart[item_id]['game_by_ticket_option'].keys():
            # If in cart, increment quantity
            cart[item_id]['game_by_ticket_option'][ticket_option] += quantity
        else:
            # Else add ticket option to game ID
            cart[item_id]['game_by_ticket_option'][ticket_option] = quantity
    else:
        # If not, add new key to cart
        cart[item_id] = {'game_by_ticket_option': {ticket_option: quantity}}
        messages.success(request, f'Added {product.name} to your cart')

    # Pushes cart back to session
    request.session['cart'] = cart

    # Redirect to last page visited
    return redirect(redirect_url)

def adjust_cart(request, item_id):
    '''Amends the number of items in the cart'''

    # Fetch variables from page
    quantity = int(request.POST.get('quantity'))

    # If cart exists in session fetches it, else create empty cart
    cart = request.session.get('cart', {})

    # Update quantity
    if quantity > 0:
        cart[item_id] = quantity
    else:
        cart.pop(item_id)
    # Pushes cart back to session
    request.session['cart'] = cart

    # Redirect to last page visited
    return redirect(reverse('view_cart'))

def remove_from_cart(request, item_id):
    '''Deletes item from cart'''

    try:
        # If cart exists in session fetches it, else create empty cart
        cart = request.session.get('cart', {})

        cart.pop(item_id)

        # Pushes cart back to session
        request.session['cart'] = cart

        # Redirect to last page visited
        return HttpResponse(status=200)

    except Exception as e: #pylint: disable=W0612,W0718
        return HttpResponse(status=500)
