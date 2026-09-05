from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from Products.models import Application, Project, ProjectGalleryImage
from Products.services.latest_project_import import (
    LATEST_PROJECTS,
    TRANSLATED_FIELDS,
    validate_latest_projects,
)


class Command(BaseCommand):
    help = "Preview or import the three newest bilingual projects from veronalighting.co."

    def add_arguments(self, parser):
        parser.add_argument(
            "--apply",
            action="store_true",
            help="Create or update the projects in the configured database.",
        )

    def handle(self, *args, **options):
        try:
            validate_latest_projects(settings.MEDIA_ROOT)
        except ValueError as exc:
            raise CommandError(str(exc)) from exc

        application_slugs = {
            record["application_slug"] for record in LATEST_PROJECTS.values()
        }
        applications = {
            application.slug: application
            for application in Application.objects.filter(slug__in=application_slugs)
        }
        missing_applications = application_slugs - set(applications)
        if missing_applications:
            raise CommandError(
                "Missing applications: " + ", ".join(sorted(missing_applications))
            )

        if not options["apply"]:
            self.stdout.write("PREVIEW MODE (no database changes)")
            for slug in LATEST_PROJECTS:
                status = "UPDATE" if Project.objects.filter(slug=slug).exists() else "CREATE"
                self.stdout.write(f"[{status}] {slug}")
            return

        with transaction.atomic():
            for slug, record in LATEST_PROJECTS.items():
                defaults = {
                    "completion_year": record["completion_year"],
                    "hero_image": record["hero_image"],
                    "application": applications[record["application_slug"]],
                    "order": record["order"],
                    "is_published": True,
                }
                for field in TRANSLATED_FIELDS:
                    defaults[field] = record[f"{field}_fa"]
                    defaults[f"{field}_fa"] = record[f"{field}_fa"]
                    defaults[f"{field}_en"] = record[f"{field}_en"]

                project, created = Project.objects.update_or_create(
                    slug=slug,
                    defaults=defaults,
                )

                for order, image_name in enumerate(record["gallery_images"], start=1):
                    gallery_image = ProjectGalleryImage.objects.filter(
                        project=project,
                        image=image_name,
                    ).order_by("pk").first()
                    if gallery_image is None:
                        ProjectGalleryImage.objects.create(
                            project=project,
                            image=image_name,
                            order=order,
                        )
                    elif gallery_image.order != order:
                        gallery_image.order = order
                        gallery_image.save(update_fields=("order",))

                action = "CREATED" if created else "UPDATED"
                self.stdout.write(f"[{action}] {slug}")

            # Preserve the same newest-first order as the live project listing.
            Project.objects.filter(slug="private-villa").update(order=4)

        self.stdout.write(
            self.style.SUCCESS("Imported the three newest bilingual projects.")
        )

