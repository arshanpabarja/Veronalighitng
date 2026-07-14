import json

from django.core.management.base import BaseCommand

from Products.models import Family


class Command(BaseCommand):

    help = "Export families to JSON"


    def handle(self, *args, **kwargs):

        data = []

        for family in Family.objects.prefetch_related("applications").select_related("category"):

            data.append({
                "id": family.id,
                "name": family.name_en,
                "subtitle": family.subtitle,
                "meta_title": family.meta_title,
                "meta_description": family.meta_description,
                "category": family.category.name if family.category else "",
                "applications": [
                    app.name
                    for app in family.applications.all()
                ]
            })

        with open(
            "families.json",
            "w",
            encoding="utf-8"
        ) as f:
            json.dump(
                data,
                f,
                ensure_ascii=False,
                indent=4
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Exported {len(data)} families."
            )
        )