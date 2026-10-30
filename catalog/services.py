from django.conf import settings
from django.core.cache import cache

from catalog.models import Product

MODERATOR_GROUP_NAME = "Модератор продуктов"


def get_products_by_category(category_id):
    """Возвращает продукты категории с низкоуровневым кешированием в Redis."""
    cache_key = f"category_{category_id}"
    products = cache.get(cache_key)

    if products is not None:
        return products

    products = list(
        Product.objects.filter(
            category_id=category_id,
            is_published=True,
        ).select_related("category", "owner")
    )
    cache.set(cache_key, products, settings.CACHE_TTL)
    return products


def user_is_moderator(user):
    """Проверяет, является ли пользователь модератором продуктов."""
    if not user.is_authenticated:
        return False
    return (
        user.has_perm("catalog.can_unpublish_product")
        or user.groups.filter(name=MODERATOR_GROUP_NAME).exists()
    )


def user_can_edit_product(user, product):
    """Редактировать может владелец или модератор."""
    if not user.is_authenticated:
        return False
    return product.owner_id == user.id or user_is_moderator(user)


def user_can_delete_product(user, product):
    """Удалять может владелец или модератор."""
    if not user.is_authenticated:
        return False
    return (
        product.owner_id == user.id
        or user.has_perm("catalog.delete_product")
        or user_is_moderator(user)
    )


def user_can_unpublish_product(user):
    """Отменять публикацию может пользователь с правом can_unpublish_product."""
    return user.is_authenticated and user.has_perm(
        "catalog.can_unpublish_product"
    )
