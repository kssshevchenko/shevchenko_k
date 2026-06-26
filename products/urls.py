from django.urls import path
from . import views


urlpatterns = [
    path("", views.products, name="products"),
    path('categories/', views.catalog_list, name="categories"),
    path('category_products/<slug:slug>/', views.category_products, name="category_products"),
    path('<slug:slug>/', views.product_list, name="product_list"),

    # path('<slug:slug>/', views.categories_details, name='categories_details'),


]