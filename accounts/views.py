from django.shortcuts import render, get_object_or_404
from checkout.models import NewOrder
from .models import UserAccount
from .forms import UserAccountForm


def personal_account(request):
    """ Display the user's personal account. """
    template = 'accounts/account.html'

    if request.user.is_authenticated:
        my_account = get_object_or_404(UserAccount, user=request.user)
        form = UserAccountForm(instance=my_account)
        orders = my_account.orders.all()

        if request.method == 'POST':
            form = UserAccountForm(request.POST, instance=my_account)
            if form.is_valid():
                form.save()

        context = {
            'form': form,
            'orders': orders,
        }

        return render(request, template, context)
    else:
        return render(request, template)


def order_history(request, order_number):
    """ Create order history """
    order = get_object_or_404(NewOrder, order_number=order_number)

    template = 'accounts/order_history.html'
    context = {
        'order': order,
        'from_account': True,
    }

    return render(request, template, context)


def management(request):
    """ Display management panel. """
    template = 'accounts/management.html'

    return render(request, template)
