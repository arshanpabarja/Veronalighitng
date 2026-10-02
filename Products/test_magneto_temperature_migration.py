from importlib import import_module

from django.test import SimpleTestCase


rewrite_temperature_range = import_module(
    "Products.migrations.0054_update_magneto_color_temperature_descriptions"
).rewrite_temperature_range


class MagnetoTemperatureDescriptionMigrationTests(SimpleTestCase):
    def test_rewrites_english_and_persian_range_variants(self):
        examples = {
            "3000K to 6000K": "3000K to 4000K",
            "3000K تا 6000K": "3000K تا 4000K",
            "3000K-6000K": "3000K-4000K",
            "3000–6000K": "3000–4000K",
        }

        for original, expected in examples.items():
            with self.subTest(original=original):
                self.assertEqual(rewrite_temperature_range(original), expected)

    def test_rewrites_three_item_temperature_lists_without_duplicates(self):
        examples = {
            "3000K, 4000K, and 6000K": "3000K and 4000K",
            "3000K (Warm White), 4000K (Neutral White), and 6000K (Cool White)": (
                "3000K (Warm White) and 4000K (Neutral White)"
            ),
            "3000K، 4000K و 6000K": "3000K و 4000K",
        }

        for original, expected in examples.items():
            with self.subTest(original=original):
                self.assertEqual(rewrite_temperature_range(original), expected)

    def test_leaves_unrelated_copy_unchanged(self):
        copy = "This 48V product is available in 3000K and 4000K."

        self.assertEqual(rewrite_temperature_range(copy), copy)
