from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product


def basket_contents(request):

    basket_items = []
    total = 0
    product_count = 0
    cart = request.session.get('cart', {})

    for item_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=item_id)
        total += quantity * product.price
        product_count += quantity
        basket_items.append({
            'item_id': item_id,
            'quantity': quantity,
            'product': product,
        })

    if total > settings.FREE_DELIVERY_FROM:
        standard_delivery = 0
    else:
        standard_delivery = settings.STANDARD_DELIVERY

    total_cost = standard_delivery + total

    context = {
        'basket_items': basket_items,
        'total': total,
        'product_count': product_count,
        'standard_delivery': standard_delivery,
        'total_cost': total_cost,
    }

    return context
