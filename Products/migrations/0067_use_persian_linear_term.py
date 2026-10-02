from django.db import migrations


def use_persian_linear_term(apps, schema_editor):
    for model_name in ("Family", "Product"):
        model = apps.get_model("Products", model_name)
        for item in model.objects.filter(name_fa__contains="لاینر").iterator():
            item.name_fa = item.name_fa.replace("لاینر", "خطی")
            item.save(update_fields=["name_fa"])


class Migration(migrations.Migration):
    dependencies = [
        ("Products", "0066_use_persian_trim_terms"),
    ]

    operations = [
        migrations.RunPython(
            use_persian_linear_term,
            reverse_code=migrations.RunPython.noop,
        )
    ]
