from django.db.models import Case, IntegerField, Prefetch, Value, When

from ..models import Category


MAGNETIC_CHILD_SLUGS = (
    "magent-large4cm-family",
    "magent-small-family",
    "magnet-curve",
    "mmagne-tbelt",
)


def order_navigation_children(queryset):
    """Keep magnetic systems first in the requested commercial order."""
    priority_cases = [
        When(slug=slug, then=Value(position))
        for position, slug in enumerate(MAGNETIC_CHILD_SLUGS)
    ]
    return queryset.annotate(
        _navigation_priority=Case(
            *priority_cases,
            default=Value(len(MAGNETIC_CHILD_SLUGS)),
            output_field=IntegerField(),
        ),
    ).order_by("_navigation_priority", "number", "order", "pk")


def navigation_categories():
    """Return the shared navbar category tree with consistently ordered children."""
    return Category.objects.filter(
        is_active=True,
        parent__isnull=True,
    ).exclude(slug="").prefetch_related(
        "products",
        Prefetch(
            "children",
            queryset=order_navigation_children(
                Category.objects.filter(is_active=True),
            ),
        ),
    )
