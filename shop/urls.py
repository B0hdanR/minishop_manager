from django.urls import path

from .views import (
    index,
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    OrderListView,
    UserListView,
    CategoryListView
)

urlpatterns = [
    path('', index, name='index'),
    path('products/', ProductListView.as_view(),
         name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(),
         name='product-detail'),
    path('products/create/', ProductCreateView.as_view(),
         name='product-create'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(),
         name='product-update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(),
         name='product-delete'),
    path('orders/', OrderListView.as_view(),
         name='order-list'),
    path('users/', UserListView.as_view(),
         name='user-list'),
    path('categories/', CategoryListView.as_view(),
         name='category-list'),
]

app_name = "shop"