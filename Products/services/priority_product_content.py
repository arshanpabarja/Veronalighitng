from dataclasses import dataclass

from django.urls import reverse


@dataclass(frozen=True)
class GuideItem:
    title: str
    body: str


@dataclass(frozen=True)
class FAQ:
    question: str
    answer: str


@dataclass(frozen=True)
class RelatedLink:
    label: str
    description: str
    route_name: str
    route_kwargs: tuple[tuple[str, str], ...]


@dataclass(frozen=True)
class ProductTranslation:
    keyword: str
    name: str
    subtitle: str
    description: str
    meta_title: str
    meta_description: str
    image_alt: str
    guide_heading: str
    guide_intro: str
    guide_items: tuple[GuideItem, ...]
    faq_heading: str
    faqs: tuple[FAQ, ...]
    related_heading: str
    related_links: tuple[RelatedLink, ...]


@dataclass(frozen=True)
class PriorityProduct:
    category_slug: str
    family_slug: str
    translations: dict[str, ProductTranslation]


def _product_link(label, description, family_slug, product_slug):
    return RelatedLink(
        label,
        description,
        "products:product_detail",
        (
            ("cat_slug", "linear" if family_slug in {"sp", "BD"} else "low-voltage-magneto"),
            (
                "child_slug",
                "recessed"
                if family_slug in {"sp", "BD"}
                else (
                    "magent-small-family"
                    if family_slug == "magnet-linear-small"
                    else "magent-large4cm-family"
                ),
            ),
            (
                "family_slug",
                family_slug
                if family_slug in {"sp", "BD"}
                else "magnet-linear",
            ),
            ("slug", product_slug),
        ),
    )


PRIORITY_PRODUCT_CONTENT = {
    "sp-narrow": PriorityProduct(
        category_slug="recessed",
        family_slug="sp",
        translations={
            "fa": ProductTranslation(
                keyword="چراغ خطی توکار لبه‌دار باریک",
                name="چراغ خطی توکار لبه‌دار SP NARROW",
                subtitle=(
                    "چراغ خطی توکار باریک با لبه ظریف، برش ۳۵ میلی‌متر و توان "
                    "۲۰ وات در متر برای نور عمومی داخلی"
                ),
                description=(
                    "SP NARROW یک چراغ خطی توکار لبه‌دار با بدنه آلومینیومی و "
                    "دیفیوزر PMMA است؛ مناسب اجرای خطوط نور باریک در سقف و دیوار."
                ),
                meta_title="چراغ خطی توکار لبه‌دار SP NARROW | ورونا لایتینگ",
                meta_description=(
                    "چراغ خطی توکار لبه‌دار SP NARROW با برش ۳۵ میلی‌متر، توان "
                    "۲۰ وات/متر، شار ۲۰۰۰ لومن/متر، CRI بالای ۸۰ و بدنه آلومینیومی."
                ),
                image_alt="چراغ خطی توکار لبه‌دار باریک SP NARROW ورونا لایتینگ",
                guide_heading="راهنمای انتخاب چراغ خطی توکار لبه‌دار SP NARROW",
                guide_intro=(
                    "SP NARROW برای پروژه‌ای مناسب است که یک خط نور باریک و یکنواخت "
                    "می‌خواهد و حضور لبه ظریف چراغ در سطح سقف یا دیوار قابل قبول است. "
                    "پیش از سفارش، مقطع نصب و خروجی نوری را با نقشه اجرایی تطبیق دهید."
                ),
                guide_items=(
                    GuideItem(
                        "ابعاد نصب و دیتیل سقف",
                        "عرض برش ثبت‌شده برای این مدل ۳۵ میلی‌متر و عرض کلی آن حدود "
                        "۴۵ میلی‌متر است. شیار، زیرسازی، محل درایور و دسترسی سرویس را "
                        "پیش از تکمیل سقف با مقطع نهایی محصول هماهنگ کنید.",
                    ),
                    GuideItem(
                        "خروجی نور در طول خط",
                        "توان نامی ۲۰ وات و شار نوری ۲۰۰۰ لومن در هر متر است. طول کل "
                        "خط، روشنایی موردنیاز و یکنواختی را در محاسبات پروژه لحاظ کنید؛ "
                        "وات یا لومن یک متر به‌تنهایی نتیجه کل فضا را مشخص نمی‌کند.",
                    ),
                    GuideItem(
                        "انتخاب مدل لبه‌دار",
                        "لبه پیرامونی مرز نصب را می‌پوشاند و کنترل تلرانس اجرای سقف را "
                        "ساده‌تر می‌کند. اگر هدف پروژه سطح کاملاً یکپارچه و بدون قاب است، "
                        "پیش از انتخاب نهایی مدل تریم‌لس BD NARROW را نیز مقایسه کنید.",
                    ),
                ),
                faq_heading="پرسش‌های متداول درباره SP NARROW",
                faqs=(
                    FAQ(
                        "آیا SP NARROW چراغ خطی توکار لبه‌دار است؟",
                        "بله. SP NARROW با لبه ظریف طراحی شده است تا مرز شیار و سطح "
                        "نهایی سقف را پوشش دهد و اجرای توکار کنترل‌شده‌تری ایجاد کند.",
                    ),
                    FAQ(
                        "عرض برش SP NARROW چقدر است؟",
                        "عرض برش درج‌شده برای این محصول ۳۵ میلی‌متر است. ابعاد دقیق "
                        "شیار و عمق نصب را پیش از اجرا با دیتاشیت و نمونه قطعی کنترل کنید.",
                    ),
                    FAQ(
                        "توان و شار نوری SP NARROW چقدر است؟",
                        "مشخصات محصول توان ۲۰ وات در متر و شار نوری ۲۰۰۰ لومن در متر "
                        "را نشان می‌دهد. نتیجه نهایی به طول خط و طراحی روشنایی فضا وابسته است.",
                    ),
                    FAQ(
                        "SP NARROW برای چه پروژه‌هایی مناسب است؟",
                        "این مدل برای خطوط نور باریک در روشنایی عمومی فضاهای داخلی مانند "
                        "دفتر، فروشگاه و فضاهای مسکونی قابل بررسی است؛ انتخاب نهایی باید "
                        "با سطح روشنایی و جزئیات سقف همان پروژه هماهنگ شود.",
                    ),
                ),
                related_heading="مقایسه و انتخاب مسیر بعدی",
                related_links=(
                    RelatedLink(
                        "همه چراغ‌های خطی توکار",
                        "راهنمای انتخاب مدل لبه‌دار و بدون لبه و مشاهده خانواده‌های توکار.",
                        "products:child_detail",
                        (("cat_slug", "linear"), ("child_slug", "recessed")),
                    ),
                    _product_link(
                        "مقایسه با BD NARROW",
                        "مدل توکار بدون لبه را برای دیتیل یکپارچه‌تر سقف بررسی کنید.",
                        "BD",
                        "bd-narrow",
                    ),
                ),
            ),
            "en": ProductTranslation(
                keyword="narrow trimmed recessed linear light",
                name="SP NARROW Trimmed Recessed Linear Light",
                subtitle=(
                    "Narrow trimmed recessed linear light with a 35 mm cut-out and "
                    "20 W/m output for indoor general lighting"
                ),
                description=(
                    "SP NARROW is a trimmed recessed linear luminaire with an aluminium "
                    "body and PMMA diffuser, designed for narrow continuous lines in ceilings and walls."
                ),
                meta_title="SP NARROW Trimmed Recessed Linear Light | Verona",
                meta_description=(
                    "SP NARROW trimmed recessed linear light: 35 mm cut-out, 20 W/m, "
                    "2000 lm/m, CRI above 80, aluminium body and continuous PMMA diffuser."
                ),
                image_alt="SP NARROW narrow trimmed recessed linear light by Verona Lighting",
                guide_heading="How to specify the SP NARROW trimmed recessed linear light",
                guide_intro=(
                    "SP NARROW suits a project that needs a fine, continuous light line and "
                    "accepts a narrow visible trim at the ceiling or wall. Coordinate the "
                    "installation section and required output before ordering."
                ),
                guide_items=(
                    GuideItem(
                        "Installation dimensions",
                        "The recorded cut-out width is 35 mm and the overall width is approximately "
                        "45 mm. Coordinate the channel, ceiling support, driver location and future "
                        "service access against the final product section.",
                    ),
                    GuideItem(
                        "Output along the line",
                        "The stated performance is 20 W and 2000 lumens per metre. Include the "
                        "complete line length, target illuminance and uniformity in the project "
                        "calculation rather than evaluating a single metre in isolation.",
                    ),
                    GuideItem(
                        "Why select a trimmed profile",
                        "The perimeter trim covers the channel edge and manages normal ceiling "
                        "tolerances more easily. If the design requires a completely integrated "
                        "surface, compare the trimless BD NARROW before final specification.",
                    ),
                ),
                faq_heading="SP NARROW frequently asked questions",
                faqs=(
                    FAQ(
                        "Is SP NARROW a trimmed recessed linear light?",
                        "Yes. Its fine perimeter trim defines and covers the installation edge, "
                        "supporting a controlled recessed detail.",
                    ),
                    FAQ(
                        "What cut-out width does SP NARROW require?",
                        "The product information records a 35 mm cut-out. Confirm the full channel "
                        "depth and final dimensions against the current product data before construction.",
                    ),
                    FAQ(
                        "What are the stated power and lumen output?",
                        "The stated figures are 20 W/m and 2000 lm/m. The complete lighting result "
                        "depends on line length, layout and the requirements of the space.",
                    ),
                    FAQ(
                        "Where can SP NARROW be considered?",
                        "It can be considered for narrow general-lighting lines in interior offices, "
                        "retail and residential spaces, subject to the project illuminance and ceiling detail.",
                    ),
                ),
                related_heading="Compare and continue",
                related_links=(
                    RelatedLink(
                        "All recessed linear lighting",
                        "Compare trimmed and trimless systems and browse the recessed families.",
                        "products:child_detail",
                        (("cat_slug", "linear"), ("child_slug", "recessed")),
                    ),
                    _product_link(
                        "Compare BD NARROW",
                        "Review the trimless alternative for a more integrated ceiling detail.",
                        "BD",
                        "bd-narrow",
                    ),
                ),
            ),
        },
    ),
    "bd-narrow": PriorityProduct(
        category_slug="recessed",
        family_slug="BD",
        translations={
            "fa": ProductTranslation(
                keyword="چراغ خطی توکار بدون لبه",
                name="چراغ خطی توکار بدون لبه BD NARROW",
                subtitle=(
                    "چراغ خطی توکار تریم‌لس با توان ۲۵ وات در متر و شار ۲۵۰۰ "
                    "لومن در متر برای ادغام خط نور با سقف"
                ),
                description=(
                    "BD NARROW یک چراغ خطی توکار بدون لبه با بدنه آلومینیومی و "
                    "نور مستقیم یکنواخت است؛ مناسب جزئیات یکپارچه سقف کاذب."
                ),
                meta_title="چراغ خطی توکار بدون لبه BD NARROW | ورونا لایتینگ",
                meta_description=(
                    "چراغ خطی توکار بدون لبه BD NARROW با توان ۲۵ وات/متر، شار "
                    "۲۵۰۰ لومن/متر، ورودی ۲۲۰–۲۴۰ ولت، CRI بالای ۸۰ و بدنه آلومینیومی."
                ),
                image_alt="چراغ خطی توکار بدون لبه باریک BD NARROW ورونا لایتینگ",
                guide_heading="راهنمای انتخاب چراغ خطی توکار بدون لبه BD NARROW",
                guide_intro=(
                    "BD NARROW برای پروژه‌ای طراحی شده که در آن پروفیل پس از پرداخت "
                    "سقف کمترین حضور بصری را داشته باشد. کیفیت نتیجه نهایی به هماهنگی "
                    "زودهنگام پروفیل، زیرسازی و اجرای سقف وابسته است."
                ),
                guide_items=(
                    GuideItem(
                        "اجرای تریم‌لس و زیرسازی",
                        "این مدل بدون لبه است و باید پیش از پرداخت نهایی سقف به‌درستی "
                        "تراز و تثبیت شود. دیتیل مقطع، فضای پشت چراغ، محل درایور و روش "
                        "دسترسی سرویس را پیش از شروع سقف‌سازی قطعی کنید.",
                    ),
                    GuideItem(
                        "توان و خروجی نور",
                        "توان نامی ۲۵ وات و شار نوری ۲۵۰۰ لومن در هر متر است. طول خط، "
                        "دمای رنگ، CRI بالای ۸۰ و سطح روشنایی موردنیاز باید همراه با "
                        "چیدمان کل پروژه بررسی شود.",
                    ),
                    GuideItem(
                        "هماهنگی با کنترل روشنایی",
                        "اطلاعات محصول امکان بررسی گزینه DALI را نشان می‌دهد. در صورت "
                        "نیاز به کنترل یا دیمر، نوع درایور و سازگاری تجهیزات را پیش از "
                        "سفارش به‌صورت پروژه‌ای تأیید کنید.",
                    ),
                ),
                faq_heading="پرسش‌های متداول درباره BD NARROW",
                faqs=(
                    FAQ(
                        "آیا BD NARROW کاملاً بدون لبه است؟",
                        "این مدل برای دیتیل تریم‌لس طراحی شده است؛ پس از اجرای صحیح، "
                        "مرز پروفیل با پرداخت سقف یکپارچه می‌شود و قاب روی سطح دیده نمی‌شود.",
                    ),
                    FAQ(
                        "توان و شار نوری BD NARROW چقدر است؟",
                        "مشخصات محصول ۲۵ وات در متر و ۲۵۰۰ لومن در متر را اعلام می‌کند. "
                        "طول نهایی خط و محاسبات فضا برای تعیین تعداد و چیدمان ضروری است.",
                    ),
                    FAQ(
                        "BD NARROW در چه نوع سقفی نصب می‌شود؟",
                        "اطلاعات محصول به سازگاری با سقف‌های کاذب کناف و رابیتس اشاره "
                        "می‌کند. مقطع و روش نصب باید پیش از اجرا با شرایط واقعی سقف تطبیق داده شود.",
                    ),
                    FAQ(
                        "تفاوت BD NARROW و SP NARROW چیست؟",
                        "BD NARROW بدون لبه و وابسته به پرداخت دقیق سقف است؛ SP NARROW "
                        "لبه ظریفی دارد که مرز نصب را می‌پوشاند و تلرانس اجرا را بهتر مدیریت می‌کند.",
                    ),
                ),
                related_heading="مقایسه و انتخاب مسیر بعدی",
                related_links=(
                    RelatedLink(
                        "همه چراغ‌های خطی توکار",
                        "راهنمای انتخاب مدل لبه‌دار و بدون لبه و مشاهده خانواده‌های توکار.",
                        "products:child_detail",
                        (("cat_slug", "linear"), ("child_slug", "recessed")),
                    ),
                    _product_link(
                        "مقایسه با SP NARROW",
                        "مدل لبه‌دار باریک را برای اجرای کنترل‌شده‌تر بررسی کنید.",
                        "sp",
                        "sp-narrow",
                    ),
                ),
            ),
            "en": ProductTranslation(
                keyword="narrow trimless recessed linear light",
                name="BD NARROW Trimless Recessed Linear Light",
                subtitle=(
                    "Trimless recessed linear light with 25 W/m and 2500 lm/m, "
                    "designed to integrate the light line with the ceiling"
                ),
                description=(
                    "BD NARROW is a trimless recessed linear luminaire with an aluminium "
                    "body and uniform direct light for integrated suspended-ceiling details."
                ),
                meta_title="BD NARROW Trimless Recessed Linear Light | Verona",
                meta_description=(
                    "BD NARROW trimless recessed linear light: 25 W/m, 2500 lm/m, "
                    "220–240 V input, CRI above 80, aluminium construction and DALI option."
                ),
                image_alt="BD NARROW narrow trimless recessed linear light by Verona Lighting",
                guide_heading="How to specify the BD NARROW trimless recessed linear light",
                guide_intro=(
                    "BD NARROW is intended for projects where the profile should have minimal "
                    "visual presence after ceiling finishing. The final quality depends on early "
                    "coordination of the profile, support framing and finish."
                ),
                guide_items=(
                    GuideItem(
                        "Trimless preparation",
                        "The profile must be aligned and fixed before final ceiling finishing. "
                        "Confirm the section, rear space, driver position and maintenance route "
                        "before the ceiling construction begins.",
                    ),
                    GuideItem(
                        "Power and light output",
                        "The stated performance is 25 W and 2500 lumens per metre. Assess the "
                        "complete line length, colour temperature, CRI above 80 and required "
                        "illuminance as part of the full lighting layout.",
                    ),
                    GuideItem(
                        "Lighting-control coordination",
                        "The product information identifies a DALI option. Where dimming or control "
                        "is required, confirm the driver type and component compatibility for the "
                        "specific project before ordering.",
                    ),
                ),
                faq_heading="BD NARROW frequently asked questions",
                faqs=(
                    FAQ(
                        "Is BD NARROW a fully trimless product?",
                        "It is designed for a trimless detail. With correct installation and finishing, "
                        "the profile edge is integrated with the ceiling rather than visible as a frame.",
                    ),
                    FAQ(
                        "What are the stated power and lumen output?",
                        "The stated figures are 25 W/m and 2500 lm/m. Final line length and room-level "
                        "lighting calculations are still required.",
                    ),
                    FAQ(
                        "Which ceilings can use BD NARROW?",
                        "The product information references Knauf suspended and Rabitz ceilings. "
                        "The installation section must be checked against the actual ceiling build-up.",
                    ),
                    FAQ(
                        "How does BD NARROW differ from SP NARROW?",
                        "BD NARROW is trimless and relies on precise ceiling finishing. SP NARROW has "
                        "a fine trim that covers the installation edge and manages tolerances more easily.",
                    ),
                ),
                related_heading="Compare and continue",
                related_links=(
                    RelatedLink(
                        "All recessed linear lighting",
                        "Compare trimmed and trimless systems and browse the recessed families.",
                        "products:child_detail",
                        (("cat_slug", "linear"), ("child_slug", "recessed")),
                    ),
                    _product_link(
                        "Compare SP NARROW",
                        "Review the narrow trimmed alternative for a more controlled installation edge.",
                        "sp",
                        "sp-narrow",
                    ),
                ),
            ),
        },
    ),
    "magnetar-small-linear": PriorityProduct(
        category_slug="magent-small-family",
        family_slug="magnet-linear",
        translations={
            "fa": ProductTranslation(
                keyword="چراغ خطی مگنتی ۴۸ ولت ظریف",
                name="چراغ خطی مگنتی ۴۸ ولت MAGNETO SMALL LINEAR",
                subtitle=(
                    "ماژول خطی مگنتی ظریف برای ریل خانواده Small با مدل‌های "
                    "۱۰ تا ۳۰ وات و نصب مغناطیسی بدون ابزار"
                ),
                description=(
                    "MAGNETO SMALL LINEAR ماژول چراغ خطی مگنتی ۴۸ ولت برای ریل "
                    "Small است؛ مناسب نور عمومی یکنواخت در سیستم روشنایی ماژولار."
                ),
                meta_title="چراغ خطی مگنتی ۴۸ ولت Small Linear | ورونا لایتینگ",
                meta_description=(
                    "چراغ خطی مگنتی ۴۸ ولت MAGNETO SMALL LINEAR در مدل‌های "
                    "۱۰ تا ۳۰ وات و ۱۲۰۰ تا ۳۰۰۰ لومن، با مقطع ۲۲×۴۲ میلی‌متر."
                ),
                image_alt="چراغ خطی مگنتی ۴۸ ولت MAGNETO SMALL LINEAR",
                guide_heading="راهنمای انتخاب MAGNETO SMALL LINEAR",
                guide_intro=(
                    "این محصول ماژول خطی خانواده Magnet Small است و برای ساخت نور "
                    "عمومی یکنواخت روی ریل ۴۸ ولت همان سیستم استفاده می‌شود. پیش از "
                    "سفارش، طول، توان و سازگاری همه اجزا را در یک خانواده کنترل کنید."
                ),
                guide_items=(
                    GuideItem(
                        "انتخاب مدل بر اساس طول و خروجی",
                        "مدل‌های ثبت‌شده بازه ۱۰، ۱۵، ۲۰ و ۳۰ وات با شار نوری ۱۲۰۰ تا "
                        "۳۰۰۰ لومن را پوشش می‌دهند. طول و خروجی هر ماژول را بر اساس "
                        "چیدمان ریل و سطح روشنایی موردنیاز انتخاب کنید.",
                    ),
                    GuideItem(
                        "سازگاری با ریل Small",
                        "این ماژول برای خانواده Magnet Small طراحی شده و با اتصال "
                        "مغناطیسی روی ریل ۴۸ ولت نصب می‌شود. ریل، منبع تغذیه و اتصال‌ها "
                        "باید از اجزای سازگار همین سیستم انتخاب شوند.",
                    ),
                    GuideItem(
                        "مقیاس ظریف‌تر در معماری",
                        "مقطع مدل‌های ثبت‌شده حدود ۲۲×۴۲ میلی‌متر است و در مقایسه با "
                        "خانواده Large حضور بصری ظریف‌تری دارد. انتخاب را با ارتفاع سقف، "
                        "تناسب فضا و تعداد ماژول‌های موردنیاز هماهنگ کنید.",
                    ),
                ),
                faq_heading="پرسش‌های متداول درباره MAGNETO SMALL LINEAR",
                faqs=(
                    FAQ(
                        "MAGNETO SMALL LINEAR روی چه ریلی نصب می‌شود؟",
                        "این ماژول برای ریل ۴۸ ولت خانواده Magnet Small طراحی شده است. "
                        "پیش از سفارش، سازگاری ریل، منبع تغذیه و قطعات اتصال را تأیید کنید.",
                    ),
                    FAQ(
                        "چه توان‌هایی برای این چراغ خطی مگنتی وجود دارد؟",
                        "مدل‌های ثبت‌شده شامل ۱۰، ۱۵، ۲۰ و ۳۰ وات هستند و شار آن‌ها از "
                        "۱۲۰۰ تا ۳۰۰۰ لومن متغیر است.",
                    ),
                    FAQ(
                        "تفاوت Small Linear و Large Linear چیست؟",
                        "Small Linear مقطع ظریف‌تری دارد؛ مدل‌های Large در مقطع بزرگ‌تر "
                        "۳۵×۷۰ میلی‌متر ارائه شده‌اند. هر ماژول فقط باید با خانواده ریل سازگار خود استفاده شود.",
                    ),
                    FAQ(
                        "آیا جای ماژول روی ریل قابل تغییر است؟",
                        "اتصال مغناطیسی جابه‌جایی و بازچینی ماژول را در محدوده طراحی "
                        "سیستم ساده‌تر می‌کند؛ ظرفیت منبع تغذیه و مسیر ریل همچنان باید رعایت شود.",
                    ),
                ),
                related_heading="سیستم سازگار و گزینه مقایسه",
                related_links=(
                    RelatedLink(
                        "راهنمای سیستم چراغ مگنتی",
                        "خانواده‌های ریل، روش‌های نصب و ماژول‌های مگنتی را مقایسه کنید.",
                        "products:category_detail",
                        (("cat_slug", "low-voltage-magneto"),),
                    ),
                    _product_link(
                        "مقایسه با MAGNETO LARGE LINEAR",
                        "ماژول خطی خانواده Large را برای مقیاس و مقطع بزرگ‌تر بررسی کنید.",
                        "magnet-linear-large",
                        "magnetar-large-linear",
                    ),
                ),
            ),
            "en": ProductTranslation(
                keyword="slim 48V magnetic linear light",
                name="MAGNETO SMALL LINEAR 48V Magnetic Light",
                subtitle=(
                    "Slim linear module for the Magnet Small track family, with "
                    "10–30 W models and tool-free magnetic mounting"
                ),
                description=(
                    "MAGNETO SMALL LINEAR is a 48V magnetic linear module for the Small "
                    "track family, designed to provide uniform general light in a modular system."
                ),
                meta_title="MAGNETO SMALL LINEAR 48V Magnetic Light | Verona",
                meta_description=(
                    "MAGNETO SMALL LINEAR 48V magnetic light in 10–30 W and "
                    "1200–3000 lm models, with a 22×42 mm section and tool-free track mounting."
                ),
                image_alt="MAGNETO SMALL LINEAR slim 48V magnetic linear light",
                guide_heading="How to select MAGNETO SMALL LINEAR",
                guide_intro=(
                    "This is the linear module for the Magnet Small family, intended to provide "
                    "uniform general light on its compatible 48V track. Confirm module length, "
                    "output and system compatibility before ordering."
                ),
                guide_items=(
                    GuideItem(
                        "Model length and output",
                        "The recorded variants cover 10, 15, 20 and 30 W, with outputs from "
                        "1200 to 3000 lumens. Select the module length and output for the track "
                        "layout and the illuminance required in the space.",
                    ),
                    GuideItem(
                        "Small-family compatibility",
                        "The module is designed for the Magnet Small 48V track and uses magnetic "
                        "mounting. Track, power supply and connectors must all be selected as "
                        "compatible components from the same system.",
                    ),
                    GuideItem(
                        "A finer architectural scale",
                        "The recorded section is approximately 22×42 mm, giving it a finer visual "
                        "scale than the Large family. Coordinate the choice with ceiling height, "
                        "room proportions and the required number of modules.",
                    ),
                ),
                faq_heading="MAGNETO SMALL LINEAR frequently asked questions",
                faqs=(
                    FAQ(
                        "Which track accepts MAGNETO SMALL LINEAR?",
                        "It is designed for the 48V Magnet Small track family. Confirm track, "
                        "power supply and connector compatibility before ordering.",
                    ),
                    FAQ(
                        "Which power options are recorded for this module?",
                        "The recorded variants are 10, 15, 20 and 30 W, with outputs ranging "
                        "from 1200 to 3000 lumens.",
                    ),
                    FAQ(
                        "How does Small Linear differ from Large Linear?",
                        "Small Linear has a finer section. The Large variants use a larger "
                        "35×70 mm section, and each module must remain within its compatible track family.",
                    ),
                    FAQ(
                        "Can the module position be changed on the track?",
                        "Magnetic mounting simplifies repositioning within the designed system. "
                        "The track route and power-supply capacity must still be respected.",
                    ),
                ),
                related_heading="Compatible system and comparison",
                related_links=(
                    RelatedLink(
                        "Magnetic track lighting guide",
                        "Compare track families, mounting methods and magnetic light modules.",
                        "products:category_detail",
                        (("cat_slug", "low-voltage-magneto"),),
                    ),
                    _product_link(
                        "Compare MAGNETO LARGE LINEAR",
                        "Review the Large-family linear module for a larger architectural scale.",
                        "magnet-linear-large",
                        "magnetar-large-linear",
                    ),
                ),
            ),
        },
    ),
    "magnetar-large-linear": PriorityProduct(
        category_slug="magent-large4cm-family",
        family_slug="magnet-linear",
        translations={
            "fa": ProductTranslation(
                keyword="چراغ خطی مگنتی ۴۸ ولت بزرگ",
                name="چراغ خطی مگنتی ۴۸ ولت MAGNETO LARGE LINEAR",
                subtitle=(
                    "ماژول خطی مگنتی خانواده Large با مدل‌های ۱۲ تا ۳۰ وات، "
                    "شار ۱۲۰۰ تا ۳۰۰۰ لومن و نصب بدون ابزار"
                ),
                description=(
                    "MAGNETO LARGE LINEAR ماژول چراغ خطی مگنتی ۴۸ ولت برای ریل "
                    "Large است؛ مناسب ایجاد نور عمومی یکنواخت در مقیاس معماری بزرگ‌تر."
                ),
                meta_title="چراغ خطی مگنتی ۴۸ ولت Large Linear | ورونا لایتینگ",
                meta_description=(
                    "چراغ خطی مگنتی ۴۸ ولت MAGNETO LARGE LINEAR در مدل‌های "
                    "۱۲ تا ۳۰ وات و ۱۲۰۰ تا ۳۰۰۰ لومن، با مقطع ۳۵×۷۰ میلی‌متر."
                ),
                image_alt="چراغ خطی مگنتی ۴۸ ولت MAGNETO LARGE LINEAR",
                guide_heading="راهنمای انتخاب MAGNETO LARGE LINEAR",
                guide_intro=(
                    "این ماژول خطی برای ریل خانواده Magnet Large طراحی شده و نور عمومی "
                    "پیوسته‌ای در سیستم مگنتی ۴۸ ولت ایجاد می‌کند. مقیاس بزرگ‌تر مقطع "
                    "باید با تناسبات فضا و سایر اجزای ریل هماهنگ شود."
                ),
                guide_items=(
                    GuideItem(
                        "چهار طول و خروجی نوری",
                        "مدل‌های ثبت‌شده ۱۲، ۱۸، ۲۴ و ۳۰ وات با شار نوری ۱۲۰۰، ۱۸۰۰، "
                        "۲۴۰۰ و ۳۰۰۰ لومن هستند. ترکیب طول‌ها را بر اساس مسیر ریل و "
                        "سطح روشنایی موردنیاز پروژه انتخاب کنید.",
                    ),
                    GuideItem(
                        "ریل و تغذیه ۴۸ ولت سازگار",
                        "MAGNETO LARGE LINEAR باید روی ریل و تجهیزات خانواده Large "
                        "استفاده شود. طول مسیر، تعداد ماژول‌ها، محل تغذیه و ظرفیت منبع "
                        "۴۸ ولت را پیش از سفارش روی نقشه کنترل کنید.",
                    ),
                    GuideItem(
                        "مقطع و حضور بصری بزرگ‌تر",
                        "مقطع ثبت‌شده برای مدل‌های این خانواده حدود ۳۵×۷۰ میلی‌متر است. "
                        "این ابعاد نسبت به Small حضور معماری قوی‌تری ایجاد می‌کند و برای "
                        "فضاهایی که خط ریل خواناتر است قابل بررسی است.",
                    ),
                ),
                faq_heading="پرسش‌های متداول درباره MAGNETO LARGE LINEAR",
                faqs=(
                    FAQ(
                        "MAGNETO LARGE LINEAR با چه ولتاژی کار می‌کند؟",
                        "این ماژول برای سیستم ریل مگنتی ۴۸ ولت خانواده Large طراحی شده است. "
                        "منبع تغذیه و همه اتصالات باید با همین سیستم سازگار باشند.",
                    ),
                    FAQ(
                        "چه مدل‌هایی برای Large Linear ثبت شده است؟",
                        "چهار مدل ۱۲، ۱۸، ۲۴ و ۳۰ وات با خروجی ۱۲۰۰ تا ۳۰۰۰ لومن و "
                        "طول‌های متناظر ۴۰ تا ۱۰۰ سانتی‌متر ثبت شده‌اند.",
                    ),
                    FAQ(
                        "تفاوت Large Linear و Small Linear چیست؟",
                        "Large Linear مقطع حدود ۳۵×۷۰ میلی‌متر و حضور بصری بزرگ‌تری دارد؛ "
                        "Small Linear ظریف‌تر است. این دو متعلق به خانواده‌های ریل متفاوت هستند.",
                    ),
                    FAQ(
                        "این ماژول برای نور عمومی مناسب است؟",
                        "ماهیت خطی و دیفیوزر آن برای نور پایه یکنواخت قابل بررسی است. "
                        "برای نور تأکیدی می‌توان ماژول‌های اسپات سازگار را در همان سیستم ترکیب کرد.",
                    ),
                ),
                related_heading="سیستم سازگار و گزینه مقایسه",
                related_links=(
                    RelatedLink(
                        "راهنمای سیستم چراغ مگنتی",
                        "خانواده‌های ریل، روش‌های نصب و ماژول‌های مگنتی را مقایسه کنید.",
                        "products:category_detail",
                        (("cat_slug", "low-voltage-magneto"),),
                    ),
                    _product_link(
                        "مقایسه با MAGNETO SMALL LINEAR",
                        "ماژول خطی خانواده Small را برای مقیاس ظریف‌تر بررسی کنید.",
                        "magnet-linear-small",
                        "magnetar-small-linear",
                    ),
                ),
            ),
            "en": ProductTranslation(
                keyword="48V large magnetic linear light",
                name="MAGNETO LARGE LINEAR 48V Magnetic Light",
                subtitle=(
                    "Large-family magnetic linear module with 12–30 W models, "
                    "1200–3000 lm output and tool-free mounting"
                ),
                description=(
                    "MAGNETO LARGE LINEAR is a 48V magnetic linear module for the Large "
                    "track family, providing uniform general light at a larger architectural scale."
                ),
                meta_title="MAGNETO LARGE LINEAR 48V Magnetic Light | Verona",
                meta_description=(
                    "MAGNETO LARGE LINEAR 48V magnetic light in 12–30 W and "
                    "1200–3000 lm models, with a 35×70 mm section and tool-free track mounting."
                ),
                image_alt="MAGNETO LARGE LINEAR 48V magnetic linear light",
                guide_heading="How to select MAGNETO LARGE LINEAR",
                guide_intro=(
                    "This linear module is designed for the Magnet Large track family and provides "
                    "continuous general light within a 48V magnetic system. Its larger section should "
                    "be coordinated with the room scale and the other track components."
                ),
                guide_items=(
                    GuideItem(
                        "Four lengths and outputs",
                        "The recorded variants are 12, 18, 24 and 30 W, delivering 1200, 1800, "
                        "2400 and 3000 lumens. Combine the lengths according to the track route "
                        "and the project’s required illuminance.",
                    ),
                    GuideItem(
                        "Compatible 48V track and power",
                        "MAGNETO LARGE LINEAR must be used with Large-family track and components. "
                        "Confirm route length, module quantity, feed location and 48V power-supply "
                        "capacity on the coordinated plan.",
                    ),
                    GuideItem(
                        "A larger visual scale",
                        "The recorded section is approximately 35×70 mm. This is larger than the "
                        "Small family and creates a stronger architectural presence where a more "
                        "legible track line is appropriate.",
                    ),
                ),
                faq_heading="MAGNETO LARGE LINEAR frequently asked questions",
                faqs=(
                    FAQ(
                        "What voltage does MAGNETO LARGE LINEAR use?",
                        "It is designed for the 48V Magnet Large track family. The power supply "
                        "and every connector must be compatible with that system.",
                    ),
                    FAQ(
                        "Which Large Linear variants are recorded?",
                        "Four variants are recorded: 12, 18, 24 and 30 W, with 1200–3000 lumen "
                        "outputs and corresponding lengths from 40 to 100 cm.",
                    ),
                    FAQ(
                        "How does Large Linear differ from Small Linear?",
                        "Large Linear uses an approximately 35×70 mm section and has a stronger "
                        "visual presence. Small Linear is finer, and the two belong to different track families.",
                    ),
                    FAQ(
                        "Can this module provide general lighting?",
                        "Its linear form and diffuser can support uniform base light. Compatible "
                        "spot modules may be combined in the same system where accent light is required.",
                    ),
                ),
                related_heading="Compatible system and comparison",
                related_links=(
                    RelatedLink(
                        "Magnetic track lighting guide",
                        "Compare track families, mounting methods and magnetic light modules.",
                        "products:category_detail",
                        (("cat_slug", "low-voltage-magneto"),),
                    ),
                    _product_link(
                        "Compare MAGNETO SMALL LINEAR",
                        "Review the Small-family linear module for a finer architectural scale.",
                        "magnet-linear-small",
                        "magnetar-small-linear",
                    ),
                ),
            ),
        },
    ),
}


def validate_priority_product_content():
    expected = {
        "sp-narrow",
        "bd-narrow",
        "magnetar-small-linear",
        "magnetar-large-linear",
    }
    if set(PRIORITY_PRODUCT_CONTENT) != expected:
        raise ValueError("The Step 4 priority-product set is incomplete.")

    keywords = {"fa": set(), "en": set()}
    for slug, campaign in PRIORITY_PRODUCT_CONTENT.items():
        if set(campaign.translations) != {"fa", "en"}:
            raise ValueError(f"{slug} must provide Persian and English content.")
        for language, content in campaign.translations.items():
            if not 35 <= len(content.meta_title) <= 65:
                raise ValueError(f"{slug}/{language} meta title length is invalid.")
            if not 110 <= len(content.meta_description) <= 165:
                raise ValueError(f"{slug}/{language} meta description length is invalid.")
            keyword_terms = content.keyword.casefold().split()
            campaign_text = (
                f"{content.name} {content.subtitle} {content.description} "
                f"{content.meta_title} {content.meta_description}"
            ).casefold()
            if not all(term in campaign_text for term in keyword_terms):
                raise ValueError(f"{slug}/{language} is missing its assigned keyword.")
            if len(content.guide_items) != 3 or len(content.faqs) != 4:
                raise ValueError(f"{slug}/{language} must have three guide items and four FAQs.")
            if content.keyword.casefold() in keywords[language]:
                raise ValueError(f"{slug}/{language} duplicates a product keyword.")
            keywords[language].add(content.keyword.casefold())


def build_priority_product_context(slug, language_code):
    campaign = PRIORITY_PRODUCT_CONTENT.get(slug)
    if not campaign:
        return None
    language = "fa" if language_code == "fa" else "en"
    content = campaign.translations[language]
    return {
        "content": content,
        "related_links": [
            {
                "label": link.label,
                "description": link.description,
                "url": reverse(link.route_name, kwargs=dict(link.route_kwargs)),
            }
            for link in content.related_links
        ],
    }
