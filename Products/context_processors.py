from urllib.parse import urlencode

from django.urls import translate_url

from core.business_identity import BUSINESS_IDENTITY

from .models import Application
from .services.category_ordering import navigation_categories


def navbar_categories(request):
    """
    این context processor در تمام تمپلیت‌ها
    متغیر categories را در دسترس قرار می‌دهد
    """
    categories = navigation_categories()

    applications = Application.objects.filter(
        is_active=True,
    )
    return {
        'categories': categories,
        'applications': applications,
    }


def seo_context(request):
    """
    Build one clean, language-aware SEO URL for every public template.

    Filter and tracking parameters are intentionally excluded. A standalone
    pagination parameter is retained so paginated result pages can canonicalize
    to themselves.
    """
    query_string = ""
    page = request.GET.get("page")
    query_keys = set(request.GET.keys())
    if query_keys == {"page"} and page and page.isdigit() and int(page) > 1:
        query_string = urlencode({"page": int(page)})

    clean_path = request.path
    if query_string:
        clean_path = f"{clean_path}?{query_string}"

    current_url = request.build_absolute_uri(clean_path)

    alternate_fa = translate_url(current_url, "fa")
    alternate_en = translate_url(current_url, "en")

    return {
        "canonical_url": current_url,
        "seo_canonical_url": current_url,
        "alternate_fa": alternate_fa,
        "alternate_en": alternate_en,
        "alternate_x_default": alternate_fa,
        "seo_noindex_query": bool(query_keys - {"page"}),
        "site_url": request.build_absolute_uri("/"),
        "site_name": "Verona Lighting",
        "current_language": request.LANGUAGE_CODE,
        "business_identity": BUSINESS_IDENTITY,
    }
