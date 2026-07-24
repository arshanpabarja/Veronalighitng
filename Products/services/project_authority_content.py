"""Reviewed bilingual SEO content for the projects used in authority outreach."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ProjectAuthorityContent:
    name_fa: str
    location_fa: str
    project_type_fa: str
    intro_heading_fa: str
    intro_text_fa: str
    overview_text_fa: str
    about_content_fa: str
    meta_title_fa: str
    meta_description_fa: str
    meta_title_en: str
    meta_description_en: str


PROJECT_AUTHORITY_CONTENT = {
    "private-villa": ProjectAuthorityContent(
        name_fa="ویلای خصوصی رویان",
        location_fa="رویان، مازندران",
        project_type_fa="مسکونی",
        intro_heading_fa="نورپردازی ویلای خصوصی در رویان",
        intro_text_fa=(
            "این ویلای خصوصی در رویان با رویکردی معاصر و متناسب با اقلیم آرام "
            "ساحلی مازندران طراحی شده است. نورپردازی داخلی پروژه بر ایجاد روشنایی "
            "یکنواخت، کنترل خیرگی و حفظ سادگی معماری تمرکز دارد. ترکیب نور عمومی "
            "و نورهای موضعی، بافت متریال‌ها و تناسبات فضا را بدون ایجاد شلوغی بصری "
            "نمایان می‌کند."
        ),
        overview_text_fa=(
            "در طراحی نورپردازی ویلای خصوصی رویان، هر فضا بر اساس نوع استفاده، "
            "میزان نور طبیعی و ارتباط آن با بخش‌های مجاور بررسی شده است. هدف، ایجاد "
            "محیطی آرام و کاربردی برای زندگی روزمره بود؛ به همین دلیل شدت و جهت نور "
            "در مسیرهای حرکتی، فضاهای نشیمن و نقاط تمرکز به‌صورت جداگانه تعریف شد.\n\n"
            "چراغ‌های سقفی روکار و دکوراتیو با جانمایی حساب‌شده، روشنایی پایه و تأکیدی "
            "را تأمین می‌کنند. این ترکیب به معماری اجازه می‌دهد در طول روز و شب هویت "
            "یکپارچه خود را حفظ کند و در عین حال امکان نگهداری و تغییر چیدمان نیز ساده "
            "باقی بماند."
        ),
        about_content_fa=(
            "<p>ایده اصلی پروژه، شکل‌دادن به فضایی مسکونی بود که آرامش، عملکرد و "
            "کیفیت بصری را هم‌زمان حفظ کند. زبان معماری کنترل‌شده است و نور، تناسب "
            "و جنس سطوح عناصر اصلی ساختن اتمسفر فضا هستند.</p>"
            "<p>در انتخاب چراغ‌ها، کیفیت نور، هماهنگی ابعاد چراغ با مقیاس سقف و امکان "
            "ایجاد لایه‌های متفاوت روشنایی در اولویت قرار گرفت. نور عمومی برای حرکت "
            "و فعالیت روزانه با نور تأکیدی برای برجسته‌کردن مبلمان و جزئیات معماری "
            "ترکیب شده است.</p>"
            "<p>نتیجه، نورپردازی یکپارچه‌ای است که حضور تجهیزات را به حداقل می‌رساند "
            "و در عین حال خوانایی و عمق فضای داخلی ویلا را افزایش می‌دهد.</p>"
        ),
        meta_title_fa="نورپردازی ویلای خصوصی رویان | ورونا لایتینگ",
        meta_description_fa=(
            "پروژه نورپردازی ویلای خصوصی رویان؛ بررسی طراحی روشنایی مسکونی، ترکیب "
            "نور عمومی و تأکیدی و چراغ‌های استفاده‌شده در این پروژه."
        ),
        meta_title_en="Private Villa Lighting, Royan | Verona Lighting",
        meta_description_en=(
            "Explore the lighting design of a private villa in Royan, including "
            "its layered residential lighting approach and selected luminaires."
        ),
    ),
    "diamond-boutique": ProjectAuthorityContent(
        name_fa="بوتیک دایموند",
        location_fa="مرکز خرید اپال، تهران",
        project_type_fa="فضای تجاری",
        intro_heading_fa="طراحی نورپردازی بوتیک دایموند",
        intro_text_fa=(
            "بوتیک دایموند در مرکز خرید اپال تهران، یک پروژه نورپردازی فروشگاهی "
            "است که در آن نمایش دقیق محصول و ساختن اتمسفر برند در اولویت قرار دارد. "
            "راهکار روشنایی بر کنترل کنتراست، هدایت نگاه و انعطاف‌پذیری چیدمان تمرکز "
            "می‌کند تا محصولات در مرکز توجه باقی بمانند."
        ),
        overview_text_fa=(
            "در بوتیک دایموند، نور به‌عنوان بخشی از طراحی داخلی و تجربه خرید در نظر "
            "گرفته شده است. روشنایی عمومی کنترل‌شده، پس‌زمینه‌ای آرام ایجاد می‌کند و "
            "نورهای تأکیدی، ویترین‌ها و محدوده‌های اصلی نمایش محصول را از نظر بصری "
            "تفکیک می‌کنند.\n\n"
            "سیستم روشنایی قابل تنظیم به فروشگاه اجازه می‌دهد با تغییر کالکشن یا "
            "چیدمان، جهت و تمرکز نور را اصلاح کند. این انعطاف باعث می‌شود هویت بصری "
            "فروشگاه ثابت بماند، در حالی که سناریوی نمایش محصولات می‌تواند متناسب با "
            "نیاز هر دوره تغییر کند."
        ),
        about_content_fa=(
            "<p>فلسفه طراحی بوتیک دایموند بر دقت و انعطاف استوار است. جزئیات داخلی "
            "عمداً ساده نگه داشته شده‌اند تا کالاها نقطه اصلی توجه باشند و نور، ریتم "
            "و سلسله‌مراتب فضا را تعریف کند.</p>"
            "<p>چراغ‌های ریلی و نورهای موضعی امکان تنظیم زاویه تابش و تمرکز بر قفسه‌ها، "
            "ویترین و نقاط شاخص را فراهم می‌کنند. کنترل خیرگی و فاصله مناسب چراغ‌ها "
            "کمک می‌کند رنگ، فرم و درخشش محصولات با وضوح بیشتری دیده شود.</p>"
            "<p>نتیجه، فضایی تجاری با نورپردازی منظم و قابل بازتنظیم است که ارائه "
            "محصول، مسیر حرکت مشتری و شخصیت برند را در یک ساختار هماهنگ جمع می‌کند.</p>"
        ),
        meta_title_fa="طراحی نورپردازی بوتیک دایموند تهران | ورونا",
        meta_description_fa=(
            "پروژه نورپردازی بوتیک دایموند در مرکز خرید اپال تهران؛ طراحی روشنایی "
            "فروشگاهی با نور تأکیدی، کنترل کنتراست و چیدمان انعطاف‌پذیر."
        ),
        meta_title_en="Diamond Boutique Lighting, Tehran | Verona",
        meta_description_en=(
            "See the retail lighting concept for Diamond Boutique in Tehran, using "
            "adjustable accent lighting to support product display and visual focus."
        ),
    ),
}


def validate_project_authority_content():
    if set(PROJECT_AUTHORITY_CONTENT) != {"private-villa", "diamond-boutique"}:
        raise ValueError("The authority project set must contain the two published projects.")

    for slug, content in PROJECT_AUTHORITY_CONTENT.items():
        for language in ("fa", "en"):
            title = getattr(content, f"meta_title_{language}")
            description = getattr(content, f"meta_description_{language}")
            if not 30 <= len(title) <= 60:
                raise ValueError(f"{slug} {language} meta title is outside 30–60 characters.")
            if not 110 <= len(description) <= 160:
                raise ValueError(
                    f"{slug} {language} meta description is outside 110–160 characters."
                )

        visible_fa = " ".join(
            (
                content.intro_text_fa,
                content.overview_text_fa,
                content.about_content_fa,
            )
        )
        if len(visible_fa) < 1200:
            raise ValueError(f"{slug} Persian case-study content is too short.")
