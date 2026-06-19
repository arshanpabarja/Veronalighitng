from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Min, Max, Q
from core.models import SiteSettings
from .models import (
    Category, Application, Family, Product, Project
)

# ---------------------
# Pagination helper
# ---------------------
def _paginate(request, qs, per_page=12):
    paginator = Paginator(qs, per_page)
    page_number = request.GET.get("page")
    return paginator.get_page(page_number)

# ---------------------
# Family-level filters
# ---------------------
def _apply_family_filters(request, families):
    applications = [a for a in request.GET.getlist("application") if a]
    family_slugs = [f for f in request.GET.getlist("product_family") if f]

    if applications:
        families = families.filter(
            Q(applications__slug__in=applications) |
            Q(applications__name__in=applications)
        ).distinct()

    if family_slugs:
        families = families.filter(
            Q(slug__in=family_slugs) |
            Q(name__in=family_slugs)
        )

    return families, {
        "selected_applications": applications,
        "selected_product_families": family_slugs,
    }

# ---------------------
# Product-level filters
# ---------------------
def _apply_product_filters(request, qs, include_family_filters=True):
    applications = [a for a in request.GET.getlist("application") if a]
    families     = [f for f in request.GET.getlist("product_family") if f]
    mounting     = [m for m in request.GET.getlist("mounting_type") if m]
    color_temps  = [c for c in request.GET.getlist("color_temp") if c]

    lumens       = [l for l in request.GET.getlist("lumens") if l]
    voltages     = [v for v in request.GET.getlist("voltage") if v]
    beam_angles  = [b for b in request.GET.getlist("beam_angle") if b]
    ip_ratings   = [i for i in request.GET.getlist("ip_rating") if i]
    cri          = [c for c in request.GET.getlist("cri") if c]
    certifications = [c for c in request.GET.getlist("certifications") if c]

    dimmable   = request.GET.get("dimmable")
    wattage_min = request.GET.get("wattage_min")
    wattage_max = request.GET.get("wattage_max")

    if include_family_filters:
        if applications:
            qs = qs.filter(
                Q(family__applications__slug__in=applications) |
                Q(family__applications__name__in=applications)
            ).distinct()

        if families:
            qs = qs.filter(
                Q(family__slug__in=families) |
                Q(family__name__in=families)
            )

    if mounting:
        qs = qs.filter(mounting_type__in=mounting)
    if color_temps:
        qs = qs.filter(color_temperature__in=color_temps)

    if lumens:
        qs = qs.filter(lumens__in=lumens)
    if voltages:
        qs = qs.filter(voltage__in=voltages)
    if beam_angles:
        qs = qs.filter(beam_angle__in=beam_angles)
    if ip_ratings:
        qs = qs.filter(ip_rating__in=ip_ratings)
    if cri:
        qs = qs.filter(cri__in=cri)
    if dimmable in ("yes", "no"):
        qs = qs.filter(dimmable=(dimmable == "yes"))
    if wattage_min:
        qs = qs.filter(wattage__gte=wattage_min)
    if wattage_max:
        qs = qs.filter(wattage__lte=wattage_max)

    # اگر certifications به صورت M2M دارید:
    # if certifications:
    #     qs = qs.filter(
    #         Q(certifications__slug__in=certifications) |
    #         Q(certifications__name__in=certifications)
    #     ).distinct()

    return qs, {
        "selected_applications": applications,
        "selected_product_families": families,
        "selected_mounting_types": mounting,
        "selected_color_temps": color_temps,
        "selected_lumens": lumens,
        "selected_voltages": voltages,
        "selected_beam_angles": beam_angles,
        "selected_ip_ratings": ip_ratings,
        "selected_cri": cri,
        "selected_certifications": certifications,
        "dimmable": dimmable,
        "wattage_min": wattage_min,
        "wattage_max": wattage_max,
    }

# ---------------------
# Filter context builder
# ---------------------
def _product_filter_context(products_qs):
    wattage_range = products_qs.aggregate(Min('wattage'), Max('wattage'))
    lumens_range  = products_qs.aggregate(Min('lumens'),  Max('lumens'))

    return {
        "wattage_min_db": wattage_range['wattage__min'],
        "wattage_max_db": wattage_range['wattage__max'],
        "lumens_min_db":  lumens_range['lumens__min'],
        "lumens_max_db":  lumens_range['lumens__max'],

        "available_applications": Application.objects.filter(
            is_active=True
        ).order_by("name"),

        "available_product_families": Family.objects.filter(
            is_active=True
        ).order_by("name"),

        "available_mounting_types": products_qs.values_list('mounting_type', flat=True).distinct().order_by('mounting_type'),
        "available_color_temps": products_qs.values_list('color_temperature', flat=True).distinct().order_by('color_temperature'),
        "available_lumens":        products_qs.values_list('lumens', flat=True).distinct().order_by('lumens'),
        "available_voltages":      products_qs.values_list('voltage', flat=True).distinct().order_by('voltage'),
        "available_beam_angles":   products_qs.values_list('beam_angle', flat=True).distinct().order_by('beam_angle'),
        "available_ip_ratings":    products_qs.values_list('ip_rating', flat=True).distinct().order_by('ip_rating'),
        "available_cri":           products_qs.values_list('cri', flat=True).distinct().order_by('cri'),
    }

def _has_product_filters(selected):
    return any([
        selected.get("selected_mounting_types"),
        selected.get("selected_color_temps"),
        selected.get("selected_lumens"),
        selected.get("selected_voltages"),
        selected.get("selected_beam_angles"),
        selected.get("selected_ip_ratings"),
        selected.get("selected_cri"),
        selected.get("selected_certifications"),
        selected.get("dimmable"),
        selected.get("wattage_min"),
        selected.get("wattage_max"),
    ])

# =========================================================
# Views
# =========================================================

def product_detail(request, cat_slug, child_slug, family_slug, slug):
    product = get_object_or_404(
        Product.objects.select_related('category', 'family')
                       .prefetch_related(
                           'finishes',
                           'installment',
                           'variants',
                           'variants__dimension',
                       ),
        slug=slug,
        is_active=True,
    )

    related_products = Product.objects.filter(
        family=product.family,
        is_active=True,
    ).exclude(pk=product.pk).prefetch_related('finishes')[:4]

    if not related_products.exists():
        related_products = Product.objects.filter(
            category=product.category,
            is_active=True,
        ).exclude(pk=product.pk).prefetch_related('finishes')[:4]

    context = {
        "product": product,
        "related_products": related_products,
        "meta_title": product.meta_title or product.name,
    }

    return render(request, "products/product_detail.html", context)


def application_list(request):
    applications = Application.objects.filter(is_active=True).order_by('sort_order', 'name')
    context = {
        'applications': applications,
        "site_settings": SiteSettings.get(),
    }
    return render(request, 'products/application_list.html', context)


def product_list(request):
    base_products = Product.objects.filter(is_active=True).select_related('category','family')
    products, selected = _apply_product_filters(request, base_products)

    page_obj = _paginate(request, products)

    context = {
        "products": page_obj.object_list,
        "page_obj": page_obj,
        "site_settings": SiteSettings.get(),
        "categories": Category.objects.filter(is_active=True, parent__isnull=True),
        **_product_filter_context(base_products),  # ✅ base_qs
        **selected,
    }
    return render(request, "products/product_list.html", context)


def category_detail(request, cat_slug):
                
    category = get_object_or_404(Category, slug=cat_slug, is_active=True, parent__isnull=True)
    children = Category.objects.filter(parent=category, is_active=True).order_by("order")

    if children.exists():
        families = Family.objects.filter(
            Q(category__in=children) | Q(category=category),
            is_active=True
        ).distinct()
    else:
        families = Family.objects.filter(
            category=category,
            is_active=True
    )
    families = families.prefetch_related('applications')
    families, selected_family = _apply_family_filters(request, families)

    product_base_qs = Product.objects.filter(is_active=True, family__in=families)
    product_qs, selected_prod = _apply_product_filters(request, product_base_qs, include_family_filters=False)

    if _has_product_filters(selected_prod):
        families = families.filter(products__in=product_qs).distinct()

    page_obj = _paginate(request, families)

    context = {
    "category": category,
    "children": children,
    "families": page_obj.object_list,
    "page_obj": page_obj,
    "meta_title": category.meta_title or category.name,
    "categories": Category.objects.filter(
        is_active=True, parent__isnull=True, slug__isnull=False
    ).exclude(slug='').order_by("number"),
    **_product_filter_context(product_base_qs),
    **selected_family,
    **selected_prod,
}

    return render(request, "products/category_detail.html", context)


def child_detail(request, cat_slug, child_slug):
    parent = get_object_or_404(Category, slug=cat_slug, is_active=True, parent__isnull=True)
    child  = get_object_or_404(Category, slug=child_slug, is_active=True, parent=parent)

    families = Family.objects.filter(category=child, is_active=True).prefetch_related('applications')
    families, selected_family = _apply_family_filters(request, families)

    product_base_qs = Product.objects.filter(is_active=True, family__in=families)
    product_qs, selected_prod = _apply_product_filters(request, product_base_qs, include_family_filters=False)

    if _has_product_filters(selected_prod):
        families = families.filter(products__in=product_qs).distinct()

    page_obj = _paginate(request, families)

    context = {
        "parent": parent,
        "child": child,
        "families": page_obj.object_list,
        "page_obj": page_obj,
        "meta_title": child.meta_title or child.name,
        "categories": Category.objects.filter(is_active=True, parent__isnull=True),
        **_product_filter_context(product_base_qs),  # ✅ base_qs
        **selected_family,
        **selected_prod,
    }
    return render(request, "products/child_detail.html", context)


def application_detail(request, slug):
    app = get_object_or_404(Application, slug=slug, is_active=True)

    families = Family.objects.filter(applications=app, is_active=True).prefetch_related('applications')
    families, selected_family = _apply_family_filters(request, families)

    product_base_qs = Product.objects.filter(is_active=True, family__in=families)
    product_qs, selected_prod = _apply_product_filters(request, product_base_qs, include_family_filters=False)

    if _has_product_filters(selected_prod):
        families = families.filter(products__in=product_qs).distinct()

    page_obj = _paginate(request, families)

    context = {
        "application": app,
        "families": page_obj.object_list,
        "page_obj": page_obj,
        "meta_title": app.meta_title or app.name,
        "categories": Category.objects.filter(is_active=True, parent__isnull=True),
        **_product_filter_context(product_base_qs),  # ✅ base_qs
        **selected_family,
        **selected_prod,
    }
    return render(request, "products/application_detail.html", context)


def family_detail(request, cat_slug, child_slug, family_slug):
    parent = get_object_or_404(Category, slug=cat_slug, is_active=True, parent__isnull=True)
    child  = get_object_or_404(Category, slug=child_slug, is_active=True, parent=parent)
    family = get_object_or_404(Family, slug=family_slug, is_active=True, category=child)

    base_products = Product.objects.filter(is_active=True, family=family)
    products, selected = _apply_product_filters(request, base_products, include_family_filters=False)

    page_obj = _paginate(request, products)

    context = {
        "parent": parent,
        "child": child,
        "family": family,
        "products": page_obj.object_list,
        "page_obj": page_obj,
        "meta_title": family.meta_title or family.name,
        "categories": Category.objects.filter(is_active=True, parent__isnull=True),
        **_product_filter_context(base_products),  # ✅ base_qs
        **selected,
    }
    return render(request, "products/family_detail.html", context)


def project_list(request):
    qs = Project.objects.filter(is_published=True).prefetch_related('gallery_images')

    # Search
    q = request.GET.get('q', '').strip()
    if q:
        qs = qs.filter(
            Q(name__icontains=q) |
            Q(location__icontains=q) |
            Q(project_type__icontains=q)
        )

    # Filter by type
    project_type = request.GET.get('type', '').strip()
    if project_type:
        qs = qs.filter(project_type__iexact=project_type)

    # Filter by city
    city = request.GET.get('city', '').strip()
    if city:
        qs = qs.filter(location__icontains=city)

    # Sort
    sort = request.GET.get('sort', 'newest')
    if sort == 'oldest':
        qs = qs.order_by('completion_year', 'order', 'name')
    else:
        qs = qs.order_by('-completion_year', 'order', 'name')

    # Distinct project types and cities for filter dropdowns
    all_types = (
        Project.objects.filter(is_published=True)
        .exclude(project_type='')
        .values_list('project_type', flat=True)
        .distinct()
        .order_by('project_type')
    )
    all_cities = (
        Project.objects.filter(is_published=True)
        .exclude(location='')
        .values_list('location', flat=True)
        .distinct()
        .order_by('location')
    )

    # Pagination
    paginator = Paginator(qs, 9)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'projects/project_list.html', {
        'page_obj': page_obj,
        'projects': page_obj.object_list,
        'total_count': paginator.count,
        'all_types': all_types,
        'all_cities': all_cities,
        # preserve filter state
        'q': q,
        'selected_type': project_type,
        'selected_city': city,
        'sort': sort,
    })



def project_detail(request, slug):
    project = get_object_or_404(
        Project.objects.prefetch_related(
            "gallery_images",
            "downloads",
            "products",
            "products__category",  # needed for the "View Products" category link
        ),
        slug=slug,
        is_published=True,
    )
    return render(request, "projects/project_detail.html", {"project": project})




def family_detail_no_child(request, cat_slug, family_slug):
    category = get_object_or_404(
        Category,
        slug=cat_slug,
        is_active=True
    )

    family = get_object_or_404(
        Family,
        slug=family_slug,
        is_active=True,
        category=category
    )

    base_products = Product.objects.filter(
        is_active=True,
        family=family
    )

    products, selected = _apply_product_filters(
        request,
        base_products,
        include_family_filters=False
    )

    page_obj = _paginate(request, products)

    context = {
        "category": category,
        "family": family,
        "products": page_obj.object_list,
        "page_obj": page_obj,
        "meta_title": family.meta_title or family.name,
        "categories": Category.objects.filter(
            is_active=True,
            parent__isnull=True
        ),
        **_product_filter_context(base_products),
        **selected,
    }

    return render(
        request,
        "products/family_detail.html",
        context
    )



def product_detail_no_child(request, cat_slug, family_slug, slug):
    category = get_object_or_404(
        Category,
        slug=cat_slug,
        is_active=True
    )

    family = get_object_or_404(
        Family,
        slug=family_slug,
        is_active=True,
        category=category
    )

    product = get_object_or_404(
        Product.objects.select_related('category', 'family')
        .prefetch_related(
            'finishes',
            'installment',
            'variants',
            'variants__dimension',
        ),
        slug=slug,
        family=family,
        is_active=True,
    )

    related_products = Product.objects.filter(
        family=family,
        is_active=True,
    ).exclude(pk=product.pk)[:4]

    context = {
        "category": category,
        "family": family,
        "product": product,
        "related_products": related_products,
        "meta_title": product.meta_title or product.name,
    }

    return render(request, "products/product_detail.html", context)



def search(request):
    query = request.GET.get('q', '').strip()
    
    if not query:
        context = {
            "query": "",
            "products": [],
            "page_obj": None,
            "meta_title": "Search Products",
        }
        return render(request, "products/search.html", context)
    
    products = Product.objects.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query) |
        Q(family__name__icontains=query) |
        Q(category__name__icontains=query),
        is_active=True
    ).select_related('category', 'family').prefetch_related('finishes')
    page_obj = _paginate(request, products)

    context = {
        "query": query,
        "products": page_obj.object_list,
        "page_obj": page_obj,
        "meta_title": f"Search results for '{query}'",
    }
    return render(request, "products/search.html", context)