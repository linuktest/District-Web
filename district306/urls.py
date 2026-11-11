"""
URL configuration for Leo District 306 D3 Web Portal.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from apps.portal.seo import StaticViewSitemap, robots_txt

urlpatterns = [
    path('admin/', admin.site.urls),
    path('robots.txt', robots_txt, name='robots'),
    path('sitemap.xml', sitemap, {'sitemaps': {'static': StaticViewSitemap}}, name='sitemap'),
    path('', include('apps.portal.urls')),
    path('academy/', include('apps.academy.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Customize admin site header
admin.site.site_header = "Leo District 306 D3 — Administration"
admin.site.site_title = "District 306 D3 Admin"
admin.site.index_title = "Portal & Academy Management"
