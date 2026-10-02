from importlib import import_module

from django.apps import apps
from django.test import TestCase

from Products.models import Category, Family, Product


migration = import_module(
    "Products.migrations.0057_normalize_sp_lineo_product_names"
)


class SpLineoNameNormalizationTests(TestCase):
    def setUp(self):
        category = Category.objects.create(name="Recessed", slug="recessed")
        self.family = Family.objects.create(
            name="SP LINEO",
            slug=migration.SP_LINEO_FAMILY_SLUG,
            category=category,
        )
        self.other_family = Family.objects.create(
            name="Other",
            slug="other-family",
            category=category,
        )

    def test_normalizes_all_sp_lineo_persian_product_names(self):
        products = []
        for slug, expected_name in migration.PRODUCT_NAMES_FA.items():
            product = Product.objects.create(
                name="Legacy name",
                name_fa="نام قدیمی",
                name_en=slug,
                slug=slug,
                family=self.family,
                image1=f"products/{slug}.png",
                meta_title_fa="چراغ نقطه‌ای اس‌پی باریک",
            )
            products.append((product, expected_name))

        migration.normalize_sp_lineo_product_names(apps, None)

        for product, expected_name in products:
            product.refresh_from_db()
            self.assertEqual(product.name, expected_name)
            self.assertEqual(product.name_fa, expected_name)
            self.assertEqual(
                product.meta_title_fa,
                "چراغ دات SP نارو",
            )

        self.assertEqual(
            migration.normalize_sp_terms("SP NARROW"),
            "SP نارو",
        )

    def test_does_not_change_matching_slug_outside_sp_lineo(self):
        product = Product.objects.create(
            name="Outside",
            name_fa="نام بیرونی",
            slug="sp-narrow",
            family=self.other_family,
            image1="products/outside.png",
        )

        migration.normalize_sp_lineo_product_names(apps, None)

        product.refresh_from_db()
        self.assertEqual(product.name_fa, "نام بیرونی")
