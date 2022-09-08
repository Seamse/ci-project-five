from django.shortcuts import render, get_object_or_404
from .models import UserAccount
from .forms import UserAccountForm


def personal_account(request):
    """ Display the user's personal account. """
    my_account = get_object_or_404(UserAccount, user=request.user)
    form = UserAccountForm(instance=my_account)
    order_history = my_account.orders.all()

    if request.method == 'POST':
        form = UserAccountForm(request.POST, instance=my_account)
        if form.is_valid():
            form.save()

    template = 'accounts/account.html'
    context = {
        'form': form,
        'order_history': order_history,
    }

    return render(request, template, context)
