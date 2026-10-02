from importlib import import_module

from django.apps import apps
from django.test import TestCase

from Products.models import Application, Category, Family, Product


migration = import_module(
    "Products.migrations.0056_split_belt_and_flexi_product_families"
)


class BeltAndFlexiFamilySplitTests(TestCase):
    def setUp(self):
        self.application = Application.objects.create(
            name="Retail",
            slug="retail",
        )
        self.products_by_category = {}

        for category_slug, family_slug in migration.CATEGORY_FAMILY_PAIRS:
            category = Category.objects.create(
                name=category_slug,
                slug=category_slug,
            )
            aggregate_family = Family.objects.create(
                name=family_slug,
                slug=family_slug,
                category=category,
            )
            aggregate_family.applications.add(self.application)

            products = []
            for index in range(1, 3):
                product = Product.objects.create(
                    name=f"{category_slug} product {index}",
                    name_fa=f"محصول {index}",
                    name_en=f"Product {index}",
                    slug=f"{category_slug}-product-{index}",
                    category=category,
                    family=aggregate_family,
                    image1=f"products/{category_slug}-{index}.png",
                    subtitle_fa=f"زیرعنوان {index}",
                    subtitle_en=f"Subtitle {index}",
                    meta_title_fa=f"عنوان {index}",
                    meta_title_en=f"Title {index}",
                )
                products.append(product)
            self.products_by_category[category_slug] = products

    def test_creates_one_family_per_product_then_removes_aggregate_families(self):
        migration.split_belt_and_flexi_families(apps, None)

        for category_slug, aggregate_slug in migration.CATEGORY_FAMILY_PAIRS:
            self.assertFalse(Family.objects.filter(slug=aggregate_slug).exists())

            products = self.products_by_category[category_slug]
            category = Category.objects.get(slug=category_slug)
            families = Family.objects.filter(category=category).order_by("number")

            self.assertEqual(families.count(), len(products))
            self.assertEqual(
                list(families.values_list("number", flat=True)),
                [1, 2],
            )

            family_ids = set()
            for product in products:
                product.refresh_from_db()
                family_ids.add(product.family_id)
                self.assertEqual(
                    product.family.slug,
                    migration.product_family_slug(product.slug),
                )
                self.assertEqual(product.family.name_fa, product.name_fa)
                self.assertEqual(product.family.name_en, product.name_en)
                self.assertEqual(str(product.family.icon), str(product.image1))
                self.assertEqual(
                    list(
                        product.family.applications.values_list(
                            "slug", flat=True
                        )
                    ),
                    ["retail"],
                )

            self.assertEqual(len(family_ids), len(products))
