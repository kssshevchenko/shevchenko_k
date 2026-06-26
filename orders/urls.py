from django.urls import path
from . import views

app_name = "checkout"
urlpatterns = [
    path("", views.create_order, name="create_order"),
    path("order_success/<int:order_id>", views.order_success, name="order_success")
]