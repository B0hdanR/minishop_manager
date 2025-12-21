from django.shortcuts import render
from django.views import View, generic
from django.contrib.auth import get_user_model

from shop.models import Product, Order, ProductCategory


def index(request):
    context = {
        "num_categories": ProductCategory.objects.count(),
        "num_products": Product.objects.count(),
        "num_users": get_user_model().objects.count(),
        "num_orders": Order.objects.count(),
    }
    return render(request, 'shop/index.html', context=context)


class ProductListView(generic.ListView):
    model = Product
    queryset = Product.objects.select_related("category")
    paginate_by = 10


class ProductDetailView(generic.DetailView):
    model = Product


class OrderListView(generic.ListView):
    model = Order
    paginate_by = 10


class UserListView(generic.ListView):
    model = get_user_model()
    paginate_by = 10

class CategoryListView(generic.ListView):
    model = ProductCategory
    paginate_by = 10