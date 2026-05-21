from django.contrib import admin
from .models import Order, OrderItem


class OrderInline(admin.TabularInline):
    model = OrderItem
    extra = 20

class OrderItemAdmin(admin.ModelAdmin):
    inlines = [OrderInline]

admin.site.register(Order, OrderItemAdmin)
