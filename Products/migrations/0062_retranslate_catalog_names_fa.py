import re

from django.db import migrations


TERM_TRANSLATIONS = {
    "and": "و", "angle": "انگل", "arin": "آرین", "bahar": "بهار",
    "bambo": "بامبو", "bd": "بی‌دی", "belt": "بلت", "blink": "بلینک",
    "c": "سی", "caror": "کارور", "castor": "کستور", "ceiling": "سیلینگ",
    "cob": "سی‌او‌بی", "connection": "کانکشن", "connector": "کانکتور",
    "corner": "کرنر", "cove": "کاو", "cube": "کیوب", "curve": "کرو", "cylindra": "سیلیندرا",
    "decorative": "دکوراتیو", "diamond": "دایموند", "direct": "دایرکت",
    "dot": "دات", "double": "دوبل", "downlight": "دان‌لایت", "dual": "دوبل",
    "emergency": "امرجنسی", "flexi": "فلکسی", "flexible": "فلکسیبل", "fadak": "فدک", "fl": "اف‌ال",
    "folcano": "فولکانو", "fornax": "فورنکس", "four": "فور", "gu": "GU",
    "gypsum": "جیپسوم", "hami": "حامی", "haloo": "هالو", "hat": "هت", "hely": "هلی",
    "highbay": "های‌بی", "inground": "این‌گراند", "inside": "اینساید", "internal": "اینترنال", "ip": "IP",
    "karen": "کارن", "l": "ال", "large": "لارج", "led": "ال‌ای‌دی", "lei": "لی",
    "lia": "لیا", "liber": "لیبر", "light": "لایت", "lighting": "لایتینگ",
    "line": "لاین", "linear": "لاینر", "lineo": "لاینئو", "lina": "لینا", "magnet": "مگنت",
    "magnetar": "مگنتار", "magnetic": "مگنتیک", "magneto": "مگنتو",
    "magnto": "مگنتو", "md": "ام‌دی", "mid": "مید", "mini": "مینی",
    "moon": "مون", "narrow": "نرو", "neon": "نئون", "ney": "نی", "old": "اولد", "offiance": "آفیانس", "onefold": "وان‌فولد", "p": "پی",
    "panel": "پنل", "payam": "پیام", "pd": "پی‌دی", "pendant": "پندنت",
    "peransa": "پرنسا", "pictor": "پیکتور", "plaxi": "پلکسی", "plus": "پلاس",
    "pollux": "پولکس", "power": "پاور", "profile": "پروفایل", "pyxis": "پیکسیس", "qasedak": "قاصدک",
    "rail": "ریل", "reck": "رک", "recessed": "ریسسد", "ressed": "ریسسد",
    "ring": "رینگ", "roshana": "روشنا", "rotate": "روتیت", "samll": "اسمال",
    "short": "شورت", "sign": "ساین", "signage": "ساینیج", "single": "سینگل", "slim": "اسلیم",
    "small": "اسمال", "smallrotate": "اسمال روتیت", "smll": "اسمال",
    "sp": "اس‌پی", "spot": "اسپات", "spotlight": "اسپات‌لایت", "spy": "اسپای", "stand": "استند",
    "square": "اسکوئر", "strip": "استریپ", "surface": "سرفیس", "taban": "تابان", "t": "تی",
    "tee": "تی", "track": "ترک", "trim": "تریم", "trimmed": "تریمد", "trimles": "تریم لس",
    "trimless": "تریم لس", "triple": "تریپل", "triton": "تریتون", "tube": "تیوب", "tl": "تی‌ال",
    "umiqu": "اومیکو", "umiqe": "اومیکو", "vega": "وگا", "vela": "ولا",
    "virgo": "ویرگو", "wall": "وال", "wave": "ویو", "way": "وی", "wid": "واید",
    "wide": "واید", "win": "وین", "up": "آپ",
}

TOKEN_RE = re.compile(r"\d+[A-Za-z]+|[A-Za-z]+\d+|[A-Za-z]+|\d+|[&()\-]")
TECHNICAL_CODE_RE = re.compile(r"^(?:\d+(?:PH|V|CM)|IP\d+|GU\d+)$", re.I)


def translate_name(name):
    translated = []
    for token in TOKEN_RE.findall(name or ""):
        if token == "&":
            translated.append("و")
        elif token in {"(", ")", "-"}:
            translated.append(token)
        elif token.isdigit() or TECHNICAL_CODE_RE.fullmatch(token):
            translated.append(token.upper())
        else:
            translated.append(TERM_TRANSLATIONS[token.casefold()])
    result = re.sub(r"\s+", " ", " ".join(translated)).strip()
    return result.replace("( ", "(").replace(" )", ")").replace(" - ", "-")


def retranslate_names(apps, schema_editor):
    for model_name in ("Family", "Product"):
        model = apps.get_model("Products", model_name)
        for item in model.objects.all().iterator():
            item.name_fa = translate_name(item.name_en)
            item.save(update_fields=["name_fa"])


class Migration(migrations.Migration):
    dependencies = [("Products", "0061_split_magneto_curve_product_families")]
    operations = [migrations.RunPython(retranslate_names, migrations.RunPython.noop)]
