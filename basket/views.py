from django.shortcuts import render, redirect

# Create your views here.


def basket(request):
    """ A view to render the shopping basket """

    return render(request, 'basket/basket.html')


def add_to_basket(request, item_id):
    """ A view to allow users to add products to their shopping basket """

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('cart', {})

    if item_id in list(cart.keys()):
        cart[item_id] += quantity
    else:
        cart[item_id] = quantity

    request.session['cart'] = cart
    return redirect(redirect_url)
