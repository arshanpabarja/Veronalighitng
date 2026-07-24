"""Reviewed bilingual SEO copy for the main public site pages."""

from dataclasses import dataclass


@dataclass(frozen=True)
class PageSEO:
    meta_title_fa: str
    meta_title_en: str
    meta_description_fa: str
    meta_description_en: str
    og_title_fa: str
    og_title_en: str
    og_description_fa: str
    og_description_en: str


SITE_SEO = {
    "index": PageSEO(
        meta_title_fa="چراغ خطی و مگنتی معماری | ورونا لایتینگ",
        meta_title_en="Architectural Linear & Magnetic Lighting | Verona",
        meta_description_fa="چراغ خطی توکار، روکار و آویز، چراغ مگنتی ریلی، پنل، ترک‌لایت و راهکارهای روشنایی معماری ورونا را برای پروژه‌های ایران بررسی کنید.",
        meta_description_en="Explore Verona architectural lighting: recessed, surface and pendant linear lights, magnetic track systems, panels and track lighting.",
        og_title_fa="روشنایی معماری ورونا؛ چراغ خطی و مگنتی",
        og_title_en="Verona Architectural Lighting",
        og_description_fa="مجموعه چراغ‌های خطی، مگنتی، پنل، ریلی، دکوراتیو و صنعتی ورونا برای بررسی و انتخاب در پروژه‌های معماری.",
        og_description_en="Discover Verona linear, magnetic, panel, track, decorative and industrial lighting for architectural projects.",
    ),
    "about": PageSEO(
        meta_title_fa="درباره ورونا لایتینگ | روشنایی معماری",
        meta_title_en="About Verona Lighting | Architectural Lighting",
        meta_description_fa="با رویکرد ورونا لایتینگ در طراحی و توسعه چراغ‌های معماری، هماهنگی فنی با پروژه و مجموعه راهکارهای روشنایی این برند آشنا شوید.",
        meta_description_en="Learn about Verona Lighting's approach to architectural luminaires, technical project coordination and considered lighting solutions.",
        og_title_fa="درباره استودیو روشنایی ورونا",
        og_title_en="About Verona Lighting",
        og_description_fa="نگاهی به رویکرد طراحی، توسعه محصول و همکاری پروژه‌ای ورونا لایتینگ در حوزه روشنایی معماری.",
        og_description_en="A look at Verona Lighting's design approach, product development and collaboration on architectural lighting projects.",
    ),
    "story": PageSEO(
        meta_title_fa="داستان ورونا لایتینگ | مسیر طراحی و اعتماد",
        meta_title_en="Our Story | Verona Lighting",
        meta_description_fa="داستان شکل‌گیری و رشد ورونا لایتینگ، نگاه این مجموعه به طراحی چراغ، کیفیت فنی و همکاری با معماران و مجریان پروژه را بخوانید.",
        meta_description_en="Read the story of Verona Lighting and its approach to luminaire design, technical quality and collaboration with project teams.",
        og_title_fa="داستان ورونا؛ مسیر نور، طراحی و اعتماد",
        og_title_en="The Verona Lighting Story",
        og_description_fa="با مسیر شکل‌گیری ورونا لایتینگ و ارزش‌هایی که طراحی محصول و همکاری‌های پروژه‌ای این مجموعه را هدایت می‌کنند آشنا شوید.",
        og_description_en="Discover the journey and values that guide Verona Lighting's product design and architectural project partnerships.",
    ),
    "products": PageSEO(
        meta_title_fa="محصولات روشنایی معماری | ورونا لایتینگ",
        meta_title_en="Architectural Lighting Products | Verona Lighting",
        meta_description_fa="محصولات ورونا شامل چراغ خطی، مگنتی، پنل و دانلایت، ترک‌لایت، دکوراتیو، صنعتی و فضای باز را با مشخصات فنی بررسی کنید.",
        meta_description_en="Browse Verona linear, magnetic, panel, downlight, track, decorative, industrial and outdoor lighting with technical product data.",
        og_title_fa="کاتالوگ محصولات روشنایی ورونا",
        og_title_en="Explore Verona Lighting Products",
        og_description_fa="دسته‌بندی‌ها، خانواده‌ها و مدل‌های روشنایی ورونا را برای انتخاب متناسب با نیاز پروژه بررسی و مقایسه کنید.",
        og_description_en="Explore and compare Verona lighting categories, families and models for architectural project requirements.",
    ),
    "applications": PageSEO(
        meta_title_fa="کاربردهای روشنایی معماری | ورونا لایتینگ",
        meta_title_en="Architectural Lighting Applications | Verona",
        meta_description_fa="راهکارهای روشنایی ورونا را برای خانه، دفتر، فروشگاه، گالری، فضای هتلی، نما و محوطه بررسی و خانواده‌های مرتبط را پیدا کنید.",
        meta_description_en="Explore Verona lighting for homes, offices, retail, galleries, hospitality, façades and landscapes, with related product families.",
        og_title_fa="راهکارهای روشنایی برای فضاهای مختلف",
        og_title_en="Lighting Solutions by Application",
        og_description_fa="از فضای مسکونی و اداری تا فروشگاه، گالری، هتل، نما و محوطه؛ محصولات مرتبط ورونا را براساس کاربرد پیدا کنید.",
        og_description_en="Find Verona product families for residential, office, retail, gallery, hospitality, façade and landscape lighting.",
    ),
    "news": PageSEO(
        meta_title_fa="مجله روشنایی و معماری | ورونا لایتینگ",
        meta_title_en="Lighting and Architecture Journal | Verona",
        meta_description_fa="مقاله‌ها و خبرهای ورونا درباره روشنایی معماری، انتخاب چراغ، طراحی نور و معرفی راهکارها و محصولات مرتبط را مطالعه کنید.",
        meta_description_en="Read Verona articles and news about architectural lighting, luminaire selection, lighting design and related product solutions.",
        og_title_fa="مجله ورونا؛ روشنایی، محصول و معماری",
        og_title_en="Verona Lighting Journal",
        og_description_fa="مطالب آموزشی و خبری درباره طراحی نور، انتخاب محصولات روشنایی و راهکارهای کاربردی برای پروژه‌های معماری.",
        og_description_en="Articles and updates on lighting design, product selection and practical solutions for architectural projects.",
    ),
}


def validate_site_seo() -> None:
    if set(SITE_SEO) != {
        "index",
        "about",
        "story",
        "products",
        "applications",
        "news",
    }:
        raise ValueError("SEO copy must cover all six public page groups.")

    for page, content in SITE_SEO.items():
        for language in ("fa", "en"):
            title = getattr(content, f"meta_title_{language}")
            description = getattr(content, f"meta_description_{language}")
            og_title = getattr(content, f"og_title_{language}")
            og_description = getattr(content, f"og_description_{language}")
            if not all((title, description, og_title, og_description)):
                raise ValueError(f"{page}/{language}: an SEO field is empty.")
            if len(title) > 60 or len(og_title) > 60:
                raise ValueError(f"{page}/{language}: a title exceeds 60 characters.")
            if len(description) > 160 or len(og_description) > 160:
                raise ValueError(
                    f"{page}/{language}: a description exceeds 160 characters."
                )
