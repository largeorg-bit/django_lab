from django.contrib import admin

from catalog.models import Category, ContactMessage, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "price",
        "category",
        "is_available",
        "is_published",
        "owner",
    )
    list_filter = ("category", "is_available", "is_published")
    search_fields = ("name", "description")
    list_editable = ("is_published",)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone", "created_at")
    search_fields = ("name", "phone", "message")
