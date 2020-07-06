import os

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps import views as sitemaps_views
from django.views.decorators.cache import cache_page


import autocomplete_light
from eguide.sitemap import ElectionSitemap, CountrySitemap, DigestSitemap

# import every app/autocomplete_light_registry.py
autocomplete_light.autodiscover()

admin.autodiscover()

sitemaps = {
    'election': ElectionSitemap,
    'country': CountrySitemap,
    'digest': DigestSitemap,
}

pattern = patterns(
    '',
    url(r'^myeguide/', include('allauth.urls'), name='myeguide'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^chaining/', include('smart_selects.urls')),
    url(r'^autocomplete/', include('autocomplete_light.urls')),
    url(r'^djangojs/', include('djangojs.urls')),

    url(r'^sitemap\.xml$', cache_page(86400)(sitemaps_views.index),
        {'sitemaps': sitemaps, 'sitemap_url_name': 'sitemaps'}, name='sitemap_index'),
    url(r'^sitemap-(?P<section>.+)\.xml$', cache_page(86400)(sitemaps_views.sitemap),
        {'sitemaps': sitemaps}, name='sitemaps'),

    (r'^ckeditor/', include('ckeditor.urls')),

    # Election Guide:
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^api/', include('api.urls')),
    url(r'^', include('eguide.urls')),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


PROJECT_ENV = os.environ.get('PROJECT_ENV')

if PROJECT_ENV == 'development':
    from django.conf import settings
    from django.conf.urls.static import static

    urlpatterns = pattern + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

else:
    urlpatterns = pattern
