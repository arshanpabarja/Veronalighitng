from django.db import migrations


# Frozen copy of the reviewed English-name/slug matching against Binder1_707930.
# The source catalogue says MAGNETAR; the live product names say MAGNETO.
PRODUCT_PAGE_BY_SLUG = {
    "magnetar-large-ressed-track-trimless": 14,
    "magnetar-large-surface-pendant-track": 16,
    "magnetar-large-linear": 18,
    "magnetar-large-dot-linear": 20,
    "magnetar-rotate-linear": 22,
    "magnetar-rotate-dot-linear": 24,
    "magnetar-large-angle-linear": 26,
    "magnetar-large-angle-dot-linear": 28,
    "magnetar-large-pendant-35": 30,
    "magnetar-large-pendant-65": 32,
    "magnetar-large-spot-35": 34,
    "magnetar-large-spot-65": 36,
    "magnetar-large-tube-plaxi": 38,
    "magnetar-large-spot-linear": 40,
    "magnetar-large-spot-dot-panel": 42,
    "magnetar-large-spot-panel": 44,
    "magnetar-large-flexible-linear": 46,
    "magnetar-small-ressed-track-trimles": 48,
    "magnetar-small-surface-pendant-track": 50,
    "magnetar-smll-ressed-track-trim": 52,
    "magnetar-smll-surface-pendant-track": 54,
    "magnetar-small-linear": 56,
    "magnetar-small-dot-linear": 58,
    "magnetar-small-rotate-linear": 60,
    "magnetar-small-spot-35-1": 62,
    "magnetar-small-spot-55": 64,
    "magnetar-smallrotate-dot-linear": 66,
    "magnetar-small-angle-linear": 68,
    "magnetar-small-angle-dot-linear": 70,
    "magnetar-small-pendant-35": 72,
    "magnetar-small-pendant-65": 74,
    "magnetar-small-flexible-linear": 76,
    "sp-mini": 80,
    "sp-narrow": 82,
    "sp-mid-slim": 84,
    "sp-wid": 86,
    "sp-wid-ip": 88,
    "sp-plus": 90,
    "sp-narrow-dot": 92,
    "mirdamad-mini-pendant": 100,
    "md-mini-surface": 100,
    "md-narrow-surface": 102,
    "md-narrow-pendant": 102,
    "md-narrow-dot-pendant": 102,
    "md-narrow-dot-surface": 102,
    "md-mid-surface": 104,
    "md-mid-pendant": 104,
    "mad-old": 108,
    "mad-old-pendant": 108,
    "bd-mini": 112,
    "bd-narrow": 114,
    "peransa": 138,
    "ring-line-downlight": 140,
    "ring-line-inside": 142,
    "ring-line-inside-90cm": 142,
    "bahar-single": 156,
    "bahar-dual": 158,
    "bahar-triple": 160,
    "payam-6": 162,
    "payam-8": 164,
    "payam-square": 166,
    "payam-led": 168,
    "trimless-4": 170,
    "trimless-8": 172,
    "taban-single": 174,
    "taban-double": 176,
    "hely-short-diamond": 192,
    "hely-small": 194,
    "hely-mid": 196,
    "hely-angle": 198,
    "arin": 200,
    "liber-large": 202,
    "liber-small": 204,
    "bambo-wall": 232,
    "triton": 242,
    "karen-highbay": 244,
    "moon": 258,
    "roshana": 284,
}


# These two products had duplicate product renders in image2 before this import.
PREVIOUS_IMAGE2_BY_SLUG = {
    "magnetar-large-linear": "products/magnetar_linear_4cm_Vfhi1xL.png",
    "magnetar-large-dot-linear": "products/magnetar_dot_linear_4cm_CGNrcBJ.png",
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

    # One legacy English label remained after the MAGNETAR -> MAGNETO rename.
    Product.objects.filter(slug="magnetar-small-sign-emergency").update(
        name_en="MAGNETO SMALL SIGN EMERGENCY"
    )


def restore_application_images(apps, schema_editor):
    Product = apps.get_model("Products", "Product")
    for slug, page_number in PRODUCT_PAGE_BY_SLUG.items():
        Product.objects.filter(
            slug=slug,
            image2=asset_name(page_number),
        ).update(
            image2=PREVIOUS_IMAGE2_BY_SLUG.get(slug, ""),
            image2_alt_en="",
            image2_alt_fa="",
        )

    Product.objects.filter(
        slug="magnetar-small-sign-emergency",
        name_en="MAGNETO SMALL SIGN EMERGENCY",
    ).update(name_en="MAGNETAR SMALL SIGN EMERGENCY")


class Migration(migrations.Migration):

    dependencies = [
        ("Products", "0051_apply_magnetar_review_rows"),
    ]

    operations = [
        migrations.RunPython(assign_application_images, restore_application_images),
    ]
