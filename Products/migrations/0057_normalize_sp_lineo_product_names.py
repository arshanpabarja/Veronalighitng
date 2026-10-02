import re

from django.db import migrations


SP_LINEO_FAMILY_SLUG = "sp-lineo"

PRODUCT_NAMES_FA = {
    "sp-mini": "چراغ خطی توکار تریم بک‌لایت SP مینی",
    "sp-wid-ip": "چراغ توکار IP SP واید",
    "sp-narrow": "چراغ خطی توکار لبه‌دار SP نارو",
    "sp-narrow-dot": "چراغ خطی توکار دات SP نارو",
    "sp-mid-slim": "چراغ خطی توکار تریم اسلیم SP مید",
    "sp-wid": "چراغ خطی توکار تریم بک‌لایت SP واید",
    "sp-plus": "چراغ خطی توکار تریم بک‌لایت SP پلاس",
}


def normalize_sp_terms(value):
    if not value:
        return value

    value = re.sub(r"(?i)\bNARROW\b", "نارو", value)
    value = re.sub(r"نقطه[‌\s]*[اآ]?ی", "دات", value)
    value = re.sub(r"اس[‌\s-]*پی", "SP", value)
    return value.replace("باریک", "نارو")


def normalize_sp_lineo_product_names(apps, schema_editor):
    Product = apps.get_model("Products", "Product")

    products = Product.objects.filter(
        family__slug=SP_LINEO_FAMILY_SLUG,
        slug__in=PRODUCT_NAMES_FA,
    )
    for product in products:
        name_fa = PRODUCT_NAMES_FA[product.slug]
        Product.objects.filter(pk=product.pk).update(
            name=name_fa,
            name_fa=name_fa,
            meta_title_fa=normalize_sp_terms(product.meta_title_fa),
        )


class Migration(migrations.Migration):

    dependencies = [
        ("Products", "0056_split_belt_and_flexi_product_families"),
    ]

    operations = [
        migrations.RunPython(
            normalize_sp_lineo_product_names,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
