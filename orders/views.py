from decimal import Decimal

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Order, OrderItem
from products.models import Product
from cart.models import CartItem


# =========================================
# CHECKOUT PAGE
# =========================================

def checkout(request):

    buy_now = request.session.get(
        'buy_now_product'
    )

    total_price = Decimal('0.00')

    # ================= BUY NOW =================

    if buy_now:

        product = get_object_or_404(
            Product,
            id=buy_now['id']
        )

        quantity = buy_now['quantity']

        cart_items = [{
            'product': product,
            'quantity': quantity,
            'subtotal': product.price * quantity
        }]

        total_price = (
            product.price * quantity
        )

    # ================= CART =================

    else:

        cart_items = CartItem.objects.filter(
            cart__user=request.user
        )

        if not cart_items.exists():

            messages.error(
                request,
                "Your cart is empty"
            )

            return redirect('home')

        for item in cart_items:

            item.subtotal = (
                item.product.price *
                item.quantity
            )

            total_price += item.subtotal

    context = {

        'cart_items': cart_items,
        'total_price': total_price

    }

    return render(
        request,
        'orders/checkout.html',
        context
    )
    # ================= BUY NOW =================

    if buy_now:

        product = get_object_or_404(
            Product,
            id=buy_now['id']
        )

        quantity = buy_now['quantity']

        cart_items = [{
            'product': product,
            'quantity': quantity,
            'subtotal': product.price * quantity
        }]

        total_price = (
            product.price * quantity
        )

    # ================= CART =================

    else:

        cart_items = CartItem.objects.filter(
            cart__user=request.user
        )

        if not cart_items.exists():

            messages.error(
                request,
                "Your cart is empty"
            )

            return redirect('home')

        for item in cart_items:

            item.subtotal = (
                item.product.price *
                item.quantity
            )

            total_price += item.subtotal

    context = {

        'cart_items': cart_items,
        'total_price': total_price

    }

    return render(
        request,
        'orders/checkout.html',
        context
    )


# =========================================
# SHIPPING PAGE
# =========================================

@login_required
def shipping(request):

    buy_now = request.session.get(
        'buy_now_product'
    )

    total_price = Decimal('0.00')

    # ================= BUY NOW =================

    if buy_now:

        product = get_object_or_404(
            Product,
            id=buy_now['id']
        )

        quantity = buy_now['quantity']

        cart_items = [{
            'product': product,
            'quantity': quantity,
            'subtotal': product.price * quantity
        }]

        total_price = (
            product.price * quantity
        )

    # ================= CART =================

    else:

        cart_items = CartItem.objects.filter(
            cart__user=request.user
        )

        if not cart_items.exists():

            messages.error(
                request,
                "Your cart is empty"
            )

            return redirect('home')

        for item in cart_items:

            item.subtotal = (
                item.product.price *
                item.quantity
            )

            total_price += item.subtotal

    context = {

        'cart_items': cart_items,
        'total_price': total_price

    }

    return render(
        request,
        'orders/shipping.html',
        context
    )


# =========================================
# PLACE ORDER
# =========================================

@login_required
def place_order(request):

    # ONLY POST

    if request.method != "POST":

        return redirect('shipping')

    # ================= SHIPPING DATA =================

    full_name = request.POST.get(
        'full_name'
    )

    phone = request.POST.get(
        'phone'
    )

    address = request.POST.get(
        'address'
    )

    city = request.POST.get(
        'city'
    )

    pincode = request.POST.get(
        'pincode'
    )

    # ================= VALIDATION =================

    if not full_name:

        messages.error(
            request,
            "Full name required"
        )

        return redirect('shipping')

    if not phone:

        messages.error(
            request,
            "Phone number required"
        )

        return redirect('shipping')

    if not address:

        messages.error(
            request,
            "Address required"
        )

        return redirect('shipping')

    if not city:

        messages.error(
            request,
            "City required"
        )

        return redirect('shipping')

    # ================= BUY NOW =================

    buy_now = request.session.get(
        'buy_now_product'
    )

    total_price = Decimal('0.00')

    # ================= BUY NOW FLOW =================

    if buy_now:

        product = get_object_or_404(
            Product,
            id=buy_now['id']
        )

        quantity = buy_now['quantity']

        total_price = (
            product.price * quantity
        )

    # ================= CART FLOW =================

    else:

        cart_items = CartItem.objects.filter(
            cart__user=request.user
        )

        if not cart_items.exists():

            messages.error(
                request,
                "Cart is empty"
            )

            return redirect('cart')

        for item in cart_items:

            total_price += (
                item.product.price *
                item.quantity
            )

    # =========================================
    # CREATE ORDER
    # =========================================

    order = Order.objects.create(

        user=request.user,

        full_name=full_name,

        phone=phone,

        address=address,

        city=city,

        pincode=pincode,

        total_price=total_price,

        status='On the way'

    )

    # =========================================
    # BUY NOW ORDER ITEM
    # =========================================

    if buy_now:

        OrderItem.objects.create(

            order=order,

            product=product,

            quantity=quantity,

            price=product.price

        )

        del request.session[
            'buy_now_product'
        ]

    # =========================================
    # CART ORDER ITEMS
    # =========================================

    else:

        for item in cart_items:

            OrderItem.objects.create(

                order=order,

                product=item.product,

                quantity=item.quantity,

                price=item.product.price

            )

        # CLEAR CART

        cart_items.delete()

    # =========================================
    # SUCCESS MESSAGE
    # =========================================

    messages.success(

        request,

        "Order placed successfully!"

    )

    return redirect('orders')


# =========================================
# MY ORDERS
# =========================================

@login_required
def orders(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by('-id')

    context = {

        'orders': orders

    }

    return render(

        request,

        'orders/orders.html',

        context

    )


# =========================================
# BUY NOW
# =========================================

@login_required
def buy_now(request, id):

    product = get_object_or_404(

        Product,

        id=id

    )

    request.session[
        'buy_now_product'
    ] = {

        'id': product.id,

        'quantity': 1

    }

    request.session.modified = True

    return redirect('checkout')