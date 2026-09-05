from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from Products.services.catalog_application_images import (
    CATALOG_APPLICATION_PAGE_BY_SLUG,
    extract_catalog_application_images,
)


class Command(BaseCommand):
    help = (
        "Extract the lower application-scene images from mapped product intro "
        "pages in the 2024 technical catalogue."
    )

    def add_arguments(self, parser):
        parser.add_argument("pdf_path", help="Path to Binder1_707930.pdf")
        parser.add_argument(
            "--overwrite",
            action="store_true",
            help="Replace application assets that were already extracted.",
        )

    def handle(self, *args, **options):
        try:
            extracted, skipped = extract_catalog_application_images(
                options["pdf_path"],
                settings.MEDIA_ROOT,
                overwrite=options["overwrite"],
            )
        except (FileNotFoundError, OSError, RuntimeError, ValueError) as exc:
            raise CommandError(str(exc)) from exc

        self.stdout.write(
            self.style.SUCCESS(
                f"Mapped {len(CATALOG_APPLICATION_PAGE_BY_SLUG)} products; "
                f"extracted {len(extracted)} unique application images and "
                f"skipped {len(skipped)} existing files."
            )
        )
