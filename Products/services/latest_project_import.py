"""Reviewed bilingual records for the three newest published project pages."""

from pathlib import Path


LATEST_PROJECTS = {
    "hormozan-tower-residence": {
        "application_slug": "house",
        "order": 1,
        "completion_year": "2026",
        "hero_image": "projects/heroes/kitchen_hero_under_100kb.jpg",
        "gallery_images": (
            "projects/gallery/interior_5_under_100kb.jpg",
            "projects/gallery/interior_4_under_100kb.jpg",
        ),
        "name_fa": "برج هرمزان",
        "name_en": "Hormozan Tower Residence",
        "location_fa": "تهران - شهرک غرب",
        "location_en": "Tehran - Shahrak Gharb",
        "project_type_fa": "مسکونی",
        "project_type_en": "Residential",
        "intro_heading_fa": "طراحی نورپردازی واحد مسکونی برج هرمزان",
        "intro_heading_en": "HORMOZAN TOWER - RESIDENCE",
        "intro_text_fa": (
            "پروژه نورپردازی مسکونی برج هرمزان در شهرک غرب تهران با تمرکز بر "
            "ایجاد فضایی آرام، مدرن و دلنشین شکل گرفته است. نورپردازی در این پروژه "
            "به‌گونه‌ای طراحی شده که ضمن تأمین روشنایی مناسب، با معماری داخلی "
            "هماهنگ باشد و حس گرما و آسایش را در فضای زندگی تقویت کند."
        ),
        "intro_text_en": (
            "The lighting project for the Hormozan Tower Residence in Shahrak-e "
            "Gharb, Tehran, was developed with a focus on creating a calm, modern, "
            "and inviting living environment. The lighting complements the interior "
            "architecture while providing comfortable illumination and enhancing "
            "the warmth and character of the space."
        ),
        "overview_text_fa": (
            "در نورپردازی پروژه مسکونی برج هرمزان، توجه ویژه‌ای به تعادل میان "
            "روشنایی کاربردی و نورپردازی دکوراتیو شده است. ترکیب منابع نوری مختلف "
            "به تعریف بهتر فضاها، ایجاد عمق بصری و برجسته‌کردن عناصر معماری و "
            "دکوراسیون داخلی کمک می‌کند. هدف اصلی، ایجاد محیطی بوده که نور در آن "
            "به‌صورت طبیعی با فضای داخلی ترکیب شود و در کنار تأمین نیازهای روزمره، "
            "کیفیت بصری و حس آرامش محیط مسکونی را افزایش دهد."
        ),
        "overview_text_en": (
            "The lighting concept for the Hormozan Tower Residence focuses on "
            "balancing functional illumination with decorative and ambient lighting. "
            "The combination of different light sources helps define individual spaces, "
            "create visual depth, and highlight key architectural and interior elements. "
            "The main objective was to integrate lighting naturally into the interior, "
            "providing the illumination required for everyday living while enhancing "
            "the visual quality, comfort, and atmosphere of the residence."
        ),
        "about_content_fa": (
            "<p>پروژه مسکونی برج هرمزان در شهرک غرب تهران نمونه‌ای از نقش نورپردازی "
            "در تکمیل معماری داخلی یک فضای مسکونی مدرن است. در این پروژه، نور تنها "
            "به‌عنوان منبع روشنایی در نظر گرفته نشده، بلکه به‌عنوان عنصری مؤثر در "
            "شکل‌گیری حس و هویت فضا مورد توجه قرار گرفته است. استفاده هماهنگ از "
            "نورهای مستقیم، غیرمستقیم و تأکیدی باعث شده بخش‌های مختلف خانه هویت "
            "بصری مشخصی داشته باشند و در عین حال ارتباط و یکپارچگی میان فضاها حفظ "
            "شود. نتیجه، محیطی متعادل و آرام است که نورپردازی در آن به کیفیت معماری "
            "و تجربه زندگی روزمره کمک می‌کند.</p>"
        ),
        "about_content_en": (
            "<p>The Hormozan Tower Residence in Shahrak-e Gharb, Tehran, demonstrates "
            "how thoughtful lighting can complement the interior architecture of a "
            "modern residential space. In this project, light is considered not simply "
            "as a source of illumination, but as an integral design element that "
            "contributes to the atmosphere and identity of the interior. A balanced use "
            "of direct, indirect, and accent lighting gives different areas of the "
            "residence their own visual character while maintaining a sense of continuity "
            "throughout the space. The result is a refined and comfortable environment "
            "where lighting enhances both the architecture and the everyday living "
            "experience.</p>"
        ),
        "meta_title_fa": "برج هرمزان",
        "meta_title_en": "Hormozan Tower Residence",
        "meta_description_fa": (
            "پروژه نورپردازی مسکونی برج هرمزان در شهرک غرب تهران با تمرکز بر ایجاد "
            "فضایی آرام، مدرن و دلنشین شکل گرفته است. نورپردازی در این پروژه به‌گونه‌ای "
            "طراحی شده که ض…"
        ),
        "meta_description_en": (
            "The lighting project for the Hormozan Tower Residence in Shahrak-e Gharb, "
            "Tehran, was developed with a focus on creating a calm, modern, and inviting "
            "living en…"
        ),
    },
    "diamond-boutique": {
        "application_slug": "retail",
        "order": 2,
        "completion_year": "2026",
        "hero_image": "projects/heroes/IMG_20260531_003124_983_2ItUVEm.jpg",
        "gallery_images": (
            "projects/gallery/IMG_20260531_003124_983_7kALDF1.jpg",
            "projects/gallery/IMG_20260531_003122_812_3YuUVDk.jpg",
        ),
        "name_fa": "بوتیک دایموند",
        "name_en": "Diamond Boutique",
        "location_fa": "مرکز خرید اپال، تهران",
        "location_en": "Opal, Tehran",
        "project_type_fa": "فضای تجاری",
        "project_type_en": "Retail",
        "intro_heading_fa": "طراحی نورپردازی بوتیک دایموند",
        "intro_heading_en": "Diamond Boutique – Retail Lighting Concept",
        "intro_text_fa": (
            "بوتیک دایموند در مرکز خرید اپال تهران، یک پروژه نورپردازی فروشگاهی است "
            "که در آن نمایش دقیق محصول و ساختن اتمسفر برند در اولویت قرار دارد. "
            "راهکار روشنایی بر کنترل کنتراست، هدایت نگاه و انعطاف‌پذیری چیدمان تمرکز "
            "می‌کند تا محصولات در مرکز توجه باقی بمانند."
        ),
        "intro_text_en": (
            "Diamond Boutique is a contemporary retail lighting project located in "
            "Tehran, designed to highlight the relationship between product display "
            "and atmospheric illumination. The space uses a refined lighting strategy "
            "based on track lighting systems, allowing precise control over focus, "
            "contrast, and visual hierarchy within the store."
        ),
        "overview_text_fa": (
            "در بوتیک دایموند، نور به‌عنوان بخشی از طراحی داخلی و تجربه خرید در نظر "
            "گرفته شده است. روشنایی عمومی کنترل‌شده، پس‌زمینه‌ای آرام ایجاد می‌کند و "
            "نورهای تأکیدی، ویترین‌ها و محدوده‌های اصلی نمایش محصول را از نظر بصری "
            "تفکیک می‌کنند.\n\nسیستم روشنایی قابل تنظیم به فروشگاه اجازه می‌دهد با "
            "تغییر کالکشن یا چیدمان، جهت و تمرکز نور را اصلاح کند. این انعطاف باعث "
            "می‌شود هویت بصری فروشگاه ثابت بماند، در حالی که سناریوی نمایش محصولات "
            "می‌تواند متناسب با نیاز هر دوره تغییر کند."
        ),
        "overview_text_en": (
            "Diamond Boutique is a retail interior project developed in Tehran, where "
            "lighting is treated as a core design element rather than a secondary "
            "technical feature. The concept focuses on creating a clean, flexible retail "
            "environment that enhances product visibility and strengthens the overall "
            "shopping experience.\n\nThe spatial organization is supported by a track "
            "lighting system that enables adjustable spotlighting across display zones. "
            "This approach allows the store to adapt to changing collections while "
            "maintaining a consistent visual identity. The lighting design emphasizes "
            "clarity, depth, and selective focus, guiding attention toward key retail "
            "elements without visual clutter."
        ),
        "about_content_fa": (
            "<p>فلسفه طراحی بوتیک دایموند بر دقت و انعطاف استوار است. جزئیات داخلی "
            "عمداً ساده نگه داشته شده‌اند تا کالاها نقطه اصلی توجه باشند و نور، ریتم "
            "و سلسله‌مراتب فضا را تعریف کند.</p><p>چراغ‌های ریلی و نورهای موضعی امکان "
            "تنظیم زاویه تابش و تمرکز بر قفسه‌ها، ویترین و نقاط شاخص را فراهم می‌کنند. "
            "کنترل خیرگی و فاصله مناسب چراغ‌ها کمک می‌کند رنگ، فرم و درخشش محصولات "
            "با وضوح بیشتری دیده شود.</p><p>نتیجه، فضایی تجاری با نورپردازی منظم و "
            "قابل بازتنظیم است که ارائه محصول، مسیر حرکت مشتری و شخصیت برند را در یک "
            "ساختار هماهنگ جمع می‌کند.</p>"
        ),
        "about_content_en": (
            "The design philosophy behind Diamond Boutique is based on precision and "
            "adaptability. The interior is kept minimal to ensure that the merchandise "
            "remains the focal point, while lighting defines mood and spatial rhythm.\n\n"
            "Linear track lighting is used throughout the space to provide modular "
            "illumination, enabling targeted highlighting of products and flexible "
            "reconfiguration of display areas. This system supports both functional "
            "retail needs and a refined aesthetic language, resulting in a controlled "
            "yet visually engaging environment.\n\nOverall, Diamond Boutique reflects "
            "a modern retail approach where architecture and lighting work together to "
            "shape perception, improve product presentation, and create a distinct brand "
            "atmosphere."
        ),
        "meta_title_fa": "طراحی نورپردازی بوتیک دایموند تهران | ورونا",
        "meta_title_en": "Diamond Boutique Lighting, Tehran | Verona",
        "meta_description_fa": (
            "پروژه نورپردازی بوتیک دایموند در مرکز خرید اپال تهران؛ طراحی روشنایی "
            "فروشگاهی با نور تأکیدی، کنترل کنتراست و چیدمان انعطاف‌پذیر."
        ),
        "meta_description_en": (
            "See the retail lighting concept for Diamond Boutique in Tehran, using "
            "adjustable accent lighting to support product display and visual focus."
        ),
    },
    "tl-frosh": {
        "application_slug": "retail",
        "order": 3,
        "completion_year": "2026",
        "hero_image": "projects/heroes/jewelry_hero_under_100kb.jpg",
        "gallery_images": (
            "projects/gallery/interior_3_under_100kb.jpg",
            "projects/gallery/interior_2_under_100kb.jpg",
        ),
        "name_fa": "طلا فروشی",
        "name_en": "Gold shop",
        "location_fa": "اهواز",
        "location_en": "Ahvaz",
        "project_type_fa": "تجاری",
        "project_type_en": "Retail",
        "intro_heading_fa": "THE BRIEF",
        "intro_heading_en": "THE BRIEF",
        "intro_text_fa": (
            "پروژه نورپردازی طلا فروشی اهواز با هدف ایجاد فضایی لوکس، چشم‌نواز و "
            "هماهنگ با درخشش طلا و جواهرات طراحی شده است. در این پروژه، نور به‌عنوان "
            "یکی از عناصر اصلی طراحی فضا در نظر گرفته شده تا علاوه بر ایجاد جلوه‌ای "
            "جذاب، جزئیات و زیبایی محصولات را به بهترین شکل به نمایش بگذارد."
        ),
        "intro_text_en": (
            "The Ahvaz Jewelry Store lighting project was designed to create a luxurious, "
            "visually striking atmosphere that complements the brilliance of gold and "
            "jewelry. Lighting was treated as a key element of the space, enhancing the "
            "overall ambiance while highlighting the beauty and fine details of each piece."
        ),
        "overview_text_fa": (
            "در نورپردازی طلا فروشی اهواز، تمرکز اصلی بر ایجاد تعادل میان نورپردازی "
            "عمومی فضا و نورهای تأکیدی بوده است. نورپردازی به‌گونه‌ای طراحی شده که "
            "ویترین‌ها و محصولات به نقاط اصلی توجه تبدیل شوند و در عین حال، فضای "
            "فروشگاه حس لوکس و یکپارچه‌ای داشته باشد. انتخاب جهت و نحوه توزیع نور با "
            "هدف افزایش درخشش و وضوح طلا و جواهرات انجام شده است. نتیجه، فضایی روشن "
            "و جذاب است که نور در آن نه‌تنها یک نیاز عملکردی، بلکه بخشی از هویت بصری "
            "و تجربه حضور در فروشگاه محسوب می‌شود."
        ),
        "overview_text_en": (
            "The lighting concept for the Ahvaz Jewelry Store focuses on achieving a "
            "balanced combination of ambient and accent lighting. The lighting is designed "
            "to draw attention to the showcases and jewelry while maintaining a refined "
            "and cohesive atmosphere throughout the store. The direction and distribution "
            "of light were carefully considered to enhance the brilliance, clarity, and "
            "visual presence of the displayed pieces. The result is a bright and elegant "
            "environment where lighting serves not only a functional purpose but also as "
            "an essential part of the store’s visual identity and customer experience."
        ),
        "about_content_fa": (
            "<p>طلا فروشی اهواز پروژه‌ای با تمرکز ویژه بر نقش نور در نمایش طلا و "
            "جواهرات است. در فضایی که کیفیت نمایش محصولات اهمیت بالایی دارد، "
            "نورپردازی می‌تواند تأثیر مستقیمی بر نحوه دیده‌شدن رنگ، بافت و درخشش هر "
            "قطعه داشته باشد. رویکرد این پروژه بر ایجاد یک تجربه بصری لوکس و حرفه‌ای "
            "استوار بوده است؛ جایی که نورپردازی معماری فضا را تکمیل می‌کند و در عین "
            "حال توجه مخاطب را به مهم‌ترین عنصر فروشگاه، یعنی طلا و جواهرات، هدایت "
            "می‌کند. ترکیب نور عمومی و تأکیدی باعث ایجاد عمق بصری و تفکیک مناسب "
            "بخش‌های مختلف فروشگاه شده و محیطی دعوت‌کننده و متمایز شکل داده است.</p>"
        ),
        "about_content_en": (
            "<p>The Ahvaz Jewelry Store project places a strong emphasis on the role of "
            "lighting in the presentation of gold and jewelry. In an environment where "
            "product presentation is essential, lighting can directly influence the way "
            "the color, texture, and brilliance of each piece are perceived. The project’s "
            "approach was centered around creating a luxurious and professional visual "
            "experience. The lighting complements the architecture while naturally "
            "directing attention toward the most important elements of the store—the "
            "jewelry itself. By combining ambient and accent lighting, the design creates "
            "visual depth, defines different areas of the space, and establishes an "
            "inviting and distinctive retail environment.</p>"
        ),
        "meta_title_fa": "طلا فروشی",
        "meta_title_en": "Gold shop",
        "meta_description_fa": (
            "پروژه نورپردازی طلا فروشی اهواز با هدف ایجاد فضایی لوکس، چشم‌نواز و "
            "هماهنگ با درخشش طلا و جواهرات طراحی شده است. در این پروژه، نور به‌عنوان "
            "یکی از عناصر اصلی ط…"
        ),
        "meta_description_en": (
            "The Ahvaz Jewelry Store lighting project was designed to create a luxurious, "
            "visually striking atmosphere that complements the brilliance of gold and "
            "jewelry. …"
        ),
    },
}


TRANSLATED_FIELDS = (
    "name",
    "location",
    "project_type",
    "intro_heading",
    "intro_text",
    "overview_text",
    "about_content",
    "meta_title",
    "meta_description",
)


def validate_latest_projects(media_root=None):
    expected_slugs = {
        "hormozan-tower-residence",
        "diamond-boutique",
        "tl-frosh",
    }
    if set(LATEST_PROJECTS) != expected_slugs:
        raise ValueError("The latest-project import must contain exactly three projects.")

    orders = []
    for slug, record in LATEST_PROJECTS.items():
        orders.append(record["order"])
        for field in TRANSLATED_FIELDS:
            for language in ("fa", "en"):
                if not record.get(f"{field}_{language}"):
                    raise ValueError(f"{slug} is missing {field}_{language}.")

        for language in ("fa", "en"):
            if len(record[f"meta_title_{language}"]) > 70:
                raise ValueError(f"{slug} {language} meta title exceeds 70 characters.")
            if len(record[f"meta_description_{language}"]) > 160:
                raise ValueError(
                    f"{slug} {language} meta description exceeds 160 characters."
                )

        if media_root is not None:
            media_root = Path(media_root)
            for image_name in (record["hero_image"], *record["gallery_images"]):
                if not (media_root / image_name).is_file():
                    raise ValueError(f"Missing project image: {image_name}")

    if len(orders) != len(set(orders)):
        raise ValueError("Latest-project display orders must be unique.")

