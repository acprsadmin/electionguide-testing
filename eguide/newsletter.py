from django.template.loader import render_to_string
from eguide.models import Election, Digest
import datetime


def generate_newsletter():
    now = datetime.datetime.now()
    elections = Election.objects.all().select_related('country', 'institution')
    future_elections = elections.order_by('date').filter(active=1, date__gt=now.date())[:7]
    updated_elections = elections.order_by('-date').filter(active=1,cast_votes__gt = 0, date__lt=now.date())[:5]
    
    
    week_ago = now - datetime.timedelta(days=7)
        
    digest = Digest.objects.all().select_related('catgory').order_by('-post_date').filter(active=1, post_date__gt = week_ago.date())
    
    return render_to_string('newsletter/generator.html', 
                            {
                             'future_elections': future_elections,
                             'updated_elections': updated_elections,
                             'digest': digest,
                             'subject': generate_title(), 
                             'domain': 'http://www.electionguide.org'
                            })

def generate_title():
    now = datetime.datetime.now()
    week_ago = now - datetime.timedelta(days=7)
    
    subject = 'ElectList: %s-%s, %s' % (week_ago.strftime('%b %d'), now.strftime('%b %d'), now.strftime('%Y'))
    return subject
