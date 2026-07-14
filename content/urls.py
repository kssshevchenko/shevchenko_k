from django.urls import path
from . import views

urlpatterns =[
    path("", views.blocks, name="block"),
    path("pages/<slug:slug>/", views.footer_articles, name="footer_articles")
]