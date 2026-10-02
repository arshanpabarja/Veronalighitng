from importlib import import_module

from django.apps import apps
from django.test import TestCase

from Products.models import Family, Product


migration = import_module("Products.migrations.0068_use_persian_track_term")


class PersianTrackTermMigrationTests(TestCase):
    def test_replaces_track_transliteration_without_duplicate_rail(self):
        family = Family.objects.create(
            name_en="Track",
            name_fa="ترک",
            slug="persian-track-family",
        )
        product = Product.objects.create(
            name_en="Rail Track",
            name_fa="ریل ترک",
            slug="persian-track-product",
            family=family,
            image1="products/test.png",
        )

        migration.use_persian_track_term(apps, None)

        family.refresh_from_db()
        product.refresh_from_db()
        self.assertEqual(family.name_fa, "ریل")
        self.assertEqual(product.name_fa, "ریل")
