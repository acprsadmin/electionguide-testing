from django import template
from django.core.cache import cache
from eguide.models import (Election, Country, Party_votes, Candidate_votes, Provision_votes, Choice, Category,
                           Institution_type, Digest, Newsletter)
from django.db.models import Sum
import datetime

register = template.Library()


@register.filter(name='integer')
def integer(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0


@register.filter(name='percent')
def percent(value1, value2):
    try:
        percent = (float(value1)/float(value2))*100
        return percent
    except (ValueError, TypeError):
        return None


@register.simple_tag
def active(path, pattern):
    import re
    if re.search(pattern, path):
        return 'active'
    return ''


@register.inclusion_tag('modules/digest_box.html')
def digest_box():

    digest = cache.get('digest_box')
    if not digest:
        digest = Digest.objects.only('id', 'title', 'post_date').filter(active=1)[3:6]
        cache.set('digest_box', digest, None)

    return {'digest': digest}


@register.inclusion_tag('modules/search_box.html')
def search_box():

    countries = cache.get('search_box_countries')
    if not countries:
        countries = Country.objects.only('id', 'name').order_by('name').filter(active=1)
        cache.set('search_box_countries', countries, None)

    institution_type = cache.get('search_box_institution_type', None)
    if not institution_type:
        institution_type = Institution_type.objects.order_by('name').only('id', 'name')
        cache.set('search_box_institution_type', institution_type, None)

    years = cache.get('search_box_years')
    if not years:

        this_year = datetime.datetime.now().year
        past_year = 1998
        year = this_year
        years = []

        while past_year <= year:
            years.append(year)
            year = year - 1

        cache.set('search_box_years', years, 60*60*24*30)

    return {'countries': countries,
            'institution_type': institution_type,
            'years': years}


@register.inclusion_tag('modules/navigation.html')
def navigation(path='/'):
    categories = cache.get('nav_category', None)
    if not categories:
        categories = Category.objects.order_by('name').all().filter(active=1)
        cache.set('nav_category', categories)

    return {'categories': categories, 'path': path}


@register.inclusion_tag('modules/recent_results.html')
def recent_results():

    elections = cache.get('recent_results')

    if not elections:
        today = datetime.datetime.now().date()
        elections = Election.objects.order_by('-date'
                                          ).filter(date__lt=today, active=1, cast_votes__gt=0
                                                   ).select_related('country',
                                                                    'institution').only('id',
                                                                                        'date',
                                                                                        'country',
                                                                                        'institution',
                                                                                        'country__name',
                                                                                        'country__flag',
                                                                                        'cast_votes',
                                                                                        'institution__name'
                                                                                        )[:4]
        cache.set('recent_results', elections, 216000)

    return {'elections': elections}


@register.inclusion_tag('modules/total_elections.html')
def total_elections():

    total = cache.get('total_elections')

    if not total:

        year = datetime.date.today().year
        today = datetime.date.today()
        start = datetime.datetime.strptime('0101%s' % year, "%d%m%Y").date()
        end = datetime.datetime.strptime(str(today), "%Y-%m-%d").date()
        total = Election.objects.filter(date__gt=start, date__lt=end, active=1).count()
        cache.set('total_elections', total, None)

    return {'total': total}


@register.inclusion_tag('modules/total_votes.html')
def total_votes():
    total = cache.get('total_votes')
    if not total:

        year = datetime.date.today().year
        start = datetime.datetime.strptime('0101%s' % year, "%d%m%Y").date()
        end = datetime.datetime.strptime('3112%s' % year, "%d%m%Y").date()
        elections = Election.objects.filter(date__gt=start, date__lt=end, active=1).aggregate(total=Sum('cast_votes'))

        total = elections['total']
        cache.set('total_votes', total)

    return {'total': total}


@register.inclusion_tag('modules/newsletter_analytics.html')
def newsletter_analytics(object_pk):

    analytic_fields = ['delivered',
                       'complained',
                       'clicked',
                       'opened',
                       'dropped',
                       'bounced',
                       'unsubscribed']
    analytic_items = []

    newsletter = Newsletter.objects.get(pk=object_pk)
    for item in analytic_fields:
        field = getattr(newsletter, item)
        analytic_items.append({'name': item, 'value': field})

    return {'newsletter': newsletter, 'analytic_items': analytic_items}


@register.inclusion_tag('modules/related_elections.html')
def related_election(country_id=2, limit=5):
    country = Country.objects.get(id=country_id)
    elections = Election.objects.order_by('-date').all().filter(country=country_id)[:limit]

    return {'elections': elections, 'country': country}


@register.inclusion_tag('modules/election_results.html')
def election_results(election_id):
    if int(election_id) > 0:
        election = Election.objects.only('id', 'cast_votes', 'valid_votes', 'invalid_votes').get(id=election_id)
        result_list = False

        if election:
            if Candidate_votes.objects.filter(election=election.id).exists():
                # Fetch all related candidate votes objects related to this election
                related = Candidate_votes.objects.order_by('-votes'
                                                           ).all().filter(election=election.id
                                                                          ).select_related('candidate')

                # Make sure votes and percetage are available, if not calculate them
                for i, item in enumerate(related):
                    if not result_list:
                        result_list = True

                    try:
                        # First: If there votes is empty but percentage is entered
                        if int(item.votes) <= 0 and int(item.percentage) > 0:
                            if int(election.valid_votes) > 0:
                                related[i].votes = (int(item.percentage) / 100)*int(election.valid_votes)
                            elif int(election.cast_votes) > 0:
                                related[i].votes = (int(item.percentage) / 100)*int(election.cast_votes)

                        # Second: If percentage is empty but vote is entered
                        elif int(item.votes) > 0 and int(item.percentage) <= 0:
                            if int(election.valid_votes) > 0:
                                related[i].percentage = (int(item.votes) / int(election.valid_votes))*100
                            elif int(election.cast_votes) > 0:
                                related[i].percentage = (int(item.votes) / int(election.cast_votes))*100

                        if int(related[i].votes) > 0:
                            related[i].votes = format(related[i].votes, ",d")
                        else:
                            related[i].votes = '-'
                    except TypeError:
                        pass

                return {'results': related, 'candidate_list': result_list}

            elif Party_votes.objects.filter(election=election.id).exists():
                return calculate_party_changes(election_id)

            elif Provision_votes.objects.filter(election=election.id).exists():

                provisions = Provision_votes.objects.all().filter(election=election.id)

                # Make sure votes and percetage are available,
                # if not calculate them
                for j, provision in enumerate(provisions):
                    provisions[j].choices = Choice.objects.all().filter(provision=provision.id)

                    for i, item in enumerate(provisions[j].choices):
                        if not result_list:
                            result_list = True

                        try:
                            # First: If there votes is empty but percentage is entered
                            if int(item.votes) <= 0 and int(item.percentage) > 0:
                                if int(election.valid_votes) > 0:
                                    provisions[j].choices[i].votes = (int(item.percentage) / 100)*int(election.valid_votes)
                                elif int(election.cast_votes) > 0:
                                    provisions[j].choices[i].votes = (int(item.percentage) / 100)*int(election.cast_votes)

                            # Second: If percentage is empty but vote is entered
                            elif int(item.votes) > 0 and int(item.percentage) <= 0:
                                if int(election.valid_votes) > 0:
                                    provisions[j].choices[i].\
                                        percentage = (int(item.votes) / int(election.valid_votes))*100
                                elif int(election.cast_votes) > 0:
                                    provisions[j].choices[i].percentage = (int(item.votes) /
                                                                           int(election.cast_votes)) * 100

                            if int(provisions[j].choices[i].votes) > 0:
                                provisions[j].choices[i].votes = format(provisions[j].choices[i].votes, ",d")
                            else:
                                provisions[j].choices[i].votes = '-'

                        except TypeError:
                            pass

                return {'results': provisions, 'referendum_list': result_list}
    else:
        pass


@register.inclusion_tag('modules/party_seats_share.html')
def party_seats(election_id):
    return calculate_party_changes(election_id)


def calculate_party_changes(election_id):

    if int(election_id) > 0:
        election = Election.objects.get(id=election_id)
        previous_election = Election.objects.only('id').filter(institution=election.institution.id,
                                                               date__lt=election.date)[:1]

        seat_share = False
        party_list = False

        if election:
            related = Party_votes.objects.order_by('-votes').all().filter(election=election.id).select_related('party')

            bool(related)
            bool(previous_election)

            # Make sure votes and percetage are available, if not calculate them
            for i, item in enumerate(related):

                if not party_list:
                    party_list = True

                try:
                    # First: If there votes is empty but percentage is entered
                    if int(item.votes) <= 0 and int(item.percentage) > 0:
                        if int(election.valid_votes) > 0:
                            related[i].votes = (int(item.percentage) / 100)*int(election.valid_votes)
                        elif int(election.cast_votes) > 0:
                            related[i].votes = (int(item.percentage) / 100)*int(election.cast_votes)

                    # Second: If percentage is empty but vote is entered
                    elif int(item.votes) > 0 and int(item.percentage) < 0:
                        if int(election.valid_votes) > 0:
                            related[i].percentage = (int(item.votes) / int(election.valid_votes))*100
                        elif int(election.cast_votes) > 0:
                            related[i].percentage = (int(item.votes) / int(election.cast_votes))*100

                    if int(related[i].votes) > 0:
                        related[i].votes = format(related[i].votes, ",d")
                    else:
                        related[i].votes = '-'

                    # Calculate change in number of seats from pervious election
                    if int(item.seats_won) > 0:

                        if not seat_share:
                            seat_share = True

                        if previous_election:
                            try:
                                party_previous_info = Party_votes.objects.\
                                                      only('id',
                                                           'seats_won').\
                                                      filter(election=previous_election[0].id,
                                                             party=item.party.id
                                                             )

                                if party_previous_info:
                                    related[i].seats_change = (int(item.seats_won) -
                                                               int(party_previous_info[0].seats_won))
                                    if related[i].seats_change < 0:
                                        related[i].seats_change_direction = '<span class="down">&#9660;</span>'
                                    elif related[i].seats_change == 0:
                                        related[i].seats_change_direction = '-'
                                    else:
                                        related[i].seats_change_direction = '<span class="up">&#9650;</span>'
                                related[i].seats_change = "-"
                            except Party_votes.DoesNotExist:
                                related[i].seats_change = "-"

                    else:
                        item.seats_won = "-"
                        related[i].seats_change = "-"
                except TypeError:
                    pass

            return {'results': related,
                    'seat_share': seat_share,
                    'party_list': party_list}
    else:
        pass
