from django.shortcuts import render
from .models import Blocks, Pages
from products.models import Categories


def blocks(request):
    blocks = Blocks.objects.all()
    categories = Categories.objects.filter(is_active=True)
    return render(request,"content/content.html", {"blocks": blocks, "categories": categories})

def footer_articles(request, slug):
    pages = Pages.objects.get(slug=slug)
    return render(request, "content/pages.html",{
        "pages": pages})
