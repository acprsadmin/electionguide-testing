from django.contrib.sitemaps import Sitemap
from eguide.models import Election, Country, Digest
from django.core.urlresolvers import reverse

class ElectionSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Election.objects.order_by('-date').filter(active=1)

    def lastmod(self, obj):
        return obj.date_updated
    
    def location(self, obj):
        return reverse('election', args=[str(obj.id)])
    
    
class CountrySitemap(Sitemap):
    changefreq = 'yearly'
    priority = 0.3

    def items(self):
        return Country.objects.filter(active=1)

    def lastmod(self, obj):
        return obj.date_updated
    
    def location(self, obj):
        return reverse('country', args=[str(obj.id)])
    
class DigestSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return Digest.objects.filter(active=1)

    def lastmod(self, obj):
        return obj.date_updated
    
    def location(self, obj):
        return reverse('post', args=[str(obj.id)])