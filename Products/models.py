from django.db import models
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator
from django.urls import reverse
import os


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    number = models.IntegerField(unique=True, blank=True, null=True)
    parent = models.ForeignKey(
        'self',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='children'
    )
    icon = models.FileField('ایکون', blank=True, null=True, upload_to='icons/')
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    meta_title = models.CharField(
        max_length=60,
        blank=True,
        verbose_name='عنوان SEO',
        help_text='حداکثر ۶۰ کاراکتر — در صورت خالی بودن، نام دسته‌بندی استفاده می‌شود'
    )
    meta_description = models.TextField(
        blank=True,
        verbose_name='توضیح SEO',
        help_text='حداکثر ۱۶۰ کاراکتر — خلاصه‌ای که در نتایج گوگل نمایش داده می‌شود'
    )
    canonical_url = models.URLField(
        blank=True,
        verbose_name='URL کانونیکال',
        help_text='فقط در صورتی پر کنید که این صفحه محتوای تکراری دارد'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'دسته‌بندی'
        verbose_name_plural = 'دسته‌بندی‌ها'
        ordering = ['number']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._unique_slug(self.name)
        super().save(*args, **kwargs)

    def _unique_slug(self, name):
        base = slugify(name, allow_unicode=True)
        slug = base
        counter = 1
        while Category.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f'{base}-{counter}'
            counter += 1
        return slug

    def get_meta_title(self):
        """Fallback chain: meta_title → name"""
        return self.meta_title or self.name

    def get_meta_description(self):
        """Fallback chain: meta_description → description (truncated)"""
        return self.meta_description or self.description[:160]


    def __str__(self):
        return self.name


class Application(models.Model):
    name = models.CharField(max_length=200, verbose_name='نام کاربرد')
    slug = models.SlugField(unique=True, blank=True, verbose_name='اسلاگ')

    icon = models.FileField(upload_to='applications/icons/', blank=True, null=True, verbose_name='آیکون')
    cover_image = models.ImageField(upload_to='applications/images/', blank=True, null=True, verbose_name='تصویر کاور')
    cover_image_alt = models.CharField(
        max_length=125,
        blank=True,
        verbose_name='alt تصویر کاور',
        help_text='توضیح تصویر برای موتورهای جستجو و screen readerها'
    )

    short_description = models.CharField(max_length=300, blank=True, verbose_name='توضیح کوتاه')
    description = models.TextField(blank=True, verbose_name='توضیح کامل')

    is_active = models.BooleanField(default=True, verbose_name='فعال')
    sort_order = models.PositiveIntegerField(default=0, verbose_name='ترتیب نمایش')

    meta_title = models.CharField(
        max_length=60,
        blank=True,
        verbose_name='عنوان SEO',
        help_text='حداکثر ۶۰ کاراکتر'
    )
    meta_description = models.TextField(
        blank=True,
        verbose_name='توضیح SEO',
        help_text='حداکثر ۱۶۰ کاراکتر'
    )
    canonical_url = models.URLField(
        blank=True,
        verbose_name='URL کانونیکال',
        help_text='فقط در صورتی پر کنید که این صفحه محتوای تکراری دارد'
    )

    class Meta:
        verbose_name = 'کاربرد (Application)'
        verbose_name_plural = 'کاربردها'
        ordering = ['sort_order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._unique_slug(self.name)
        super().save(*args, **kwargs)

    def _unique_slug(self, name):
        base = slugify(name, allow_unicode=True)
        slug = base
        counter = 1
        while Application.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f'{base}-{counter}'
            counter += 1
        return slug

    def get_meta_title(self):
        return self.meta_title or self.name

    def get_meta_description(self):
        return self.meta_description or self.short_description or self.description[:160]

    def __str__(self):
        return self.name


class Family(models.Model):
    name = models.CharField(max_length=200, verbose_name='نام محصول', null=True, blank=True)
    slug = models.SlugField(unique=True, verbose_name='اسلاگ', null=True, blank=True)
    icon = models.ImageField(upload_to='Family', blank=True)
    number = models.IntegerField(blank=True, null=True)
    category = models.ForeignKey(
        Category,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='families',
        verbose_name='دسته‌بندی'
    )
    applications = models.ManyToManyField(
        Application, blank=True,
        related_name='families',
        verbose_name='کاربردها'
    )
    is_active = models.BooleanField(default=True, verbose_name='فعال', null=True, blank=True)
    subtitle = models.CharField(max_length=1000, verbose_name='زیرعنوان', null=True, blank=True)

    meta_title = models.CharField(
        max_length=60,
        verbose_name='عنوان SEO',
        null=True, blank=True,
        help_text='حداکثر ۶۰ کاراکتر'
    )
    meta_description = models.TextField(
        verbose_name='توضیح SEO',
        null=True, blank=True,
        help_text='حداکثر ۱۶۰ کاراکتر'
    )
    canonical_url = models.URLField(
        blank=True,
        verbose_name='URL کانونیکال',
        help_text='فقط در صورتی پر کنید که این صفحه محتوای تکراری دارد'
    )

    class Meta:
        verbose_name = 'برند'
        verbose_name_plural = 'برندها'
        ordering = ['number']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._unique_slug(self.name)
        super().save(*args, **kwargs)

    def _unique_slug(self, name):
        base = slugify(name, allow_unicode=True)
        slug = base
        counter = 1
        while Family.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f'{base}-{counter}'
            counter += 1
        return slug

    def get_meta_title(self):
        return self.meta_title or self.name

    def get_meta_description(self):
        return self.meta_description or self.subtitle or ''

    def __str__(self):
        return self.name


class Finish(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام فینیش')
    color = models.CharField(
        max_length=7,
        verbose_name='کد رنگ',
        help_text='کد هگز رنگ مثال: #C9A84C'
    )
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name = 'فینیش'
        verbose_name_plural = 'فینیش‌ها'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Dimension(models.Model):
    label = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='برچسب سایز',
        help_text='مثال: کوچک، متوسط، بزرگ، ۶۰×۶۰'
    )
    width = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, verbose_name='عرض (mm)')
    height = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, verbose_name='ارتفاع (mm)')
    depth = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, verbose_name='طول (mm)')
    weight = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name='وزن (kg)')

    class Meta:
        verbose_name = 'ابعاد'
        verbose_name_plural = 'ابعاد'
        ordering = ['label']

    def __str__(self):
        parts = [self.label]
        if self.width and self.height:
            parts.append(f'{self.width}×{self.height} mm')
        return ' | '.join(parts)


class ProductVariant(models.Model):
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='variants',
        verbose_name='محصول'
    )
    model_name = models.CharField(
        max_length=200,
        verbose_name='نام مدل',
        help_text='مثال: مدل A، کلاسیک، مدرن'
    )
    dimension = models.ForeignKey(
        Dimension,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        verbose_name='ابعاد / سایز'
    )
    wattage = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name='توان (وات)')
    lumens = models.PositiveIntegerField(null=True, blank=True, verbose_name='شار نوری (لومن)')
    color_temperature = models.PositiveIntegerField(null=True, blank=True, verbose_name='دمای رنگ (کلوین)')
    sku = models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        verbose_name='کد محصول (SKU)',
        help_text='کد یکتا برای این ترکیب'
    )
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    note = models.CharField(
        max_length=300,
        blank=True,
        verbose_name='یادداشت',
        help_text='هر توضیح اضافی برای این مدل/سایز'
    )

    class Meta:
        verbose_name = 'مدل / سایز'
        verbose_name_plural = 'مدل‌ها / سایزها'
        unique_together = ('product', 'model_name', 'dimension')
        ordering = ['model_name']

    def __str__(self):
        dimension_label = self.dimension.label if self.dimension else '—'
        return f'{self.product.name} | {self.model_name} | {dimension_label}'


class Installment(models.Model):
    STEPS_CHOICES = [
        ('1', 'step 1'),
        ('2', 'step 2'),
        ('3', 'step 3'),
        ('4', 'step 4'),
    ]

    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='installment',
        verbose_name='محصول'
    )
    name = models.CharField('تایتل', max_length=120, blank=True, null=True)
    step = models.CharField(max_length=10, choices=STEPS_CHOICES, blank=True, null=True, verbose_name='مرحله')
    description = models.CharField(max_length=355, verbose_name='توضیحات')

    class Meta:
        verbose_name = 'طریقه نصب'


class Product(models.Model):
    order = models.PositiveIntegerField(default=0, verbose_name='ترتیب نمایش', blank=True, null=True)
    LAMP_BASE_CHOICES = [
        ('E27', 'E27'),
        ('E14', 'E14'),
        ('GU10', 'GU10'),
        ('GU5.3', 'GU5.3'),
        ('B22', 'B22'),
        ('MR16', 'MR16'),
        ('G9', 'G9'),
        ('G4', 'G4'),
        ('other', 'سایر'),
    ]

    IP_RATING_CHOICES = [
        ('IP20', 'IP20 - فضای داخلی'),
        ('IP44', 'IP44 - مقاوم در برابر پاشش آب'),
        ('IP54', 'IP54 - مقاوم در برابر گرد و پاشش'),
        ('IP65', 'IP65 - ضد گرد و جت آب'),
        ('IP67', 'IP67 - ضد آب (غوطه‌وری کوتاه)'),
        ('IP68', 'IP68 - ضد آب کامل'),
    ]

    name = models.CharField(max_length=200, verbose_name='نام محصول')
    slug = models.SlugField(unique=True, blank=True, verbose_name='اسلاگ')
    category = models.ForeignKey(
        Category,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='products',
        verbose_name='دسته‌بندی'
    )
    family = models.ForeignKey(
        Family,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='products',
    )
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    subtitle = models.CharField(max_length=300, blank=True, verbose_name='زیرعنوان')
    description = models.TextField(blank=True, verbose_name='توضیح کوتاه')
    full_description = models.TextField(blank=True, verbose_name='توضیح کامل')
    # Technical specs
    wattage = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name='توان (وات)')
    lumens = models.PositiveIntegerField(null=True, blank=True, verbose_name='شار نوری (لومن)')
    color_temperature = models.PositiveIntegerField(null=True, blank=True, verbose_name='دمای رنگ (کلوین)')
    cri = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='شاخص رنگ‌دهی (CRI)')
    beam_angle = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='زاویه تابش (درجه)')
    voltage = models.CharField(max_length=50, blank=True, verbose_name='ولتاژ')
    ip_rating = models.CharField(max_length=10, choices=IP_RATING_CHOICES, blank=True, verbose_name='درجه حفاظت (IP)')
    dimmable = models.BooleanField(default=False, verbose_name='دیمر پذیر')
    lamp_base_type = models.CharField(max_length=20, choices=LAMP_BASE_CHOICES, blank=True, verbose_name='نوع سرپیچ')
    lifespan = models.PositiveIntegerField(null=True, blank=True, verbose_name='طول عمر (ساعت)')
    mounting_type = models.CharField(max_length=10, default='afds')
    finishes = models.ManyToManyField(Finish, blank=True, related_name='products', verbose_name='رنگ‌بندی / فینیش')

    # Images — alt text is required for SEO and accessibility
    image1 = models.ImageField(upload_to='products/', verbose_name='تصویر ۱')
    image1_alt = models.CharField(
        max_length=125,
        blank=True,
        verbose_name='alt تصویر ۱',
        help_text='توضیح تصویر برای موتورهای جستجو — حداکثر ۱۲۵ کاراکتر'
    )
    image2 = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name='تصویر ۲')
    image2_alt = models.CharField(max_length=125, blank=True, verbose_name='alt تصویر ۲')
    image3 = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name='تصویر ۳')
    image3_alt = models.CharField(max_length=125, blank=True, verbose_name='alt تصویر ۳')
    image4 = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name='تصویر ۴')
    image4_alt = models.CharField(max_length=125, blank=True, verbose_name='alt تصویر ۴')

    # SEO
    meta_title = models.CharField(
        max_length=60,
        blank=True,
        verbose_name='عنوان SEO',
        help_text='حداکثر ۶۰ کاراکتر — در صورت خالی بودن، نام محصول استفاده می‌شود'
    )
    meta_description = models.TextField(
        blank=True,
        verbose_name='توضیح SEO',
        help_text='حداکثر ۱۶۰ کاراکتر'
    )
    canonical_url = models.URLField(
        blank=True,
        verbose_name='URL کانونیکال',
        help_text='فقط در صورتی پر کنید که این صفحه محتوای تکراری دارد'
    )

    catelog = models.FileField('کاتالوگ', upload_to='catelogs/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'
        ordering = ['order']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._unique_slug(self.name)
        super().save(*args, **kwargs)

    def _unique_slug(self, name):
        base = slugify(name, allow_unicode=True)
        slug = base
        counter = 1
        while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f'{base}-{counter}'
            counter += 1
        return slug

    def get_meta_title(self):
        """Fallback chain: meta_title → name"""
        return self.meta_title or self.name

    def get_meta_description(self):
        """Fallback chain: meta_description → description (truncated)"""
        return self.meta_description or self.description[:160]

    def get_image1_alt(self):
        """Fallback to product name if alt is empty"""
        return self.image1_alt or self.name

    def __str__(self):
        return self.name


class Download(models.Model):
    """Model for downloadable files (datasheets, catalogs, manuals, etc.)"""

    FILE_TYPE_CHOICES = [
        ('pdf', 'PDF Document'),
        ('doc', 'Word Document'),
        ('xls', 'Excel Spreadsheet'),
        ('zip', 'ZIP Archive'),
        ('dwg', 'AutoCAD Drawing'),
        ('ies', 'IES Photometric File'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=200, verbose_name='عنوان')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    file = models.FileField(
        upload_to='downloads/%Y/%m/',
        validators=[FileExtensionValidator(
            allowed_extensions=['pdf', 'doc', 'docx', 'xls', 'xlsx', 'zip', 'rar', 'dwg', 'ies']
        )],
        verbose_name='فایل'
    )
    file_type = models.CharField(
        max_length=10,
        choices=FILE_TYPE_CHOICES,
        blank=True,
        verbose_name='نوع فایل',
        help_text='به صورت خودکار تشخیص داده می‌شود'
    )
    file_size = models.CharField(
        max_length=20,
        blank=True,
        editable=False,
        verbose_name='حجم فایل'
    )

    application = models.ForeignKey(
        'Application',
        on_delete=models.CASCADE,
        related_name='downloads',
        null=True, blank=True,
        verbose_name='کاربرد'
    )
    family = models.ForeignKey(
        'Family',
        on_delete=models.CASCADE,
        related_name='downloads',
        null=True, blank=True,
        verbose_name='برند'
    )
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='downloads',
        null=True, blank=True,
        verbose_name='محصول'
    )

    download_count = models.PositiveIntegerField(default=0, verbose_name='تعداد دانلود')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'فایل دانلودی'
        verbose_name_plural = 'فایل‌های دانلودی'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.file_type and self.file:
            ext = os.path.splitext(self.file.name)[1][1:].lower()
            for choice_value, _ in self.FILE_TYPE_CHOICES:
                if ext.startswith(choice_value):
                    self.file_type = choice_value
                    break
            if not self.file_type:
                self.file_type = 'other'

        if self.file:
            size = self.file.size
            if size < 1024:
                self.file_size = f"{size} B"
            elif size < 1024 * 1024:
                self.file_size = f"{size / 1024:.1f} KB"
            else:
                self.file_size = f"{size / (1024 * 1024):.1f} MB"

        super().save(*args, **kwargs)

    def increment_download_count(self):
        self.download_count += 1
        self.save(update_fields=['download_count'])


class Project(models.Model):
    # Core
    name             = models.CharField(max_length=200)
    slug             = models.SlugField(max_length=220, unique=True, blank=True)

    # Overview card fields
    location         = models.CharField(max_length=200, blank=True, help_text="e.g. Tehran, Iran")
    project_type     = models.CharField(max_length=200, blank=True, help_text="e.g. Commercial Complex")
    completion_year  = models.CharField(max_length=10, blank=True, help_text="e.g. 2025")
    application = models.ForeignKey(Application, on_delete=models.PROTECT, blank=True , null=True, related_name='projects')
    # Hero
    hero_image       = models.ImageField(
        upload_to="projects/heroes/",
        blank=True, null=True,
        help_text="Full-width hero background image."
    )

    # Intro section (below hero)
    intro_heading    = models.CharField(
        max_length=300, blank=True,
        help_text="Bold heading below the hero, e.g. 'Premium, Efficient Lighting…'"
    )
    intro_text       = models.TextField(blank=True, help_text="Paragraph below the intro heading.")

    # Overview section
    overview_text    = models.TextField(blank=True, help_text="Body text in the Overview section.")

    # About section (supports multiple paragraphs via HTML)
    about_content    = models.TextField(blank=True, help_text="About This Project section. HTML allowed.")

    # Products used (M2M to existing Product model)
# In Project model — replace the products M2M field
    products = models.ManyToManyField(
        "Product",          # same app, no label needed
        blank=True,
        related_name="projects",
        help_text="Products featured in this project."
    )


    # SEO
    meta_title       = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)

    # Ordering / visibility
    order            = models.PositiveSmallIntegerField(default=0, db_index=True)
    is_published     = models.BooleanField(default=False)

    class Meta:
        ordering        = ["order", "-completion_year", "name"]
        verbose_name        = "Project"
        verbose_name_plural = "Projects"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("products:project_detail", kwargs={"slug": self.slug})


class ProjectGalleryImage(models.Model):
    project  = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="gallery_images"
    )
    image    = models.ImageField(upload_to="projects/gallery/")
    alt_text = models.CharField(
        max_length=200, blank=True,
        help_text="Descriptive alt text for accessibility and SEO."
    )
    order    = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering        = ["order"]
        verbose_name        = "Gallery Image"
        verbose_name_plural = "Gallery Images"

    def __str__(self):
        return f"{self.project.name} — image {self.order}"


class ProjectDownload(models.Model):
    project     = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="downloads"
    )
    title       = models.CharField(max_length=200)
    description = models.CharField(max_length=300, blank=True)
    file        = models.FileField(upload_to="projects/downloads/")
    file_type   = models.CharField(
        max_length=20, blank=True,
        help_text="Display label, e.g. PDF, DWG."
    )
    file_size   = models.CharField(
        max_length=20, blank=True,
        help_text="Human-readable size, e.g. 4.2 MB."
    )
    order       = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering        = ["order", "title"]
        verbose_name        = "Project Download"
        verbose_name_plural = "Project Downloads"

    def __str__(self):
        return f"{self.project.name} — {self.title}"