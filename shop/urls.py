from django.urls import path

from .views import (index, ProductListView, ProductDetailView, OrderListView, UserListView, CategoryListView)

urlpatterns = [
    path('', index, name='index'),
    path('products/', ProductListView.as_view(),
         name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(),
         name='product-detail'),
    path('orders/', OrderListView.as_view(),
         name='order-list'),
    path('users/', UserListView.as_view(),
         name='user-list'),
    path('categories/', CategoryListView.as_view(),
         name='category-list'),
]

app_name = "shop"