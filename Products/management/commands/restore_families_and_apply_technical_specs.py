import re
from decimal import Decimal

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from Products.models import Dimension, Family, Product, ProductVariant


TARGET_PRODUCT_IDS = [
    2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
    20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 36, 37,
    39, 40, 41, 42, 43, 45, 46, 48, 49, 51, 52, 53, 55, 56, 57, 58, 59,
    60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 74, 75, 76, 77,
    78, 81, 82, 206, 231,
]


# This is the product-to-family structure that existed immediately before the
# catalog consolidation. Family IDs are retained so existing links remain
# stable.
PRODUCT_FAMILIES = {
    2: 61, 3: 61, 4: 37, 5: 62, 6: 63, 7: 64, 8: 65, 9: 66, 10: 67,
    11: 68, 12: 69, 13: 70, 14: 71, 15: 72, 16: 73, 17: 74, 18: 74,
    19: 76, 20: 75, 21: 76, 22: 37, 23: 77, 24: 79, 25: 78, 26: 80,
    27: 85, 28: 81, 29: 85, 30: 82, 31: 83, 32: 86, 33: 87, 34: 85,
    36: 88, 37: 72, 39: 85, 40: 85, 41: 79, 42: 85, 43: 85, 45: 48,
    46: 48, 48: 49, 49: 95, 51: 95, 52: 49, 53: 49, 55: 97, 56: 95,
    57: 49, 58: 97, 59: 147, 60: 147, 61: 148, 62: 148, 63: 148,
    64: 148, 65: 149, 66: 149, 67: 100, 68: 149, 69: 100, 70: 101,
    71: 100, 72: 100, 74: 113, 75: 113, 76: 113, 77: 113, 78: 112,
    81: 111, 82: 110, 206: 95, 231: 157,
}


# Names come from the pre-consolidation family export. Icon paths are restored
# from the repository's historical data where available.
FAMILY_DEFINITIONS = {
    37: ("MAGNETO  LINEAR", "magneto-linear", "Family/magnetar_linear_4cm.png"),
    48: ("BD LINEO", "bd-lineo", "Family/Bardia_Mini_render.png"),
    49: ("MD LINEO", "md-lineo-pendant", "Family/Mirdamad_Old_render.png"),
    61: ("Magnet Track", "magnet-track", "Family/Magnetar_Recessed_4cm_rail.png"),
    62: ("MAGNETO DOT LINEAR", "magneto-dot-linear", "Family/magnetar_dot_linear_4cm.png"),
    63: ("MAGNETO ROTATE LINEAR", "magneto-rotate-linear", "Family/magnetar_rotate_linear_4cm.png"),
    64: ("MAGNETO ROTATE DOT LINEAR", "magneto-rotate-dot-linear", "Family/magnetar_rotate_dot_4cm.png"),
    65: ("MAGNETO  ANGLE LINEAR", "magneto-angle-linear", "Family/magnetar_angle_linear_4cm.png"),
    66: ("MAGNETO ANGLE DOT LINEAR", "magneto-angle-dot-linear", "Family/magnetar_angle_dot_4cm.png"),
    67: ("MAGNETO SPOT DOT PANEL", "magneto-spot-dot-panel", "Family/magnetar_spot_dot_panel_4cm.png"),
    68: ("MAGNETO SPOT PANEL", "magneto-spot-panel", "Family/magnetar_spot_panel_4cm.png"),
    69: ("MAGNETO SPOT 65", "magneto-spot-65", "Family/magnetar_spot_65_4cm.png"),
    70: ("MAGNETO  SMALL SPOT 35", "magneto-large-spot-35", "Family/magnetar_spot_35_4cm.png"),
    71: ("MAGNETO PENDANT 65", "magneto-pendant-65", "Family/magnetar_pendant_65_4cm.png"),
    72: ("MAGNETO PENDANT 35", "magneto-pendant-35", "Family/magnetar_spot_35_4cm_azHuJFb.png"),
    73: ("MAGNETO TUBE PLAXI", "magneto-tube-plaxi", "Family/magnetar_tube_4cm.png"),
    74: ("MAGNETO  RESSED TRACK TRIMLES", "magneto-ressed-track-trimles", "Family/Magnetar_trim_3cm_rail_W41bCJ3.png"),
    75: ("MAGNETO LARGE FLEXIBLE LINEAR", "magneto-large-flexible-linear", "Family/magnetar_flex_4cm_ULpWutx.png"),
    76: ("MAGNET SURFACE & PENDANT SMALL RAIL", "magnet-surface-pendant-small-rail", "Family/Magnetar_Circle_3cm_rail_hBHknzG.png"),
    77: ("MAGNETO LARGE SPOT  LINEAR", "magneto-large-spot-linear", "Family/magnetar_spot_linear_4cm.png"),
    78: ("MAGNETO SMALL DOT LINEAR", "magneto-small-dot-linear", "Family/magnetar_dot_linear_2cm_2ZZT4gT.png"),
    79: ("MAGNETO SIGN EMERGENCY", "magneto-sign-emergency", "Family/exit.png"),
    80: ("MAGNETO SMALL ROTATE LINEAR", "magneto-small-rotate-linear", "Family/magnetar_rotate_linear_2cm_JN9MOkX.png"),
    81: ("MAGNETO SMALL ROTATE DOT LINEAR", "magneto-small-rotate-dot-linear", "Family/magnetar_rotate_dot_2cm_5g6iW3M.png"),
    82: ("MAGNETO SMALL ANGLE LINEAR", "magneto-small-angle-linear", "Family/magnetar_angle_linear_2cm_cbmcutx.png"),
    83: ("MAGNETO SMALL ANGLE DOT LINEAR", "magneto-small-angle-dot-linear", "Family/magnetar_angle_dot_2cm_Eey4ROO.png"),
    85: ("SP LINEO", "sp-lineo", "Family/Sepehr_Mid.png"),
    86: ("MAGNETO SAMLL SPOT LIA", "magneto-samll-spot-lia", "Family/magnetar_spot_55_2cm_AeDfxXR.png"),
    87: ("MAGNETO SMALL SPOT 55", "magneto-small-spot-55", "Family/magnetar_spot_55_2cm_15On1su_eUQS2Wc.png"),
    88: ("MAGNETO SMALL SPOT 35", "magneto-small-spot-35", "Family/magnetar_spot_35_2cm.png"),
    95: ("MD LINEO", "md-lineo-surface", "Family/Mirdamad_Mid_render.png"),
    97: ("TABAN", "taban", "Family/Taban_Double_render.png"),
    100: ("PERANSA", "peransa", "Family/ringlight_inside_90cm_surface.png"),
    101: ("HALOO", "haloo", "Family/Bahar_60x60.png"),
    110: ("MOON", "moon", "Family/moon_120.png"),
    111: ("BAMBO", "bambo", "Family/bambo_Dot_wall.png"),
    112: ("ARIN", "arin", "Family/Ariyan_pendant_render.png"),
    113: ("HELY", "hely", "Family/Helia_Mid_AhY3H9G.png"),
    147: ("TRIMLESS", "trimless", "Family/Trimless_8_render.png"),
    148: ("PAYAM", "payam", "Family/Payam_8.png"),
    149: ("BAHAR", "bahar", "Family/Bahar_Double_render.png"),
    157: ("Karen Highbay", "karen-highbay", "Family/Screenshot_2026-07-02_134215.png"),
}


def technical(
    lumens=None,
    *,
    variant_lumens=None,
    color_temperature=4000,
    cri=80,
    beam_angle=None,
    voltage="",
    ip_rating="",
    lifespan=50000,
    lamp_base_type="",
    dimmable=False,
):
    return {
        "lumens": lumens,
        "variant_lumens": variant_lumens,
        "color_temperature": color_temperature,
        "cri": cri,
        "beam_angle": beam_angle,
        "voltage": voltage,
        "ip_rating": ip_rating,
        "lifespan": lifespan,
        "lamp_base_type": lamp_base_type,
        "dimmable": dimmable,
    }


TECHNICAL_SPECS = {
    # Track profiles
    2: technical(color_temperature=None, cri=None, voltage="48 VDC", lifespan=None),
    3: technical(color_temperature=None, cri=None, voltage="48 VDC", lifespan=None),
    17: technical(color_temperature=None, cri=None, voltage="48 VDC", lifespan=None),
    18: technical(color_temperature=None, cri=None, voltage="48 VDC", lifespan=None),
    19: technical(color_temperature=None, cri=None, voltage="48 VDC", lifespan=None),
    21: technical(color_temperature=None, cri=None, voltage="48 VDC", lifespan=None),

    # 4 cm magnetic luminaires
    4: technical(1200, variant_lumens=[1200], voltage="48 VDC", ip_rating="IP44"),
    5: technical(2400, variant_lumens=[2400], beam_angle=42, voltage="48 VDC", ip_rating="IP44"),
    6: technical(1200, variant_lumens=[1200], voltage="48 VDC", ip_rating="IP44"),
    7: technical(1200, variant_lumens=[1200], beam_angle=42, voltage="48 VDC", ip_rating="IP44"),
    8: technical(1200, variant_lumens=[1200], voltage="48 VDC", ip_rating="IP44"),
    9: technical(1200, variant_lumens=[1200], beam_angle=42, voltage="48 VDC", ip_rating="IP44"),
    10: technical(1200, variant_lumens=[1200], beam_angle=42, voltage="48 VDC", ip_rating="IP44"),
    11: technical(1200, variant_lumens=[1200], voltage="48 VDC", ip_rating="IP44"),
    12: technical(1650, variant_lumens=[1650], beam_angle=42, voltage="48 VDC", ip_rating="IP44"),
    13: technical(330, variant_lumens=[330], beam_angle=42, voltage="48 VDC", ip_rating="IP44"),
    14: technical(1650, variant_lumens=[1650], beam_angle=42, voltage="48 VDC", ip_rating="IP44"),
    15: technical(330, variant_lumens=[330], beam_angle=42, voltage="48 VDC", ip_rating="IP44"),
    16: technical(720, variant_lumens=[720], voltage="48 VDC", ip_rating="IP44"),
    20: technical(720, variant_lumens=[720], voltage="48 VDC", ip_rating="IP44"),
    23: technical(1800, variant_lumens=[600, 1200, 1800], beam_angle=42, voltage="48 VDC", ip_rating="IP44"),
    24: technical(160, variant_lumens=[160], voltage="48 VDC", ip_rating="IP54"),

    # 2 cm magnetic luminaires
    22: technical(1200, variant_lumens=[1200], voltage="48 VDC", ip_rating="IP44"),
    25: technical(1980, variant_lumens=[1980], beam_angle=42, voltage="48 VDC", ip_rating="IP44"),
    26: technical(1200, variant_lumens=[1200], voltage="48 VDC", ip_rating="IP44"),
    28: technical(1980, variant_lumens=[1980], beam_angle=42, voltage="48 VDC", ip_rating="IP44"),
    30: technical(1200, variant_lumens=[1200], voltage="48 VDC", ip_rating="IP44"),
    31: technical(1980, variant_lumens=[1980], beam_angle=42, voltage="48 VDC", ip_rating="IP44"),
    32: technical(1650, variant_lumens=[1650], beam_angle=42, voltage="48 VDC", ip_rating="IP44"),
    33: technical(1650, variant_lumens=[1650], beam_angle=42, voltage="48 VDC", ip_rating="IP44"),
    36: technical(330, variant_lumens=[330], beam_angle=42, voltage="48 VDC", ip_rating="IP44"),
    37: technical(330, variant_lumens=[330], beam_angle=42, voltage="48 VDC", ip_rating="IP44"),
    41: technical(160, variant_lumens=[160], voltage="48 VDC", ip_rating="IP54"),

    # Recessed, surface and pendant linear luminaires
    27: technical(1500, variant_lumens=[1500], voltage="220-240 VAC", ip_rating="IP44"),
    29: technical(2000, variant_lumens=[2000], voltage="220-240 VAC", ip_rating="IP44"),
    34: technical(1320, variant_lumens=[1320], voltage="220-240 VAC", ip_rating="IP44"),
    39: technical(3000, variant_lumens=[3000], voltage="220-240 VAC", ip_rating="IP44"),
    40: technical(3000, variant_lumens=[3000], voltage="220-240 VAC", ip_rating="IP44"),
    42: technical(3000, variant_lumens=[3000], voltage="220-240 VAC", ip_rating="IP44"),
    43: technical(4500, variant_lumens=[4500], voltage="220-240 VAC", ip_rating="IP44"),
    45: technical(1500, variant_lumens=[1500], voltage="220-240 VAC", ip_rating="IP44"),
    46: technical(2500, variant_lumens=[2500], voltage="220-240 VAC", ip_rating="IP44"),
    48: technical(1500, variant_lumens=[1500], voltage="220-240 VAC", ip_rating="IP44"),
    49: technical(1500, variant_lumens=[1500], voltage="220-240 VAC", ip_rating="IP44"),
    51: technical(2000, variant_lumens=[2000], voltage="220-240 VAC", ip_rating="IP44"),
    52: technical(2000, variant_lumens=[2000], voltage="220-240 VAC", ip_rating="IP44"),
    53: technical(1320, variant_lumens=[1320], voltage="220-240 VAC", ip_rating="IP44"),
    56: technical(2500, variant_lumens=[2500], voltage="220-240 VAC", ip_rating="IP44"),
    57: technical(2500, variant_lumens=[2500], voltage="220-240 VAC", ip_rating="IP44"),
    206: technical(1320, variant_lumens=[1320], voltage="220-240 VAC", ip_rating="IP44"),

    # Panel and downlight families
    55: technical(3850, variant_lumens=[3850], voltage="220-240 VAC", ip_rating="IP44"),
    58: technical(7700, variant_lumens=[7700], voltage="220-240 VAC", ip_rating="IP44"),
    59: technical(color_temperature=4000, cri=None, voltage="220-240 VAC", ip_rating="IP44", lifespan=None),
    60: technical(color_temperature=4000, cri=None, voltage="220-240 VAC", ip_rating="IP44", lifespan=None),
    61: technical(630, variant_lumens=[630], color_temperature=3000, voltage="220-240 VAC", ip_rating="IP20"),
    62: technical(color_temperature=None, cri=None, lifespan=None, lamp_base_type="GU10"),
    63: technical(color_temperature=None, cri=None, lifespan=None, lamp_base_type="GU10"),
    64: technical(color_temperature=None, cri=None, lifespan=None, lamp_base_type="GU10"),
    65: technical(color_temperature=4000, voltage="220-240 VAC", ip_rating="IP44", lamp_base_type="GU10"),
    66: technical(color_temperature=4000, voltage="220-240 VAC", ip_rating="IP44", lamp_base_type="GU10"),
    67: technical(10000, variant_lumens=[3000, 5000, 7000, 10000], beam_angle=180, voltage="220-240 VAC", ip_rating="IP44"),
    68: technical(color_temperature=4000, voltage="220-240 VAC", ip_rating="IP44", lamp_base_type="GU10"),
    69: technical(10000, variant_lumens=[5000, 7000, 10000], beam_angle=180, voltage="220-240 VAC", ip_rating="IP44"),
    70: technical(3780, variant_lumens=[3780], beam_angle=180, voltage="220-240 VAC", ip_rating="IP44"),
    71: technical(10000, variant_lumens=[5000, 7000, 10000], beam_angle=180, voltage="220-240 VAC", ip_rating="IP44"),
    72: technical(7000, variant_lumens=[7000], beam_angle=180, voltage="220-240 VAC", ip_rating="IP44"),

    # Decorative, outdoor and industrial families
    74: technical(color_temperature=None, cri=None, voltage="220-240 VAC", lifespan=None, lamp_base_type="E27"),
    75: technical(1250, variant_lumens=[1250], cri=None, voltage="220-240 VAC", lamp_base_type="E27"),
    76: technical(cri=None, voltage="220-240 VAC", lamp_base_type="E27"),
    77: technical(1250, variant_lumens=[1250, 1250], voltage="220-240 VAC", ip_rating="IP44"),
    78: technical(1500, variant_lumens=[1500, 1500], voltage="220-240 VAC", ip_rating="IP44"),
    81: technical(1200, variant_lumens=[1200], cri=None, voltage="220 VAC", ip_rating="IP20"),
    82: technical(2250, variant_lumens=[1250, 1750, 2250], cri=None, voltage="220-240 VAC", ip_rating="IP65"),
    231: technical(15000, variant_lumens=[10000, 15000], voltage="220-240 VAC", ip_rating="IP54"),
}


FORBIDDEN_LATIN = re.compile(r"(?i)\b" + "are" + "nd" + r"\b")


def clean_text(value):
    if not value:
        return value
    value = FORBIDDEN_LATIN.sub("Verona", value)
    return value.replace(
        "\u0622\u0631\u0646\u062f",
        "\u0648\u0631\u0648\u0646\u0627",
    )


def product_fingerprint(product):
    return (
        str(product.wattage) if product.wattage is not None else None,
        tuple(
            (
                variant.id,
                str(variant.wattage) if variant.wattage is not None else None,
                variant.dimension_id,
                (
                    str(variant.dimension.width) if variant.dimension and variant.dimension.width is not None else None,
                    str(variant.dimension.height) if variant.dimension and variant.dimension.height is not None else None,
                    str(variant.dimension.depth) if variant.dimension and variant.dimension.depth is not None else None,
                ),
            )
            for variant in product.variants.select_related("dimension").order_by("id")
        ),
    )


class Command(BaseCommand):
    help = (
        "Restore the former product-family structure and apply technical "
        "specifications without changing wattages or dimensions. Runs as a "
        "dry-run unless --apply is supplied."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--apply",
            action="store_true",
            help="Commit the family restoration and technical data updates.",
        )

    def handle(self, *args, **options):
        apply_changes = options["apply"]
        products = {
            product.id: product
            for product in Product.objects.filter(id__in=TARGET_PRODUCT_IDS)
            .select_related("category", "family")
            .prefetch_related("variants__dimension")
        }
        missing = sorted(set(TARGET_PRODUCT_IDS) - set(products))
        if missing:
            raise CommandError(
                "Required product IDs are missing: "
                + ", ".join(str(product_id) for product_id in missing)
            )
        if set(PRODUCT_FAMILIES) != set(TARGET_PRODUCT_IDS):
            raise CommandError("The family mapping does not cover every target product.")
        if set(TECHNICAL_SPECS) != set(TARGET_PRODUCT_IDS):
            raise CommandError("The technical mapping does not cover every target product.")

        before = {
            product_id: product_fingerprint(product)
            for product_id, product in products.items()
        }
        source_applications = {}
        for product_id, family_id in PRODUCT_FAMILIES.items():
            product = products[product_id]
            source_applications.setdefault(family_id, set())
            if product.family_id:
                source_applications[family_id].update(
                    product.family.applications.values_list("id", flat=True)
                )

        mode = "APPLY" if apply_changes else "DRY RUN"
        self.stdout.write(
            f"{mode}: {len(products)} products, "
            f"{len(FAMILY_DEFINITIONS)} restored families"
        )

        with transaction.atomic():
            restored_families = {}
            for family_id, (name, slug, icon) in FAMILY_DEFINITIONS.items():
                conflicting = Family.objects.filter(slug=slug).exclude(pk=family_id)
                if conflicting.exists():
                    raise CommandError(
                        f"Family slug {slug!r} is already used by family "
                        f"{conflicting.first().pk}."
                    )

                assigned_product_ids = [
                    product_id
                    for product_id, mapped_family_id in PRODUCT_FAMILIES.items()
                    if mapped_family_id == family_id
                ]
                representative = products[assigned_product_ids[0]]
                family, _ = Family.objects.get_or_create(
                    pk=family_id,
                    defaults={"category_id": representative.category_id},
                )
                family.name = name
                if hasattr(family, "name_en"):
                    family.name_en = name
                if hasattr(family, "name_fa"):
                    family.name_fa = name
                family.slug = slug
                family.icon = icon
                family.icon_alt = name
                family.number = None
                family.category_id = representative.category_id
                family.is_active = True
                family.subtitle = ""
                if hasattr(family, "subtitle_en"):
                    family.subtitle_en = ""
                if hasattr(family, "subtitle_fa"):
                    family.subtitle_fa = ""
                family.meta_title = None
                if hasattr(family, "meta_title_en"):
                    family.meta_title_en = None
                if hasattr(family, "meta_title_fa"):
                    family.meta_title_fa = None
                family.meta_description = ""
                if hasattr(family, "meta_description_en"):
                    family.meta_description_en = ""
                if hasattr(family, "meta_description_fa"):
                    family.meta_description_fa = ""
                family.canonical_url = ""
                family.save()
                family.applications.set(source_applications.get(family_id, set()))
                restored_families[family_id] = family

            updated_variants = 0
            for product_id in TARGET_PRODUCT_IDS:
                product = products[product_id]
                product.family = restored_families[PRODUCT_FAMILIES[product_id]]
                spec = TECHNICAL_SPECS[product_id]
                for field in (
                    "lumens",
                    "color_temperature",
                    "cri",
                    "beam_angle",
                    "voltage",
                    "ip_rating",
                    "lifespan",
                    "lamp_base_type",
                    "dimmable",
                ):
                    setattr(product, field, spec[field])
                product.save(
                    update_fields=[
                        "family",
                        "lumens",
                        "color_temperature",
                        "cri",
                        "beam_angle",
                        "voltage",
                        "ip_rating",
                        "lifespan",
                        "lamp_base_type",
                        "dimmable",
                        "updated_at",
                    ]
                )

                variants = list(product.variants.select_related("dimension").order_by("id"))
                variant_lumens = spec["variant_lumens"]
                if variant_lumens is not None and len(variant_lumens) != len(variants):
                    raise CommandError(
                        f"Product {product_id} has {len(variants)} variants but "
                        f"{len(variant_lumens)} lumen values."
                    )
                for index, variant in enumerate(variants, start=1):
                    variant.lumens = (
                        variant_lumens[index - 1]
                        if variant_lumens is not None
                        else None
                    )
                    variant.color_temperature = spec["color_temperature"]
                    variant.sku = clean_text(variant.sku)
                    variant.model_name = clean_text(variant.model_name)
                    variant.note = clean_text(variant.note)
                    variant.save(
                        update_fields=[
                            "lumens",
                            "color_temperature",
                            "sku",
                            "model_name",
                            "note",
                        ]
                    )
                    if variant.dimension:
                        cleaned_label = clean_text(variant.dimension.label)
                        if cleaned_label != variant.dimension.label:
                            variant.dimension.label = cleaned_label
                            variant.dimension.save(update_fields=["label"])
                    updated_variants += 1

            # Remove the prohibited catalog brand from all user-visible product
            # and family text fields, including records outside this catalog set.
            text_models = (
                (
                    Family,
                    (
                        "name", "name_en", "name_fa", "subtitle", "subtitle_en",
                        "subtitle_fa", "meta_title", "meta_title_en",
                        "meta_title_fa", "meta_description",
                        "meta_description_en", "meta_description_fa", "icon_alt",
                    ),
                ),
                (
                    Product,
                    (
                        "name", "name_en", "name_fa", "subtitle", "subtitle_en",
                        "subtitle_fa", "description", "description_en",
                        "description_fa", "full_description",
                        "full_description_en", "full_description_fa",
                        "meta_title", "meta_title_en", "meta_title_fa",
                        "meta_description", "meta_description_en",
                        "meta_description_fa", "image1_alt", "image1_alt_en",
                        "image1_alt_fa", "image2_alt", "image2_alt_en",
                        "image2_alt_fa", "image3_alt", "image3_alt_en",
                        "image3_alt_fa", "image4_alt", "image4_alt_en",
                        "image4_alt_fa",
                    ),
                ),
                (ProductVariant, ("model_name", "sku", "note")),
                (Dimension, ("label",)),
            )
            sanitized_records = 0
            for model, requested_fields in text_models:
                actual_fields = {
                    field.name for field in model._meta.get_fields()
                    if getattr(field, "concrete", False)
                }
                fields = [
                    field for field in requested_fields if field in actual_fields
                ]
                for record in model.objects.all().only("pk", *fields):
                    changed = []
                    for field in fields:
                        value = getattr(record, field)
                        cleaned = clean_text(value)
                        if cleaned != value:
                            setattr(record, field, cleaned)
                            changed.append(field)
                    if changed:
                        record.save(update_fields=changed)
                        sanitized_records += 1

            refreshed = {
                product.id: product
                for product in Product.objects.filter(id__in=TARGET_PRODUCT_IDS)
                .prefetch_related("variants__dimension")
            }
            changed_physical = [
                product_id
                for product_id, product in refreshed.items()
                if product_fingerprint(product) != before[product_id]
            ]
            if changed_physical:
                raise CommandError(
                    "Wattage or dimension changed unexpectedly for products: "
                    + ", ".join(str(product_id) for product_id in changed_physical)
                )

            if not apply_changes:
                transaction.set_rollback(True)

        self.stdout.write(
            self.style.SUCCESS(
                f"{mode} complete: {updated_variants} variants updated; "
                f"{sanitized_records} records cleaned; wattages and dimensions unchanged."
            )
        )
