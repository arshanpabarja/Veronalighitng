from django.db import migrations
from django.db.models import Q


PILOT_HOVER_IMAGES = {
    4: "products/hover_product_4_technical.png",
    5: "products/hover_product_5_technical.png",
    6: "products/hover_product_6_technical.png",
    12: "products/hover_product_12_technical.png",
    32: "products/hover_product_32_technical.png",
}


def assign_pilot_hover_images(apps, schema_editor):
    Product = apps.get_model("Products", "Product")

    for product_id, image_name in PILOT_HOVER_IMAGES.items():
        Product.objects.filter(pk=product_id).filter(
            Q(hover_image="") | Q(hover_image__isnull=True)
        ).update(hover_image=image_name)


def remove_pilot_hover_images(apps, schema_editor):
    Product = apps.get_model("Products", "Product")

    for product_id, image_name in PILOT_HOVER_IMAGES.items():
        Product.objects.filter(
            pk=product_id,
            hover_image=image_name,
        ).update(hover_image="")


class Migration(migrations.Migration):

    dependencies = [
        ("Products", "0045_product_hover_image"),
    ]

    operations = [
        migrations.RunPython(
            assign_pilot_hover_images,
            remove_pilot_hover_images,
        ),
    ]
