from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from Products.models import Product, Category
from .models import SiteSettings, NewsCategory, NewsArticle

def index(request):
    context = {"site_settings": SiteSettings.get()}
    return render(request, 'index.html', context)

def about(request):
    context = {"site_settings": SiteSettings.get()}
    return render(request, 'company/about.html', context)

def story(request):
    context = {"site_settings": SiteSettings.get()}
    return render(request, 'company/story.html', context)

def news_list(request):
    category_slug = request.GET.get('category')
    articles = NewsArticle.objects.filter(is_published=True).select_related('category')

    if category_slug:
        articles = articles.filter(category__slug=category_slug)

    featured = NewsArticle.objects.filter(is_published=True, is_featured=True).select_related('category').first()
    # Exclude featured from the grid
    if featured:
        articles = articles.exclude(pk=featured.pk)

    paginator = Paginator(articles, 6)
    page = paginator.get_page(request.GET.get('page'))

    context = {
        "site_settings": SiteSettings.get(),
        "category": NewsCategory.objects.all(),
        "featured": featured,
        "page_obj": page,
        "active_category": category_slug or '',
    }
    return render(request, 'news/news_list.html', context)



def news_detail(request, slug):
    article = get_object_or_404(NewsArticle, slug=slug, is_published=True)

    related = (
        NewsArticle.objects
        .filter(is_published=True)
        .exclude(pk=article.pk)
        .select_related('category')
    )
    if article.category:
        # Prefer same-category articles, fall back to latest
        related = related.filter(category=article.category)

    related = related[:3]

    context = {
        "site_settings": SiteSettings.get(),
        "article": article,
        "related": related,
    }
    return render(request, 'news/news_detail.html', context)
