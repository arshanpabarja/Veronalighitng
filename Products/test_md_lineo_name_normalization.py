from importlib import import_module

from django.apps import apps
from django.test import TestCase

from Products.models import Category, Family, Product


migration = import_module(
    "Products.migrations.0059_normalize_md_lineo_product_names"
)


class MdLineoNameNormalizationTests(TestCase):
    def test_updates_four_models_in_both_md_lineo_families(self):
        products = []
        category = Category.objects.create(name="Linear", slug="linear-test")
        families = {
            slug: Family.objects.create(
                name=slug,
                slug=slug,
                category=category,
            )
            for slug in migration.MD_LINEO_FAMILY_SLUGS
        }

        for slug in migration.PRODUCT_NAMES_FA:
            family_slug = (
                "md-lineo-pendant"
                if slug.endswith("-pendant")
                else "md-lineo-surface"
            )
            products.append(
                Product.objects.create(
                    name="Legacy name",
                    name_fa="نام قدیمی",
                    name_en=slug,
                    slug=slug,
                    family=families[family_slug],
                    image1=f"products/{slug}.png",
                )
            )

        old_product = Product.objects.create(
            name="MD OLD",
            name_fa="MD OLD",
            slug="mad-old",
            family=families["md-lineo-surface"],
            image1="products/md-old.png",
        )

        migration.normalize_md_lineo_product_names(apps, None)

        for product in products:
            product.refresh_from_db()
            expected_name = migration.PRODUCT_NAMES_FA[product.slug]
            self.assertEqual(product.name, expected_name)
            self.assertEqual(product.name_fa, expected_name)
            self.assertEqual(
                product.meta_title_fa,
                f"{expected_name} | ورونا لایتینگ",
            )

        old_product.refresh_from_db()
        self.assertEqual(old_product.name_fa, "MD OLD")
