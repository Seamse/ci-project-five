from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from . import forms
import os

import stripe

if os.path.isfile('env.py'):
    import env

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

# Create your views here.


def checkout(request):
    """ A view to render the page where personal details can be filled out """

    cart = request.session.get('cart', {})
    print(cart)
    if not cart:
        messages.error(request, 'basket is empty')
        return redirect('products')

    form = forms.CheckoutForm()
    template = 'checkout/checkout.html'

    # intent = stripe.PaymentIntent.create(
    #     amount=5000,
    #     currency='eur',
    #     automatic_payment_methods={
    #         'enabled': True,
    #     },
    #     # can use this later in webhook if you want to update billing status or something like that
    #     metadata={'userid': request.user.id}
    # )

    context = {
        'form': form,
        'S_P_K': os.environ.get('STRIPE_PUBLIC_KEY')
        # 'client_secret': intent.client_secret,
        # 'intent': intent,
    }

    return render(request, template, context)
