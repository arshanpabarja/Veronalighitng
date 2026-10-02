import re

from django.db import migrations


DOWNLIGHT_SPELLINGS = ("دان‌لایت", "دان لایت", "دانلایت")


def remove_downlight_from_gypsum_product_names(apps, schema_editor):
    Family = apps.get_model("Products", "Family")
    Product = apps.get_model("Products", "Product")
    gypsum_family_ids = Family.objects.filter(slug="gypsum").values_list(
        "id", flat=True
    )

    for product in Product.objects.filter(family_id__in=gypsum_family_ids).iterator():
        translated_name = product.name_fa or ""
        for spelling in DOWNLIGHT_SPELLINGS:
            translated_name = translated_name.replace(spelling, " ")
        translated_name = re.sub(r"\s+", " ", translated_name).strip()
        if translated_name != product.name_fa:
            product.name_fa = translated_name
            product.save(update_fields=["name_fa"])


class Migration(migrations.Migration):
    dependencies = [
        ("Products", "0068_use_persian_track_term"),
    ]

    operations = [
        migrations.RunPython(
            remove_downlight_from_gypsum_product_names,
            reverse_code=migrations.RunPython.noop,
        )
    ]
