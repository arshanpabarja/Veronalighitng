from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.html import strip_tags

from Products.models import Product
from Products.services.fa_seo import (
    build_full_description_fa,
    build_product_fa_seo,
)


class Command(BaseCommand):
    help = (
        "Preview or improve missing/thin Persian full product descriptions. "
        "Descriptions already meeting the minimum length are preserved."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--apply",
            action="store_true",
            help="Write changes. Without this flag, run as a preview.",
        )
        parser.add_argument(
            "--min-chars",
            type=int,
            default=500,
            help="Improve descriptions shorter than this length (default: 500).",
        )
        parser.add_argument(
            "--limit",
            type=int,
            help="Limit the number of matching products.",
        )
        parser.add_argument(
            "--quiet",
            action="store_true",
            help="Hide per-product output.",
        )

    def handle(self, *args, **options):
        apply_changes = options["apply"]
        min_chars = options["min_chars"]
        limit = options["limit"]
        quiet = options["quiet"]

        if min_chars < 200:
            raise CommandError("--min-chars must be at least 200.")
        if limit is not None and limit < 1:
            raise CommandError("--limit must be greater than zero.")

        products = (
            Product.objects.filter(is_active=True)
            .select_related("category", "family")
            .order_by("order", "pk")
        )
        candidates = []
        for product in products:
            current = " ".join(strip_tags(product.full_description_fa or "").split())
            if len(current) < min_chars:
                candidates.append((product, current))
        if limit:
            candidates = candidates[:limit]

        self.stdout.write(
            self.style.WARNING(
                "APPLY MODE" if apply_changes else "PREVIEW MODE (no database changes)"
            )
        )

        updated = 0
        for product, current in candidates:
            category = product.category
            family = product.family
            data = {
                "name_en": product.name_en,
                "name_fa": product.name_fa,
                "subtitle_en": product.subtitle_en,
                "subtitle_fa": product.subtitle_fa,
                "description_en": product.description_en,
                "description_fa": product.description_fa,
                "full_description_en": product.full_description_en,
                "full_description_fa": product.full_description_fa,
                "category_en": category.name_en if category else "",
                "category_fa": category.name_fa if category else "",
                "category_slug": category.slug if category else "",
                "family_en": family.name_en if family else "",
                "family_fa": family.name_fa if family else "",
                "wattage": product.wattage,
                "lumens": product.lumens,
                "color_temperature": product.color_temperature,
                "cri": product.cri,
                "ip_rating": product.ip_rating,
                "voltage": product.voltage,
            }
            seo = build_product_fa_seo(data)
            improved = build_full_description_fa(
                data,
                existing_text=product.full_description_fa or product.description_fa,
            )
            if not quiet:
                self.stdout.write(
                    f"[P{seo.priority}] {product.pk} {product.name_en or product.name}: "
                    f"{len(current)} -> {len(improved)} chars ({seo.keyword})"
                )
            if apply_changes:
                with transaction.atomic():
                    product.full_description_fa = improved
                    product.save(update_fields=["full_description_fa"])
            updated += 1

        action = "Updated" if apply_changes else "Would update"
        self.stdout.write(self.style.SUCCESS(f"{action} {updated} products."))
