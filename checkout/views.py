import os
from django.shortcuts import render, redirect
from django.conf import settings
import stripe
from . import forms
from basket.contexts import basket_contents




# if os.path.isfile('env.py'):
#     import env

# stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

# Create your views here.


def checkout(request):
    """ A view to render the page where personal details can be filled out """

    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    cart = request.session.get('cart', {})
    print(cart)
    if not cart:
        return redirect('products')
    
    current_basket = basket_contents(request)
    total = current_basket['total_cost']
    stripe_total = round(total * 100)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

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
        'S_P_K': stripe_public_key
        # 'client_secret': intent.client_secret,
        # 'intent': intent,
    }

    return render(request, template, context)
