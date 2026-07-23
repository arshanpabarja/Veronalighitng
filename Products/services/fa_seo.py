"""Deterministic Persian SEO helpers for the Verona Lighting catalogue.

The functions in this module only use information already present on a product.
They intentionally avoid prices, availability, certifications, guarantees, and
other claims that cannot be inferred safely from catalogue data.
"""

from dataclasses import dataclass
import re
from typing import Any, Mapping


BRAND_FA = "ورونا لایتینگ"
TITLE_LIMIT = 65
DESCRIPTION_LIMIT = 160
ALT_LIMIT = 125

CATEGORY_KEYWORDS_BY_SLUG = {
    "low-voltage-magneto": ("magnetic", "چراغ مگنتی ریلی", 1),
    "magent-large4cm-family": ("magnetic-large", "چراغ مگنتی ۴۸ ولت", 1),
    "magent-small-family": ("magnetic-small", "چراغ مگنتی ظریف", 2),
    "magnet-curve": ("magnetic-curve", "چراغ مگنتی منحنی", 2),
    "mmagne-tbelt": ("magnetic-belt", "چراغ مگنتی نواری", 2),
    "magnet-flexi": ("magnetic-flexible", "چراغ مگنتی انعطاف‌پذیر", 2),
    "magnet-super-slim": ("magnetic-slim", "چراغ مگنتی سوپر اسلیم", 3),
    "linear": ("linear", "چراغ خطی", 1),
    "recessed": ("linear-recessed", "چراغ خطی توکار", 1),
    "surface-mount": ("linear-surface", "چراغ خطی روکار", 2),
    "pendant": ("linear-pendant", "چراغ خطی آویز", 2),
    "in-ground-mount": ("linear-inground", "چراغ خطی دفنی", 3),
    "cove-lighting": ("cove-lighting", "ریسه و نور مخفی", 3),
    "panel-downlight": ("panel-downlight", "چراغ پنل و دانلایت", 2),
    "panel": ("panel", "چراغ پنل LED", 2),
    "spotlights-track-lighting": ("track-lighting", "چراغ ریلی فروشگاهی", 2),
    "1hp": ("track-single-phase", "چراغ ریلی تک فاز", 2),
    "3hp": ("track-three-phase", "چراغ ریلی سه فاز", 2),
    "decorative": ("decorative", "چراغ دکوراتیو", 3),
    "industrial": ("industrial", "چراغ صنعتی LED", 3),
    "spotlights-underwater": ("waterproof", "چراغ ضد آب", 3),
    "outdoor": ("outdoor", "چراغ فضای باز", 3),
    "accessories": ("accessories", "اکسسوری روشنایی", 3),
}


@dataclass(frozen=True)
class PersianSEO:
    cluster: str
    keyword: str
    priority: int
    meta_title: str
    meta_description: str
    image_alt: str
    short_description: str


def _clean(value: Any) -> str:
    return " ".join(str(value or "").replace("\u200c", " ").split())


def _normalise(value: Any) -> str:
    text = _clean(value).lower()
    return (
        text.replace("ي", "ی")
        .replace("ك", "ک")
        .replace("‌", " ")
        .replace("&", " and ")
    )


def _contains(text: str, *terms: str) -> bool:
    return any(_normalise(term) in text for term in terms)


def _clip(text: str, limit: int) -> str:
    text = _clean(text)
    if len(text) <= limit:
        return text
    clipped = text[: limit - 1].rsplit(" ", 1)[0].rstrip("،؛:.- ")
    if not clipped:
        clipped = text[: limit - 1].rstrip()
    return f"{clipped}…"


def _joined_search_text(data: Mapping[str, Any]) -> str:
    fields = (
        "name_en",
        "name_fa",
        "subtitle_en",
        "subtitle_fa",
        "description_en",
        "description_fa",
        "full_description_en",
        "full_description_fa",
        "category_en",
        "category_fa",
        "family_en",
        "family_fa",
    )
    return _normalise(" ".join(_clean(data.get(field)) for field in fields))


def classify_keyword(data: Mapping[str, Any]) -> tuple[str, str, int]:
    """Return (cluster, primary Persian keyword, priority)."""

    text = _joined_search_text(data)
    identity_text = _normalise(
        " ".join(
            _clean(data.get(field))
            for field in (
                "name_en",
                "name_fa",
                "category_en",
                "category_fa",
            )
        )
    )
    name_text = _normalise(
        f"{_clean(data.get('name_en'))} {_clean(data.get('name_fa'))}"
    )
    name_en_text = _normalise(data.get("name_en"))
    type_name_text = name_en_text or name_text
    magnetic = _contains(
        identity_text,
        "magnet",
        "magnt",
        "مگنت",
        "مغناطیسی",
    )

    if magnetic:
        # Product names are more reliable than descriptions here: virtually
        # every magnetic module description mentions its compatible track.
        if _contains(type_name_text, "track", "ریل"):
            if _contains(text, "recess", "trimless", "توکار", "بدون لبه"):
                return "magnetic-track-recessed", "ریل مگنتی توکار", 1
            if _contains(text, "surface", "pendant", "روکار", "آویز"):
                return "magnetic-track-surface", "ریل مگنتی روکار و آویز", 2
            return "magnetic-track", "ریل چراغ مگنتی", 1
        if _contains(type_name_text, "sign emergency", "اضطراری"):
            return "magnetic-emergency", "چراغ اضطراری مگنتی", 3
        if _contains(type_name_text, "curve", "منحنی"):
            return "magnetic-curve", "چراغ مگنتی منحنی", 2
        if _contains(type_name_text, "flex", "انعطاف"):
            return "magnetic-flexible", "چراغ مگنتی انعطاف‌پذیر", 2
        if _contains(type_name_text, "belt", "نواری"):
            return "magnetic-belt", "چراغ مگنتی نواری", 2
        if _contains(type_name_text, "pendant", "آویز"):
            return "magnetic-pendant", "چراغ آویز مگنتی", 2
        if _contains(type_name_text, "spot", "اسپات"):
            return "magnetic-spot", "چراغ اسپات مگنتی", 1
        if _contains(type_name_text, "dot linear", "dot", "نقطه"):
            return "magnetic-dot-linear", "چراغ خطی نقطه‌ای مگنتی", 2
        if _contains(type_name_text, "linear", "خطی"):
            return "magnetic-linear", "چراغ خطی مگنتی", 1
        return "magnetic", "چراغ مگنتی ریلی", 1

    if _contains(type_name_text, "strip light", "ریسه"):
        if _contains(identity_text, "ip65", "ضد آب"):
            return "strip-ip", "ریسه LED ضد آب", 3
        return "strip", "ریسه LED", 3
    if _contains(type_name_text, "neon"):
        return "neon", "نئون فلکسی LED", 3
    if _contains(type_name_text, "profile", "پروفیل"):
        return "linear-profile", "پروفیل چراغ خطی", 3
    if _contains(type_name_text, "highbay", "های بی", "سوله"):
        return "highbay", "چراغ سوله‌ای LED", 3
    if _contains(type_name_text, "inground", "دفنی"):
        return "inground", "چراغ دفنی LED", 3

    if _contains(identity_text, "1ph", "3ph", "track", "ریل"):
        if _contains(type_name_text, "connector", "connection", "رابط", "اتصال"):
            return "track-accessory", "اتصالات ریل چراغ", 3
        if _contains(type_name_text, "spot", "spotlight", "اسپات"):
            return "track-spot", "چراغ ریلی فروشگاهی", 2
        return "track-lighting", "سیستم روشنایی ریلی", 2

    linear = _contains(
        text,
        "linear",
        "line light",
        "خطی",
        "لاین نوری",
        "recessed mount back light",
        "pendant mount back light",
    )
    if linear:
        if _contains(text, "recess", "trimless", "توکار", "بدون لبه"):
            if _contains(text, "trimless", "بدون لبه"):
                return "linear-recessed-trimless", "چراغ خطی توکار بدون لبه", 1
            return "linear-recessed", "چراغ خطی توکار", 1
        if _contains(text, "pendant", "آویز"):
            return "linear-pendant", "چراغ خطی آویز", 2
        if _contains(text, "surface", "روکار"):
            return "linear-surface", "چراغ خطی روکار", 2
        return "linear", "چراغ خطی LED", 2

    if _contains(type_name_text, "gypsum", "گچی"):
        return "gypsum-downlight", "چراغ گچی توکار", 2
    if _contains(type_name_text, "downlight", "دانلایت", "دان لایت"):
        return "downlight", "چراغ دانلایت توکار", 2
    if _contains(type_name_text, "surface", "روکار"):
        return "surface", "چراغ سقفی روکار", 3
    if _contains(type_name_text, "decorative", "دکوراتیو", "تزئینی"):
        return "decorative", "چراغ دکوراتیو", 3
    if _contains(identity_text, "downlight", "دانلایت", "دان لایت"):
        return "downlight", "چراغ دانلایت توکار", 2
    if _contains(identity_text, "trimless", "بدون لبه"):
        return "trimless", "چراغ توکار بدون لبه", 2

    if _contains(identity_text, "strip light", "ریسه"):
        if _contains(text, "ip65", "ضد آب"):
            return "strip-ip", "ریسه LED ضد آب", 3
        return "strip", "ریسه LED", 3
    if _contains(identity_text, "neon"):
        return "neon", "نئون فلکسی LED", 3
    if _contains(identity_text, "profile", "پروفیل"):
        return "linear-profile", "پروفیل چراغ خطی", 3
    if _contains(identity_text, "highbay", "های بی", "سوله"):
        return "highbay", "چراغ سوله‌ای LED", 3
    if _contains(identity_text, "inground", "دفنی"):
        return "inground", "چراغ دفنی LED", 3
    if _contains(text, "surface", "روکار"):
        return "surface", "چراغ سقفی روکار", 3
    if _contains(text, "pendant", "آویز"):
        return "pendant", "چراغ آویز مدرن", 3
    if _contains(text, "decorative", "دکوراتیو", "تزئینی"):
        return "decorative", "چراغ دکوراتیو", 3

    category_slug = _clean(data.get("category_slug"))
    if category_slug in CATEGORY_KEYWORDS_BY_SLUG:
        return CATEGORY_KEYWORDS_BY_SLUG[category_slug]

    category = _clean(data.get("category_fa"))
    if category and re.search(r"[\u0600-\u06ff]", category):
        return "category", category, 3
    return "architectural", "چراغ معماری", 3


def _display_name(data: Mapping[str, Any], prefer_fa: bool = False) -> str:
    name_fa = _clean(data.get("name_fa"))
    name_en = _clean(data.get("name_en"))
    if prefer_fa:
        return name_fa or name_en or "محصول روشنایی"
    # Product/family names are model identifiers and should remain exact.
    # Persian search intent is supplied by the keyword placed before them.
    return name_en or name_fa or "محصول روشنایی"


def _title(keyword: str, name: str) -> str:
    normal_keyword = _normalise(keyword)
    normal_name = _normalise(name)
    heading = name if normal_keyword in normal_name else f"{keyword} {name}"
    suffix = f" | {BRAND_FA}"
    available = TITLE_LIMIT - len(suffix)
    return f"{_clip(heading, available)}{suffix}"


def _keyword_title(keyword: str) -> str:
    suffix = f" | {BRAND_FA}"
    return f"{_clip(keyword, TITLE_LIMIT - len(suffix))}{suffix}"


def _specification_parts(data: Mapping[str, Any]) -> list[str]:
    parts: list[str] = []
    wattage = data.get("wattage")
    lumens = data.get("lumens")
    color_temperature = data.get("color_temperature")
    cri = data.get("cri")
    ip_rating = _clean(data.get("ip_rating"))
    voltage = _clean(data.get("voltage"))

    if wattage not in (None, ""):
        parts.append(f"توان {wattage} وات")
    if lumens not in (None, ""):
        parts.append(f"شار نوری {lumens} لومن")
    if color_temperature not in (None, ""):
        parts.append(f"دمای رنگ {color_temperature} کلوین")
    if cri not in (None, ""):
        parts.append(f"CRI {cri}")
    if ip_rating:
        parts.append(f"درجه حفاظت {ip_rating}")
    if voltage:
        parts.append(f"ولتاژ {voltage}")
    return parts


def _description_guidance(cluster: str, keyword: str) -> str:
    if cluster.startswith("magnetic"):
        return (
            "این مدل بخشی از یک سیستم روشنایی مگنتی است؛ بنابراین ریل، منبع تغذیه "
            "و سایر ماژول‌ها باید از نظر ابعاد و مشخصات الکتریکی با آن سازگار باشند. "
            "در طراحی مسیر نور، نوع نصب ریل و فاصله ماژول‌ها را متناسب با پلان پروژه انتخاب کنید."
        )
    if cluster.startswith("linear"):
        return (
            "برای انتخاب چراغ خطی مناسب، نوع نصب، طول مسیر، عرض برش یا سطح نصب و "
            "مقدار نور مورد نیاز فضا را هم‌زمان بررسی کنید. پیوستگی مسیر و محل قرارگیری "
            "اتصالات نیز باید پیش از اجرا با نقشه سقف هماهنگ شود."
        )
    if cluster in ("gypsum-downlight", "downlight", "trimless"):
        return (
            "در انتخاب چراغ توکار، ابعاد برش سقف، عمق فضای پشت سقف و نحوه پخش نور اهمیت دارد. "
            "تعداد و فاصله چراغ‌ها باید بر اساس ابعاد فضا و روشنایی مورد نیاز تعیین شود تا "
            "چیدمان نهایی منظم و عملکرد نور متناسب با پروژه باشد."
        )
    if cluster.startswith("track"):
        return (
            "این محصول باید با نوع ریل و قطعات همان سیستم هماهنگ انتخاب شود. پیش از سفارش، "
            "تک‌فاز یا سه‌فاز بودن ریل، شکل اتصال، مسیر اجرا و تعداد چراغ‌های مورد نیاز را "
            "در نقشه روشنایی کنترل کنید."
        )
    if cluster in ("strip", "strip-ip", "neon", "linear-profile"):
        return (
            "در طراحی نور خطی و مخفی، محل نصب، طول مسیر، فضای دفع حرارت و دسترسی به منبع تغذیه "
            "باید از ابتدا مشخص باشد. انتخاب پروفیل و تجهیزات سازگار به اجرای مرتب‌تر و "
            "نگهداری ساده‌تر مجموعه کمک می‌کند."
        )
    if cluster == "inground":
        return (
            "برای چراغ دفنی باید محل نصب، شرایط محیطی، زهکشی و درجه حفاظت مورد نیاز پروژه "
            "پیش از انتخاب بررسی شود. ابعاد محل نصب و دسترسی آینده برای سرویس نیز باید "
            "در جزئیات اجرایی پیش‌بینی شود."
        )
    if cluster == "highbay":
        return (
            "در انتخاب چراغ برای فضاهای مرتفع، ارتفاع نصب، سطح روشنایی مورد نیاز و نحوه "
            "توزیع نور اهمیت دارد. جانمایی چراغ‌ها باید بر اساس ابعاد فضا و شرایط واقعی "
            "پروژه انجام شود."
        )
    if cluster in ("decorative", "surface", "pendant"):
        return (
            "در انتخاب این مدل، تناسب ابعاد چراغ با مقیاس فضا، ارتفاع نصب و نقش آن در "
            "نور عمومی یا دکوراتیو را در نظر بگیرید. رنگ نور و نحوه قرارگیری چراغ باید "
            "با سایر منابع نور و طراحی داخلی هماهنگ باشد."
        )
    return (
        f"برای انتخاب {keyword} مناسب، نوع نصب، ابعاد، مشخصات الکتریکی و مقدار نور مورد نیاز "
        "پروژه را بررسی کنید. انتخاب نهایی باید با نقشه روشنایی و شرایط واقعی محل اجرا هماهنگ باشد."
    )


def build_full_description_fa(
    data: Mapping[str, Any],
    existing_text: str = "",
) -> str:
    """Expand a missing or thin Persian description using verified catalogue data."""

    cluster, keyword, _priority = classify_keyword(data)
    name = _display_name(data)
    category = _clean(data.get("category_fa") or data.get("category_en"))
    existing = _clean(existing_text)
    specs = _specification_parts(data)

    if existing:
        opening = existing
    else:
        context = f" در گروه {category}" if category else ""
        opening = (
            f"{name} یکی از مدل‌های {keyword} {BRAND_FA}{context} است. "
            "این صفحه برای بررسی ویژگی‌های محصول، مدل‌های موجود و اطلاعات مورد نیاز "
            "برای انتخاب آن در پروژه‌های روشنایی تهیه شده است."
        )

    if specs:
        visible_specs = "، ".join(specs[:4])
        specification_text = (
            f"مشخصات ثبت‌شده برای این محصول شامل {visible_specs} است. "
            "این مقادیر را همراه با ابعاد، شرایط نصب و نیاز روشنایی فضا بررسی کنید؛ "
            "زیرا انتخاب مناسب فقط بر اساس یک مشخصه انجام نمی‌شود."
        )
    else:
        specification_text = (
            "هنگام انتخاب نسخه مناسب، مشخصات مدل، ابعاد، نوع نصب و سازگاری تجهیزات را "
            "با نیاز پروژه کنترل کنید. اگر اطلاعات فنی مورد نیاز در جدول محصول درج نشده است، "
            "پیش از سفارش آن را با واحد فنی ورونا لایتینگ بررسی کنید."
        )

    family_text = (
        f"برای مقایسه {name} با سایر مدل‌های مرتبط، جدول مدل‌ها و محصولات پیشنهادی همین صفحه "
        "را بررسی کنید. انتخاب نهایی باید بر اساس محل نصب، هدف نورپردازی و مشخصات مورد نیاز "
        "پروژه انجام شود."
    )

    return "\n\n".join(
        (
            opening,
            _description_guidance(cluster, keyword),
            specification_text,
            family_text,
        )
    )


def build_product_fa_seo(data: Mapping[str, Any]) -> PersianSEO:
    cluster, keyword, priority = classify_keyword(data)
    name = _display_name(data)
    specs = _specification_parts(data)

    intro = f"{name}، {keyword} از {BRAND_FA}"
    if specs:
        description = (
            f"{intro} با {specs[0]}"
            f"{f' و {specs[1]}' if len(specs) > 1 else ''}. "
            "مشخصات فنی، مدل‌ها و تصاویر محصول را بررسی و برای انتخاب پروژه مشاوره دریافت کنید."
        )
    else:
        description = (
            f"{intro}. مشخصات فنی، مدل‌ها و تصاویر محصول را بررسی کنید "
            "و برای انتخاب روشنایی مناسب پروژه مشاوره دریافت کنید."
        )

    short_description = (
        f"{name} از خانواده {keyword} {BRAND_FA} است. "
        "برای بررسی مشخصات فنی، مدل‌های موجود و انتخاب مناسب پروژه طراحی شده است."
    )
    image_alt = (
        name
        if _normalise(keyword) in _normalise(name)
        else f"{keyword} مدل {name}"
    )
    image_alt = f"{image_alt} {BRAND_FA}"

    return PersianSEO(
        cluster=cluster,
        keyword=keyword,
        priority=priority,
        meta_title=_title(keyword, name),
        meta_description=_clip(description, DESCRIPTION_LIMIT),
        image_alt=_clip(image_alt, ALT_LIMIT),
        short_description=_clip(short_description, 300),
    )


def build_family_fa_seo(data: Mapping[str, Any]) -> PersianSEO:
    """Build metadata for a family/collection page without product claims."""

    cluster, keyword, priority = classify_keyword(data)
    name = _display_name(data)
    description = (
        f"خانواده {name} از مجموعه {keyword} {BRAND_FA}. "
        "مدل‌ها، تصاویر و اطلاعات فنی این مجموعه را مقایسه کنید "
        "و برای انتخاب مناسب پروژه مشاوره دریافت کنید."
    )
    short_description = (
        f"مجموعه {name} شامل راهکارهای {keyword} برای پروژه‌های روشنایی است. "
        "مدل‌های این خانواده را بررسی و با یکدیگر مقایسه کنید."
    )
    image_alt = f"خانواده {keyword} {name} {BRAND_FA}"

    return PersianSEO(
        cluster=cluster,
        keyword=keyword,
        priority=priority,
        meta_title=_title(keyword, name),
        meta_description=_clip(description, DESCRIPTION_LIMIT),
        image_alt=_clip(image_alt, ALT_LIMIT),
        short_description=_clip(short_description, 300),
    )


def build_category_fa_seo(data: Mapping[str, Any]) -> PersianSEO:
    """Build metadata for a broad category landing page."""

    slug = _clean(data.get("slug"))
    cluster, keyword, priority = CATEGORY_KEYWORDS_BY_SLUG.get(
        slug,
        classify_keyword(data),
    )
    name = _display_name(data, prefer_fa=True)
    heading = name if _normalise(keyword) in _normalise(name) else keyword
    description = (
        f"انواع {heading} {BRAND_FA} را با تصاویر و اطلاعات فنی بررسی کنید. "
        "مقایسه خانواده‌ها و دریافت مشاوره برای انتخاب روشنایی مناسب پروژه."
    )
    short_description = (
        f"مجموعه محصولات {heading} {BRAND_FA} برای بررسی و مقایسه "
        "راهکارهای روشنایی پروژه‌های معماری."
    )

    return PersianSEO(
        cluster=cluster,
        keyword=keyword,
        priority=priority,
        meta_title=_keyword_title(keyword),
        meta_description=_clip(description, DESCRIPTION_LIMIT),
        image_alt="",
        short_description=_clip(short_description, 300),
    )
