from django.db import migrations


BD_LINEO_FAMILY_SLUG = "bd-lineo"

PRODUCT_NAMES_FA = {
    "bd-narrow": "چراغ خطی توکار بدون لبه BD نرو",
    "bd-mini": "چراغ خطی توکار بدون لبه BD مینی",
}


def normalize_bd_lineo_product_names(apps, schema_editor):
    Product = apps.get_model("Products", "Product")

    products = Product.objects.filter(
        family__slug=BD_LINEO_FAMILY_SLUG,
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
        ("Products", "0057_normalize_sp_lineo_product_names"),
    ]

    operations = [
        migrations.RunPython(
            normalize_bd_lineo_product_names,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
