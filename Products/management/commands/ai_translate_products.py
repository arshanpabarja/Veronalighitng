from django.core.management.base import BaseCommand

from Products.models import Product
from Products.services.translator import translate_product


class Command(BaseCommand):

    help = "Translate products to Persian using AI"


    def add_arguments(self, parser):

        parser.add_argument(
            "--force",
            action="store_true",
            help="Retranslate all products",
        )

        parser.add_argument(
            "--id",
            type=int,
            help="Translate specific product",
        )
        
        parser.add_argument(
            "--ids",
            type=str,
            help="Translate multiple products. Example: 3,24,28",
        )


    def handle(self, *args, **options):

        force = options["force"]
        ids = options.get("ids")
        product_id = options.get("id")


        if product_id:

            products = Product.objects.filter(
                id=product_id
            )

        elif ids:

            id_list = [
                int(x.strip())
                for x in ids.split(",")
                if x.strip()
            ]

            products = Product.objects.filter(
                id__in=id_list
            )

        elif force:

            products = Product.objects.all()


        else:

            products = (
                Product.objects.filter(
                    name_fa__isnull=True
                )
                |
                Product.objects.filter(
                    name_fa=""
                )
            ).order_by("id")



        self.stdout.write(
            self.style.SUCCESS(
                f"\nFound {products.count()} products\n"
            )
        )


        translated_count = 0
        skipped_count = 0
        failed_count = 0



        for product in products:


            if (
                not force
                and not product_id
                and not ids
                and product.name_fa
            ):

                skipped_count += 1

                self.stdout.write(
                    self.style.WARNING(
                        f"⏭ Skipped: {product.name}"
                    )
                )

                continue



            self.stdout.write(
                f"🌐 Translating #{product.id} - {product.name}"
            )



            data = {

                "name": (
                    product.name_en
                    or product.name
                    or ""
                ),


                "subtitle": (
                    product.subtitle_en
                    or product.subtitle
                    or ""
                ),


                "description": (
                    product.description_en
                    or product.description
                    or ""
                ),


                "full_description": (
                    product.full_description_en
                    or product.full_description
                    or ""
                ),


                "meta_title": (
                    product.meta_title_en
                    or product.meta_title
                    or ""
                ),


                "meta_description": (
                    product.meta_description_en
                    or product.meta_description
                    or ""
                ),


                "images": {

                    "image1_alt": (
                        product.image1_alt_en
                        or product.image1_alt
                        or ""
                    ),

                    "image2_alt": (
                        product.image2_alt_en
                        or product.image2_alt
                        or ""
                    ),

                    "image3_alt": (
                        product.image3_alt_en
                        or product.image3_alt
                        or ""
                    ),

                    "image4_alt": (
                        product.image4_alt_en
                        or product.image4_alt
                        or ""
                    ),

                },


                "product_info": {

                    "category": (
                        product.category.name
                        if getattr(product, "category", None)
                        else ""
                    ),


                    "family": (
                        product.family.name
                        if getattr(product, "family", None)
                        else ""
                    ),

                }

            }



            try:


                translated = translate_product(
                    data
                )


                if not translated:

                    raise Exception(
                        "Empty translation result"
                    )



                product.name_fa = (
                    translated["name"]
                )

                product.subtitle_fa = (
                    translated["subtitle"]
                )

                product.description_fa = (
                    translated["description"]
                )

                product.full_description_fa = (
                    translated["full_description"]
                )

                product.meta_title_fa = (
                    translated["meta_title"]
                )

                product.meta_description_fa = (
                    translated["meta_description"]
                )

                product.image1_alt_fa = (
                    translated["image1_alt"]
                )

                product.image2_alt_fa = (
                    translated["image2_alt"]
                )

                product.image3_alt_fa = (
                    translated["image3_alt"]
                )

                product.image4_alt_fa = (
                    translated["image4_alt"]
                )



                product.save(
                    update_fields=[

                        "name_fa",

                        "subtitle_fa",

                        "description_fa",

                        "full_description_fa",

                        "meta_title_fa",

                        "meta_description_fa",

                        "image1_alt_fa",

                        "image2_alt_fa",

                        "image3_alt_fa",

                        "image4_alt_fa",

                    ]
                )



                translated_count += 1


                self.stdout.write(
                    self.style.SUCCESS(
                        f"✅ Saved: {product.name}"
                    )
                )



            except Exception as e:


                failed_count += 1


                self.stdout.write(
                    self.style.ERROR(
                        f"❌ Failed: {product.name}"
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