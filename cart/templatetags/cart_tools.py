'''Tools for the cart page'''
from django import template

register = template.Library()

@register.filter(name='calc_subtotal')
def calc_subtotal(price, quantity):
    '''calculate subtotal for cart items'''
    return price * quantity
