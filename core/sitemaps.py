from django.contrib.sitemaps import Sitemap
from django.db.models import Q
from django.urls import reverse

from Products.models import (
    Category,
    Family,
    Product,
    Project,
    Application,
)
from .models import NewsArticle


class LocalizedSitemap(Sitemap):
    """Expose both Persian and English URLs with hreflang alternates."""

    i18n = True
    alternates = True
    x_default = True


class StaticViewSitemap(LocalizedSitemap):
    protocol = "https"
    priority = 1.0
    changefreq = "weekly"

    def items(self):
        return [
            "home",
            "about",
            "story",
            "services",
            "contact",
            "catalog",
            "news_list",
            "products:product_list",
            "products:project_list",
            "products:application_list",
        ]

    def location(self, item):
        return reverse(item)


class CategorySitemap(LocalizedSitemap):
    protocol = "https"
    priority = 0.9
    changefreq = "weekly"

    def items(self):
        return Category.objects.filter(is_active=True).filter(
            Q(parent__isnull=True) | Q(parent__is_active=True)
        )

    def lastmod(self, obj):
        return obj.updated_at


class FamilySitemap(LocalizedSitemap):
    protocol = "https"
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return Family.objects.filter(
            is_active=True,
            category__is_active=True,
        ).filter(
            Q(category__parent__isnull=True)
            | Q(category__parent__is_active=True)
        )


class ProductSitemap(LocalizedSitemap):
    protocol = "https"
    priority = 0.7
    changefreq = "weekly"

    def items(self):
        return Product.objects.filter(
            is_active=True,
            category__is_active=True,
            family__is_active=True,
        ).filter(
            Q(category__parent__isnull=True)
            | Q(category__parent__is_active=True)
        )

    def lastmod(self, obj):
        return obj.updated_at


class ProjectSitemap(LocalizedSitemap):
    protocol = "https"
    priority = 0.7
    changefreq = "monthly"

    def items(self):
        return Project.objects.filter(is_published=True)


class ApplicationSitemap(LocalizedSitemap):
    protocol = "https"
    priority = 0.7
    changefreq = "monthly"

    def items(self):
        return Application.objects.filter(is_active=True)



class NewsSitemap(LocalizedSitemap):
    protocol = "https"
    priority = 0.6
    changefreq = "daily"

    def items(self):
        return NewsArticle.objects.filter(is_published=True)
