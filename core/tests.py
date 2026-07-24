from django.test import TestCase

from .site_seo import SITE_SEO, validate_site_seo


class SiteSEOTests(TestCase):
    def test_reviewed_site_seo_is_complete_and_within_limits(self):
        validate_site_seo()
        self.assertEqual(len(SITE_SEO), 6)
