from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from Products.management.commands.correct_gypsum_catalog_specs import (
    CATALOG_PRODUCTS,
)
from Products.models import Family, Product


class Command(BaseCommand):
    help = (
        "Place every product corrected from the gypsum catalog in one Gypsum "
        "family. Runs as a dry-run unless --apply is supplied."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--apply",
            action="store_true",
            help="Commit the family consolidation to the configured database.",
        )

    def handle(self, *args, **options):
        apply_changes = options["apply"]
        products = list(
            Product.objects.select_related("category", "family")
            .filter(name_en__in=CATALOG_PRODUCTS)
            .order_by("id")
        )
        if len(products) != len(CATALOG_PRODUCTS):
            found = {product.name_en for product in products}
            missing = sorted(set(CATALOG_PRODUCTS) - found)
            raise CommandError(
                "Catalog products missing from the database: "
                + ", ".join(missing)
            )

        category_ids = {product.category_id for product in products}
        if None in category_ids or len(category_ids) != 1:
            raise CommandError(
                "All gypsum catalog products must belong to one category."
            )
        category = products[0].category

        mode = "APPLY" if apply_changes else "DRY RUN"
        self.stdout.write(
            f"{mode}: consolidate {len(products)} products into Gypsum"
        )

        with transaction.atomic():
            old_families = {
                product.family_id: product.family
                for product in products
                if product.family_id
            }
            existing_gypsum = Family.objects.filter(pk=123).first()
            if not existing_gypsum:
                existing_gypsum = Family.objects.filter(
                    name_en__iexact="Gypsum"
                ).first()
            if existing_gypsum and existing_gypsum.category_id != category.id:
                raise CommandError(
                    "A Gypsum family already exists under another category."
                )

            if existing_gypsum:
                gypsum = existing_gypsum
                representative = products[0].family
                if not gypsum.icon and representative and representative.icon:
                    gypsum.icon = representative.icon
            else:
                representative = products[0].family
                if not representative:
                    raise CommandError(
                        "Cannot create Gypsum without a representative family."
                    )
                gypsum = representative

            application_ids = set()
            for family in old_families.values():
                application_ids.update(
                    family.applications.values_list("id", flat=True)
                )

            gypsum.name_en = "Gypsum"
            gypsum.name_fa = "گچی"
            gypsum.slug = "gypsum"
            gypsum.category = category
            gypsum.is_active = True
            gypsum.subtitle_en = "Gypsum recessed lighting family"
            gypsum.subtitle_fa = "خانواده چراغ‌های توکار گچی"
            gypsum.meta_title_en = (
                "Gypsum Recessed Lighting Family | Verona Lighting"
            )
            gypsum.meta_title_fa = (
                "خانواده چراغ‌های توکار گچی | ورونا لایتینگ"
            )
            gypsum.meta_description_en = (
                "Explore Verona Lighting gypsum recessed fixtures, including "
                "single and double GU10 downlights."
            )
            gypsum.meta_description_fa = (
                "مجموعه چراغ‌های توکار گچی ورونا لایتینگ شامل مدل‌های تک‌لامپ "
                "و دولامپ GU10."
            )
            gypsum.icon_alt_en = "Gypsum recessed lighting family"
            gypsum.icon_alt_fa = "خانواده چراغ‌های توکار گچی"
            gypsum.save()
            gypsum.applications.set(application_ids)

            Product.objects.filter(id__in=[p.id for p in products]).update(
                family=gypsum
            )

            removable_ids = [
                family_id
                for family_id in old_families
                if family_id != gypsum.id
                and not Product.objects.filter(family_id=family_id).exists()
            ]
            deleted_families = len(removable_ids)
            if removable_ids:
                Family.objects.filter(id__in=removable_ids).delete()

            self.stdout.write(
                f"  family {gypsum.id}: Gypsum ({gypsum.slug})"
            )
            self.stdout.write(
                f"  assigned products: {len(products)}"
            )
            self.stdout.write(
                f"  removed empty former families: {deleted_families}"
            )

            if not apply_changes:
                transaction.set_rollback(True)
                self.stdout.write(
                    self.style.WARNING(
                        "Dry-run complete; PostgreSQL was not changed."
                    )
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(
                        "Gypsum family consolidation committed to PostgreSQL."
                    )
                )
