from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from catalog.models import Product
from catalog.services import MODERATOR_GROUP_NAME


class Command(BaseCommand):
    help = "Создаёт группу «Модератор продуктов» с нужными правами"

    def handle(self, *args, **options):
        content_type = ContentType.objects.get_for_model(Product)

        can_unpublish = Permission.objects.get(
            codename="can_unpublish_product",
            content_type=content_type,
        )
        delete_product = Permission.objects.get(
            codename="delete_product",
            content_type=content_type,
        )

        group, created = Group.objects.get_or_create(name=MODERATOR_GROUP_NAME)
        group.permissions.set([can_unpublish, delete_product])

        action = "создана" if created else "обновлена"
        self.stdout.write(
            self.style.SUCCESS(
                f'Группа «{MODERATOR_GROUP_NAME}» {action}. '
                f"Права: can_unpublish_product, delete_product."
            )
        )
