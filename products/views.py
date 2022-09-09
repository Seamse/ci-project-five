from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Avg
from .models import Product, Review
from .forms import ProductForm, ReviewForm

# Create your views here.


def all_products(request):
    """ A view to render all products on the page and add the ability to search the site """

    products = Product.objects.all()
    query = None
    category = None
    sort = None

    if request.GET:
        if 'sort' in request.GET:
            if 'l2h' in request.GET:
                products = products.order_by("price")
            elif 'h2l' in request.GET:
                products = products.order_by("-price")
            else:
                products = products.order_by("-rating")

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)

        if 'search' in request.GET:
            query = request.GET['search']
            if not query:
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    context = {
        'products': products,
        'search_input': query,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to render a product's details on the page """

    product = get_object_or_404(Product, pk=product_id)
    reviews = Review.objects.filter(product=product_id).order_by("-comment")

    average = reviews.aggregate(Avg("rating"))["rating__avg"]
    if average is None:
        average = 0
    else:
        average = round(average, 2)

    context = {
        'product': product,
        'reviews': reviews,
        'average': average
    }

    return render(request, 'products/product_detail.html', context)


@login_required
def add_product(request):
    """ Add a product to the store """
    if not request.user.is_superuser:
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            return redirect(reverse('home'))
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """
    if not request.user.is_superuser:
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            return redirect(reverse('home'))
    else:
        form = ProductForm(instance=product)

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    return redirect(reverse('products'))

@login_required
def add_review(request, product_id):
    """ Add a review to a product """
    if request.user.is_authenticated:
        product = Product.objects.get(id=product_id)
        if request.method == "POST":
            form = ReviewForm(request.POST or None)
            if form.is_valid():
                new_review = form.save(commit=False)
                new_review.comment = request.POST["comment"]
                new_review.rating = request.POST["rating"]
                new_review.user = request.user
                new_review.product = product
                new_review.save()
                return redirect(request.META.get('HTTP_REFERER'))
        else:
            form = ReviewForm()
            context = {
                'form': form
            }
        return render(request,'products/products.html', context)
    else:
        return redirect('home')


@login_required()
def edit_review(request, product_id, review_id):
    """ Edit a previously created review """
    if request.user.is_authenticated:
        product = Product.objects.get(id=product_id)
        review = Review.objects.get(product=product, id=review_id)
        if request.user == review.user:
            if request.method == "POST":
                form = ReviewForm(request.POST, instance=review)
                if form.is_valid():
                    data = form.save(commit=False)
                    if (data.rating>5) or (data.rating<0):
                        error="Out of range. Please select rating from 0 to 5."
                        context = {
                            'error': error,
                            'form': form
                        }
                        return render(request, 'products/edit_review.html', context)
                    else:
                        data.save()
                        return redirect(f'/products/int:{product_id}')
            else:
                form = ReviewForm(instance=review)
                context = {
                    'form': form
                }
            return render(request,'products/edit_review.html', context)
        else:
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('home')


@login_required
def delete_review(request, product_id, review_id):
    """ Delete a previously created review """
    if request.user.is_authenticated:
        product = Product.objects.get(id=product_id)
        review = Review.objects.get(product=product, id=review_id)
        if request.user == review.user:
            review.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('home')
