from django.db import migrations


def reorder_persian_catalog_names(apps, schema_editor):
    from Products.services.catalog_fa_names import translate_catalog_name

    Family = apps.get_model("Products", "Family")
    Product = apps.get_model("Products", "Product")

    for item in Family.objects.select_related("category__parent").iterator():
        category = item.category
        translated_name = translate_catalog_name(
            item.name_en or "",
            category_name=category.name_en if category else "",
            parent_category_name=(
                category.parent.name_en if category and category.parent else ""
            ),
            is_gypsum=(
                item.slug == "gypsum"
                or "gypsum" in (item.name_en or "").casefold()
                or "گچی" in (item.name_fa or "")
            ),
        )
        if translated_name != item.name_fa:
            item.name_fa = translated_name
            item.save(update_fields=["name_fa"])

    for item in Product.objects.select_related(
        "category__parent", "family"
    ).iterator():
        category = item.category
        family = item.family
        is_gypsum = bool(
            family
            and (
                family.slug == "gypsum"
                or "gypsum" in (family.name_en or "").casefold()
                or "گچی" in (family.name_fa or "")
            )
        )
        translated_name = translate_catalog_name(
            item.name_en or "",
            category_name=category.name_en if category else "",
            parent_category_name=(
                category.parent.name_en if category and category.parent else ""
            ),
            is_gypsum=is_gypsum,
        )
        if translated_name != item.name_fa:
            item.name_fa = translated_name
            item.save(update_fields=["name_fa"])


class Migration(migrations.Migration):
    dependencies = [
        ("Products", "0070_use_persian_ceiling_term"),
    ]

    operations = [
        migrations.RunPython(
            reorder_persian_catalog_names,
            reverse_code=migrations.RunPython.noop,
        )
    ]
