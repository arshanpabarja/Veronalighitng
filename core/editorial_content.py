from dataclasses import dataclass
from html import escape
import re

from django.urls import reverse


@dataclass(frozen=True)
class Section:
    heading: str
    paragraphs: tuple[str, ...]


@dataclass(frozen=True)
class ArticleTranslation:
    keyword: str
    title: str
    excerpt: str
    meta_title: str
    meta_description: str
    sections: tuple[Section, ...]


@dataclass(frozen=True)
class EditorialArticle:
    cluster: str
    cover_image: str
    read_time: int
    published_at: str
    translations: dict[str, ArticleTranslation]


EDITORIAL_ARTICLES = {
    "trimmed-vs-trimless-recessed-linear-lighting": EditorialArticle(
        cluster="recessed-linear",
        cover_image="products/Bardia_Narrow_render.png",
        read_time=8,
        published_at="2026-07-03",
        translations={
            "fa": ArticleTranslation(
                keyword="تفاوت چراغ خطی توکار لبه‌دار و بدون لبه",
                title="تفاوت چراغ خطی توکار لبه‌دار و بدون لبه؛ کدام مناسب پروژه است؟",
                excerpt=(
                    "مقایسه اجرایی و معماری چراغ خطی توکار لبه‌دار و تریم‌لس؛ "
                    "از زیرسازی و پرداخت سقف تا نگهداری و انتخاب مدل مناسب پروژه."
                ),
                meta_title="تفاوت چراغ خطی توکار لبه‌دار و بدون لبه",
                meta_description=(
                    "تفاوت چراغ خطی توکار لبه‌دار و بدون لبه را از نظر ظاهر، "
                    "زیرسازی، نصب، نگهداری و کاربرد بررسی کنید و مدل مناسب پروژه را انتخاب کنید."
                ),
                sections=(
                    Section(
                        "تفاوت اصلی در کجاست؟",
                        (
                            "در مدل لبه‌دار، قاب باریکی پیرامون پروفیل روی سطح نهایی دیده می‌شود و مرز برش سقف را می‌پوشاند. در مدل بدون لبه یا تریم‌لس، پروفیل پیش از پرداخت نهایی در سقف تثبیت می‌شود تا بعد از بتونه و رنگ، خط نور با سطح معماری یکپارچه دیده شود. بنابراین تفاوت فقط ظاهری نیست؛ ترتیب اجرا، میزان تلرانس و مسئولیت تیم سقف نیز تغییر می‌کند.",
                            "صفحه <a href='/linear/c/recessed/'>راهنمای چراغ خطی توکار</a> خانواده‌های ورونا را بر اساس همین منطق مقایسه می‌کند. انتخاب باید پیش از بسته‌شدن سقف انجام شود، زیرا عرض شیار، عمق نصب، محل درایور و روش دسترسی سرویس بخشی از دیتیل معماری هستند.",
                        ),
                    ),
                    Section(
                        "چه زمانی مدل لبه‌دار منطقی‌تر است؟",
                        (
                            "مدل لبه‌دار زمانی انتخاب قابل‌کنترل‌تری است که سرعت اجرا، پوشاندن تلرانس برش یا امکان نصب پس از بخشی از عملیات سقف اهمیت دارد. لبه ظریف می‌تواند اختلاف‌های کوچک میان شیار و بدنه را مدیریت کند و مرز چراغ را خواناتر نشان دهد.",
                            "این ویژگی به معنی بی‌نیازی از دیتیل دقیق نیست. تراز خط، پیوستگی دیفیوزر، محل اتصال شاخه‌ها و دسترسی به تجهیزات همچنان باید کنترل شوند. برای یک نمونه باریک، مشخصات <a href='/linear/c/recessed/sp/sp-narrow/'>چراغ خطی توکار لبه‌دار SP NARROW</a> را با مقطع پروژه تطبیق دهید.",
                        ),
                    ),
                    Section(
                        "چه زمانی تریم‌لس ارزش بیشتری دارد؟",
                        (
                            "مدل بدون لبه زمانی ارزش معماری بیشتری ایجاد می‌کند که هدف، حذف قاب و تبدیل نور به بخشی از سطح سقف یا دیوار باشد. نتیجه مینیمال‌تر است، اما کیفیت آن مستقیماً به زیرسازی، تراز پروفیل و پرداخت نهایی وابسته است. اصلاح یک خط تریم‌لس پس از رنگ معمولاً دشوارتر از اصلاح مدل لبه‌دار است.",
                            "پیش از سفارش، تیم معماری، مجری کناف و تأمین‌کننده باید مقطع واحدی را تأیید کنند. صفحه <a href='/linear/c/recessed/BD/bd-narrow/'>چراغ خطی توکار بدون لبه BD NARROW</a> نمونه‌ای از اطلاعاتی است که باید کنار نقشه سقف بررسی شود.",
                        ),
                    ),
                    Section(
                        "مقایسه نور، نگهداری و هزینه اجرا",
                        (
                            "لبه‌دار یا بدون لبه بودن به‌تنهایی توان، شار نوری یا کیفیت نور را تعیین نمی‌کند. برای مقایسه واقعی باید لومن در متر، توان در متر، CRI، دمای رنگ، اپتیک و طول کل خط را دید. دو محصول با ظاهر مشابه ممکن است خروجی یا مقطع متفاوتی داشته باشند.",
                            "هزینه نیز فقط قیمت چراغ نیست. زیرسازی، زمان پرداخت، احتمال اصلاح سقف، درایور، کابل‌کشی و دسترسی آینده بر هزینه کل اثر می‌گذارند. تصمیم درست مدلی است که با زبان معماری و توان اجرایی پروژه هم‌زمان سازگار باشد، نه مدلی که صرفاً در تصویر جذاب‌تر دیده می‌شود.",
                        ),
                    ),
                    Section(
                        "چک‌لیست تصمیم نهایی",
                        (
                            "نوع سقف و زمان نصب، عرض و عمق شیار، امکان دسترسی به درایور، کیفیت مورد انتظار از لبه، طول خط، سطح روشنایی و مسئولیت تحویل دیتیل را پیش از سفارش ثبت کنید. اگر تیم اجرا تجربه کافی در پرداخت تریم‌لس ندارد، نمونه اجرایی کوچک می‌تواند ریسک پروژه را کاهش دهد.",
                            "پس از انتخاب نوع لبه، مدل نهایی را با دیتاشیت و نمونه قطعی کنید. برای مرحله بعد، راهنمای <a href='/news/recessed-linear-lighting-knauf-ceiling-installation/'>نصب چراغ خطی توکار در سقف کناف</a> نقاط هماهنگی قبل از اجرا را توضیح می‌دهد.",
                        ),
                    ),
                ),
            ),
            "en": ArticleTranslation(
                keyword="trimmed vs trimless recessed linear lighting",
                title="Trimmed vs trimless recessed linear lighting: which detail suits the project?",
                excerpt=(
                    "An architectural and installation comparison of trimmed and trimless "
                    "recessed linear lighting, from ceiling preparation to maintenance."
                ),
                meta_title="Trimmed vs Trimless Recessed Linear Lighting",
                meta_description=(
                    "Compare trimmed vs trimless recessed linear lighting for appearance, "
                    "ceiling preparation, installation tolerance, maintenance and project use."
                ),
                sections=(
                    Section(
                        "What is the fundamental difference?",
                        (
                            "A trimmed profile leaves a fine frame visible around the luminaire and covers the ceiling cut edge. A trimless profile is fixed before final finishing so plaster and paint integrate its edge with the architectural surface. The choice therefore changes the construction sequence and tolerance, not only the appearance.",
                            "The <a href='/en/linear/c/recessed/'>recessed linear lighting guide</a> compares Verona families using this distinction. Decide before the ceiling is closed because channel width, installation depth, driver position and maintenance access all belong in the coordinated detail.",
                        ),
                    ),
                    Section(
                        "When is a trimmed profile practical?",
                        (
                            "A trimmed system is often more controllable where programme, normal cut-out tolerance or later installation matters. The fine edge can manage small differences between the channel and housing and gives the line a clearly defined boundary.",
                            "Accurate alignment, diffuser continuity and equipment access are still required. For a narrow example, compare the project section with the data for <a href='/en/linear/c/recessed/sp/sp-narrow/'>SP NARROW trimmed recessed linear light</a>.",
                        ),
                    ),
                    Section(
                        "When does trimless add value?",
                        (
                            "Trimless is valuable when the design intends the light to read as part of the ceiling rather than as a framed fitting. The result can be more minimal, but it depends directly on framing accuracy, profile alignment and final finishing. Correction after painting is normally more disruptive.",
                            "The architect, ceiling contractor and supplier should approve one section before ordering. The <a href='/en/linear/c/recessed/BD/bd-narrow/'>BD NARROW trimless recessed linear light</a> page shows the kind of product information that should be checked against the ceiling plan.",
                        ),
                    ),
                    Section(
                        "Light performance, maintenance and total cost",
                        (
                            "Trim condition does not determine output or light quality. Compare lumens per metre, watts per metre, CRI, colour temperature, optics and total line length. Products with similar proportions may deliver different performance.",
                            "Total cost also includes framing, finishing time, driver and cabling access, and the risk of remedial ceiling work. The right system matches both the architectural language and the project’s ability to execute and maintain it.",
                        ),
                    ),
                    Section(
                        "A final decision checklist",
                        (
                            "Record the ceiling type, installation sequence, channel dimensions, driver access, expected edge quality, line length and target illuminance before ordering. A small mock-up is useful where the contractor has limited trimless experience.",
                            "Once the trim condition is selected, confirm the exact model against current product data. Continue with the guide to <a href='/en/news/recessed-linear-lighting-knauf-ceiling-installation/'>recessed linear lighting in plasterboard ceilings</a> for the coordination sequence.",
                        ),
                    ),
                ),
            ),
        },
    ),
    "recessed-linear-lighting-knauf-ceiling-installation": EditorialArticle(
        cluster="recessed-linear",
        cover_image="products/Sepehr_Narrow_render.png",
        read_time=8,
        published_at="2026-07-10",
        translations={
            "fa": ArticleTranslation(
                keyword="نصب چراغ خطی توکار در سقف کناف",
                title="نصب چراغ خطی توکار در سقف کناف؛ چک‌لیست قبل از اجرا",
                excerpt=(
                    "راهنمای هماهنگی چراغ خطی توکار با سقف کناف؛ از انتخاب پروفیل "
                    "و شیار تا درایور، کابل، تست اولیه و دسترسی نگهداری."
                ),
                meta_title="نصب چراغ خطی توکار در سقف کناف؛ چک‌لیست اجرا",
                meta_description=(
                    "برای نصب چراغ خطی توکار در سقف کناف، ترتیب هماهنگی شیار، "
                    "زیرسازی، درایور، کابل‌کشی، تراز، تست و دسترسی نگهداری را بررسی کنید."
                ),
                sections=(
                    Section(
                        "کار از انتخاب مدل قطعی شروع می‌شود",
                        (
                            "ابعاد شیار را از روی نام عمومی «چراغ خطی» یا تصویر تعیین نکنید. ابتدا خانواده و مدل قطعی، نوع لبه، مقطع پروفیل، طول شاخه‌ها و تجهیزات الکتریکی مشخص شوند. سپس مقطع تأییدشده وارد نقشه کناف شود.",
                            "در <a href='/linear/c/recessed/'>صفحه چراغ خطی توکار</a> می‌توانید تفاوت خانواده‌های لبه‌دار و بدون لبه را ببینید. مدل لبه‌دار و تریم‌لس ترتیب نصب یکسانی ندارند و تغییر تصمیم پس از زیرسازی می‌تواند به اصلاح سقف منجر شود.",
                        ),
                    ),
                    Section(
                        "زیرسازی، شیار و مسیر پیوسته",
                        (
                            "مسیر خط نور را با سازه سقف، دریچه‌ها، سنسورها، اسپرینکلر و تجهیزات مکانیکی تداخل‌سنجی کنید. محل اتصال شاخه‌ها و گوشه‌ها باید پشتوانه سازه‌ای کافی داشته باشد تا پروفیل در طول مسیر موج یا شکست پیدا نکند.",
                            "برای مدل لبه‌دار باریک مانند <a href='/linear/c/recessed/sp/sp-narrow/'>SP NARROW</a> عرض برش و تلرانس فریم اهمیت دارد. در مدل بدون لبه مانند <a href='/linear/c/recessed/BD/bd-narrow/'>BD NARROW</a> تراز بدنه و پرداخت پیرامون پروفیل بخشی از کیفیت نهایی است.",
                        ),
                    ),
                    Section(
                        "درایور، کابل و دسترسی سرویس",
                        (
                            "پیش از بسته‌شدن سقف، محل درایور، ورودی برق، طول کابل و روش دسترسی آینده را تعیین کنید. درایور نباید در نقطه‌ای قرار گیرد که برای تعویض آن نیاز به تخریب سقف باشد. الزامات تهویه و فاصله مجاز کابل را از اطلاعات تجهیزات همان پروژه بگیرید.",
                            "اتصالات الکتریکی و تست ایمنی باید توسط نیروی واجد صلاحیت انجام شود. این مقاله جایگزین نقشه اجرایی یا دستورالعمل سازنده نیست؛ هدف آن مشخص‌کردن نقاط هماهنگی میان معمار، برق‌کار و مجری سقف است.",
                        ),
                    ),
                    Section(
                        "تراز، تست اولیه و پرداخت",
                        (
                            "پیش از بتونه و رنگ، راستای پروفیل، پیوستگی خط، محل دیفیوزر و امکان جاگذاری تجهیزات را کنترل کنید. یک تست روشنایی اولیه می‌تواند مشکل کابل، اتصال یا درایور را پیش از پایان کار آشکار کند.",
                            "در سیستم تریم‌لس، از پروفیل در برابر مصالح و رنگ محافظت کنید و پرداخت را بدون ایجاد موج انجام دهید. در مدل لبه‌دار نیز لبه نباید برای جبران شیار نامنظم تحت فشار یا پیچش قرار گیرد.",
                        ),
                    ),
                    Section(
                        "تحویل و نگهداری",
                        (
                            "پس از نصب، مدل چراغ، طول‌ها، محل درایورها و مسیر دسترسی را در نقشه چون‌ساخت ثبت کنید. دیفیوزر و سطح نور را با روش مناسب تمیز کنید و قطعات سازگار را برای تعمیرات آینده مشخص نگه دارید.",
                            "اگر هنوز میان دو روش نصب تصمیم نگرفته‌اید، مقاله <a href='/news/trimmed-vs-trimless-recessed-linear-lighting/'>تفاوت چراغ خطی توکار لبه‌دار و بدون لبه</a> معیارهای تصمیم را جمع‌بندی می‌کند.",
                        ),
                    ),
                ),
            ),
            "en": ArticleTranslation(
                keyword="recessed linear lighting plasterboard ceiling installation",
                title="Recessed linear lighting in plasterboard ceilings: a coordination checklist",
                excerpt=(
                    "A practical coordination guide covering profile selection, channel framing, "
                    "drivers, cabling, testing and maintenance access."
                ),
                meta_title="Recessed Linear Lighting Ceiling Installation Guide",
                meta_description=(
                    "Plan recessed linear lighting in plasterboard ceilings by coordinating "
                    "the channel, framing, driver, cabling, alignment, testing and maintenance access."
                ),
                sections=(
                    Section(
                        "Begin with the confirmed product",
                        (
                            "Do not set the channel from a generic product name or photograph. Confirm the family, model, trim condition, profile section, line lengths and electrical equipment first, then place the approved section in the ceiling documentation.",
                            "The <a href='/en/linear/c/recessed/'>recessed linear lighting page</a> explains trimmed and trimless families. Their installation sequences differ, and changing the decision after framing can require ceiling rework.",
                        ),
                    ),
                    Section(
                        "Framing, channels and continuous routes",
                        (
                            "Coordinate the light route with ceiling framing, access panels, sensors, sprinklers and mechanical services. Joints and corners need adequate support so the profile remains straight without waves or visible steps.",
                            "For a narrow trimmed model such as <a href='/en/linear/c/recessed/sp/sp-narrow/'>SP NARROW</a>, cut-out tolerance and trim width matter. With a trimless model such as <a href='/en/linear/c/recessed/BD/bd-narrow/'>BD NARROW</a>, housing alignment and finishing around the profile become part of the visible result.",
                        ),
                    ),
                    Section(
                        "Drivers, cabling and service access",
                        (
                            "Define the driver, feed point, cable length and future access before closing the ceiling. Avoid locations that would require destructive work for replacement. Follow the equipment data for ventilation and permitted cable distances.",
                            "Electrical connections and safety testing belong with qualified personnel. This guide does not replace the manufacturer’s instructions or project drawings; it identifies the coordination responsibilities shared by the architect, electrician and ceiling contractor.",
                        ),
                    ),
                    Section(
                        "Alignment, early testing and finishing",
                        (
                            "Before plastering and paint, inspect profile alignment, line continuity, diffuser position and equipment fit. An early lighting test can expose a cable, connection or driver issue while access is still available.",
                            "Protect trimless profiles from finishing materials and avoid waves along the edge. A trimmed profile should not be twisted or loaded to compensate for an irregular channel.",
                        ),
                    ),
                    Section(
                        "Handover and maintenance",
                        (
                            "Record luminaire models, line lengths, driver locations and access routes in the as-built information. Keep compatible component references available for future maintenance and use appropriate methods to clean the diffuser.",
                            "If the trim condition is not yet resolved, read <a href='/en/news/trimmed-vs-trimless-recessed-linear-lighting/'>trimmed vs trimless recessed linear lighting</a> before finalising the section.",
                        ),
                    ),
                ),
            ),
        },
    ),
    "what-is-magnetic-track-lighting": EditorialArticle(
        cluster="magnetic-track",
        cover_image="products/magnetar_linear_2cm.png",
        read_time=8,
        published_at="2026-07-17",
        translations={
            "fa": ArticleTranslation(
                keyword="چراغ مگنتی چیست",
                title="چراغ مگنتی چیست؟ اجزای سیستم و نکات انتخاب برای پروژه",
                excerpt=(
                    "آشنایی با ریل، منبع تغذیه، اتصال‌ها و ماژول‌های چراغ مگنتی "
                    "و روشی برای انتخاب یک سیستم سازگار و قابل توسعه."
                ),
                meta_title="چراغ مگنتی چیست؟ اجزا و راهنمای انتخاب سیستم",
                meta_description=(
                    "چراغ مگنتی چیست و چه اجزایی دارد؟ ریل، منبع تغذیه، اتصال‌ها، "
                    "ماژول‌های خطی و اسپات و نکات سازگاری سیستم ۴۸ ولت را بررسی کنید."
                ),
                sections=(
                    Section(
                        "چراغ مگنتی یک سیستم است، نه یک قطعه",
                        (
                            "چراغ مگنتی از ریل کم‌ولتاژ، منبع تغذیه، اتصال‌ها و ماژول‌های نوری سازگار تشکیل می‌شود. اتصال مغناطیسی نصب و جابه‌جایی ماژول را ساده می‌کند، اما سازگاری مکانیکی و الکتریکی اجزا همچنان ضروری است.",
                            "برای مشاهده ساختار خانواده‌ها، صفحه <a href='/low-voltage-magneto/'>راهنمای چراغ مگنتی و ریل مگنتی</a> را ببینید. انتخاب درست از ریل و روش نصب شروع می‌شود، نه از ظاهر یک ماژول منفرد.",
                        ),
                    ),
                    Section(
                        "اجزای اصلی سیستم",
                        (
                            "ریل مسیر مکانیکی و الکتریکی را ایجاد می‌کند؛ منبع تغذیه ولتاژ موردنیاز سیستم را تأمین می‌کند؛ رابط‌ها مسیر مستقیم، گوشه یا انشعاب را می‌سازند؛ و ماژول‌های خطی، اسپات، پنل یا آویز نقش‌های نوری متفاوتی دارند.",
                            "ظرفیت منبع تغذیه باید با مجموع بار ماژول‌ها و شرایط طراحی هماهنگ شود. محل تغذیه، طول مسیر و تعداد اتصال‌ها پیش از سفارش روی نقشه مشخص شوند تا فهرست قطعات ناقص نباشد.",
                        ),
                    ),
                    Section(
                        "Small یا Large؛ تفاوت فقط نام نیست",
                        (
                            "خانواده‌های Small و Large مقطع، مقیاس بصری و اجزای سازگار متفاوتی دارند. مدل Small برای حضور ظریف‌تر ریل قابل بررسی است؛ Large خط معماری خواناتری ایجاد می‌کند. قطعات دو خانواده را بدون تأیید سازنده ترکیب نکنید.",
                            "برای مقایسه ماژول‌های خطی، صفحات <a href='/low-voltage-magneto/c/magent-small-family/magnet-linear/magnetar-small-linear/'>MAGNETO SMALL LINEAR</a> و <a href='/low-voltage-magneto/c/magent-large4cm-family/magnet-linear/magnetar-large-linear/'>MAGNETO LARGE LINEAR</a> را بررسی کنید.",
                        ),
                    ),
                    Section(
                        "چگونه ترکیب ماژول‌ها را انتخاب کنیم؟",
                        (
                            "ماژول خطی معمولاً برای نور پایه، اسپات برای تأکید روی اثر یا کالا، پنل برای سطح نور گسترده‌تر و آویز برای نزدیک‌کردن نور به میز یا کانتر استفاده می‌شود. ترکیب باید بر اساس کاربری، خیرگی، ارتفاع سقف و سناریوی کنترل انتخاب شود.",
                            "تعداد بیشتر چراغ همیشه نتیجه بهتر نمی‌دهد. یک طراحی متعادل میان نور عمومی و تأکیدی تفاوت می‌گذارد و فضای خالی روی ریل را برای تغییرات آینده حفظ می‌کند.",
                        ),
                    ),
                    Section(
                        "چک‌لیست سفارش سیستم مگنتی",
                        (
                            "خانواده ریل، روش نصب، مسیر و گوشه‌ها، محل ورودی برق، ظرفیت منبع، نوع و تعداد ماژول‌ها، رنگ نور، CRI و کنترل را در یک فهرست واحد ثبت کنید. قیمت کل نیز باید بر اساس همین مجموعه محاسبه شود.",
                            "مرحله بعد، انتخاب نوع نصب ریل است. مقاله <a href='/news/recessed-surface-suspended-magnetic-track/'>تفاوت ریل مگنتی توکار، روکار و آویز</a> اثر هر روش بر سقف و ظاهر پروژه را توضیح می‌دهد.",
                        ),
                    ),
                ),
            ),
            "en": ArticleTranslation(
                keyword="what is magnetic track lighting",
                title="What is magnetic track lighting? System components and selection",
                excerpt=(
                    "Understand magnetic track, power supplies, connectors and light modules, "
                    "and learn how to specify one compatible, adaptable system."
                ),
                meta_title="What Is Magnetic Track Lighting? System Guide",
                meta_description=(
                    "What is magnetic track lighting? Review tracks, power supplies, connectors, "
                    "linear and spot modules, 48V compatibility and project selection."
                ),
                sections=(
                    Section(
                        "A system rather than a single fitting",
                        (
                            "Magnetic track lighting combines low-voltage track, a power supply, connectors and compatible light modules. Magnetic attachment simplifies placement and repositioning, but mechanical and electrical compatibility remains essential.",
                            "The <a href='/en/low-voltage-magneto/'>magnetic track lighting guide</a> maps Verona’s system families. A reliable specification starts with the track and mounting method, not with the appearance of one module.",
                        ),
                    ),
                    Section(
                        "The principal components",
                        (
                            "Track provides the mechanical and electrical route; the power supply serves the system voltage; connectors form straight runs, corners and branches; linear, spot, panel and pendant modules perform different lighting roles.",
                            "Power-supply capacity must suit the connected load and project conditions. Plot the feed location, route length and connectors before ordering so the component schedule is complete.",
                        ),
                    ),
                    Section(
                        "Small or Large is a system decision",
                        (
                            "Small and Large families differ in section, visual scale and compatible components. Small can provide a finer track presence; Large creates a more legible architectural line. Do not mix components between families without explicit confirmation.",
                            "Compare the linear modules on the <a href='/en/low-voltage-magneto/c/magent-small-family/magnet-linear/magnetar-small-linear/'>MAGNETO SMALL LINEAR</a> and <a href='/en/low-voltage-magneto/c/magent-large4cm-family/magnet-linear/magnetar-large-linear/'>MAGNETO LARGE LINEAR</a> pages.",
                        ),
                    ),
                    Section(
                        "Composing the light modules",
                        (
                            "Linear modules generally support base light, spots add emphasis to art or merchandise, panels create a broader luminous surface and pendants bring light closer to a table or counter. Select the mix for use, glare, ceiling height and control scenes.",
                            "More modules do not automatically improve the result. A balanced design separates general and accent lighting and preserves useful free track for future adjustment.",
                        ),
                    ),
                    Section(
                        "An ordering checklist",
                        (
                            "Record the track family, mounting method, route and corners, power entry, supply capacity, module types and quantities, colour temperature, CRI and controls in one coordinated schedule. Price the complete system, not one luminaire.",
                            "The next decision is mounting. Read <a href='/en/news/recessed-surface-suspended-magnetic-track/'>recessed, surface and suspended magnetic track compared</a> for their ceiling and visual implications.",
                        ),
                    ),
                ),
            ),
        },
    ),
    "recessed-surface-suspended-magnetic-track": EditorialArticle(
        cluster="magnetic-track",
        cover_image="products/magnetar_linear_4cm.png",
        read_time=7,
        published_at="2026-07-24",
        translations={
            "fa": ArticleTranslation(
                keyword="تفاوت ریل مگنتی توکار روکار و آویز",
                title="تفاوت ریل مگنتی توکار، روکار و آویز در طراحی و اجرا",
                excerpt=(
                    "مقایسه سه روش نصب ریل مگنتی از نظر زیرسازی، ارتفاع سقف، "
                    "ظاهر معماری، دسترسی نگهداری و زمان مناسب تصمیم‌گیری."
                ),
                meta_title="تفاوت ریل مگنتی توکار، روکار و آویز",
                meta_description=(
                    "تفاوت ریل مگنتی توکار، روکار و آویز را از نظر زیرسازی، "
                    "ارتفاع سقف، ظاهر، اجرا و نگهداری بررسی کنید و روش مناسب پروژه را انتخاب کنید."
                ),
                sections=(
                    Section(
                        "روش نصب چه چیزی را تغییر می‌دهد؟",
                        (
                            "ریل توکار در ساختار سقف ادغام می‌شود، ریل روکار روی سطح نهایی قرار می‌گیرد و ریل آویز با کابل یا اتصالات مناسب پایین‌تر از سقف تعریف می‌شود. هر سه می‌توانند ماژول‌های سازگار یک خانواده را حمل کنند، اما دیتیل معماری و زمان تصمیم‌گیری آن‌ها متفاوت است.",
                            "پیش از مقایسه نصب، خانواده سیستم را در <a href='/low-voltage-magneto/'>راهنمای چراغ مگنتی</a> انتخاب کنید. ابعاد ریل، منبع تغذیه و اتصال‌های هر خانواده باید در کل مسیر یکپارچه باشند.",
                        ),
                    ),
                    Section(
                        "ریل مگنتی توکار",
                        (
                            "توکار برای سقف کاذب و پروژه‌ای مناسب است که می‌خواهد حضور بدنه ریل کم شود. این روش به شیار، زیرسازی، تراز دقیق و هماهنگی قبل از پرداخت سقف نیاز دارد. محل تغذیه و دسترسی سرویس نباید پشت سطحی غیرقابل دسترس پنهان شود.",
                            "مزیت اصلی یکپارچگی معماری است؛ ریسک اصلی، تصمیم دیرهنگام و اصلاح سقف. مقطع ریل قطعی باید پیش از اجرای سازه به تیم کناف برسد.",
                        ),
                    ),
                    Section(
                        "ریل مگنتی روکار",
                        (
                            "روکار برای نصب روی سطح موجود یا پروژه‌ای با محدودیت شیار و عمق سقف قابل بررسی است. بدنه ریل دیده می‌شود و باید رنگ، مقطع و راستای آن بخشی از ترکیب معماری باشد. نصب مستقیم‌تر به معنی حذف نیاز به نقشه برق و اتصال‌ها نیست.",
                            "این روش معمولاً دسترسی نگهداری واضح‌تری دارد و برای بازسازی می‌تواند عملی‌تر باشد. سطح زیر ریل باید ظرفیت تثبیت مناسب و مسیر تغذیه کنترل‌شده داشته باشد.",
                        ),
                    ),
                    Section(
                        "ریل مگنتی آویز",
                        (
                            "آویز در سقف بلند، فضای با تأسیسات نمایان یا جایی که خط نور باید به تراز کار نزدیک شود قابل استفاده است. ارتفاع آویز، نقاط مهار، تراز افقی و مدیریت کابل برق بر کیفیت نتیجه اثر مستقیم دارند.",
                            "خط آویز حضور بصری قوی‌تری دارد؛ بنابراین فاصله از دیوار، میز، کانتر و سایر خطوط سقف باید در نما و مقطع دیده شود. مهار مکانیکی باید توسط تیم اجرایی واجد صلاحیت طراحی و کنترل شود.",
                        ),
                    ),
                    Section(
                        "انتخاب نهایی و اشتباه‌های رایج",
                        (
                            "نوع سقف، ارتفاع، برنامه اجرا، امکان زیرسازی، حضور بصری مطلوب، دسترسی سرویس و تغییرات آینده را مقایسه کنید. سپس مسیر، گوشه‌ها، منبع تغذیه و ماژول‌ها را برای همان روش نصب نهایی کنید.",
                            "خرید چراغ قبل از قطعی‌شدن ریل، ترکیب خانواده‌های ناسازگار و فراموش‌کردن ظرفیت منبع از اشتباه‌های پرهزینه هستند. اگر با اجزای سیستم آشنا نیستید، ابتدا مقاله <a href='/news/what-is-magnetic-track-lighting/'>چراغ مگنتی چیست</a> را مطالعه کنید.",
                        ),
                    ),
                ),
            ),
            "en": ArticleTranslation(
                keyword="recessed surface suspended magnetic track",
                title="Recessed, surface or suspended magnetic track: design and installation",
                excerpt=(
                    "Compare three magnetic-track mounting methods for ceiling preparation, "
                    "visual impact, maintenance access and project timing."
                ),
                meta_title="Recessed, Surface or Suspended Magnetic Track",
                meta_description=(
                    "Compare recessed, surface and suspended magnetic track for ceiling "
                    "preparation, height, appearance, installation, maintenance and project use."
                ),
                sections=(
                    Section(
                        "What does the mounting method change?",
                        (
                            "Recessed track is integrated into the ceiling, surface track sits on the finished plane and suspended track defines a line below it. All may carry compatible modules within one family, but their architectural details and decision times differ.",
                            "Choose the system family first using the <a href='/en/low-voltage-magneto/'>magnetic track lighting guide</a>. Track dimensions, power supply and connectors must remain coordinated throughout the route.",
                        ),
                    ),
                    Section(
                        "Recessed magnetic track",
                        (
                            "Recessed mounting suits suspended ceilings and projects that want a lower visual presence from the track body. It needs a channel, support framing, accurate alignment and coordination before finishing. Power and service access must not disappear behind an inaccessible surface.",
                            "Its principal benefit is architectural integration; its main risk is a late decision that requires ceiling rework. Give the confirmed track section to the ceiling team before framing.",
                        ),
                    ),
                    Section(
                        "Surface magnetic track",
                        (
                            "Surface mounting can suit an existing plane or a project with limited channel depth. The track remains visible, so its colour, section and alignment become part of the composition. Direct installation does not remove the need to plan power and connectors.",
                            "Maintenance access is usually clearer, and the method can be practical in refurbishment. The supporting surface must accept secure fixing and a controlled power route.",
                        ),
                    ),
                    Section(
                        "Suspended magnetic track",
                        (
                            "Suspended track can suit high ceilings, exposed services or a design that brings the light line closer to the working plane. Suspension height, fixing points, horizontal alignment and cable management directly affect the result.",
                            "Because the line has a stronger visual presence, its relationship to walls, tables, counters and other ceiling lines should be resolved in elevation and section. Qualified teams must design and verify the mechanical support.",
                        ),
                    ),
                    Section(
                        "Final selection and common mistakes",
                        (
                            "Compare ceiling type, height, programme, available framing, desired visual presence, service access and future change. Then coordinate the route, corners, power supply and modules for the selected mounting method.",
                            "Ordering modules before confirming the track, mixing incompatible families and overlooking supply capacity are costly mistakes. If the system components are unfamiliar, begin with <a href='/en/news/what-is-magnetic-track-lighting/'>what is magnetic track lighting?</a>",
                        ),
                    ),
                ),
            ),
        },
    ),
}


def render_article_body(content):
    parts = []
    for section in content.sections:
        parts.append(f"<h2>{escape(section.heading)}</h2>")
        parts.extend(f"<p>{paragraph}</p>" for paragraph in section.paragraphs)
    return "".join(parts)


def validate_editorial_articles():
    if len(EDITORIAL_ARTICLES) != 4:
        raise ValueError("Step 6 must contain four supporting articles.")

    keywords = {"fa": set(), "en": set()}
    for slug, article in EDITORIAL_ARTICLES.items():
        if set(article.translations) != {"fa", "en"}:
            raise ValueError(f"{slug} must provide Persian and English content.")
        for language, content in article.translations.items():
            if not 35 <= len(content.meta_title) <= 60:
                raise ValueError(f"{slug}/{language} meta title length is invalid.")
            if not 110 <= len(content.meta_description) <= 160:
                raise ValueError(f"{slug}/{language} meta description length is invalid.")
            body = render_article_body(content)
            visible = re.sub(r"<[^>]+>", " ", body)
            visible = " ".join(visible.split())
            if len(visible) < 1800:
                raise ValueError(f"{slug}/{language} article is too thin.")
            if body.count("<h2>") != 5 or body.count("<a href=") < 2:
                raise ValueError(f"{slug}/{language} structure or links are incomplete.")
            if content.keyword.casefold() in keywords[language]:
                raise ValueError(f"{slug}/{language} duplicates an article keyword.")
            keywords[language].add(content.keyword.casefold())


def build_editorial_links(cluster, language_code):
    language = "fa" if language_code == "fa" else "en"
    links = []
    for slug, article in EDITORIAL_ARTICLES.items():
        if article.cluster != cluster:
            continue
        content = article.translations[language]
        links.append(
            {
                "url": reverse("news_detail", kwargs={"slug": slug}),
                "label": content.title,
                "description": content.excerpt,
            }
        )

    if language == "fa":
        heading = "راهنماهای تخصصی مرتبط"
        intro = (
            "برای تصمیم‌گیری اجرایی و مقایسه دقیق‌تر، راهنماهای تخصصی این "
            "موضوع را مطالعه کنید."
        )
    else:
        heading = "Related technical guides"
        intro = (
            "Continue with these focused guides for installation decisions and "
            "a more detailed system comparison."
        )
    return {"heading": heading, "intro": intro, "links": links}
