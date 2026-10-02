import re
from decimal import Decimal

from django.db import migrations


MD_WIDE_IMAGE = "products/md_wide.png"

SOURCE_TARGETS = (
    ("md-mid-surface", "md-wide-surface", "surface"),
    ("md-mid-pendant", "md-wide-pendant", "pendant"),
)


def _file_name(value):
    return str(value) if value else ""


def _adapt_md_mid_copy(value):
    if not value:
        return value

    replacements = (
        ("MD MID", "MD WIDE"),
        ("Mirdamad Mid", "Mirdamad Wide"),
        ("ام‌دی مید", "MD واید"),
        ("MD مید", "MD واید"),
        ("۲۵ وات", "۳۰ وات"),
    )
    updated = value
    for old, new in replacements:
        updated = updated.replace(old, new)
    updated = re.sub(r"(?i)25\s*W(?=/|\b)", "30W", updated)
    updated = re.sub(r"(?i)25\s*w(?=/|\b)", "30 w", updated)
    return updated


def create_md_wide_products(apps, schema_editor):
    Dimension = apps.get_model("Products", "Dimension")
    Installment = apps.get_model("Products", "Installment")
    Product = apps.get_model("Products", "Product")
    ProductVariant = apps.get_model("Products", "ProductVariant")

    for source_slug, target_slug, mounting_type in SOURCE_TARGETS:
        source = Product.objects.filter(slug=source_slug).first()
        if not source:
            continue

        target, _ = Product.objects.update_or_create(
            slug=target_slug,
            defaults={
                "order": (source.order or 0) + 1,
                "name": "چراغ خطی MD واید",
                "name_fa": "چراغ خطی MD واید",
                "name_en": "MD WIDE",
                "category": source.category,
                "family": source.family,
                "is_active": source.is_active,
                "subtitle_fa": _adapt_md_mid_copy(source.subtitle_fa),
                "subtitle_en": _adapt_md_mid_copy(source.subtitle_en),
                "description_fa": _adapt_md_mid_copy(source.description_fa),
                "description_en": _adapt_md_mid_copy(source.description_en),
                "full_description_fa": _adapt_md_mid_copy(
                    source.full_description_fa
                ),
                "full_description_en": _adapt_md_mid_copy(
                    source.full_description_en
                ),
                "wattage": Decimal("30.00"),
                "lumens": source.lumens,
                "color_temperature": source.color_temperature,
                "cri": source.cri,
                "beam_angle": source.beam_angle,
                "voltage": source.voltage,
                "ip_rating": source.ip_rating,
                "dimmable": source.dimmable,
                "lamp_base_type": source.lamp_base_type,
                "lifespan": source.lifespan,
                "mounting_type": mounting_type,
                "image1": MD_WIDE_IMAGE,
                "image1_alt_fa": "چراغ خطی MD واید ورونا لایتینگ",
                "image1_alt_en": "MD WIDE linear light by Verona Lighting",
                "image2": _file_name(source.image2),
                "image2_alt_fa": _adapt_md_mid_copy(source.image2_alt_fa),
                "image2_alt_en": _adapt_md_mid_copy(source.image2_alt_en),
                "image3": _file_name(source.image3),
                "image3_alt_fa": _adapt_md_mid_copy(source.image3_alt_fa),
                "image3_alt_en": _adapt_md_mid_copy(source.image3_alt_en),
                "image4": _file_name(source.image4),
                "image4_alt_fa": _adapt_md_mid_copy(source.image4_alt_fa),
                "image4_alt_en": _adapt_md_mid_copy(source.image4_alt_en),
                # The MD MID hover image contains its old dimensions, so it
                # must not be reused for MD WIDE.
                "hover_image": "",
                "meta_title_fa": "چراغ خطی MD واید | ورونا لایتینگ",
                "meta_title_en": (
                    "MD WIDE Trimless Linear 30W/m | Verona Lighting"
                ),
                "meta_description_fa": _adapt_md_mid_copy(
                    source.meta_description_fa
                ),
                "meta_description_en": _adapt_md_mid_copy(
                    source.meta_description_en
                ),
                "canonical_url": "",
                "catelog": _file_name(source.catelog),
            },
        )

        target.finishes.set(source.finishes.all())

        target.installment.all().delete()
        for installment in source.installment.all():
            Installment.objects.create(
                product=target,
                name=installment.name,
                step=installment.step,
                description=installment.description,
            )

        target.variants.all().delete()
        for variant_number, variant in enumerate(
            source.variants.select_related("dimension").all(),
            start=1,
        ):
            source_dimension = variant.dimension
            dimension = Dimension.objects.create(
                label=(
                    f"Verona-{target.pk}-{variant_number} | "
                    "100 × 7 × 8.5 cm"
                ),
                width=Decimal("1000.00"),
                height=Decimal("70.00"),
                depth=Decimal("85.00"),
                weight=(
                    source_dimension.weight if source_dimension else None
                ),
            )
            ProductVariant.objects.create(
                product=target,
                model_name="Mirdamad Wide",
                dimension=dimension,
                wattage=Decimal("30.00"),
                lumens=variant.lumens,
                color_temperature=variant.color_temperature,
                sku=f"Verona-{target.pk}-{variant_number}",
                is_active=variant.is_active,
                note=variant.note,
            )


class Migration(migrations.Migration):

    dependencies = [
        ("Products", "0059_normalize_md_lineo_product_names"),
    ]

    operations = [
        migrations.RunPython(
            create_md_wide_products,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
