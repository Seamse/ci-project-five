from django.shortcuts import render, get_object_or_404
from .models import UserAccount


def personal_account(request):
    """ Display the user's personal account. """
    personal_account = get_object_or_404(UserAccount, user=request.user)

    template = 'accounts/account.html'
    context = {
        'personal_account': personal_account,
    }

    return render(request, template, context)
