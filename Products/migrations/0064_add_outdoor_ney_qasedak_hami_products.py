from decimal import Decimal

from django.db import migrations


CATEGORY_SLUG = "outdoor"

FAMILIES = (
    ("ney", "NEY", "نی", 1, "products/outdoor/ney-signage.png"),
    ("qasedak", "QASEDAK", "قاصدک", 2, "products/outdoor/qasedak.png"),
    ("hami", "HAMI", "حامی", 3, "products/outdoor/hami-stand.png"),
)

PRODUCTS = (
    {
        "slug": "ney-signage", "family": "ney", "order": 1,
        "name_en": "Signage", "name_fa": "ساینیج", "wattage": "40.00", "lumens": 400,
        "dimension": "950 × (3000/4000) mm", "width": "950.00", "height": "3000.00", "depth": "4000.00",
        "image": "products/outdoor/ney-signage.png",
        "description_en": "Luminous flux: 400 lm. Luminaire efficacy: 100 lm/W. Color temperature: 3000–6000 K.",
        "description_fa": "شار نوری: 400 لومن. بازده نوری: 100 لومن بر وات. دمای رنگ: 3000–6000 کلوین.",
    },
    {
        "slug": "ney-fadak", "family": "ney", "order": 2,
        "name_en": "Fadak", "name_fa": "فدک", "wattage": "50.00", "lumens": 4500,
        "dimension": "950 × 3600 mm", "width": "950.00", "height": "3600.00", "depth": None,
        "image": "products/outdoor/ney-fadak.png",
        "description_en": "Luminous flux: 4500 lm. Luminaire efficacy: 90 lm/W. Color temperature: 3000–6000 K.",
        "description_fa": "شار نوری: 4500 لومن. بازده نوری: 90 لومن بر وات. دمای رنگ: 3000–6000 کلوین.",
    },
    {
        "slug": "ney", "family": "ney", "order": 3,
        "name_en": "NEY", "name_fa": "نی", "wattage": None, "lumens": None,
        "dimension": "Ø2.5 × 80/120/160 cm", "width": "25.00", "height": "800.00", "depth": None,
        "image": "products/outdoor/ney.png",
        "description_en": "Available in 80 cm (16 W), 120 cm (24 W), and 160 cm (30 W) heights. Color temperature and body color are customizable according to customer requirements.",
        "description_fa": "قابل ارائه در ارتفاع‌های 80 سانتی‌متر (16 وات)، 120 سانتی‌متر (24 وات) و 160 سانتی‌متر (30 وات). دمای رنگ و رنگ بدنه مطابق درخواست مشتری قابل سفارشی‌سازی است.",
        "variants": (("NEY 80", "Ø2.5 × 80 cm", "25.00", "800.00", "16.00"), ("NEY 120", "Ø2.5 × 120 cm", "25.00", "1200.00", "24.00"), ("NEY 160", "Ø2.5 × 160 cm", "25.00", "1600.00", "30.00")),
    },
    {
        "slug": "qasedak", "family": "qasedak", "order": 1,
        "name_en": "QASEDAK", "name_fa": "قاصدک", "wattage": "5.00", "lumens": None,
        "dimension": "Ø16 × 73 cm", "width": "160.00", "height": "730.00", "depth": None,
        "image": "products/outdoor/qasedak.png",
        "description_en": "Decorative outdoor lighting with 5 W total power.",
        "description_fa": "چراغ دکوراتیو فضای باز با توان کل 5 وات.",
    },
    {
        "slug": "hami-stand", "family": "hami", "order": 1,
        "name_en": "Hami Stand", "name_fa": "حامی استند", "wattage": "6.00", "lumens": None,
        "dimension": "800 × 800 × 1200 mm", "width": "800.00", "height": "800.00", "depth": "1200.00",
        "image": "products/outdoor/hami-stand.png",
        "description_en": "GU10 outdoor luminaire. Color temperature and body color are customizable according to customer requirements.",
        "description_fa": "چراغ فضای باز با سرپیچ GU10. دمای رنگ و رنگ بدنه مطابق درخواست مشتری قابل سفارشی‌سازی است.",
    },
    {
        "slug": "hami-wall-1", "family": "hami", "order": 2,
        "name_en": "Hami Wall 1", "name_fa": "حامی وال 1", "wattage": "6.00", "lumens": None,
        "dimension": "80 × 80 × 150 mm", "width": "80.00", "height": "80.00", "depth": "150.00",
        "image": "products/outdoor/hami-wall-1.png",
        "description_en": "GU10 outdoor wall luminaire. Color temperature and body color are customizable according to customer requirements.",
        "description_fa": "چراغ دیواری فضای باز با سرپیچ GU10. دمای رنگ و رنگ بدنه مطابق درخواست مشتری قابل سفارشی‌سازی است.",
    },
    {
        "slug": "hami-wall-2", "family": "hami", "order": 3,
        "name_en": "Hami Wall 2", "name_fa": "حامی وال 2", "wattage": "6.00", "lumens": None,
        "dimension": "80 × 80 × 600 mm", "width": "80.00", "height": "80.00", "depth": "600.00",
        "image": "products/outdoor/hami-wall-2.png",
        "description_en": "GU10 outdoor wall luminaire. Color temperature and body color are customizable according to customer requirements.",
        "description_fa": "چراغ دیواری فضای باز با سرپیچ GU10. دمای رنگ و رنگ بدنه مطابق درخواست مشتری قابل سفارشی‌سازی است.",
    },
)


def add_outdoor_products(apps, schema_editor):
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
    for slug, name_en, name_fa, number, icon in FAMILIES:
        family, _ = Family.objects.update_or_create(
            slug=slug,
            defaults={
                "name": name_fa, "name_en": name_en, "name_fa": name_fa,
                "subtitle_en": f"{name_en} decorative outdoor lighting family",
                "subtitle_fa": f"خانواده چراغ‌های دکوراتیو فضای باز {name_fa}",
                "category": category, "number": number, "icon": icon,
                "icon_alt_en": f"{name_en} outdoor lighting family",
                "icon_alt_fa": f"خانواده چراغ فضای باز {name_fa}",
                "meta_title_en": f"{name_en} Outdoor Lights | Verona Lighting",
                "meta_title_fa": f"چراغ‌های فضای باز {name_fa} | ورونا لایتینگ",
                "meta_description_en": f"{name_en} decorative outdoor lighting by Verona Lighting.",
                "meta_description_fa": f"چراغ‌های دکوراتیو فضای باز {name_fa} از ورونا لایتینگ.",
                "is_active": True,
            },
        )
        if landscape:
            family.applications.add(landscape)
        families[slug] = family

    for row in PRODUCTS:
        variants = row.get("variants")
        product, _ = Product.objects.update_or_create(
            slug=row["slug"],
            defaults={
                "order": row["order"], "name": row["name_fa"],
                "name_en": row["name_en"], "name_fa": row["name_fa"],
                "category": category, "family": families[row["family"]], "is_active": True,
                "subtitle_en": row["description_en"], "subtitle_fa": row["description_fa"],
                "description_en": row["description_en"], "description_fa": row["description_fa"],
                "full_description_en": f'{row["name_en"]}: {row["dimension"]}. {row["description_en"]}',
                "full_description_fa": f'{row["name_fa"]}: {row["dimension"]}. {row["description_fa"]}',
                "wattage": Decimal(row["wattage"]) if row["wattage"] else None,
                "lumens": row["lumens"],
                "lamp_base_type": "GU10" if row["slug"].startswith("hami-") else "",
                "mounting_type": "wall" if row["slug"].startswith("hami-wall") else "surface",
                "image1": row["image"],
                "image1_alt_en": f'{row["name_en"]} outdoor light',
                "image1_alt_fa": f'چراغ فضای باز {row["name_fa"]}',
                "meta_title_en": f'{row["name_en"]} Outdoor Light | Verona Lighting',
                "meta_title_fa": f'چراغ فضای باز {row["name_fa"]} | ورونا لایتینگ',
                "meta_description_en": f'{row["name_en"]}, {row["dimension"]}. {row["description_en"]}',
                "meta_description_fa": f'{row["name_fa"]}، {row["dimension"]}. {row["description_fa"]}',
            },
        )
        product.variants.all().delete()
        rows = variants or ((row["name_en"], row["dimension"], row["width"], row["height"], row["wattage"]),)
        for index, (model_name, label, width, height, wattage) in enumerate(rows, start=1):
            dimension = Dimension.objects.create(
                label=label, width=Decimal(width), height=Decimal(height), depth=Decimal(row["depth"]) if not variants and row["depth"] else None,
            )
            ProductVariant.objects.create(
                product=product, model_name=model_name, dimension=dimension,
                wattage=Decimal(wattage) if wattage else None,
                sku=f'VERONA-{row["slug"].upper()}-{index}', is_active=True,
            )


class Migration(migrations.Migration):
    dependencies = [("Products", "0063_add_waterproof_lei_lina_products")]
    operations = [migrations.RunPython(add_outdoor_products, migrations.RunPython.noop)]
