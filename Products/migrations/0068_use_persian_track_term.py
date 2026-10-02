from django.db import migrations


def use_persian_track_term(apps, schema_editor):
    for model_name in ("Family", "Product"):
        model = apps.get_model("Products", model_name)
        for item in model.objects.filter(name_fa__contains="ترک").iterator():
            translated_name = item.name_fa.replace("ترک", "ریل")
            while "ریل ریل" in translated_name:
                translated_name = translated_name.replace("ریل ریل", "ریل")
            item.name_fa = translated_name
            item.save(update_fields=["name_fa"])


class Migration(migrations.Migration):
    dependencies = [
        ("Products", "0067_use_persian_linear_term"),
    ]

    operations = [
        migrations.RunPython(
            use_persian_track_term,
            reverse_code=migrations.RunPython.noop,
        )
    ]
