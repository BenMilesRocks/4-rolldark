'''Cart app contexts'''
from django.shortcuts import get_object_or_404
from dice.models import Dice

def cart_contents(request):
    '''Show content of cart'''

    cart_items = []
    total = 0
    product_count = 0
    delivery = 0
    cart = request.session.get('cart', {})

    for item_id, quantity in cart.items():
        product = get_object_or_404(Dice, pk=item_id)
        total += quantity * product.price
        product_count += quantity
        cart_items.append({
            'item_id': item_id,
            'quantity': quantity,
            'product': product,
        })
        if product.delivery_charge:
            delivery = 2.50

    grand_total = delivery + total

    context = {
        'cart_items': cart_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'grand_total': grand_total,
    }

    return context
