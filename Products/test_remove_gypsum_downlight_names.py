from importlib import import_module

from django.apps import apps
from django.test import TestCase

from Products.models import Family, Product


migration = import_module(
    "Products.migrations.0069_remove_downlight_from_gypsum_product_names"
)


class RemoveGypsumDownlightNamesMigrationTests(TestCase):
    def test_removes_downlight_from_gypsum_products_only(self):
        gypsum = Family.objects.create(
            name_en="Gypsum",
            name_fa="گچی",
            slug="gypsum",
        )
        other = Family.objects.create(
            name_en="Recessed",
            name_fa="توکار",
            slug="other-family",
        )
        gypsum_product = Product.objects.create(
            name_en="Virgo Downlight",
            name_fa="ویرگو دان‌لایت",
            slug="gypsum-product",
            family=gypsum,
            image1="products/test.png",
        )
        other_product = Product.objects.create(
            name_en="Spy Downlight",
            name_fa="اسپای دان‌لایت",
            slug="other-product",
            family=other,
            image1="products/test.png",
        )

        migration.remove_downlight_from_gypsum_product_names(apps, None)

        gypsum_product.refresh_from_db()
        other_product.refresh_from_db()
        self.assertEqual(gypsum_product.name_fa, "ویرگو")
        self.assertEqual(other_product.name_fa, "اسپای دان‌لایت")
