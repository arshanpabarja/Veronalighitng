# context_processors.py
from .models import Category, Application
from django.utils.translation import activate
from django.urls import translate_url


def navbar_categories(request):
    """
    این context processor در تمام تمپلیت‌ها
    متغیر categories را در دسترس قرار می‌دهد
    """
    categories = Category.objects.filter(
        is_active=True,
        parent=None
    ).prefetch_related('products')

    applications = Application.objects.filter(
        is_active=True,
    )
    return {
        'categories': categories,
        'applications': applications,
    }





from django.utils.translation import override
from django.urls import translate_url


def seo_context(request):
    current_url = request.build_absolute_uri()

    with override("fa"):
        alternate_fa = translate_url(current_url, "fa")

    with override("en"):
        alternate_en = translate_url(current_url, "en")

    return {
        "canonical_url": current_url,
        "alternate_fa": alternate_fa,
        "alternate_en": alternate_en,
        "site_url": request.build_absolute_uri("/"),
        "site_name": "Verona Lighting",
        "current_language": request.LANGUAGE_CODE,
    }