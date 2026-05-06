from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path("add/<int:product_id>/", views.add_products, name="add_products"),
    path("", views.cart_view, name="cart_view"),
    path("cart_data/", views.cart_data, name="cart_data"),
    path("increase/<str:key>/", views.increase, name="increase"),
    path("decrease/<str:key>/", views.decrease, name="decrease"),
    path("delete/<str:key>/", views.delete, name="delete"),
]