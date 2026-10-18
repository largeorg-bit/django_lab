from django.core.management import call_command
from django.core.management.base import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    help = "Удаляет данные каталога и загружает тестовые объекты из фикстур"

    def handle(self, *args, **options):
        Product.objects.all().delete()
        Category.objects.all().delete()

        call_command("loaddata", "categories.json")
        call_command("loaddata", "products.json")

        self.stdout.write(
            self.style.SUCCESS("Тестовые данные успешно загружены")
        )
