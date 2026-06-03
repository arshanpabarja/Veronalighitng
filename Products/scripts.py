import random
from django.core.files.base import ContentFile
from Products.models import Product, Category


def create_random_products():
    categories = list(Category.objects.all())

    if not categories:
        print("You need at least one Category and Brand in the database.")
        return

    for i in range(3):
        product = Product.objects.create(
            name=f"Sample Lamp {random.randint(100,999)}",
            category=random.choice(categories),
            subtitle="Modern decorative lamp",
            description="Short description for demo product.",
            full_description="Full description for demo lighting product.",
            wattage=random.choice([5, 7, 10, 12]),
            lumens=random.randint(400, 1200),
            color_temperature=random.choice([2700, 3000, 4000, 6500]),
            cri=random.choice([80, 90]),
            beam_angle=random.choice([30, 45, 60, 120]),
            voltage="220-240V",
            ip_rating=random.choice(["IP20", "IP44"]),
            dimmable=random.choice([True, False]),
            lamp_base_type=random.choice(["E27", "E14", "GU10"]),
            lifespan=random.randint(15000, 50000),
            image1="products/default.jpg",  # placeholder image
        )

        print(f"Created product: {product.name}")


create_random_products()
