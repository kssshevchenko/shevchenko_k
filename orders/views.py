from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from products.models import Product
from .models import Order, OrderItem
from .forms import Client


def create_order(request):
    cart = request.session.get("cart", {})
    form = Client(request.POST)
    total_price = 0
    products = []
    if request.method == "GET":

        for key, item in cart.items():
            product_id = item.get("product_id")
            product_obj = Product.objects.get(id=product_id)
            quantity = item.get("quantity", 1)
            price = product_obj.final_price
            price += product_obj.surcharge
            count_sticker = item.get("stickers_count", 200)
            subtotal = price * quantity
            total_price += subtotal
            checkout_items = {
                "product":product_obj,
                "product_name":product_obj.name,
                "embroidery":item.get("embroidery"),
                "count_sticker":count_sticker,
                "price":subtotal,
                "quantity":quantity,
                "sticker_position":item.get("print_position"),
                "sizes":item.get("size")
            }
            products.append(checkout_items)
        return render(request, "orders/orders.html", {"products": products,
                                                          "form": form,
                                                          "total_price": total_price})

    elif request.method == "POST":
        if form.is_valid():
            order = Order.objects.create(**form.cleaned_data)
        else:
            return JsonResponse({"error": "Перевірте правильність вводу даних"}, status=400)

        for key, item in cart.items():
            product_id = item.get("product_id")
            product_obj = Product.objects.get(id=product_id)
            quantity = item.get("quantity", 1)
            price = product_obj.final_price
            price += product_obj.surcharge
            count_sticker = item.get("stickers_count", 200)
            subtotal = price * quantity
            total_price += subtotal

            OrderItem.objects.create(
                order=order,
                product=product_obj,
                product_name=product_obj.name,
                embroidery=item.get("embroidery"),
                count_sticker=count_sticker,
                price=subtotal,
                quantity=quantity,
                sticker_position=item.get("print_position"),
                sizes=item.get("size")
            )

    request.session["cart"] = {}
    return JsonResponse({
        "success_url": reverse("checkout:order_success", kwargs={"order_id": order.id})
    })

def order_success(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, "orders/order_success.html", {"order": order,
                                                         "total_price": order.total_price})