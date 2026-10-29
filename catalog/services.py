MODERATOR_GROUP_NAME = "Модератор продуктов"


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
