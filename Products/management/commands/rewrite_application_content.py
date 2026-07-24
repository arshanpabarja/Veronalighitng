from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from Products.models import Application
from Products.services.application_content import (
    APPLICATION_CONTENT,
    validate_application_content,
)


class Command(BaseCommand):
    help = (
        "Preview or apply reviewed bilingual names, descriptions, image alt "
        "text and SEO metadata for all active application pages."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--apply",
            action="store_true",
            help="Write the reviewed application content to the database.",
        )

    def handle(self, *args, **options):
        try:
            validate_application_content()
        except ValueError as exc:
            raise CommandError(str(exc)) from exc

        applications = list(Application.objects.filter(is_active=True).order_by("pk"))
        active_slugs = {application.slug for application in applications}
        mapped_slugs = set(APPLICATION_CONTENT)
        missing = sorted(active_slugs - mapped_slugs)
        stale = sorted(mapped_slugs - active_slugs)
        if missing or stale:
            raise CommandError(
                f"Application map mismatch. Missing={missing or 'none'}; "
                f"inactive/unknown={stale or 'none'}"
            )

        apply_changes = options["apply"]
        if not apply_changes:
            self.stdout.write("PREVIEW MODE (no database changes)")

        changed = 0
        with transaction.atomic():
            for application in applications:
                content = APPLICATION_CONTENT[application.slug]
                values = {
                    "name_fa": content.name_fa,
                    "name_en": content.name_en,
                    "short_description_fa": content.short_description_fa,
                    "short_description_en": content.short_description_en,
                    "description_fa": content.description_fa,
                    "description_en": content.description_en,
                    "meta_title_fa": content.meta_title_fa,
                    "meta_title_en": content.meta_title_en,
                    "meta_description_fa": content.meta_description_fa,
                    "meta_description_en": content.meta_description_en,
                    "cover_image_alt_fa": content.cover_image_alt_fa,
                    "cover_image_alt_en": content.cover_image_alt_en,
                }
                updates = {
                    field: value
                    for field, value in values.items()
                    if getattr(application, field) != value
                }
                if not updates:
                    continue

                changed += 1
                self.stdout.write(
                    f"{application.pk}: {application.slug} "
                    f"(fa={len(content.description_fa)}, "
                    f"en={len(content.description_en)}, fields={len(updates)})"
                )
                if apply_changes:
                    for field, value in updates.items():
                        setattr(application, field, value)
                    application.save(update_fields=list(updates))

            if not apply_changes:
                transaction.set_rollback(True)

        verb = "Updated" if apply_changes else "Would update"
        self.stdout.write(self.style.SUCCESS(f"{verb} {changed} applications."))
