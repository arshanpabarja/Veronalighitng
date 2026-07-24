import json
import re
from html import unescape
from django.test import TestCase
from django.core.management import call_command
from django.utils.translation import override
from io import StringIO

from .models import Application, Category, Family, Product
from .services.application_content import (
    APPLICATION_CONTENT,
    validate_application_content,
)
from .services.fa_seo import (
    build_category_fa_seo,
    build_full_description_fa,
    build_family_fa_seo,
    build_product_fa_seo,
    classify_keyword,
)
from .services.category_content import (
    CATEGORY_CONTENT,
    validate_category_content,
)


class PersianSEOServiceTests(TestCase):
    def test_reviewed_application_content_is_complete_and_unique(self):
        validate_application_content()
        self.assertEqual(len(APPLICATION_CONTENT), 7)
        self.assertEqual(
            len(
                {
                    content.meta_title_fa
                    for content in APPLICATION_CONTENT.values()
                }
            ),
            7,
        )
        self.assertEqual(
            len(
                {
                    content.meta_description_en
                    for content in APPLICATION_CONTENT.values()
                }
            ),
            7,
        )

    def test_application_rewrite_and_bilingual_page_seo(self):
        for position, slug in enumerate(APPLICATION_CONTENT, start=1):
            Application.objects.create(
                name="Placeholder",
                name_fa="Placeholder",
                name_en="Placeholder",
                slug=slug,
                sort_order=position,
                meta_title_fa="asdf" if slug == "office" else "",
                meta_title_en="asdf" if slug == "office" else "",
            )

        call_command("rewrite_application_content", stdout=StringIO())
        office = Application.objects.get(slug="office")
        self.assertEqual(office.meta_title_fa, "asdf")

        call_command(
            "rewrite_application_content",
            "--apply",
            stdout=StringIO(),
        )
        office.refresh_from_db()
        self.assertEqual(
            office.meta_title_fa,
            APPLICATION_CONTENT["office"].meta_title_fa,
        )
        self.assertEqual(
            office.meta_title_en,
            APPLICATION_CONTENT["office"].meta_title_en,
        )
        self.assertTrue(office.description_fa)
        self.assertTrue(office.description_en)

        fa_list = self.client.get("/applications/")
        self.assertEqual(fa_list.status_code, 200)
        self.assertContains(fa_list, "راهکارهای روشنایی بر اساس کاربرد")
        self.assertContains(
            fa_list,
            APPLICATION_CONTENT["office"].short_description_fa,
        )

        en_list = self.client.get("/en/applications/")
        self.assertEqual(en_list.status_code, 200)
        self.assertContains(en_list, "Architectural Lighting Applications")
        self.assertContains(
            en_list,
            APPLICATION_CONTENT["office"].short_description_en,
        )

        fa_detail = self.client.get("/applications/office/")
        self.assertEqual(fa_detail.status_code, 200)
        self.assertContains(
            fa_detail,
            f"<title>{APPLICATION_CONTENT['office'].meta_title_fa}</title>",
            html=True,
        )
        self.assertContains(
            fa_detail,
            APPLICATION_CONTENT["office"].description_fa.split("\n\n")[0],
        )

        en_detail = self.client.get("/en/applications/office/")
        self.assertEqual(en_detail.status_code, 200)
        self.assertContains(
            en_detail,
            f"<title>{APPLICATION_CONTENT['office'].meta_title_en}</title>",
            html=True,
        )
        self.assertContains(
            en_detail,
            APPLICATION_CONTENT["office"].description_en.split("\n\n")[0],
        )

        for response in (fa_list, en_list, fa_detail, en_detail):
            schema_blocks = re.findall(
                r'<script type="application/ld\+json">\s*(.*?)\s*</script>',
                response.content.decode(),
                flags=re.DOTALL,
            )
            schema_types = {
                json.loads(unescape(block)).get("@type")
                for block in schema_blocks
            }
            self.assertIn("BreadcrumbList", schema_types)
            self.assertIn("CollectionPage", schema_types)

    def test_catalog_pages_do_not_publish_ineligible_product_schema(self):
        category = Category.objects.create(
            name="Recessed",
            name_fa="چراغ توکار",
            name_en="Recessed",
            slug="schema-category",
        )
        family = Family.objects.create(
            name="TRITON",
            name_fa="TRITON",
            name_en="TRITON",
            slug="schema-family",
            category=category,
        )
        product = Product.objects.create(
            name="TRITON",
            name_fa="TRITON",
            name_en="TRITON",
            slug="schema-product",
            category=category,
            family=family,
            image1="products/test.jpg",
        )

        with override("fa"):
            fa_url = product.get_absolute_url()
        with override("en"):
            en_url = product.get_absolute_url()

        for url in (fa_url, en_url):
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, '"@type": "ItemPage"')
                self.assertContains(response, '"@type": "BreadcrumbList"')
                self.assertNotContains(response, '"@type": "Product"')
                schema_blocks = re.findall(
                    r'<script type="application/ld\+json">\s*(.*?)\s*</script>',
                    response.content.decode(),
                    flags=re.DOTALL,
                )
                schema_types = {
                    json.loads(unescape(block)).get("@type")
                    for block in schema_blocks
                }
                self.assertIn("ItemPage", schema_types)
                self.assertIn("BreadcrumbList", schema_types)
                self.assertNotIn("Product", schema_types)

    def test_reviewed_category_content_is_complete_and_unique(self):
        validate_category_content()
        self.assertEqual(len(CATEGORY_CONTENT), 23)
        self.assertEqual(
            len({item.description_fa for item in CATEGORY_CONTENT.values()}),
            23,
        )
        self.assertEqual(
            len({item.description_en for item in CATEGORY_CONTENT.values()}),
            23,
        )

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
