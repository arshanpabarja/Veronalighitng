from importlib import import_module

from django.test import SimpleTestCase

from Products.services.catalog_application_images import (
    CATALOG_APPLICATION_PAGE_BY_SLUG,
    catalog_application_asset_name,
)


class CatalogApplicationImageMappingTests(SimpleTestCase):
    def test_catalog_mapping_uses_magneto_database_slugs(self):
        self.assertEqual(
            CATALOG_APPLICATION_PAGE_BY_SLUG["magnetar-large-linear"],
            18,
        )
        self.assertNotIn("magnetar-small-sign-emergency", CATALOG_APPLICATION_PAGE_BY_SLUG)

    def test_shared_product_variants_reuse_the_same_application_scene(self):
        self.assertEqual(
            CATALOG_APPLICATION_PAGE_BY_SLUG["md-mini-surface"],
            CATALOG_APPLICATION_PAGE_BY_SLUG["mirdamad-mini-pendant"],
        )
        self.assertEqual(
            CATALOG_APPLICATION_PAGE_BY_SLUG["ring-line-inside"],
            CATALOG_APPLICATION_PAGE_BY_SLUG["ring-line-inside-90cm"],
        )

    def test_asset_names_are_stable_media_relative_paths(self):
        self.assertEqual(
            catalog_application_asset_name(18),
            "products/catalog_applications/catalog_application_page_018.jpg",
        )

    def test_migration_contains_the_frozen_reviewed_mapping(self):
        catalog_migration = import_module(
            "Products.migrations.0052_assign_catalog_application_images"
        )
        track_migration = import_module(
            "Products.migrations.0053_assign_global_track_application_images"
        )
        self.assertEqual(
            {
                **catalog_migration.PRODUCT_PAGE_BY_SLUG,
                **track_migration.PRODUCT_PAGE_BY_SLUG,
            },
            CATALOG_APPLICATION_PAGE_BY_SLUG,
        )
