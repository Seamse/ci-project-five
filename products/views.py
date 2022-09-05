from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product

# Create your views here.


def all_products(request):
    """ A view to render all products on the page and add the ability to search the site """

    products = Product.objects.all()
    query = None
    category = None

    if request.GET:

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)


        if 'search' in request.GET:
            query = request.GET['search']
            if not query:
                messages.error(request, "I'm not sure what you're looking for")
                return redirect(reverse('products'))
            
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products=products.filter(queries)

    context = {
        'products': products,
        'search_input': query,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to render a product's details on the page """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)