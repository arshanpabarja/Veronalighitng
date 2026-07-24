from dataclasses import dataclass

from django.urls import reverse


@dataclass(frozen=True)
class ClusterLink:
    key: str
    route_name: str
    route_kwargs: tuple[tuple[str, str], ...]
    label_fa: str
    label_en: str
    description_fa: str
    description_en: str


CLUSTER_LINKS = {
    "recessed-linear": ClusterLink(
        key="recessed-linear",
        route_name="products:child_detail",
        route_kwargs=(("cat_slug", "linear"), ("child_slug", "recessed")),
        label_fa="راهنمای انتخاب چراغ خطی توکار",
        label_en="Recessed linear lighting selection guide",
        description_fa=(
            "مدل‌های لبه‌دار و بدون لبه، نکات اجرای سقف و خانواده‌های "
            "چراغ خطی توکار ورونا را مقایسه کنید."
        ),
        description_en=(
            "Compare trimmed and trimless systems, ceiling coordination points "
            "and Verona recessed linear families."
        ),
    ),
    "magnetic-track": ClusterLink(
        key="magnetic-track",
        route_name="products:category_detail",
        route_kwargs=(("cat_slug", "low-voltage-magneto"),),
        label_fa="راهنمای انتخاب چراغ مگنتی و ریل مگنتی",
        label_en="Magnetic track lighting selection guide",
        description_fa=(
            "خانواده‌های ریل، روش‌های نصب و ماژول‌های خطی، اسپات و آویز "
            "سیستم چراغ مگنتی را بررسی کنید."
        ),
        description_en=(
            "Review track families, mounting methods and linear, spot and pendant "
            "modules for magnetic lighting systems."
        ),
    ),
}


def cluster_key_for_category(category):
    if not category:
        return None

    slugs = []
    current = category
    while current:
        slugs.append(current.slug)
        current = current.parent

    if category.slug == "recessed" and "linear" in slugs:
        return "recessed-linear"
    if "low-voltage-magneto" in slugs:
        return "magnetic-track"
    return None


def build_seo_cluster_links(categories, language_code):
    keys = {
        key
        for category in categories
        if (key := cluster_key_for_category(category))
    }
    if not keys:
        return None

    language = "fa" if language_code == "fa" else "en"
    links = []
    for key in ("recessed-linear", "magnetic-track"):
        if key not in keys:
            continue
        config = CLUSTER_LINKS[key]
        links.append(
            {
                "key": key,
                "url": reverse(config.route_name, kwargs=dict(config.route_kwargs)),
                "label": getattr(config, f"label_{language}"),
                "description": getattr(config, f"description_{language}"),
            }
        )

    if language == "fa":
        heading = "راهنماهای مرتبط با این صفحه"
        intro = (
            "برای مقایسه دقیق‌تر سیستم‌ها و رسیدن به صفحه اصلی هر موضوع، "
            "از راهنماهای مرتبط زیر استفاده کنید."
        )
    else:
        heading = "Guides related to this page"
        intro = (
            "Use these related guides to compare systems and continue to the "
            "primary page for each lighting topic."
        )

    return {"heading": heading, "intro": intro, "links": links}
