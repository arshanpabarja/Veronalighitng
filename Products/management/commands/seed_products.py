from django.core.management.base import BaseCommand
from django.db import transaction

from Products.models import Category, Family, Product


class Command(BaseCommand):
    help = "Rename MAGNETAR to MAGNETO for families and products in Magent Small and Large categories"

    @transaction.atomic
    def handle(self, *args, **options):
        
        # Define the categories you want to update
        category_names = [
            "Magent Small(2cm) Family",
            "Magent Large(4cm) Family"
        ]
        
        # Get all matching categories
        categories = Category.objects.filter(name__in=category_names)
        
        if not categories.exists():
            self.stdout.write(
                self.style.ERROR(
                    f'No categories found matching: {", ".join(category_names)}'
                )
            )
            return
        
        # Get all families in these categories
        families = Family.objects.filter(category__in=categories)
        
        families_updated = 0
        products_updated = 0
        
        # Update Family names
        self.stdout.write(self.style.WARNING("\n=== Updating Families ==="))
        for family in families:
            if family.name and "MAGNETAR" in family.name.upper():
                old_name = family.name
                new_name = old_name.replace("MAGNETAR", "MAGNETO")
                
                family.name = new_name
                family.save(update_fields=["name"])
                
                families_updated += 1
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Family: {old_name} -> {new_name}'
                    )
                )
        
        # Update Product names in these families
        self.stdout.write(self.style.WARNING("\n=== Updating Products ==="))
        products = Product.objects.filter(family__in=families)
        
        for product in products:
            if product.name and "MAGNETAR" in product.name.upper():
                old_name = product.name
                new_name = old_name.replace("MAGNETAR", "MAGNETO")
                
                product.name = new_name
                product.save(update_fields=["name"])
                
                products_updated += 1
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Product: {old_name} -> {new_name}'
                    )
                )
        
        # Summary
        self.stdout.write(
            self.style.SUCCESS(
                f"\n✓ Updated {families_updated} families"
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"✓ Updated {products_updated} products"
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"✓ Total: {families_updated + products_updated} items renamed"
            )
        )