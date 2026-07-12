from django.core.management.base import BaseCommand

from Products.models import Product
from Products.services.translator import translate_product


class Command(BaseCommand):
    help = "Translate all products to Persian"

    def handle(self, *args, **options):

        # فقط محصولاتی که هنوز ترجمه فارسی ندارند
        products = Product.objects.filter(
            name_fa__isnull=True
        ) | Product.objects.filter(
            name_fa=""
        )

        products = products.order_by("id")

        self.stdout.write(
            self.style.SUCCESS(f"\nFound {products.count()} products\n")
        )

        translated_count = 0
        skipped_count = 0
        failed_count = 0

        for product in products:

            # اگر قبلاً ترجمه شده ردش کن
            if product.name_fa:
                skipped_count += 1
                self.stdout.write(
                    self.style.WARNING(f"⏭ Skipped: {product.name}")
                )
                continue

            data = {
                "name": product.name_en or product.name,
                "subtitle": product.subtitle_en or product.subtitle,
                "description": product.description_en or product.description,
                "full_description": product.full_description_en or product.full_description,
                "meta_title": product.meta_title_en or product.meta_title,
                "meta_description": product.meta_description_en or product.meta_description,
                "image1_alt": product.image1_alt_en or product.image1_alt,
                "image2_alt": product.image2_alt_en or product.image2_alt,
                "image3_alt": product.image3_alt_en or product.image3_alt,
                "image4_alt": product.image4_alt_en or product.image4_alt,
            }

            self.stdout.write(f"🌐 Translating #{product.id} - {product.name}")

            try:
                translated = translate_product(data)

                product.name_fa = translated.get("name", "")
                product.subtitle_fa = translated.get("subtitle", "")
                product.description_fa = translated.get("description", "")
                product.full_description_fa = translated.get("full_description", "")
                product.meta_title_fa = translated.get("meta_title", "")
                product.meta_description_fa = translated.get("meta_description", "")
                product.image1_alt_fa = translated.get("image1_alt", "")
                product.image2_alt_fa = translated.get("image2_alt", "")
                product.image3_alt_fa = translated.get("image3_alt", "")
                product.image4_alt_fa = translated.get("image4_alt", "")

                product.save()

                translated_count += 1

                self.stdout.write(
                    self.style.SUCCESS(f"✅ Saved: {product.name}")
                )

            except Exception as e:

                failed_count += 1

                self.stdout.write(
                    self.style.ERROR(f"❌ Failed: {product.name}")
                )

                self.stdout.write(str(e))

                # برو سراغ محصول بعدی
                continue

        self.stdout.write("\n")
        self.stdout.write(self.style.SUCCESS("========== DONE =========="))
        self.stdout.write(f"Translated : {translated_count}")
        self.stdout.write(f"Skipped    : {skipped_count}")
        self.stdout.write(f"Failed     : {failed_count}")