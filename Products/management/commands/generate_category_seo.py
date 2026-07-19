from django.core.management.base import BaseCommand
from django.db import transaction

from Products.models import Family
from Products.services.translator import translate_product


class Command(BaseCommand):
    help = "Generate SEO for families using AI"

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Regenerate SEO even if it already exists.",
        )

    def handle(self, *args, **options):

        force = options["force"]

        families = Family.objects.all().select_related("category")

        total = families.count()

        self.stdout.write(
            self.style.SUCCESS(f"Found {total} families.\n")
        )

        for index, family in enumerate(families, start=1):

            if (
                not force
                and family.meta_title_en
                and family.meta_description_en
                and family.meta_title_fa
                and family.meta_description_fa
            ):
                self.stdout.write(
                    self.style.WARNING(
                        f"[{index}/{total}] Skipped: {family.name}"
                    )
                )
                continue

            try:

                data = {
                    "name_en": family.name_en,
                    "name_fa": family.name_fa,
                    "subtitle_en": family.subtitle_en,
                    "subtitle_fa": family.subtitle_fa,
                    "category_en": (
                        family.category.name_en
                        if family.category
                        else ""
                    ),
                    "category_fa": (
                        family.category.name_fa
                        if family.category
                        else ""
                    ),
                }

                seo = translate_product(data)

                with transaction.atomic():

                    family.meta_title_en = seo["meta_title_en"]
                    family.meta_description_en = seo["meta_description_en"]

                    family.meta_title_fa = seo["meta_title_fa"]
                    family.meta_description_fa = seo["meta_description_fa"]

                    family.icon_alt_fa = seo["icon_alt_fa"]
                    family.icon_alt_en = seo["icon_alt_en"]

                    family.save(
                        update_fields=[
                            "meta_title_en",
                            "meta_description_en",
                            "meta_title_fa",
                            "meta_description_fa",
                        ]
                    )

                self.stdout.write(
                    self.style.SUCCESS(
                        f"[{index}/{total}] ✔ {family.name}"
                    )
                )

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f"[{index}/{total}] ✖ {family.name} -> {e}"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS("\nFamily SEO generation completed.")
        )