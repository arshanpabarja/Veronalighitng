from django.contrib import admin
from django.utils.html import format_html, mark_safe
from .models import Project, ProjectGalleryImage, ProjectDownload

from .models import (
    Application, Category, Finish, Family,
    Dimension, ProductVariant, Product,
    Installment, Download
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display        = ['name', 'parent', 'is_active', 'thumbnail_preview', 'created_at']
    list_filter         = ['parent', 'is_active']
    search_fields       = ['name', 'description']
    ordering            = ['name']
    prepopulated_fields = {'slug': ('name',)}

    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('name', 'slug', 'parent', 'icon', 'is_active', 'number')
        }),
        ('محتوا', {
            'fields': ('description',)
        }),
        ('تنظیمات SEO', {
            'classes': ('collapse',),
            'fields': ('meta_title', 'meta_description', 'canonical_url')
        }),
    )

    def thumbnail_preview(self, obj):
        if obj.icon:
            return format_html('{}', obj.icon)
        return '—'
    thumbnail_preview.short_description = 'تصویر'


@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    list_display        = ['id', 'number','name', 'category', 'logo_preview', 'get_applications', 'is_active']
    list_filter         = ['is_active', 'category']
    search_fields       = ['name']
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal   = ['applications']
    ordering = ['number']
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('name', 'slug', 'applications', 'category','number', 'is_active', 'subtitle')
        }),
        ('تصویر', {
            'fields': ('icon',)
        }),
        ('تنظیمات SEO', {
            'classes': ('collapse',),
            'fields': ('meta_title', 'meta_description', 'canonical_url')
        }),
    )

    def get_applications(self, obj):
        return ", ".join([app.name for app in obj.applications.all()])
    get_applications.short_description = 'کاربردها'

    def logo_preview(self, obj):
        if obj.icon:
            return format_html(
                '<img src="{}" style="width:48px; height:48px; '
                'object-fit:contain; border-radius:4px;" />',
                obj.icon.url
            )
        return '—'
    logo_preview.short_description = 'لوگو'


@admin.register(Finish)
class FinishAdmin(admin.ModelAdmin):
    list_display        = ['name', 'color_preview', 'color', 'slug']
    search_fields       = ['name']
    prepopulated_fields = {'slug': ('name',)}

    def color_preview(self, obj):
        return format_html(
            '<div style="width:32px; height:32px; border-radius:50%; '
            'background:{}; border:1px solid #ccc; display:inline-block;"></div>',
            obj.color
        )
    color_preview.short_description = 'رنگ'


@admin.register(Dimension)
class DimensionAdmin(admin.ModelAdmin):
    list_display  = ['label', 'width', 'height', 'depth', 'weight']
    search_fields = ['label']

    fieldsets = (
        ('برچسب', {
            'fields': ('label',)
        }),
        ('ابعاد (سانتی‌متر)', {
            'fields': (('width', 'height', 'depth'),)
        }),
        ('وزن', {
            'fields': ('weight',)
        }),
    )


class ProductVariantInline(admin.TabularInline):
    model            = ProductVariant
    extra            = 1
    fields           = ['model_name', 'dimension', 'wattage', 'lumens', 'color_temperature', 'sku', 'is_active', 'note']
    show_change_link = True


class ProductInstallmentInline(admin.TabularInline):
    model            = Installment
    extra            = 1
    fields           = ['step', 'name', 'description']
    show_change_link = True


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display  = ['product', 'model_name', 'dimension', 'sku', 'is_active']
    list_filter   = ['is_active', 'product']
    search_fields = ['model_name', 'sku', 'product__name']

    fieldsets = (
        ('محصول', {
            'fields': ('product',)
        }),
        ('مدل / سایز', {
            'fields': ('model_name', 'dimension', 'sku', 'is_active', 'note')
        }),
    )


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display        = ['name', 'is_active', 'sort_order']
    list_editable       = ['is_active', 'sort_order']
    prepopulated_fields = {'slug': ('name',)}
    search_fields       = ['name']

    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('name', 'slug', 'is_active', 'sort_order')
        }),
        ('محتوا', {
            'fields': ('short_description', 'description')
        }),
        ('تصویر', {
            'fields': ('icon', 'cover_image', 'cover_image_alt')
        }),
        ('تنظیمات SEO', {
            'classes': ('collapse',),
            'fields': ('meta_title', 'meta_description', 'canonical_url')
        }),
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display        = ['order',
        'name', 'category', 'family',
        'wattage', 'dimmable',
        'thumbnail_preview', 'is_active', 'updated_at'
    ]
    list_filter         = ['category', 'family', 'is_active', 'dimmable', 'lamp_base_type', 'finishes']
    search_fields       = ['name', 'subtitle', 'slug', 'description']
    ordering            = ['order']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields     = ['images_preview']
    filter_horizontal   = ['finishes']
    inlines             = [ProductInstallmentInline, ProductVariantInline]

    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('name', 'slug', 'category', 'family', 'is_active', 'order')
        }),
        ('محتوا', {
            'fields': ('subtitle', 'description', 'full_description', 'catelog')
        }),
        ('مشخصات فنی نور', {
            'classes': ('collapse',),
            'fields': (
                ('wattage', 'lumens'),
                ('color_temperature', 'cri'),
                ('beam_angle', 'voltage'),
                ('ip_rating', 'lamp_base_type'),
                ('dimmable', 'lifespan'),
            )
        }),
        ('رنگ‌بندی / فینیش', {
            'fields': ('finishes',)
        }),
        ('تصویر اصلی', {
            'fields': ('image1', 'image1_alt')
        }),
        ('تصویر دوم', {
            'classes': ('collapse',),
            'fields': ('image2', 'image2_alt')
        }),
        ('تصویر سوم', {
            'classes': ('collapse',),
            'fields': ('image3', 'image3_alt')
        }),
        ('تصویر چهارم', {
            'classes': ('collapse',),
            'fields': ('image4', 'image4_alt')
        }),
        ('پیش‌نمایش تصاویر', {
            'fields': ('images_preview',)
        }),
        ('تنظیمات SEO', {
            'classes': ('collapse',),
            'fields': ('meta_title', 'meta_description', 'canonical_url')
        }),
    )

    def thumbnail_preview(self, obj):
        if obj.image1:
            return format_html(
                '<img src="{}" style="width:60px; height:60px; '
                'object-fit:cover; border-radius:6px;" />',
                obj.image1.url
            )
        return '—'
    thumbnail_preview.short_description = 'تصویر'

    def images_preview(self, obj):
        images   = [obj.image1, obj.image2, obj.image3, obj.image4]
        existing = [img for img in images if img]

        if not existing:
            return 'هیچ تصویری آپلود نشده'

        # build each <img> safely through format_html, collect as a list
        parts = [
            format_html(
                '<img src="{}" style="width:130px; height:130px; '
                'object-fit:cover; border-radius:8px; margin:4px;" />',
                img.url
            )
            for img in existing
        ]
        # mark_safe is fine here — every part was escaped by format_html
        return format_html(
            '<div style="display:flex; flex-wrap:wrap; gap:4px;">{}</div>',
            mark_safe(''.join(parts))
        )
    images_preview.short_description = 'پیش‌نمایش همه تصاویر'


@admin.register(Download)
class DownloadAdmin(admin.ModelAdmin):
    list_display    = ['title', 'file_type', 'file_size', 'application', 'family', 'product', 'download_count', 'is_active', 'created_at']
    list_filter     = ['file_type', 'is_active', 'created_at', 'application']
    search_fields   = ['title', 'description']
    readonly_fields = ['file_size', 'download_count', 'created_at', 'updated_at']

    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('title', 'description', 'file', 'file_type')
        }),
        ('ارتباطات', {
            'fields': ('application', 'family', 'product')
        }),
        ('متادیتا', {
            'classes': ('collapse',),
            'fields': ('file_size', 'download_count', 'is_active', 'created_at', 'updated_at')
        }),
    )

# projects/admin.py




class ProjectGalleryImageInline(admin.TabularInline):
    model = ProjectGalleryImage
    extra = 1
    fields = ("image", "image_preview", "alt_text", "order")
    readonly_fields = ("image_preview",)
    ordering = ("order",)

    @admin.display(description="Preview")
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:60px;object-fit:cover;border-radius:4px;">',
                obj.image.url,
            )
        return "—"


class ProjectDownloadInline(admin.TabularInline):
    model = ProjectDownload
    extra = 1
    fields = ("title", "description", "file", "file_type", "file_size", "order")
    ordering = ("order",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display  = ("name", "location", "project_type", 'application', "completion_year", "is_published", "order")
    list_editable = ("is_published", "order")
    list_filter   = ("is_published", "project_type")
    search_fields = ("name", "location", "meta_title", "meta_description")
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ("products",)

    inlines = [ProjectGalleryImageInline, ProjectDownloadInline]

    fieldsets = (
        ("Core", {
            "fields": ("name", "slug", "is_published", "order"),
        }),
        ("Hero & Intro", {
            "fields": ("hero_image", "intro_heading", "intro_text"),
        }),
        ("Overview", {
            "fields": ("location", "project_type", "completion_year", "overview_text"),
        }),
        ("About", {
            "fields": ("about_content",),
        }),
        ("Products Used", {
            "fields": ("products",),
        }),
        ("SEO", {
            "classes": ("collapse",),
            "fields": ("meta_title", "meta_description"),
        }),
    )
