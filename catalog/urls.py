from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("categories", views.catalog_list, name="categories"),
    path('categories/<slug:slug>/', views.catalog_details, name='category_detail')
]