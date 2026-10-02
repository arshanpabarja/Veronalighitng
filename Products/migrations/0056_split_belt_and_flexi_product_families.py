from django.db import migrations


CATEGORY_FAMILY_PAIRS = (
    ("mmagne-tbelt", "magneto-belt"),
    ("magnet-flexi", "magneto-flexi"),
)


def product_family_slug(product_slug):
    return f"{product_slug.lower()}-family"


def split_belt_and_flexi_families(apps, schema_editor):
    Category = apps.get_model("Products", "Category")
    Family = apps.get_model("Products", "Family")
    Product = apps.get_model("Products", "Product")

    for category_slug, aggregate_family_slug in CATEGORY_FAMILY_PAIRS:
        category = Category.objects.filter(slug=category_slug).first()
        if not category:
            continue

        aggregate_family = Family.objects.filter(
            category=category,
            slug=aggregate_family_slug,
        ).first()
        if not aggregate_family:
            continue

        application_ids = list(
            aggregate_family.applications.values_list("id", flat=True)
        )
        products = list(
            Product.objects.filter(
                category=category,
                family=aggregate_family,
            ).order_by("order", "id")
        )

        for position, product in enumerate(products, start=1):
            family, _ = Family.objects.update_or_create(
                slug=product_family_slug(product.slug),
                defaults={
                    "name": product.name_fa or product.name,
                    "name_fa": product.name_fa or product.name,
                    "name_en": product.name_en or product.name,
                    "icon": product.image1,
                    "icon_alt_fa": (
                        product.image1_alt_fa
                        or product.name_fa
                        or product.name
                    ),
                    "icon_alt_en": (
                        product.image1_alt_en
                        or product.name_en
                        or product.name
                    ),
                    "number": position,
                    "category": category,
                    "is_active": product.is_active,
                    "subtitle_fa": product.subtitle_fa,
                    "subtitle_en": product.subtitle_en,
                    "meta_title_fa": product.meta_title_fa,
                    "meta_title_en": product.meta_title_en,
                    "meta_description_fa": product.meta_description_fa,
                    "meta_description_en": product.meta_description_en,
                },
            )
            family.applications.set(application_ids)
            product.family = family
            product.save(update_fields=["family"])

        # Every product is attached to its replacement family before the
        # aggregate family is removed.
        aggregate_family.delete()


class Migration(migrations.Migration):

    dependencies = [
        ("Products", "0055_organize_small_magneto_families"),
    ]

    operations = [
        migrations.RunPython(
            split_belt_and_flexi_families,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
