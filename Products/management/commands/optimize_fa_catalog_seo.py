from collections import Counter

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from Products.models import Category, Family, Product
from Products.services.fa_seo import (
    build_category_fa_seo,
    build_family_fa_seo,
    build_product_fa_seo,
)


class Command(BaseCommand):
    help = (
        "Preview or apply safe Persian SEO metadata for the complete product "
        "catalogue. Existing values are preserved unless --force is supplied."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--apply",
            action="store_true",
            help="Write changes to the database. Without this flag, run as a preview.",
        )
        parser.add_argument(
            "--scope",
            choices=("products", "families", "categories", "all"),
            default="all",
            help="Catalogue level to process (default: all).",
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="Overwrite existing Persian SEO values.",
        )
        parser.add_argument(
            "--fill-missing-descriptions",
            action="store_true",
            help="Fill an empty Persian short description using only safe catalogue facts.",
        )
        parser.add_argument(
            "--priority",
            type=int,
            choices=(1, 2, 3),
            help="Process only one campaign priority.",
        )
        parser.add_argument(
            "--limit",
            type=int,
            help="Limit the number of products processed.",
        )
        parser.add_argument(
            "--quiet",
            action="store_true",
            help="Hide per-object preview lines and print only the summary.",
        )

    def handle(self, *args, **options):
        apply_changes = options["apply"]
        scope = options["scope"]
        force = options["force"]
        fill_descriptions = options["fill_missing_descriptions"]
        requested_priority = options["priority"]
        limit = options["limit"]
        quiet = options["quiet"]

        if limit is not None and limit < 1:
            raise CommandError("--limit must be greater than zero.")

        counters = Counter()
        changed_objects = Counter()

        self.stdout.write(
            self.style.WARNING(
                "APPLY MODE" if apply_changes else "PREVIEW MODE (no database changes)"
            )
        )

        if scope in ("categories", "all"):
            categories = Category.objects.filter(is_active=True).order_by("order", "pk")
            if limit:
                categories = categories[:limit]
            for category in categories:
                seo = build_category_fa_seo(
                    {
                        "name_en": category.name_en,
                        "name_fa": category.name_fa,
                        "description_en": category.description_en,
                        "description_fa": category.description_fa,
                        "category_en": category.name_en,
                        "category_fa": category.name_fa,
                        "slug": category.slug,
                    }
                )
                if requested_priority and seo.priority != requested_priority:
                    continue
                updates = self._updates(
                    category,
                    {
                        "meta_title_fa": seo.meta_title,
                        "meta_description_fa": seo.meta_description,
                        **(
                            {"description_fa": seo.short_description}
                            if fill_descriptions
                            else {}
                        ),
                    },
                    force,
                )
                if updates:
                    self._write(category, updates, apply_changes)
                    changed_objects["categories"] += 1
                    counters[seo.keyword] += 1
                    if not quiet:
                        self.stdout.write(
                            f"[CATEGORY P{seo.priority}] {category.pk}: {seo.meta_title}"
                        )

        if scope in ("families", "all"):
            families = (
                Family.objects.filter(is_active=True)
                .select_related("category")
                .order_by("number", "pk")
            )
            if limit:
                families = families[:limit]
            for family in families:
                category = family.category
                seo = build_family_fa_seo(
                    {
                        "name_en": family.name_en,
                        "name_fa": family.name_fa,
                        "subtitle_en": family.subtitle_en,
                        "subtitle_fa": family.subtitle_fa,
                        "category_en": category.name_en if category else "",
                        "category_fa": category.name_fa if category else "",
                    }
                )
                if requested_priority and seo.priority != requested_priority:
                    continue
                updates = self._updates(
                    family,
                    {
                        "meta_title_fa": seo.meta_title,
                        "meta_description_fa": seo.meta_description,
                        "icon_alt_fa": seo.image_alt,
                        **(
                            {"subtitle_fa": seo.short_description}
                            if fill_descriptions
                            else {}
                        ),
                    },
                    force,
                )
                if updates:
                    self._write(family, updates, apply_changes)
                    changed_objects["families"] += 1
                    counters[seo.keyword] += 1
                    if not quiet:
                        self.stdout.write(
                            f"[FAMILY P{seo.priority}] {family.pk}: {seo.meta_title}"
                        )

        if scope not in ("products", "all"):
            self._summary(apply_changes, changed_objects, counters)
            return

        products = (
            Product.objects.filter(is_active=True)
            .select_related("category", "family")
            .order_by("order", "pk")
        )
        if limit:
            products = products[:limit]

        for product in products:
            category = product.category
            family = product.family
            seo = build_product_fa_seo(
                {
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
            )

            if requested_priority and seo.priority != requested_priority:
                continue

            counters[seo.keyword] += 1
            field_values = {
                "meta_title_fa": seo.meta_title,
                "meta_description_fa": seo.meta_description,
                "image1_alt_fa": seo.image_alt,
                "image2_alt_fa": seo.image_alt,
                "image3_alt_fa": seo.image_alt,
                "image4_alt_fa": seo.image_alt,
            }
            if fill_descriptions:
                field_values["description_fa"] = seo.short_description

            updates = self._updates(product, field_values, force)

            if not updates:
                counters["unchanged"] += 1
                continue

            changed_objects["products"] += 1
            if not quiet:
                self.stdout.write(
                    f"[P{seo.priority}] {product.pk} {product.name_en or product.name}: "
                    f"{seo.keyword} -> {seo.meta_title}"
                )

            self._write(product, updates, apply_changes)

        self._summary(apply_changes, changed_objects, counters)

    @staticmethod
    def _updates(instance, field_values, force):
        updates = {}
        for field, value in field_values.items():
            if force or not getattr(instance, field, ""):
                updates[field] = value
        return updates

    @staticmethod
    def _write(instance, updates, apply_changes):
        if not apply_changes:
            return
        with transaction.atomic():
            for field, value in updates.items():
                setattr(instance, field, value)
            instance.save(update_fields=list(updates))

    def _summary(self, apply_changes, changed_objects, counters):
        self.stdout.write("")
        action = "Updated" if apply_changes else "Would update"
        self.stdout.write(
            self.style.SUCCESS(
                f"{action} {changed_objects['categories']} categories, "
                f"{changed_objects['families']} families, and "
                f"{changed_objects['products']} products."
            )
        )
        for keyword, count in counters.most_common():
            self.stdout.write(f"{keyword}: {count}")
