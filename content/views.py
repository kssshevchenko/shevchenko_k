from django.shortcuts import render
from .models import Blocks
from products.models import Categories
def blocks(request):
    blocks = Blocks.objects.all()
    categories = Categories.objects.all()
    return render(request,"content/content.html", {"blocks": blocks, "categories": categories})
