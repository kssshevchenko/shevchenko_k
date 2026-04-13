from django.urls import path

from . import views

urlpatterns = [
    path('', views.catalog_list, name="categories"),
    path('<slug:slug>/', views.categories_details, name='categories_details'),
    path('category_products/<slug:slug>/', views.category_products, name="category_products"),

]