from django.urls import path

from .views import (
    ProductCreateView,
    ProductDeleteView,
    ProductUpdateView,
    category_products,
    contacts,
    home,
    product_detail,
    product_unpublish,
)

urlpatterns = [
    path("", home, name="home"),
    path("contacts/", contacts, name="contacts"),
    path(
        "categories/<int:pk>/",
        category_products,
        name="category_products",
    ),
    path("products/create/", ProductCreateView.as_view(), name="product_create"),
    path("products/<int:pk>/", product_detail, name="product_detail"),
    path(
        "products/<int:pk>/edit/",
        ProductUpdateView.as_view(),
        name="product_update",
    ),
    path(
        "products/<int:pk>/delete/",
        ProductDeleteView.as_view(),
        name="product_delete",
    ),
    path(
        "products/<int:pk>/unpublish/",
        product_unpublish,
        name="product_unpublish",
    ),
]
