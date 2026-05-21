from django.urls import path
from . import views

urlpatterns = [
    path("", views.create_order, name="create_order"),
    # path("client_info", views.client_info, name="client_info")
    path("order_success/<int:order_id>", views.order_success, name="order_success")
]