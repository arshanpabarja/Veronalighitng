from django.test import TestCase
from django.core.management import call_command
from io import StringIO

from .models import Category, Family, Product
from .services.fa_seo import (
    build_category_fa_seo,
    build_full_description_fa,
    build_family_fa_seo,
    build_product_fa_seo,
    classify_keyword,
)


class PersianSEOServiceTests(TestCase):
    def test_magnetic_track_uses_recessed_keyword(self):
        cluster, keyword, priority = classify_keyword(
            {
                "name_en": "MAGNETO LARGE RECESSED TRACK TRIMLESS",
                "name_fa": "ریل توکار بدون قاب MAGNETO LARGE",
            }
        )
        self.assertEqual(cluster, "magnetic-track-recessed")
        self.assertEqual(keyword, "ریل مگنتی توکار")
        self.assertEqual(priority, 1)

    def test_sp_family_maps_to_recessed_linear(self):
        result = build_product_fa_seo(
            {
                "name_en": "SP NARROW",
                "name_fa": "SP NARROW",
                "subtitle_en": "recessed mount back light LED trim linear",
                "wattage": 20,
                "lumens": 2000,
            }
        )
        self.assertEqual(result.keyword, "چراغ خطی توکار")
        self.assertLessEqual(len(result.meta_title), 65)
        self.assertLessEqual(len(result.meta_description), 160)
        self.assertIn("۲۰", result.meta_description.replace("20", "۲۰"))

    def test_downlight_and_other_catalogue_groups_are_not_ignored(self):
        result = build_product_fa_seo(
            {
                "name_en": "Virgo Gypsum Downlight",
                "name_fa": "Virgo",
                "description_fa": "دان‌لایت گچی معماری",
            }
        )
        self.assertEqual(result.keyword, "چراغ گچی توکار")
        self.assertEqual(result.priority, 2)

    def test_panel_category_wins_over_an_incorrect_magnetic_family(self):
        result = build_product_fa_seo(
            {
                "name_en": "BAHAR SINGLE",
                "name_fa": "BAHAR SINGLE",
                "category_en": "Panel",
                "category_fa": "پنل",
                "category_slug": "panel",
                "family_en": "MAGNETO SMALL SPOT 35",
                "family_fa": "MAGNETO SMALL SPOT 35",
            }
        )
        self.assertEqual(result.keyword, "چراغ پنل LED")

    def test_family_and_category_metadata_stay_within_limits(self):
        family = build_family_fa_seo(
            {
                "name_en": "MAGNETO SPOT",
                "name_fa": "MAGNETO SPOT",
                "category_fa": "مگنت لارج",
            }
        )
        category = build_category_fa_seo(
            {
                "name_en": "Recessed",
                "name_fa": "چراغ توکار",
                "category_fa": "چراغ توکار",
                "slug": "recessed",
            }
        )
        self.assertEqual(category.keyword, "چراغ خطی توکار")
        self.assertIn("MAGNETO SPOT", family.meta_title)
        self.assertEqual(
            category.meta_title,
            "چراغ خطی توکار | ورونا لایتینگ",
        )
        self.assertLessEqual(len(family.meta_title), 65)
        self.assertLessEqual(len(family.meta_description), 160)
        self.assertLessEqual(len(category.meta_title), 65)
        self.assertLessEqual(len(category.meta_description), 160)

    def test_full_description_preserves_existing_copy_and_adds_guidance(self):
        existing = "متن موجود و تأییدشده محصول."
        improved = build_full_description_fa(
            {
                "name_en": "SP NARROW",
                "name_fa": "SP NARROW",
                "subtitle_en": "recessed linear light",
                "category_fa": "توکار",
                "family_fa": "اس‌پی لاینئو",
                "wattage": 20,
                "lumens": 2000,
            },
            existing,
        )
        self.assertTrue(improved.startswith(existing))
        self.assertIn("توان 20 وات", improved)
        self.assertIn("سایر مدل‌های مرتبط", improved)
        self.assertGreater(len(improved), 500)

    def test_command_preview_does_not_write(self):
        category = Category.objects.create(
            name="مگنت",
            name_fa="مگنت",
            name_en="Magnetic",
            slug="magnetic",
        )
        family = Family.objects.create(
            name="MAGNETO",
            name_fa="MAGNETO",
            name_en="MAGNETO",
            slug="magneto",
            category=category,
        )
        product = Product.objects.create(
            name="MAGNETO LINEAR",
            name_fa="MAGNETO LINEAR",
            name_en="MAGNETO LINEAR",
            slug="magneto-linear-test",
            category=category,
            family=family,
            image1="products/test.jpg",
        )

        call_command("optimize_fa_catalog_seo", stdout=StringIO())
        product.refresh_from_db()
        self.assertFalse(product.meta_title_fa)

        call_command("optimize_fa_catalog_seo", "--apply", stdout=StringIO())
        product.refresh_from_db()
        self.assertIn("چراغ خطی مگنتی", product.meta_title_fa)
        self.assertTrue(product.meta_description_fa)
        self.assertTrue(product.image1_alt_fa)
