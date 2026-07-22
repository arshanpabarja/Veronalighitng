import re

from django.core.management.base import BaseCommand

from Products.models import Category


class Command(BaseCommand):
    help = "Replace 'Verona Lighting' with 'ورونا لایتینگ' in Persian category meta titles."

    def handle(self, *args, **options):

        pattern = re.compile(r"verona\s+lighting", re.IGNORECASE)

        categories = Category.objects.all()
        updated = 0

        for category in categories:

            if not category.meta_title_fa:
                continue

            new_title = pattern.sub(
                "ورونا لایتینگ",
                category.meta_title_fa,
            )

            if new_title != category.meta_title_fa:
                category.meta_title_fa = new_title
                category.save(update_fields=["meta_title_fa"])

                updated += 1

                self.stdout.write(
                    self.style.SUCCESS(f"✔ {category.name}")
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"\nDone! Updated {updated} categories."
            )
        )