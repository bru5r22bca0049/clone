from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Case, When, IntegerField

from .models import Product, Wishlist, Category
from .forms import ProductForm
from django.http import JsonResponse


# HOME PAGE

def home(request):

    products = Product.objects.all()
    categories = Category.objects.all()

    query = request.GET.get('q')
    category = request.GET.get('category')

    if category:
        products = products.filter(
            category_id=category
        )

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    return render(
        request,
        'home.html',
        {
            'products': products,
            'categories': categories,
            'query': query
        }
    )


def search_suggestions(request):

    # legacy/placeholder - suggestions handled by unified function at file end
    return JsonResponse([], safe=False)

# PRODUCT LIST
@login_required
def product_list(request):

    products = Product.objects.all()

    return render(request, 'products.html', {
        'products': products
    })


# PRODUCT DETAIL
def product_detail(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    return render(request, 'products/product_detail.html', {
        'product': product
    })


# ADD PRODUCT
@login_required
def add_product(request):

    if request.method == 'POST':

        form = ProductForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            return redirect('products')

        else:
            print(form.errors)

    else:

        form = ProductForm()

    return render(
    request,
    'products/add_product.html',
    {'form': form}
    )


# SELL PRODUCT
@login_required
def sell_product(request):

    if request.method == 'POST':

        form = ProductForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            return redirect('/')

        else:
            print(form.errors)

    else:

        form = ProductForm()

    return render(
        request,
        'products/sell_product.html',
        {
            'form': form
        }
    )


# ADD TO WISHLIST
@login_required
def add_to_wishlist(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    return redirect('wishlist')


# REMOVE FROM WISHLIST
@login_required
def remove_from_wishlist(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    Wishlist.objects.filter(
        user=request.user,
        product=product
    ).delete()

    return redirect('wishlist')


# WISHLIST PAGE
@login_required
def wishlist(request):

    items = Wishlist.objects.filter(
        user=request.user
    )

    return render(
        request,
        'wishlist.html',
        {
            'items': items
        }
    )
    
    
def buy_now(request, id):

    product = get_object_or_404(Product, id=id)

    request.session['buy_now_product'] = {
        'id': product.id,
        'quantity': 1
    }

    return redirect('checkout')    


def search_products(request):

    query = request.GET.get('q')

    products = Product.objects.filter(
        Q(name__icontains=query)
    ) if query else Product.objects.none()

    return render(
        request,
        'products/search.html',
        {
            'products': products,
            'query': query
        }
    )
    
    
    
def search_suggestions(request):
    """Return JSON suggestions for the search box.

    Response items include id, name, price and image (if available).
    """
    q = request.GET.get('q', '')

    products = Product.objects.filter(
        Q(name__icontains=q) | Q(description__icontains=q)
    )[:10] if q else Product.objects.none()

    data = []

    for product in products:
        image_url = ''
        try:
            if product.image and hasattr(product.image, 'url'):
                image_url = product.image.url
        except Exception:
            image_url = ''

        data.append({
            'id': product.id,
            'name': product.name,
            'price': str(product.price),
            'image': image_url
        })

    return JsonResponse(data, safe=False)