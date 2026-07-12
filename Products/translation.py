from modeltranslation.translator import TranslationOptions, register
from .models import (
    Category,
    Application,
    Family,
    Product,
    Project,
)


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = (
        "name",
        "description",
        "meta_title",
        "meta_description",
    )


@register(Application)
class ApplicationTranslationOptions(TranslationOptions):
    fields = (
        "name",
        "cover_image_alt",
        "short_description",
        "description",
        "meta_title",
        "meta_description",
    )


@register(Family)
class FamilyTranslationOptions(TranslationOptions):
    fields = (
        "name",
        "subtitle",
        "meta_title",
        "meta_description",
    )


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = (
        "name",
        "subtitle",
        "description",
        "full_description",
        "meta_title",
        "meta_description",
        "image1_alt",
        "image2_alt",
        "image3_alt",
        "image4_alt",
    )


@register(Project)
class ProjectTranslationOptions(TranslationOptions):
    fields = (
        "name",
        "location",
        "project_type",
        "intro_heading",
        "intro_text",
        "overview_text",
        "about_content",
        "meta_title",
        "meta_description",
    )
