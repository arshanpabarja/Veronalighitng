from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from Products.models import Category, Family
import os


class Command(BaseCommand):
    help = 'Update family icons with product images for a specific category'

    def add_arguments(self, parser):
        parser.add_argument(
            'category',
            type=str,
            help='Category name (e.g., "Magnet Small", "Magnet Curve")'
        )

    def handle(self, *args, **options):
        category_name = options['Magnet Curve']
        
        # Find the category (case-insensitive)
        try:
            category = Category.objects.get(name__icontains=category_name)
        except Category.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Category "{category_name}" not found'))
            return
        except Category.MultipleObjectsReturned:
            self.stdout.write(self.style.ERROR(f'Multiple categories match "{category_name}". Be more specific.'))
            return

        # Get all families in this category
        families = Family.objects.filter(category=category)
        self.stdout.write(f'Found {families.count()} families in "{category.name}"')

        updated_count = 0
        for family in families:
            # Get first product with image1
            product = family.products.filter(is_active=True, image1__isnull=False).exclude(image1='').first()
            
            if product and product.image1:
                try:
                    # Read the product image
                    product_image = product.image1
                    
                    # Copy to family icon
                    with product_image.open('rb') as f:
                        image_content = f.read()
                    
                    # Generate filename
                    filename = os.path.basename(product_image.name)
                    
                    # Save to family icon (replace existing or create new)
                    if family.icon:
                        family.icon.delete()
                    family.icon.save(filename, ContentFile(image_content), save=True)
                    
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ {family.name} → {product.name}')
                    )
                    updated_count += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'✗ {family.name}: {str(e)}'))
            else:
                self.stdout.write(self.style.WARNING(f'- {family.name} (no product image found)'))

        self.stdout.write(self.style.SUCCESS(f'\nCompleted: {updated_count} families updated'))
