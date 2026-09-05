from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory

from django.core.management import call_command
from django.test import TestCase, override_settings

from Products.models import Application, Project
from Products.services.latest_project_import import LATEST_PROJECTS


class LatestProjectImportTests(TestCase):
    def setUp(self):
        Application.objects.create(name="Residential", slug="house")
        Application.objects.create(name="Retail", slug="retail")

    def _create_media_files(self, media_root):
        for record in LATEST_PROJECTS.values():
            for image_name in (record["hero_image"], *record["gallery_images"]):
                image_path = Path(media_root) / image_name
                image_path.parent.mkdir(parents=True, exist_ok=True)
                image_path.write_bytes(b"test image")

    def test_command_previews_then_idempotently_imports_three_projects(self):
        with TemporaryDirectory() as media_root, override_settings(MEDIA_ROOT=media_root):
            self._create_media_files(media_root)

            preview = StringIO()
            call_command("import_latest_projects", stdout=preview)
            self.assertIn("PREVIEW MODE", preview.getvalue())
            self.assertEqual(Project.objects.count(), 0)

            call_command("import_latest_projects", "--apply", stdout=StringIO())
            call_command("import_latest_projects", "--apply", stdout=StringIO())

        self.assertEqual(Project.objects.count(), 3)
        self.assertEqual(
            sum(project.gallery_images.count() for project in Project.objects.all()),
            6,
        )

        hormozan = Project.objects.get(slug="hormozan-tower-residence")
        self.assertEqual(hormozan.name_fa, "برج هرمزان")
        self.assertEqual(hormozan.name_en, "Hormozan Tower Residence")
        self.assertEqual(hormozan.application.slug, "house")
        self.assertTrue(hormozan.is_published)

        diamond = Project.objects.get(slug="diamond-boutique")
        self.assertEqual(diamond.application.slug, "retail")
        self.assertEqual(diamond.gallery_images.count(), 2)

