from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from Products.models import Family, Product
from Products.services.catalog_fa_names import (
    UnknownCatalogTerm,
    translate_catalog_name,
)


class Command(BaseCommand):
    help = "Retranslate Persian product and family names offline from English"

    def add_arguments(self, parser):
        parser.add_argument(
            "--apply",
            action="store_true",
            help="Save translations. Without this flag the command is a preview.",
        )

    def handle(self, *args, **options):
        rows = [
            *(('Family', item) for item in Family.objects.order_by('id')),
            *(('Product', item) for item in Product.objects.order_by('id')),
        ]

        try:
            changes = [
                (kind, item, self._translate_name(kind, item))
                for kind, item in rows
            ]
        except UnknownCatalogTerm as exc:
            raise CommandError(str(exc)) from exc

        changed = [row for row in changes if row[1].name_fa != row[2]]
        for kind, item, translated_name in changed:
            self.stdout.write(
                f"{kind} #{item.pk}: {item.name_en} -> {translated_name}"
            )

        if not options["apply"]:
            self.stdout.write(
                self.style.WARNING(
                    f"Preview only: {len(changed)} of {len(rows)} names would change."
                )
            )
            return

        with transaction.atomic():
            for _, item, translated_name in changed:
                item.name_fa = translated_name
                item.save(update_fields=["name_fa"])

        self.stdout.write(
            self.style.SUCCESS(
                f"Updated {len(changed)} of {len(rows)} Persian catalog names."
            )
        )

    @staticmethod
    def _translate_name(kind, item):
        family = item.family if kind == "Product" and item.family_id else None
        if kind == "Family":
            is_gypsum = (
                item.slug == "gypsum"
                or "gypsum" in (item.name_en or "").casefold()
                or "گچی" in (item.name_fa or "")
            )
        else:
            is_gypsum = bool(
                family
                and (
                family.slug == "gypsum"
                or "gypsum" in (family.name_en or "").casefold()
                or "گچی" in (family.name_fa or "")
                )
            )
        category = item.category
        return translate_catalog_name(
            item.name_en or "",
            category_name=category.name_en if category else "",
            parent_category_name=(
                category.parent.name_en if category and category.parent else ""
            ),
            is_gypsum=is_gypsum,
        )
