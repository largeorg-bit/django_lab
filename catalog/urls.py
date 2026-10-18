from django.urls import path

from .views import (
    ProductCreateView,
    ProductDeleteView,
    ProductUpdateView,
    contacts,
    home,
    product_detail,
)

urlpatterns = [
    path("", home, name="home"),
    path("contacts/", contacts, name="contacts"),
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
]
