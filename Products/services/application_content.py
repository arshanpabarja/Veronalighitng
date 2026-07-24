"""Reviewed bilingual content for Verona Lighting application pages."""

from dataclasses import dataclass, fields


@dataclass(frozen=True)
class ApplicationContent:
    name_fa: str
    name_en: str
    short_description_fa: str
    short_description_en: str
    description_fa: str
    description_en: str
    meta_title_fa: str
    meta_title_en: str
    meta_description_fa: str
    meta_description_en: str
    cover_image_alt_fa: str
    cover_image_alt_en: str


APPLICATION_CONTENT = {
    "fashion": ApplicationContent(
        name_fa="گالری هنری",
        name_en="Art Gallery",
        short_description_fa=(
            "راهکارهای نورپردازی گالری برای نمایش دقیق آثار، کنترل خیرگی و ایجاد نور تأکیدی انعطاف‌پذیر."
        ),
        short_description_en=(
            "Gallery lighting solutions for accurate artwork presentation, glare control and flexible accent light."
        ),
        description_fa=(
            "نورپردازی گالری هنری باید اثر را واضح و طبیعی نمایش دهد، بدون آنکه خیرگی، بازتاب مزاحم یا "
            "سایه‌های ناخواسته توجه بازدیدکننده را منحرف کند. شاخص نمود رنگ، زاویه تابش، فاصله چراغ از اثر "
            "و امکان تنظیم جهت نور از مهم‌ترین معیارهای طراحی این فضا هستند.\n\n"
            "در این صفحه می‌توانید خانواده‌های روشنایی مرتبط ورونا را برای نور عمومی، نور تأکیدی و "
            "روشن‌کردن دیوارهای نمایش بررسی کنید. چراغ‌های ریلی و مدل‌های جهت‌پذیر امکان هماهنگی نور با "
            "چیدمان متغیر آثار را فراهم می‌کنند؛ پیش از انتخاب نهایی، مشخصات اپتیکی و ابعاد هر خانواده را "
            "با ارتفاع سقف، ابعاد اثر و سناریوی نمایش پروژه مقایسه کنید."
        ),
        description_en=(
            "Art gallery lighting should reveal each work clearly and naturally without distracting glare, "
            "reflections or unwanted shadows. Colour rendering, beam angle, distance from the artwork and the "
            "ability to aim the light are central considerations for exhibition spaces.\n\n"
            "This page brings together relevant Verona lighting families for ambient, accent and display-wall "
            "illumination. Track-mounted and adjustable luminaires can respond to changing exhibition layouts; "
            "before specifying a family, compare its optical data and dimensions with the ceiling height, "
            "artwork scale and curatorial lighting plan."
        ),
        meta_title_fa="نورپردازی گالری هنری | ورونا لایتینگ",
        meta_title_en="Art Gallery Lighting Solutions | Verona Lighting",
        meta_description_fa=(
            "راهکارهای نورپردازی گالری هنری ورونا را برای نمایش آثار، کنترل خیرگی و نور تأکیدی بررسی و خانواده‌های چراغ مرتبط را مقایسه کنید."
        ),
        meta_description_en=(
            "Explore Verona art gallery lighting for accurate artwork presentation, glare control and flexible accent illumination."
        ),
        cover_image_alt_fa="نورپردازی معماری گالری هنری با چراغ‌های تأکیدی",
        cover_image_alt_en="Architectural art gallery lighting with accent luminaires",
    ),
    "facade": ApplicationContent(
        name_fa="نمای ساختمان",
        name_en="Facade",
        short_description_fa=(
            "راهکارهای نورپردازی نما برای خوانایی حجم، تأکید بر جزئیات معماری و عملکرد مطمئن در فضای باز."
        ),
        short_description_en=(
            "Facade lighting solutions that reveal architectural form, emphasise details and perform outdoors."
        ),
        description_fa=(
            "نورپردازی نمای ساختمان باید فرم، ریتم و متریال معماری را در شب خوانا کند و هم‌زمان از خیرگی "
            "برای عابر، همسایه و راننده جلوگیری کند. محل نصب، فاصله از سطح، زاویه تابش، یکنواختی نور، "
            "درجه حفاظت و دسترسی برای نگهداری باید از ابتدای طراحی در نظر گرفته شوند.\n\n"
            "در این صفحه خانواده‌های مرتبط ورونا برای نور خطی، تأکید موضعی و روشنایی بخش‌های بیرونی معرفی "
            "شده‌اند. انتخاب محصول باید براساس ارتفاع نما، بافت سطح، جهت دید اصلی و شرایط محیطی پروژه انجام "
            "شود؛ تصاویر و مشخصات هر خانواده را بررسی کنید تا ابعاد، روش نصب و پخش نور با جزئیات اجرایی "
            "هماهنگ باشد."
        ),
        description_en=(
            "Facade lighting should make architectural form, rhythm and material legible after dark while "
            "limiting glare for pedestrians, neighbours and drivers. Mounting position, setback from the "
            "surface, beam distribution, uniformity, ingress protection and maintenance access should be "
            "considered from the start of the design.\n\n"
            "This page presents relevant Verona families for linear illumination, local accents and exterior "
            "architectural details. Selection should respond to façade height, surface texture, primary viewing "
            "directions and environmental conditions. Review each family's images and specifications so its "
            "dimensions, installation method and light distribution coordinate with the project details."
        ),
        meta_title_fa="نورپردازی نمای ساختمان | ورونا لایتینگ",
        meta_title_en="Architectural Facade Lighting | Verona Lighting",
        meta_description_fa=(
            "راهکارهای نورپردازی نمای ساختمان ورونا را براساس فرم معماری، زاویه تابش، روش نصب و شرایط فضای باز بررسی و مقایسه کنید."
        ),
        meta_description_en=(
            "Explore Verona architectural facade lighting by form, beam distribution, mounting method and outdoor project conditions."
        ),
        cover_image_alt_fa="نورپردازی نمای ساختمان و جزئیات معماری بیرونی",
        cover_image_alt_en="Architectural facade and exterior detail lighting",
    ),
    "hospitality": ApplicationContent(
        name_fa="هتل و مهمان‌نوازی",
        name_en="Hospitality",
        short_description_fa=(
            "راهکارهای روشنایی هتل، لابی، اتاق و رستوران با تمرکز بر آسایش بصری و هویت فضا."
        ),
        short_description_en=(
            "Lighting solutions for hotels, lobbies, guest rooms and restaurants focused on comfort and identity."
        ),
        description_fa=(
            "نورپردازی هتل و فضاهای مهمان‌نوازی باید میان آسایش، عملکرد و هویت بصری تعادل ایجاد کند. لابی، "
            "راهرو، اتاق مهمان، رستوران و فضاهای خدماتی هرکدام به شدت نور، دمای رنگ و نحوه کنترل متفاوتی "
            "نیاز دارند و بهتر است در قالب سناریوهای هماهنگ طراحی شوند.\n\n"
            "خانواده‌های مرتبط ورونا در این صفحه برای ایجاد نور عمومی، نور وظیفه‌ای، تأکید معماری و عناصر "
            "دکوراتیو گردآوری شده‌اند. هنگام مقایسه، به کیفیت نور، کنترل خیرگی، ابعاد چراغ، روش نصب و امکان "
            "هماهنگی مدل‌ها در بخش‌های مختلف پروژه توجه کنید تا تجربه‌ای پیوسته از ورودی تا فضای اقامت شکل گیرد."
        ),
        description_en=(
            "Hospitality lighting must balance visual comfort, practical performance and a distinctive sense "
            "of place. Lobbies, corridors, guest rooms, restaurants and service areas each require an appropriate "
            "level, colour temperature and control strategy, ideally coordinated through a consistent set of scenes.\n\n"
            "The Verona families collected on this page support ambient, task, architectural accent and "
            "decorative lighting. Compare light quality, glare control, luminaire dimensions, mounting method "
            "and the ability to coordinate models across different areas so the guest experience remains "
            "coherent from arrival to accommodation."
        ),
        meta_title_fa="نورپردازی هتل و فضای مهمان‌نوازی | ورونا",
        meta_title_en="Hospitality and Hotel Lighting | Verona Lighting",
        meta_description_fa=(
            "راهکارهای نورپردازی هتل، لابی، اتاق و رستوران ورونا را برای آسایش بصری، نور تأکیدی و هماهنگی طراحی داخلی بررسی کنید."
        ),
        meta_description_en=(
            "Explore Verona hospitality lighting for hotels, lobbies, guest rooms and restaurants, balancing comfort, function and atmosphere."
        ),
        cover_image_alt_fa="نورپردازی داخلی هتل و فضای مهمان‌نوازی",
        cover_image_alt_en="Hotel interior and hospitality lighting",
    ),
    "house": ApplicationContent(
        name_fa="فضای مسکونی",
        name_en="Residential",
        short_description_fa=(
            "روشنایی مسکونی برای نشیمن، آشپزخانه، اتاق‌ها و مسیرهای حرکتی با ترکیب نور عمومی و تأکیدی."
        ),
        short_description_en=(
            "Residential lighting for living areas, kitchens, bedrooms and circulation using layered illumination."
        ),
        description_fa=(
            "روشنایی فضای مسکونی زمانی موفق است که نیازهای روزمره را با آرامش و شخصیت خانه ترکیب کند. "
            "نشیمن، آشپزخانه، اتاق خواب، ورودی و مسیرهای حرکتی به لایه‌های متفاوت نور عمومی، وظیفه‌ای و "
            "تأکیدی نیاز دارند؛ جانمایی درست از تعداد زیاد چراغ مهم‌تر است.\n\n"
            "در این صفحه می‌توانید خانواده‌های مرتبط ورونا را براساس نوع نصب، فرم، ابعاد و کیفیت نور بررسی "
            "کنید. برای انتخاب دقیق، به ارتفاع سقف، چیدمان مبلمان، سطوح بازتابنده، دمای رنگ و نیاز به کنترل "
            "یا دیمر توجه کنید و مشخصات هر محصول را با سناریوی استفاده از فضای خانه تطبیق دهید."
        ),
        description_en=(
            "Residential lighting works best when everyday tasks, visual comfort and the character of the home "
            "are considered together. Living areas, kitchens, bedrooms, entrances and circulation routes need "
            "different layers of ambient, task and accent light; thoughtful placement matters more than simply "
            "adding more luminaires.\n\n"
            "Use this page to compare relevant Verona families by mounting type, form, dimensions and light "
            "quality. Ceiling height, furniture layout, reflective surfaces, colour temperature and the need "
            "for dimming or control should all inform the selection. Check each product's specifications against "
            "the way the residential space will actually be used."
        ),
        meta_title_fa="روشنایی فضای مسکونی | ورونا لایتینگ",
        meta_title_en="Residential Lighting Solutions | Verona Lighting",
        meta_description_fa=(
            "راهکارهای روشنایی مسکونی ورونا را برای نشیمن، آشپزخانه، اتاق خواب و مسیرهای حرکتی براساس نوع نصب و کیفیت نور بررسی کنید."
        ),
        meta_description_en=(
            "Explore Verona residential lighting for living areas, kitchens, bedrooms and circulation, with ambient, task and accent solutions."
        ),
        cover_image_alt_fa="روشنایی معماری فضای مسکونی و نشیمن",
        cover_image_alt_en="Architectural lighting for a residential living space",
    ),
    "landescape": ApplicationContent(
        name_fa="محوطه و فضای سبز",
        name_en="Landscape",
        short_description_fa=(
            "راهکارهای روشنایی محوطه برای مسیر، حیاط، باغ و عناصر سبز با توجه به ایمنی و شرایط فضای باز."
        ),
        short_description_en=(
            "Landscape lighting for paths, courtyards, gardens and planting with safe, considered outdoor light."
        ),
        description_fa=(
            "روشنایی محوطه و فضای سبز باید حرکت ایمن را ممکن کند و هم‌زمان عمق، بافت و نقاط شاخص محیط را "
            "در شب نشان دهد. مسیرها، پله‌ها، حیاط، باغچه، درختان و لبه‌های معماری به روش‌های متفاوتی از "
            "نورپردازی نیاز دارند و کنترل خیرگی در تمام آن‌ها ضروری است.\n\n"
            "خانواده‌های مرتبط ورونا در این صفحه برای بررسی نور مسیر، نور تأکیدی و روشنایی عناصر بیرونی "
            "گردآوری شده‌اند. پیش از انتخاب، محل نصب، زاویه دید، درجه حفاظت ثبت‌شده، نحوه کابل‌کشی و دسترسی "
            "برای سرویس را با شرایط پروژه تطبیق دهید و پخش نور هر مدل را براساس فاصله و مقیاس عناصر محوطه بسنجید."
        ),
        description_en=(
            "Landscape lighting should support safe movement while revealing depth, texture and focal points "
            "after dark. Paths, steps, courtyards, planting, trees and architectural edges each call for a "
            "different lighting approach, with careful glare control throughout the scheme.\n\n"
            "This page gathers relevant Verona families for path lighting, accents and exterior elements. Before "
            "selection, coordinate the mounting location, viewing direction, documented ingress protection, "
            "cable route and maintenance access with the site conditions. Assess each model's distribution "
            "against the distance and scale of the landscape feature it will illuminate."
        ),
        meta_title_fa="روشنایی محوطه و فضای سبز | ورونا لایتینگ",
        meta_title_en="Landscape Lighting Solutions | Verona Lighting",
        meta_description_fa=(
            "راهکارهای روشنایی محوطه ورونا را برای مسیر، حیاط، باغ و فضای سبز براساس محل نصب، پخش نور و شرایط فضای باز مقایسه کنید."
        ),
        meta_description_en=(
            "Explore Verona landscape lighting for paths, courtyards, gardens and planting by mounting location, distribution and outdoor conditions."
        ),
        cover_image_alt_fa="روشنایی محوطه، مسیر و فضای سبز در شب",
        cover_image_alt_en="Night lighting for landscape paths and planting",
    ),
    "office": ApplicationContent(
        name_fa="فضای اداری",
        name_en="Office",
        short_description_fa=(
            "راهکارهای روشنایی اداری برای میز کار، جلسه و فضاهای مشترک با تمرکز بر آسایش بصری."
        ),
        short_description_en=(
            "Office lighting for workstations, meeting rooms and shared areas with visual comfort in mind."
        ),
        description_fa=(
            "روشنایی فضای اداری باید تمرکز، آسایش بصری و انعطاف چیدمان را پشتیبانی کند. میزهای کار، اتاق "
            "جلسه، فضای همکاری، پذیرش و مسیرهای حرکتی به توزیع نور و شدت‌های متفاوتی نیاز دارند؛ کنترل خیرگی "
            "روی نمایشگرها و هماهنگی نور مصنوعی با نور روز از معیارهای اصلی طراحی هستند.\n\n"
            "در این صفحه خانواده‌های مرتبط ورونا برای نور عمومی، نور خطی، روشنایی موضعی و تأکید معماری "
            "معرفی شده‌اند. هنگام مقایسه، شار نوری، شاخص نمود رنگ، دمای رنگ، ابعاد و روش نصب را در کنار "
            "ارتفاع سقف و شبکه‌بندی فضای اداری بررسی کنید تا انتخاب چراغ با پلان و نحوه استفاده واقعی هماهنگ باشد."
        ),
        description_en=(
            "Office lighting should support concentration, visual comfort and changing workplace layouts. "
            "Workstations, meeting rooms, collaborative areas, reception and circulation require different "
            "distributions and light levels; limiting screen glare and coordinating electric light with daylight "
            "are key design considerations.\n\n"
            "This page presents relevant Verona families for ambient, linear, local and architectural accent "
            "lighting. Compare luminous flux, colour rendering, colour temperature, dimensions and mounting "
            "method alongside the ceiling height and workplace grid so the selected luminaires suit both the "
            "plan and the way the office is used."
        ),
        meta_title_fa="روشنایی فضای اداری و دفتر کار | ورونا",
        meta_title_en="Office Lighting Solutions | Verona Lighting",
        meta_description_fa=(
            "راهکارهای روشنایی اداری ورونا را برای میز کار، اتاق جلسه و فضاهای مشترک براساس آسایش بصری، کیفیت نور و نوع نصب بررسی کنید."
        ),
        meta_description_en=(
            "Explore Verona office lighting for workstations, meeting rooms and shared spaces, with visual comfort, light quality and mounting in mind."
        ),
        cover_image_alt_fa="روشنایی فضای اداری مدرن و میزهای کار",
        cover_image_alt_en="Modern office and workstation lighting",
    ),
    "retail": ApplicationContent(
        name_fa="فروشگاه و خرده‌فروشی",
        name_en="Retail",
        short_description_fa=(
            "راهکارهای نورپردازی فروشگاه برای نمایش دقیق کالا، هدایت نگاه و تغییرپذیری چیدمان."
        ),
        short_description_en=(
            "Retail lighting for accurate merchandise display, visual guidance and adaptable store layouts."
        ),
        description_fa=(
            "نورپردازی فروشگاه باید کالا را دقیق نمایش دهد، مسیر حرکت مشتری را خوانا کند و نقاط مهم فضا را "
            "برجسته سازد. شاخص نمود رنگ، شدت نور روی محصول، زاویه تابش و کنترل خیرگی مستقیماً بر تجربه دیدن "
            "کالا و کیفیت فضای فروش اثر می‌گذارند.\n\n"
            "در این صفحه خانواده‌های مرتبط ورونا برای نور عمومی، چراغ ریلی، نور تأکیدی و روشنایی ویترین "
            "گردآوری شده‌اند. سیستم‌های قابل تنظیم برای چیدمان‌هایی که در طول زمان تغییر می‌کنند انعطاف بیشتری "
            "ایجاد می‌کنند؛ پیش از انتخاب، ارتفاع نصب، فاصله چراغ تا کالا، عرض پرتو و مشخصات ثبت‌شده هر مدل "
            "را با پلان فروشگاه مقایسه کنید."
        ),
        description_en=(
            "Retail lighting should present merchandise accurately, make customer routes legible and draw "
            "attention to important displays. Colour rendering, illuminance on the product, beam angle and glare "
            "control directly influence how merchandise and the wider store environment are perceived.\n\n"
            "This page gathers relevant Verona families for ambient, track, accent and window-display lighting. "
            "Adjustable systems offer flexibility where merchandising changes over time; before choosing a model, "
            "compare mounting height, distance to the merchandise, beam width and documented specifications with "
            "the store layout."
        ),
        meta_title_fa="نورپردازی فروشگاه و ویترین | ورونا لایتینگ",
        meta_title_en="Retail and Store Lighting | Verona Lighting",
        meta_description_fa=(
            "راهکارهای نورپردازی فروشگاه ورونا را برای نمایش کالا، ویترین و نور تأکیدی براساس نمود رنگ، زاویه تابش و چیدمان بررسی کنید."
        ),
        meta_description_en=(
            "Explore Verona retail lighting for merchandise, displays and shop windows by colour rendering, beam angle and store layout."
        ),
        cover_image_alt_fa="نورپردازی فروشگاه، ویترین و نمایش کالا",
        cover_image_alt_en="Retail store, window and merchandise lighting",
    ),
}


def validate_application_content() -> None:
    expected_slugs = {
        "fashion",
        "facade",
        "hospitality",
        "house",
        "landescape",
        "office",
        "retail",
    }
    if set(APPLICATION_CONTENT) != expected_slugs:
        raise ValueError("Application content must cover every active application slug.")

    for slug, content in APPLICATION_CONTENT.items():
        for field in fields(content):
            if not getattr(content, field.name).strip():
                raise ValueError(f"{slug}/{field.name}: content is empty.")
        for language in ("fa", "en"):
            if len(getattr(content, f"meta_title_{language}")) > 60:
                raise ValueError(f"{slug}/{language}: meta title exceeds 60 characters.")
            if len(getattr(content, f"meta_description_{language}")) > 160:
                raise ValueError(
                    f"{slug}/{language}: meta description exceeds 160 characters."
                )
            if len(getattr(content, f"short_description_{language}")) > 300:
                raise ValueError(
                    f"{slug}/{language}: short description exceeds 300 characters."
                )
            if len(getattr(content, f"cover_image_alt_{language}")) > 125:
                raise ValueError(f"{slug}/{language}: image alt exceeds 125 characters.")

    for field_name in (
        "meta_title_fa",
        "meta_title_en",
        "meta_description_fa",
        "meta_description_en",
        "description_fa",
        "description_en",
    ):
        values = [getattr(content, field_name) for content in APPLICATION_CONTENT.values()]
        if len(values) != len(set(values)):
            raise ValueError(f"{field_name}: values must be unique.")
