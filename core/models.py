from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField

from Products.models import Product

class SiteSettings(models.Model):
    # --- Index / Home ---
    index_meta_title = models.CharField(max_length=60, blank=True, verbose_name="Home Meta Title")
    index_meta_description = models.CharField(max_length=160, blank=True)
    index_og_image = models.ImageField(upload_to='seo/', blank=True)
    index_og_title = models.CharField(max_length=60, blank=True)
    index_og_description = models.CharField(max_length=160, blank=True)
    index_canonical_url = models.URLField(blank=True)

    # --- About ---
    about_meta_title = models.CharField(max_length=60, blank=True, verbose_name="About Meta Title")
    about_meta_description = models.CharField(max_length=160, blank=True)
    about_og_image = models.ImageField(upload_to='seo/', blank=True)
    about_og_title = models.CharField(max_length=60, blank=True)
    about_og_description = models.CharField(max_length=160, blank=True)
    about_canonical_url = models.URLField(blank=True)

    # --- Story ---
    story_meta_title = models.CharField(max_length=60, blank=True, verbose_name="Story Meta Title")
    story_meta_description = models.CharField(max_length=160, blank=True)
    story_og_image = models.ImageField(upload_to='seo/', blank=True)
    story_og_title = models.CharField(max_length=60, blank=True)
    story_og_description = models.CharField(max_length=160, blank=True)
    story_canonical_url = models.URLField(blank=True)

    # --- Products List ---
    products_meta_title = models.CharField(max_length=60, blank=True)
    products_meta_description = models.CharField(max_length=160, blank=True)
    products_og_image = models.ImageField(upload_to='seo/', blank=True)
    products_og_title = models.CharField(max_length=60, blank=True)
    products_og_description = models.CharField(max_length=160, blank=True)
    products_canonical_url = models.URLField(blank=True)

    # --- Applications List ---
    applications_meta_title = models.CharField(max_length=60, blank=True)
    applications_meta_description = models.CharField(max_length=160, blank=True)
    applications_og_image = models.ImageField(upload_to='seo/', blank=True)
    applications_og_title = models.CharField(max_length=60, blank=True)
    applications_og_description = models.CharField(max_length=160, blank=True)
    applications_canonical_url = models.URLField(blank=True)

    # --- News List ---
    news_meta_title = models.CharField(max_length=60, blank=True, verbose_name="News Meta Title")
    news_meta_description = models.CharField(max_length=160, blank=True, verbose_name="News Meta Description")
    news_og_image = models.ImageField(upload_to='seo/', blank=True, verbose_name="News OG Image")
    news_og_title = models.CharField(max_length=60, blank=True, verbose_name="News OG Title")
    news_og_description = models.CharField(max_length=160, blank=True, verbose_name="News OG Description")
    news_canonical_url = models.URLField(blank=True, verbose_name="News Canonical URL")

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return "Site SEO Settings"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class NewsCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    order = models.PositiveSmallIntegerField(default=0, help_text="Display order in the filter tabs")

    class Meta:
        verbose_name = "News Category"
        verbose_name_plural = "News Categories"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class NewsArticle(models.Model):
    category = models.ForeignKey(
        NewsCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="articles",
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    excerpt = models.TextField(max_length=300, help_text="Short summary shown on the list page")
    body = RichTextField()
    cover_image = models.ImageField(upload_to="news/covers/")
    read_time = models.PositiveSmallIntegerField(default=3, help_text="Estimated read time in minutes")
    is_featured = models.BooleanField(
        default=False,
        help_text="Show this article in the featured slot at the top of the list page",
    )
    is_published = models.BooleanField(default=False)
    published_at = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Per-article SEO
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    og_image = models.ImageField(upload_to="news/seo/", blank=True)

    class Meta:
        verbose_name = "News Article"
        verbose_name_plural = "News Articles"
        ordering = ["-published_at", "-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        # Enforce only one featured article at a time
        if self.is_featured:
            NewsArticle.objects.exclude(pk=self.pk).filter(is_featured=True).update(is_featured=False)
        super().save(*args, **kwargs)