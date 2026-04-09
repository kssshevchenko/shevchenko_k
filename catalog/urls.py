from django.urls import path
from products.views import product_list, products_by_category

from . import views

urlpatterns = [
    path('', views.catalog_list, name="categories"),
    path('categories/<slug:slug>/', views.categories_details, name='categories_details'),
    path('products/', product_list, name="all_products"),
    path('products_by_category/<slug:slug>/', products_by_category, name="products_by_category"),

]