from django.test import TestCase
from django.utils.translation import override

from core.business_identity import BUSINESS_IDENTITY

from .models import Category, Dimension, Family, Product, ProductVariant, Project
from .services.catalog_localization import catalog_text_fa


class RequestedSiteUpdatesTests(TestCase):
    def setUp(self):
        self.parent = Category.objects.create(
            name="Magnetic",
            name_fa="مگنتی",
            name_en="Magnetic",
            slug="magnetic-scroll-test",
            number=9001,
        )
        self.child = Category.objects.create(
            name="Magnet Large",
            name_fa="مگنت بزرگ",
            name_en="Magnet Large",
            slug="magnet-large-scroll-test",
            number=9002,
            order=1,
            parent=self.parent,
        )
        self.sibling = Category.objects.create(
            name="Magnet Small",
            name_fa="مگنت کوچک",
            name_en="Magnet Small",
            slug="magnet-small-scroll-test",
            number=9003,
            order=2,
            parent=self.parent,
        )
        self.family = Family.objects.create(
            name="Magnet Track",
            name_fa="ریل مگنتی",
            name_en="Magnet Track",
            slug="magnet-track-translation-test",
            number=9001,
            category=self.child,
        )
        self.product = Product.objects.create(
            name="Magnet Rail",
            name_fa="ریل مگنتی",
            name_en="Magnet Rail",
            slug="magnet-rail-translation-test",
            category=self.child,
            family=self.family,
            image1="products/test.jpg",
        )
        dimension = Dimension.objects.create(
            label="Verona-3-1 | 400 × 4 × 8 cm",
            width=80,
            height=40,
            depth=4000,
        )
        ProductVariant.objects.create(
            product=self.product,
            model_name="Magnetar Surface & Pendant Wide Rail",
            dimension=dimension,
            note=(
                "Length is customizable. Color temperature and body color "
                "are customized to customer requirements."
            ),
        )
        Project.objects.create(
            name="Hormozan Tower Residence",
            name_fa="برج هرمزان",
            name_en="Hormozan Tower Residence",
            slug="hormozan-tower-residence",
            hero_image="projects/heroes/hormozan-test.jpg",
            order=1,
            is_published=True,
        )
        Project.objects.create(
            name="Gold Shop",
            name_fa="طلا فروشی",
            name_en="Gold Shop",
            slug="tl-frosh",
            hero_image="projects/heroes/gold-shop-test.jpg",
            order=3,
            is_published=True,
        )
        Project.objects.create(
            name="Diamond Boutique",
            name_fa="بوتیک الماس",
            name_en="Diamond Boutique",
            slug="diamond-boutique",
            hero_image="projects/heroes/diamond-test.jpg",
            order=2,
            is_published=True,
        )
        Project.objects.create(
            name="Private Villa",
            name_fa="ویلای خصوصی",
            name_en="Private Villa",
            slug="private-villa",
            hero_image="projects/heroes/villa-test.jpg",
            order=4,
            is_published=True,
        )

    def test_contact_phones_are_visible_in_footer_about_and_contact_pages(self):
        phone_keys = (
            "telephone_e164",
            "telephone_secondary_e164",
            "telephone_tertiary_e164",
        )
        for path, expected_count in (("/", 1), ("/about/", 2), ("/contact/", 2)):
            response = self.client.get(path)
            for phone_key in phone_keys:
                with self.subTest(path=path, phone_key=phone_key):
                    self.assertContains(
                        response,
                        f'tel:{BUSINESS_IDENTITY[phone_key]}',
                        count=expected_count,
                    )
        contact_response = self.client.get("/contact/")
        self.assertContains(contact_response, "آقای تقی‌زاده")

    def test_subcategory_links_land_on_families_section(self):
        category_response = self.client.get(self.parent.get_absolute_url())
        child_response = self.client.get(self.child.get_absolute_url())

        self.assertContains(
            category_response,
            f'href="{self.child.get_absolute_url()}#families"',
        )
        self.assertContains(
            child_response,
            f'href="{self.sibling.get_absolute_url()}#families"',
        )
        self.assertContains(child_response, 'id="families"')
        self.assertContains(child_response, "scroll-mt-24")

    def test_homepage_uses_no_light_before_and_completed_after_images(self):
        response = self.client.get("/")

        self.assertContains(response, "data-project-slug=", count=4)
        self.assertContains(response, "lg:grid-cols-3")
        self.assertContains(response, "hormozan-before-lighting-ai.png")
        self.assertContains(response, "diamond-boutique-before-no-lights-ai.png")
        self.assertContains(response, "diamond-boutique-after-ai.png")
        self.assertContains(response, "gold-shop-before-lighting-ai.png")
        self.assertContains(response, "private-villa-before-lighting-ai.png")
        self.assertContains(response, "/projects/hormozan-tower-residence/")
        self.assertContains(response, "/projects/diamond-boutique/")
        self.assertContains(response, "/projects/tl-frosh/")
        self.assertContains(response, "/projects/private-villa/")
        self.assertContains(response, "برج هرمزان")
        self.assertContains(response, "طلا فروشی")

    def test_concept_design_is_scoped_to_main_content(self):
        homepage = self.client.get("/")
        product_index = self.client.get("/products/")

        self.assertContains(homepage, 'class="main-padding verona-main"')
        self.assertContains(homepage, "css/verona-concept.css")
        self.assertContains(homepage, 'class="home-concept"')
        self.assertContains(homepage, "home-project-track")
        self.assertContains(homepage, "home-card-index", count=6)
        self.assertContains(product_index, "concept-category-visual")

    def test_magnetic_children_use_requested_navigation_order(self):
        magnetic = Category.objects.create(
            name="Magnetic Products",
            name_fa="چراغ مگنتی",
            name_en="Magnetic Products",
            slug="low-voltage-magneto",
            number=9010,
        )
        requested_children = (
            ("Magnet 4 cm", "magent-large4cm-family", 9050),
            ("Magnet 2 cm", "magent-small-family", 9040),
            ("Magnet Curve", "magnet-curve", 9030),
            ("Magnet Belt", "mmagne-tbelt", 9020),
            ("Magnet Flexi", "magnet-flexi", 9011),
        )
        for position, (name, slug, number) in enumerate(requested_children, start=1):
            Category.objects.create(
                name=name,
                name_fa=name,
                name_en=name,
                slug=slug,
                number=number,
                order=10 - position,
                parent=magnetic,
            )

        homepage_html = self.client.get("/").content.decode()
        positions = [
            homepage_html.index(f"/{magnetic.slug}/c/{slug}/")
            for _, slug, _ in requested_children
        ]
        self.assertEqual(positions, sorted(positions))

        detail_response = self.client.get(magnetic.get_absolute_url())
        self.assertEqual(
            list(detail_response.context["children"].values_list("slug", flat=True)),
            [slug for _, slug, _ in requested_children],
        )

    def test_models_and_sizes_are_localized_on_persian_product_pages(self):
        with override("fa"):
            response = self.client.get(self.product.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "مگنتار ریل عریض روکار و آویز")
        self.assertContains(response, "ورونا-3-1 | 400 × 4 × 8 سانتی‌متر")
        self.assertContains(response, "طول قابل سفارشی‌سازی است")
        self.assertContains(
            response,
            "دمای رنگ و رنگ بدنه مطابق نیاز مشتری سفارشی‌سازی می‌شوند",
        )
        self.assertNotContains(response, "Length is customizable")

    def test_catalog_localizer_handles_lowercase_length_phrase(self):
        self.assertEqual(
            catalog_text_fa("Cut-out 5 cm; length is customizable."),
            "ابعاد برش 5 سانتی‌متر؛ طول قابل سفارشی‌سازی است.",
        )
