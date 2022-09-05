from django.shortcuts import render

# Create your views here.


def basket(request):
    """ A view to render the shopping basket """

    return render(request, 'basket/basket.html')
