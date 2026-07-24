from datetime import date

from django.core.management.base import BaseCommand
from django.db import transaction

from core.editorial_content import (
    EDITORIAL_ARTICLES,
    render_article_body,
    validate_editorial_articles,
)
from core.models import NewsArticle, NewsCategory


class Command(BaseCommand):
    help = (
        "Preview or publish the reviewed bilingual Step 6 editorial cluster "
        "and unpublish thin sample articles."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--apply",
            action="store_true",
            help="Write changes. Without this flag, the command is read-only.",
        )

    def handle(self, *args, **options):
        validate_editorial_articles()
        apply_changes = options["apply"]
        sample_articles = NewsArticle.objects.filter(
            slug__startswith="sample-news-article-",
            is_published=True,
        )
        sample_count = sample_articles.count()
        existing_slugs = set(
            NewsArticle.objects.filter(
                slug__in=EDITORIAL_ARTICLES
            ).values_list("slug", flat=True)
        )

        self.stdout.write(
            self.style.WARNING(
                "APPLY MODE" if apply_changes else "PREVIEW MODE (no database changes)"
            )
        )
        self.stdout.write(
            f"Thin published sample articles to unpublish: {sample_count}"
        )
        for slug in EDITORIAL_ARTICLES:
            action = "update" if slug in existing_slugs else "create"
            self.stdout.write(f"[{action.upper()}] {slug}")

        if apply_changes:
            with transaction.atomic():
                sample_articles.update(
                    is_published=False,
                    is_featured=False,
                )
                category, _ = NewsCategory.objects.get_or_create(
                    slug="guides",
                    defaults={"name": "راهنمای طراحی و اجرا"},
                )
                category.name_fa = "راهنمای طراحی و اجرا"
                category.name_en = "Design and Installation Guides"
                category.order = 1
                category.save(
                    update_fields=["name_fa", "name_en", "order"]
                )

                for slug, article in EDITORIAL_ARTICLES.items():
                    fa = article.translations["fa"]
                    en = article.translations["en"]
                    values = {
                        "category": category,
                        "title": fa.title,
                        "title_fa": fa.title,
                        "title_en": en.title,
                        "excerpt": fa.excerpt,
                        "excerpt_fa": fa.excerpt,
                        "excerpt_en": en.excerpt,
                        "body": render_article_body(fa),
                        "body_fa": render_article_body(fa),
                        "body_en": render_article_body(en),
                        "cover_image": article.cover_image,
                        "read_time": article.read_time,
                        "is_featured": slug == "what-is-magnetic-track-lighting",
                        "is_published": True,
                        "published_at": date.fromisoformat(article.published_at),
                        "meta_title": fa.meta_title,
                        "meta_title_fa": fa.meta_title,
                        "meta_title_en": en.meta_title,
                        "meta_description": fa.meta_description,
                        "meta_description_fa": fa.meta_description,
                        "meta_description_en": en.meta_description,
                    }
                    NewsArticle.objects.update_or_create(
                        slug=slug,
                        defaults=values,
                    )

        action = "Published" if apply_changes else "Would publish"
        self.stdout.write(
            self.style.SUCCESS(
                f"{action} {len(EDITORIAL_ARTICLES)} bilingual guides and "
                f"{'unpublished' if apply_changes else 'would unpublish'} "
                f"{sample_count} thin sample articles."
            )
        )
