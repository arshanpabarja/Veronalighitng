from importlib import import_module

from django.apps import apps
from django.test import TestCase

from Products.models import Category, Family, Product


migration = import_module(
    "Products.migrations.0058_normalize_bd_lineo_product_names"
)


class BdLineoNameNormalizationTests(TestCase):
    def test_updates_only_the_two_bd_lineo_persian_names(self):
        category = Category.objects.create(name="Recessed", slug="recessed")
        family = Family.objects.create(
            name="BD LINEO",
            slug=migration.BD_LINEO_FAMILY_SLUG,
            category=category,
        )

        products = []
        for slug in migration.PRODUCT_NAMES_FA:
            products.append(
                Product.objects.create(
                    name="Legacy name",
                    name_fa="نام قدیمی",
                    name_en=slug,
                    slug=slug,
                    family=family,
                    image1=f"products/{slug}.png",
                    meta_title_fa="عنوان قدیمی",
                )
            )

        migration.normalize_bd_lineo_product_names(apps, None)

        for product in products:
            product.refresh_from_db()
            expected_name = migration.PRODUCT_NAMES_FA[product.slug]
            self.assertEqual(product.name, expected_name)
            self.assertEqual(product.name_fa, expected_name)
            self.assertEqual(
                product.meta_title_fa,
                f"{expected_name} | ورونا لایتینگ",
            )
