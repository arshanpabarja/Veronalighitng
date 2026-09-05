from django.db import migrations


# The database distinguishes 1PH and 3PH products.  The older catalogue groups
# their matching bodies under GLOBAL TRACK and TRACK SPOT/PENDANT names.
PRODUCT_PAGE_BY_SLUG = {
    "3ph-track-recessed": 178,
    "1ph-track-surface-pendant": 180,
    "3ph-track-surface": 180,
    "1ph-spot": 182,
    "1ph-track-spot-65-p": 184,
    "3ph-spotlight-and-pendant-light": 184,
    "1ph-track-pendant-65": 188,
}


def asset_name(page_number):
    return f"products/catalog_applications/catalog_application_page_{page_number:03d}.jpg"


def assign_application_images(apps, schema_editor):
    Product = apps.get_model("Products", "Product")
    for slug, page_number in PRODUCT_PAGE_BY_SLUG.items():
        for product in Product.objects.filter(slug=slug):
            product.image2 = asset_name(page_number)
            product.image2_alt_en = f"{product.name_en or product.name} in an illuminated interior"
            product.image2_alt_fa = f"نمونه اجرای {product.name_fa or product.name} در فضای داخلی"
            product.save(update_fields=("image2", "image2_alt_en", "image2_alt_fa"))


def restore_application_images(apps, schema_editor):
    Product = apps.get_model("Products", "Product")
    for slug, page_number in PRODUCT_PAGE_BY_SLUG.items():
        Product.objects.filter(
            slug=slug,
            image2=asset_name(page_number),
        ).update(image2="", image2_alt_en="", image2_alt_fa="")


class Migration(migrations.Migration):

    dependencies = [
        ("Products", "0052_assign_catalog_application_images"),
    ]

    operations = [
        migrations.RunPython(assign_application_images, restore_application_images),
    ]
