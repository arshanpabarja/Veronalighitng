from django.core.management.base import BaseCommand

from Products.models import Family
from Products.services.translator import translate_product


class Command(BaseCommand):

    help = "Translate families to Persian using AI"


    def add_arguments(self, parser):

        parser.add_argument(
            "--force",
            action="store_true",
            help="Retranslate all families",
        )

        parser.add_argument(
            "--id",
            type=int,
            help="Translate specific family",
        )

        parser.add_argument(
            "--ids",
            type=str,
            help="Translate multiple families. Example: 3,24,28",
        )


    def handle(self, *args, **options):

        force = options["force"]
        ids = options.get("ids")
        family_id = options.get("id")


        if family_id:

            families = Family.objects.filter(id=family_id)
            print(families)


        elif ids:

            id_list = [
                int(x.strip())
                for x in ids.split(",")
                if x.strip()
            ]

            families = Family.objects.filter(
                id__in=id_list
            )


        elif force:

            families = Family.objects.all()


        else:

            families = (
                Family.objects.filter(
                    name_fa__isnull=True
                )
                |
                Family.objects.filter(
                    name_fa=""
                )
            ).order_by("id")


        self.stdout.write(
            self.style.SUCCESS(
                f"\nFound {families.count()} families\n"
            )
        )


        translated_count = 0
        skipped_count = 0
        failed_count = 0


        for family in families:


            if (
                not force
                and not family_id
                and not ids
                and family.name_fa
            ):

                skipped_count += 1

                self.stdout.write(
                    self.style.WARNING(
                        f"⏭ Skipped: {family.name}"
                    )
                )

                continue


            self.stdout.write(
                f"🌐 Translating #{family.id} - {family.name}"
            )


            data = {

                "name": (
                    family.name_en
                    or ""
                ),

                "subtitle": (
                    family.subtitle_en
                    or ""
                ),

                "meta_title": (
                    family.meta_title_en
                    or ""
                ),

                "meta_description": (
                    family.meta_description_en
                    or ""
                ),

            }


            try:

                translated = translate_product(
                    data
                ) 
                print(translated)


                if not translated:

                    raise Exception(
                        "Empty translation result"
                    )


                print(translated["name"])
                family.name_fa = (
                    translated["name"]
                )

                family.subtitle_fa = (
                    translated["subtitle"]
                )

                family.meta_title_fa = (
                    translated["meta_title"]
                )

                family.meta_description_fa = (
                    translated["meta_description"]
                )


                family.save(
                    update_fields=[

                        "name_fa",

                        "subtitle_fa",

                        "meta_title_fa",

                        "meta_description_fa",

                    ]
                )


                translated_count += 1


                self.stdout.write(
                    self.style.SUCCESS(
                        f"✅ Saved: {family.name}"
                    )
                )


            except Exception as e:


                failed_count += 1


                self.stdout.write(
                    self.style.ERROR(
                        f"❌ Failed: {family.name}"
                    )
                )


                self.stdout.write(
                    str(e)
                )


        self.stdout.write("\n")

        self.stdout.write(
            self.style.SUCCESS(
                "========== DONE =========="
            )
        )

        self.stdout.write(
            f"Translated : {translated_count}"
        )

        self.stdout.write(
            f"Skipped    : {skipped_count}"
        )

        self.stdout.write(
            f"Failed     : {failed_count}"
        )