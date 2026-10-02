from decimal import Decimal

from django.db import migrations


CATEGORY_SLUG = "spotlights-underwater"

FAMILIES = (
    {
        "slug": "lei",
        "name_en": "LEI",
        "name_fa": "لی",
        "subtitle_en": "LEI waterproof lighting family",
        "subtitle_fa": "خانواده چراغ‌های ضد آب لی",
        "number": 1,
        "icon": "products/waterproof/lei-mid-fl-tl.png",
    },
    {
        "slug": "lina",
        "name_en": "LINA",
        "name_fa": "لینا",
        "subtitle_en": "LINA waterproof lighting family",
        "subtitle_fa": "خانواده چراغ‌های ضد آب لینا",
        "number": 2,
        "icon": "products/waterproof/lina-onefold.png",
    },
)

PRODUCTS = (
    {
        "slug": "lei-mid-fl-tl",
        "family_slug": "lei",
        "order": 1,
        "name_en": "Lei MID FL-TL",
        "name_fa": "لی مید اف‌ال-تی‌ال",
        "wattage": "9.00",
        "mounting_type": "surface",
        "dimension_label": "Ø10 × 5 cm; cut-out Ø10.5 cm",
        "diameter_mm": "100.00",
        "height_mm": "50.00",
        "image": "products/waterproof/lei-mid-fl-tl.png",
        "description_en": (
            "Color temperature and body color are customizable according "
            "to customer requirements."
        ),
        "description_fa": (
            "دمای رنگ و رنگ بدنه مطابق درخواست مشتری قابل "
            "سفارشی‌سازی است."
        ),
    },
    {
        "slug": "lei-mid-up-t",
        "family_slug": "lei",
        "order": 2,
        "name_en": "Lei MID Up-T",
        "name_fa": "لی مید آپ-تی",
        "wattage": "9.00",
        "mounting_type": "recessed",
        "dimension_label": "Ø12 × 5 cm; cut-out Ø10.5 cm",
        "diameter_mm": "120.00",
        "height_mm": "50.00",
        "image": "products/waterproof/lei-mid-up-t.png",
        "description_en": (
            "Color temperature and body color are customizable according "
            "to customer requirements."
        ),
        "description_fa": (
            "دمای رنگ و رنگ بدنه مطابق درخواست مشتری قابل "
            "سفارشی‌سازی است."
        ),
    },
    {
        "slug": "lei-mini-fl-tl",
        "family_slug": "lei",
        "order": 3,
        "name_en": "Lei Mini FL-TL",
        "name_fa": "لی مینی اف‌ال-تی‌ال",
        "wattage": "3.50",
        "mounting_type": "surface",
        "dimension_label": "Ø3 × 7.5 cm",
        "diameter_mm": "30.00",
        "height_mm": "75.00",
        "image": "products/waterproof/lei-mini-fl-tl.png",
        "description_en": (
            "Color temperature and body color are customizable according "
            "to customer requirements."
        ),
        "description_fa": (
            "دمای رنگ و رنگ بدنه مطابق درخواست مشتری قابل "
            "سفارشی‌سازی است."
        ),
    },
    {
        "slug": "lei-mini-win",
        "family_slug": "lei",
        "order": 4,
        "name_en": "Lei Mini Win",
        "name_fa": "لی مینی وین",
        "wattage": "3.50",
        "mounting_type": "recessed",
        "dimension_label": "Ø3 × 9 cm; cut-out Ø3.5 cm",
        "diameter_mm": "30.00",
        "height_mm": "90.00",
        "image": "products/waterproof/lei-mini-win.png",
        "description_en": (
            "Color temperature and body color are customizable according "
            "to customer requirements."
        ),
        "description_fa": (
            "دمای رنگ و رنگ بدنه مطابق درخواست مشتری قابل "
            "سفارشی‌سازی است."
        ),
    },
    {
        "slug": "lina-onefold",
        "family_slug": "lina",
        "order": 1,
        "name_en": "Lina onefold",
        "name_fa": "لینا وان‌فولد",
        "wattage": "30.00",
        "mounting_type": "surface",
        "dimension_label": "Ø20 × 5 cm",
        "diameter_mm": "200.00",
        "height_mm": "50.00",
        "image": "products/waterproof/lina-onefold.png",
        "description_en": (
            "R-G-B, RGB and RGBW options with DMX self-control; also "
            "available with a single color temperature."
        ),
        "description_fa": (
            "قابل ارائه در حالت‌های R-G-B، RGB و RGBW با کنترل "
            "داخلی DMX؛ امکان تولید با دمای رنگ تک‌رنگ نیز وجود دارد."
        ),
    },
    {
        "slug": "lina-offiance",
        "family_slug": "lina",
        "order": 2,
        "name_en": "Lina offiance",
        "name_fa": "لینا آفیانس",
        "wattage": "30.00",
        "mounting_type": "recessed",
        "dimension_label": "Ø20 × 5 cm",
        "diameter_mm": "200.00",
        "height_mm": "50.00",
        "image": "products/waterproof/lina-offiance.png",
        "description_en": (
            "R-G-B, RGB and RGBW options with DMX self-control; also "
            "available with a single color temperature."
        ),
        "description_fa": (
            "قابل ارائه در حالت‌های R-G-B، RGB و RGBW با کنترل "
            "داخلی DMX؛ امکان تولید با دمای رنگ تک‌رنگ نیز وجود دارد."
        ),
    },
)


def add_waterproof_products(apps, schema_editor):
    Application = apps.get_model("Products", "Application")
    Category = apps.get_model("Products", "Category")
    Dimension = apps.get_model("Products", "Dimension")
    Family = apps.get_model("Products", "Family")
    Product = apps.get_model("Products", "Product")
    ProductVariant = apps.get_model("Products", "ProductVariant")

    category = Category.objects.filter(slug=CATEGORY_SLUG).first()
    if not category:
        return

    landscape = Application.objects.filter(slug="landescape").first()
    families = {}
    for row in FAMILIES:
        family, _ = Family.objects.update_or_create(
            slug=row["slug"],
            defaults={
                "name": row["name_fa"],
                "name_fa": row["name_fa"],
                "name_en": row["name_en"],
                "subtitle_fa": row["subtitle_fa"],
                "subtitle_en": row["subtitle_en"],
                "category": category,
                "number": row["number"],
                "icon": row["icon"],
                "icon_alt_fa": f'خانواده چراغ ضد آب {row["name_fa"]}',
                "icon_alt_en": f'{row["name_en"]} waterproof lighting family',
                "is_active": True,
                "meta_title_fa": (
                    f'چراغ‌های ضد آب {row["name_fa"]} | ورونا لایتینگ'
                ),
                "meta_title_en": (
                    f'{row["name_en"]} Waterproof Lights | Verona Lighting'
                ),
                "meta_description_fa": row["subtitle_fa"],
                "meta_description_en": row["subtitle_en"],
            },
        )
        if landscape:
            family.applications.add(landscape)
        families[row["slug"]] = family

    for row in PRODUCTS:
        wattage = Decimal(row["wattage"])
        product, _ = Product.objects.update_or_create(
            slug=row["slug"],
            defaults={
                "order": row["order"],
                "name": row["name_fa"],
                "name_fa": row["name_fa"],
                "name_en": row["name_en"],
                "category": category,
                "family": families[row["family_slug"]],
                "is_active": True,
                "subtitle_fa": row["description_fa"],
                "subtitle_en": row["description_en"],
                "description_fa": row["description_fa"],
                "description_en": row["description_en"],
                "full_description_fa": (
                    f'{row["name_fa"]}: {row["dimension_label"]}، '
                    f'{row["wattage"]} وات. {row["description_fa"]}'
                ),
                "full_description_en": (
                    f'{row["name_en"]}: {row["dimension_label"]}, '
                    f'{row["wattage"]} W. {row["description_en"]}'
                ),
                "wattage": wattage,
                "mounting_type": row["mounting_type"],
                "image1": row["image"],
                "image1_alt_fa": f'چراغ ضد آب {row["name_fa"]}',
                "image1_alt_en": f'{row["name_en"]} waterproof light',
                "meta_title_fa": (
                    f'چراغ ضد آب {row["name_fa"]} | ورونا لایتینگ'
                ),
                "meta_title_en": (
                    f'{row["name_en"]} Waterproof Light | Verona Lighting'
                ),
                "meta_description_fa": (
                    f'{row["name_fa"]}، {row["wattage"]} وات، '
                    f'{row["dimension_label"]}. {row["description_fa"]}'
                ),
                "meta_description_en": (
                    f'{row["name_en"]}, {row["wattage"]} W, '
                    f'{row["dimension_label"]}. {row["description_en"]}'
                ),
            },
        )

        product.variants.all().delete()
        dimension = Dimension.objects.create(
            label=row["dimension_label"],
            width=Decimal(row["diameter_mm"]),
            height=Decimal(row["height_mm"]),
        )
        ProductVariant.objects.create(
            product=product,
            model_name=row["name_en"],
            dimension=dimension,
            wattage=wattage,
            sku=f'VERONA-{row["slug"].upper()}',
            is_active=True,
        )


class Migration(migrations.Migration):
    dependencies = [("Products", "0062_retranslate_catalog_names_fa")]
    operations = [
        migrations.RunPython(
            add_waterproof_products,
            reverse_code=migrations.RunPython.noop,
        )
    ]
