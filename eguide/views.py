from __future__ import division
import datetime
from numpy import asarray

from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required, permission_required

from mailgun.methods import Mailgun

from eguide.models import (Election, Party_votes, Party, Candidate_votes, Provision_votes, Person, Choice, Country, Institution, Digest, Category, Page, EguideUser,
                           Newsletter)
from eguide.forms import EguideUserForm, ElectionCreateForm, ElectionEditForm, ElectionMethodForm, IfesReviewForm, ElectionRightsForm, ProvisionLinkForm, PartyLinkForm, CandidateLinkForm, PersonLinkForm, PartyForm
from eguide.eztables_extend import IfesDatatablesView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
#from bootstrap_modal_forms.generic import BSModalCreateView
from django.core.urlresolvers import reverse_lazy
#from django.views.generic import UpdateView, CreateView
from django.template import loader
from django.db.models import F
import xlsxwriter
import io
from django.views.generic import View

import time
import regex

from ckeditor.widgets import CKEditorWidget

class ElectionTable(IfesDatatablesView):

    queryset = Election.objects.filter(active=1).\
                   only('id',
                        'country__id',
                        'country__flag',
                        'country__name',
                        'institution__name',
                        'date',
                        'election_status__name',
                        'id',
                        'name',
                        'institution__institution_type__name')

    def get_queryset(self):
        '''Apply Datatables sort and search criterion to QuerySet'''
        qs = super(IfesDatatablesView, self).get_queryset()
        try:
            report_type = self.kwargs['type']

            if report_type == 'upcoming':
                qs = Election.objects.all().filter(date__gte=datetime.datetime.now().date())
            if report_type == 'past':
                qs = Election.objects.all().filter(active=1, date__lte=datetime.datetime.now().date())
        except KeyError:
            pass

        # Perform global search
        qs = self.global_search(qs)
        # Perform column search
        qs = self.column_search(qs)
        # Return the ordered queryset
        return qs.order_by(*self.get_orders())

    fields = (
        'country__flag',
        'country__name',
        'institution__name',
        'date',
        'election_status__name',
        'id',
        'name',
        'institution__institution_type__name',
        'country__id',
    )

    """
    " the field that is needed as an argument for the URL must be included
    " in the fields for url_fields to work
    " the result is returned in form of an array with the first item as the
    " value and the second item as the URL
    """

    url_fields = [
                    {
                        'field': 'country__name',
                        'target': 'country',
                        'arg': 'country__id'
                    },
                    {
                        'field': 'institution__name',
                        'target': 'election',
                        'arg': 'id'
                    }
                  ]
    image_fields = ['country__flag']


class CountryTable(IfesDatatablesView):
    queryset = Country.objects.all().filter(active=1)
    fields = (
        'flag',
        'name',
        'region__name',
        'population',
        'id',
    )

    """
    " the field that is needed as an argument for the URL must be included in
    " the fields for url_fields to work
    " the result is returned in form of an array with the first item as the
    " value and the second item as the URL
    """

    url_fields = [
                  {
                       'field': 'name',
                       'target': 'country',
                       'arg': 'id'
                   },
                  ]
    image_fields = ['flag']


def home(request):

    election = cache.get('home_election')
    if not election:

        election = Election.objects.order_by('date'
                                             ).filter(date__gte=datetime.datetime.now().date(), active=1
                                                      ).select_related('country',
                                                                       'institution').only('id',
                                                                                           'country__alpha3',
                                                                                           'country',
                                                                                           'institution',
                                                                                           'country__name',
                                                                                           'date',
                                                                                           'institution__name',
                                                                                           'country__id',
                                                                                           'institution__id')[:20]
        cache.set('home_election', election, None)

    digest = cache.get('home_digest')
    if not digest:
        digest = Digest.objects.filter(active=True).order_by('-post_date')[:3]
        cache.set('home_digest', digest, None)

    return render(request, 'base/index.html', {'election': election, 'digest': digest})


def elections(request, report_type=None):

    if request.user.is_authenticated():
        eguideuser = EguideUser.objects.get(id=request.user.id)
        isDataEntry =  eguideuser.isdataentry()
    else:
        isDataEntry =  False
    # for testing.
    # isDataEntry = False   
    

    query_items = []
    if request.GET.get('inst'):
        query_items.append(request.GET.get('inst'))
    if request.GET.get('cont'):
        query_items.append(request.GET.get('cont'))
    if request.GET.get('yr'):
        query_items.append(request.GET.get('yr'))

    query = ' '.join(query_items)
    elections = ''
    count = ''

    if(report_type):
        if report_type == 'upcoming':
            elections = cache.get('elections_upcoming')

            if not elections:
                elections = Election.objects.order_by('date').all().filter(date__gte=datetime.datetime.now().date()
                                                                           ).select_related('country',
                                                                                            'institution',
                                                                                            'election_status')[:30]
                cache.set('elections_upcoming', elections, None)

            count = cache.get('elections_upcoming_count')

            if not count:
                count = Election.objects.all().filter(date__gte=datetime.datetime.now().date()).count()
                cache.set('elections_upcoming_count', count, None)

        if report_type == 'past':
            elections = cache.get('elections_past')

            if not elections:
                elections = Election.objects.order_by('-date').all().filter(active=1,
                                                                            date__lte=datetime.datetime.now().date()
                                                                            ).select_related('country',
                                                                                             'institution',
                                                                                             'election_status')[:30]
                cache.set('elections_past', elections, None)

            count = cache.get('elections_past_count')

            if not count:
                count = Election.objects.all().filter(active=1, date__lte=datetime.datetime.now().date()).count()
                cache.set('elections_past_count', count, None)

    return render(request, 'election/browse.html', {'query': query,
                                                    'type': report_type,
                                                    'elections': elections,
                                                    'count': count,
                                                    'isDataEntry': isDataEntry})






def election(request, election_id=1):

    try:
        if request.GET.get('ID') and election_id == 1:
            legacy_election = Election.objects.all().filter(legacy_id=int(request.GET.get('ID')))[:1]
            election = legacy_election[0]

        else:
            election = Election.objects.get(id=election_id)

    except (IndexError, ValueError, Election.DoesNotExist):
            return redirect('elections')

    election.participation = 0
    parliamentary_type = False

    if Party_votes.objects.filter(election=election.id).exists():
        parliamentary_type = True

    try:
        # Calculate Participation
        if int(election.cast_votes) > 0 and int(election.registered_voters) > 0:
            election.participation = (int(election.valid_votes) / int(election.registered_voters)) * 100
            election.not_voted = int(election.registered_voters) - int(election.valid_votes)

        if int(election.participation) > 100:
            election.participation = None
    except TypeError:
        election.participation = None

    return render(request, 'election/post.html', {'election': election,
                                                  'parliamentary_type': parliamentary_type})



def isAccessed(request):
    if request.user.is_authenticated():
        eguideuser = EguideUser.objects.get(id=request.user.id)
        return eguideuser.isdataentry()
    else:
        return False

#UTILITY
def update_elections(request):
    query_items = []

    # First Method.
    # elections = Election.objects.all().filter(original_election_year__isnull=True).update(original_election_year=F('date').year)        

    # Second Method.
    elections = Election.objects.all().filter(original_election_year__isnull=True)
    print 'election year = null'
    for election in elections:
        
        print election.id
        if election.date != None:
            election.original_election_year = election.date.year
            election.save()

    return redirect('/allelections')

    # return render(request, 'election/update_elections.html', {'success': True})

#UTILITY
def view_fields(request):
    query_items = []
    elections = Election.objects.all().exclude(inperson_voting_instructions=u'')
    return render(request, 'election/utilities/view_fields.html', {'elections': elections})

#UTILITY
def view_provision_fields(request):
    query_items = []
    provisions = Provision_votes.objects.all().exclude(provision=u'')
    return render(request, 'election/utilities/view_provision_fields.html', {'provisions': provisions})


def view_descriptions(request):
    query_items = []
    elections = Election.objects.all().exclude(description=u'')
    return render(request, 'election/utilities/view_descriptions.html', {'elections': elections})













#management list
def allelections(request):
    electionresults = Election.objects.all().filter(original_election_year = 2020).order_by('-date')
    template = loader.get_template('election/see_elections.html')
    context = {electionresults}

    user = request.user
    create_allowed = False
    
    return render(request, 'election/see_elections.html', {'electionresults': electionresults, 'create_allowed': create_allowed})



#def view_election(request, election_id, tab = 'general'):
#    election = Election.objects.get(id=election_id)
#    country = Country.objects.get(id=election.country_id)
#    parties = Party.objects.all().filter(country = country.name)
#
#
#
#    partyvotes = Party_votes.objects.all().filter(election_id = election_id)
#    candidatevotes = Candidate_votes.objects.all().filter(election_id = election_id)
#    provisions = Provision_votes.objects.all().filter(election_id = election_id)
#
#    return render(request, 'election/show/detail.html', {'election': election, 'partyvotes': partyvotes, 'candidatevotes': candidatevotes, 'provisions': provisions, 'tab': tab})


#VIEW ELECTION

def view_election_general(request, election_id):
    if  isAccessed(request)== True:

        election = Election.objects.get(id=election_id)
        country = Country.objects.get(id=election.country_id)

        return render(request, 'election/show/detail_general.html', {'election': election})
    else:
        return redirect('/') 
        

def view_election_parties(request, election_id):
    if  isAccessed(request)== True:

        election = Election.objects.get(id=election_id)
        partyvotes = Party_votes.objects.all().filter(election_id = election_id)

        return render(request, 'election/show/detail_parties.html', {'election': election,'partyvotes': partyvotes, })
    else:
        return redirect('/') 
       

def view_election_candidates(request, election_id):
    if  isAccessed(request)== True:
        election = Election.objects.get(id=election_id)
        candidatevotes = Candidate_votes.objects.all().filter(election_id = election_id)

        return render(request, 'election/show/detail_candidates.html', {'election': election, 'candidatevotes': candidatevotes, })
    else:
        return redirect('/') 
        

def view_election_provisions(request, election_id):
    if  isAccessed(request)== True:
        election = Election.objects.get(id=election_id)
        provisions = Provision_votes.objects.all().filter(election_id = election_id)

        return render(request, 'election/show/detail_provisions.html', {'election': election, 'provisions': provisions})
    else:
        return redirect('/') 


def view_election_methods(request, election_id):
    if  isAccessed(request)== True:
        election = Election.objects.get(id=election_id)

        return render(request, 'election/show/detail_methods.html', {'election': election})
    else:
        return redirect('/') 


def view_election_rights(request, election_id):
    if  isAccessed(request)== True:
        election = Election.objects.get(id=election_id)

        return render(request, 'election/show/detail_rights.html', {'election': election})
    else:
        return redirect('/') 


def view_election_reviews(request, election_id):
    if  isAccessed(request)== True:
        election = Election.objects.get(id=election_id)

        return render(request, 'election/show/detail_reviews.html', {'election': election})
    else:
        return redirect('/') 




#EXCEL DOWNLOAD
def xls2(request, election_id):
    try:
        import cStringIO as StringIO
    except ImportError:
        import StringIO

    output = StringIO.StringIO()

    election = Election.objects.get(id=election_id)
    partyvotes = Party_votes.objects.all().filter(election_id = election_id)
    candidatevotes = Candidate_votes.objects.all().filter(election_id = election_id)
    provisions = Provision_votes.objects.all().filter(election_id = election_id)
    
        
    from xlsxwriter.workbook import Workbook

    book = Workbook(output)
    bold = book.add_format({'bold': True})
    votes = book.add_format({'num_format': '#,##0'})
    date_format = book.add_format({'num_format': 'yyyy-mm-dd'})
    atop = book.add_format({'valign': 'top'})

  


    ifes = book.add_worksheet('README')  
    worksheet = book.add_worksheet('election basics')  
    worksheet1 = book.add_worksheet('description')  
    worksheet2 = book.add_worksheet('parties')  
    worksheet3 = book.add_worksheet('candidates')  
    worksheet4 = book.add_worksheet('provisions')  
    worksheet5 = book.add_worksheet('provision_choices')  
    
    mylevel = ""
    if election.is_national_exec:
       mylevel = mylevel + 'NATIONAL_EXEC' + ' '
    if election.is_national_legislative:
          mylevel = mylevel + 'NATIONAL_LEGISLATIVE' + ' '
    if election.is_national_upper:
          mylevel = mylevel + 'NATIONAL_UPPER' + ' '
    if election.is_national_lower:
        mylevel = mylevel + 'NATIONAL_LOWER' + ' '


    row = 1
    col = 0

    textarea_height = 20

    now = datetime.datetime.now()
    filename = election.name + "_" + str(election.original_election_year) + now.strftime("%Y%m%d(%H%M%S)") + ".xlsx"
    disclaim = 'While IFES strives to make the information on this website as timely and accurate as possible, IFES makes no claims nor guarantees about the accuracy and completeness of the data on this site beyond what is outlined in our verification process, and expressly disclaims liability for errors and omissions in the contents of this site.'

    ifes.set_column('A:A', 35)
    ifes.set_column('B:B', 80)
    ifes.write(0,0, 'IFES Election Guide Data', bold)
    ifes.write(1,0, 'Download Date:')
    ifes.write(1,1, now.strftime("%Y%m%d(%H%M%S)"))
    ifes.write(2,0, 'Filename: ')
    ifes.write(2,1, filename)
    ifes.write(3,0, 'Country')
    ifes.write(3,1, election.country.name)
    ifes.write(4,0, 'Year (original):')
    ifes.write(4,1, election.original_election_year)
    ifes.write(5,0, 'Election Name')
    ifes.write(5,1, election.name)
    ifes.write(6,0, 'Disclaimer')
    ifes.write(6,1, disclaim)







    #DESCRIPTION SHEET
    worksheet1.set_column('A:A', 1000)
    worksheet1.set_default_row(200)
    print(election.description)
    worksheet1.write(0, 0, election.description, atop)
   
  
    s_ary = regex.findall(r"\n", election.description)
    print("len n: ", len(s_ary))




    #ELECTION GENERAL DATA
    worksheet.set_column('A:A', 35)
    worksheet.set_column('B:B', 80)

     # Write a total using a formula.
    worksheet.write(0, 0, 'Election Field', bold)
    worksheet.write(0, 1, 'Value', bold)

    row += 1
    worksheet.write(row, 0, 'ID')
    worksheet.write(row, 1, election.id)
    row += 1
    worksheet.write(row, 0, 'Election Name')
    worksheet.write(row, 1, election.name)
    row += 1
    worksheet.write(row, 0, 'Election Level')
    worksheet.write(row, 1, mylevel)
    row += 1
    worksheet.write(row, 0, 'Institution:')
    worksheet.write(row, 1, election.institution.name)
    row += 1
    worksheet.write(row, 0, 'Election Type')
    worksheet.write(row, 1, election.election_type.name)
    row += 1
    
    worksheet.write(row, 0, 'Electoral System')
    if election.electoral_system == None:
        worksheet.write(row, 1, 'n/a')
    else:
        worksheet.write(row, 1, election.electoral_system.name)

    row += 1
    worksheet.write(row, 0, 'Voting Age Minimum')
    worksheet.write(row, 1, election.voting_age_minimum_inclusive)
    row += 1
    worksheet.write(row, 0, 'Voting Age Minimum Source')
    worksheet.write(row, 1, election.voting_age_minimum_source)
    row += 1
    worksheet.write(row, 0, 'Administering Commission Website')
    worksheet.write(row, 1, election.administering_election_commission_website)
    row += 1
    worksheet.write(row, 0, 'Election Website')
    worksheet.write(row, 1, election.source_website)
    row += 1
    worksheet.write(row, 0, 'Status')
    worksheet.write(row, 1, election.election_status.name)
    row += 1
    worksheet.write(row, 0, 'Delayed by COVID-19')
    worksheet.write(row, 1, election.is_delayed_covid19)
    row += 1
    worksheet.write(row, 0, 'Original Election Year')
    worksheet.write(row, 1, election.original_election_year)
    row += 1
    worksheet.write(row, 0, 'Election Date (deprecated')
    worksheet.write(row, 1, election.date, date_format)
    row += 1
    worksheet.write(row, 0, 'Election Range Start Date:')
    worksheet.write(row, 1, election.election_range_start_date, date_format)
    row += 1
    worksheet.write(row, 0, 'Election Range End Date:')
    worksheet.write(row, 1, election.election_range_end_date, date_format) 
    row += 1

    
    worksheet.set_row(row, 20)
    worksheet.set_row(row, textarea_height)
    worksheet.write(row, 0, 'Election Range Details')
    worksheet.write(row, 1, election.election_range_notes)
    row += 1
    worksheet.write(row, 0, 'Election Range Source')
    worksheet.write(row, 1, election.election_range_source, atop)
    row += 1
    worksheet.write(row, 0, 'Election Range Start Date:')
    worksheet.write(row, 1, election.election_declared_start_date, date_format)
    row += 1
    worksheet.write(row, 0, 'Election Range End Date:')
    worksheet.write(row, 1, election.election_declared_end_date, date_format) 
    row += 1
    worksheet.write(row, 0, 'Declared Dates Source')
    worksheet.write(row, 1, election.election_declared_source)
    row += 1

    worksheet.write(row, 0, 'Election Blackout Start Date:')
    worksheet.write(row, 1, election.election_declared_start_date, date_format)
    row += 1
    worksheet.write(row, 0, 'Election Blackout End Date:')
    worksheet.write(row, 1, election.election_declared_end_date, date_format) 
    row += 1
    worksheet.write(row, 0, 'Blackout Dates Source')
    worksheet.write(row, 1, election.blackout_date_source)

    row += 1
    worksheet.write(row, 0, 'Voter Registration Deadline Date')
    worksheet.write(row, 1, election.voter_registration_deadline, date_format)
    row += 1
    worksheet.write(row, 0, 'Candidate Filing Deadline Date')
    worksheet.write(row, 1, election.election_candidate_filing_deadline, date_format)
    row += 1
    worksheet.write(row, 0, 'Candidate Filing Deadline Source')
    worksheet.write(row, 1, election.election_candidate_filing_deadline_source)

    row += 1
    worksheet.write(row, 0, 'Elected Female Leaders', votes)
    worksheet.write(row, 1, election.female_elected)
    row += 1
    worksheet.write(row, 0, 'Registered Voters Source Date', date_format)
    worksheet.write(row, 1, election.registered_voters_date)
    row += 1
    worksheet.write(row, 0, 'Registered Voters Total', votes)
    worksheet.write(row, 1, election.registered_voters)
    row += 1
    worksheet.write(row, 0, 'Registered Voters Female', votes)
    worksheet.write(row, 1, election.registered_voters_female)
    row += 1
    worksheet.write(row, 0, 'Registered Voters Male', votes)
    worksheet.write(row, 1, election.registered_voters_male)
    row += 1
    worksheet.write(row, 0, 'Registered Voters Source')
    worksheet.write(row, 1, election.registered_voters_source)
    row += 1
    worksheet.write(row, 0, 'Total Cast Votes', votes)
    worksheet.write(row, 1, election.cast_votes)
    row += 1
    worksheet.write(row, 0, 'Valid Votes', votes)
    worksheet.write(row, 1, election.valid_votes)
    row += 1
    worksheet.write(row, 0, 'Invalid Votes', votes)
    worksheet.write(row, 1, election.invalid_votes)

    if election.yn_support_electoral_rights == 1:
      yn_support = 'Yes'
    elif election.yn_support_electoral_rights == 2:
      yn_support = 'No'
    else:
      yn_support = 'n/a'
    row += 1
    worksheet.write(row, 0, 'Support Electoral Rights')
    worksheet.write(row, 1, yn_support)

    row += 1
    worksheet.set_row(row, textarea_height)
    worksheet.write(row, 0, 'Support Electoral Rights Details')
    worksheet.write(row, 1,  election.support_electoral_rights_details, atop)

    if election.yn_restrict_electoral_rights == 1:
      yn_restrict = 'Yes'
    elif election.yn_restrict_electoral_rights == 2:
      yn_restrict = 'No'
    else:
      yn_restrict = 'n/a'
   
    row += 1
    worksheet.write(row, 0, 'Restrict Electoral Rights')
    worksheet.write(row, 1, yn_restrict)

    row += 1
    worksheet.set_row(row, textarea_height)
    worksheet.write(row, 0, 'Restrict Electoral Rights Details')
    worksheet.write(row, 1, election.restrict_electoral_rights_details, atop)

    row += 1
    worksheet.write(row, 0, 'Restrict Electoral Rights Source')
    worksheet.write(row, 1, election.electoral_rights_info_source)
    

    if election.yn_hate_speech_prohibited == 1:
        yn_hate = 'Yes'
    elif election.yn_hate_speech_prohibited == 2:
        yn_hate = 'No'
    else:
        yn_hate = 'n/a'
    row += 1
    worksheet.write(row, 0, 'Hate Speech Prohibited')
    worksheet.write(row, 1, yn_hate)

    row += 1
    worksheet.set_row(row, textarea_height)
    worksheet.write(row, 0, 'Hate Speech Prohibited Detail')
    worksheet.write(row, 1, election.hate_speech_details, atop)

    row += 1
    worksheet.write(row, 0, 'Hate Speech Prohibited Source')
    worksheet.write(row, 1, election.hate_speech_prohibition_source)

    if election.yn_disinformation_prohibited == 1:
        yn_info = 'Yes'
    elif election.yn_disinformation_prohibited == 2:
        yn_info = 'No'
    else:
        yn_info = 'n/a'
    row += 1
    worksheet.write(row, 0, 'Disinformation Prohibited')
    worksheet.write(row, 1, yn_info)

    row += 1
    worksheet.set_row(row, textarea_height)
    worksheet.write(row, 0, 'Disinformation Prohibited Details')
    worksheet.write(row, 1, election.disinformation_details, atop)

    row += 1
    worksheet.write(row, 0, 'Disinformation Prohibited Source')
    worksheet.write(row, 1, election.disinformation_prohibition_source)

  
    worksheet2.write(0, 0, 'ID', bold)
    worksheet2.write(0, 1, 'Party', bold)
    worksheet2.write(0, 2, 'Seats Won', bold)
    worksheet2.write(0, 3, 'Votes', bold)
    worksheet2.write(0, 4, 'Percentage', bold)
    worksheet2.write(0, 5, 'Description', bold)
    worksheet2.set_column('B:B', 35)
    worksheet2.set_column('F:F', 80)
  

    row = 1
    for pv in partyvotes:
      worksheet2.set_row(row, textarea_height)
      worksheet2.write(row, 0, pv.id)
      worksheet2.write(row, 1, pv.party.name)
      worksheet2.write(row, 2, pv.seats_won)
      worksheet2.write(row, 3, pv.votes)
      worksheet2.write(row, 4, pv.percentage)
      worksheet2.write(row, 5, pv.description, atop)
  
      row += 1

   

       
    worksheet3.write(0, 0, 'ID', bold)
    worksheet3.write(0, 1, 'Candidate', bold)
    worksheet3.write(0, 2, 'Party', bold)
    worksheet3.write(0, 3, 'Votes', bold)
    worksheet3.write(0, 4, 'Percentage', bold)
    worksheet3.set_column('B:B', 35)
    
    row = 1
    for cv in candidatevotes:
      myperson = Person.objects.get(id=cv.candidate_id)
      if myperson.party_id == None:
          partyname = 'n/a'
      else:
          partyname = myperson.party.name

      worksheet3.write(row, 0, cv.candidate.name)
      worksheet3.write(row, 1, partyname)
      worksheet3.write(row, 2, cv.votes, votes)
      worksheet3.write(row, 3, cv.percentage)
      row += 1
    
   

    worksheet4.write(0, 0, 'ID', bold)
    worksheet4.write(0, 1, 'Provision', bold)
    worksheet4.write(0, 2, 'Comments', bold)
    worksheet4.write(0, 3, 'Cast Votes', bold)
    worksheet4.write(0, 4, 'Valid Votes', bold)
    worksheet4.write(0, 5, 'Invalid Votes', bold)
    worksheet4.set_column('B:B', 50)
    worksheet4.set_column('C:C', 35)




    worksheet5.write(0, 0, 'ID', bold)
    worksheet5.write(0, 1, 'Provision ID', bold)
    worksheet5.write(0, 2, 'Choice Name', bold)
    worksheet5.write(0, 3, 'Votes', bold)
    worksheet5.write(0, 4, 'Percentage', bold)
    worksheet5.set_column('C:C', 35)
 

    row = 1 
    choicerow = 1 
    for rf in provisions:
      myChoices = Choice.objects.all().filter(provision_id = rf.id)
      txtprovision = "'" + rf.provision
      worksheet4.write(row, 0, rf.id)
      worksheet4.write(row, 1, txtprovision, atop)
      worksheet4.write(row, 2, rf.comment, atop)
      worksheet4.write(row, 3, rf.cast_votes, votes)
      worksheet4.write(row, 4, rf.valid_votes, votes)
      worksheet4.write(row, 5, rf.invalid_votes, votes)
      worksheet4.set_row(row, textarea_height)
      row += 1


      for choice in myChoices:
        print 'Choice'
        print choice.id
        worksheet5.write(choicerow, 0, choice.id)
        worksheet5.write(choicerow, 1, choice.provision_id)
        worksheet5.write(choicerow, 2, choice.name)
        worksheet5.write(choicerow, 3, choice.votes, votes)
        worksheet5.write(choicerow, 4, choice.percentage)
        choicerow += 1
    

  
    book.close()

  
    # construct response
    output.seek(0)
    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=" + filename

    return response


def edit_election_general(request, election_id):
    election = Election.objects.get(id=election_id)
    form= ElectionEditForm(request.POST or None, instance = election)
    
    if form.is_valid():
        form.save() 
  
        return HttpResponseRedirect('/election/' + str(election.id) + '/general/')
    
    context = {
        'form': form,
        'election': election
    }

    return render(request, "election/forms/edit_election_general.html", context)

def edit_election_methods(request, election_id):
    election = Election.objects.get(id=election_id)
    form= ElectionMethodForm(request.POST or None, instance = election)
    
    if form.is_valid():
        form.save() 
        return HttpResponseRedirect('/election/' + str(election.id) + '/methods/')    
 
    context = {
        'form': form,
        'election': election
    }
    return render(request, "election/forms/edit_voting_methods.html", context)


def edit_election_rights(request, election_id):
    election = Election.objects.get(id=election_id)
    form= ElectionRightsForm(request.POST or None, instance = election)

    if form.is_valid():
        form.save() 
        #return detail_rights(request, election.id)
        return HttpResponseRedirect('/election/' + str(election.id) + '/rights/') 
  
    context = {
        'form': form,
        'election': election
    }
    return render(request, "election/forms/edit_election_rights.html", context)

def edit_election_reviews(request, election_id):
    election = Election.objects.get(id=election_id)
    form= IfesReviewForm(request.POST or None, instance = election)
    
    if form.is_valid():
        form.save()
        #return redirect('/allelections')
        return HttpResponseRedirect('/election/' + str(election.id) + '/reviews/')
        #return view_election_reviews(request, election.id)
    context = {
       'form': form,
       'election': election
    }
    return render(request, "election/forms/edit_election_review.html", context)



# election create view NEED this to redirect to the allelections url after saving     WATCH
def election_create_view(request):
    form=ElectionCreateForm(request.POST or None)
    if form.is_valid():
        newElection = form.save()
        #return redirect('/allelections')
        return view_election_general(request, newElection.pk)
    context = {
        'form': form,
        'election': election
    }
  
    return render(request, "election/forms/election_create.html", context)



def partyvote_create_view(request, election_id):
    election = Election.objects.get(id=election_id)
    form = PartyLinkForm()
    party = Party.objects.all()

    if request.method == 'POST':
        form = PartyLinkForm(request.POST)
        form.election = election 
        print(form.is_valid())
        if form.is_valid():

            form.save()
            return HttpResponseRedirect('/election/' + str(election.id) + '/parties/')

    context = {
        'form': form,
        'party': party,
        'election': election,
        'is_create': True
    }
    return render(request, "election/forms/partyvote_create.html", context)



def candidate_create_view(request, election_id):
    election = Election.objects.get(id=election_id)
    form = CandidateLinkForm()
    people = Person.objects.all()
    
    if request.method == 'POST':
        form = CandidateLinkForm(request.POST)
        form.election = election 
        print(form.is_valid())
        if form.is_valid():

            form.save()
            return HttpResponseRedirect('/election/' + str(election.id) + '/candidates/')
   
    context = { 
        'form': form,
        'people': people,
        'election': election,
        'is_create': True
    }
    return render(request, "election/forms/candidate_create.html", context)


def person_create(request, election_id):
  
    election = Election.objects.get(id=election_id)
    form = PersonLinkForm()
    
    
    if request.method == 'POST':
        form = PersonLinkForm(request.POST)
        form.election = election 
        if form.is_valid():

            newPerson = form.save()
            print('new Persion id: ', newPerson.pk)

            newCandidate = Candidate_votes()
            newCandidate.candidate = newPerson
            newCandidate.election = election
            newCandi = newCandidate.save()

            return HttpResponseRedirect('/election/' + str(election.id) + '/candidates/')

    context = { 
        'form': form,
        'election': election
    }
    return render(request, "election/forms/person_create.html", context)


def party_create(request, election_id):
    election = Election.objects.get(id=election_id)
    form = PartyForm()
    
    
    if request.method == 'POST':
        form = PartyForm(request.POST)
        form.election = election 
        if form.is_valid():

            newParty = form.save()
            print('new Party: ', newParty.pk)

            newPartyvote = Party_votes()
            newPartyvote.party = newParty
            newPartyvote.election = election
            newP = newPartyvote.save()

            return HttpResponseRedirect('/election/' + str(election.id) + '/parties/')
   
    context = { 
        'form': form,
        'election': election
    }
    return render(request, "election/forms/party_create.html", context)


def provision_view(request, pk):
    provision = Provision.objects.get(id=election_id)
    election = Election.objects.get(id=provision.election_id)
    choices = Choice.objects.all().filter(provision_id = pk)
  
    return render(request, 'election/show/provision_detail.html', {'provision': provision, 'election': election, 'choices': choices})





def provision_create_view(request, election_id):
    election = Election.objects.get(id=election_id)
    form=ProvisionLinkForm(request.POST or None)

    if request.method == 'POST':
        form = ProvisionLinkForm(request.POST)
        form.election = election 
        print(form.is_valid())
        if form.is_valid():

            form.save()
            
            return HttpResponseRedirect('/election/' + str(election.id) + '/provisions/')
    
    context = {
        'form': form,
        'election': election,
       'is_create': True
    }
    return render(request, "election/forms/provision_create.html", context)

 

def provision_edit(request, pk):
    provision = Provision_votes.objects.get(id=pk)
    election = Election.objects.get(id=provision.election_id)
    choices = Choice.objects.all().filter(provision_id = pk)
    form= ProvisionLinkForm(request.POST or None, instance = provision)
    
    if form.is_valid():
        form.save()
    
        return HttpResponseRedirect('/election/' + str(provision.election_id) + '/provisions/')
    
    context = {
        'form': form,
        'election': election,
        'choices': choices,
        'is_create': False,
        'provision_id': pk
    }
   
    return render(request, "election/forms/provision_create.html", context)


def provision_delete(request, pk):
    provision = Provision_votes.objects.get(id=pk)
    election = Election.objects.get(id=provision.election_id)
    print('provision delete: ', pk)
    provision.delete();
   
    return HttpResponseRedirect('/election/' + str(provision.election_id) + '/provisions/')
    

def choice_add(request, pk):
    provision = Provision_votes.objects.get(id=pk)
    choice = Choice()
    choice.name = request.POST.get('name', None)
    if request.POST.get('votes', None) == '' or request.POST.get('votes', None) == None:
        choice.votes = None
    else:
        choice.votes = request.POST.get('votes') 
    if request.POST.get('percentage', None) == '' or request.POST.get('percentage', None) == None:
        choice.percentage = None
    else:
        choice.percentage = request.POST.get('percentage', None)

    choice.provision = provision

    new_choice = choice.save()
    print(choice.pk)
    return JsonResponse( {
            'status': 'success',
            'choice_id': choice.pk
        })

def choice_edit(request, pk):
    provision = Provision_votes.objects.get(id=pk)
    choice_id = request.POST.get('choice_id', None)
    if choice_id:

        choice = Choice.objects.get(id=choice_id)
    else:
        return JsonResponse( {
            'status': 'failed',
        })

    choice.name = request.POST.get('name', None)
    if request.POST.get('votes', None) == '' or request.POST.get('votes', None) == None:
        choice.votes = None
    else:
        choice.votes = request.POST.get('votes') 
    if request.POST.get('percentage', None) == '' or request.POST.get('percentage', None) == None:
        choice.percentage = None
    else:
        choice.percentage = request.POST.get('percentage', None)

    choice.provision = provision

    new_choice = choice.save()
    print(choice.pk)
    return JsonResponse( {
            'status': 'success',
            'choice_id': choice.pk
        })



def choice_delete(request, pk):
    provision = Provision_votes.objects.get(id=pk)
    choice_id = request.POST.get('choice_id', None)
    if choice_id:
        choice = Choice.objects.get(id=choice_id)
        choice.delete()
        return JsonResponse( {
            'status': 'success'
        })
    else:
        return JsonResponse( {
            'status': 'failed',
        })

def partyvote_edit(request, pk):
    party = Party_votes.objects.get(id=pk)
    election = Election.objects.get(id=party.election_id)
    form= PartyLinkForm(request.POST or None, instance = party)
    
    if form.is_valid():
        form.save()
             
        return HttpResponseRedirect('/election/' + str(party.election_id) + '/parties/')
       
    context = {
        'form': form,
        'election': election,
        'party_id': pk,
        'is_create': False
    }
   
    return render(request, "election/forms/partyvote_create.html", context)



def candidate_edit(request, pk):
    candidate = Candidate_votes.objects.get(id=pk)
    election = Election.objects.get(id=candidate.election_id)
    form= CandidateLinkForm(request.POST or None, instance = candidate)
    
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/election/' + str(candidate.election_id) + '/candidates/')
   
    context = {
        'form': form,
        'election': election,
        'candidate_id': pk,
        'is_create': False
    }
   
    return render(request, "election/forms/candidate_create.html", context)


def candidate_delete(request, pk):
    candidate = Candidate_votes.objects.get(id=pk)
    election = Election.objects.get(id=candidate.election_id)
    print('candidate delete: ', pk)
    candidate.delete();

    return HttpResponseRedirect('/election/' + str(candidate.election_id) + '/candidates/')


def partyvote_delete(request, pk):
    partyvote = Party_votes.objects.get(id=pk)
    election = Election.objects.get(id=partyvote.election_id)
    partyvote.delete();
   
    return HttpResponseRedirect('/election/' + str(partyvote.election_id) + '/parties/')


def country(request, country_id=2):

    try:
        if request.GET.get('ID'):
            return redirect('country', country_id=int(request.GET.get('ID')))

        try:
            country = Country.objects.get(id=int(country_id))
        except ValueError:
            country = Country.objects.get(alpha2=str(country_id).upper())

    except (Country.DoesNotExist, ValueError):
        return redirect('countries')

    institution = Institution.objects.all().filter(country=country.id)

    election = Election.objects.only('cast_votes',
                                     'registered_voters',
                                     'registered_voters_date',
                                     'date',
                                     'name').order_by('date').filter(country=country.id, active=1)

    average = []

    try:
        for i, item in enumerate(election):
            if int(item.cast_votes) > 0 and int(item.registered_voters) > 0:
                election[i].participation = round((int(item.cast_votes) / int(item.registered_voters)) * 100, 2)
                average.append(election[i].participation)
            else:
                pass
    except (TypeError, AttributeError):
        pass

    # CALCULATE data for info section
    info = {'election_number': election.count()}
    i = 1
    registered_voters_empty = True
    while registered_voters_empty \
            and info['election_number'] > 0 \
            and election[info['election_number']-i].registered_voters > 0:
        if election[info['election_number']-i].registered_voters > 0:
            registered_voters_empty = False
            info['registered'] = election[info['election_number']-i].registered_voters
            info['registered_date'] = election[info['election_number']-i].registered_voters_date
        else:
            i = i + 1

    if not average:
        average = 0

    average = asarray(average)

    info['average_voter_turnout'] = average.mean()

    return render(request, 'country/post.html', {'country': country,
                                                 'institution': institution,
                                                 'elections': election,
                                                 'info': info})


def countries(request):

    countries = cache.get('countries')

    if not countries:
        countries = Country.objects.all().filter(active=1).select_related('region')[:20]
        cache.set('countries', countries, None)

    count = cache.get('countries_count')

    if not count:
        count = Country.objects.all().filter(active=1).count()
        cache.set('countries_count', count, None)

    return render(request, 'country/browse.html', {'countries': countries, 'count': count})


def digest(request):
    entry_list = cache.get('digest_entry_list')

    if not entry_list:
        entry_list = Digest.objects.order_by('-post_date').only('id',
                                                                'title',
                                                                'excerpt',
                                                                'post_date',
                                                                'slug')
        cache.set('digest_entry_list', entry_list, None)

    paginator = Paginator(entry_list, 25)  # Show 25 contacts per page
    page = request.GET.get('page')

    try:
        entries = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        entries = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        entries = paginator.page(paginator.num_pages)

    return render(request, 'digest/browse.html', {'entries': entries})


def digestCategory(request, slug='features'):
    try:
        entry_list = Category.objects.get(slug=slug).digest_set.order_by('-post_date').all()
        category = Category.objects.get(slug=slug)

        # entry_list = Digest.objects.order_by('-post_date').all().filter(=slug)
        paginator = Paginator(entry_list, 10)  # Show 10 per page
    except Category.DoesNotExist:
        return redirect('digest')

    page = request.GET.get('page')
    try:
        entries = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        entries = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        entries = paginator.page(paginator.num_pages)

    return render(request, 'digest/browse.html', {'entries': entries, 'category': category})


def digestEntry(request, post_id=5202):
    try:
        entry = Digest.objects.get(id=post_id)
    except Digest.DoesNotExist:
        return redirect('digest')

    return render(request, 'digest/post.html', {'entry': entry})


def ifesmap(request):

    election = cache.get('ifesmap')

    if not election:
        election = Election.objects.order_by('date').filter(date__gt=datetime.datetime.now().date(),
                                                            active=1
                                                            ).select_related('country',
                                                                             'institution'
                                                                             ).only('id',
                                                                                    'country__alpha3',
                                                                                    'country',
                                                                                    'institution',
                                                                                    'country__name',
                                                                                    'date',
                                                                                    'institution__name',
                                                                                    'country__id',
                                                                                    'institution__id')[:20]
        cache.set('ifesmap', election, None)

    return render(request, 'pages/map.html', {'election': election})


def pageView(request, slug='about'):
    page = cache.get('page_%s' % slug)

    if not page:
        try:
            page = Page.objects.get(slug=slug)
            cache.set('page_%s' % slug, page, None)
        except Page.DoesNotExist:
            raise Http404

    return render(request, 'pages/page.html', {'page': page})


def newsletter_preview(request, newsletter_id):
    newsletter = Newsletter.objects.get(pk=newsletter_id)

    return render(request, 'newsletter/preview.html', {'newsletter': newsletter})


def reports(request):

    return render(request, 'pages/reports.html')


def contact(request):
    return render(request, 'pages/contact.html')


@login_required
def myeguideView(request):

    # Forced to excute the relationship manually due to an error in production
    # site that apparently is due to a problem with python 2.7.4 and django 1.5.4

    from django.db import connection
    cursor = connection.cursor()
    cursor.execute("SELECT country_id from eguide_eguideuser_favorite_country where eguideuser_id = %s", [request.user.id])

    countries = cursor.fetchall()
    country_ids = [item[0] for item in countries]

    elections = Election.objects.filter(active=1,
                                        country__in=country_ids).only('id',
                                                                      'country__id',
                                                                      'country__flag',
                                                                      'country__name',
                                                                      'institution__name',
                                                                      'date',
                                                                      'election_status__id',
                                                                      'election_status__name',
                                                                      'id',
                                                                      'name',
                                                                      'institution__institution_type__name'
                                                                      ).select_related('country',
                                                                                       'institution',
                                                                                       'election_status')[:30]
    digest = Digest.objects.filter(active=1, country__in=country_ids).order_by('-post_date').only('id',
                                                                                                  'title',
                                                                                                  'excerpt',
                                                                                                  'post_date',
                                                                                                  'slug')[:20]

    return render(request, 'myeguide/profile.html', {'elections': elections,
                                                     'digest': digest})


@login_required
def myeguideEditProfile(request):
    user = EguideUser.objects.get(id=request.user.id)
    form = EguideUserForm(instance=user)

    if request.method == 'POST':
        form = EguideUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('myeguide')

    return render(request, 'myeguide/editprofile.html', {'form': form})


@permission_required('newsletter.change_newsletter', login_url='/myeguide/login/')
def newsletter_start(request):
    if request.method == 'POST':
        newsletter_ajax = request.POST
        mailgun = Mailgun()

        newsletter = Newsletter.objects.get(pk=newsletter_ajax['id'])
        r = mailgun.send_mail(subject=newsletter.subject, plaintext=newsletter.body, html=newsletter.body,
                              campaign=newsletter.id, to_address=newsletter.to)
        response = HttpResponse(r['message'])
        newsletter.status = r['message']
        newsletter.active = True
        newsletter.save()
        response.status_code = 200

    return response

