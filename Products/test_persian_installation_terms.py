from importlib import import_module

from django.apps import apps
from django.test import TestCase

from Products.models import Family, Product


migration = import_module(
    "Products.migrations.0065_use_persian_installation_terms"
)


class PersianInstallationTermMigrationTests(TestCase):
    def test_replaces_awkward_transliterations_in_existing_names(self):
        family = Family.objects.create(
            name_en="Gypsum Recessed",
            name_fa="جیپسوم ریسسد",
            slug="persian-installation-family",
        )
        product = Product.objects.create(
            name_en="Surface & Pendant",
            name_fa="سرفیس و پندنت",
            slug="persian-installation-product",
            family=family,
            image1="products/test.png",
        )

        migration.use_persian_installation_terms(apps, None)

        family.refresh_from_db()
        product.refresh_from_db()
        self.assertEqual(family.name_fa, "گچی توکار")
        self.assertEqual(product.name_fa, "روکار و آویز")
