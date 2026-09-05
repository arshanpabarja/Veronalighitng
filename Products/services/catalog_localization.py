"""Persian presentation helpers for catalog variant data.

Technical identifiers and units remain unchanged; human-readable catalog terms
are localized at render time so every current and future product variant gets a
Persian-facing model-and-size table without corrupting its source catalog data.
"""

import re


_PHRASES = {
    "Surface & Pendant Wide Rail": "ریل عریض روکار و آویز",
    "Surface & Pendant Mini Rail": "ریل مینی روکار و آویز",
    "Circle Surface & Pendant Rail": "ریل دایره‌ای روکار و آویز",
    "Recessed Trimless Wide Rail": "ریل عریض توکار بدون لبه",
    "Recessed Trimless Mini Rail": "ریل مینی توکار بدون لبه",
    "Recessed Trim Mini Rail": "ریل مینی توکار لبه‌دار",
    "Decorative Ceiling Light": "چراغ سقفی دکوراتیو",
    "Super Ring High Power Downlight": "دانلایت پرتوان سوپر رینگ",
    "Supernova High Power Downlight": "دانلایت پرتوان سوپرنوا",
    "High Power Downlight": "دانلایت پرتوان",
    "Decorative Downlight": "دانلایت دکوراتیو",
    "Gypsum Downlight": "دانلایت گچی",
    "Recessed Downlight": "دانلایت توکار",
    "Linear Downlight": "دانلایت خطی",
    "COB Surface Light": "چراغ روکار COB",
    "GU10 Surface Light": "چراغ روکار GU10",
    "SMD Surface Light": "چراغ روکار SMD",
    "Light Engine Module": "ماژول موتور نور",
    "Bluetooth Speaker": "بلندگوی بلوتوثی",
    "Ring Line Downlight": "دانلایت رینگ‌لاین",
    "Ring Line Inside": "رینگ‌لاین داخلی",
    "Branded Exit Sign": "تابلو خروج برنددار",
    "Exit Sign": "تابلو خروج",
    "Spot Dot Panel": "پنل اسپات نقطه‌ای",
    "Spot Linear": "اسپات خطی",
    "Spot Panel": "پنل اسپات",
    "Flexible Linear": "خطی انعطاف‌پذیر",
    "Strip Light": "نوار نوری",
    "LED Lamp": "لامپ LED",
    "Ceiling Light": "چراغ سقفی",
    "Downlight": "دانلایت",
}

_WORDS = {
    "Magnetar": "مگنتار",
    "Magneto": "مگنتو",
    "Magnet": "مگنت",
    "Verona": "ورونا",
    "Arian": "آریان",
    "Bahar": "بهار",
    "Bambo": "بامبو",
    "Bardia": "بردیا",
    "Caror": "کارور",
    "Castor": "کاستور",
    "Cylindra": "سیلندرا",
    "Blink": "بلینک",
    "Folcano": "فولکانو",
    "Fornax": "فورناکس",
    "Pictor": "پیکتور",
    "Pollux": "پولوکس",
    "Pyxis": "پیکسیس",
    "Vega": "وگا",
    "Vela": "ولا",
    "Virgo": "ویرگو",
    "Wave": "ویو",
    "Helia": "هلیا",
    "Karen": "کارن",
    "LIBER": "لیبر",
    "Liber": "لیبر",
    "Mirdamad": "میرداماد",
    "MIRDAMAD": "میرداماد",
    "Moon": "مون",
    "Payam": "پیام",
    "Peransa": "پرانسا",
    "ROSHANA": "روشانا",
    "Sepehr": "سپهر",
    "Shayan": "شایان",
    "Taban": "تابان",
    "TRITON": "تریتون",
    "Vanta": "ونتا",
    "Plano": "پلانو",
    "Point": "پوینت",
    "Spy": "اسپای",
    "Lyra": "لایرا",
    "Double": "دوتایی",
    "Single": "تکی",
    "Triple": "سه‌تایی",
    "Pendant": "آویز",
    "Surface": "روکار",
    "Recessed": "توکار",
    "Trimless": "بدون لبه",
    "Trim": "لبه‌دار",
    "Large": "بزرگ",
    "SMALL": "کوچک",
    "Small": "کوچک",
    "Mini": "مینی",
    "Narrow": "باریک",
    "Wide": "عریض",
    "Mid": "متوسط",
    "medium": "متوسط",
    "Angle": "زاویه‌دار",
    "Diamond": "الماسی",
    "Highbay": "چراغ صنعتی سقفی",
    "Dot": "نقطه‌ای",
    "dot": "نقطه‌ای",
    "Linear": "خطی",
    "LINEAR": "خطی",
    "Curve": "منحنی",
    "Circle": "دایره‌ای",
    "Flex": "انعطاف‌پذیر",
    "FLEXIBLE": "انعطاف‌پذیر",
    "Rotate": "چرخشی",
    "Spotlight": "پروژکتوری",
    "Spot": "اسپات",
    "Panel": "پنل",
    "Tube": "لوله‌ای",
    "Track": "ریل",
    "Belt": "کمربندی",
    "Wall": "دیواری",
    "Square": "مربعی",
    "Inside": "داخلی",
    "OLD": "قدیمی",
}


def _translate_name(value):
    translated = value
    for source, target in sorted(_PHRASES.items(), key=lambda item: -len(item[0])):
        translated = translated.replace(source, target)
    for source, target in sorted(_WORDS.items(), key=lambda item: -len(item[0])):
        translated = re.sub(rf"(?<![A-Za-z]){re.escape(source)}(?![A-Za-z])", target, translated)
    translated = (
        translated.replace("�", "×")
        .replace(" cm", " سانتی‌متر")
        .replace(" mm", " میلی‌متر")
        .replace(" W", " وات")
    )
    return re.sub(r"\s{2,}", " ", translated).strip()


def _translate_note(value):
    translated = value.replace("�", "×")
    if ";" in translated:
        first, remainder = translated.split(";", 1)
        translated = f"{_translate_name(first)}؛{remainder}"

    replacements = {
        "The catalog also lists customized lengths from 120 to 160 cm.":
            "در کاتالوگ، طول‌های سفارشی از 120 تا 160 cm نیز ارائه شده‌اند.",
        "Color temperature and body color are customized to customer requirements.":
            "دمای رنگ و رنگ بدنه مطابق نیاز مشتری سفارشی‌سازی می‌شوند.",
        "Available customized lengths:": "طول‌های سفارشی قابل ارائه:",
        "Length is customizable.": "طول قابل سفارشی‌سازی است.",
        "length is customizable.": "طول قابل سفارشی‌سازی است.",
        "E27 replaceable lamp.": "لامپ E27 قابل تعویض است.",
        "lamp replaceable without tools": "تعویض لامپ بدون ابزار",
        "max 35 W each": "حداکثر توان هر لامپ 35 W",
        "plaster housing": "بدنه گچی",
        "Cut-out": "ابعاد برش",
        "cut-out": "ابعاد برش",
        "available lengths": "طول‌های قابل ارائه",
        "body color": "رنگ بدنه",
        "white": "سفید",
        "each": "برای هر لامپ",
        " or GU10": " یا GU10",
        " and ": " و ",
    }
    for source, target in replacements.items():
        translated = translated.replace(source, target)

    translated = (
        translated.replace(";", "؛")
        .replace(", ", "، ")
        .replace(" cm", " سانتی‌متر")
        .replace(" mm", " میلی‌متر")
        .replace(" W", " وات")
    )
    return re.sub(r"\s{2,}", " ", translated).strip()


def catalog_text_fa(value):
    if not value:
        return value
    value = str(value)
    note_markers = (
        "custom", "Cut-out", "cut-out", "lamp", "housing", "catalog",
        "requirements", "available lengths", "Available customized",
    )
    if any(marker in value for marker in note_markers):
        return _translate_note(value)
    return _translate_name(value)
