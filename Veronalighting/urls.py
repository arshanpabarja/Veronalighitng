from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import *    

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='home'),
    path('about/', about, name='about'),
    path('story/', story, name='story'),
    path('news/', news_list, name='news_list'),
    path('news/<slug:slug>/', news_detail, name='news_detail'),
    path('', include('Products.urls', namespace='products')),
]

# برای serve کردن media در development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
