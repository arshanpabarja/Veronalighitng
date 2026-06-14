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
        category_name = options['category']
        
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

        downlights = Category.objects.get(name="Downlights")

        for family in families:
            family.category = downlights
            family.save()
            self.stdout.write(self.style.SUCCESS(f'Updated family "{family.name}" to category "{downlights.name}"'))