from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView

from catalog.forms import ContactForm, ProductForm
from catalog.models import Product
from catalog.services import (
    user_can_delete_product,
    user_can_edit_product,
    user_can_unpublish_product,
)


def home(request):
    """Отображает список опубликованных товаров."""
    products = Product.objects.filter(is_published=True)
    if request.user.is_authenticated:
        products = Product.objects.filter(
            Q(is_published=True) | Q(owner=request.user)
        ).distinct()
    return render(request, "catalog/home.html", {"products": products})


@login_required
def product_detail(request, pk):
    """Отображает подробную информацию о товаре."""
    product = get_object_or_404(Product, pk=pk)
    context = {
        "product": product,
        "can_edit": user_can_edit_product(request.user, product),
        "can_delete": user_can_delete_product(request.user, product),
        "can_unpublish": (
            user_can_unpublish_product(request.user) and product.is_published
        ),
    }
    return render(request, "catalog/product_detail.html", context)


@login_required
@permission_required("catalog.can_unpublish_product", raise_exception=True)
def product_unpublish(request, pk):
    """Отменяет публикацию продукта."""
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.is_published = False
        product.save(update_fields=["is_published", "updated_at"])
        messages.success(
            request,
            f'Публикация продукта «{product.name}» отменена.',
        )
        return redirect("product_detail", pk=product.pk)
    return render(
        request,
        "catalog/product_confirm_unpublish.html",
        {"product": product},
    )


def contacts(request):
    """Принимает форму обратной связи и сохраняет её в БД."""
    success = False
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            success = True
            form = ContactForm()
    else:
        form = ContactForm()

    return render(
        request,
        "catalog/contacts.html",
        {"form": form, "success": success},
    )


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Создание нового продукта."""

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.is_published = False
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Добавление продукта"
        return context


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Редактирование продукта владельцем или модератором."""

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"

    def test_func(self):
        return user_can_edit_product(self.request.user, self.get_object())

    def get_success_url(self):
        return reverse_lazy("product_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Редактирование продукта"
        return context


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Удаление продукта владельцем или модератором."""

    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("home")

    def test_func(self):
        return user_can_delete_product(self.request.user, self.get_object())
