from django.urls import path

from . import views

urlpatterns = [
    path("", views.catalog_list, name="categories"),
    path('categories/<slug:slug>/', views.categories_details, name='category_detail'),

]