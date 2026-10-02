from importlib import import_module

from django.apps import apps
from django.test import TestCase

from Products.models import Application, Category, Family, Product


migration = import_module(
    "Products.migrations.0055_organize_small_magneto_families"
)


class SmallMagnetoFamilyOrganizationTests(TestCase):
    def setUp(self):
        self.small_category = Category.objects.create(
            name="Magnet Small",
            slug=migration.SMALL_MAGNETO_CATEGORY_SLUG,
        )
        self.large_category = Category.objects.create(
            name="Magnet Large",
            slug="magent-large4cm-family",
        )
        self.application = Application.objects.create(
            name="Office",
            slug="office",
        )

        self.trim_family = Family.objects.create(
            name="Combined recessed tracks",
            slug=migration.RECESSED_TRIM_FAMILY_SLUG,
            category=self.small_category,
        )
        self.trim_family.applications.add(self.application)

        self.pendant_65_family = Family.objects.create(
            name="Small pendant 65",
            slug="magnetar-small-pendant-65",
            category=self.small_category,
        )
        self.pendant_65_family.applications.add(self.application)

        self.large_pendant_family = Family.objects.create(
            name="Large pendant 35",
            slug="magneto-pendant-35",
            category=self.large_category,
        )

        for slug in migration.ORDERED_FAMILY_SLUGS:
            if slug in {
                migration.RECESSED_TRIMLESS_FAMILY_SLUG,
                migration.RECESSED_TRIM_FAMILY_SLUG,
                migration.SMALL_PENDANT_35_FAMILY_SLUG,
                "magnetar-small-pendant-65",
            }:
                continue
            Family.objects.create(
                name=slug,
                slug=slug,
                category=self.small_category,
            )

        self.trimless_product = Product.objects.create(
            name="Small recessed trimless track",
            slug=migration.RECESSED_TRIMLESS_PRODUCT_SLUG,
            category=self.small_category,
            family=self.trim_family,
            image1="products/trimless.png",
        )
        self.trim_product = Product.objects.create(
            name="Small recessed trim track",
            slug=migration.RECESSED_TRIM_PRODUCT_SLUG,
            category=self.small_category,
            family=self.trim_family,
            image1="products/trim.png",
        )
        self.pendant_35_product = Product.objects.create(
            name="Small pendant 35",
            slug=migration.SMALL_PENDANT_35_PRODUCT_SLUG,
            category=self.small_category,
            family=self.large_pendant_family,
            image1="products/pendant-35.png",
        )

    def test_splits_tracks_repairs_small_pendant_and_orders_families(self):
        migration.organize_small_magneto_families(apps, None)

        self.trimless_product.refresh_from_db()
        self.trim_product.refresh_from_db()
        self.pendant_35_product.refresh_from_db()

        self.assertEqual(
            self.trimless_product.family.slug,
            migration.RECESSED_TRIMLESS_FAMILY_SLUG,
        )
        self.assertEqual(
            self.trim_product.family.slug,
            migration.RECESSED_TRIM_FAMILY_SLUG,
        )
        self.assertEqual(
            self.pendant_35_product.family.slug,
            migration.SMALL_PENDANT_35_FAMILY_SLUG,
        )

        trimless_family = self.trimless_product.family
        self.assertEqual(
            list(trimless_family.applications.values_list("slug", flat=True)),
            ["office"],
        )
        self.assertEqual(
            list(
                self.pendant_35_product.family.applications.values_list(
                    "slug", flat=True
                )
            ),
            ["office"],
        )

        actual_order = list(
            Family.objects.filter(
                category=self.small_category,
                slug__in=migration.ORDERED_FAMILY_SLUGS,
            )
            .order_by("number")
            .values_list("slug", flat=True)
        )
        self.assertEqual(actual_order, list(migration.ORDERED_FAMILY_SLUGS))
