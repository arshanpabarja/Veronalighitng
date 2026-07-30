import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from Products.models import Application, Category, Family, Product


# The site intentionally keeps all gypsum catalog products in one family.
# IDs 123-136 in the export represent the former split structure and must not
# overwrite or recreate that consolidated family.
GYPSUM_JSON_FAMILY_IDS = frozenset(range(123, 137))


# The JSON export contains family records, but not the product relationship.
# This non-gypsum relationship is unambiguous from the family category.
PRODUCT_FAMILY_CORRECTIONS = {
    41: 165,   # MAGNETO SMALL SIGN EMERGENCY
}

TRANSLATED_FIELDS = (
    "name_en",
    "name_fa",
    "subtitle_en",
    "subtitle_fa",
    "meta_title_en",
    "meta_title_fa",
    "meta_description_en",
    "meta_description_fa",
)


class Command(BaseCommand):
    help = (
        "Import family metadata from a JSON export while preserving the "
        "site's consolidated Gypsum family, and restore the remaining "
        "product-family relationships represented by that export. "
        "Runs as a dry-run unless --apply is supplied."
    )

    def add_arguments(self, parser):
        parser.add_argument("json_path", help="Path to the families JSON export.")
        parser.add_argument(
            "--apply",
            action="store_true",
            help="Commit the validated family and product relationship changes.",
        )

    def handle(self, *args, **options):
        path = Path(options["json_path"]).expanduser().resolve()
        if not path.is_file():
            raise CommandError(f"Family JSON file does not exist: {path}")

        try:
            records = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise CommandError(f"Could not read valid UTF-8 JSON: {exc}") from exc

        self._validate(records)
        import_records = [
            record
            for record in records
            if record["id"] not in GYPSUM_JSON_FAMILY_IDS
        ]
        summary = self._build_summary(import_records)

        if not options["apply"]:
            self._write_summary(summary, applied=False)
            return

        with transaction.atomic():
            category_by_name = {
                category.name: category
                for category in Category.objects.filter(
                    name__in={
                        record["category"] for record in import_records
                    }
                )
            }
            application_by_name = {
                application.name: application
                for application in Application.objects.filter(
                    name__in={
                        name
                        for record in import_records
                        for name in record.get("applications", [])
                    }
                )
            }

            for record in import_records:
                family, created = Family.objects.get_or_create(
                    pk=record["id"],
                    defaults={
                        "name": record["name_en"],
                        "is_active": True,
                    },
                )
                for field in TRANSLATED_FIELDS:
                    setattr(family, field, record.get(field))
                family.category = category_by_name[record["category"]]
                if created and family.is_active is None:
                    family.is_active = True
                family.save()
                family.applications.set(
                    application_by_name[name]
                    for name in record.get("applications", [])
                )

            for product_id, family_id in PRODUCT_FAMILY_CORRECTIONS.items():
                Product.objects.filter(pk=product_id).update(family_id=family_id)

        self._write_summary(summary, applied=True)

    def _validate(self, records):
        if not isinstance(records, list) or not records:
            raise CommandError("The JSON root must be a non-empty list.")

        required = {"id", "name_en", "name_fa", "category", "applications"}
        ids = []
        category_names = set()
        application_names = set()
        for index, record in enumerate(records):
            if not isinstance(record, dict):
                raise CommandError(f"Record {index} is not a JSON object.")
            missing = required - set(record)
            if missing:
                raise CommandError(
                    f"Record {index} is missing: {', '.join(sorted(missing))}"
                )
            if not isinstance(record["id"], int):
                raise CommandError(f"Record {index} has a non-integer id.")
            if not record["name_en"] or not record["name_fa"]:
                raise CommandError(f"Family {record['id']} has an empty name.")
            if not isinstance(record["applications"], list):
                raise CommandError(
                    f"Family {record['id']} applications must be a list."
                )
            ids.append(record["id"])
            category_names.add(record["category"])
            application_names.update(record["applications"])

        duplicate_ids = sorted(
            family_id for family_id in set(ids) if ids.count(family_id) > 1
        )
        if duplicate_ids:
            raise CommandError(
                "Duplicate family IDs: "
                + ", ".join(str(family_id) for family_id in duplicate_ids)
            )

        missing_categories = sorted(
            category_names
            - set(
                Category.objects.filter(name__in=category_names).values_list(
                    "name", flat=True
                )
            )
        )
        if missing_categories:
            raise CommandError(
                "Unknown categories: " + ", ".join(missing_categories)
            )

        missing_applications = sorted(
            application_names
            - set(
                Application.objects.filter(
                    name__in=application_names
                ).values_list("name", flat=True)
            )
        )
        if missing_applications:
            raise CommandError(
                "Unknown applications: " + ", ".join(missing_applications)
            )

        missing_products = sorted(
            set(PRODUCT_FAMILY_CORRECTIONS)
            - set(
                Product.objects.filter(
                    pk__in=PRODUCT_FAMILY_CORRECTIONS
                ).values_list("pk", flat=True)
            )
        )
        if missing_products:
            raise CommandError(
                "Products required for family restoration are missing: "
                + ", ".join(str(product_id) for product_id in missing_products)
            )

        json_family_ids = set(ids)
        missing_target_families = sorted(
            set(PRODUCT_FAMILY_CORRECTIONS.values()) - json_family_ids
        )
        if missing_target_families:
            raise CommandError(
                "Product target families are absent from the JSON: "
                + ", ".join(str(family_id) for family_id in missing_target_families)
            )

    def _build_summary(self, records):
        family_by_id = {
            family.id: family
            for family in Family.objects.filter(
                pk__in=[record["id"] for record in records]
            ).select_related("category")
        }
        created = []
        updated = []
        unchanged = []
        for record in records:
            family = family_by_id.get(record["id"])
            if family is None:
                created.append(record["id"])
                continue
            differs = any(
                (getattr(family, field) or "") != (record.get(field) or "")
                for field in TRANSLATED_FIELDS
            )
            differs = differs or (
                (family.category.name if family.category else "")
                != record["category"]
            )
            current_applications = set(
                family.applications.values_list("name", flat=True)
            )
            differs = differs or current_applications != set(
                record.get("applications", [])
            )
            (updated if differs else unchanged).append(record["id"])

        changed_products = []
        for product in Product.objects.filter(
            pk__in=PRODUCT_FAMILY_CORRECTIONS
        ).only("id", "family_id"):
            target = PRODUCT_FAMILY_CORRECTIONS[product.id]
            if product.family_id != target:
                changed_products.append((product.id, product.family_id, target))

        return {
            "created": created,
            "updated": updated,
            "unchanged": unchanged,
            "changed_products": sorted(changed_products),
        }

    def _write_summary(self, summary, *, applied):
        mode = "APPLIED" if applied else "DRY RUN"
        self.stdout.write(self.style.SUCCESS(f"{mode}: family JSON validated"))
        self.stdout.write(
            f"Families: {len(summary['created'])} create, "
            f"{len(summary['updated'])} update, "
            f"{len(summary['unchanged'])} unchanged"
        )
        self.stdout.write(
            f"Product-family corrections: {len(summary['changed_products'])}"
        )
        self.stdout.write(
            "Preserved consolidated Gypsum family; skipped split family "
            "records 123-136."
        )
        for product_id, old_family_id, new_family_id in summary[
            "changed_products"
        ]:
            self.stdout.write(
                f"  Product {product_id}: {old_family_id} -> {new_family_id}"
            )
