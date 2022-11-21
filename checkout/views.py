import json
from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.contrib import messages
from django.conf import settings
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import stripe
from products.models import Product
from basket.contexts import basket_contents
from accounts.models import UserAccount
from accounts.forms import UserAccountForm
from . import forms
from .models import NewOrder, OrderLineItem


# Create your views here.

@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'cart': json.dumps(request.session.get('cart', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


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
        'stripe_public_key': stripe_public_key,
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

    if 'cart' in request.session:
        del request.session['cart']

    template = 'checkout/make_purchase.html'
    context = {
        'order': order,
    }

    return render(request, template, context)


def payment_confirmation(data):
    """ post webhook payment confirmation view """
    # find order and update payment to True
    NewOrder.objects.filter(order_key=data).update(billing_status=True)
    # find order items and send confirmation email containing links
    order = NewOrder.objects.get(order_key=data)
    order_items = OrderLineItem.objects.filter(order=order)
    order_items_url = [item.product.pdf.url for item in order_items]
    subject = 'Your The Winery Order'
    from_email = settings.EMAIL_HOST_USER
    to = order.email
    text_message = f'''
        Hi there, {order.first_name}. Your payment was successful.
        Here are the details of your order,{"".join(order_items_url)}'''
    html_message = get_template(("email.html")).render({
        'order': order,
        'order_items': order_items
    })
    message = EmailMultiAlternatives(subject, text_message, from_email, [to])
    message.attach_alternative(html_message, "text/html")
    message.send()


@csrf_exempt
def stripe_webhook(request):
    """listens for payment_intent.succeeded"""
    payload = request.body
    stripe.api_key = settings.STRIPE_SECRET_KEY
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        print(e)
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'payment_intent.succeeded':
        payment_confirmation(event.data.object.client_secret)

    else:
        print(f'Unhandled event type {event.type}')

    return HttpResponse(status=200)
