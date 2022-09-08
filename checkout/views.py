import json
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.conf import settings
import stripe
from products.models import Product
from basket.contexts import basket_contents
from accounts.models import UserAccount
from accounts.forms import UserAccountForm
from . import forms
from .models import NewOrder, OrderLineItem


# Create your views here.


def checkout(request):
    """ A view to render the page where personal details can be filled out """

    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        cart = request.session.get('cart', {})

        form_data = {
            'first_name': request.POST['first_name'],
            'last_name': request.POST['last_name'],
            'email': request.POST['email'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'country': request.POST['country'],
        }

        form = forms.CheckoutForm(form_data)
        if form.is_valid():
            order = form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_cart = json.dumps(cart)
            order.save()
            for item_id, item_data in cart.items():
                try:
                    product = Product.objects.get(id=item_id)
                    order_line_item = OrderLineItem(
                        order=order,
                        product=product,
                        quantity=item_data,
                        )
                    order_line_item.save()
                except Product.DoesNotExist:
                    order.delete()
                    return redirect(reverse('basket'))

            # Save the info to the user's profile if all is well
            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('make_purchase', args=[order.order_number]))
    else:
        cart = request.session.get('cart', {})
        if not cart:
            return redirect(reverse('products'))

    current_basket = basket_contents(request)
    total = current_basket['total_cost']
    stripe_total = round(total * 100)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    # Attempt to prefill the form with any info the user maintains in their profile
    if request.user.is_authenticated:
        try:
            account = UserAccount.objects.get(user=request.user)
            form = forms.CheckoutForm(initial={
                # 'first_name': account.user.get_first_name(),
                # 'last_name': account.user.get_last_name(),
                'email': account.user.email,
                'street_address1': account.default_street_address1,
                'street_address2': account.default_street_address2,
                'postcode': account.default_postcode,
                'town_or_city': account.default_town_or_city,
                'country': account.default_country,
            })
        except UserAccount.DoesNotExist:
            form = forms.CheckoutForm()
    else:
        form = forms.CheckoutForm()

    template = 'checkout/checkout.html'

    context = {
        'form': form,
        'S_P_K': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)


def make_purchase(request, order_number):
    """
    Handle successful checkouts
    """
    save_info = request.session.get('save_info')
    order = get_object_or_404(NewOrder, order_number=order_number)

    if request.user.is_authenticated:
        account = UserAccount.objects.get(user=request.user)
        # Attach the user's profile to the order
        order.user_account = account
        order.save()

        # Save the user's info
        if save_info:
            account_data = {
                'default_street_address1': order.street_address1,
                'default_street_address2': order.street_address2,
                'default_postcode': order.postcode,
                'default_town_or_city': order.town_or_city,
                'default_country': order.country,
            }
            user_account_form = UserAccountForm(account_data, instance=account)
            if user_account_form.is_valid():
                user_account_form.save()

    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')

    if 'cart' in request.session:
        del request.session['cart']

    template = 'checkout/make_purchase.html'
    context = {
        'order': order,
    }

    return render(request, template, context)
