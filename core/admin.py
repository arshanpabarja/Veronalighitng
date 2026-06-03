from django.contrib import admin

from .models import NewsArticle, NewsCategory, SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Home Page", {
            "fields": (
                "index_meta_title", "index_meta_description",
                "index_og_title", "index_og_description",
                "index_og_image", "index_canonical_url",
            )
        }),
        ("About Page", {
            "fields": (
                "about_meta_title", "about_meta_description",
                "about_og_title", "about_og_description",
                "about_og_image", "about_canonical_url",
            )
        }),
        ("Story Page", {
            "fields": (
                "story_meta_title", "story_meta_description",
                "story_og_title", "story_og_description",
                "story_og_image", "story_canonical_url",
            )
        }),
        ("Products List Page", {
            "fields": (
                "products_meta_title", "products_meta_description",
                "products_og_title", "products_og_description",
                "products_og_image", "products_canonical_url",
            )
        }),
        ("Applications List Page", {
            "fields": (
                "applications_meta_title", "applications_meta_description",
                "applications_og_title", "applications_og_description",
                "applications_og_image", "applications_canonical_url",
            )
        }),
        ("News List Page", {
            "fields": (
                "news_meta_title", "news_meta_description",
                "news_og_title", "news_og_description",
                "news_og_image", "news_canonical_url",
            )
        }),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "order")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("order", "name")


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "is_featured", "is_published", "published_at")
    list_filter = ("is_published", "is_featured", "category")
    list_editable = ("is_published", "is_featured")
    search_fields = ("title", "excerpt", "body")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"
    fieldsets = (
        ("Content", {
            "fields": (
                "title", "slug", "category",
                "excerpt", "body",
                "cover_image", "read_time",
            )
        }),
        ("Publishing", {
            "fields": ("is_published", "is_featured", "published_at")
        }),
        ("SEO", {
            "classes": ("collapse",),
            "fields": ("meta_title", "meta_description", "og_image")
        }),
    )



from django.contrib import admin
from django.urls import path
from django.http import HttpResponseRedirect
from django.utils.html import format_html

from .models import Invoice
from .models import InvoiceItem

from .services import generate_invoice_excel


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1

    fields = (
        "product",
        "invoice_name",
        "description",
        "quantity",
        "unit",
        "unit_price",
        "discount",
    )


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):

    inlines = [InvoiceItemInline]

    list_display = (
        "serial",
        "customer_name",
        "customer_phone",
        "date",
        "download_excel",
    )

    search_fields = (
        "serial",
        "customer_name",
        "customer_phone",
    )

    list_filter = (
        "province",
        "city",
        "date",
    )

    fieldsets = (
        (
            "اطلاعات فاکتور",
            {
                "fields": (
                    "serial",
                    "date",
                    "expire_date",
                )
            }
        ),
        (
            "اطلاعات مشتری",
            {
                "fields": (
                    "customer_name",
                    "customer_phone",
                    "province",
                    "city",
                    "address",
                )
            }
        ),
    )

    def get_urls(self):

        urls = super().get_urls()

        custom_urls = [
            path(
                "<int:invoice_id>/excel/",
                self.admin_site.admin_view(
                    self.export_excel
                ),
                name="invoice-export-excel",
            ),
        ]

        return custom_urls + urls

    def download_excel(self, obj):

        return format_html(
            '<a class="button" href="{}">دانلود اکسل</a>',
            f"{obj.id}/excel/"
        )

    download_excel.short_description = "خروجی"

    def export_excel(
        self,
        request,
        invoice_id
    ):

        from django.http import FileResponse
        from tempfile import NamedTemporaryFile

        invoice = Invoice.objects.prefetch_related(
            "items"
        ).get(
            id=invoice_id
        )

        temp = NamedTemporaryFile(
            suffix=".xlsx",
            delete=False
        )

        generate_invoice_excel(
            invoice,
            temp.name
        )

        return FileResponse(
            open(temp.name, "rb"),
            as_attachment=True,
            filename=f"invoice_{invoice.serial}.xlsx"
        )