from django.db import migrations


REPLACEMENTS = (
    ("تریم لس", "بدون لبه"),
    ("تریم‌لس", "بدون لبه"),
    ("تریمد", "لبه‌دار"),
    ("تریم", "لبه‌دار"),
)


def use_persian_trim_terms(apps, schema_editor):
    for model_name in ("Family", "Product"):
        model = apps.get_model("Products", model_name)
        for item in model.objects.all().iterator():
            translated_name = item.name_fa or ""
            for old, new in REPLACEMENTS:
                translated_name = translated_name.replace(old, new)
            if translated_name != item.name_fa:
                item.name_fa = translated_name
                item.save(update_fields=["name_fa"])


class Migration(migrations.Migration):
    dependencies = [
        ("Products", "0065_use_persian_installation_terms"),
    ]

    operations = [
        migrations.RunPython(
            use_persian_trim_terms,
            reverse_code=migrations.RunPython.noop,
        )
    ]
