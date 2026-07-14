from django.shortcuts import render, get_object_or_404
from .models import Product, Categories, ProductType
from cart.forms import ProductChoices

def products(request):
    products = Product.objects.filter(is_active=True)
    stickers = Product.objects.filter(is_active=True, is_sticker=True)

    product_types = ProductType.objects.all()
    selected_type = request.GET.get("product_type")
    product_categories = Categories.objects.filter(is_active=True)

    if selected_type:
        products = products.filter(product_type=selected_type)


    return render(request, "products/products.html",
                  {"products": products,
                   "stickers": stickers,
                   "product_types": product_types,
                   "product_categories": product_categories,
                   })

def product_list(request, slug):
    product = get_object_or_404(Product, slug=slug)
    form = ProductChoices()
    stickers = Product.objects.filter(is_active=True, is_sticker=True)
    return render(request, "products/product_detail.html", {"product": product,
                                                            "form": form,
                                                            "stickers": stickers
                                                           })

"""categories"""
def home(request):
    return render(request, "catalog/home.html")

def category_products(request, slug):
    categories = get_object_or_404(Categories, slug=slug)
    products = Product.objects.filter(is_active=True, category=categories)
    category = Categories.objects.get(slug=slug)
    selected_type = request.GET.get("product_type")

    if selected_type:
        products = products.filter(product_type=selected_type)

    return render(request, "products/products.html", {"products": products, "category": category})

