from importlib import import_module

from django.apps import apps
from django.test import TestCase

from Products.models import Application, Category, Family, Product


migration = import_module(
    "Products.migrations.0063_add_waterproof_lei_lina_products"
)


class WaterproofProductMigrationTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name_en="Spotlights & Underwater",
            name_fa="چراغ ضد آب",
            slug="spotlights-underwater",
        )
        Application.objects.create(
            name_en="Landscape",
            name_fa="محوطه",
            slug="landescape",
        )

    def test_creates_two_families_and_all_six_products(self):
        migration.add_waterproof_products(apps, None)

        self.assertEqual(
            set(
                Family.objects.filter(category=self.category).values_list(
                    "slug", flat=True
                )
            ),
            {"lei", "lina"},
        )
        self.assertEqual(
            set(
                Product.objects.filter(category=self.category).values_list(
                    "slug", flat=True
                )
            ),
            {
                "lei-mid-fl-tl",
                "lei-mid-up-t",
                "lei-mini-fl-tl",
                "lei-mini-win",
                "lina-onefold",
                "lina-offiance",
            },
        )

        mid = Product.objects.get(slug="lei-mid-fl-tl")
        self.assertEqual(mid.name_fa, "لی مید اف‌ال-تی‌ال")
        self.assertEqual(mid.wattage, 9)
        self.assertEqual(mid.family.slug, "lei")
        self.assertEqual(mid.variants.count(), 1)
        self.assertIn("Ø10 × 5 cm", mid.variants.get().dimension.label)

        lina = Product.objects.get(slug="lina-offiance")
        self.assertEqual(lina.wattage, 30)
        self.assertEqual(lina.family.slug, "lina")
        self.assertIn("RGBW", lina.description_en)
        self.assertIn("DMX", lina.description_fa)

    def test_rerun_is_idempotent_for_catalog_records(self):
        migration.add_waterproof_products(apps, None)
        migration.add_waterproof_products(apps, None)

        self.assertEqual(Family.objects.filter(category=self.category).count(), 2)
        self.assertEqual(Product.objects.filter(category=self.category).count(), 6)
        self.assertTrue(
            all(product.variants.count() == 1 for product in Product.objects.all())
        )
