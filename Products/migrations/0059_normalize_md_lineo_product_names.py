from django.db import migrations


MD_LINEO_FAMILY_SLUGS = ("md-lineo-pendant", "md-lineo-surface")

PRODUCT_NAMES_FA = {
    "mirdamad-mini-pendant": "چراغ خطی MD مینی",
    "md-narrow-pendant": "چراغ خطی MD نرو",
    "md-narrow-dot-pendant": "چراغ خطی دات MD نرو",
    "md-mid-pendant": "چراغ خطی MD مید",
    "md-mini-surface": "چراغ خطی MD مینی",
    "md-narrow-surface": "چراغ خطی MD نرو",
    "md-narrow-dot-surface": "چراغ خطی دات MD نرو",
    "md-mid-surface": "چراغ خطی MD مید",
}


def normalize_md_lineo_product_names(apps, schema_editor):
    Product = apps.get_model("Products", "Product")

    products = Product.objects.filter(
        family__slug__in=MD_LINEO_FAMILY_SLUGS,
        slug__in=PRODUCT_NAMES_FA,
    )
    for product in products:
        name_fa = PRODUCT_NAMES_FA[product.slug]
        Product.objects.filter(pk=product.pk).update(
            name=name_fa,
            name_fa=name_fa,
            meta_title_fa=f"{name_fa} | ورونا لایتینگ",
        )


class Migration(migrations.Migration):

    dependencies = [
        ("Products", "0058_normalize_bd_lineo_product_names"),
    ]

    operations = [
        migrations.RunPython(
            normalize_md_lineo_product_names,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
