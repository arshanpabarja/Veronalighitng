from django.db import migrations
from django.db.models import Q


HOVER_IMAGES = {
    27: "products/hover_product_27_technical.png",
    29: "products/hover_product_29_technical.png",
    34: "products/hover_product_34_technical.png",
    39: "products/hover_product_39_technical.png",
    40: "products/hover_product_40_technical.png",
    42: "products/hover_product_42_technical.png",
    43: "products/hover_product_43_technical.png",
    46: "products/hover_product_46_technical.png",
    48: "products/hover_product_48_technical.png",
    49: "products/hover_product_49_technical.png",
    51: "products/hover_product_51_technical.png",
    52: "products/hover_product_52_technical.png",
    55: "products/hover_product_55_technical.png",
    56: "products/hover_product_56_technical.png",
    57: "products/hover_product_57_technical.png",
    59: "products/hover_product_59_technical.png",
    61: "products/hover_product_61_technical.png",
    72: "products/hover_product_72_technical.png",
    78: "products/hover_product_78_technical.png",
    81: "products/hover_product_81_technical.png",
    83: "products/hover_product_83_technical.png",
}


def assign_catalog_hover_images(apps, schema_editor):
    Product = apps.get_model("Products", "Product")
    for product_id, image_name in HOVER_IMAGES.items():
        Product.objects.filter(pk=product_id).filter(
            Q(hover_image="") | Q(hover_image__isnull=True)
        ).update(hover_image=image_name)


def remove_catalog_hover_images(apps, schema_editor):
    Product = apps.get_model("Products", "Product")
    for product_id, image_name in HOVER_IMAGES.items():
        Product.objects.filter(
            pk=product_id,
            hover_image=image_name,
        ).update(hover_image="")


class Migration(migrations.Migration):

    dependencies = [
        ("Products", "0048_assign_emergency_sign_hover_image"),
    ]

    operations = [
        migrations.RunPython(
            assign_catalog_hover_images,
            remove_catalog_hover_images,
        ),
    ]
