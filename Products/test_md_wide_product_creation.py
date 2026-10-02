from decimal import Decimal
from importlib import import_module

from django.apps import apps
from django.test import TestCase

from Products.models import (
    Category,
    Dimension,
    Family,
    Finish,
    Installment,
    Product,
    ProductVariant,
)


migration = import_module(
    "Products.migrations.0060_create_md_wide_products"
)


class MdWideProductCreationTests(TestCase):
    def setUp(self):
        self.finish = Finish.objects.create(
            name="Black",
            color="#000000",
            slug="black-test",
        )
        self.sources = []

        for index, (source_slug, _, mounting_type) in enumerate(
            migration.SOURCE_TARGETS,
            start=1,
        ):
            category = Category.objects.create(
                name=f"Category {index}",
                slug=f"category-{index}",
            )
            family = Family.objects.create(
                name=f"MD LINEO {index}",
                slug=f"md-lineo-{index}",
                category=category,
            )
            source = Product.objects.create(
                order=4,
                name="چراغ خطی MD مید",
                name_fa="چراغ خطی MD مید",
                name_en="MD MID",
                slug=source_slug,
                category=category,
                family=family,
                subtitle_fa="چراغ MD مید با توان ۲۵ وات",
                subtitle_en="MD MID 25 W/m linear light",
                description_fa="محصول ام‌دی مید با توان ۲۵ وات",
                description_en="MD MID operating at 25W/m",
                full_description_fa="چراغ ام‌دی مید با توان ۲۵ وات بر متر",
                full_description_en="MD MID total power is 25 w/m",
                wattage=Decimal("25.00"),
                lumens=2500,
                color_temperature=4000,
                cri=80,
                voltage="220-240 VAC",
                ip_rating="IP44",
                lifespan=50000,
                mounting_type=mounting_type,
                image1=f"products/md-mid-{index}.png",
                image2="products/application.jpg",
                hover_image=f"products/md-mid-hover-{index}.png",
                meta_description_fa="MD مید، ۲۵ وات و ۲۵۰۰ لومن",
                meta_description_en="MD MID, 25W/m and 2500 lm/m",
            )
            source.finishes.add(self.finish)
            Installment.objects.create(
                product=source,
                name="Mounting",
                step="1",
                description="Pendant and surface mount.",
            )
            dimension = Dimension.objects.create(
                label="100 × 5 × 8.5 cm",
                width=Decimal("1000.00"),
                height=Decimal("50.00"),
                depth=Decimal("85.00"),
            )
            ProductVariant.objects.create(
                product=source,
                model_name="Mirdamad Mid",
                dimension=dimension,
                wattage=Decimal("25.00"),
                lumens=2500,
                color_temperature=4000,
                sku=f"SOURCE-{index}",
                note="Colors are customizable.",
            )
            self.sources.append(source)

    def test_clones_both_md_mid_products_with_wide_dimensions_and_image(self):
        migration.create_md_wide_products(apps, None)

        for source, (_, target_slug, mounting_type) in zip(
            self.sources,
            migration.SOURCE_TARGETS,
        ):
            target = Product.objects.get(slug=target_slug)
            self.assertEqual(target.name_fa, "چراغ خطی MD واید")
            self.assertEqual(target.name_en, "MD WIDE")
            self.assertEqual(target.category_id, source.category_id)
            self.assertEqual(target.family_id, source.family_id)
            self.assertEqual(target.order, 5)
            self.assertEqual(target.wattage, Decimal("30.00"))
            self.assertEqual(target.lumens, source.lumens)
            self.assertEqual(target.mounting_type, mounting_type)
            self.assertEqual(str(target.image1), migration.MD_WIDE_IMAGE)
            self.assertFalse(target.hover_image)
            self.assertIn("30W", target.description_en)
            self.assertNotIn("25W", target.description_en)
            self.assertEqual(
                list(target.finishes.values_list("slug", flat=True)),
                ["black-test"],
            )
            self.assertEqual(target.installment.count(), 1)

            variant = target.variants.get()
            self.assertEqual(variant.model_name, "Mirdamad Wide")
            self.assertEqual(variant.wattage, Decimal("30.00"))
            self.assertEqual(variant.lumens, 2500)
            self.assertEqual(variant.note, "Colors are customizable.")
            self.assertEqual(variant.dimension.width, Decimal("1000.00"))
            self.assertEqual(variant.dimension.height, Decimal("70.00"))
            self.assertEqual(variant.dimension.depth, Decimal("85.00"))
            self.assertIn("100 × 7 × 8.5 cm", variant.dimension.label)

        self.assertEqual(
            Product.objects.filter(slug__startswith="md-wide-").count(),
            2,
        )
