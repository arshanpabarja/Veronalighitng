from pathlib import Path
from uuid import uuid4

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand

from Products.models import (
    Product,
    ProductVariant,
    Dimension,
    Category,
    Family,
    Finish,
)


class Command(BaseCommand):
    help = "Seed Downlight Products"

    def handle(self, *args, **options):

        category = Category.objects.get(name="Magnet Curve")

        black_finish = Finish.objects.get(name="black")
        white_finish = Finish.objects.get(name="White")

        image_path = (
            Path(settings.BASE_DIR)
            / "static"
            / "images"
            / "categories"
            / "retail1.png"
        )

        PRODUCTS = []

        PRODUCTS = [
    {
        "family": "Spy",
        "name": "Spy Recessed Downlight",
        "subtitle": "Compact recessed spotlight for modern interiors",
        "wattage": 12,
        "lumens": 1150,
        "variants": [
            {"watt": 12, "lumens": 1150, "cri": 90, "color_temperature": 4000, "width": 80, "height": 80}
        ]
    },

    {
        "family": "Spy On",
        "name": "Spy On Recessed Downlight",
        "subtitle": "Minimal recessed lighting solution",
        "wattage": 7,
        "lumens": 560,
        "variants": [
            {"watt": 7, "lumens": 560, "cri": 80, "color_temperature": 4000, "width": 80, "height": 80}
        ]
    },

    {
        "family": "Plano",
        "name": "Plano Recessed Downlight",
        "subtitle": "High efficiency ceiling recessed downlight",
        "wattage": 6,
        "lumens": 600,
        "variants": [
            {"watt": 6, "lumens": 600, "cri": 90, "color_temperature": 4000, "width": 65, "height": 65},
            {"watt": 9, "lumens": 900, "cri": 90, "color_temperature": 4000, "width": 80, "height": 80},
            {"watt": 12, "lumens": 1200, "cri": 90, "color_temperature": 4000, "width": 120, "height": 120},
            {"watt": 24, "lumens": 2400, "cri": 90, "color_temperature": 4000, "width": 150, "height": 150},
        ]
    },

    {
        "family": "Vanta",
        "name": "Vanta Linear Downlight",
        "subtitle": "Linear recessed lighting fixture",
        "wattage": 12,
        "lumens": 1200,
        "variants": [
            {"watt": 12, "lumens": 1200, "cri": 90, "color_temperature": 4000, "width": 40, "height": 140},
            {"watt": 24, "lumens": 2400, "cri": 90, "color_temperature": 4000, "width": 40, "height": 280},
        ]
    },

    {
        "family": "Lyra Bluetooth Speaker",
        "name": "Lyra Bluetooth Speaker",
        "subtitle": "Integrated ceiling speaker solution",
        "wattage": 10,
        "lumens": 0,
        "variants": [
            {"watt": 10, "lumens": 0, "cri": 0, "color_temperature": 0, "width": 75, "height": 75},
        ]
    },

    {
        "family": "Light Engine",
        "name": "Light Engine Module",
        "subtitle": "High performance lighting engine",
        "wattage": 12,
        "lumens": 1200,
        "variants": [
            {"watt": 10, "lumens": 900, "cri": 92, "color_temperature": 3000},
            {"watt": 12, "lumens": 1100, "cri": 92, "color_temperature": 3000},
            {"watt": 12, "lumens": 1150, "cri": 92, "color_temperature": 4000},
        ]
    },

    {
        "family": "GU10 Lamp",
        "name": "GU10 LED Lamp",
        "subtitle": "Efficient GU10 retrofit lamp",
        "wattage": 7,
        "lumens": 560,
        "variants": [
            {"watt": 7, "lumens": 560, "cri": 85, "color_temperature": 4000},
        ]
    },

    {
        "family": "Virgo",
        "name": "Virgo Gypsum Downlight",
        "subtitle": "Square gypsum recessed downlight",
        "wattage": 6,
        "lumens": 560,
        "variants": [
            {"watt": 6, "lumens": 560, "cri": 80, "color_temperature": 4000, "width": 125, "height": 125},
        ]
    },

    {
        "family": "Virgo C",
        "name": "Virgo C Gypsum Downlight",
        "subtitle": "Round gypsum recessed downlight",
        "wattage": 6,
        "lumens": 560,
        "variants": [
            {"watt": 6, "lumens": 560, "cri": 80, "color_temperature": 4000, "depth": 140, "height": 140},
        ]
    },

    {
        "family": "Vega",
        "name": "Vega Gypsum Downlight",
        "subtitle": "Compact gypsum ceiling fixture",
        "wattage": 6,
        "lumens": 560,
        "variants": [
            {"watt": 6, "lumens": 560, "cri": 80, "color_temperature": 4000, "width": 120, "height": 120},
        ]
    },
]
        PRODUCTS += [

    {
        "family": "Fornax",
        "name": "Fornax Gypsum Downlight",
        "subtitle": "Architectural square gypsum downlight",
        "wattage": 6,
        "lumens": 560,
        "variants": [
            {"watt": 6, "lumens": 560, "cri": 80, "color_temperature": 4000, "width": 170, "height": 170},
        ]
    },

    {
        "family": "Pollux",
        "name": "Pollux Gypsum Downlight",
        "subtitle": "Compact square recessed fixture",
        "wattage": 6,
        "lumens": 560,
        "variants": [
            {"watt": 6, "lumens": 560, "cri": 80, "color_temperature": 4000, "width": 90, "height": 90},
        ]
    },

    {
        "family": "Pictor",
        "name": "Pictor Decorative Downlight",
        "subtitle": "Elegant recessed lighting fixture",
        "wattage": 6,
        "lumens": 550,
        "variants": [
            {"watt": 6, "lumens": 550, "cri": 80, "color_temperature": 4000, "width": 125, "height": 125},
        ]
    },

    {
        "family": "Pyxis",
        "name": "Pyxis Decorative Downlight",
        "subtitle": "Modern recessed architectural luminaire",
        "wattage": 6,
        "lumens": 550,
        "variants": [
            {"watt": 6, "lumens": 550, "cri": 80, "color_temperature": 4000, "width": 110, "height": 110},
        ]
    },

    {
        "family": "Blink",
        "name": "Blink Decorative Downlight",
        "subtitle": "Minimalist ceiling recessed fixture",
        "wattage": 6,
        "lumens": 550,
        "variants": [
            {"watt": 6, "lumens": 550, "cri": 80, "color_temperature": 4000, "width": 110, "height": 110},
        ]
    },

    {
        "family": "Folcano",
        "name": "Folcano Decorative Downlight",
        "subtitle": "Architectural recessed ceiling light",
        "wattage": 6,
        "lumens": 550,
        "variants": [
            {"watt": 6, "lumens": 550, "cri": 80, "color_temperature": 4000, "width": 110, "height": 110},
        ]
    },

    {
        "family": "Wave",
        "name": "Wave Decorative Downlight",
        "subtitle": "Curved gypsum recessed luminaire",
        "wattage": 6,
        "lumens": 550,
        "variants": [
            {"watt": 6, "lumens": 550, "cri": 80, "color_temperature": 4000, "width": 170, "height": 170},
        ]
    },

    {
        "family": "Vela",
        "name": "Vela Decorative Downlight",
        "subtitle": "Modern decorative ceiling fixture",
        "wattage": 6,
        "lumens": 550,
        "variants": [
            {"watt": 6, "lumens": 550, "cri": 80, "color_temperature": 4000, "width": 140, "height": 160},
        ]
    },

    {
        "family": "Virgo Double",
        "name": "Virgo Double Downlight",
        "subtitle": "Dual head gypsum downlight",
        "wattage": 12,
        "lumens": 1100,
        "variants": [
            {"watt": 12, "lumens": 1100, "cri": 80, "color_temperature": 4000, "width": 235, "height": 125},
        ]
    },

    {
        "family": "Pollux Double",
        "name": "Pollux Double Downlight",
        "subtitle": "Twin recessed spotlight fixture",
        "wattage": 12,
        "lumens": 1100,
        "variants": [
            {"watt": 12, "lumens": 1100, "cri": 80, "color_temperature": 4000, "width": 150, "height": 80},
        ]
    },

    {
        "family": "Castor",
        "name": "Castor Downlight",
        "subtitle": "Rectangular recessed architectural light",
        "wattage": 12,
        "lumens": 1100,
        "variants": [
            {"watt": 12, "lumens": 1100, "cri": 80, "color_temperature": 4000, "width": 205, "height": 125},
        ]
    },

    {
        "family": "Castor 3",
        "name": "Castor Triple Downlight",
        "subtitle": "Triple head recessed lighting fixture",
        "wattage": 18,
        "lumens": 1650,
        "variants": [
            {"watt": 18, "lumens": 1650, "cri": 80, "color_temperature": 4000, "width": 205, "height": 125},
        ]
    },

]
        PRODUCTS += [

    {
        "family": "Cylindra GU10",
        "name": "Cylindra GU10 Surface Light",
        "subtitle": "Surface mounted GU10 cylindrical luminaire",
        "wattage": 6,
        "lumens": 560,
        "variants": [
            {"watt": 6, "lumens": 560, "cri": 80, "color_temperature": 4000, "depth": 60, "height": 84},
        ]
    },

    {
        "family": "Cylindra COB",
        "name": "Cylindra COB Surface Light",
        "subtitle": "High performance COB surface mounted fixture",
        "wattage": 6,
        "lumens": 600,
        "variants": [
            {"watt": 6, "lumens": 600, "cri": 90, "color_temperature": 4000},
            {"watt": 12, "lumens": 1440, "cri": 90, "color_temperature": 4000},
            {"watt": 20, "lumens": 2400, "cri": 90, "color_temperature": 4000},
        ]
    },

    {
        "family": "Cylindra SMD",
        "name": "Cylindra SMD Surface Light",
        "subtitle": "Modern cylindrical SMD ceiling fixture",
        "wattage": 8,
        "lumens": 720,
        "variants": [
            {"watt": 8, "lumens": 720, "cri": 80, "color_temperature": 4000},
            {"watt": 15, "lumens": 1300, "cri": 80, "color_temperature": 4000},
        ]
    },

    {
        "family": "Caror",
        "name": "Caror Decorative Ceiling Light",
        "subtitle": "Decorative ceiling luminaire with premium light quality",
        "wattage": 18,
        "lumens": 1600,
        "variants": [
            {"watt": 18, "lumens": 1600, "cri": 90, "color_temperature": 4000},
        ]
    },

    {
        "family": "Point",
        "name": "Point Recessed Downlight",
        "subtitle": "Professional recessed downlight for architectural projects",
        "wattage": 12,
        "lumens": 1200,
        "variants": [
            {"watt": 7, "lumens": 670, "cri": 90, "color_temperature": 4000},
            {"watt": 12, "lumens": 1150, "cri": 90, "color_temperature": 4000},
            {"watt": 15, "lumens": 1400, "cri": 90, "color_temperature": 4000},
            {"watt": 20, "lumens": 1900, "cri": 90, "color_temperature": 4000},
        ]
    },

    {
        "family": "Supernova",
        "name": "Supernova High Power Downlight",
        "subtitle": "High output commercial lighting solution",
        "wattage": 60,
        "lumens": 5100,
        "variants": [
            {"watt": 60, "lumens": 5100, "cri": 90, "color_temperature": 4000},
            {"watt": 100, "lumens": 8400, "cri": 90, "color_temperature": 4000},
            {"watt": 140, "lumens": 11700, "cri": 90, "color_temperature": 4000},
            {"watt": 170, "lumens": 14200, "cri": 90, "color_temperature": 4000},
        ]
    },

    {
        "family": "Super Ring",
        "name": "Super Ring High Power Downlight",
        "subtitle": "Circular commercial downlight with powerful illumination",
        "wattage": 60,
        "lumens": 5100,
        "variants": [
            {"watt": 60, "lumens": 5100, "cri": 90, "color_temperature": 4000},
            {"watt": 90, "lumens": 8100, "cri": 90, "color_temperature": 4000},
            {"watt": 120, "lumens": 10000, "cri": 90, "color_temperature": 4000},
            {"watt": 150, "lumens": 12500, "cri": 90, "color_temperature": 4000},
        ]
    },

]

        for item in PRODUCTS:

            family, _ = Family.objects.get_or_create(
                name=item["family"],
                defaults={
                    "category": category,
                    "subtitle": f"{item['family']} Lighting Family",
                    "is_active": True,
                }
            )

            product, created = Product.objects.get_or_create(
            name=item["name"],
            defaults={
                "category": category,
                "family": family,

                "subtitle": item["subtitle"],
                "description": item["subtitle"],

                "full_description": (
                    f"{item['name']} is a premium architectural lighting fixture "
                    f"designed for commercial, retail and residential applications. "
                    f"Manufactured from high quality aluminum and engineered for "
                    f"excellent visual comfort, efficiency and long-term reliability."
                ),

                "cri": item["variants"][0]["cri"],
                "color_temperature": item["variants"][0]["color_temperature"],
                "wattage": item["wattage"],
                "lumens": item["lumens"],
                "voltage": "220V",
                "ip_rating": "IP20",
                "lifespan": 50000,

                "is_active": True,

                "meta_title": item["name"][:60],
                "meta_description": item["subtitle"][:160],

                "image1_alt": item["name"],
            }
        )

            product.finishes.add(black_finish, white_finish)

            if created and image_path.exists():
                with open(image_path, "rb") as img:
                    product.image1.save(
                        "retail1.png",
                        File(img),
                        save=True
                    )

            for variant in item["variants"]:

                dimension, _ = Dimension.objects.get_or_create(
                label=f"{variant['watt']}W",
                defaults={
                    "width": variant.get("width"),
                    "height": variant.get("height"),
                    "depth": variant.get("depth"),
                    }
                )

                ProductVariant.objects.get_or_create(
                product=product,
                model_name=f"{variant['watt']}W",
                dimension=dimension,
                defaults={
                    "wattage": variant["watt"],
                    "lumens": variant["lumens"],
                    "color_temperature": variant["color_temperature"],
                    "sku": f"SKU-{uuid4().hex[:10].upper()}",
                    "is_active": True,
                }
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully seeded {len(PRODUCTS)} products."
            )
        )