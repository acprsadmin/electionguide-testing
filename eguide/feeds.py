from datetime import datetime, time

from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.utils.feedgenerator import rfc2822_date
from django.contrib.sites.models import Site
from django.utils import timezone
from django.utils.text import Truncator
from django.utils import dateformat
from django.core.cache import cache

from eguide.models import Election, Digest, Category


# This is the default class
# It shows upcoming elections
class ElectionFeed(Feed):
    title = "ElectionGuide.org: Elections Calendar"
    link = "/elections/"
    description = "Latest updates from Election Guide"

    def items(self):
        today = timezone.now()
        return Election.objects.order_by('date').filter(active=1, date__gt = today)[:30]

    def item_title(self, item):
        try:
            title = '%s: Election for %s' % (item.country.name, item.institution.name)
        except AttributeError:
            title = '%s: Referendum' % (item.country.name)

        return title

    def item_description(self, item):
        description = '<p>Election Date: <strong> %s </strong></p>' % (dateformat.format(item.date, 'N d, Y'))
        if item.registered_voters > 0:
            description += '<p>Registered Voters: <strong> %s </strong></p>' % (str(format(item.registered_voters, ',d')))
        if item.show_results and item.cast_votes > 0:
            description += '<p>Cast Votes: <strong> %s </strong></p>' % (str(format(item.cast_votes, ',d')))

        text = Truncator(item.description)
        description += text.words(30)

        return description

    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        return reverse('election', args=[item.pk])

    def item_pubdate(self, item):
        return datetime.combine(item.date, time())


class ElectionUpdates(ElectionFeed):

    def items(self):
        return Election.objects.order_by('-date_updated')[:30]


class LegacyElectionFeed(ElectionFeed):

    def __call__(self, request, *args, **kwargs):

        output = cache.get('legacy_election_feed')
        if not output:
            output = super(LegacyElectionFeed, self).__call__(request, *args, **kwargs)
            cache.set('legacy_election_feed', output, None)

        return output

    def item_title(self, item):
        return item.country.name

    def item_description(self, item):
        try:
            description = 'Election for %s' % (item.institution.name)
        except AttributeError:
            description = 'Referendum'
        return description


class DigestCategoryFeed(Feed):

    def get_object(self, request, slug):
        if slug == 'all':
            return None
        else:
            return get_object_or_404(Category, slug=slug)

    def title(self, obj):
        if obj:
            return "Election Digest: %s" % obj.name
        else:
            return "Election Digest: All"

    def link(self, obj):
        if obj:
            return reverse('digest-category', args=[obj.slug])
        else:
            return reverse('digest')

    def description(self, obj):
        return "Read the latest Election Guide Digest"

    def items(self, obj):
        if obj:
            return Digest.objects.filter(category=obj, active=1).order_by('-post_date')[:30]
        else:
            return Digest.objects.filter(active=1).order_by('-post_date')[:30]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.excerpt

    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        return reverse('post', args=[item.pk])

    def item_pubdate(self, item):
        return item.post_date


def calendar_legacy_rss(request):

    output = cache.get('calendar_legacy_rss')

    if not output:

        today = timezone.now()
        elections = Election.objects.order_by('date').all().filter(date__gt=today)[:20]
        current_site = Site.objects.get_current()

        today = rfc2822_date(today)

        for item in elections:
            if item.date_updated:
                        item.date_updated = rfc2822_date(item.date_updated)
                        item.country.link = 'http://%s%s' % (current_site.domain, reverse('country',  args=[item.country.id]))
                        item.link = 'http://%s%s' % (current_site.domain, reverse('election',  args=[item.id]))

        output = render(request, 'pages/legacy_calendar.rss', {'elections': elections,
                                                               'today': today})
        cache.set('calendar_legacy_rss', output, None)

    return output


