import re

from django.db import migrations
from django.db.models import Q


TEMPERATURE_FIELDS = ("full_description_fa", "full_description_en")


def rewrite_temperature_range(value):
    """Limit Magneto description copy to the available 3000K/4000K options."""
    if not value:
        return value

    replacements = (
        # Lists of three discrete options need to become a natural two-item list.
        (
            r"3000\s*K(\s*\([^)]*\))?\s*,\s*"
            r"4000\s*K(\s*\([^)]*\))?\s*,\s*and\s*"
            r"6000\s*K(?:\s*\([^)]*\))?",
            r"3000K\1 and 4000K\2",
        ),
        (r"3000\s*K\s*,\s*4000\s*K\s*,\s*and\s*6000\s*K", "3000K and 4000K"),
        (r"3000\s*K\s*[،,]\s*4000\s*K\s*(?:و|and)\s*6000\s*K", "3000K و 4000K"),
        # Ranges occur in both Persian and English with several separators.
        (r"3000\s*K\s*(?:to|تا)\s*6000\s*K", None),
        (r"3000\s*(K?)\s*([-–—])\s*6000\s*K", None),
    )

    updated = value
    for pattern, replacement in replacements:
        if replacement is None:
            updated = re.sub(
                pattern,
                lambda match: (
                    "3000K تا 4000K"
                    if "تا" in match.group(0)
                    else (
                        f"3000{match.group(1)}{match.group(2)}4000K"
                        if match.lastindex
                        else "3000K to 4000K"
                    )
                ),
                updated,
                flags=re.IGNORECASE,
            )
        else:
            updated = re.sub(pattern, replacement, updated, flags=re.IGNORECASE)

    return updated


def update_magneto_descriptions(apps, schema_editor):
    Product = apps.get_model("Products", "Product")
    magneto_products = Product.objects.filter(
        Q(category__slug="low-voltage-magneto")
        | Q(category__parent__slug="low-voltage-magneto")
    ).distinct()

    for product in magneto_products.iterator():
        changed_fields = []
        for field_name in TEMPERATURE_FIELDS:
            current_value = getattr(product, field_name)
            updated_value = rewrite_temperature_range(current_value)
            if updated_value != current_value:
                setattr(product, field_name, updated_value)
                changed_fields.append(field_name)
        if changed_fields:
            product.save(update_fields=changed_fields)


class Migration(migrations.Migration):

    dependencies = [
        ("Products", "0053_assign_global_track_application_images"),
    ]

    operations = [
        migrations.RunPython(
            update_magneto_descriptions,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
