from importlib import import_module

from django.apps import apps
from django.test import TestCase

from Products.models import Family, Product


migration = import_module("Products.migrations.0070_use_persian_ceiling_term")


class PersianCeilingTermMigrationTests(TestCase):
    def test_replaces_ceiling_transliteration_in_existing_names(self):
        family = Family.objects.create(
            name_en="Ceiling",
            name_fa="سیلینگ",
            slug="persian-ceiling-family",
        )
        product = Product.objects.create(
            name_en="Ceiling Light",
            name_fa="سیلینگ لایت",
            slug="persian-ceiling-product",
            family=family,
            image1="products/test.png",
        )

        migration.use_persian_ceiling_term(apps, None)

        family.refresh_from_db()
        product.refresh_from_db()
        self.assertEqual(family.name_fa, "سقفی")
        self.assertEqual(product.name_fa, "سقفی لایت")
