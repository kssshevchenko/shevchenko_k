from django.urls import path
from . import views

urlpatterns = [
    path("add/<int:product_id>/", views.add_products, name="add_products"),
    path("", views.cart_view, name="cart_view"),
    path("cart_data/", views.cart_data, name="cart_data"),
    path("increase/<int:product_id>/", views.increase, name="increase"),
    path("decrease/<int:product_id>/", views.decrease, name="decrease"),
    path("delete/<int:product_id>/", views.delete, name="delete"),
]