from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse
from .models import Categories

def index(request):
    return HttpResponse("There are catalog")

def catalog_list(request):
    categories = Categories.objects.all()
    return render(request, "categories.html", {'categories': categories})

def catalog_details(request, slug):
    category = get_object_or_404(Categories, slug=slug)
    return render(request, "category_detail.html", {"category": category})