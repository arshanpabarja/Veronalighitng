from django.core.management.base import BaseCommand
from django.db import transaction

from Products.models import (
    Product,
    Category,
    Family,
    Application,
    Project,
)


class Command(BaseCommand):
    help = "Move old English data from *_fa to *_en."

    @transaction.atomic
    def handle(self, *args, **kwargs):

        self.stdout.write("Fixing Products...")

        for p in Product.objects.all():

            fields = [
                "name",
                "subtitle",
                "description",
                "full_description",
                "meta_title",
                "meta_description",
                "image1_alt",
                "image2_alt",
                "image3_alt",
                "image4_alt",
            ]

            for field in fields:
                fa = f"{field}_fa"
                en = f"{field}_en"

                if hasattr(p, fa) and hasattr(p, en):
                    fa_value = getattr(p, fa)

                    if fa_value and not getattr(p, en):
                        setattr(p, en, fa_value)
                        setattr(p, fa, "")

            p.save()

        self.stdout.write(self.style.SUCCESS("Products fixed."))

        self.stdout.write("Fixing Categories...")

        for obj in Category.objects.all():

            fields = [
                "name",
                "description",
                "meta_title",
                "meta_description",
            ]

            for field in fields:
                fa = f"{field}_fa"
                en = f"{field}_en"

                if hasattr(obj, fa) and hasattr(obj, en):
                    value = getattr(obj, fa)

                    if value and not getattr(obj, en):
                        setattr(obj, en, value)
                        setattr(obj, fa, "")

            obj.save()

        self.stdout.write(self.style.SUCCESS("Categories fixed."))

        self.stdout.write("Fixing Families...")

        for obj in Family.objects.all():

            fields = [
                "name",
                "subtitle",
                "meta_title",
                "meta_description",
            ]

            for field in fields:
                fa = f"{field}_fa"
                en = f"{field}_en"

                if hasattr(obj, fa) and hasattr(obj, en):
                    value = getattr(obj, fa)

                    if value and not getattr(obj, en):
                        setattr(obj, en, value)
                        setattr(obj, fa, "")

            obj.save()

        self.stdout.write(self.style.SUCCESS("Families fixed."))

        self.stdout.write("Fixing Applications...")

        for obj in Application.objects.all():

            fields = [
                "name",
                "short_description",
                "description",
                "cover_image_alt",
                "meta_title",
                "meta_description",
            ]

            for field in fields:
                fa = f"{field}_fa"
                en = f"{field}_en"

                if hasattr(obj, fa) and hasattr(obj, en):
                    value = getattr(obj, fa)

                    if value and not getattr(obj, en):
                        setattr(obj, en, value)
                        setattr(obj, fa, "")

            obj.save()

        self.stdout.write(self.style.SUCCESS("Applications fixed."))

        self.stdout.write("Fixing Projects...")

        for obj in Project.objects.all():

            fields = [
                "name",
                "location",
                "project_type",
                "intro_heading",
                "intro_text",
                "overview_text",
                "about_content",
                "meta_title",
                "meta_description",
            ]

            for field in fields:
                fa = f"{field}_fa"
                en = f"{field}_en"

                if hasattr(obj, fa) and hasattr(obj, en):
                    value = getattr(obj, fa)

                    if value and not getattr(obj, en):
                        setattr(obj, en, value)
                        setattr(obj, fa, "")

            obj.save()

        self.stdout.write(self.style.SUCCESS("Projects fixed."))

        self.stdout.write(self.style.SUCCESS("\n✓ All translations fixed successfully."))