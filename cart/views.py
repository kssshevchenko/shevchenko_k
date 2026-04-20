from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from django.http import JsonResponse

def cart_view(request):
    cart = request.session.get("cart", {})
    total_price = 0
    cart_items = []
    for key, item in cart.items():
        product = Product.objects.get(id=key)
        price = product.price
        subprice = price * item
        total_price += subprice
        cart_items.append({
            "product": product,
            "quantity": item,
            "subprice": subprice
        })
    return render(request, "cart/cart.html", {"cart": cart,
                                              "cart_items": cart_items,
                                              "total_price": total_price})


def cart_data(request):
    cart = request.session.get("cart", {})

    total_price = 0
    cart_items = []

    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)

        subtotal = product.price * quantity
        total_price += subtotal

        cart_items.append({
            "id": product_id,
            "name": product.name,
            "quantity": quantity,
            "subtotal": subtotal,
        })

    return JsonResponse({
        "cart_items": cart_items,
        "total_price": total_price
    })

def add_products(request, product_id):
    cart = request.session.get("cart", {})
    if str(product_id) in cart:
        cart[str(product_id)] += 1
    else:
        cart[str(product_id)] = 1

    request.session["cart"] = cart
    return redirect(request.META.get("HTTP_REFERER"))


def increase(request, product_id):
    cart = request.session.get("cart", {})
    cart[str(product_id)] += 1
    request.session["cart"] = cart
    return redirect(request.META.get("HTTP_REFERER"))


def decrease(request, product_id):
    cart = request.session.get("cart", {})
    if str(product_id) in cart:
        if cart[str(product_id)] > 1:
            cart[str(product_id)] -= 1
        else:
            del cart[str(product_id)]
    else:
        return redirect("cart_view")
    request.session["cart"] = cart
    return redirect(request.META.get("HTTP_REFERER"))


def delete(request, product_id):
    cart = request.session.get("cart", {})
    cart.pop(str(product_id), None)
    request.session["cart"] = cart
    return redirect(request.META.get("HTTP_REFERER"))
