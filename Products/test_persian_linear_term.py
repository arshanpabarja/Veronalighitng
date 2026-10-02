from importlib import import_module

from django.apps import apps
from django.test import TestCase

from Products.models import Family, Product


migration = import_module("Products.migrations.0067_use_persian_linear_term")


class PersianLinearTermMigrationTests(TestCase):
    def test_replaces_linear_transliteration_in_existing_names(self):
        family = Family.objects.create(
            name_en="Linear",
            name_fa="لاینر",
            slug="persian-linear-family",
        )
        product = Product.objects.create(
            name_en="Dot Linear",
            name_fa="دات لاینر",
            slug="persian-linear-product",
            family=family,
            image1="products/test.png",
        )

        migration.use_persian_linear_term(apps, None)

        family.refresh_from_db()
        product.refresh_from_db()
        self.assertEqual(family.name_fa, "خطی")
        self.assertEqual(product.name_fa, "دات خطی")
