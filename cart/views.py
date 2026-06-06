from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from products.models import Product
from .models import Cart, CartItem


# ADD TO CART
@login_required
def add_to_cart(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        cart_item.quantity += 1
    else:
        cart_item.quantity = 1

    cart_item.save()

    return redirect('cart')


# BUY NOW
@login_required
def buy_now(request, id):

    product = get_object_or_404(Product, id=id)

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    cart_item.quantity = 1
    cart_item.save()

    return redirect('checkout')


# CART PAGE
@login_required
def cart_view(request):

    cart_items = CartItem.objects.filter(
        cart__user=request.user
    )

    subtotal = 0

    for item in cart_items:
        subtotal += item.product.price * item.quantity

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'subtotal': subtotal
    })


# REMOVE FROM CART
@login_required
def remove_from_cart(request, product_id):

    cart_item = get_object_or_404(
        CartItem,
        cart__user=request.user,
        product__id=product_id
    )

    cart_item.delete()

    return redirect('cart')


# UPDATE CART
@login_required
def update_cart(request, item_id):

    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    if request.method == "POST":

        quantity = request.POST.get("quantity")

        if quantity and int(quantity) > 0:

            item.quantity = int(quantity)
            item.save()

        else:
            item.delete()

    return redirect('cart')


# CHECKOUT
@login_required
def checkout(request):

    cart_items = CartItem.objects.filter(
        cart__user=request.user
    )

    subtotal = 0

    for item in cart_items:
        subtotal += item.product.price * item.quantity

    total_price = subtotal

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'total_price': total_price
    })