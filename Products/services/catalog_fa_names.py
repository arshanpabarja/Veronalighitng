import re


class UnknownCatalogTerm(ValueError):
    """Raised when a catalog name contains an unreviewed English term."""


# Catalog names use reviewed Persian technical terms without adding
# descriptive copy beyond the source name.
TERM_TRANSLATIONS = {
    "and": "و",
    "angle": "انگل",
    "arin": "آرین",
    "bahar": "بهار",
    "bambo": "بامبو",
    "bd": "بی‌دی",
    "belt": "بلت",
    "blink": "بلینک",
    "c": "سی",
    "caror": "کارور",
    "castor": "کستور",
    "ceiling": "سقفی",
    "cob": "سی‌او‌بی",
    "connection": "کانکشن",
    "connector": "کانکتور",
    "corner": "کرنر",
    "cove": "کاو",
    "cube": "کیوب",
    "curve": "کرو",
    "cylindra": "سیلیندرا",
    "decorative": "دکوراتیو",
    "diamond": "دایموند",
    "direct": "دایرکت",
    "dot": "دات",
    "double": "دوبل",
    "downlight": "دان‌لایت",
    "dual": "دوبل",
    "emergency": "امرجنسی",
    "flexi": "فلکسی",
    "flexible": "فلکسیبل",
    "fadak": "فدک",
    "fl": "اف‌ال",
    "folcano": "فولکانو",
    "fornax": "فورنکس",
    "four": "فور",
    "gu": "GU",
    "gypsum": "گچی",
    "hami": "حامی",
    "haloo": "هالو",
    "hat": "هت",
    "hely": "هلی",
    "highbay": "های‌بی",
    "inground": "این‌گراند",
    "inside": "اینساید",
    "internal": "اینترنال",
    "ip": "IP",
    "karen": "کارن",
    "l": "ال",
    "large": "لارج",
    "led": "ال‌ای‌دی",
    "lei": "لی",
    "lia": "لیا",
    "liber": "لیبر",
    "light": "چراغ",
    "lighting": "چراغ",
    "line": "لاین",
    "linear": "خطی",
    "lineo": "لاینئو",
    "lina": "لینا",
    "magnet": "مگنت",
    "magnetar": "مگنتار",
    "magnetic": "مگنتیک",
    "magneto": "مگنتو",
    "magnto": "مگنتو",
    "md": "ام‌دی",
    "mid": "مید",

    "mini": "مینی",
    "moon": "مون",
    "narrow": "نرو",
    "neon": "نئون",
    "ney": "نی",
    "old": "اولد",
    "offiance": "آفیانس",
    "onefold": "وان‌فولد",
    "p": "پی",
    "panel": "پنل",
    "payam": "پیام",
    "pd": "پی‌دی",
    "pendant": "آویز",
    "peransa": "پرنسا",
    "pictor": "پیکتور",
    "plaxi": "پلکسی",
    "plus": "پلاس",
    "pollux": "پولکس",
    "power": "پاور",
    "profile": "پروفایل",
    "pyxis": "پیکسیس",
    "qasedak": "قاصدک",
    "rail": "ریل",
    "reck": "رک",
    "recessed": "توکار",
    "ressed": "توکار",
    "ressessd": "توکار",
    "ring": "رینگ",
    "roshana": "روشنا",
    "rotate": "روتیت",
    "samll": "اسمال",
    "short": "شورت",
    "sign": "ساین",
    "single": "سینگل",
    "signage": "ساینیج",
    "slim": "اسلیم",
    "small": "اسمال",
    "smallrotate": "اسمال روتیت",
    "smll": "اسمال",
    "sp": "اس‌پی",
    "spot": "اسپات",
    "spotlight": "اسپات‌لایت",
    "spy": "اسپای",
    "stand": "استند",
    "square": "اسکوئر",
    "strip": "استریپ",
    "surface": "روکار",
    "taban": "تابان",
    "t": "تی",
    "tee": "تی",
    "track": "ریل",
    "trim": "لبه‌دار",
    "trimmed": "لبه‌دار",
    "trimles": "بدون لبه",
    "trimless": "بدون لبه",
    "triple": "تریپل",
    "triton": "تریتون",
    "tube": "تیوب",
    "tl": "تی‌ال",
    "umiqu": "اومیکو",
    "umiqe": "اومیکو",
    "vega": "وگا",
    "vela": "ولا",
    "virgo": "ویرگو",
    "wall": "وال",
    "wave": "ویو",
    "way": "وی",
    "wid": "واید",
    "wide": "واید",
    "win": "وین",
    "up": "آپ",
}


TOKEN_RE = re.compile(r"\d+[A-Za-z]+|[A-Za-z]+\d+|[A-Za-z]+|\d+|[&()\-]")
TECHNICAL_CODE_RE = re.compile(r"^(?:\d+(?:PH|V|CM)|IP\d+|GU\d+)$", re.IGNORECASE)


TYPE_TERM_ORDER = (
    "linear",
    "panel",
    "downlight",
    "spotlight",
    "spot",
    "tube",
    "strip",
    "neon",
    "highbay",
    "inground",
    "ring",
    "emergency",
    "signage",
)
INSTALLATION_TERM_ORDER = (
    "recessed",
    "ressed",
    "ressessd",
    "ceiling",
    "surface",
    "pendant",
    "wall",
    "stand",
    "inside",
    "internal",
)
FINISH_TERM_ORDER = ("trimless", "trimles", "trimmed", "trim")
ATTRIBUTE_TERMS = {
    "angle",
    "cob",
    "decorative",
    "diamond",
    "direct",
    "dot",
    "flexible",
    "four",
    "led",
    "magnetic",
    "power",
    "rotate",
    "short",
    "square",
    "tee",
    "way",
}
SKIPPED_TERMS = {"and", "light", "lighting"}


def _source_words(name: str) -> list[str]:
    words = re.findall(r"\d+[A-Za-z]+|[A-Za-z]+\d+|[A-Za-z]+|\d+", name)
    expanded = []
    for word in words:
        normalized = word.casefold()
        if normalized == "smallrotate":
            expanded.extend(("small", "rotate"))
        else:
            expanded.append(normalized)
    return expanded


def _translate_word(word: str, source_name: str) -> str:
    if word.isdigit() or TECHNICAL_CODE_RE.fullmatch(word):
        return word.upper()
    replacement = TERM_TRANSLATIONS.get(word)
    if replacement is None:
        raise UnknownCatalogTerm(
            f"Unreviewed catalog term {word!r} in {source_name!r}"
        )
    return replacement


def translate_catalog_name(
    name: str,
    *,
    category_name: str = "",
    parent_category_name: str = "",
    is_gypsum: bool = False,
) -> str:
    """Translate and arrange one catalog name in natural Persian order."""
    if not name or not name.strip():
        return ""

    words = _source_words(name)
    word_set = set(words)
    category = (category_name or "").casefold()
    parent_category = (parent_category_name or "").casefold()

    component_head = ""
    consumed_components = set()
    if "connector" in word_set:
        component_head = TERM_TRANSLATIONS["connector"]
        consumed_components.add("connector")
    elif "connection" in word_set:
        component_head = TERM_TRANSLATIONS["connection"]
        consumed_components.add("connection")
    elif "profile" in word_set:
        component_head = TERM_TRANSLATIONS["profile"]
        consumed_components.add("profile")
    elif word_set.intersection({"track", "rail"}):
        component_head = TERM_TRANSLATIONS["rail"]
        consumed_components.update({"track", "rail"})
    elif "corner" in word_set:
        component_head = TERM_TRANSLATIONS["corner"]
        consumed_components.add("corner")

    inferred_types = []
    inferred_installations = []
    if not component_head:
        if "recessed linear" in category:
            inferred_types.append("linear")
            inferred_installations.append("recessed")
        elif parent_category == "linear" and category == "surface mount":
            inferred_types.append("linear")
            inferred_installations.append("surface")
        elif parent_category == "linear" and category == "pendant mount":
            inferred_types.append("linear")
            inferred_installations.append("pendant")
        elif category == "downlights" and not is_gypsum:
            inferred_types.append("downlight")
        elif category == "panel":
            inferred_types.append("panel")

    type_words = []
    for term in TYPE_TERM_ORDER:
        if (term in word_set or term in inferred_types) and not (
            is_gypsum and term == "downlight"
        ):
            if term == "emergency" and "sign" in word_set:
                type_words.append("اضطراری")
            else:
                type_words.append(_translate_word(term, name))

    installation_words = []
    normalized_installations = set(inferred_installations)
    normalized_installations.update(
        term for term in INSTALLATION_TERM_ORDER if term in word_set
    )
    if normalized_installations.intersection({"recessed", "ressed", "ressessd"}):
        installation_words.append(TERM_TRANSLATIONS["recessed"])
    for term in ("ceiling", "surface", "pendant", "wall", "stand", "inside", "internal"):
        if term in normalized_installations:
            installation_words.append(_translate_word(term, name))
    if "surface" in normalized_installations and "pendant" in normalized_installations:
        surface = TERM_TRANSLATIONS["surface"]
        pendant = TERM_TRANSLATIONS["pendant"]
        installation_words = [
            word for word in installation_words if word not in {surface, pendant}
        ] + [f"{surface} و {pendant}"]

    finish_words = []
    if word_set.intersection({"trimless", "trimles"}):
        finish_words.append(TERM_TRANSLATIONS["trimless"])
    if word_set.intersection({"trimmed", "trim"}):
        finish_words.append(TERM_TRANSLATIONS["trim"])

    attribute_words = []
    for word in words:
        if word in ATTRIBUTE_TERMS:
            if word == "way" and "four" in word_set:
                continue
            translated = _translate_word(word, name)
            if translated not in attribute_words:
                attribute_words.append(translated)
    if "four" in word_set and "way" in word_set:
        attribute_words = [
            word for word in attribute_words if word != TERM_TRANSLATIONS["four"]
        ]
        attribute_words.append(
            f"{TERM_TRANSLATIONS['four']}-{TERM_TRANSLATIONS['way']}"
        )

    semantic_terms = (
        set(TYPE_TERM_ORDER)
        | set(INSTALLATION_TERM_ORDER)
        | set(FINISH_TERM_ORDER)
        | ATTRIBUTE_TERMS
        | SKIPPED_TERMS
        | consumed_components
        | {"sign"}
    )
    if component_head:
        semantic_terms |= {
            "connector",
            "connection",
            "corner",
            "profile",
            "rail",
            "track",
        }
        if "connector" in consumed_components or "connection" in consumed_components:
            semantic_terms.add("reck")
            if "l" in word_set and "reck" in word_set:
                semantic_terms.add("l")
    model_words = [
        _translate_word(word, name) for word in words if word not in semantic_terms
    ]

    if component_head:
        secondary_components = []
        if "connector" in consumed_components or "connection" in consumed_components:
            if word_set.intersection({"track", "rail"}):
                secondary_components.append(TERM_TRANSLATIONS["rail"])
            if "reck" in word_set:
                if "l" in word_set:
                    secondary_components.append(
                        f"{TERM_TRANSLATIONS['l']}-{TERM_TRANSLATIONS['reck']}"
                    )
                else:
                    secondary_components.append(TERM_TRANSLATIONS["reck"])
        elif "profile" in consumed_components and "corner" in word_set:
            secondary_components.append(TERM_TRANSLATIONS["corner"])
        translated = [
            component_head,
            *attribute_words,
            *secondary_components,
            *installation_words,
            *finish_words,
            *type_words,
            *model_words,
        ]
    else:
        translated = [
            "چراغ",
            *type_words,
            *installation_words,
            *finish_words,
            *attribute_words,
            *model_words,
        ]

    result = " ".join(word for word in translated if word)
    result = re.sub(r"\s+", " ", result).strip()
    if {"spotlight", "pendant"}.issubset(word_set) and word_set.intersection(
        {"and"}
    ):
        result = result.replace("اسپات‌لایت آویز", "اسپات‌لایت و آویز")
    result = result.replace("اف‌ال تی‌ال", "اف‌ال-تی‌ال")
    result = result.replace("آپ تی", "آپ-تی")
    result = result.replace("پی‌دی این‌گراند", "پی‌دی-این‌گراند")
    result = result.replace("ال رک", "ال-رک")
    return result


def remove_downlight_from_gypsum_name(name: str) -> str:
    """Remove the redundant product type from names inside the Gypsum family."""
    result = name or ""
    for spelling in ("دان‌لایت", "دان لایت", "دانلایت"):
        result = result.replace(spelling, " ")
    return re.sub(r"\s+", " ", result).strip()
