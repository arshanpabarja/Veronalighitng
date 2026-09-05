from django import template

from Products.services.catalog_localization import catalog_text_fa


register = template.Library()


@register.filter(name="catalog_fa")
def catalog_fa(value):
    """Render human-readable catalog text in Persian."""
    return catalog_text_fa(value)
