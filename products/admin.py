from django.contrib import admin
from .models import Product, Size, Color, ProductImage, Categories, ProductType


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "categories")
    list_filter = ("categories",)
    ordering = ("categories__name", "name")

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3

class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price")
    inlines = [ProductImageInline]


admin.site.register(Size)
admin.site.register(Color)
admin.site.register(Product, ProductAdmin)
admin.site.register(Categories)


