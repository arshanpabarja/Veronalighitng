from django.db import migrations


def use_persian_ceiling_term(apps, schema_editor):
    for model_name in ("Family", "Product"):
        model = apps.get_model("Products", model_name)
        for item in model.objects.filter(name_fa__contains="سیلینگ").iterator():
            item.name_fa = item.name_fa.replace("سیلینگ", "سقفی")
            item.save(update_fields=["name_fa"])


class Migration(migrations.Migration):
    dependencies = [
        ("Products", "0069_remove_downlight_from_gypsum_product_names"),
    ]

    operations = [
        migrations.RunPython(
            use_persian_ceiling_term,
            reverse_code=migrations.RunPython.noop,
        )
    ]
