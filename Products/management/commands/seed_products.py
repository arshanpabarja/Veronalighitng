from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.utils import timezone
from Products.models import Family, Product
from core.models import NewsArticle, NewsCategory


class Command(BaseCommand):
    help = "Seed 10 news articles"

    def handle(self, *args, **kwargs):

        family = Family.objects.filter(category='Magent Small(2cm) Family')

        for i in family:
            print(i)