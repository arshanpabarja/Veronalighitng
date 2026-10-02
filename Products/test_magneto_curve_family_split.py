from importlib import import_module

from django.apps import apps
from django.test import TestCase

from Products.models import Application, Category, Family, Product


migration = import_module(
    "Products.migrations.0061_split_magneto_curve_product_families"
)


class MagnetoCurveFamilySplitTests(TestCase):
    def setUp(self):
        self.application = Application.objects.create(
            name="Retail",
            slug="retail",
        )
        self.category = Category.objects.create(
            name="Magneto Curve",
            slug=migration.CATEGORY_SLUG,
        )
        self.aggregate_family = Family.objects.create(
            name="Magneto Curve",
            slug=migration.AGGREGATE_FAMILY_SLUG,
            category=self.category,
        )
        self.aggregate_family.applications.add(self.application)
        self.products = [
            Product.objects.create(
                name=f"Curve product {index}",
                name_fa=f"محصول کرو {index}",
                name_en=f"Curve Product {index}",
                slug=f"curve-product-{index}",
                category=self.category,
                family=self.aggregate_family,
                image1=f"products/curve-{index}.png",
                order=index,
            )
            for index in range(1, 5)
        ]

    def test_creates_one_family_per_curve_product_in_product_order(self):
        migration.split_magneto_curve_product_families(apps, None)

        self.assertFalse(
            Family.objects.filter(slug=migration.AGGREGATE_FAMILY_SLUG).exists()
        )
        families = Family.objects.filter(category=self.category).order_by("number")
        self.assertEqual(families.count(), 4)
        self.assertEqual(
            list(families.values_list("number", flat=True)),
            [1, 2, 3, 4],
        )

        for product in self.products:
            product.refresh_from_db()
            self.assertEqual(
                product.family.slug,
                migration.product_family_slug(product.slug),
            )
            self.assertEqual(product.family.name_fa, product.name_fa)
            self.assertEqual(product.family.name_en, product.name_en)
            self.assertEqual(str(product.family.icon), str(product.image1))
            self.assertEqual(
                list(product.family.applications.values_list("slug", flat=True)),
                ["retail"],
            )
