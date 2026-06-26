from django.urls import path
from . import views

urlpatterns =[
    path("", views.blocks, name="block"),
]