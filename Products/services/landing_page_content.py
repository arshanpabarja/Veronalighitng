from dataclasses import dataclass

from django.urls import reverse


@dataclass(frozen=True)
class ContentItem:
    title: str
    body: str


@dataclass(frozen=True)
class RelatedLink:
    label: str
    description: str
    route_name: str
    route_kwargs: tuple[tuple[str, str], ...]


@dataclass(frozen=True)
class FAQ:
    question: str
    answer: str


@dataclass(frozen=True)
class LandingPageContent:
    primary_keyword: str
    eyebrow: str
    heading: str
    lead: str
    intro_paragraphs: tuple[str, ...]
    selection_heading: str
    selection_intro: str
    selection_items: tuple[ContentItem, ...]
    comparison_heading: str
    comparison_paragraphs: tuple[str, ...]
    related_heading: str
    related_intro: str
    related_links: tuple[RelatedLink, ...]
    faq_heading: str
    faqs: tuple[FAQ, ...]


LANDING_PAGE_CONTENT = {
    "recessed-linear": {
        "fa": LandingPageContent(
            primary_keyword="چراغ خطی توکار",
            eyebrow="راهنمای انتخاب و اجرای پروژه",
            heading="راهنمای انتخاب چراغ خطی توکار برای سقف و جزئیات معماری",
            lead=(
                "انتخاب چراغ خطی توکار فقط انتخاب یک چراغ نیست؛ پروفیل، ابعاد شیار، "
                "زیرسازی سقف، درایور و مسیر کابل باید پیش از اجرای نهایی با یکدیگر "
                "هماهنگ شوند. این راهنما خانواده‌های توکار ورونا را برای یک انتخاب "
                "دقیق‌تر و قابل اجرا مقایسه می‌کند."
            ),
            intro_paragraphs=(
                "در یک پروژه حرفه‌ای، عرض خط نور، نوع لبه، عمق نصب، محل تجهیزات و "
                "دسترسی سرویس باید پیش از بسته‌شدن سقف مشخص باشد. تصمیم دیرهنگام ممکن "
                "است باعث تغییر شیار، اصلاح کناف یا محدودشدن انتخاب توان و اپتیک شود. "
                "به همین دلیل بهتر است دیتیل معماری و مشخصات فنی چراغ هم‌زمان بررسی شوند.",
                "SP LINEO و BD LINEO دو خانواده اصلی چراغ خطی توکار ورونا هستند. هر دو "
                "برای ساخت یک خط نور منظم طراحی شده‌اند، اما جزئیات اتصال آن‌ها به سقف "
                "یکسان نیست. انتخاب نهایی باید بر اساس نوع سقف، کیفیت لبه مورد انتظار، "
                "ابعاد واقعی محل نصب و اطلاعات درج‌شده در صفحه هر محصول انجام شود.",
            ),
            selection_heading="برای انتخاب چراغ خطی توکار چه مواردی را بررسی کنیم؟",
            selection_intro=(
                "پیش از سفارش، این چهار موضوع را با معمار، طراح روشنایی و مجری سقف "
                "نهایی کنید تا محصول انتخاب‌شده با دیتیل اجرایی پروژه سازگار باشد."
            ),
            selection_items=(
                ContentItem(
                    "لبه‌دار یا بدون لبه",
                    "مدل لبه‌دار قاب باریکی روی سطح سقف نشان می‌دهد و معمولاً اجرای "
                    "قابل‌کنترل‌تری دارد. مدل بدون لبه پس از تکمیل سقف یکپارچه‌تر دیده "
                    "می‌شود، اما به زیرسازی دقیق، تراز مناسب و اجرای تمیز نیاز دارد.",
                ),
                ContentItem(
                    "ابعاد شیار و زیرسازی",
                    "عرض و عمق شیار را از روی دیتاشیت همان خانواده تعیین کنید؛ اندازه‌گیری "
                    "صرفاً از روی تصویر یا نام محصول کافی نیست. فضای پروفیل، اتصالات، "
                    "کابل و تلرانس اجرای سقف نیز باید در دیتیل در نظر گرفته شود.",
                ),
                ContentItem(
                    "توان و خروجی نور",
                    "وات به‌تنهایی کیفیت یا مقدار نور مناسب را مشخص نمی‌کند. شار نوری، "
                    "دمای رنگ، CRI، اپتیک، طول خط و روشنایی موردنیاز فضا را کنار هم "
                    "بررسی کنید و در پروژه‌های حساس از محاسبات روشنایی کمک بگیرید.",
                ),
                ContentItem(
                    "دسترسی به درایور و نگهداری",
                    "محل درایور باید از نظر تهویه، فاصله کابل و دسترسی بعدی مشخص باشد. "
                    "پیش از اجرا تعیین کنید که سرویس تجهیزات از داخل چراغ، دریچه بازدید "
                    "یا فضای مجاور انجام می‌شود تا نگهداری به تخریب سقف نیاز نداشته باشد.",
                ),
            ),
            comparison_heading="تفاوت خانواده‌های SP LINEO و BD LINEO",
            comparison_paragraphs=(
                "خانواده SP LINEO برای دیتیلی مناسب است که حضور یک لبه ظریف در پیرامون "
                "پروفیل پذیرفته شده باشد. این لبه مرز نصب را خواناتر می‌کند و می‌تواند "
                "تلرانس‌های معمول اجرای سقف را بهتر مدیریت کند. برای ابعاد، توان‌ها و "
                "گزینه‌های نوری موجود باید مدل موردنظر را در صفحه خانواده بررسی کنید.",
                "خانواده BD LINEO برای ظاهر بدون لبه و ادغام خط نور با سطح سقف انتخاب "
                "می‌شود. نتیجه نهایی مینیمال‌تر است، اما کیفیت آن مستقیماً به دقت "
                "زیرسازی، تراز پروفیل و پرداخت نهایی وابسته است. هماهنگی زودهنگام میان "
                "تأمین‌کننده، مجری کناف و تیم معماری در این روش اهمیت بیشتری دارد.",
                "هیچ‌کدام از این دو خانواده در همه پروژه‌ها برتر نیست. SP LINEO معمولاً "
                "برای اجرای ساده‌تر و لبه مشخص مناسب‌تر است؛ BD LINEO زمانی ارزش بیشتری "
                "دارد که دیتیل بدون لبه بخشی از زبان معماری باشد. انتخاب را پس از مشاهده "
                "نقشه سقف، مقطع اجرایی و صفحه فنی محصول نهایی کنید.",
            ),
            related_heading="خانواده‌های چراغ خطی توکار",
            related_intro=(
                "برای دیدن مدل‌ها، تصاویر، مشخصات فنی و فایل‌های هر سیستم وارد صفحه "
                "خانواده شوید. موجودبودن گزینه‌ها را از اطلاعات همان محصول بررسی کنید."
            ),
            related_links=(
                RelatedLink(
                    "SP LINEO",
                    "چراغ خطی توکار لبه‌دار برای اجرای دقیق و کنترل‌شده در سقف.",
                    "products:family_detail",
                    (("cat_slug", "linear"), ("child_slug", "recessed"), ("family_slug", "sp")),
                ),
                RelatedLink(
                    "BD LINEO",
                    "چراغ خطی توکار بدون لبه برای یکپارچگی بیشتر با سطح معماری.",
                    "products:family_detail",
                    (("cat_slug", "linear"), ("child_slug", "recessed"), ("family_slug", "BD")),
                ),
            ),
            faq_heading="پرسش‌های متداول درباره چراغ خطی توکار",
            faqs=(
                FAQ(
                    "تفاوت چراغ خطی توکار لبه‌دار و بدون لبه چیست؟",
                    "مدل لبه‌دار پس از نصب یک قاب ظریف در اطراف پروفیل دارد و معمولاً "
                    "تلرانس اجرا را بهتر پوشش می‌دهد. مدل بدون لبه با پرداخت سقف یکپارچه "
                    "می‌شود، اما زیرسازی و اجرای دقیق‌تری می‌خواهد.",
                ),
                FAQ(
                    "ابعاد شیار چراغ خطی توکار را چه زمانی باید مشخص کرد؟",
                    "ابعاد شیار و عمق نصب باید پیش از اجرای نهایی سقف و بر اساس دیتاشیت "
                    "مدل قطعی شود. هم‌زمان فضای درایور، کابل، اتصالات و مسیر دسترسی برای "
                    "سرویس را نیز در نقشه اجرایی مشخص کنید.",
                ),
                FAQ(
                    "آیا توان چراغ برای انتخاب مدل مناسب کافی است؟",
                    "خیر. علاوه بر توان باید شار نوری، طول خط، دمای رنگ، شاخص نمود رنگ، "
                    "اپتیک و روشنایی موردنیاز فضا بررسی شود. توان مصرفی به‌تنهایی نتیجه "
                    "نوری پروژه را پیش‌بینی نمی‌کند.",
                ),
                FAQ(
                    "برای پروژه SP LINEO بهتر است یا BD LINEO؟",
                    "اگر اجرای لبه‌دار و کنترل تلرانس سقف اولویت دارد SP LINEO گزینه "
                    "مناسب‌تری است. اگر ظاهر کاملاً یکپارچه و بدون لبه می‌خواهید و امکان "
                    "زیرسازی دقیق وجود دارد، BD LINEO را بررسی کنید.",
                ),
            ),
        ),
        "en": LandingPageContent(
            primary_keyword="recessed linear lighting",
            eyebrow="Selection and installation guide",
            heading="How to select recessed linear lighting for architectural ceilings",
            lead=(
                "Selecting recessed linear lighting is not only about choosing a luminaire. "
                "The profile, channel dimensions, ceiling build-up, driver position and cable "
                "route must be coordinated before the ceiling is closed. This guide compares "
                "Verona’s recessed families so the final specification is both architectural "
                "and practical."
            ),
            intro_paragraphs=(
                "A reliable specification defines the visible line width, trim condition, "
                "installation depth, equipment location and maintenance access at an early "
                "stage. A late decision may require changes to the ceiling channel or restrict "
                "the available output and optical options. Review the architectural detail and "
                "the luminaire data together rather than treating them as separate decisions.",
                "SP LINEO and BD LINEO are Verona’s principal recessed linear families. Both "
                "create a controlled continuous line, but they meet the ceiling differently. "
                "The correct choice depends on the ceiling construction, the desired edge "
                "finish, the actual installation space and the technical information shown on "
                "the selected product page.",
            ),
            selection_heading="What should you check before selecting recessed linear lighting?",
            selection_intro=(
                "Confirm these four points with the architect, lighting designer and ceiling "
                "contractor before ordering, so the selected family matches the construction detail."
            ),
            selection_items=(
                ContentItem(
                    "Trimmed or trimless finish",
                    "A trimmed profile leaves a narrow, deliberate edge at the ceiling and is "
                    "generally more tolerant of normal finishing variation. A trimless profile "
                    "offers a more integrated appearance but needs accurate framing, alignment "
                    "and a carefully finished ceiling surface.",
                ),
                ContentItem(
                    "Channel size and ceiling build-up",
                    "Set the channel width and depth from the data for the exact family; a product "
                    "photo or family name is not a construction dimension. Allow for the profile, "
                    "connectors, cabling and installation tolerances in the coordinated section.",
                ),
                ContentItem(
                    "Output and lighting quality",
                    "Wattage alone does not define a suitable result. Compare delivered lumens, "
                    "colour temperature, CRI, optics, line length and the illuminance required "
                    "for the space. Use a lighting calculation where uniformity or task levels "
                    "are important.",
                ),
                ContentItem(
                    "Driver access and maintenance",
                    "Define the driver location with adequate ventilation, cable distance and "
                    "future access. Decide whether service will be possible through the luminaire, "
                    "an access panel or an adjacent void so routine maintenance does not require "
                    "damage to the finished ceiling.",
                ),
            ),
            comparison_heading="SP LINEO compared with BD LINEO",
            comparison_paragraphs=(
                "SP LINEO suits a detail where a fine visible trim around the profile is acceptable. "
                "The edge clearly defines the installation and can manage normal ceiling tolerances "
                "more easily. Available sizes, outputs and light options should be confirmed on the "
                "relevant family and product pages.",
                "BD LINEO is intended for a trimless detail in which the line of light is integrated "
                "with the ceiling plane. The result can look more minimal, but it depends on accurate "
                "framing, profile alignment and final finishing. Early coordination between the "
                "supplier, ceiling contractor and architect is especially important.",
                "Neither family is universally better. SP LINEO is often the practical choice for a "
                "defined edge and controlled installation; BD LINEO is appropriate when a trimless "
                "detail is part of the architectural concept. Confirm the choice against the reflected "
                "ceiling plan, construction section and final product data.",
            ),
            related_heading="Explore the recessed linear families",
            related_intro=(
                "Open each family to review its models, images, technical data and available files. "
                "Confirm the precise options from the selected product rather than the overview alone."
            ),
            related_links=(
                RelatedLink(
                    "SP LINEO",
                    "Trimmed recessed linear lighting for a precise, controlled ceiling installation.",
                    "products:family_detail",
                    (("cat_slug", "linear"), ("child_slug", "recessed"), ("family_slug", "sp")),
                ),
                RelatedLink(
                    "BD LINEO",
                    "Trimless recessed linear lighting for closer integration with the ceiling plane.",
                    "products:family_detail",
                    (("cat_slug", "linear"), ("child_slug", "recessed"), ("family_slug", "BD")),
                ),
            ),
            faq_heading="Frequently asked questions about recessed linear lighting",
            faqs=(
                FAQ(
                    "What is the difference between trimmed and trimless recessed linear lighting?",
                    "A trimmed system leaves a fine frame around the profile and accommodates normal "
                    "finishing tolerances more easily. A trimless system is finished into the ceiling "
                    "for an integrated appearance, but requires more accurate preparation and finishing.",
                ),
                FAQ(
                    "When should the recessed channel dimensions be confirmed?",
                    "Confirm the channel width and installation depth from the final model’s data before "
                    "the ceiling is closed. The coordinated detail should also show the driver, cabling, "
                    "connectors and the intended maintenance access.",
                ),
                FAQ(
                    "Is wattage enough to choose a recessed linear luminaire?",
                    "No. Review delivered lumens, line length, colour temperature, CRI, optics and the "
                    "required illuminance as a group. Wattage describes electrical consumption and does "
                    "not by itself predict the visual result.",
                ),
                FAQ(
                    "Should I specify SP LINEO or BD LINEO?",
                    "Consider SP LINEO when a fine trim is acceptable and installation tolerance is "
                    "important. Consider BD LINEO when the design requires a trimless appearance and "
                    "the project can provide the accurate framing and finishing that it needs.",
                ),
            ),
        ),
    },
    "magnetic-track": {
        "fa": LandingPageContent(
            primary_keyword="چراغ مگنتی",
            eyebrow="راهنمای انتخاب سیستم مگنتی",
            heading="راهنمای انتخاب چراغ مگنتی و ریل مگنتی برای پروژه",
            lead=(
                "چراغ مگنتی یک سیستم ماژولار است، نه یک چراغ مستقل. انتخاب درست از "
                "خانواده ریل، روش نصب و مسیر تغذیه شروع می‌شود و سپس به ترکیب ماژول‌های "
                "نوری می‌رسد. این راهنما به شما کمک می‌کند اجزای سیستم را هماهنگ انتخاب کنید."
            ),
            intro_paragraphs=(
                "ابعاد ریل، خانواده محصول، نوع نصب، منبع تغذیه، اتصال‌ها و سازگاری "
                "ماژول‌ها باید یک مجموعه واحد دیده شوند. انتخاب یک چراغ جذاب بدون بررسی "
                "ریل و تجهیزات سازگار ممکن است در مرحله اجرا به محدودیت اتصال، کمبود "
                "فضا یا تغییر ناخواسته در طرح سقف منجر شود.",
                "مجموعه مگنتی ورونا شامل خانواده‌های Small، Large، Curve، Belt و Flexi "
                "است و در زیرگروه‌های آن می‌توان ماژول‌های خطی، اسپات، آویز و پنلی را "
                "بررسی کرد. هر خانواده زبان طراحی و الزامات اجرایی خود را دارد؛ بنابراین "
                "ابتدا سیستم مناسب پروژه را انتخاب کنید و بعد مدل‌های نور را در همان سیستم بچینید.",
            ),
            selection_heading="پیش از خرید چراغ مگنتی چه تصمیم‌هایی لازم است؟",
            selection_intro=(
                "این چهار تصمیم، ساختار سیستم مگنتی را مشخص می‌کنند و باید پیش از نهایی‌شدن "
                "نقشه سقف و سفارش تجهیزات با تیم طراحی و اجرا هماهنگ شوند."
            ),
            selection_items=(
                ContentItem(
                    "انتخاب خانواده و ابعاد ریل",
                    "Small و Large فقط دو نام ظاهری نیستند؛ ابعاد، مقیاس بصری و تجهیزات "
                    "سازگار آن‌ها متفاوت است. همه ریل‌ها، اتصال‌ها و چراغ‌ها را از یک "
                    "خانواده سازگار انتخاب کنید و برای ترکیب سیستم‌ها فرض سازگاری نداشته باشید.",
                ),
                ContentItem(
                    "توکار، روکار یا آویز",
                    "ریل توکار به شیار و زیرسازی هماهنگ نیاز دارد، ریل روکار اجرای مستقیم‌تری "
                    "روی سطح فراهم می‌کند و ریل آویز برای سقف بلند یا ایجاد یک خط معماری "
                    "معلق مناسب است. روش نصب را پیش از تعیین مقطع و طول ریل قطعی کنید.",
                ),
                ContentItem(
                    "ترکیب ماژول‌های نور",
                    "ماژول خطی برای نور عمومی، اسپات برای تأکید، آویز برای نور نزدیک‌تر و "
                    "پنل برای سطح نور گسترده‌تر قابل بررسی است. ترکیب مناسب باید بر اساس "
                    "کاربری فضا، چیدمان، خیرگی و سناریوهای روشنایی انتخاب شود.",
                ),
                ContentItem(
                    "مسیر، اتصال‌ها و توسعه آینده",
                    "طول شاخه‌ها، گوشه‌ها، محل ورودی برق، ظرفیت منبع تغذیه و نقاط اتصال را "
                    "روی نقشه مشخص کنید. اگر تغییر چیدمان آینده مهم است، فضای قابل استفاده "
                    "روی ریل و امکان افزودن ماژول را از ابتدا در طراحی نگه دارید.",
                ),
            ),
            comparison_heading="کدام خانواده چراغ مگنتی برای پروژه مناسب است؟",
            comparison_paragraphs=(
                "خانواده Small برای مقیاس ظریف‌تر و حضور بصری کم‌تر ریل مناسب است؛ خانواده "
                "Large بیان قوی‌تر و ابعاد بزرگ‌تری دارد. انتخاب میان آن‌ها باید با تناسبات "
                "فضا، ارتفاع سقف، نوع ماژول‌های موردنیاز و مشخصات فنی همان خانواده انجام شود.",
                "Curve برای مسیرهای منحنی و بیان نرم‌تر، Belt برای یک خط منعطف با شخصیت "
                "متفاوت و Flexi برای سناریوهایی که انعطاف‌پذیری فرم اهمیت دارد قابل بررسی "
                "است. این خانواده‌ها جایگزین مستقیم یکدیگر نیستند و پیش از طراحی مسیر باید "
                "محدودیت‌های نصب و اجزای قابل استفاده هرکدام را ببینید.",
                "برای مقایسه قیمت چراغ مگنتی، هزینه یک ماژول را به‌تنهایی معیار قرار ندهید. "
                "ریل، منبع تغذیه، اتصال‌ها، قطعات نصب و تعداد و نوع چراغ‌ها قیمت کل سیستم "
                "را می‌سازند. ابتدا مسیر و سناریوی نور را مشخص کنید و سپس فهرست کامل اجزا "
                "را برای استعلام و کنترل سازگاری آماده کنید.",
            ),
            related_heading="خانواده‌های سیستم چراغ مگنتی",
            related_intro=(
                "هر خانواده را باز کنید تا زیرگروه‌ها، مدل‌ها و مشخصات مرتبط با همان سیستم "
                "را ببینید. پیش از سفارش، سازگاری اجزا را در یک خانواده واحد کنترل کنید."
            ),
            related_links=(
                RelatedLink(
                    "Magnet Small",
                    "سیستم مگنتی با مقیاس ظریف‌تر برای حضور بصری کنترل‌شده.",
                    "products:child_detail",
                    (("cat_slug", "low-voltage-magneto"), ("child_slug", "magent-small-family")),
                ),
                RelatedLink(
                    "Magnet Large",
                    "سیستم مگنتی بزرگ‌تر برای فضاها و ترکیب‌های نوری با بیان قوی‌تر.",
                    "products:child_detail",
                    (("cat_slug", "low-voltage-magneto"), ("child_slug", "magent-large4cm-family")),
                ),
                RelatedLink(
                    "Magnet Curve",
                    "راهکار مگنتی برای طراحی مسیرهای منحنی و خطوط نرم‌تر.",
                    "products:child_detail",
                    (("cat_slug", "low-voltage-magneto"), ("child_slug", "magnet-curve")),
                ),
                RelatedLink(
                    "Magnet Belt",
                    "خانواده‌ای منعطف برای ساخت یک خط نور با هویت متفاوت.",
                    "products:child_detail",
                    (("cat_slug", "low-voltage-magneto"), ("child_slug", "mmagne-tbelt")),
                ),
                RelatedLink(
                    "Magnet Flexi",
                    "سیستم مگنتی منعطف برای مسیرها و فرم‌های غیرخطی.",
                    "products:child_detail",
                    (("cat_slug", "low-voltage-magneto"), ("child_slug", "magnet-flexi")),
                ),
            ),
            faq_heading="پرسش‌های متداول درباره چراغ مگنتی",
            faqs=(
                FAQ(
                    "چراغ مگنتی چیست و چگونه کار می‌کند؟",
                    "چراغ مگنتی مجموعه‌ای از ریل کم‌ولتاژ، منبع تغذیه، اتصالات و ماژول‌های "
                    "نور سازگار است. ماژول‌ها روی ریل نصب می‌شوند و در محدوده طراحی سیستم "
                    "امکان جابه‌جایی یا تغییر ترکیب آن‌ها وجود دارد.",
                ),
                FAQ(
                    "تفاوت چراغ مگنتی Small و Large چیست؟",
                    "این دو خانواده در ابعاد ریل، مقیاس ظاهری و اجزای سازگار تفاوت دارند. "
                    "Small ظاهر ظریف‌تری دارد و Large حضور بصری قوی‌تری ایجاد می‌کند. انتخاب "
                    "نهایی را با نیاز نوری و مشخصات فنی مدل‌ها هماهنگ کنید.",
                ),
                FAQ(
                    "ریل مگنتی توکار بهتر است یا روکار؟",
                    "هیچ‌کدام همیشه بهتر نیست. توکار برای ادغام بیشتر با سقف به شیار و "
                    "زیرسازی دقیق نیاز دارد؛ روکار اجرای ساده‌تری روی سطح موجود فراهم می‌کند. "
                    "نوع سقف، زمان اجرا و دیتیل معماری تعیین‌کننده هستند.",
                ),
                FAQ(
                    "قیمت سیستم چراغ مگنتی چگونه محاسبه می‌شود؟",
                    "قیمت کل از طول و نوع ریل، منبع تغذیه، اتصال‌ها، لوازم نصب و تعداد و مدل "
                    "ماژول‌های نور تشکیل می‌شود. برای برآورد درست باید نقشه مسیر و فهرست کامل "
                    "اجزای سازگار آماده شود.",
                ),
            ),
        ),
        "en": LandingPageContent(
            primary_keyword="magnetic track lighting",
            eyebrow="Magnetic system selection guide",
            heading="How to select magnetic track lighting for an architectural project",
            lead=(
                "Magnetic track lighting is a modular system, not a stand-alone fitting. A sound "
                "specification begins with the track family, mounting method and power route, then "
                "builds the required mix of light modules. This guide explains the decisions that "
                "keep the system coordinated from design through installation."
            ),
            intro_paragraphs=(
                "Track dimensions, product family, mounting method, power supply, connectors and "
                "module compatibility must be treated as one assembly. Choosing an attractive light "
                "module without checking the supporting system can create connection, space or "
                "ceiling-detail problems when the project reaches installation.",
                "Verona’s magnetic range includes Small, Large, Curve, Belt and Flexi families, with "
                "linear, spot, pendant and panel options available across their relevant subgroups. "
                "Each family has its own visual language and installation requirements. Select the "
                "system first, then compose the lighting modules that belong to it.",
            ),
            selection_heading="What should be decided before ordering magnetic track lighting?",
            selection_intro=(
                "These four decisions define the system and should be coordinated with the design "
                "and installation teams before the ceiling plan and equipment schedule are final."
            ),
            selection_items=(
                ContentItem(
                    "Track family and dimensions",
                    "Small and Large are not simply visual labels: their dimensions, scale and "
                    "compatible components differ. Select tracks, connectors and luminaires from "
                    "one compatible family and never assume that components from separate systems "
                    "can be mixed.",
                ),
                ContentItem(
                    "Recessed, surface or suspended mounting",
                    "A recessed track needs a coordinated channel and ceiling build-up; surface track "
                    "offers a more direct installation on the finished plane; suspended track can suit "
                    "high ceilings or a floating architectural line. Confirm mounting before setting "
                    "the track section and lengths.",
                ),
                ContentItem(
                    "The mix of lighting modules",
                    "Linear modules can provide general light, spots can add emphasis, pendants can "
                    "bring light closer to a task and panels can create a broader luminous surface. "
                    "Choose the mix for the room use, layout, glare control and intended lighting scenes.",
                ),
                ContentItem(
                    "Route, connectors and future changes",
                    "Plot track lengths, corners, power-entry points, driver capacity and every connector "
                    "on the plan. If future layout changes are important, retain useful free track length "
                    "and confirm how additional modules can be supported by the system.",
                ),
            ),
            comparison_heading="Which magnetic lighting family suits the project?",
            comparison_paragraphs=(
                "The Small family suits a finer scale and a lower visual presence, while Large creates "
                "a stronger line with larger proportions. Compare them against the room size, ceiling "
                "height, required module types and the technical data available within each family.",
                "Curve supports curved routes and a softer geometric expression; Belt offers a flexible "
                "line with a distinct character; Flexi is relevant where adaptable, non-linear form is "
                "central to the concept. They are not direct substitutes, so review the installation "
                "limits and available components before drawing the route.",
                "When comparing magnetic track lighting prices, do not use the cost of one module as "
                "the project total. Track, power supplies, connectors, mounting components and the "
                "quantity and type of luminaires form the complete system price. Define the route and "
                "lighting scenes first, then prepare a coordinated component schedule.",
            ),
            related_heading="Explore Verona magnetic lighting families",
            related_intro=(
                "Open a family to review its subgroups, models and relevant technical information. "
                "Before ordering, confirm that every item belongs to the same compatible system."
            ),
            related_links=(
                RelatedLink(
                    "Magnet Small",
                    "A finer-scale magnetic system with a controlled visual presence.",
                    "products:child_detail",
                    (("cat_slug", "low-voltage-magneto"), ("child_slug", "magent-small-family")),
                ),
                RelatedLink(
                    "Magnet Large",
                    "A larger magnetic system for spaces and compositions that need a stronger line.",
                    "products:child_detail",
                    (("cat_slug", "low-voltage-magneto"), ("child_slug", "magent-large4cm-family")),
                ),
                RelatedLink(
                    "Magnet Curve",
                    "A magnetic solution for curved routes and softer architectural geometry.",
                    "products:child_detail",
                    (("cat_slug", "low-voltage-magneto"), ("child_slug", "magnet-curve")),
                ),
                RelatedLink(
                    "Magnet Belt",
                    "A flexible family for creating a light line with a distinct character.",
                    "products:child_detail",
                    (("cat_slug", "low-voltage-magneto"), ("child_slug", "mmagne-tbelt")),
                ),
                RelatedLink(
                    "Magnet Flexi",
                    "A flexible magnetic system for adaptable and non-linear forms.",
                    "products:child_detail",
                    (("cat_slug", "low-voltage-magneto"), ("child_slug", "magnet-flexi")),
                ),
            ),
            faq_heading="Frequently asked questions about magnetic track lighting",
            faqs=(
                FAQ(
                    "What is magnetic track lighting?",
                    "It is a coordinated system of low-voltage track, power supply, connectors and "
                    "compatible light modules. Modules attach to the track and, within the limits of "
                    "the system design, can be repositioned or recomposed as lighting needs change.",
                ),
                FAQ(
                    "What is the difference between Magnet Small and Magnet Large?",
                    "The families differ in track dimensions, visual scale and compatible components. "
                    "Small has a finer appearance, while Large creates a stronger visual presence. "
                    "Coordinate the choice with the required output and the data for the actual modules.",
                ),
                FAQ(
                    "Is recessed or surface magnetic track better?",
                    "Neither is universally better. Recessed track integrates more closely with the "
                    "ceiling but needs an accurate channel and build-up. Surface track provides a more "
                    "direct installation on an existing plane. Ceiling type, programme and architectural "
                    "detail should determine the choice.",
                ),
                FAQ(
                    "How is a magnetic track lighting system priced?",
                    "The total includes the track type and length, power supply, connectors, installation "
                    "components and the number and type of light modules. A reliable estimate requires "
                    "a planned route and a complete schedule of compatible components.",
                ),
            ),
        ),
    },
}


def _visible_text(content):
    return " ".join(
        (
            content.primary_keyword,
            content.heading,
            content.lead,
            *content.intro_paragraphs,
            content.selection_heading,
            content.selection_intro,
            *(item.title + " " + item.body for item in content.selection_items),
            content.comparison_heading,
            *content.comparison_paragraphs,
            content.related_heading,
            content.related_intro,
            *(link.label + " " + link.description for link in content.related_links),
            content.faq_heading,
            *(faq.question + " " + faq.answer for faq in content.faqs),
        )
    )


def validate_landing_page_content():
    expected_clusters = {"recessed-linear", "magnetic-track"}
    if set(LANDING_PAGE_CONTENT) != expected_clusters:
        raise ValueError("Landing-page keyword clusters are incomplete.")

    for cluster, translations in LANDING_PAGE_CONTENT.items():
        if set(translations) != {"fa", "en"}:
            raise ValueError(f"{cluster} must provide both Persian and English content.")
        for language, content in translations.items():
            visible_text = _visible_text(content)
            if len(visible_text) < 2500:
                raise ValueError(f"{cluster}/{language} content is too thin.")
            if content.primary_keyword.casefold() not in visible_text.casefold():
                raise ValueError(f"{cluster}/{language} is missing its primary keyword.")
            if len(content.selection_items) != 4 or len(content.faqs) != 4:
                raise ValueError(f"{cluster}/{language} must contain four criteria and four FAQs.")
            questions = [faq.question for faq in content.faqs]
            if len(questions) != len(set(questions)):
                raise ValueError(f"{cluster}/{language} contains duplicate FAQ questions.")


def build_landing_page_context(cluster, language_code):
    language = "fa" if language_code == "fa" else "en"
    content = LANDING_PAGE_CONTENT[cluster][language]
    related_links = [
        {
            "label": link.label,
            "description": link.description,
            "url": reverse(link.route_name, kwargs=dict(link.route_kwargs)),
        }
        for link in content.related_links
    ]
    return {"content": content, "related_links": related_links}
