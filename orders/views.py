from django.shortcuts import render, redirect
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
            add_price = price
            if item.get("embroidery") == "YES":
                add_price += product_obj.surcharge
            count_sticker = item.get("stickers_count", 200)
            subtotal = add_price * quantity
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
        print(form.is_valid())
        print(form.errors)
        if form.is_valid():
            order = Order.objects.create(**form.cleaned_data)
        for key, item in cart.items():
            product_id = item.get("product_id")
            product_obj = Product.objects.get(id=product_id)
            quantity = item.get("quantity", 1)
            price = product_obj.final_price
            add_price = price
            if item.get("embroidery") == "YES":
                add_price += product_obj.surcharge
            count_sticker = item.get("stickers_count", 200)
            subtotal = add_price * quantity
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
    print("order here", order, type(order))
    # return render(request, "orders/orders.html", {"order": order})
    return redirect("order_success", order_id = order.id)

def order_success(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, "orders/order_success.html", {"order": order,
                                                         "total_price": order.total_price})