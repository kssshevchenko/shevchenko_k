from django.shortcuts import render, get_object_or_404
from .models import Product, Stickers
from cart.forms import ProductChoices

def products(request):
    products = Product.objects.all()
    # form = ProductChoices() , "form": form
    return render(request, "products/products.html", {"products": products})

def product_list(request, slug):
    product = get_object_or_404(Product, slug=slug)
    form = ProductChoices()
    stickers = Stickers.objects.all()
    return render(request, "products/product_detail.html", {"product": product,
                                                            "form": form,
                                                            "stickers": stickers})
