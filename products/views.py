from django.shortcuts import render, get_object_or_404
from .models import Product, Categories, ProductType
from cart.forms import ProductChoices

def products(request):
    products = Product.objects.all()
    stickers = Product.objects.filter(is_sticker=True)

    product_types = ProductType.objects.all()
    selected_type = request.GET.get("product_type")

    if selected_type:
        products = products.filter(product_type=selected_type)

    return render(request, "products/products.html",
                  {"products": products,
                   "stickers": stickers,
                   "product_types": product_types,

                   })

def product_list(request, slug):
    product = get_object_or_404(Product, slug=slug)
    form = ProductChoices()
    stickers = Product.objects.filter(is_sticker=True)
    return render(request, "products/product_detail.html", {"product": product,
                                                            "form": form,
                                                            "stickers": stickers
                                                           })

"""categories"""
def home(request):
    return render(request, "catalog/home.html")

def catalog_list(request):
    categories = Categories.objects.all()
    return render(request, "catalog/categories.html", {'categories': categories})

def categories_details(request, slug):
    category = get_object_or_404(Categories, slug=slug)

    products = Product.objects.filter(category=category)


    return render(request, "catalog/products.html", {"category": category,
                                                         "products": products})


def category_products(request, slug):
    categories = get_object_or_404(Categories, slug=slug)
    products = Product.objects.filter(category=categories)
    return render(request, "products/products.html", {"products": products})