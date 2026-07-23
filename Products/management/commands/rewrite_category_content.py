from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from Products.models import Category
from Products.services.category_content import (
    CATEGORY_CONTENT,
    validate_category_content,
)


class Command(BaseCommand):
    help = (
        "Preview or apply reviewed bilingual descriptions and metadata for all "
        "active product categories. Preview mode is the default."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--apply",
            action="store_true",
            help="Write the reviewed category content to the database.",
        )

    def handle(self, *args, **options):
        try:
            validate_category_content()
        except ValueError as exc:
            raise CommandError(str(exc)) from exc

        categories = list(Category.objects.filter(is_active=True).order_by("pk"))
        active_slugs = {category.slug for category in categories}
        mapped_slugs = set(CATEGORY_CONTENT)
        missing = sorted(active_slugs - mapped_slugs)
        stale = sorted(mapped_slugs - active_slugs)
        if missing or stale:
            raise CommandError(
                f"Category map mismatch. Missing={missing or 'none'}; "
                f"inactive/unknown={stale or 'none'}"
            )

        apply_changes = options["apply"]
        if not apply_changes:
            self.stdout.write("PREVIEW MODE (no database changes)")

        changed = 0
        with transaction.atomic():
            for category in categories:
                content = CATEGORY_CONTENT[category.slug]
                values = {
                    "description_fa": content.description_fa,
                    "description_en": content.description_en,
                    "meta_title_fa": content.meta_title_fa,
                    "meta_title_en": content.meta_title_en,
                    "meta_description_fa": content.meta_description_fa,
                    "meta_description_en": content.meta_description_en,
                }
                updates = {
                    field: value
                    for field, value in values.items()
                    if getattr(category, field) != value
                }
                if not updates:
                    continue
                changed += 1
                self.stdout.write(
                    f"{category.pk}: {category.slug} "
                    f"(fa={len(content.description_fa)}, "
                    f"en={len(content.description_en)})"
                )
                if apply_changes:
                    for field, value in updates.items():
                        setattr(category, field, value)
                    category.save(update_fields=[*updates, "updated_at"])

            if not apply_changes:
                transaction.set_rollback(True)

        verb = "Updated" if apply_changes else "Would update"
        self.stdout.write(self.style.SUCCESS(f"{verb} {changed} categories."))
