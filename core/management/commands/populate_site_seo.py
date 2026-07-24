from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from core.models import SiteSettings
from core.site_seo import SITE_SEO, validate_site_seo


class Command(BaseCommand):
    help = (
        "Preview or apply reviewed bilingual metadata for the home, about, "
        "story, products, applications and news list pages."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--apply",
            action="store_true",
            help="Write the reviewed metadata to SiteSettings.",
        )

    def handle(self, *args, **options):
        try:
            validate_site_seo()
        except ValueError as exc:
            raise CommandError(str(exc)) from exc

        settings = SiteSettings.get()
        values = {}
        for prefix, content in SITE_SEO.items():
            for language in ("fa", "en"):
                values[f"{prefix}_meta_title_{language}"] = getattr(
                    content, f"meta_title_{language}"
                )
                values[f"{prefix}_meta_description_{language}"] = getattr(
                    content, f"meta_description_{language}"
                )
                values[f"{prefix}_og_title_{language}"] = getattr(
                    content, f"og_title_{language}"
                )
                values[f"{prefix}_og_description_{language}"] = getattr(
                    content, f"og_description_{language}"
                )

        updates = {
            field: value
            for field, value in values.items()
            if getattr(settings, field) != value
        }
        if not options["apply"]:
            self.stdout.write("PREVIEW MODE (no database changes)")
            self.stdout.write(
                self.style.SUCCESS(f"Would update {len(updates)} SEO fields.")
            )
            return

        with transaction.atomic():
            for field, value in updates.items():
                setattr(settings, field, value)
            if updates:
                settings.save(update_fields=list(updates))

        self.stdout.write(
            self.style.SUCCESS(f"Updated {len(updates)} SEO fields.")
        )
