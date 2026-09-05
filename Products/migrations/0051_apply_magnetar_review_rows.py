from django.db import migrations


MAGNETIC_SYSTEM_DESCRIPTION_FA = (
    "سیستم روشنایی مگنت (Magnetic Lighting System)\n\n"
    "۱. نسل جدید نورپردازی\n"
    "سیستم مگنت یکی از مدرن‌ترین روش‌های نورپردازی در فضاهای داخلی است. "
    "این سیستم به‌جای چراغ‌های ثابت، بر پایه یک ریل مغناطیسی طراحی شده است. "
    "هدف آن ایجاد نورپردازی زیبا، منعطف و قابل تغییر، متناسب با نیاز فضاست.\n\n"
    "۲. ساختار مبتنی بر ریل مغناطیسی کم‌ولتاژ و ایمن\n"
    "سیستم از یک ریل آلومینیومی تشکیل شده که مسیر انتقال برق و محل نصب چراغ‌ها را فراهم می‌کند. "
    "چراغ‌ها با اتصال مغناطیسی روی ریل قرار می‌گیرند. طراحی با ولتاژ پایین باعث افزایش ایمنی و "
    "امکان استفاده از چراغ‌های متنوع در فضاهای مختلف، از جمله دیوارهای مهدکودک و پت‌شاپ، می‌شود.\n\n"
    "۳. نصب آسان و بدون محدودیت\n"
    "چراغ‌ها بدون نیاز به ابزار تخصصی روی ریل نصب یا از آن جدا می‌شوند. جای چراغ‌ها را می‌توان در "
    "هر زمان تغییر داد و تعداد یا نوع آن‌ها را متناسب با نیاز پروژه تنظیم کرد.\n\n"
    "۴. انعطاف‌پذیری در طراحی نور\n"
    "سیستم مگنت به طراح اجازه می‌دهد نور را مطابق تغییرات دکوراسیون تنظیم کند و انواع چراغ‌های "
    "اسپات، خطی، آویز و دکوراتیو را در یک سیستم ترکیب نماید.\n\n"
    "۵. هماهنگ با معماری مدرن\n"
    "ظاهر مینیمال و خطوط ظریف ریل باعث می‌شود سیستم با سبک‌های مدرن، مینیمال و لوکس هماهنگ باشد. "
    "به‌جای دیده‌شدن تجهیزات روشنایی، تمرکز روی اثر نور در فضا قرار می‌گیرد."
)


def apply_review_rows(apps, schema_editor):
    Application = apps.get_model("Products", "Application")
    Category = apps.get_model("Products", "Category")
    Family = apps.get_model("Products", "Family")
    Product = apps.get_model("Products", "Product")

    category_order = (
        "magent-large4cm-family",
        "magent-small-family",
        "magnet-curve",
        "magnet-flexi",
        "mmagne-tbelt",
        "magnet-super-slim",
    )
    for position, slug in enumerate(category_order, start=1):
        Category.objects.filter(slug=slug).update(order=position)

    large_family_order = (
        "magnet-track",
        "magneto-linear",
        "magneto-dot-linear",
        "magneto-rotate-linear",
        "magneto-rotate-dot-linear",
        "magneto-angle-linear",
        "magneto-angle-dot-linear",
    )
    for position, slug in enumerate(large_family_order, start=1):
        Family.objects.filter(slug=slug).update(number=position)

    Product.objects.filter(
        slug__in=(
            "magnetar-large-ressed-track-trimless",
            "magnetar-large-surface-pendant-track",
        )
    ).update(
        description_fa=(
            "سیستم ریل مگنتی ۴۸ ولت با نصب ماژولار، ایمن و بدون ابزار؛ "
            "مناسب نورپردازی منعطف در معماری مدرن."
        ),
        full_description_fa=MAGNETIC_SYSTEM_DESCRIPTION_FA,
        voltage="48V DC",
    )

    office = Application.objects.filter(slug="office").first()
    if office:
        empty_magnetic_families = Family.objects.filter(
            category__parent__slug="low-voltage-magneto",
            products__isnull=False,
            applications__isnull=True,
        ).distinct()
        for family in empty_magnetic_families:
            family.applications.add(office)


class Migration(migrations.Migration):

    dependencies = [
        ("Products", "0050_assign_remaining_hover_images"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="category",
            options={
                "ordering": ["order", "number"],
                "verbose_name": "دسته‌بندی",
                "verbose_name_plural": "دسته‌بندی‌ها",
            },
        ),
        migrations.RunPython(apply_review_rows, migrations.RunPython.noop),
    ]
