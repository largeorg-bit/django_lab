from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView

from catalog.forms import ContactForm, ProductForm
from catalog.models import Product


def home(request):
    """Отображает список товаров на главной странице."""
    products = Product.objects.all()
    return render(request, "catalog/home.html", {"products": products})


@login_required
def product_detail(request, pk):
    """Отображает подробную информацию о товаре."""
    product = get_object_or_404(Product, pk=pk)
    return render(
        request,
        "catalog/product_detail.html",
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Добавление продукта"
        return context


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование продукта."""

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"

    def get_success_url(self):
        return reverse_lazy("product_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Редактирование продукта"
        return context


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление продукта."""

    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("home")
