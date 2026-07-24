from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from Products.models import Project
from Products.services.project_authority_content import (
    PROJECT_AUTHORITY_CONTENT,
    validate_project_authority_content,
)


class Command(BaseCommand):
    help = "Preview or apply reviewed bilingual SEO content for authority projects."

    def add_arguments(self, parser):
        parser.add_argument(
            "--apply",
            action="store_true",
            help="Write the reviewed project content to the database.",
        )

    def handle(self, *args, **options):
        validate_project_authority_content()
        projects = {
            project.slug: project
            for project in Project.objects.filter(
                slug__in=PROJECT_AUTHORITY_CONTENT,
                is_published=True,
            )
        }
        missing = set(PROJECT_AUTHORITY_CONTENT) - set(projects)
        if missing:
            raise CommandError(
                f"Published authority projects not found: {', '.join(sorted(missing))}"
            )

        if not options["apply"]:
            self.stdout.write("PREVIEW MODE (no database changes)")
            for slug, project in projects.items():
                status = "COMPLETE" if project.name_fa and project.meta_title_fa else "NEEDS CONTENT"
                self.stdout.write(f"[{status}] {slug}")
            self.stdout.write(
                "Would add Persian case-study content and bilingual metadata to 2 projects."
            )
            return

        update_fields = (
            "name_fa",
            "location_fa",
            "project_type_fa",
            "intro_heading_fa",
            "intro_text_fa",
            "overview_text_fa",
            "about_content_fa",
            "meta_title_fa",
            "meta_description_fa",
            "meta_title_en",
            "meta_description_en",
        )
        with transaction.atomic():
            for slug, content in PROJECT_AUTHORITY_CONTENT.items():
                project = projects[slug]
                for field in update_fields:
                    setattr(project, field, getattr(content, field))
                project.save(update_fields=update_fields)
                self.stdout.write(f"[UPDATED] {slug}")

        self.stdout.write(
            self.style.SUCCESS(
                "Prepared 2 bilingual project pages for editorial and partner outreach."
            )
        )
