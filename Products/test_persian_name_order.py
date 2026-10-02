from django.test import SimpleTestCase

from Products.services.catalog_fa_names import translate_catalog_name


class PersianCatalogNameOrderTests(SimpleTestCase):
    def test_orders_luminaire_names_in_persian(self):
        examples = {
            "Caror Decorative Ceiling Light": "چراغ سقفی دکوراتیو کارور",
            "SP NARROW Trimmed Recessed Linear Light": (
                "چراغ خطی توکار لبه‌دار اس‌پی نرو"
            ),
            "MAGNETO LARGE DOT LINEAR": "چراغ خطی دات مگنتو لارج",
            "Cylindra COB Surface Light": "چراغ روکار سی‌او‌بی سیلیندرا",
        }
        for source, expected in examples.items():
            with self.subTest(source=source):
                self.assertEqual(translate_catalog_name(source), expected)

    def test_orders_components_without_calling_them_lights(self):
        examples = {
            "MAGNETO LARGE RECESSED TRACK TRIMLESS": (
                "ریل توکار بدون لبه مگنتو لارج"
            ),
            "1ph track power connector": "کانکتور پاور ریل 1PH",
            "Corner Profile": "پروفایل کرنر",
        }
        for source, expected in examples.items():
            with self.subTest(source=source):
                self.assertEqual(translate_catalog_name(source), expected)
