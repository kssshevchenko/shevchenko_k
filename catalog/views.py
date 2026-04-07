from django.shortcuts import render, get_object_or_404

from .models import Categories
# from products.models import Product

def catalog_list(request):
    categories = Categories.objects.filter(parent=None).order_by("order")
    return render(request, "categories.html", {'categories': categories})

def categories_details(request, slug):
    categories = get_object_or_404(Categories, slug=slug)
    children_list = categories.children.all().order_by("order")
    return render(request, "categories_list.html", {"categories": categories,
                                                    "subcategories": children_list})
