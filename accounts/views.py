from django.shortcuts import render, get_object_or_404
from checkout.models import NewOrder
from .models import UserAccount
from .forms import UserAccountForm


def personal_account(request):
    """ Display the user's personal account. """
    my_account = get_object_or_404(UserAccount, user=request.user)
    form = UserAccountForm(instance=my_account)
    previous_orders = my_account.orders.all()

    if request.method == 'POST':
        form = UserAccountForm(request.POST, instance=my_account)
        if form.is_valid():
            form.save()

    template = 'accounts/account.html'
    context = {
        'form': form,
        'previous_orders': previous_orders,
    }

    return render(request, template, context)


def order_history(request, order_number):
    """ Create order history """
    order = get_object_or_404(NewOrder, order_number=order_number)

    template = 'checkout/make_purchase.html'
    context = {
        'order': order,
        'from_account': True,
    }

    return render(request, template, context)
