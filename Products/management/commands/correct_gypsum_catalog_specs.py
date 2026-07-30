from decimal import Decimal

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from Products.models import Dimension, Finish, Product, ProductVariant


CATALOG_PRODUCTS = {
    "Vega Gypsum Downlight": [
        {
            "code": "FAGF01002",
            "name": "Vega",
            "max_wattage": "35.00",
            "width": "110.00",
            "height": "110.00",
            "depth": "40.00",
            "weight": "0.16",
            "overall": "Ø110 × 40 mm",
            "cutout": "Ø120 mm",
        }
    ],
    "Virgo Gypsum Downlight": [
        {
            "code": "FAGF01003",
            "name": "Virgo",
            "max_wattage": "35.00",
            "width": "120.00",
            "height": "120.00",
            "depth": "50.00",
            "weight": "0.33",
            "overall": "120 × 120 × 50 mm",
            "cutout": "125 × 125 mm",
        }
    ],
    "Virgo C Gypsum Downlight": [
        {
            "code": "FAGF01004",
            "name": "Virgo C",
            "max_wattage": "35.00",
            "width": "130.00",
            "height": "130.00",
            "depth": "50.00",
            "weight": "0.35",
            "overall": "Ø130 × 50 mm",
            "cutout": "Ø140 mm",
        }
    ],
    "Pictor Decorative Downlight": [
        {
            "code": "FAGF01005",
            "name": "Pictor",
            "max_wattage": "35.00",
            "width": "120.00",
            "height": "120.00",
            "depth": "50.00",
            "weight": "0.36",
            "overall": "120 × 120 × 50 mm",
            "cutout": "125 × 125 mm",
        }
    ],
    "Pyxis Decorative Downlight": [
        {
            "code": "FAGF01006",
            "name": "Pyxis Single (1X)",
            "max_wattage": "35.00",
            "width": "80.00",
            "height": "80.00",
            "depth": "50.00",
            "weight": "0.30",
            "overall": "80 × 80 × 50 mm",
            "cutout": "90 × 90 mm",
        },
        {
            "code": "FAGF01007",
            "name": "Pyxis Double (2X)",
            "max_wattage": "70.00",
            "width": "150.00",
            "height": "80.00",
            "depth": "46.00",
            "weight": "0.50",
            "overall": "150 × 80 × 46 mm",
            "cutout": "155 × 85 mm",
        },
    ],
    "Pollux Gypsum Downlight": [
        {
            "code": "FAGF01008",
            "name": "Pollux Single (1X)",
            "max_wattage": "35.00",
            "width": "80.00",
            "height": "80.00",
            "depth": "50.00",
            "weight": "0.25",
            "overall": "80 × 80 × 50 mm",
            "cutout": "90 × 90 mm",
        }
    ],
    "Pollux Double Downlight": [
        {
            "code": "FAGF01009",
            "name": "Pollux Double (2X)",
            "max_wattage": "70.00",
            "width": "147.00",
            "height": "77.00",
            "depth": "47.00",
            "weight": "0.53",
            "overall": "147 × 77 × 47 mm",
            "cutout": "150 × 80 mm",
        }
    ],
    "Fornax Gypsum Downlight": [
        {
            "code": "FAGF01011",
            "name": "Fornax",
            "max_wattage": "35.00",
            "width": "160.00",
            "height": "160.00",
            "depth": "45.00",
            "weight": "0.70",
            "overall": "160 × 160 × 45 mm",
            "cutout": "170 × 170 mm",
        }
    ],
    "Castor Downlight": [
        {
            "code": "FAGF01012",
            "name": "Castor (2X)",
            "max_wattage": "70.00",
            "width": "198.00",
            "height": "118.00",
            "depth": "50.00",
            "weight": "0.65",
            "overall": "198 × 118 × 50 mm",
            "cutout": "205 × 125 mm",
        }
    ],
    "Folcano Decorative Downlight": [
        {
            "code": "FAGF01014",
            "name": "Folcano",
            "max_wattage": "35.00",
            "width": "230.00",
            "height": "230.00",
            "depth": "150.00",
            "weight": "0.85",
            "overall": "Ø230 × 150 mm",
            "cutout": "Ø240 mm",
        }
    ],
    "Vela Decorative Downlight": [
        {
            "code": "FAGF01015",
            "name": "Vela",
            "max_wattage": "35.00",
            "width": "140.00",
            "height": "160.00",
            "depth": "70.00",
            "weight": "0.68",
            "overall": "140 × 160 × 70 mm",
            "cutout": "130 × 150 mm",
        }
    ],
    "Blink Decorative Downlight": [
        {
            "code": "FAGF01016",
            "name": "Blink Single (1X)",
            "max_wattage": "35.00",
            "width": "100.00",
            "height": "100.00",
            "depth": "22.00",
            "weight": "0.20",
            "overall": "100 × 100 × 22 mm",
            "cutout": "110 × 110 mm",
        },
        {
            "code": "FAGF01017",
            "name": "Blink Double (2X)",
            "max_wattage": "70.00",
            "width": "170.00",
            "height": "100.00",
            "depth": "22.00",
            "weight": "0.32",
            "overall": "170 × 100 × 22 mm",
            "cutout": "180 × 110 mm",
        },
    ],
    "Virgo Double Downlight": [
        {
            "code": "FAGF01022",
            "name": "Virgo Double (2X)",
            "max_wattage": "70.00",
            "width": "230.00",
            "height": "120.00",
            "depth": "50.00",
            "weight": "0.65",
            "overall": "230 × 120 × 50 mm",
            "cutout": "235 × 125 mm",
        }
    ],
    "Wave Decorative Downlight": [
        {
            "code": "FAGF01023",
            "name": "Wave",
            "max_wattage": "35.00",
            "width": "160.00",
            "height": "160.00",
            "depth": "45.00",
            "weight": "0.70",
            "overall": "160 × 160 × 45 mm",
            "cutout": "170 × 170 mm",
        }
    ],
}


def _decimal(value):
    return Decimal(value) if value is not None else None


class Command(BaseCommand):
    help = (
        "Correct gypsum/decorative product specifications from the supplied "
        "Verona Lighting catalog. Runs as a dry-run unless --apply is supplied."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--apply",
            action="store_true",
            help="Commit the catalog corrections to the configured database.",
        )

    def handle(self, *args, **options):
        apply_changes = options["apply"]
        missing = [
            name
            for name in CATALOG_PRODUCTS
            if not Product.objects.filter(name_en=name).exists()
        ]
        if missing:
            raise CommandError(
                "Catalog products not found by exact English name: "
                + ", ".join(missing)
            )

        mode = "APPLY" if apply_changes else "DRY RUN"
        self.stdout.write(f"{mode}: {len(CATALOG_PRODUCTS)} products")

        with transaction.atomic():
            white_finish = Finish.objects.filter(slug="white").first()

            for product_name, variants in CATALOG_PRODUCTS.items():
                product = Product.objects.select_for_update().get(
                    name_en=product_name
                )
                maximum_wattage = max(
                    _decimal(variant["max_wattage"]) for variant in variants
                )

                product.wattage = maximum_wattage
                product.lumens = None
                product.color_temperature = None
                product.cri = None
                product.beam_angle = None
                product.voltage = "230V"
                product.ip_rating = "IP20"
                product.dimmable = False
                product.lamp_base_type = "GU10"
                product.lifespan = None
                product.mounting_type = "recessed"
                product.save(
                    update_fields=[
                        "wattage",
                        "lumens",
                        "color_temperature",
                        "cri",
                        "beam_angle",
                        "voltage",
                        "ip_rating",
                        "dimmable",
                        "lamp_base_type",
                        "lifespan",
                        "mounting_type",
                        "updated_at",
                    ]
                )
                if white_finish:
                    product.finishes.set([white_finish])

                existing = list(product.variants.order_by("id"))
                retained_ids = []
                for index, spec in enumerate(variants):
                    label = (
                        f'{spec["code"]} | {spec["overall"]} | '
                        f'cut-out {spec["cutout"]}'
                    )
                    dimension, _ = Dimension.objects.get_or_create(
                        label=label,
                        defaults={
                            "width": _decimal(spec["width"]),
                            "height": _decimal(spec["height"]),
                            "depth": _decimal(spec["depth"]),
                            "weight": _decimal(spec["weight"]),
                        },
                    )
                    dimension.width = _decimal(spec["width"])
                    dimension.height = _decimal(spec["height"])
                    dimension.depth = _decimal(spec["depth"])
                    dimension.weight = _decimal(spec["weight"])
                    dimension.save(
                        update_fields=["width", "height", "depth", "weight"]
                    )

                    if index < len(existing):
                        variant = existing[index]
                    else:
                        variant = ProductVariant(product=product)

                    socket_count = 2 if _decimal(spec["max_wattage"]) == 70 else 1
                    variant.model_name = spec["code"]
                    variant.dimension = dimension
                    variant.wattage = _decimal(spec["max_wattage"])
                    variant.lumens = None
                    variant.color_temperature = None
                    variant.sku = spec["code"]
                    variant.is_active = True
                    variant.note = (
                        f'{spec["name"]}; {socket_count} × GU10, max 35 W each; '
                        f'cut-out {spec["cutout"]}; plaster housing; white; '
                        "IK02; lamp replaceable without tools."
                    )
                    variant.save()
                    retained_ids.append(variant.id)

                product.variants.exclude(id__in=retained_ids).delete()
                self.stdout.write(
                    f"  {product.id}: {product_name} -> "
                    f"{maximum_wattage:g} W max, {len(variants)} variant(s)"
                )

            if not apply_changes:
                transaction.set_rollback(True)
                self.stdout.write(
                    self.style.WARNING(
                        "Dry-run complete; PostgreSQL was not changed."
                    )
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(
                        "Catalog specifications committed to PostgreSQL."
                    )
                )
