# context_processors.py
from .models import Category, Application


def navbar_categories(request):
    """
    این context processor در تمام تمپلیت‌ها
    متغیر categories را در دسترس قرار می‌دهد
    """
    categories = Category.objects.filter(
        is_active=True,
        parent=None
    ).prefetch_related('products')

    applications = Application.objects.filter(
        is_active=True,
    )
    return {
        'categories': categories,
        'applications': applications,
    }

