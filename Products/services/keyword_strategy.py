"""Primary keyword ownership for the first 90-day Persian SEO campaign."""

from dataclasses import dataclass


@dataclass(frozen=True)
class KeywordLandingPage:
    cluster: str
    primary_keyword_fa: str
    supporting_keywords_fa: tuple[str, ...]
    category_slug: str
    parent_slug: str | None
    name_fa: str
    name_en: str
    meta_title_fa: str
    meta_title_en: str
    meta_description_fa: str
    meta_description_en: str
    supporting_pages: tuple[str, ...]


KEYWORD_LANDING_PAGES = {
    "recessed-linear": KeywordLandingPage(
        cluster="recessed-linear",
        primary_keyword_fa="چراغ خطی توکار",
        supporting_keywords_fa=(
            "چراغ خطی توکار سقفی",
            "چراغ خطی بدون لبه",
            "قیمت چراغ خطی توکار",
            "خرید چراغ خطی توکار",
        ),
        category_slug="recessed",
        parent_slug="linear",
        name_fa="چراغ خطی توکار",
        name_en="Recessed Linear Lighting",
        meta_title_fa="چراغ خطی توکار سقفی و بدون لبه | ورونا لایتینگ",
        meta_title_en="Recessed Linear Lighting | Verona Lighting",
        meta_description_fa=(
            "مدل‌های چراغ خطی توکار سقفی ورونا را در نسخه‌های لبه‌دار و بدون لبه "
            "بررسی کنید؛ مقایسه ابعاد شیار، عرض پروفیل، توان و شار نوری برای انتخاب پروژه."
        ),
        meta_description_en=(
            "Compare Verona recessed linear lighting in trimmed and trimless "
            "profiles, including cut-out dimensions, profile widths, power and "
            "lumen output."
        ),
        supporting_pages=(
            "/linear/",
            "/linear/c/recessed/BD/",
            "/linear/c/recessed/sp/",
        ),
    ),
    "magnetic-track": KeywordLandingPage(
        cluster="magnetic-track",
        primary_keyword_fa="چراغ مگنتی",
        supporting_keywords_fa=(
            "چراغ ریلی مگنتی",
            "ریل مگنتی",
            "قیمت چراغ مگنتی",
            "خرید چراغ مگنتی",
            "سیستم روشنایی مگنتی",
        ),
        category_slug="low-voltage-magneto",
        parent_slug=None,
        name_fa="چراغ مگنتی",
        name_en="Magnetic Track Lighting",
        meta_title_fa="چراغ مگنتی و ریل مگنتی | ورونا لایتینگ",
        meta_title_en="Magnetic Track Lighting | Verona Lighting",
        meta_description_fa=(
            "مدل‌های چراغ مگنتی و ریل مگنتی ورونا را در سری‌های اسمال، لارج، "
            "کرو، بلت و فلکسی بررسی و برای پروژه‌های نورپردازی معماری مقایسه کنید."
        ),
        meta_description_en=(
            "Explore Verona magnetic track lighting systems, rails and modules "
            "across Small, Large, Curve, Belt and Flexi collections for "
            "architectural projects."
        ),
        supporting_pages=(
            "/low-voltage-magneto/c/magent-small-family/",
            "/low-voltage-magneto/c/magent-large4cm-family/",
            "/low-voltage-magneto/c/mmagne-tbelt/",
            "/low-voltage-magneto/c/magnet-curve/",
            "/low-voltage-magneto/c/magnet-flexi/",
        ),
    ),
}


SUPPORTING_CATEGORY_METADATA = {
    "linear": {
        "meta_title_fa": "چراغ خطی معماری؛ روکار، آویز و دفنی | ورونا لایتینگ",
        "meta_title_en": "Architectural Linear Lighting | Verona Lighting",
    },
}


def validate_keyword_strategy() -> None:
    """Reject ambiguous or search-snippet-unfriendly campaign mappings."""

    primary_keywords = set()
    category_keys = set()

    for landing_page in KEYWORD_LANDING_PAGES.values():
        keyword = landing_page.primary_keyword_fa
        category_key = (landing_page.parent_slug, landing_page.category_slug)

        if keyword in primary_keywords:
            raise ValueError(f"Duplicate primary keyword: {keyword}")
        if category_key in category_keys:
            raise ValueError(f"Duplicate primary category: {category_key}")
        if keyword not in landing_page.name_fa:
            raise ValueError(
                f"{landing_page.cluster}: primary keyword is missing from H1."
            )
        if keyword not in landing_page.meta_title_fa:
            raise ValueError(
                f"{landing_page.cluster}: primary keyword is missing from title."
            )
        if len(landing_page.meta_title_fa) > 65:
            raise ValueError(
                f"{landing_page.cluster}: Persian title exceeds 65 characters."
            )
        if len(landing_page.meta_title_en) > 65:
            raise ValueError(
                f"{landing_page.cluster}: English title exceeds 65 characters."
            )
        if len(landing_page.meta_description_fa) > 160:
            raise ValueError(
                f"{landing_page.cluster}: Persian description exceeds 160 characters."
            )
        if len(landing_page.meta_description_en) > 160:
            raise ValueError(
                f"{landing_page.cluster}: English description exceeds 160 characters."
            )

        primary_keywords.add(keyword)
        category_keys.add(category_key)
