from django.core.management.base import BaseCommand
from django.db import transaction

from Products.services.translator import translate_product
from Products.models import Product


class Command(BaseCommand):
    help = "Generate SEO for products using AI"

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Regenerate SEO even if it already exists.",
        )

    def handle(self, *args, **options):

        force = options["force"]

        products = Product.objects.all().select_related(
            "category",
            "family",
        )

        total = products.count()

        self.stdout.write(self.style.SUCCESS(f"Found {total} products.\n"))

        for index, product in enumerate(products, start=1):

            if (
                not force
                and product.meta_title_en
                and product.meta_description_en
                and product.image1_alt
            ):
                self.stdout.write(
                    self.style.WARNING(
                        f"[{index}/{total}] Skipped: {product.name}"
                    )
                )
                continue

            try:

                data = {
                    "name": product.name_en,
                    "subtitle": product.subtitle_en,
                    "description": product.description_en,
                    "full_description": product.full_description_en,
                    "category": (
                        product.category.name_en
                        if product.category
                        else ""
                    ),
                    "family": (
                        product.family.name_en
                        if product.family
                        else ""
                    ),
                }

                seo = translate_product(data)

                with transaction.atomic():
                    product.meta_title_en = seo["meta_title"]
                    product.meta_description_en = seo["meta_description"]
                    product.image1_alt = seo["image1_alt"]

                    product.save(
                        update_fields=[
                            "meta_title_en",
                            "meta_description_en",
                            "image1_alt",
                        ]
                    )

                self.stdout.write(
                    self.style.SUCCESS(
                        f"[{index}/{total}] ✔ {product.name}"
                    )
                )

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f"[{index}/{total}] ✖ {product.name} -> {e}"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS("\nSEO generation completed.")
        )