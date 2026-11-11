from django.conf import settings
from django.contrib.sitemaps import Sitemap
from django.http import HttpResponse
from django.urls import reverse


def seo(request):
    """Expose canonical URL data to every template."""
    return {
        'SITE_URL': settings.SITE_URL,
        'CANONICAL_URL': settings.SITE_URL + request.path,
    }


class StaticViewSitemap(Sitemap):
    changefreq = 'weekly'
    protocol = 'https'

    PRIORITIES = {
        'portal:home': 1.0,
        'portal:about': 0.8,
        'portal:clubs': 0.8,
        'portal:leadership': 0.7,
        'portal:calendar': 0.7,
    }

    def items(self):
        return list(self.PRIORITIES)

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return self.PRIORITIES[item]


def robots_txt(request):
    body = (
        "User-agent: *\n"
        "Disallow: /admin/\n"
        "Disallow: /academy/\n"
        "\n"
        f"Sitemap: {settings.SITE_URL}/sitemap.xml\n"
    )
    return HttpResponse(body, content_type='text/plain')
