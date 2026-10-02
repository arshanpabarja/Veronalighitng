from importlib import import_module

from django.apps import apps
from django.test import TestCase

from Products.models import Family, Product


migration = import_module("Products.migrations.0066_use_persian_trim_terms")


class PersianTrimTermMigrationTests(TestCase):
    def test_replaces_trim_transliterations_in_existing_names(self):
        family = Family.objects.create(
            name_en="Recessed Trimless",
            name_fa="توکار تریم لس",
            slug="persian-trim-family",
        )
        product = Product.objects.create(
            name_en="Recessed Trim",
            name_fa="توکار تریم",
            slug="persian-trim-product",
            family=family,
            image1="products/test.png",
        )

        migration.use_persian_trim_terms(apps, None)

        family.refresh_from_db()
        product.refresh_from_db()
        self.assertEqual(family.name_fa, "توکار بدون لبه")
        self.assertEqual(product.name_fa, "توکار لبه‌دار")
