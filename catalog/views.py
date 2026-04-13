from django.shortcuts import render, get_object_or_404

from .models import Categories
from products.models import Product

def home(request):
    return render(request, "catalog/home.html")

def catalog_list(request):
    categories = Categories.objects.filter(parent=None).order_by("order")
    return render(request, "catalog/categories.html", {'categories': categories})

def categories_details(request, slug):
    category = get_object_or_404(Categories, slug=slug)
    children_list = category.children.all().order_by("order")
    products = Product.objects.filter(category=category)
    if children_list:
        return render(request, "catalog/categories_list.html", {"category": category,
                                                    "subcategories": children_list})
    else:

        return render(request, "catalog/products.html", {"category": category,
                                                         "products": products})

def get_subcategories(category):
    all_categories = [category]
    for child in category.children.all():
        all_categories.extend(get_subcategories(child))
    return all_categories


def category_products(request, slug):
    categories = get_object_or_404(Categories, slug=slug)
    subcategories = get_subcategories(categories)
    products = Product.objects.filter(category__in=subcategories)
    return render(request, "products/products.html", {"products": products})
