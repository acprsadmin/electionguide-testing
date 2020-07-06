from django.conf.urls import patterns, include, url

from api.v1 import urls

urlpatterns = patterns(
    '',
    url(r'^v1/', include(urls)),
)
