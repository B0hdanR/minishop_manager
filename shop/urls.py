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
    CategoryListView,
    add_to_cart,
    cart_detail,
    confirm_order, update_cart, remove_from_cart
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
    path("cart/add/<int:pk>", add_to_cart,
         name="add-to-cart"),
    path("cart/", cart_detail,
         name="cart-detail"),
    path("order/confirm", confirm_order,
         name="order-confirm"),
    path("cart/update/<int:pk>/", update_cart,
         name="cart-update"),
    path("cart/remove/<int:pk>/", remove_from_cart,
         name="cart-remove"),
]

app_name = "shop"