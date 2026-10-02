from django.core.management import call_command
from django.test import TestCase

from Products.models import Family, Product
from Products.services.catalog_fa_names import (
    UnknownCatalogTerm,
    translate_catalog_name,
)


class CatalogPersianNameTests(TestCase):
    def test_requested_technical_terms_are_transliterated_without_extra_copy(self):
        examples = {
            "MAGNETO DOT LINEAR": "چراغ خطی دات مگنتو",
            "TRIMLESS SINGLE": "چراغ بدون لبه سینگل",
            "TRIM TRIMMED TRIMLES": "چراغ بدون لبه لبه‌دار",
            "ROTATE DUAL TRIPLE": "چراغ روتیت دوبل تریپل",
            "Strip Light 220v IP65": "چراغ استریپ 220V IP65",
            "Lei MID FL-TL": "چراغ لی مید اف‌ال-تی‌ال",
            "Lina onefold": "چراغ لینا وان‌فولد",
            "Recessed Ressed Ressessd": "چراغ توکار",
            "Pendant Surface Gypsum": "چراغ روکار و آویز گچی",
            "Recessed Track": "ریل توکار",
            "Ceiling Light": "چراغ سقفی",
        }
        for source, expected in examples.items():
            with self.subTest(source=source):
                self.assertEqual(translate_catalog_name(source), expected)

    def test_unreviewed_term_fails_instead_of_being_guessed(self):
        with self.assertRaises(UnknownCatalogTerm):
            translate_catalog_name("MAGNETO UNREVIEWED")

    def test_offline_command_updates_products_and_families_from_english(self):
        family = Family.objects.create(
            name_en="MAGNETO DOT LINEAR",
            name_fa="ترجمه قبلی",
            slug="offline-name-family",
        )
        product = Product.objects.create(
            name_en="TRIMLESS SINGLE",
            name_fa="نام قبلی",
            slug="offline-name-product",
            family=family,
            image1="products/test.png",
        )

        call_command("retranslate_catalog_fa", "--apply")

        family.refresh_from_db()
        product.refresh_from_db()
        self.assertEqual(family.name_fa, "چراغ خطی دات مگنتو")
        self.assertEqual(product.name_fa, "چراغ بدون لبه سینگل")

    def test_offline_command_omits_downlight_only_for_gypsum_products(self):
        gypsum = Family.objects.create(
            name_en="Gypsum",
            name_fa="گچی",
            slug="gypsum",
        )
        other = Family.objects.create(
            name_en="Recessed",
            name_fa="توکار",
            slug="other-downlights",
        )
        gypsum_product = Product.objects.create(
            name_en="Virgo Downlight",
            name_fa="نام قبلی",
            slug="gypsum-downlight-test",
            family=gypsum,
            image1="products/test.png",
        )
        other_product = Product.objects.create(
            name_en="Spy Downlight",
            name_fa="نام قبلی",
            slug="other-downlight-test",
            family=other,
            image1="products/test.png",
        )

        call_command("retranslate_catalog_fa", "--apply")

        gypsum_product.refresh_from_db()
        other_product.refresh_from_db()
        self.assertEqual(gypsum_product.name_fa, "چراغ ویرگو")
        self.assertEqual(other_product.name_fa, "چراغ دان‌لایت اسپای")
