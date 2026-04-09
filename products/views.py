from django.shortcuts import render, get_object_or_404
from .models import Product
from catalog.models import Categories

def product_list(request):
    products = Product.objects.all()
    return render(request, "products/products.html", {"products": products})

def get_subcategories(category):
    all_categories = [category]
    for child in category.children.all():
        all_categories.extend(get_subcategories(child))
    return all_categories


def products_by_category(request, slug):
    categories = get_object_or_404(Categories, slug=slug)
    subcategories = get_subcategories(categories)
    products = Product.objects.filter(category__in=subcategories)
    return render(request, "products/products.html", {"products": products})