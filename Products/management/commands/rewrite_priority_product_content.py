from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from Products.models import Product
from Products.services.priority_product_content import (
    PRIORITY_PRODUCT_CONTENT,
    validate_priority_product_content,
)


class Command(BaseCommand):
    help = (
        "Preview or apply the reviewed bilingual Step 4 SEO content for the "
        "four priority product pages."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--apply",
            action="store_true",
            help="Write changes. Without this flag, the command is read-only.",
        )

    def handle(self, *args, **options):
        validate_priority_product_content()
        apply_changes = options["apply"]
        self.stdout.write(
            self.style.WARNING(
                "APPLY MODE" if apply_changes else "PREVIEW MODE (no database changes)"
            )
        )

        products = {
            product.slug: product
            for product in Product.objects.filter(
                slug__in=PRIORITY_PRODUCT_CONTENT
            ).select_related("category", "family")
        }
        missing = set(PRIORITY_PRODUCT_CONTENT) - set(products)
        if missing:
            raise CommandError(
                "Missing priority products: " + ", ".join(sorted(missing))
            )

        changed_products = 0
        changed_fields = 0
        pending_updates = []

        for slug, campaign in PRIORITY_PRODUCT_CONTENT.items():
            product = products[slug]
            if (
                not product.category
                or product.category.slug != campaign.category_slug
                or not product.family
                or product.family.slug != campaign.family_slug
            ):
                raise CommandError(
                    f"{slug} is not assigned to the expected category and family."
                )

            fa = campaign.translations["fa"]
            en = campaign.translations["en"]
            desired = {
                "name_fa": fa.name,
                "name_en": en.name,
                "subtitle_fa": fa.subtitle,
                "subtitle_en": en.subtitle,
                "description_fa": fa.description,
                "description_en": en.description,
                "meta_title_fa": fa.meta_title,
                "meta_title_en": en.meta_title,
                "meta_description_fa": fa.meta_description,
                "meta_description_en": en.meta_description,
                "image1_alt_fa": fa.image_alt,
                "image1_alt_en": en.image_alt,
            }
            for number in (2, 3, 4):
                if getattr(product, f"image{number}"):
                    desired[f"image{number}_alt_fa"] = fa.image_alt
                    desired[f"image{number}_alt_en"] = en.image_alt

            updates = {
                field: value
                for field, value in desired.items()
                if getattr(product, field) != value
            }
            if not updates:
                self.stdout.write(f"[UNCHANGED] {slug}")
                continue

            changed_products += 1
            changed_fields += len(updates)
            pending_updates.append((product, updates))
            self.stdout.write(
                f"[UPDATE] {slug}: {', '.join(sorted(updates))}"
            )

        if apply_changes:
            with transaction.atomic():
                for product, updates in pending_updates:
                    for field, value in updates.items():
                        setattr(product, field, value)
                    product.save(update_fields=list(updates))

        action = "Updated" if apply_changes else "Would update"
        self.stdout.write(
            self.style.SUCCESS(
                f"{action} {changed_products} products and {changed_fields} fields."
            )
        )
