from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View, generic
from django.contrib.auth import get_user_model

from shop.models import Product, Order, ProductCategory
from shop.forms import ProductForm


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


class ProductDetailView(LoginRequiredMixin, generic.DetailView):
    model = Product
    queryset = Product.objects.select_related("category")


class ProductCreateView(LoginRequiredMixin, generic.CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("shop:product-list")


class ProductUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("shop:product-list")


class ProductDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Product
    success_url = reverse_lazy("shop:product-list")


class OrderListView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    model = Order
    paginate_by = 10

    def test_func(self):
        return self.request.user.is_employee or self.request.user.is_staff


class UserListView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    model = get_user_model()
    paginate_by = 10

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_employee


class CategoryListView(LoginRequiredMixin, generic.ListView):
    model = ProductCategory
    paginate_by = 10