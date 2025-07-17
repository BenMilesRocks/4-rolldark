'''Checkout views.py'''
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.conf import settings

import stripe

from products.models import Product
from cart.contexts import cart_contents
from .forms import OrderForm
from .models import Order, OrderLineItem

def checkout(request):
    '''Checkout view. Pulls cart from session, else displays error'''

    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        cart = request.session.get('cart', {})

        # Call form data
        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }

        # Create OrderForm object, using form data as an argument
        order_form = OrderForm(form_data)

        if order_form.is_valid():

            order = order_form.save()

            # Iterate through the cart, create line items for each
            for item_id, item_data in cart.items():

                try:
                    product = Product.objects.get(id=item_id) #pylint: disable = E1101
                    order_line_item = OrderLineItem(
                        order=order,
                        product=product,
                        quantity=item_data,
                    )
                    order_line_item.save()


                except Product.DoesNotExist: #pylint: disable = E1101
                    messages.error(request, (
                        "One of the products in your cart wasn't found in our database. "
                        "Please call us for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('view_cart'))

            # If SAVE INFO checked, redirect to save_info page
            request.session['save_info'] = 'save-info' in request.POST

            # Finally, redirect to checkout_success with order number in args
            return redirect(reverse('checkout_success', args=[order.order_number]))

        else:
            messages.error(request, 'There was an error with your form. \
                Please double check your information.')

    else:
        cart = request.session.get('cart', {})
        if not cart:
            # If cart empty display error
            messages.error(request, "There's nothing in your cart!")
            # Redirect back to products, preventing users from entering URL
            # to access the Checkout Page without adding products to cart
            return redirect(reverse('products'))

        # Call cart_contents to new variable, ensuring we don't overwrite the old one
        current_cart = cart_contents(request)
        total = current_cart['grand_total']

        # Stripe requires an INT not FLOAT, so multiply by 100 & round to 0 decimal places
        stripe_total = round(total * 100)
        # Call secret key to authorise payments
        stripe.api_key = stripe_secret_key
        # Create payment intent
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        order_form = OrderForm()

        if not stripe_public_key:
            messages.warning(request, 'Stripe public key is missing. \
                Did you forget to set it in your environment?')

        template = 'checkout/checkout.html'
        context = {
            'order_form': order_form,
            'stripe_public_key': stripe_public_key,
            'client_secret': intent.client_secret,
        }

        return render(request, template, context)
