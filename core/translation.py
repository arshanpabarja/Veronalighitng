from modeltranslation.translator import TranslationOptions, register
from .models import *
@register(SiteSettings)
class SiteSettingsTranslationOptions(TranslationOptions):
    fields = (
        "index_meta_title",
        "index_meta_description",
        "index_og_title",
        "index_og_description",
        "about_meta_title",
        "about_meta_description",
        "about_og_title",
        "about_og_description",
        "story_meta_title",
        "story_meta_description",
        "story_og_title",
        "story_og_description",
        "products_meta_title",
        "products_meta_description",
        "products_og_title",
        "products_og_description",
        "applications_meta_title",
        "applications_meta_description",
        "applications_og_title",
        "applications_og_description",
        "news_meta_title",
        "news_meta_description",
        "news_og_title",
        "news_og_description"
    )