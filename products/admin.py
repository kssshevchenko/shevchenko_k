from django.contrib import admin
from .models import Product, Size, Color, Stickers

admin.site.register(Product)
admin.site.register(Size)
admin.site.register(Color)
admin.site.register(Stickers)
