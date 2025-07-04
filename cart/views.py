'''Cart app views'''
from django.shortcuts import render, redirect
from django.contrib import messages

from products.models import Product

def view_cart(request):
    '''Returns cart page'''
    return render(request, 'cart/cart.html')

def add_to_bag(request, item_id):
    '''Adds items to the bag'''

    # Fetch variables from page
    product = Product.objects.get(pk=item_id) #pylint: disable=E1101
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')

    # If bag exists in session fetches it, else create empty bag
    bag = request.session.get('bag', {})

    # Check if already in bag
    if item_id in list(bag.keys()):
        # If in bag, increment quantity
        bag[item_id] += quantity
    else:
        # If not, add new key to bag
        bag[item_id] = quantity
        messages.success(request, f'Added {product.name} to your bag')

    # Pushes bag back to session
    request.session['bag'] = bag

    # Redirect to last page visited
    return redirect(redirect_url)
