"""Reviewed bilingual copy for Verona Lighting product category pages."""

from dataclasses import dataclass


@dataclass(frozen=True)
class CategoryContent:
    description_fa: str
    description_en: str
    meta_title_fa: str
    meta_title_en: str
    meta_description_fa: str
    meta_description_en: str


CATEGORY_CONTENT = {
    "low-voltage-magneto": CategoryContent(
        description_fa=(
            "چراغ مگنتی ریلی ورونا یک سیستم روشنایی ماژولار برای فضاهای معماری است که امکان ترکیب چراغ‌های "
            "خطی، نقطه‌ای، اسپات، آویز و ماژول‌های زاویه‌پذیر را روی یک ساختار مشترک فراهم می‌کند. در این "
            "دسته می‌توانید خانواده‌های مگنت اسمال، مگنت لارج، کرو، بلت و فلکسی را بررسی کنید و میان ریل‌های "
            "توکار بدون لبه، روکار و آویز مقایسه انجام دهید. برای انتخاب دقیق، به ابعاد ریل، نوع نصب، شکل "
            "پخش نور و نقش هر ماژول در نور عمومی یا تأکیدی توجه کنید. صفحات خانواده و محصول، تصاویر و "
            "مشخصات ثبت‌شده هر مدل را برای تصمیم‌گیری پروژه‌ای در اختیار شما قرار می‌دهند."
        ),
        description_en=(
            "Verona magnetic track lighting is a modular architectural system that brings linear, dot, spot, "
            "pendant and adjustable light modules onto a shared track platform. This category brings together "
            "the Magneto Small, Large, Curve, Belt and Flexi ranges, along with recessed trimless, surface and "
            "pendant track options. When comparing a system, consider the track dimensions, mounting method, "
            "light distribution and whether each module will provide general or accent lighting. Family and "
            "product pages present the available images and recorded specifications for project evaluation."
        ),
        meta_title_fa="چراغ مگنتی ریلی و مولتی ترک | ورونا لایتینگ",
        meta_title_en="Magnetic Track Lighting Systems | Verona Lighting",
        meta_description_fa="چراغ مگنتی ریلی ورونا را در مدل‌های اسمال، لارج، کرو، بلت و فلکسی بررسی کنید؛ مناسب مقایسه ریل و ماژول‌های نورپردازی معماری.",
        meta_description_en="Compare Verona magnetic track systems, including Small, Large, Curve, Belt and Flexi ranges with recessed, surface and pendant options.",
    ),
    "linear": CategoryContent(
        description_fa=(
            "چراغ خطی راهکاری منظم و انعطاف‌پذیر برای ایجاد خطوط پیوسته نور در معماری داخلی و محوطه است. "
            "مجموعه چراغ‌های خطی ورونا شامل مدل‌های توکار، روکار، آویز، دفنی و تجهیزات نور مخفی است تا نوع "
            "نصب متناسب با سقف، دیوار، کف یا جزئیات معماری انتخاب شود. تفاوت خانواده‌ها فقط در ظاهر نیست؛ "
            "عرض پروفیل، نحوه نصب، پیوستگی خط نور، نوع دیفیوزر و خروجی ثبت‌شده هر مدل باید با نیاز پروژه "
            "مقایسه شود. از زیرمجموعه‌های این صفحه می‌توانید به خانواده‌ها و مدل‌های مرتبط برسید و اطلاعات "
            "فنی موجود را پیش از مشخص‌کردن چراغ بررسی کنید."
        ),
        description_en=(
            "Linear lighting creates ordered, continuous lines of light across interior architecture and "
            "landscape details. Verona's linear collection is organised into recessed, surface-mounted, pendant, "
            "in-ground and cove-lighting categories so the mounting method can follow the ceiling, wall, floor or "
            "architectural detail. Selection should consider more than appearance: profile width, installation "
            "method, continuity of the light line, diffuser and the documented output of each model all affect the "
            "result. Use the subcategories to compare related families and review the available technical data "
            "before specifying a luminaire."
        ),
        meta_title_fa="چراغ خطی توکار، روکار و آویز | ورونا لایتینگ",
        meta_title_en="Architectural Linear Lighting | Verona Lighting",
        meta_description_fa="مدل‌های چراغ خطی توکار، روکار، آویز، دفنی و نور مخفی ورونا را براساس نوع نصب، ابعاد پروفیل و مشخصات فنی مقایسه کنید.",
        meta_description_en="Explore recessed, surface, pendant, in-ground and cove linear lighting by Verona, with product families and technical details.",
    ),
    "panel-downlight": CategoryContent(
        description_fa=(
            "چراغ پنل و دانلایت برای تأمین نور سقفی در فضاهای اداری، تجاری، مسکونی و عمومی استفاده می‌شود و "
            "انتخاب درست آن به نوع سقف و کیفیت نور موردنیاز وابسته است. در این بخش می‌توانید پنل‌ها و چراغ‌های "
            "توکار ورونا را در فرم‌های دایره‌ای، مربعی، تک‌خانه و چندخانه بررسی کنید. ابعاد برش، توان، شار "
            "نوری، دمای رنگ، شاخص نمود رنگ و نوع نصب از مهم‌ترین مواردی هستند که باید میان مدل‌ها مقایسه شوند. "
            "اطلاعات هر محصول براساس داده‌های ثبت‌شده در کاتالوگ نمایش داده می‌شود تا انتخاب برای پلان روشنایی "
            "و هماهنگی با جزئیات سقف دقیق‌تر باشد."
        ),
        description_en=(
            "Panel lights and downlights provide ceiling illumination for offices, commercial interiors, homes "
            "and public spaces, with the right choice depending on the ceiling and required light quality. This "
            "section presents Verona panel and recessed luminaires in round, square, single and multi-cell forms. "
            "Cut-out dimensions, wattage, luminous flux, colour temperature, colour rendering and mounting type "
            "are the main points to compare between models. Each product page uses the technical information "
            "recorded in the catalogue to support lighting layouts and coordination with ceiling details."
        ),
        meta_title_fa="چراغ پنل و دانلایت LED | ورونا لایتینگ",
        meta_title_en="LED Panel Lights and Downlights | Verona Lighting",
        meta_description_fa="چراغ پنل و دانلایت ورونا را در فرم‌ها و ابعاد مختلف بررسی و براساس نوع نصب، توان، شار نوری و مشخصات ثبت‌شده مقایسه کنید.",
        meta_description_en="Compare Verona LED panel lights and downlights by form, mounting type, dimensions and recorded lighting specifications.",
    ),
    "decorative": CategoryContent(
        description_fa=(
            "چراغ دکوراتیو علاوه بر روشنایی، بخشی از هویت بصری فضا را شکل می‌دهد و باید با مقیاس، متریال و "
            "زبان طراحی پروژه هماهنگ باشد. در مجموعه دکوراتیو ورونا می‌توانید خانواده‌هایی مانند HELY، ARIN، "
            "LIBER و BAMBO را در مدل‌های آویز یا دیواری بررسی کنید. هنگام انتخاب، به ابعاد چراغ، جهت تابش، "
            "ارتفاع نصب، ترکیب چند چراغ و ارتباط آن با مبلمان یا سطح مجاور توجه کنید. تصاویر و اطلاعات هر مدل "
            "کمک می‌کنند تناسب فرم چراغ با فضای پذیرایی، لابی، کافه، فروشگاه یا سایر محیط‌های معماری پیش از "
            "انتخاب نهایی ارزیابی شود."
        ),
        description_en=(
            "Decorative lighting contributes to the visual identity of a space as well as its illumination, so "
            "its scale, material language and form should relate to the project. Verona's decorative collection "
            "includes families such as HELY, ARIN, LIBER and BAMBO in pendant or wall-mounted configurations. "
            "When selecting a model, consider its dimensions, direction of light, mounting height, use in a group "
            "and relationship with nearby furniture or surfaces. Product images and recorded details help assess "
            "how each form may work in reception areas, lobbies, cafés, retail spaces and other interiors."
        ),
        meta_title_fa="چراغ دکوراتیو آویز و دیواری | ورونا لایتینگ",
        meta_title_en="Decorative Pendant and Wall Lighting | Verona Lighting",
        meta_description_fa="خانواده‌های چراغ دکوراتیو ورونا را در مدل‌های آویز و دیواری ببینید و فرم، ابعاد، جهت نور و تناسب آن‌ها با فضای معماری را مقایسه کنید.",
        meta_description_en="Explore Verona decorative pendant and wall lights, comparing form, dimensions, light direction and suitability for architectural interiors.",
    ),
    "industrial": CategoryContent(
        description_fa=(
            "چراغ صنعتی برای فضاهایی انتخاب می‌شود که ارتفاع نصب، وسعت محیط و نیاز به توزیع کنترل‌شده نور با "
            "چراغ‌های معمولی متفاوت است. در این دسته، مدل‌های صنعتی ورونا مانند Karen Highbay و TRITON برای "
            "بررسی در پروژه‌های سوله، انبار، سالن تولید و فضاهای فنی معرفی شده‌اند. پیش از انتخاب باید توان و "
            "شار نوری ثبت‌شده، زاویه یا الگوی پخش نور، ارتفاع نصب و شرایط محیط پروژه با یکدیگر سنجیده شوند. "
            "صفحه هر محصول اطلاعات و تصاویر موجود را نمایش می‌دهد تا مقایسه مدل‌ها بر پایه نیاز واقعی فضا و "
            "جانمایی چراغ‌ها انجام شود."
        ),
        description_en=(
            "Industrial luminaires are selected for spaces where mounting height, floor area and controlled light "
            "distribution differ from conventional interiors. This category presents Verona industrial models "
            "such as Karen Highbay and TRITON for evaluation in warehouses, production halls, workshops and "
            "technical spaces. Recorded wattage and luminous flux, beam or distribution pattern, mounting height "
            "and the environmental conditions of the project should be considered together. Each product page "
            "shows the available specifications and images so models can be compared against the actual layout "
            "and lighting requirements."
        ),
        meta_title_fa="چراغ صنعتی و چراغ سوله‌ای LED | ورونا لایتینگ",
        meta_title_en="Industrial and High-Bay LED Lighting | Verona Lighting",
        meta_description_fa="چراغ‌های صنعتی و سوله‌ای ورونا را برای انبار، سالن تولید و فضاهای فنی براساس توان، شار نوری، پخش نور و ارتفاع نصب بررسی کنید.",
        meta_description_en="Compare Verona industrial and high-bay luminaires for warehouses and production spaces using output, distribution and mounting data.",
    ),
    "spotlights-underwater": CategoryContent(
        description_fa=(
            "چراغ ضد آب و چراغ زیرآبی برای نقاطی در نظر گرفته می‌شود که تماس با رطوبت یا آب بخشی از شرایط "
            "کارکرد است. انتخاب این گروه باید با توجه به محل دقیق نصب، روش آب‌بندی، درجه حفاظت ثبت‌شده، جنس "
            "بدنه، ولتاژ و نحوه دسترسی برای سرویس انجام شود؛ صرف نام «ضد آب» برای تصمیم‌گیری کافی نیست. این "
            "صفحه محل معرفی مدل‌های مرتبط ورونا برای استخر، آب‌نما و جزئیات نورپردازی مرطوب است. پیش از تعیین "
            "محصول، مشخصات درج‌شده در صفحه همان مدل و الزامات اجرایی پروژه را بررسی کنید."
        ),
        description_en=(
            "Water-resistant and underwater luminaires are intended for locations where moisture or direct water "
            "contact forms part of the operating conditions. Selection must consider the exact installation "
            "location, sealing method, documented ingress rating, body material, voltage and access for service; "
            "a general waterproof label is not enough. This category is the catalogue location for relevant "
            "Verona models used around pools, fountains and wet architectural details. Always review the recorded "
            "specifications of the selected model together with the project's installation requirements."
        ),
        meta_title_fa="چراغ ضد آب و چراغ زیرآبی | ورونا لایتینگ",
        meta_title_en="Water-Resistant and Underwater Lighting | Verona",
        meta_description_fa="راهنمای بررسی چراغ ضد آب و زیرآبی ورونا برای استخر، آب‌نما و فضاهای مرطوب براساس محل نصب، درجه حفاظت و مشخصات فنی هر مدل.",
        meta_description_en="Review Verona water-resistant and underwater lighting for pools, fountains and wet areas using installation and documented product data.",
    ),
    "spotlights-track-lighting": CategoryContent(
        description_fa=(
            "چراغ ریلی امکان جابه‌جایی و تنظیم جهت نور را در امتداد ریل فراهم می‌کند و برای نورپردازی "
            "فروشگاه، گالری، فضای نمایش و پروژه‌های تجاری کاربرد دارد. مجموعه ترک لایت ورونا به دو گروه ریل "
            "تک‌فاز و سه‌فاز تقسیم شده است و شامل چراغ‌های اسپات، مدل‌های آویز و قطعات اتصال ریل می‌شود. نوع "
            "ریل و سازگاری چراغ یا کانکتور باید پیش از انتخاب مشخص شود؛ قطعات دو سیستم جایگزین یکدیگر نیستند. "
            "برای مقایسه مدل‌ها، به نوع نصب ریل، ابعاد، توان، زاویه تابش و اطلاعات ثبت‌شده در صفحه محصول توجه کنید."
        ),
        description_en=(
            "Track lighting allows luminaires to be repositioned and aimed along a rail, making it useful for "
            "retail, galleries, displays and commercial interiors. Verona track lighting is organised into "
            "single-phase and three-phase systems and includes spotlights, pendant models and track connectors. "
            "The rail type and compatibility of every luminaire or connector must be confirmed before selection, "
            "as components from the two systems are not interchangeable. Compare mounting method, dimensions, "
            "wattage, beam information and the specifications recorded on each product page."
        ),
        meta_title_fa="چراغ ریلی فروشگاهی تک‌فاز و سه‌فاز | ورونا",
        meta_title_en="Single and Three-Phase Track Lighting | Verona",
        meta_description_fa="چراغ ریلی فروشگاهی ورونا را در سیستم‌های تک‌فاز و سه‌فاز بررسی کنید؛ شامل اسپات، آویز، ریل و قطعات اتصال متناسب با هر سیستم.",
        meta_description_en="Explore Verona single-phase and three-phase track lighting, including spotlights, pendants, rails and compatible connectors.",
    ),
    "outdoor": CategoryContent(
        description_fa=(
            "چراغ فضای باز باید علاوه بر کیفیت نور، با شرایط نصب و معماری محوطه هماهنگ باشد. در این دسته، "
            "خانواده‌های فضای باز ورونا مانند MOON و ROSHANA برای بررسی در مسیرهای حرکتی، حیاط، باغ، ورودی "
            "ساختمان و جزئیات نمای بیرونی معرفی شده‌اند. محل نصب، جهت تابش، ارتفاع، درجه حفاظت ثبت‌شده و "
            "نحوه کابل‌کشی از معیارهای اصلی مقایسه هستند. مشخصات هر مدل را جداگانه بررسی کنید تا چراغ متناسب "
            "با عملکرد موردنظر انتخاب شود و از به‌کاربردن یک مدل در شرایطی خارج از اطلاعات فنی آن جلوگیری شود."
        ),
        description_en=(
            "Outdoor lighting must respond to installation conditions as well as the visual character of the "
            "landscape. This category presents Verona outdoor families such as MOON and ROSHANA for evaluation "
            "along paths, courtyards, gardens, entrances and exterior architectural details. Mounting location, "
            "aiming direction, height, documented ingress rating and cable routing are key comparison points. "
            "Review the specifications of each model separately so the luminaire matches its intended task and "
            "is not used beyond the conditions stated in its technical information."
        ),
        meta_title_fa="چراغ فضای باز و محوطه | ورونا لایتینگ",
        meta_title_en="Outdoor and Landscape Lighting | Verona Lighting",
        meta_description_fa="چراغ‌های فضای باز ورونا را برای مسیر، حیاط، باغ و ورودی ساختمان براساس محل نصب، جهت تابش و مشخصات فنی هر مدل مقایسه کنید.",
        meta_description_en="Compare Verona outdoor luminaires for paths, gardens, courtyards and entrances using mounting, aiming and documented product data.",
    ),
    "accessories": CategoryContent(
        description_fa=(
            "اکسسوری روشنایی شامل قطعاتی است که نصب، اتصال یا تکمیل عملکرد سیستم نورپردازی را ممکن می‌کنند. "
            "ریل، کانکتور، رابط، قطعه تغذیه و متعلقات نصب باید دقیقاً با خانواده و مدل چراغ سازگار باشند؛ شباهت "
            "ظاهری یک قطعه به معنی سازگاری الکتریکی یا مکانیکی آن نیست. در این دسته می‌توانید لوازم جانبی "
            "ثبت‌شده ورونا را بررسی کنید و از صفحه هر مورد به اطلاعات موجود برسید. برای انتخاب قطعه، نام "
            "سیستم، نوع ریل، ولتاژ و روش نصب پروژه را با مشخصات همان اکسسوری تطبیق دهید."
        ),
        description_en=(
            "Lighting accessories are the components used to install, connect or complete a lighting system. "
            "Rails, connectors, power feeds, joints and mounting parts must match the relevant luminaire family "
            "and model; visual similarity does not confirm electrical or mechanical compatibility. This category "
            "provides the catalogue location for Verona accessories and their available product information. "
            "When choosing a part, match the system name, rail type, voltage and installation method of the "
            "project with the specifications stated for that accessory."
        ),
        meta_title_fa="اکسسوری و قطعات سیستم روشنایی | ورونا",
        meta_title_en="Lighting Accessories and System Parts | Verona",
        meta_description_fa="اکسسوری‌های روشنایی ورونا شامل ریل، کانکتور و قطعات نصب را بررسی و سازگاری هر قطعه را با خانواده، ولتاژ و روش نصب کنترل کنید.",
        meta_description_en="Review Verona lighting accessories, rails, connectors and mounting parts, and confirm compatibility with the relevant system.",
    ),
    "magent-small-family": CategoryContent(
        description_fa=(
            "مگنت اسمال ۲ سانتی‌متری، بخش ظریف‌تر سیستم چراغ مگنتی ورونا است و برای پروژه‌هایی مناسب است که "
            "به خط ریل باریک‌تر و ماژول‌های کم‌حجم نیاز دارند. این مجموعه شامل ریل توکار بدون لبه، ریل روکار "
            "و آویز، چراغ خطی، دات‌لاینر، اسپات، آویز و مدل‌های چرخشی یا زاویه‌دار است. هنگام ترکیب قطعات، "
            "همه اجزا باید از خانواده Small انتخاب شوند. برای مقایسه، نوع ماژول، ابعاد، توان، شار نوری و "
            "زاویه تابش ثبت‌شده در هر محصول را در کنار نوع نصب ریل بررسی کنید."
        ),
        description_en=(
            "The 2 cm Magneto Small range is the slimmer part of Verona's magnetic lighting system, intended for "
            "projects that require a narrower track line and compact modules. The range includes recessed "
            "trimless, surface and pendant tracks together with linear, dot-linear, spot, pendant, rotating and "
            "angled luminaires. All combined components should belong to the Small family. Compare module type, "
            "dimensions, wattage, luminous flux and recorded beam information alongside the selected track "
            "installation method."
        ),
        meta_title_fa="چراغ مگنتی اسمال ۲ سانتی‌متر | ورونا",
        meta_title_en="Magneto Small 2 cm Track Lighting | Verona",
        meta_description_fa="ریل و چراغ مگنتی اسمال ۲ سانتی‌متر ورونا را در مدل‌های خطی، اسپات، آویز و زاویه‌پذیر با روش‌های نصب مختلف مقایسه کنید.",
        meta_description_en="Compare Verona Magneto Small 2 cm tracks and compact linear, spot, pendant, rotating and angled light modules.",
    ),
    "magent-large4cm-family": CategoryContent(
        description_fa=(
            "مگنت لارج ۴ سانتی‌متری خانواده‌ای از سیستم مولتی ترک ورونا با ریل و ماژول‌های بزرگ‌تر است. در "
            "این مجموعه می‌توانید ریل توکار بدون لبه، روکار و آویز را در کنار چراغ‌های خطی، دات‌لاینر، اسپات، "
            "پنل اسپات، آویز و مدل‌های چرخشی یا زاویه‌دار بررسی کنید. انتخاب ریل و تمام متعلقات باید از خانواده "
            "Large انجام شود تا هماهنگی مکانیکی سیستم حفظ شود. برای مشخص‌کردن مدل مناسب، ابعاد، نوع نصب، "
            "توان، شار نوری و اطلاعات اپتیکی درج‌شده در صفحه هر محصول را مقایسه کنید."
        ),
        description_en=(
            "Magneto Large is Verona's 4 cm multi-track family, using larger tracks and lighting modules. The "
            "range includes recessed trimless, surface and pendant tracks with linear, dot-linear, spot, spot-panel, "
            "pendant, rotating and angled luminaires. The track and its related components should all be selected "
            "from the Large family to retain mechanical compatibility. To specify a suitable model, compare its "
            "dimensions, mounting type, wattage, luminous flux and the optical information recorded on the "
            "individual product page."
        ),
        meta_title_fa="چراغ مگنتی لارج ۴ سانتی‌متر | ورونا",
        meta_title_en="Magneto Large 4 cm Track Lighting | Verona",
        meta_description_fa="سیستم مگنتی لارج ۴ سانتی‌متر ورونا را شامل ریل توکار، روکار و آویز و ماژول‌های خطی، اسپات و پنل بررسی کنید.",
        meta_description_en="Explore Verona Magneto Large 4 cm tracks and compatible linear, dot, spot, panel, pendant and adjustable modules.",
    ),
    "magnet-curve": CategoryContent(
        description_fa=(
            "مگنت کرو برای ایجاد مسیرهای منحنی نور در سیستم مگنتی طراحی شده و امکان ادامه‌دادن زبان خطی "
            "روشنایی در فرم‌های قوس‌دار را فراهم می‌کند. خانواده Magneto Curve شامل ریل منحنی و ماژول‌های "
            "خطی، دات‌لاینر و اسپات مرتبط است. پیش از انتخاب، شعاع و مسیر موردنیاز پروژه باید با شکل ریل و "
            "نحوه اتصال قطعات هماهنگ شود. نوع ماژول، تعداد چراغ‌ها، فاصله‌گذاری و اطلاعات توان و نور ثبت‌شده "
            "هر محصول نیز در کیفیت نهایی مسیر نور مؤثر است و باید به‌صورت یک سیستم بررسی شود."
        ),
        description_en=(
            "Magneto Curve extends magnetic lighting into curved paths, allowing a linear lighting language to "
            "follow arcs and rounded architectural forms. The family includes a curved track with related linear, "
            "dot-linear and spot modules. Before selection, the required radius and route of the project should be "
            "coordinated with the track geometry and component connections. Module type, quantity, spacing and the "
            "recorded wattage and light data of each product should be evaluated together as one system."
        ),
        meta_title_fa="چراغ مگنتی منحنی و ریل کرو | ورونا",
        meta_title_en="Curved Magnetic Track Lighting | Verona",
        meta_description_fa="ریل و چراغ مگنتی منحنی Magneto Curve ورونا را برای مسیرهای قوس‌دار با ماژول‌های خطی، دات‌لاینر و اسپات بررسی کنید.",
        meta_description_en="Explore Verona Magneto Curve track and compatible linear, dot-linear and spot modules for curved architectural light paths.",
    ),
    "mmagne-tbelt": CategoryContent(
        description_fa=(
            "مگنت بلت رویکردی نواری به روشنایی مگنتی دارد و اجزای نورپردازی آن روی ساختار انعطاف‌پذیر خانواده "
            "Belt قرار می‌گیرند. مدل‌های این بخش شامل نوار، اسپات، پنل اسپات، چراغ خطی، دات‌لاینر و فرم‌های "
            "Moon و Hat است. برای طراحی مسیر، طول و شکل قرارگیری بلت، نقاط اتصال و وزن و تعداد ماژول‌ها باید "
            "هم‌زمان بررسی شوند. سپس می‌توان توان، شار نوری، جهت تابش و ابعاد ثبت‌شده هر چراغ را براساس نقش "
            "آن در نور عمومی، تأکیدی یا دکوراتیو مقایسه کرد."
        ),
        description_en=(
            "Magneto Belt takes a ribbon-based approach to magnetic lighting, with light modules attached to the "
            "flexible structure of the Belt family. The range includes the belt itself, spots, spot panels, linear "
            "and dot-linear modules, plus Moon and Hat forms. Route length and shape, connection points, module "
            "weight and quantity should be considered together during planning. Recorded wattage, luminous flux, "
            "aiming direction and dimensions can then be compared according to each module's general, accent or "
            "decorative lighting role."
        ),
        meta_title_fa="چراغ مگنتی بلت و سیستم نواری | ورونا",
        meta_title_en="Magneto Belt Lighting System | Verona",
        meta_description_fa="سیستم چراغ مگنتی بلت ورونا را با ماژول‌های اسپات، پنل، خطی، دات‌لاینر و فرم‌های دکوراتیو برای مسیرهای نواری بررسی کنید.",
        meta_description_en="Explore Verona Magneto Belt with spot, panel, linear, dot-linear and decorative modules for ribbon-based lighting layouts.",
    ),
    "magnet-flexi": CategoryContent(
        description_fa=(
            "مگنت فلکسی برای شکل‌دادن مسیرهای آزادتر و منعطف‌تر در نورپردازی معماری در نظر گرفته شده است. "
            "خانواده Magneto Flexi شامل ساختار فلکسی و ماژول‌های خطی، تیوب، دات‌لاینر، اسپات و Moon می‌شود تا "
            "ترکیب نور پیوسته و تأکیدی در یک زبان طراحی امکان‌پذیر باشد. مسیر نصب، شعاع تغییر جهت، محل اتصالات "
            "و تعداد ماژول‌ها باید پیش از اجرا مشخص شود. برای انتخاب چراغ نیز ابعاد، توان، خروجی نور و سایر "
            "مشخصات درج‌شده در صفحه محصول را با نیاز پروژه مقایسه کنید."
        ),
        description_en=(
            "Magneto Flexi is intended for freer, more flexible lighting routes within architectural interiors. "
            "The family combines the Flexi structure with linear, tube, dot-linear, spot and Moon modules so "
            "continuous and accent light can share one visual language. The installation path, turning radius, "
            "connection points and number of modules should be planned before execution. When choosing a light "
            "module, compare its dimensions, wattage, output and the other specifications recorded on its product "
            "page with the needs of the project."
        ),
        meta_title_fa="چراغ مگنتی فلکسی و انعطاف‌پذیر | ورونا",
        meta_title_en="Magneto Flexi Lighting System | Verona",
        meta_description_fa="چراغ مگنتی فلکسی ورونا را با ماژول‌های خطی، تیوب، دات‌لاینر و اسپات برای طراحی مسیرهای منعطف نور بررسی کنید.",
        meta_description_en="Explore Verona Magneto Flexi with linear, tube, dot-linear, spot and Moon modules for flexible architectural lighting routes.",
    ),
    "magnet-super-slim": CategoryContent(
        description_fa=(
            "چراغ مگنتی سوپر اسلیم برای پروژه‌هایی تعریف می‌شود که در آن‌ها حداقل‌بودن عرض ریل و حضور بصری "
            "کمتر سیستم روشنایی اهمیت دارد. در چنین سیستمی، هماهنگی دقیق میان ریل، منبع تغذیه، اتصالات و "
            "ماژول‌های مخصوص همان خانواده ضروری است و نباید قطعات آن با خانواده‌های اسمال یا لارج جایگزین "
            "شوند. این صفحه برای معرفی محصولات Super Slim ورونا و اطلاعات فنی مربوط به آن‌ها در نظر گرفته "
            "شده است. هنگام انتشار مدل‌ها، ابعاد، نوع نصب، توان و خروجی ثبت‌شده هر محصول مبنای مقایسه خواهد بود."
        ),
        description_en=(
            "Super Slim magnetic lighting is intended for projects where minimum track width and a reduced visual "
            "presence are important. In this type of system, the track, power components, connectors and light "
            "modules must belong to the same compatible family and should not be substituted with Small or Large "
            "components. This page is reserved for Verona Super Slim products and their verified technical "
            "information. As models are added, their dimensions, mounting type, wattage and recorded output will "
            "provide the basis for comparison."
        ),
        meta_title_fa="چراغ مگنتی سوپر اسلیم | ورونا لایتینگ",
        meta_title_en="Super Slim Magnetic Track Lighting | Verona",
        meta_description_fa="معرفی سیستم چراغ مگنتی سوپر اسلیم ورونا برای مسیرهای ظریف نور؛ بررسی سازگاری ریل، اتصالات و ماژول‌های اختصاصی این خانواده.",
        meta_description_en="Discover Verona Super Slim magnetic lighting and the compatibility requirements for its narrow track, connectors and dedicated modules.",
    ),
    "pendant": CategoryContent(
        description_fa=(
            "چراغ خطی آویز برای ایجاد نور مستقیم یا ترکیبی در فضاهایی استفاده می‌شود که چراغ با فاصله از سقف "
            "قرار می‌گیرد و خودِ خط نور بخشی از ترکیب معماری است. خانواده MD LINEO ورونا در این دسته با "
            "مدل‌های MINI، NARROW، NARROW DOT و MID معرفی شده است. طول و ارتفاع آویز، محل قرارگیری نسبت به "
            "میز یا مسیر حرکت، عرض پروفیل و نوع پخش نور باید پیش از انتخاب هماهنگ شوند. مشخصات ثبت‌شده هر "
            "مدل را بررسی کنید تا تناسب ابعاد، توان و خروجی نور با مقیاس فضای پروژه مشخص شود."
        ),
        description_en=(
            "Pendant linear lighting is used where the luminaire is suspended below the ceiling and the visible "
            "line of light contributes to the architectural composition. Verona's MD LINEO family appears in this "
            "category through MINI, NARROW, NARROW DOT and MID models. Suspension length and height, position over "
            "a table or circulation route, profile width and light distribution should be coordinated before "
            "selection. Review each model's recorded specifications to relate its dimensions, wattage and output "
            "to the scale of the project."
        ),
        meta_title_fa="چراغ خطی آویز مدرن | ورونا لایتینگ",
        meta_title_en="Pendant Linear Lighting | Verona Lighting",
        meta_description_fa="چراغ خطی آویز MD LINEO ورونا را در ابعاد مختلف بررسی و ارتفاع نصب، عرض پروفیل، نوع پخش نور و مشخصات هر مدل را مقایسه کنید.",
        meta_description_en="Compare Verona MD LINEO pendant lights by profile size, suspension height, light distribution and recorded model specifications.",
    ),
    "surface-mount": CategoryContent(
        description_fa=(
            "چراغ خطی روکار زمانی انتخاب می‌شود که امکان یا نیاز به ایجاد برش توکار وجود ندارد و پروفیل به "
            "صورت مستقیم روی سقف یا سطح معماری نصب می‌شود. در این دسته، خانواده MD LINEO با مدل‌های MINI، "
            "NARROW، NARROW DOT و MID قابل بررسی است. مسیر نصب، محل عبور کابل، نحوه اتصال قطعات، عرض پروفیل "
            "و پیوستگی خط نور باید در جزئیات اجرایی پیش‌بینی شود. برای انتخاب میان مدل‌ها، ابعاد و اطلاعات "
            "توان و نور ثبت‌شده را با طول مسیر و سطح روشنایی موردنیاز پروژه مقایسه کنید."
        ),
        description_en=(
            "Surface-mounted linear lighting is selected where a recessed cut-out is unavailable or unnecessary, "
            "with the profile fixed directly to the ceiling or architectural surface. This category presents the "
            "MD LINEO family in MINI, NARROW, NARROW DOT and MID models. The route, cable entry, component joints, "
            "profile width and continuity of the light line should be resolved in the installation detail. Compare "
            "the recorded dimensions, wattage and lighting data of each model with the route length and required "
            "illumination of the project."
        ),
        meta_title_fa="چراغ خطی روکار سقفی | ورونا لایتینگ",
        meta_title_en="Surface-Mounted Linear Lighting | Verona",
        meta_description_fa="مدل‌های چراغ خطی روکار MD LINEO ورونا را براساس عرض پروفیل، مسیر نصب، ابعاد، توان و اطلاعات نوری ثبت‌شده مقایسه کنید.",
        meta_description_en="Explore Verona MD LINEO surface-mounted linear lights and compare profile width, installation route, dimensions and lighting data.",
    ),
    "in-ground-mount": CategoryContent(
        description_fa=(
            "چراغ خطی دفنی برای یکپارچه‌شدن خط نور با کف و جزئیات محوطه یا معماری استفاده می‌شود. مدل "
            "PD-Inground ورونا در این دسته قرار دارد و انتخاب آن باید هم‌زمان با طراحی شیار، زیرسازی، زهکشی "
            "و مسیر کابل انجام شود. ابعاد محل نصب و اطلاعات فنی ثبت‌شده محصول باید پیش از اجرا کنترل شوند، "
            "زیرا دسترسی و اصلاح جزئیات پس از تکمیل کف دشوارتر است. جهت تابش و محل چراغ را نیز طوری مشخص کنید "
            "که نور با مسیر حرکت، سطح مجاور و هدف معماری پروژه هماهنگ باشد."
        ),
        description_en=(
            "In-ground linear lighting integrates a line of light into floors, landscapes or architectural "
            "details. Verona's PD-Inground model is listed in this category and should be coordinated with the "
            "channel, substrate, drainage and cable route during design. Installation dimensions and the product's "
            "recorded technical data must be checked before construction because access and correction become "
            "more difficult after the floor is complete. Aiming and location should also relate to circulation, "
            "adjacent surfaces and the intended architectural effect."
        ),
        meta_title_fa="چراغ خطی دفنی و توکار کف | ورونا",
        meta_title_en="In-Ground Linear Lighting | Verona Lighting",
        meta_description_fa="چراغ خطی دفنی PD-Inground ورونا را برای نورپردازی کف و محوطه با توجه به ابعاد نصب، زیرسازی، زهکشی و مشخصات فنی بررسی کنید.",
        meta_description_en="Review Verona PD-Inground linear lighting for floors and landscapes, including installation dimensions, substrate and drainage planning.",
    ),
    "cove-lighting": CategoryContent(
        description_fa=(
            "نور مخفی برای ایجاد روشنایی غیرمستقیم در شیار سقف، دیوار، زیر کابینت و جزئیات معماری استفاده "
            "می‌شود و یکنواختی آن به انتخاب منبع نور و پروفیل مناسب وابسته است. این دسته شامل ریسه‌های ۲۴ ولت، "
            "ریسه‌های ۲۲۰ ولت، مدل‌های IP ثبت‌شده، نئون و پروفیل Corner است. طول مسیر، محل تغذیه، امکان "
            "دسترسی، دفع حرارت و فاصله منبع نور از سطح بازتابنده باید پیش از اجرا مشخص شود. مشخصات هر محصول "
            "را جداگانه بررسی کنید و ولتاژ، درجه حفاظت و قطعات موردنیاز را براساس همان مدل انتخاب کنید."
        ),
        description_en=(
            "Cove lighting creates indirect illumination within ceiling slots, walls, cabinetry and architectural "
            "details, with uniformity depending on the selected light source and profile. This category includes "
            "24 V and 220 V strip lights, listed IP versions, neon light and the Corner profile. Route length, power "
            "feed location, service access, heat management and distance from the reflecting surface should be "
            "planned before installation. Review each product separately and select voltage, ingress protection "
            "and related components according to that model's recorded information."
        ),
        meta_title_fa="ریسه LED و نور مخفی | ورونا لایتینگ",
        meta_title_en="LED Strip and Cove Lighting | Verona Lighting",
        meta_description_fa="ریسه ۲۴ و ۲۲۰ ولت، نئون و پروفیل نور مخفی ورونا را براساس طول مسیر، ولتاژ، روش نصب و مشخصات ثبت‌شده هر مدل بررسی کنید.",
        meta_description_en="Compare Verona LED strips, neon and cove profiles by route length, voltage, installation detail and recorded product specifications.",
    ),
    "recessed": CategoryContent(
        description_fa=(
            "چراغ خطی توکار داخل شیار سقف یا سطح معماری نصب می‌شود تا بدنه چراغ حضور کمتری داشته باشد و خط "
            "نور با جزئیات فضا یکپارچه شود. در این دسته خانواده‌های SP LINEO و BD LINEO با مدل‌های MINI، "
            "NARROW، DOT، MID، WIDE و PLUS معرفی شده‌اند. عرض و عمق شیار، نوع لبه، محل درایور و مسیر کابل "
            "باید پیش از اجرای سقف هماهنگ شود. برای مقایسه مدل‌ها، ابعاد، توان، شار نوری، نوع پخش نور و "
            "اطلاعات ثبت‌شده در صفحه هر محصول را در کنار طول خط نور موردنیاز بررسی کنید."
        ),
        description_en=(
            "Recessed linear lighting sits within a ceiling or architectural channel so the housing has less "
            "visual presence and the light line becomes part of the detail. This category includes SP LINEO and "
            "BD LINEO families in MINI, NARROW, DOT, MID, WIDE and PLUS models. Channel width and depth, edge "
            "detail, driver location and cable route should be coordinated before the ceiling is built. Compare "
            "dimensions, wattage, luminous flux, light distribution and the recorded data of each model alongside "
            "the required length of the lighting line."
        ),
        meta_title_fa="چراغ خطی توکار و بدون لبه | ورونا",
        meta_title_en="Recessed Linear Lighting | Verona Lighting",
        meta_description_fa="چراغ خطی توکار SP و BD LINEO ورونا را براساس ابعاد شیار، نوع لبه، عرض پروفیل، توان و خروجی نور ثبت‌شده مقایسه کنید.",
        meta_description_en="Compare Verona SP and BD LINEO recessed lights by channel dimensions, edge detail, profile width and recorded lighting output.",
    ),
    "panel": CategoryContent(
        description_fa=(
            "چراغ پنل LED برای ایجاد نور سقفی منظم در فضاهای اداری، تجاری، مسکونی و عمومی استفاده می‌شود. "
            "این دسته خانواده‌های PERANSA، HALOO، TABAN، TRIMLESS، PAYAM و BAHAR را در فرم‌های دایره‌ای، "
            "مربعی، تک‌خانه و چندخانه گردآوری می‌کند. نوع سقف، ابعاد برش یا محل نصب، تعداد چراغ‌ها و آرایش آن‌ها "
            "باید با پلان روشنایی هماهنگ شود. برای انتخاب مدل مناسب، توان، شار نوری، دمای رنگ، شاخص نمود رنگ "
            "و دیگر مشخصات ثبت‌شده در صفحه محصول را مقایسه کنید."
        ),
        description_en=(
            "LED panel lights provide ordered ceiling illumination for offices, commercial interiors, homes and "
            "public spaces. This category brings together the PERANSA, HALOO, TABAN, TRIMLESS, PAYAM and BAHAR "
            "families in round, square, single and multi-cell forms. Ceiling type, cut-out or mounting dimensions, "
            "luminaire quantity and layout should be coordinated with the lighting plan. Compare recorded wattage, "
            "luminous flux, colour temperature, colour rendering and the other available specifications to select "
            "an appropriate model."
        ),
        meta_title_fa="چراغ پنل LED سقفی و توکار | ورونا",
        meta_title_en="LED Panel and Recessed Ceiling Lights | Verona",
        meta_description_fa="چراغ پنل LED ورونا را در مدل‌های دایره‌ای، مربعی، تک‌خانه و چندخانه براساس ابعاد نصب، توان، شار نوری و مشخصات فنی مقایسه کنید.",
        meta_description_en="Compare Verona LED panel lights in round, square, single and multi-cell forms using installation dimensions and recorded output data.",
    ),
    "1hp": CategoryContent(
        description_fa=(
            "سیستم چراغ ریلی تک‌فاز برای پروژه‌هایی مناسب است که کنترل ساده یک مدار روشنایی در طول ریل کافی "
            "است. این دسته شامل ریل روکار و آویز، چراغ اسپات، مدل آویز و قطعاتی مانند کانکتور مستقیم، رابط L، "
            "رابط T و کانکتور تغذیه است. همه چراغ‌ها و اتصالات باید مخصوص سیستم 1PH باشند و پیش از اجرا، مسیر "
            "ریل و محل ورود تغذیه مشخص شود. برای انتخاب اسپات یا آویز، ابعاد، توان، زاویه تابش و سایر اطلاعات "
            "ثبت‌شده صفحه محصول را با ارتفاع نصب و هدف نورپردازی مقایسه کنید."
        ),
        description_en=(
            "A single-phase track system is suitable where one simply controlled lighting circuit along the rail "
            "meets the project requirements. This category includes surface and pendant track, spotlights, pendant "
            "models and components such as straight, L, T and power-feed connectors. Every luminaire and connector "
            "must be intended for the 1PH system, with the rail route and feed position defined before installation. "
            "For spot or pendant selection, compare dimensions, wattage, beam information and other recorded data "
            "with mounting height and the intended lighting task."
        ),
        meta_title_fa="چراغ ریلی تک‌فاز و ریل 1PH | ورونا",
        meta_title_en="Single-Phase 1PH Track Lighting | Verona",
        meta_description_fa="چراغ و ریل تک‌فاز 1PH ورونا را شامل اسپات، آویز، کانکتور مستقیم، L، T و قطعه تغذیه متناسب با یک مدار روشنایی بررسی کنید.",
        meta_description_en="Explore Verona 1PH single-phase track lighting, including spots, pendants, rails and compatible straight, L, T and power connectors.",
    ),
    "3hp": CategoryContent(
        description_fa=(
            "سیستم چراغ ریلی سه‌فاز برای پروژه‌هایی استفاده می‌شود که تقسیم چراغ‌های روی یک ریل به مدارهای "
            "مجزا و کنترل منعطف‌تر اهمیت دارد. این دسته شامل ریل توکار و روکار، چراغ اسپات یا آویز و قطعاتی "
            "مانند کانکتور مستقیم، T، چهارراه و اتصال تغذیه است. جهت و آرایش اتصال‌ها باید با مسیر ریل و مدارها "
            "هماهنگ شود و تمام اجزا از خانواده 3PH انتخاب شوند. مشخصات ثبت‌شده چراغ، توان، زاویه تابش، ارتفاع "
            "نصب و هدف نورپردازی را پیش از تعیین تعداد و فاصله چراغ‌ها بررسی کنید."
        ),
        description_en=(
            "A three-phase track system is used where luminaires on one rail need to be divided into separate "
            "circuits for more flexible control. This category includes recessed and surface tracks, spot or "
            "pendant luminaires and components such as straight, T, four-way and power connectors. Connector "
            "orientation and arrangement must follow the rail route and circuit plan, with all components selected "
            "from the 3PH family. Review recorded luminaire data, wattage, beam information, mounting height and "
            "lighting purpose before setting the quantity and spacing."
        ),
        meta_title_fa="چراغ ریلی سه‌فاز و ریل 3PH | ورونا",
        meta_title_en="Three-Phase 3PH Track Lighting | Verona",
        meta_description_fa="سیستم چراغ ریلی سه‌فاز 3PH ورونا را شامل ریل توکار و روکار، اسپات، آویز و کانکتورهای سازگار برای کنترل چند مدار بررسی کنید.",
        meta_description_en="Explore Verona 3PH three-phase track lighting with recessed and surface rails, luminaires and compatible multi-way connectors.",
    ),
}


def validate_category_content() -> None:
    """Fail before database writes if reviewed content is incomplete."""

    if len(CATEGORY_CONTENT) != 23:
        raise ValueError("The category content map must contain exactly 23 entries.")

    descriptions_fa = set()
    descriptions_en = set()
    for slug, content in CATEGORY_CONTENT.items():
        if len(content.description_fa) < 250 or len(content.description_en) < 250:
            raise ValueError(f"{slug}: category descriptions are too short.")
        if len(content.meta_title_fa) > 65 or len(content.meta_title_en) > 65:
            raise ValueError(f"{slug}: a meta title exceeds 65 characters.")
        if len(content.meta_description_fa) > 160 or len(content.meta_description_en) > 160:
            raise ValueError(f"{slug}: a meta description exceeds 160 characters.")
        if content.description_fa in descriptions_fa or content.description_en in descriptions_en:
            raise ValueError(f"{slug}: a category description is duplicated.")
        descriptions_fa.add(content.description_fa)
        descriptions_en.add(content.description_en)
