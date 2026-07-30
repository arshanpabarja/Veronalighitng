from django.db import migrations
from django.db.models import Q


PRODUCT_IDS = (
    2, 3, 10, 13, 15, 16, 17, 18, 19, 21, 22, 23, 25, 26, 28, 30, 31,
    41, 44, 45, 53, 58, 60, 62, 63, 64, 65, 66, 68, 70, 73, 74, 75, 76,
    77, 79, 80, 82, 175, 182, 183, 184, 185, 186, 187, 188, 190, 191,
    192, 193, 194, 195, 196, 198, 200, 206, 208, 209, 210, 211, 212,
    213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225,
    226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238,
    239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249,
)


def image_name(product_id):
    return f"products/hover_product_{product_id}_technical.png"


def assign_remaining_hover_images(apps, schema_editor):
    Product = apps.get_model("Products", "Product")
    for product_id in PRODUCT_IDS:
        Product.objects.filter(pk=product_id).filter(
            Q(hover_image="") | Q(hover_image__isnull=True)
        ).update(hover_image=image_name(product_id))


def remove_remaining_hover_images(apps, schema_editor):
    Product = apps.get_model("Products", "Product")
    for product_id in PRODUCT_IDS:
        Product.objects.filter(
            pk=product_id,
            hover_image=image_name(product_id),
        ).update(hover_image="")


class Migration(migrations.Migration):

    dependencies = [
        ("Products", "0049_assign_catalog_hover_images"),
    ]

    operations = [
        migrations.RunPython(
            assign_remaining_hover_images,
            remove_remaining_hover_images,
        ),
    ]
