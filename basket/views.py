from django.shortcuts import render, redirect

# Create your views here.


def basket(request):
    """ A view to list the items in the shopping basket """

    return render(request, 'basket/basket.html')


def add_to_basket(request, item_id):
    """ A view to allow users to add products to their shopping basket """

    quantity = int(request.POST.get('quantity'))
    cart = request.session.get('cart', {})

    if item_id in list(cart.keys()):
        cart[item_id] += quantity
    else:
        cart[item_id] = quantity

    request.session['cart'] = cart
    return redirect(request.META.get('HTTP_REFERER'))


def delete_item(request, item_id):
    cart = request.session.get('cart', {})
    cart.pop(item_id)
    request.session['cart'] = cart
    return render(request, 'basket/basket.html')
