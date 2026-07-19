from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from Products.models import (
    Category,
    Family,
    Product,
    Project,
    Application,
)
from .models import NewsArticle


class StaticViewSitemap(Sitemap):
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
            "news_list",
            "products:product_list",
            "products:project_list",
            "products:application_list",
        ]

    def location(self, item):
        return reverse(item)


class CategorySitemap(Sitemap):
    protocol = "https"
    priority = 0.9
    changefreq = "weekly"

    def items(self):
        return Category.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at


class FamilySitemap(Sitemap):
    protocol = "https"
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return Family.objects.filter(is_active=True)


class ProductSitemap(Sitemap):
    protocol = "https"
    priority = 0.7
    changefreq = "weekly"

    def items(self):
        return Product.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at


class ProjectSitemap(Sitemap):
    protocol = "https"
    priority = 0.7
    changefreq = "monthly"

    def items(self):
        return Project.objects.filter(is_published=True)


class ApplicationSitemap(Sitemap):
    protocol = "https"
    priority = 0.7
    changefreq = "monthly"

    def items(self):
        return Application.objects.filter(is_active=True)



class NewsSitemap(Sitemap):
    protocol = "https"
    priority = 0.6
    changefreq = "daily"

    def items(self):
        return NewsArticle.objects.filter(is_published=True)