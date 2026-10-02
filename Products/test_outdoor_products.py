from importlib import import_module

from django.apps import apps
from django.test import TestCase

from Products.models import Application, Category, Family, Product


migration = import_module(
    "Products.migrations.0064_add_outdoor_ney_qasedak_hami_products"
)


class OutdoorProductMigrationTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name_en="Outdoor", name_fa="چراغ فضای باز", slug="outdoor"
        )
        Application.objects.create(
            name_en="Landscape", name_fa="محوطه", slug="landescape"
        )

    def test_creates_three_families_and_all_seven_products(self):
        migration.add_outdoor_products(apps, None)
        self.assertEqual(
            set(Family.objects.filter(category=self.category).values_list("slug", flat=True)),
            {"ney", "qasedak", "hami"},
        )
        self.assertEqual(Product.objects.filter(category=self.category).count(), 7)
        self.assertEqual(Product.objects.get(slug="ney-signage").lumens, 400)
        self.assertEqual(Product.objects.get(slug="ney-fadak").lumens, 4500)
        self.assertEqual(Product.objects.get(slug="ney").variants.count(), 3)
        hami = Product.objects.get(slug="hami-wall-1")
        self.assertEqual(hami.lamp_base_type, "GU10")
        self.assertEqual(hami.wattage, 6)

    def test_rerun_is_idempotent_for_catalog_records(self):
        migration.add_outdoor_products(apps, None)
        migration.add_outdoor_products(apps, None)
        self.assertEqual(Family.objects.filter(category=self.category).count(), 3)
        self.assertEqual(Product.objects.filter(category=self.category).count(), 7)
        self.assertEqual(Product.objects.get(slug="ney").variants.count(), 3)
