from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View, generic
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST
from django.contrib import messages

from shop.models import Product, Order, ProductCategory, OrderItem
from shop.forms import ProductForm


def index(request):
    context = {
        "num_categories": ProductCategory.objects.count(),
        "num_products": Product.objects.count(),
        "num_users": get_user_model().objects.count(),
        "num_orders": Order.objects.count(),
        "num_myorders": Order.objects.filter(user=request.user).count() if request.user.is_authenticated else 0,
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


@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    quantity = int(request.POST.get("quantity", 1))

    if quantity > product.stock_quantity:
        quantity = product.stock_quantity
        messages.warning(
            request,
            f"{product.stock_quantity} items in stock"
        )

    if quantity <= 0:
        messages.error(request, "There must be at least 1.")
        return redirect(request.META.get("HTTP_REFERER", "shop:product-list"))

    order, _ = Order.objects.get_or_create(
        user=request.user,
        status="new"
    )

    order_item, created = OrderItem.objects.get_or_create(
        order=order,
        product=product,
    )

    if created:
        order_item.quantity = quantity
    else:
        new_quantity = order_item.quantity + quantity
        if new_quantity > product.stock_quantity:
            order_item.quantity = product.stock_quantity
            messages.warning(
                request,
                f"{product.stock_quantity} items in stock"
            )
        else:
            order_item.quantity = new_quantity
    order_item.save()

    return redirect(request.META.get("HTTP_REFERER", "shop:product-list"))


@login_required
def cart_detail(request):
    order = Order.objects.filter(
        user=request.user,
        status="new"
    ).prefetch_related("items__product").first()

    return render(request, 'shop/cart_detail.html', {'order': order})


@login_required
@require_POST
def update_cart(request, pk):
    item = get_object_or_404(
        OrderItem,
        pk=pk,
        order__user=request.user,
        order__status="new"
    )

    quantity = int(request.POST.get("quantity", 1))

    if quantity <= 0:
        item.delete()
        messages.info(request, f"{item.product.name} removed from cart.")
        return redirect("shop:cart-detail")

    if quantity > item.product.stock_quantity:
        quantity = item.product.stock_quantity
        messages.warning(
            request,
            f"{item.product.stock_quantity} items in stock"
        )

    item.quantity = quantity
    item.save()

    return redirect("shop:cart-detail")


@login_required
def confirm_order(request):
    order = get_object_or_404(
        Order,
        user=request.user,
        status="new")

    if order.items.count() == 0:
        return redirect("shop:cart-detail")

    order.status = "processing"
    order.save()
    return redirect("accounts:myorder-list")


@login_required
@require_POST
def remove_from_cart(request, pk):
    item = get_object_or_404(
        OrderItem,
        pk=pk,
        order__user=request.user,
        order__status="new"
    )

    item.delete()
    return redirect("shop:cart-detail")
