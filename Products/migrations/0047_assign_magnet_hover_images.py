from django.db import migrations
from django.db.models import Q


MAGNET_HOVER_IMAGES = {
    7: "products/hover_product_7_technical.png",
    8: "products/hover_product_8_technical.png",
    9: "products/hover_product_9_technical.png",
    11: "products/hover_product_11_technical.png",
    14: "products/hover_product_14_technical.png",
    20: "products/hover_product_20_technical.png",
    33: "products/hover_product_33_technical.png",
    36: "products/hover_product_36_technical.png",
    37: "products/hover_product_37_technical.png",
    38: "products/hover_product_38_technical.png",
}


def assign_magnet_hover_images(apps, schema_editor):
    Product = apps.get_model("Products", "Product")

    for product_id, image_name in MAGNET_HOVER_IMAGES.items():
        Product.objects.filter(pk=product_id).filter(
            Q(hover_image="") | Q(hover_image__isnull=True)
        ).update(hover_image=image_name)


def remove_magnet_hover_images(apps, schema_editor):
    Product = apps.get_model("Products", "Product")

    for product_id, image_name in MAGNET_HOVER_IMAGES.items():
        Product.objects.filter(
            pk=product_id,
            hover_image=image_name,
        ).update(hover_image="")


class Migration(migrations.Migration):

    dependencies = [
        ("Products", "0046_assign_pilot_hover_images"),
    ]

    operations = [
        migrations.RunPython(
            assign_magnet_hover_images,
            remove_magnet_hover_images,
        ),
    ]
