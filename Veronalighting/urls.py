from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from Products import views
from core.views import *

urlpatterns = [
    path('setting/', admin.site.urls),
    path('', index, name='home'),
    path('hesab-daryaft-pardakht/', hesab_daryaft_pardakht, name='hesab_daryaft_pardakht'),
    path('about/', about, name='about'),
    path('story/', story, name='story'),
    path('contact/', contact, name='contact'),
    path('services/', services, name='services'),
    path('news/', news_list, name='news_list'),
    path('news/<slug:slug>/', news_detail, name='news_detail'),
    path('search/', views.search, name='search'),
    path('', include('Products.urls', namespace='products')),
]

# برای serve کردن media در development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = "core.views.custom_404_view"