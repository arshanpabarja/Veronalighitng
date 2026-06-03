from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [

    # -------------------------------------------------
    # MAIN
    # -------------------------------------------------

    path('products/', views.product_list, name='product_list'),

    path('projects/', views.project_list, name='project_list'),
    path('projects/<slug:slug>/', views.project_detail, name='project_detail'),

    path('applications/', views.application_list, name='application_list'),
    path('applications/<slug:slug>/', views.application_detail, name='application_detail'),

    # -------------------------------------------------
    # CATEGORY
    # -------------------------------------------------

    path(
        '<slug:cat_slug>/',
        views.category_detail,
        name='category_detail'
    ),

    # -------------------------------------------------
    # CHILD CATEGORY
    # -------------------------------------------------

    path(
        '<slug:cat_slug>/c/<slug:child_slug>/',
        views.child_detail,
        name='child_detail'
    ),

    # -------------------------------------------------
    # FAMILY WITH CHILD
    # -------------------------------------------------

    path(
        '<slug:cat_slug>/c/<slug:child_slug>/<slug:family_slug>/',
        views.family_detail,
        name='family_detail'
    ),

    # -------------------------------------------------
    # PRODUCT WITH CHILD
    # -------------------------------------------------

    path(
        '<slug:cat_slug>/c/<slug:child_slug>/<slug:family_slug>/<slug:slug>/',
        views.product_detail,
        name='product_detail'
    ),

    # -------------------------------------------------
    # FAMILY WITHOUT CHILD
    # -------------------------------------------------

    path(
        '<slug:cat_slug>/<slug:family_slug>/',
        views.family_detail_no_child,
        name='family_detail_no_child'
    ),

    # -------------------------------------------------
    # PRODUCT WITHOUT CHILD
    # -------------------------------------------------

    path(
        '<slug:cat_slug>/<slug:family_slug>/<slug:slug>/',
        views.product_detail_no_child,
        name='product_detail_no_child'
    ),
]