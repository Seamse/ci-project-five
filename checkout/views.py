from django.shortcuts import render, redirect
from . import forms


# Create your views here.
def checkout(request):
    """ A view to render the page where personal details can be filled out """

    if request.method == "POST":
        print('posting')
        form = forms.CheckoutForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            print('it is not working')
        return redirect('home')
    form = forms.CheckoutForm()
    context = {
        'form': form
    }
    return render(request, "checkout/checkout.html", context)


def make_purchase(request):
    """ A view to finalize the purchase """

