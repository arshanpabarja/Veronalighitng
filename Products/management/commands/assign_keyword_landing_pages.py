from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from Products.models import Category
from Products.services.keyword_strategy import (
    KEYWORD_LANDING_PAGES,
    SUPPORTING_CATEGORY_METADATA,
    validate_keyword_strategy,
)


class Command(BaseCommand):
    help = (
        "Preview or apply the primary landing-page ownership map for the "
        "90-day Persian SEO campaign. Preview mode is the default."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--apply",
            action="store_true",
            help="Write the approved keyword ownership metadata to the database.",
        )

    def handle(self, *args, **options):
        try:
            validate_keyword_strategy()
        except ValueError as exc:
            raise CommandError(str(exc)) from exc

        apply_changes = options["apply"]
        if not apply_changes:
            self.stdout.write("PREVIEW MODE (no database changes)")

        changed = 0
        with transaction.atomic():
            for landing_page in KEYWORD_LANDING_PAGES.values():
                filters = {
                    "slug": landing_page.category_slug,
                    "is_active": True,
                }
                if landing_page.parent_slug:
                    filters["parent__slug"] = landing_page.parent_slug
                    filters["parent__is_active"] = True
                else:
                    filters["parent__isnull"] = True

                try:
                    category = Category.objects.get(**filters)
                except Category.DoesNotExist as exc:
                    raise CommandError(
                        f"Primary category is missing for {landing_page.cluster}: "
                        f"{filters}"
                    ) from exc

                values = {
                    "name_fa": landing_page.name_fa,
                    "name_en": landing_page.name_en,
                    "meta_title_fa": landing_page.meta_title_fa,
                    "meta_title_en": landing_page.meta_title_en,
                    "meta_description_fa": landing_page.meta_description_fa,
                    "meta_description_en": landing_page.meta_description_en,
                }
                updates = {
                    field: value
                    for field, value in values.items()
                    if getattr(category, field) != value
                }
                if updates:
                    changed += 1
                    if apply_changes:
                        for field, value in updates.items():
                            setattr(category, field, value)
                        category.save(update_fields=[*updates, "updated_at"])

                self.stdout.write(
                    f"{landing_page.primary_keyword_fa} -> "
                    f"{category.get_absolute_url()}"
                )

            for slug, values in SUPPORTING_CATEGORY_METADATA.items():
                try:
                    category = Category.objects.get(
                        slug=slug,
                        is_active=True,
                        parent__isnull=True,
                    )
                except Category.DoesNotExist as exc:
                    raise CommandError(
                        f"Supporting category is missing: {slug}"
                    ) from exc

                updates = {
                    field: value
                    for field, value in values.items()
                    if getattr(category, field) != value
                }
                if updates:
                    changed += 1
                    if apply_changes:
                        for field, value in updates.items():
                            setattr(category, field, value)
                        category.save(update_fields=[*updates, "updated_at"])

            if not apply_changes:
                transaction.set_rollback(True)

        verb = "Updated" if apply_changes else "Would update"
        self.stdout.write(self.style.SUCCESS(f"{verb} {changed} categories."))
