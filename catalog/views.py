from django.shortcuts import get_object_or_404, render

from catalog.forms import ContactForm
from catalog.models import Product


def home(request):
    """Отображает список товаров на главной странице."""
    products = Product.objects.all()
    return render(request, "catalog/home.html", {"products": products})


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
