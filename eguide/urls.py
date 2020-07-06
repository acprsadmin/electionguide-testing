from django.conf.urls import patterns, url
from django.views.decorators.cache import cache_page
from eguide.views import *
# from eguide.views import election_create_view, candidate_create_view, partyvote_create_view, provision_create_view, edit_election_general, edit_election_methods, edit_election_rights, edit_election_reviews, person_create, party_create, partyvote_edit
from eguide import views
from eguide import feeds
from eguide import allauth_extends
from django.views.generic import RedirectView
# from django.core.urlresolvers import reverse

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^elections/$', views.elections, name='elections'),
    url(r'^elections/id/(?P<election_id>\d+)/$', views.election, name='election'),
    url(r'^elections/(?P<report_type>.+)/$', views.elections, name='elections-type'),
    url(r'^update_elections/$', views.update_elections, name='update_elections'),
    url(r'^countries/$', views.countries, name='countries'),
    url(r'^countries/id/(?P<country_id>.+)/$', views.country, name='country'),
    url(r'^digest/$', (views.digest), name='digest'),
    url(r'^digest/post/(?P<post_id>\d+)/$', views.digestEntry, name='post'),
    url(r'^digest/(?P<slug>.+)/$', views.digestCategory, name='digest-category'),
    url(r'^map/$', views.ifesmap, name='map'),
    url(r'^reports/$', views.reports, name='reports'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^p/(?P<slug>.+)/$', views.pageView, name='page'),

    # MyEguide Setup
    url(r'^myeguide/$', views.myeguideView, name='myeguide'),
    url(r'^myeguide/edit/profile$', views.myeguideEditProfile, name='editprofile'),
    url(r'^myeguide/signup', allauth_extends.EguideSignupView.as_view(), name="account_signup"),

    #ezTable Ajax url
    url(r'^ajax/election/$', cache_page(7*60*60)(views.ElectionTable.as_view()), name='dt-election'),
    url(r'^ajax/election/(?P<type>.+)/$', cache_page(7*60*60)(views.ElectionTable.as_view()), name='dt-election-upcoming'),
    url(r'^ajax/country/', cache_page(7*60*60)(views.CountryTable.as_view()), name='dt-country'),

    #newsletter Ajax
    url(r'^newsletter/start$', views.newsletter_start),
    url(r'^newsletter/(?P<newsletter_id>\d+)/$', views.newsletter_preview),

    # New Feeds
    #url(r'^feed/calendar$', cache_page(7*60*60)(ElectionFeed())),
    url(r'^feed/calendar/upcoming$', feeds.ElectionFeed(), name='upcoming-feed'),
    url(r'^feed/calendar/updates$', feeds.ElectionUpdates(), name='updates-feed'),
    url(r'^feed/digest/(?P<slug>.+)$', cache_page(7*60*60)(feeds.DigestCategoryFeed()), name='digest-feed'),

    # Legacy Feeds
    url(r'^calendar.xml$', cache_page(7*60*60)(feeds.calendar_legacy_rss)),
    url(r'^calendar-ace.xml$', cache_page(7*60*60)(feeds.calendar_legacy_rss)),
    url(r'^upcoming-elections.xml$', feeds.LegacyElectionFeed()),
    url(r'^upcoming-elections-safe.xml$', feeds.LegacyElectionFeed()),

    # Legacy URL Redirects
    url('^calendar.php$', RedirectView.as_view(url='/elections/')),
    url('^region.php$', RedirectView.as_view(url='/countries/')),
    url('^eguide.php$', RedirectView.as_view(url='/myeguide/')),
    url('^newsletter.php$', RedirectView.as_view(url='/digest/')),
    url('^search-results.php$', RedirectView.as_view(url='/elections/')),
    url('^advanced-search.php$', RedirectView.as_view(url='/elections/')),
    url('^region-events.php$', RedirectView.as_view(url='/countries/')),
    url('^election.php$', views.election),
    url('^results.php$', views.election),
    url('^interest.php$', views.election),
    url('^country.php$', views.country),
    url('^country-events.php$', views.country),
    url('^country-news.php$', views.country),
    url('^country-links.php$', views.country),

    # Legacy Assets Redirects
    url('^images/newsletter/(?P<path>.*)$', RedirectView.as_view(url='/static/eguide/newsletter/%(path)s')),

    url(r'^myeguide/signup', allauth_extends.EguideSignupView.as_view(), name="account_signup"),






    #url(r'^edit_election/$', views.edit_election, name='edit-election'),

   
    #url(r'^elections/list/$', views.ElectionsList), 
    #url(r'^elections/new/$', NewElectionView.as_view(), name="new-election"),
    #url(r'^elections/(?P<pk>\d+)/edit/$', EditElectionView.as_view(), name="edit-election"),

    # new urls for non admin forms and views
    




    # election list
    url(r'^allelections/$', views.allelections, name='allelections'),

    #UTILITIES
    url(r'^viewfields/$', views.view_fields, name='viewfields'),
    url(r'^viewprovisionfields/$', views.view_provision_fields, name='viewprovisionfields'),
    url(r'^viewdescriptions/$', views.view_descriptions, name='viewdescriptions'),

    url(r'^viewelection/(?P<election_id>[0-9]+)/$', views.view_election_general, name="view-election"),
        
    url(r'^election/(?P<election_id>[0-9]+)/xls/$', views.xls2, name="electionview-xls"),
    
    url(r'^election/(?P<election_id>[0-9]+)/general/$', views.view_election_general, name="electionview-general"),
    url(r'^election/(?P<election_id>[0-9]+)/parties/$', views.view_election_parties, name="electionview-parties"),
    url(r'^election/(?P<election_id>[0-9]+)/candidates/$', views.view_election_candidates, name="electionview-candidates"),
    url(r'^election/(?P<election_id>[0-9]+)/provisions/$', views.view_election_provisions, name="electionview-provisions"),
    url(r'^election/(?P<election_id>[0-9]+)/methods/$', views.view_election_methods, name="electionview-methods"),
    url(r'^election/(?P<election_id>[0-9]+)/rights/$', views.view_election_rights, name="electionview-rights"),
    url(r'^election/(?P<election_id>[0-9]+)/reviews/$', views.view_election_reviews, name="electionview-reviews"),






 #url(r'^election/(?P<pk>[0-9]+)/$', views.election_basic_edit, name='election_edit'),
    url(r'^edit_general/(?P<election_id>[0-9]+)/$', views.edit_election_general, name="electionview-general"),
    url(r'^edit_methods/(?P<election_id>[0-9]+)/$', views.edit_election_methods, name="electionview-methods"),
    url(r'^edit_rights/(?P<election_id>[0-9]+)/$', views.edit_election_rights, name="electionview-rights"),
    url(r'^edit_reviews/(?P<election_id>[0-9]+)/$', views.edit_election_reviews, name='ifes_reviewt'),



    url(r'^viewprovision/(?P<provision_id>[0-9]+)/$', views.provision_view, name="view-provision"),
   
    # create url
    url(r'election/new/$', election_create_view, name='election_add'),
    
    url(r'candidate/new/(?P<election_id>[0-9]+)/$', candidate_create_view, name='candidate_add'),
    url(r'person/new/(?P<election_id>[0-9]+)/$', person_create, name='person_add'),
    url(r'party/new/(?P<election_id>[0-9]+)/$', party_create, name='party_add'),

    url(r'partyvote/new/(?P<election_id>[0-9]+)/$', partyvote_create_view, name='party_add'),
    url(r'provision/new/(?P<election_id>[0-9]+)/$', provision_create_view, name='provision_add'),

    #url(r'^election/(?P<pk>[0-9]+)/$', ElectionBasicUpdate.as_view(), name='election_edit'),
    
   
    url(r'^provision/edit/(?P<pk>[0-9]+)/$', views.provision_edit, name='provision_edit'),
    url(r'^choice/new/(?P<pk>[0-9]+)/$', views.choice_add, name='choice_add'),
    url(r'^choice/edit/(?P<pk>[0-9]+)/$', views.choice_edit, name='choice_edit'),
    url(r'^choice/delete/(?P<pk>[0-9]+)/$', views.choice_delete, name='choice_delete'),
    url(r'^partyvote/edit/(?P<pk>[0-9]+)/$', views.partyvote_edit, name='partvote_edit'),
    url(r'^candidate/edit/(?P<pk>[0-9]+)/$', views.candidate_edit, name='candidate_edit'),
    
    url(r'^candidate/delete/(?P<pk>[0-9]+)/$', views.candidate_delete, name='candidate_delete'),
    url(r'^partyvote/delete/(?P<pk>[0-9]+)/$', views.partyvote_delete, name='partyvote_delete'),
    url(r'^provision/delete/(?P<pk>[0-9]+)/$', views.provision_delete, name='provision_delete'),

    
    #url(r'^current_elections/$', views.current_elections, name='elections-type'),

)
