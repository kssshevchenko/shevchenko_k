from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product, ProductImage, Color
from .forms import ProductChoices
from django.http import JsonResponse
import uuid


def cart_view(request):
    cart = request.session.get("cart", {})

    total_price = 0
    cart_items = []

    for key, item in cart.items():
        try:

            product = Product.objects.get(id=item["product_id"])

            quantity = item["quantity"]
            price = product.final_price
            if item.get("embroidery") == "YES":
                price += product.surcharge

            subtotal = price * quantity
            total_price += subtotal

            cart_items.append({
                "key": key,
                "product": product,
                "quantity": quantity,
                "size": item.get("size"),
                "color": item.get("color"),
                "embroidery": item.get("embroidery"),
                "stickers_count": item.get("stickers_count"),
                "subtotal": subtotal
            })
        except (Product.DoesNotExist, KeyError, TypeError):
            continue

    return render(request, "cart/cart.html", {"cart": cart,
                                              "cart_items": cart_items,
                                              "total_price": total_price})

def cart_data(request):
    cart = request.session.get("cart", {})

    total_price = 0
    cart_items = []

    for key, item in cart.items():
        try:
            product_id = item["product_id"]

            images = ProductImage.objects.filter(id=product_id)
            image = images.first().image.url

            quantity = item.get("quantity", 1)
            product = Product.objects.get(id=product_id)
            price = product.final_price
            if item.get("embroidery") == "YES":
                price += product.surcharge

            subtotal = price * quantity
            total_price += subtotal

            cart_items.append({
                "key": key,
                "name": product.name,
                "image": image,
                "quantity": quantity,
                "size": item.get("size"),
                "color": item.get("color"),
                "print_position": item.get("print_position"),
                "embroidery": item.get("embroidery"),
                "stickers_count": item.get("stickers_count"),
                "subtotal": subtotal,
            })
        except (Product.DoesNotExist, TypeError, KeyError, ValueError):
            continue

    return JsonResponse({
        "cart_items": cart_items,
        "total_price": total_price
    })


def add_products(request, product_id):
    cart = request.session.get("cart", {})

    data = request.POST
    key = str(uuid.uuid4())
    form = ProductChoices(request.POST)

    stickers_count = None
    print_position = ""
    embroidery = None
    selected_stickers = []
    color = ""
    colors = Color.objects.filter(product=product_id)
    if colors and data.get("color") == None:
        return JsonResponse({"error": "Оберіть колір"}, status=400)
    elif colors and data.get("color"):
        color = data.get('color')

    size = data.get('size')

    if form.is_valid():
        stickers_count = int(form.cleaned_data["choices_count_sticker"] or 0)
        print_position = form.cleaned_data["choices_position"]
        embroidery = form.cleaned_data["choices_embroidery"]


    signature = f"{product_id}_{color}_{size}_{print_position}_{embroidery}_{stickers_count}"

    if stickers_count and int(stickers_count) > 0:
        selected_stickers = data.getlist("sticker_id")
        print("selected_stickers", selected_stickers)
        if len(selected_stickers) > stickers_count:
            selected_stickers = data.getlist("sticker_id")[-stickers_count:]
        elif stickers_count != len(selected_stickers):
            return JsonResponse({"error": "Неправильна кількість наліпок"}, status=400)

    found_key = None

    for k, product in cart.items():

        if signature == product.get("signature"):
            found_key = k
    if found_key:
        cart[found_key]["quantity"] += 1
    else:
        cart[key] = {
            "product_id": product_id,
            "quantity": 1,
            "color": color,
            "size": size,
            "print_position": print_position,
            "embroidery": embroidery,
            "stickers_count": stickers_count,
            "selected_stickers": selected_stickers,
            "signature": signature,
        }

    request.session["cart"] = cart
    request.session.modified = True

    return JsonResponse({"cart": cart})


def increase(request, key):
    cart = request.session.get("cart", {})

    cart[key]["quantity"] += 1

    request.session["cart"] = cart
    request.session.modified = True
    return redirect(request.META.get("HTTP_REFERER"))


def decrease(request, key):
    cart = request.session.get("cart", {})

    if key in cart:
        if cart[key]["quantity"] > 1:
            cart[key]["quantity"] -= 1
        else:
            cart.pop(key, None)

    request.session["cart"] = cart
    request.session.modified = True
    return redirect(request.META.get("HTTP_REFERER"))


def delete(request, key):
    cart = request.session.get("cart", {})

    cart.pop(key, None)

    request.session["cart"] = cart
    request.session.modified = True
    return redirect(request.META.get("HTTP_REFERER"))
