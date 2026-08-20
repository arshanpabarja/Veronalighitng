import json
import re
from pathlib import Path
from tempfile import TemporaryDirectory
from html import unescape
from io import StringIO

from django.core.management import call_command
from django.test import SimpleTestCase, TestCase
from django.utils.translation import override

from Products.models import Category

from .business_identity import BUSINESS_IDENTITY
from .editorial_content import (
    EDITORIAL_ARTICLES,
    build_editorial_links,
    render_article_body,
    validate_editorial_articles,
)
from .models import NewsArticle, NewsCategory
from .seo_monitoring import (
    build_search_console_report,
    classify_query,
    load_search_console_csv,
    normalize_page,
)
from .sitemaps import NewsSitemap
from .site_seo import SITE_SEO, validate_site_seo


class SiteSEOTests(TestCase):
    def test_reviewed_site_seo_is_complete_and_within_limits(self):
        validate_site_seo()
        self.assertEqual(len(SITE_SEO), 6)


class CatalogPageTests(TestCase):
    def test_catalog_page_is_bilingual_indexable_and_linked(self):
        for language, path, heading in (
            ("fa", "/catalogs/", "کاتالوگ‌های"),
            ("en", "/en/catalogs/", "Verona"),
        ):
            with self.subTest(language=language), override(language):
                response = self.client.get(path)
                html = response.content.decode()

                self.assertEqual(response.status_code, 200)
                self.assertContains(response, heading)
                self.assertEqual(html.count("<h1"), 1)
                self.assertEqual(html.count('rel="canonical"'), 1)
                self.assertContains(response, 'href="/catalogs/"' if language == "fa" else 'href="/en/catalogs/"')
                if language == "en":
                    self.assertContains(response, "Digital catalog")
                else:
                    self.assertContains(response, "کاتالوگ دیجیتال")
                self.assertContains(
                    response,
                    "/media/catalogs/verona-digital-catalog-2026.pdf",
                )
                self.assertContains(
                    response,
                    "/media/catalogs/verona-product-catalog-2026.pdf",
                )


class EditorialSEOClusterTests(TestCase):
    def setUp(self):
        self.sample_category = NewsCategory.objects.create(
            name="Sample",
            slug="sample",
        )
        self.sample = NewsArticle.objects.create(
            category=self.sample_category,
            title="Sample News Article 1",
            slug="sample-news-article-1",
            excerpt="Thin placeholder",
            body="<p>Thin placeholder</p>",
            cover_image="news/covers/sample.jpg",
            is_published=True,
        )
        linear = Category.objects.create(name="Linear", slug="linear")
        Category.objects.create(
            name="Recessed",
            slug="recessed",
            parent=linear,
        )
        Category.objects.create(
            name="Magnetic",
            slug="low-voltage-magneto",
        )

    @staticmethod
    def _article_schema(html):
        scripts = re.findall(
            r'<script type="application/ld\+json">\s*(.*?)\s*</script>',
            html,
            flags=re.DOTALL,
        )
        documents = [json.loads(unescape(script)) for script in scripts]
        return next(document for document in documents if document.get("@type") == "Article")

    def test_reviewed_articles_are_complete_and_non_cannibalizing(self):
        validate_editorial_articles()
        self.assertEqual(len(EDITORIAL_ARTICLES), 4)
        self.assertEqual(
            {
                article.cluster
                for article in EDITORIAL_ARTICLES.values()
            },
            {"recessed-linear", "magnetic-track"},
        )
        for article in EDITORIAL_ARTICLES.values():
            for content in article.translations.values():
                body = render_article_body(content)
                self.assertEqual(body.count("<h2>"), 5)
                self.assertGreaterEqual(body.count("<a href="), 2)

    def test_command_previews_then_replaces_published_sample_inventory(self):
        call_command("seed_seo_editorial_cluster", stdout=StringIO())
        self.sample.refresh_from_db()
        self.assertTrue(self.sample.is_published)
        self.assertEqual(
            NewsArticle.objects.filter(
                slug__in=EDITORIAL_ARTICLES
            ).count(),
            0,
        )

        call_command(
            "seed_seo_editorial_cluster",
            "--apply",
            stdout=StringIO(),
        )
        self.sample.refresh_from_db()
        self.assertFalse(self.sample.is_published)
        self.assertNotIn(self.sample, NewsSitemap().items())

        articles = NewsArticle.objects.filter(
            slug__in=EDITORIAL_ARTICLES,
            is_published=True,
        )
        self.assertEqual(articles.count(), 4)
        self.assertEqual(
            articles.filter(is_featured=True).count(),
            1,
        )
        self.assertTrue(
            all(article in NewsSitemap().items() for article in articles)
        )
        category = NewsCategory.objects.get(slug="guides")
        self.assertEqual(category.name_fa, "راهنمای طراحی و اجرا")
        self.assertEqual(
            category.name_en,
            "Design and Installation Guides",
        )

    def test_all_articles_render_translated_indexable_pages_and_links(self):
        call_command(
            "seed_seo_editorial_cluster",
            "--apply",
            stdout=StringIO(),
        )
        for slug, editorial in EDITORIAL_ARTICLES.items():
            article = NewsArticle.objects.get(slug=slug)
            for language in ("fa", "en"):
                with self.subTest(slug=slug, language=language), override(language):
                    response = self.client.get(article.get_absolute_url())
                    html = response.content.decode()
                    content = editorial.translations[language]

                    self.assertEqual(response.status_code, 200)
                    self.assertContains(response, content.title)
                    self.assertContains(response, content.meta_description)
                    self.assertEqual(html.count("<h1"), 1)
                    self.assertEqual(html.count("<title>"), 1)
                    self.assertEqual(html.count("<h2"), 6)
                    self.assertEqual(html.count('rel="canonical"'), 1)
                    self.assertEqual(html.count("hreflang="), 3)

                    schema = self._article_schema(html)
                    self.assertEqual(schema["inLanguage"], language)
                    self.assertEqual(
                        schema["author"]["@id"],
                        "http://testserver/#organization",
                    )
                    for section in content.sections:
                        for paragraph in section.paragraphs:
                            for target in re.findall(r"href='([^']+)'", paragraph):
                                self.assertRegex(
                                    html,
                                    rf"""href=["']{re.escape(target)}["']""",
                                )

    def test_primary_landing_pages_receive_two_editorial_links_each(self):
        for cluster in ("recessed-linear", "magnetic-track"):
            for language in ("fa", "en"):
                with self.subTest(cluster=cluster, language=language), override(language):
                    links = build_editorial_links(cluster, language)
                    self.assertEqual(len(links["links"]), 2)
                    self.assertTrue(
                        all(link["url"].startswith("/en/") for link in links["links"])
                        if language == "en"
                        else all(not link["url"].startswith("/en/") for link in links["links"])
                    )


class BusinessIdentitySEOTests(TestCase):
    @staticmethod
    def _schemas(html):
        scripts = re.findall(
            r'<script type="application/ld\+json">\s*(.*?)\s*</script>',
            html,
            flags=re.DOTALL,
        )
        return [json.loads(unescape(script)) for script in scripts]

    def test_pages_expose_one_consistent_business_entity(self):
        for language in ("fa", "en"):
            with self.subTest(language=language), override(language):
                for path in ("/", "/about/", "/story/", "/contact/"):
                    localized_path = f"/en{path}" if language == "en" else path
                    response = self.client.get(localized_path)
                    html = response.content.decode()
                    schemas = self._schemas(html)
                    entities = [
                        schema
                        for schema in schemas
                        if "Organization" in (
                            schema.get("@type")
                            if isinstance(schema.get("@type"), list)
                            else [schema.get("@type")]
                        )
                    ]

                    self.assertEqual(response.status_code, 200)
                    self.assertEqual(len(entities), 1)
                    entity = entities[0]
                    self.assertEqual(
                        entity["@id"],
                        "http://testserver/#organization",
                    )
                    self.assertEqual(
                        entity["telephone"],
                        BUSINESS_IDENTITY["telephone_e164"],
                    )
                    self.assertEqual(
                        entity["email"],
                        BUSINESS_IDENTITY["email"],
                    )
                    self.assertEqual(
                        entity["sameAs"],
                        [BUSINESS_IDENTITY["instagram"]],
                    )
                    self.assertEqual(
                        entity["address"]["addressCountry"],
                        "IR",
                    )

    def test_company_pages_reference_the_canonical_entity(self):
        expected_id = "http://testserver/#organization"
        for path, schema_type in (
            ("/about/", "AboutPage"),
            ("/story/", "AboutPage"),
            ("/contact/", "ContactPage"),
        ):
            response = self.client.get(path)
            schema = next(
                item
                for item in self._schemas(response.content.decode())
                if item.get("@type") == schema_type
            )
            self.assertEqual(schema["mainEntity"]["@id"], expected_id)

    def test_visible_primary_contact_details_use_canonical_values(self):
        response = self.client.get("/contact/")
        self.assertContains(response, BUSINESS_IDENTITY["email"])
        self.assertContains(
            response,
            f'tel:{BUSINESS_IDENTITY["telephone_e164"]}',
        )
        self.assertContains(response, BUSINESS_IDENTITY["street_address_fa"])
        self.assertContains(response, BUSINESS_IDENTITY["whatsapp"])


class SearchConsoleMonitoringTests(SimpleTestCase):
    queries_csv = (
        "Top queries,Clicks,Impressions,CTR,Position\n"
        "چراغ خطی توکار,2,100,2%,8.5\n"
        "ریل مگنتی,1,50,2%,4.5\n"
        "Verona Lighting,5,50,10%,1.0\n"
        "architectural lighting,0,20,0%,30.0\n"
    )
    pages_csv = (
        "Top pages,Clicks,Impressions,CTR,Position\n"
        "https://veronalighting.co/linear/c/recessed/,2,100,2%,8.5\n"
        "https://veronalighting.co/low-voltage-magneto/,1,50,2%,4.5\n"
    )

    def test_query_classification_and_page_normalization(self):
        self.assertEqual(classify_query("قیمت چراغ خطی توکار"), "recessed-linear")
        self.assertEqual(classify_query("خرید ريل مگنتي"), "magnetic-track")
        self.assertEqual(classify_query("VeronaLighting products"), "brand")
        self.assertEqual(
            normalize_page(
                "https://veronalighting.co/linear/c/recessed?utm_source=test"
            ),
            "/linear/c/recessed/",
        )

    def test_exports_generate_campaign_scorecard(self):
        with TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            queries = temp_path / "Queries.csv"
            pages = temp_path / "Pages.csv"
            queries.write_text(self.queries_csv, encoding="utf-8")
            pages.write_text(self.pages_csv, encoding="utf-8")

            query_rows = load_search_console_csv(
                queries,
                ("Top queries", "Query"),
            )
            page_rows = load_search_console_csv(
                pages,
                ("Top pages", "Page"),
            )
            report = build_search_console_report(
                query_rows,
                page_rows,
                "2026-07-27 to 2026-08-02",
            )

            self.assertIn("چراغ خطی توکار", report)
            self.assertIn("Ranking positions 6–20", report)
            self.assertIn("position 8.5", report)
            self.assertIn("https://veronalighting.co/linear/c/recessed/", report)
            self.assertIn("Absence from a Performance export", report)

    def test_management_command_writes_markdown_report(self):
        with TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            queries = temp_path / "Queries.csv"
            pages = temp_path / "Pages.csv"
            output = temp_path / "scorecard.md"
            queries.write_text(self.queries_csv, encoding="utf-8")
            pages.write_text(self.pages_csv, encoding="utf-8")

            call_command(
                "analyze_search_console",
                "--queries",
                str(queries),
                "--pages",
                str(pages),
                "--period",
                "2026-07-27 to 2026-08-02",
                "--output",
                str(output),
                stdout=StringIO(),
            )

            self.assertTrue(output.exists())
            self.assertIn("Campaign query clusters", output.read_text(encoding="utf-8"))
