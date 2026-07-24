import json
import re
from html import unescape
from django.test import TestCase
from django.core.management import call_command
from django.urls import reverse
from django.utils.translation import override
from io import StringIO

from core.sitemaps import FamilySitemap, ProductSitemap

from .models import Application, Category, Family, Product, Project
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
from .services.keyword_strategy import (
    KEYWORD_LANDING_PAGES,
    validate_keyword_strategy,
)
from .services.landing_page_content import (
    LANDING_PAGE_CONTENT,
    validate_landing_page_content,
)
from .services.priority_product_content import (
    PRIORITY_PRODUCT_CONTENT,
    validate_priority_product_content,
)
from .services.project_authority_content import (
    PROJECT_AUTHORITY_CONTENT,
    validate_project_authority_content,
)
from .services.seo_internal_links import (
    build_seo_cluster_links,
    cluster_key_for_category,
)


def assert_complete_breadcrumb_schema(testcase, response):
    schema_blocks = re.findall(
        r'<script type="application/ld\+json">\s*(.*?)\s*</script>',
        response.content.decode(),
        flags=re.DOTALL,
    )
    schemas = [json.loads(unescape(block)) for block in schema_blocks]
    breadcrumbs = [
        schema for schema in schemas if schema.get("@type") == "BreadcrumbList"
    ]
    testcase.assertEqual(len(breadcrumbs), 1)
    for item in breadcrumbs[0]["itemListElement"]:
        testcase.assertTrue(item.get("name"))
        testcase.assertRegex(item.get("item", ""), r"^https?://")


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
            assert_complete_breadcrumb_schema(self, response)

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
                assert_complete_breadcrumb_schema(self, response)

    def test_all_catalog_breadcrumbs_have_names_and_absolute_items(self):
        root = Category.objects.create(
            name="Linear",
            name_fa="Linear",
            name_en="Linear",
            slug="breadcrumb-linear",
        )
        child = Category.objects.create(
            name="Recessed",
            name_fa="Recessed",
            name_en="Recessed",
            slug="breadcrumb-recessed",
            parent=root,
        )
        family = Family.objects.create(
            name="Narrow",
            name_fa="Narrow",
            name_en="Narrow",
            slug="breadcrumb-narrow",
            category=child,
        )
        product = Product.objects.create(
            name="Narrow Product",
            name_fa="Narrow Product",
            name_en="Narrow Product",
            slug="breadcrumb-product",
            category=child,
            family=family,
            image1="products/test.jpg",
        )
        application = Application.objects.create(
            name="Office",
            name_fa="Office",
            name_en="Office",
            slug="breadcrumb-office",
        )
        project = Project.objects.create(
            name="Office Project",
            slug="breadcrumb-project",
            application=application,
            is_published=True,
        )

        paths = (
            reverse("products:product_list"),
            root.get_absolute_url(),
            child.get_absolute_url(),
            family.get_absolute_url(),
            product.get_absolute_url(),
            reverse("products:application_list"),
            application.get_absolute_url(),
            project.get_absolute_url(),
        )
        for path in paths:
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)
                assert_complete_breadcrumb_schema(self, response)

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


class TechnicalSEOPhaseOneTests(TestCase):
    def setUp(self):
        self.parent = Category.objects.create(
            name="Linear",
            name_fa="خطی",
            name_en="Linear",
            slug="linear-seo-test",
        )
        self.child = Category.objects.create(
            name="Recessed",
            name_fa="توکار",
            name_en="Recessed",
            slug="recessed-seo-test",
            parent=self.parent,
        )
        self.family = Family.objects.create(
            name="SEO FAMILY",
            name_fa="SEO FAMILY",
            name_en="SEO FAMILY",
            slug="seo-family-test",
            category=self.child,
        )
        self.product = Product.objects.create(
            name="SEO PRODUCT",
            name_fa="SEO PRODUCT",
            name_en="SEO PRODUCT",
            slug="seo-product-test",
            category=self.child,
            family=self.family,
            image1="products/test.jpg",
        )

    def test_product_page_has_reciprocal_language_alternates(self):
        with override("en"):
            url = self.product.get_absolute_url()

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            'hreflang="fa" href="http://testserver/linear-seo-test/c/'
            'recessed-seo-test/seo-family-test/seo-product-test/"',
        )
        self.assertContains(
            response,
            'hreflang="en" href="http://testserver/en/linear-seo-test/c/'
            'recessed-seo-test/seo-family-test/seo-product-test/"',
        )
        self.assertContains(
            response,
            'hreflang="x-default" href="http://testserver/linear-seo-test/c/'
            'recessed-seo-test/seo-family-test/seo-product-test/"',
        )

    def test_filter_parameters_are_noindex_and_not_canonicalized(self):
        with override("fa"):
            response = self.client.get(
                reverse("products:product_list"),
                {"application": "office", "utm_source": "test"},
            )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            '<link rel="canonical" href="http://testserver/products/">',
            html=True,
        )
        self.assertContains(
            response,
            '<meta name="robots" content="noindex, follow">',
            html=True,
        )
        self.assertNotContains(response, "utm_source")

    def test_mismatched_nested_product_path_redirects_to_canonical(self):
        with override("en"):
            canonical_url = self.product.get_absolute_url()
            wrong_url = reverse(
                "products:product_detail",
                kwargs={
                    "cat_slug": "wrong-parent",
                    "child_slug": "wrong-child",
                    "family_slug": "wrong-family",
                    "slug": self.product.slug,
                },
            )
            response = self.client.get(wrong_url)

        self.assertRedirects(
            response,
            canonical_url,
            status_code=301,
            fetch_redirect_response=False,
        )

    def test_nested_product_cannot_render_through_no_child_route(self):
        wrong_url = reverse(
            "products:product_detail_no_child",
            kwargs={
                "cat_slug": self.child.slug,
                "family_slug": self.family.slug,
                "slug": self.product.slug,
            },
        )

        self.assertEqual(self.client.get(wrong_url).status_code, 404)

    def test_sitemaps_exclude_items_below_inactive_taxonomy(self):
        inactive_parent = Category.objects.create(
            name="Inactive",
            slug="inactive-parent-seo-test",
            is_active=False,
        )
        active_child = Category.objects.create(
            name="Active Child",
            slug="active-child-seo-test",
            parent=inactive_parent,
            is_active=True,
        )
        excluded_family = Family.objects.create(
            name="Excluded Family",
            slug="excluded-family-seo-test",
            category=active_child,
            is_active=True,
        )
        excluded_product = Product.objects.create(
            name="Excluded Product",
            slug="excluded-product-seo-test",
            category=active_child,
            family=excluded_family,
            image1="products/test.jpg",
            is_active=True,
        )

        self.assertNotIn(excluded_family, FamilySitemap().items())
        self.assertNotIn(excluded_product, ProductSitemap().items())
        self.assertIn(self.family, FamilySitemap().items())
        self.assertIn(self.product, ProductSitemap().items())

    def test_sitemap_includes_valid_product_using_shared_family(self):
        sibling_child = Category.objects.create(
            name="Sibling System",
            slug="sibling-system-seo-test",
            parent=self.parent,
            is_active=True,
        )
        shared_family_product = Product.objects.create(
            name="Shared Family Product",
            slug="shared-family-product-seo-test",
            category=sibling_child,
            family=self.family,
            image1="products/test.jpg",
            is_active=True,
        )

        response = self.client.get(shared_family_product.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertIn(shared_family_product, ProductSitemap().items())


class KeywordLandingPageStrategyTests(TestCase):
    def setUp(self):
        self.linear = Category.objects.create(
            name="Linear",
            name_fa="چراغ خطی",
            name_en="Linear",
            slug="linear",
            meta_title_fa="چراغ خطی توکار، روکار و آویز",
        )
        self.recessed = Category.objects.create(
            name="Recessed",
            name_fa="توکار",
            name_en="Recessed",
            slug="recessed",
            parent=self.linear,
        )
        self.magnetic = Category.objects.create(
            name="Low Voltage Magneto",
            name_fa="چراغ مولتی ترک مگنتو",
            name_en="Low Voltage Magneto",
            slug="low-voltage-magneto",
        )

    def test_keyword_map_has_two_unique_primary_landing_pages(self):
        validate_keyword_strategy()
        self.assertEqual(len(KEYWORD_LANDING_PAGES), 2)
        self.assertEqual(
            {
                item.primary_keyword_fa
                for item in KEYWORD_LANDING_PAGES.values()
            },
            {"چراغ خطی توکار", "چراغ مگنتی"},
        )

    def test_command_preview_then_applies_keyword_ownership(self):
        call_command(
            "assign_keyword_landing_pages",
            stdout=StringIO(),
        )
        self.recessed.refresh_from_db()
        self.assertEqual(self.recessed.name_fa, "توکار")

        call_command(
            "assign_keyword_landing_pages",
            "--apply",
            stdout=StringIO(),
        )
        self.linear.refresh_from_db()
        self.recessed.refresh_from_db()
        self.magnetic.refresh_from_db()

        self.assertEqual(self.recessed.name_fa, "چراغ خطی توکار")
        self.assertEqual(
            self.recessed.meta_title_fa,
            "چراغ خطی توکار سقفی و بدون لبه | ورونا لایتینگ",
        )
        self.assertEqual(self.magnetic.name_fa, "چراغ مگنتی")
        self.assertEqual(
            self.magnetic.meta_title_fa,
            "چراغ مگنتی و ریل مگنتی | ورونا لایتینگ",
        )
        self.assertNotIn("چراغ خطی توکار", self.linear.meta_title_fa)

    def test_primary_pages_render_one_title_and_exact_keyword_h1(self):
        call_command(
            "assign_keyword_landing_pages",
            "--apply",
            stdout=StringIO(),
        )

        with override("fa"):
            recessed_url = self.recessed.get_absolute_url()
            magnetic_url = self.magnetic.get_absolute_url()

        for url, keyword, title in (
            (
                recessed_url,
                "چراغ خطی توکار",
                "چراغ خطی توکار سقفی و بدون لبه | ورونا لایتینگ",
            ),
            (
                magnetic_url,
                "چراغ مگنتی",
                "چراغ مگنتی و ریل مگنتی | ورونا لایتینگ",
            ),
        ):
            with self.subTest(url=url):
                response = self.client.get(url)
                html = response.content.decode()
                self.assertEqual(response.status_code, 200)
                self.assertEqual(html.count("<title>"), 1)
                self.assertContains(response, f"<title>{title}</title>", html=True)
                self.assertContains(response, keyword)
                self.assertContains(
                    response,
                    f'<link rel="canonical" href="http://testserver{url}">',
                    html=True,
                )


class SEOPrimaryLandingContentTests(TestCase):
    def setUp(self):
        self.linear = Category.objects.create(
            name="Linear",
            name_fa="چراغ خطی",
            name_en="Linear Lighting",
            slug="linear",
        )
        self.recessed = Category.objects.create(
            name="Recessed",
            name_fa="چراغ خطی توکار",
            name_en="Recessed Linear Lighting",
            slug="recessed",
            parent=self.linear,
        )
        self.magnetic = Category.objects.create(
            name="Magnetic",
            name_fa="چراغ مگنتی",
            name_en="Magnetic Track Lighting",
            slug="low-voltage-magneto",
        )
        self.other = Category.objects.create(
            name="Other",
            name_fa="سایر",
            name_en="Other",
            slug="other-seo-category",
        )

        Family.objects.create(
            name="SP LINEO",
            name_fa="SP LINEO",
            name_en="SP LINEO",
            slug="sp",
            category=self.recessed,
        )
        Family.objects.create(
            name="BD LINEO",
            name_fa="BD LINEO",
            name_en="BD LINEO",
            slug="BD",
            category=self.recessed,
        )

        magnetic_children = (
            ("Magnet Small", "magent-small-family"),
            ("Magnet Large", "magent-large4cm-family"),
            ("Magnet Curve", "magnet-curve"),
            ("Magnet Belt", "mmagne-tbelt"),
            ("Magnet Flexi", "magnet-flexi"),
        )
        for name, slug in magnetic_children:
            Category.objects.create(
                name=name,
                name_fa=name,
                name_en=name,
                slug=slug,
                parent=self.magnetic,
            )

    def _faq_schema(self, html):
        scripts = re.findall(
            r'<script type="application/ld\+json">\s*(.*?)\s*</script>',
            html,
            flags=re.DOTALL,
        )
        documents = [json.loads(unescape(script)) for script in scripts]
        return next(document for document in documents if document.get("@type") == "FAQPage")

    def test_reviewed_content_is_complete_in_both_languages(self):
        validate_landing_page_content()
        self.assertEqual(set(LANDING_PAGE_CONTENT), {"recessed-linear", "magnetic-track"})
        for translations in LANDING_PAGE_CONTENT.values():
            self.assertEqual(set(translations), {"fa", "en"})
            for content in translations.values():
                self.assertEqual(len(content.selection_items), 4)
                self.assertEqual(len(content.faqs), 4)

    def test_primary_pages_render_guides_links_and_valid_faq_schema(self):
        cases = (
            ("fa", self.recessed, "recessed-linear", 2),
            ("en", self.recessed, "recessed-linear", 2),
            ("fa", self.magnetic, "magnetic-track", 5),
            ("en", self.magnetic, "magnetic-track", 5),
        )

        for language, page, cluster, related_link_count in cases:
            with self.subTest(language=language, cluster=cluster), override(language):
                response = self.client.get(page.get_absolute_url())
                html = response.content.decode()
                content = LANDING_PAGE_CONTENT[cluster][language]

                self.assertEqual(response.status_code, 200)
                self.assertContains(response, content.heading)
                self.assertContains(response, content.primary_keyword)
                self.assertEqual(html.count("<details"), 4)
                self.assertGreaterEqual(html.count("<h2"), 4)
                self.assertEqual(
                    html.count('class="group border border-black/10 bg-white p-6'),
                    related_link_count + 2,
                )

                faq_schema = self._faq_schema(html)
                self.assertEqual(len(faq_schema["mainEntity"]), 4)
                self.assertTrue(
                    all(
                        entity["@type"] == "Question"
                        and entity["acceptedAnswer"]["@type"] == "Answer"
                        for entity in faq_schema["mainEntity"]
                    )
                )

    def test_guide_is_not_added_to_non_primary_categories(self):
        response = self.client.get(self.other.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'id="seo-guide-heading"')
        self.assertNotContains(response, '"@type": "FAQPage"')


class PriorityProductSEOTests(TestCase):
    def setUp(self):
        linear = Category.objects.create(name="Linear", slug="linear")
        recessed = Category.objects.create(
            name="Recessed",
            slug="recessed",
            parent=linear,
        )
        magnetic = Category.objects.create(
            name="Magnetic",
            slug="low-voltage-magneto",
        )
        small = Category.objects.create(
            name="Magnet Small",
            slug="magent-small-family",
            parent=magnetic,
        )
        large = Category.objects.create(
            name="Magnet Large",
            slug="magent-large4cm-family",
            parent=magnetic,
        )

        sp = Family.objects.create(name="SP", slug="sp", category=recessed)
        bd = Family.objects.create(name="BD", slug="BD", category=recessed)
        magnetic_linear = Family.objects.create(
            name="Magnet Linear",
            slug="magnet-linear",
            category=small,
        )

        product_data = (
            ("sp-narrow", recessed, sp),
            ("bd-narrow", recessed, bd),
            ("magnetar-small-linear", small, magnetic_linear),
            ("magnetar-large-linear", large, magnetic_linear),
        )
        self.products = {}
        for slug, category, family in product_data:
            self.products[slug] = Product.objects.create(
                name=f"Placeholder {slug}",
                name_fa=f"Placeholder {slug}",
                name_en=f"Placeholder {slug}",
                slug=slug,
                category=category,
                family=family,
                image1=f"products/{slug}.jpg",
            )

        self.other_product = Product.objects.create(
            name="Other Product",
            slug="other-priority-product",
            category=recessed,
            family=sp,
            image1="products/other.jpg",
        )

    @staticmethod
    def _faq_schema(html):
        scripts = re.findall(
            r'<script type="application/ld\+json">\s*(.*?)\s*</script>',
            html,
            flags=re.DOTALL,
        )
        documents = [json.loads(unescape(script)) for script in scripts]
        return next(document for document in documents if document.get("@type") == "FAQPage")

    def test_priority_product_content_is_complete_and_distinct(self):
        validate_priority_product_content()
        self.assertEqual(len(PRIORITY_PRODUCT_CONTENT), 4)
        for campaign in PRIORITY_PRODUCT_CONTENT.values():
            self.assertEqual(set(campaign.translations), {"fa", "en"})
            for content in campaign.translations.values():
                self.assertEqual(len(content.guide_items), 3)
                self.assertEqual(len(content.faqs), 4)

    def test_command_previews_then_applies_reviewed_bilingual_content(self):
        original_name = self.products["sp-narrow"].name_fa
        call_command("rewrite_priority_product_content", stdout=StringIO())
        self.products["sp-narrow"].refresh_from_db()
        self.assertEqual(self.products["sp-narrow"].name_fa, original_name)

        call_command(
            "rewrite_priority_product_content",
            "--apply",
            stdout=StringIO(),
        )
        for slug, product in self.products.items():
            product.refresh_from_db()
            campaign = PRIORITY_PRODUCT_CONTENT[slug]
            self.assertEqual(product.name_fa, campaign.translations["fa"].name)
            self.assertEqual(product.name_en, campaign.translations["en"].name)
            self.assertEqual(
                product.meta_title_fa,
                campaign.translations["fa"].meta_title,
            )
            self.assertEqual(
                product.meta_description_en,
                campaign.translations["en"].meta_description,
            )
            self.assertTrue(product.image1_alt_fa)
            self.assertTrue(product.image1_alt_en)

    def test_priority_pages_render_product_guides_links_and_faq_schema(self):
        call_command(
            "rewrite_priority_product_content",
            "--apply",
            stdout=StringIO(),
        )
        for slug, product in self.products.items():
            for language in ("fa", "en"):
                with self.subTest(slug=slug, language=language), override(language):
                    product.refresh_from_db()
                    response = self.client.get(product.get_absolute_url())
                    html = response.content.decode()
                    content = PRIORITY_PRODUCT_CONTENT[slug].translations[language]

                    self.assertEqual(response.status_code, 200)
                    self.assertContains(response, content.guide_heading)
                    self.assertContains(response, content.keyword)
                    self.assertEqual(html.count('id="priority-product-guide"'), 1)
                    self.assertEqual(html.count("<details"), 4)
                    self.assertEqual(html.count("<h1"), 1)
                    self.assertEqual(html.count("<title>"), 1)
                    self.assertEqual(
                        len(self._faq_schema(html)["mainEntity"]),
                        4,
                    )

    def test_non_priority_product_does_not_render_campaign_content(self):
        response = self.client.get(self.other_product.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'id="priority-product-guide"')


class SEOClusterInternalLinkTests(TestCase):
    def setUp(self):
        self.linear = Category.objects.create(name="Linear", slug="linear")
        self.recessed = Category.objects.create(
            name="Recessed",
            slug="recessed",
            parent=self.linear,
        )
        self.magnetic = Category.objects.create(
            name="Magnetic",
            slug="low-voltage-magneto",
        )
        self.magnetic_small = Category.objects.create(
            name="Magnet Small",
            slug="magent-small-family",
            parent=self.magnetic,
        )
        self.other_category = Category.objects.create(
            name="Other",
            slug="other-cluster-category",
        )

        self.recessed_family = Family.objects.create(
            name="Recessed Family",
            slug="recessed-cluster-family",
            category=self.recessed,
        )
        self.magnetic_family = Family.objects.create(
            name="Magnetic Family",
            slug="magnetic-cluster-family",
            category=self.magnetic_small,
        )
        self.other_family = Family.objects.create(
            name="Other Family",
            slug="other-cluster-family",
            category=self.other_category,
        )

        self.recessed_product = Product.objects.create(
            name="Recessed Product",
            slug="recessed-cluster-product",
            category=self.recessed,
            family=self.recessed_family,
            image1="products/recessed-cluster.jpg",
        )
        self.magnetic_product = Product.objects.create(
            name="Magnetic Product",
            slug="magnetic-cluster-product",
            category=self.magnetic_small,
            family=self.magnetic_family,
            image1="products/magnetic-cluster.jpg",
        )
        self.other_product = Product.objects.create(
            name="Other Product",
            slug="other-cluster-product",
            category=self.other_category,
            family=self.other_family,
            image1="products/other-cluster.jpg",
        )

        self.application = Application.objects.create(
            name="Mixed Application",
            slug="mixed-cluster-application",
        )
        self.application.families.add(
            self.recessed_family,
            self.magnetic_family,
        )

        self.project = Project.objects.create(
            name="Mixed Project",
            slug="mixed-cluster-project",
            is_published=True,
        )
        self.project.products.add(
            self.recessed_product,
            self.magnetic_product,
        )

    def test_category_classification_and_bilingual_anchor_content(self):
        self.assertEqual(
            cluster_key_for_category(self.recessed),
            "recessed-linear",
        )
        self.assertEqual(
            cluster_key_for_category(self.magnetic_small),
            "magnetic-track",
        )
        self.assertIsNone(cluster_key_for_category(self.other_category))

        links = build_seo_cluster_links(
            [self.recessed, self.magnetic_small, self.recessed],
            "fa",
        )
        self.assertEqual(len(links["links"]), 2)
        self.assertEqual(
            [link["key"] for link in links["links"]],
            ["recessed-linear", "magnetic-track"],
        )
        self.assertIn("چراغ خطی توکار", links["links"][0]["label"])
        self.assertIn("چراغ مگنتی", links["links"][1]["label"])

    def test_relevant_family_and_non_priority_product_link_upward(self):
        with override("fa"):
            family_response = self.client.get(
                self.recessed_family.get_absolute_url()
            )
            product_response = self.client.get(
                self.magnetic_product.get_absolute_url()
            )

        self.assertEqual(family_response.status_code, 200)
        self.assertContains(
            family_response,
            'href="/linear/c/recessed/"',
        )
        self.assertContains(
            family_response,
            "راهنمای انتخاب چراغ خطی توکار",
        )

        self.assertEqual(product_response.status_code, 200)
        self.assertContains(
            product_response,
            'href="/low-voltage-magneto/"',
        )
        self.assertContains(
            product_response,
            "راهنمای انتخاب چراغ مگنتی و ریل مگنتی",
        )

    def test_application_and_project_link_to_both_relevant_clusters(self):
        for page in (self.application, self.project):
            with self.subTest(page=page), override("fa"):
                response = self.client.get(page.get_absolute_url())
                self.assertEqual(response.status_code, 200)
                self.assertContains(
                    response,
                    'href="/linear/c/recessed/"',
                )
                self.assertContains(
                    response,
                    'href="/low-voltage-magneto/"',
                )
                self.assertEqual(
                    response.content.decode().count(
                        'id="seo-cluster-links-heading"'
                    ),
                    1,
                )

    def test_unrelated_pages_do_not_receive_cluster_links(self):
        for page in (self.other_family, self.other_product):
            with self.subTest(page=page):
                response = self.client.get(page.get_absolute_url())
                self.assertEqual(response.status_code, 200)
                self.assertNotContains(
                    response,
                    'id="seo-cluster-links-heading"',
                )


class AuthorityProjectSEOTests(TestCase):
    def setUp(self):
        for slug, english_name in (
            ("private-villa", "Private Villa"),
            ("diamond-boutique", "Diamond Boutique"),
        ):
            project = Project.objects.create(
                name=english_name,
                slug=slug,
                completion_year="2026",
                is_published=True,
            )
            project.name_en = english_name
            project.name_fa = ""
            project.save(update_fields=("name_en", "name_fa"))

    def test_authority_project_content_is_reviewed(self):
        validate_project_authority_content()
        self.assertEqual(
            set(PROJECT_AUTHORITY_CONTENT),
            {"private-villa", "diamond-boutique"},
        )

    def test_command_previews_then_applies_bilingual_project_content(self):
        output = StringIO()
        call_command("prepare_authority_projects", stdout=output)
        self.assertIn("PREVIEW MODE", output.getvalue())
        self.assertFalse(Project.objects.get(slug="private-villa").name_fa)

        call_command(
            "prepare_authority_projects",
            "--apply",
            stdout=StringIO(),
        )

        for slug, content in PROJECT_AUTHORITY_CONTENT.items():
            project = Project.objects.get(slug=slug)
            self.assertEqual(project.name_fa, content.name_fa)
            self.assertEqual(project.meta_title_fa, content.meta_title_fa)
            self.assertEqual(project.meta_description_en, content.meta_description_en)

    def test_prepared_projects_render_unique_fa_and_en_seo(self):
        call_command(
            "prepare_authority_projects",
            "--apply",
            stdout=StringIO(),
        )
        for slug, content in PROJECT_AUTHORITY_CONTENT.items():
            project = Project.objects.get(slug=slug)
            for language in ("fa", "en"):
                with self.subTest(slug=slug, language=language), override(language):
                    response = self.client.get(project.get_absolute_url())
                    html = response.content.decode()
                    expected_title = getattr(content, f"meta_title_{language}")
                    expected_description = getattr(
                        content,
                        f"meta_description_{language}",
                    )

                    self.assertEqual(response.status_code, 200)
                    self.assertContains(response, expected_title)
                    self.assertContains(response, expected_description)
                    self.assertEqual(html.count("<h1"), 1)
                    self.assertEqual(html.count('rel="canonical"'), 1)
