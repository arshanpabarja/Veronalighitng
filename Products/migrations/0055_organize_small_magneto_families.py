from django.db import migrations


SMALL_MAGNETO_CATEGORY_SLUG = "magent-small-family"

RECESSED_TRIM_FAMILY_SLUG = "magneto-ressed-trim"
RECESSED_TRIM_PRODUCT_SLUG = "magnetar-smll-ressed-track-trim"
RECESSED_TRIMLESS_FAMILY_SLUG = "magneto-small-recessed-track-trimless"
RECESSED_TRIMLESS_PRODUCT_SLUG = "magnetar-small-ressed-track-trimles"

SMALL_PENDANT_35_FAMILY_SLUG = "magneto-small-pendant-35"
SMALL_PENDANT_35_PRODUCT_SLUG = "magnetar-small-pendant-35"


ORDERED_FAMILY_SLUGS = (
    # Rails
    RECESSED_TRIMLESS_FAMILY_SLUG,
    RECESSED_TRIM_FAMILY_SLUG,
    "magnetar-small-surface-pendant-track",
    "magnetar-smll-surface-pendant-track",
    # Pendants
    SMALL_PENDANT_35_FAMILY_SLUG,
    "magnetar-small-pendant-65",
    # Linear families shown in the supplied screenshots
    "magneto-small-linear",
    "magneto-small-dot-linear",
    "magneto-small-rotate-linear",
    "magneto-small-rotate-dot-linear",
    "magneto-small-angle-linear",
    "magneto-small-angle-dot-linear",
    # Spots
    "magneto-small-spot-35",
    "magneto-small-spot-55",
    # Remaining small-system family
    "magnetar-small-flexible-linear",
)


def _copy_applications(source_family, target_family):
    if source_family:
        target_family.applications.set(source_family.applications.all())


def organize_small_magneto_families(apps, schema_editor):
    Category = apps.get_model("Products", "Category")
    Family = apps.get_model("Products", "Family")
    Product = apps.get_model("Products", "Product")

    small_category = Category.objects.filter(
        slug=SMALL_MAGNETO_CATEGORY_SLUG
    ).first()
    if not small_category:
        return

    trim_family = Family.objects.filter(
        slug=RECESSED_TRIM_FAMILY_SLUG
    ).first()
    trim_product = Product.objects.filter(
        slug=RECESSED_TRIM_PRODUCT_SLUG
    ).first()
    trimless_product = Product.objects.filter(
        slug=RECESSED_TRIMLESS_PRODUCT_SLUG
    ).first()

    if trim_family:
        trim_family.name = "مگنتو ریل ترک لبه دار"
        trim_family.name_fa = "مگنتو ریل ترک لبه دار"
        trim_family.name_en = "MAGNETO SMALL RECESSED TRACK TRIM"
        trim_family.subtitle_fa = (
            "خانواده ریل‌های توکار لبه‌دار مگنتو اسمال با ورودی ۴۸ ولت DC"
        )
        trim_family.subtitle_en = (
            "Low-voltage flanged recessed tracks for the 48V DC "
            "MAGNETO SMALL system"
        )
        trim_family.meta_title_fa = (
            "خانواده مگنتو ریل ترک لبه دار | ورونا لایتینگ"
        )
        trim_family.meta_title_en = (
            "MAGNETO SMALL Recessed Track Trim | Verona Lighting"
        )
        trim_family.meta_description_fa = (
            "خانواده ریل توکار لبه‌دار مگنتو اسمال با ورودی ۴۸ ولت DC، "
            "مناسب نورپردازی یکپارچه در فضاهای مسکونی و تجاری."
        )
        trim_family.meta_description_en = (
            "MAGNETO SMALL flanged recessed magnetic track family for "
            "48V DC residential and commercial lighting systems."
        )
        trim_family.icon_alt_fa = "ریل توکار لبه‌دار مگنتو اسمال"
        trim_family.icon_alt_en = "MAGNETO SMALL recessed track trim"
        trim_family.category = small_category
        trim_family.is_active = True
        trim_family.save()

    if trimless_product:
        trimless_family, _ = Family.objects.update_or_create(
            slug=RECESSED_TRIMLESS_FAMILY_SLUG,
            defaults={
                "name": "مگنتو ریل ترک بدون لبه",
                "name_fa": "مگنتو ریل ترک بدون لبه",
                "name_en": "MAGNETO SMALL RECESSED TRACK TRIMLESS",
                "icon": trimless_product.image1,
                "icon_alt_fa": "ریل توکار بدون لبه مگنتو اسمال",
                "icon_alt_en": "MAGNETO SMALL trimless recessed track",
                "category": small_category,
                "is_active": True,
                "subtitle_fa": (
                    "خانواده ریل‌های توکار بدون لبه و بدون فریم مگنتو اسمال "
                    "با ورودی ۴۸ ولت DC"
                ),
                "subtitle_en": (
                    "Low-voltage trimless recessed tracks for the 48V DC "
                    "MAGNETO SMALL system"
                ),
                "meta_title_fa": (
                    "خانواده مگنتو ریل ترک بدون لبه | ورونا لایتینگ"
                ),
                "meta_title_en": (
                    "MAGNETO SMALL Trimless Recessed Track | Verona Lighting"
                ),
                "meta_description_fa": (
                    "خانواده ریل توکار بدون لبه و بدون فریم مگنتو اسمال با "
                    "ورودی ۴۸ ولت DC، مناسب نورپردازی مینیمال و یکپارچه."
                ),
                "meta_description_en": (
                    "MAGNETO SMALL trimless recessed magnetic track family "
                    "for minimalist 48V DC lighting installations."
                ),
            },
        )
        _copy_applications(trim_family, trimless_family)
        trimless_product.family = trimless_family
        trimless_product.save(update_fields=["family"])

    if trim_product and trim_family and trim_product.family_id != trim_family.id:
        trim_product.family = trim_family
        trim_product.save(update_fields=["family"])

    pendant_35_product = Product.objects.filter(
        slug=SMALL_PENDANT_35_PRODUCT_SLUG
    ).first()
    if pendant_35_product:
        pendant_65_family = Family.objects.filter(
            slug="magnetar-small-pendant-65"
        ).first()
        pendant_35_family, _ = Family.objects.update_or_create(
            slug=SMALL_PENDANT_35_FAMILY_SLUG,
            defaults={
                "name": "مگنتو آویز اسمال 35",
                "name_fa": "مگنتو آویز اسمال 35",
                "name_en": "MAGNETO SMALL PENDANT 35",
                "icon": pendant_35_product.image1,
                "icon_alt_fa": "چراغ آویز مگنتو اسمال 35",
                "icon_alt_en": "MAGNETO SMALL PENDANT 35",
                "category": small_category,
                "is_active": True,
                "subtitle_fa": (
                    "خانواده چراغ‌های آویز ریلی مگنتو اسمال با ورودی ۴۸ ولت DC"
                ),
                "subtitle_en": (
                    "Low-voltage pendant lights for the 48V DC MAGNETO SMALL system"
                ),
                "meta_title_fa": (
                    "خانواده مگنتو آویز اسمال 35 | ورونا لایتینگ"
                ),
                "meta_title_en": "MAGNETO SMALL PENDANT 35 | Verona Lighting",
                "meta_description_fa": (
                    "خانواده چراغ آویز مگنتو اسمال 35 با ورودی ۴۸ ولت DC، "
                    "مناسب نورپردازی دکوراتیو فضاهای مسکونی و تجاری."
                ),
                "meta_description_en": (
                    "MAGNETO SMALL PENDANT 35 family for decorative 48V DC "
                    "residential and commercial magnetic-track lighting."
                ),
            },
        )
        _copy_applications(pendant_65_family, pendant_35_family)
        pendant_35_product.family = pendant_35_family
        pendant_35_product.save(update_fields=["family"])

    families_by_slug = {
        family.slug: family
        for family in Family.objects.filter(
            category=small_category,
            slug__in=ORDERED_FAMILY_SLUGS,
        )
    }
    for position, slug in enumerate(ORDERED_FAMILY_SLUGS, start=1):
        family = families_by_slug.get(slug)
        if family and family.number != position:
            family.number = position
            family.save(update_fields=["number"])


class Migration(migrations.Migration):

    dependencies = [
        ("Products", "0054_update_magneto_color_temperature_descriptions"),
    ]

    operations = [
        migrations.RunPython(
            organize_small_magneto_families,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
