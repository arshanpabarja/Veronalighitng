from django.db import migrations
from django.db.models import Q


HOVER_IMAGE = "products/hover_product_24_technical.png"


def assign_emergency_sign_hover_image(apps, schema_editor):
    Product = apps.get_model("Products", "Product")
    Product.objects.filter(pk=24).filter(
        Q(hover_image="") | Q(hover_image__isnull=True)
    ).update(hover_image=HOVER_IMAGE)


def remove_emergency_sign_hover_image(apps, schema_editor):
    Product = apps.get_model("Products", "Product")
    Product.objects.filter(
        pk=24,
        hover_image=HOVER_IMAGE,
    ).update(hover_image="")


class Migration(migrations.Migration):

    dependencies = [
        ("Products", "0047_assign_magnet_hover_images"),
    ]

    operations = [
        migrations.RunPython(
            assign_emergency_sign_hover_image,
            remove_emergency_sign_hover_image,
        ),
    ]
