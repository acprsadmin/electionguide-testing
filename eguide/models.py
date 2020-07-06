from django.db import models
from django.db.models.signals import post_save, post_delete
from django.core.cache import cache
from django.dispatch import receiver

from mailgun.methods import Mailgun
from smart_selects.db_fields import ChainedForeignKey
from allauth.account.signals import email_confirmed

from eguide import cache as eguide_cache


# Abstract Model

class CommonInfo(models.Model):
    active = models.BooleanField('Enabled?', default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Region(CommonInfo):
    name = models.CharField('Region Name', max_length=400, help_text='e.g. North America')

    def __unicode__(self):
            return self.name


class Country(CommonInfo):
    name = models.CharField('Country Name', db_index=True, max_length=200, help_text='e.g. France')
    official_name = models.CharField('Official Name', max_length=400, blank=True, help_text='e.g. French Republic')
    flag = models.ImageField('Flag File', upload_to='flags', blank=True,
                             help_text='Upload the flag. Accepted image files are JPG, PNG and GIF',)
    population = models.IntegerField('Population', null=True, blank=True,
                                     help_text='Population must be entered as numbers with no commas or separators,' +
                                     ' e.g. 39456123',)
    population_male = models.IntegerField('Male Population', null=True, blank=True,
                                          help_text='Population must be entered as numbers with no commas or '
                                          'separators, e.g. 39456123',)

    population_female = models.IntegerField('Female Population', null=True, blank=True,
                                            help_text='Population must be entered as numbers with no commas or '
                                            'separators, e.g. 39456123',)
    population_date = models.DateField('Population Date', null=True, blank=True,
                                       help_text='The date the population is retrieved')
    population_source = models.TextField('Population Source', blank=True,
                                         help_text='The source this population is retrieved from. If it\'s a URL ' +
                                         'make sure to hyperlink the URL',)
    description = models.TextField('Description', blank=True, null=True)
    alpha2 = models.CharField('ISO ALPHA-2 Code', max_length=2, blank=True)
    alpha3 = models.CharField('ISO ALPHA-3 Code', max_length=3)
    region = models.ForeignKey(Region)
    code = models.CharField('Country Name', max_length=3, null=True, blank=True)
    cedaw_signatory = models.CharField('CIDAW signatory', max_length=250, null=True, blank=True,
                                       help_text='Leave blank is the answer is NO. e.g. Yes (since 24 July 1980)')
    cedaw_ratified = models.CharField('CIDAW ratified', max_length=250, null=True, blank=True,
                                      help_text='Leave blank is the answer is NO. e.g. Yes (since 24 July 1985)')
    hdi_position = models.IntegerField('Human Development Index (HDI) Position', default=0)
    sigi = models.CharField('Social Institutions and Gender Index', max_length=250, null=True, blank=True,
                            help_text='22nd out of 86 non-OECD countries (latest rankings are from 2012)')

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"
        ordering = ['name']

    def __unicode__(self):
            return self.name


class Institution_type(CommonInfo):
    name = models.CharField('Institution Type', help_text='Type of the institution, e.g. lower house', max_length=400)

    class Meta:
        verbose_name = "Institution Type"

    def __unicode__(self):
            return self.name


class Election_system(CommonInfo):
    name = models.CharField('Election System', max_length=400,
                            help_text='Name of the election system, e.g. block vote',)
    description = models.TextField('Description', blank=True, null=True, help_text='Description of the system',)
    election = models.BooleanField('Is this an election?', default=False,
                                   help_text='We have non-election systems in this list, such as appointment ' +
                                   'by president. If it is an election based system, check this box.',)

    class Meta:
        verbose_name = "Election System"

    def __unicode__(self):
            return self.name


class Institution(CommonInfo):
    name = models.CharField('Name', help_text='Name of the instituion, e.g. French Parliament', max_length=250)
    foriegn_name = models.CharField('Foreign Name', help_text='Name in local language, e.g. Parlement francais',
                                    max_length=400, blank=True, null=True)
    description = models.TextField('Description', help_text='Description of the institution', blank=True)
    country = models.ForeignKey(Country)
    institution_type = models.ForeignKey(Institution_type)
    system = models.ForeignKey(Election_system, blank=True, null=True)
    quota = models.CharField('Gender Quota', max_length=350, null=True, blank=True,
                             help_text='e.g. Yes: "Legislated Candidate Quotas" in the National Constituent Assembly')

#     class Meta:
#         unique_together = ('name', 'country', 'institution_type')

    def __unicode__(self):
            return self.name


class Election_status(CommonInfo):
    name = models.CharField('Status', help_text='Status of the electoin, e.g. tentative', max_length=400)

    class Meta:
        verbose_name = "Election Status"
        verbose_name_plural = "Election Statuses"

    def __unicode__(self):
            return self.name


class Election_type(CommonInfo):
    name = models.CharField('Status', help_text='Status of the electoin, e.g. tentative', max_length=400)

    class Meta:
        verbose_name = "Election Type"

    def __unicode__(self):
            return self.name




class Electoral_system(CommonInfo):
    name = models.CharField('Electoral System Name', help_text='', max_length=400)

    class Meta:
        verbose_name = "Electoral System"

    def __unicode__(self):
            return self.name



class Election_scope(CommonInfo):
    name = models.CharField('Election Scope Name', help_text='', max_length=400)

    class Meta:
        verbose_name = "Election Scope"

    def __unicode__(self):
            return self.name




class Election(CommonInfo):

    VOTING_METHODS = (
        (1, 'In Person Voting'),
        (2, 'Early Voting'),
        (3, 'By Mail Voting'),
        (4, 'Online Voting')
        )

    YESNONULL = (
        (1, 'Yes'),
        (2, 'No')
        )

    YEAR_RANGE = (
        (1990, '1990'),
        (1991, '1991'),
        (1992, '1992'),
        (1993, '1993'),
        (1994, '1994'),
        (1995, '1995'),
        (1996, '1996'),
        (1997, '1997'),
        (1998, '1998'),
        (1999, '1999'),
        (2000, '2000'),
        (2001, '2001'),
        (2002, '2002'),
        (2003, '2003'),
        (2004, '2004'),
        (2005, '2005'),
        (2006, '2006'),
        (2007, '2007'),
        (2008, '2008'),
        (2009, '2009'),
        (2010, '2010'),
        (2011, '2011'),
        (2012, '2012'),
        (2013, '2013'),
        (2014, '2014'),
        (2015, '2015'),
        (2016, '2016'),
        (2017, '2017'),
        (2018, '2018'),
        (2019, '2019'),
        (2020, '2020'),
        (2021, '2021'),
        (2022, '2022'),
        (2023, '2023'),
        (2024, '2024'),
        (2025, '2025'),
        (2026, '2026'),
        (2027, '2027'),
        (2028, '2028'),
        (2029, '2029'),
        (2030, '2030'),
        (2031, '2031'),
        (2032, '2032'),
        (2033, '2033'),
        (2034, '2034'),
        (2035, '2035'),
        (2036, '2036'),
        (2037, '2037'),
        (2038, '2038'),
        (2039, '2039')

        )

    name = models.CharField('Election Name', help_text='Name of the election, e.g. Parliamentary elections round 1',
                            max_length=250)
    date = models.DateField('Election Date', db_index=True, null=True, blank=True)
    description = models.TextField('Description', blank=True)
    female_elected = models.IntegerField('Number of female elected leaders', default=0,
                                         help_text='Only enter a number of female elected officials such as'
                                         ' parliament members, presidents, members of the assembly, etc.')
    registered_voters = models.IntegerField('Registered Voters', null=True, blank=True,
                                            help_text='Number of registered voters with no commas or separators, ' +
                                            'e.g. 39456123',)
    registered_voters_male = models.IntegerField('Male Registered Voters', null=True, blank=True,
                                                 help_text='Number of registered voters with no commas or '
                                                 'separators, e.g. 39456123',)
    registered_voters_female = models.IntegerField('Female Registered Voters', null=True, blank=True,
                                                   help_text='Number of registered voters with no commas or '
                                                   'separators, e.g. 39456123',)
    registered_voters_date = models.DateField('Date Obtained', null=True, blank=True,
                                              help_text='The date the number of egistered voters is retrieved',)
    registered_voters_source = models.TextField('Source', blank=True,
                                                help_text='The source the registered voters number is retrieved ' +
                                                'from. If it\'s a URL make sure to hyperlink the URL',)
    cast_votes = models.IntegerField('Cast Votes', null=True, blank=True,
                                     help_text='Number of cast votes with no commas or separators, e.g. 39456123',)
    valid_votes = models.IntegerField('Valid Votes', null=True, blank=True,
                                      help_text='Number of valid votes with no commas or separators, e.g. 39456123',)
    invalid_votes = models.IntegerField('Invalid Votes', null=True, blank=True,
                                        help_text='Number of invalid votes with no commas or separators, ' +
                                        'e.g. 39456123',)
    ballot_description = models.TextField('Ballot Description', null=True, blank=True,
                                          help_text='Description of the ballot',)
    ballot_file = models.ImageField('Ballot image file', upload_to='flags', null=True, blank=True,
                                    help_text='Upload the ballot. Accepted image files are JPG, PNG and GIF',)
    institution = models.ForeignKey(Institution, null=True, blank=True)
    country = models.ForeignKey(Country, related_name='election_country')
    # institution = ChainedForeignKey(Institution, chained_field="country", chained_model_field="country_id",
    #                                 show_all=False, auto_choose=True, null=True, blank=True,
    #                                 related_name='election_institution')
    election_status = models.ForeignKey(Election_status)
    election_type = models.ForeignKey(Election_type)
    election_type_temp = models.IntegerField(blank=True, null=True)
    show_results = models.BooleanField('Show Results?', default=False)
    legacy_id = models.IntegerField(blank=True, null=True)
    show_seat_shares = models.BooleanField('Show Seat Shares?', default=False)

    #step-two-fields_migration 005
    election_range_start_date = models.DateField('Election Range Start Date', null=True, blank=True, help_text='',)
    election_range_end_date = models.DateField('Election Range End Date', null=True, blank=True, help_text='',)
    election_range_source = models.CharField('Range Date Source', max_length=250, help_text='', null=True, blank=True)
    election_declared_start_date = models.DateField('Election Declared Start', null=True, blank=True, help_text='',)
    election_declared_end_date = models.DateField('Election Declared End', null=True, blank=True, help_text='',)
    election_declared_source = models.CharField('Election declared date source', max_length=250, null=True, blank=True)
    electoral_system  = models.ForeignKey(Electoral_system, null=True, blank=True)
    electoral_system_other = models.CharField('Electoral system notes', max_length=500, null=True, blank=True)
    electoral_system_source = models.CharField('Electoral System Source', max_length=500, null=True, blank=True)
    source_website = models.CharField('Election Website', max_length=250, null=True, blank=True)
    administering_election_commission_website = models.CharField('Election Commission Website', max_length=250, null=True, blank=True)
    election_candidate_filing_deadline = models.DateField('Candidate Filing  Deadline', null=True, blank=True)
    election_candidate_filing_deadline_source = models.CharField('Candidate Filing Deadline Source', max_length=250, null=True, blank=True)
    voting_age_minimum_inclusive = models.IntegerField('Voting Age Minimum', null=True, help_text='', blank=True)
    voting_age_minimum_source = models.CharField('Voting Age Minimum Source', max_length=500, null=True, blank=True)
    election_blackout_start_date = models.DateField('Blackout Date Start', null=True, blank=True, )
    election_blackout_end_date = models.DateField('Blackout Date End', null=True, blank=True,)
    blackout_date_source = models.CharField('Blackout Date Source', max_length=500, null=True, blank=True)
    #step-two-fields migration 006
    support_electoral_rights = models.BooleanField('Support Electoral Rights?', default=False, help_text='Check if true')
    support_electoral_rights_details = models.TextField('Support Electoral Rights Detail', blank=True, null=True)
    restrict_electoral_rights = models.BooleanField('Restrict Electoral Rights?', default=False, help_text='Check if true')
    restrict_electoral_rights_details = models.TextField('Restrict Electoral Rights Details', blank=True, null=True)
    electoral_rights_info_source = models.CharField('Electoral Rights Info Source', max_length=500, null=True, blank=True)
    hate_speech_prohibition = models.TextField('Hate Speech Prohibited Detials', null=True, blank=True)
    hate_speech_prohibition_source = models.CharField('Hate Speech Source', max_length=500, null=True, blank=True)
    hate_speech_details = models.TextField('Hate Speech Details', blank=True, null=True)
    disinformation_prohibition = models.TextField('Disinformation Prohibited Details', null=True, blank=True)
    disinformation_prohibition_source = models.CharField('Disinformation Source', max_length=500, null=True, blank=True)
    disinformation_details = models.TextField('Disinforamtion Details', blank=True, null=True)

    #step-two-fields migration 007
    inperson_voting_enabled = models.BooleanField('In Person Voting Enabled?', default=False, help_text='Check this to publish method to FB json')
    inperson_voting_start = models.DateField('In Person Voting Method Start', null=True, blank=True,)
    inperson_voting_end = models.DateField('In Person Voting Method End', null=True, blank=True,)
    inperson_voting_instructions = models.TextField('In Person Voting Method Instructions', blank=True, null=True)
    inperson_voting_excuse_required  = models.BooleanField('In Person Voting Method Excuse Required?', default=False)
  
    early_voting_enabled = models.BooleanField('Early Voting Enabled?', default=False, help_text='Check this to publish method to FB json')
    early_voting_start = models.DateField('Early Voting Method Start', null=True, blank=True,)
    early_voting_end = models.DateField('Early Voting Method End', null=True, blank=True,)
    early_voting_instructions = models.TextField('Early Voting Method Instructions', blank=True, null=True)
    early_voting_excuse_required  = models.BooleanField('Early Voting Method Excuse Required?', default=False)
  
    mail_voting_enabled = models.BooleanField('Mail Voting Enabled?', default=False, help_text='Check this to publish method to FB json')
    mail_voting_start = models.DateField('Mail Voting Method Start', null=True, blank=True,)
    mail_voting_end = models.DateField('Mail Voting Method End', null=True, blank=True,)
    mail_voting_instructions = models.TextField('Mail Voting Method Instructions', blank=True, null=True)
    mail_voting_excuse_required  = models.BooleanField('Mail Voting Method Excuse Required?', default=False)
  
    online_voting_enabled = models.BooleanField('Online Voting Enabled?', default=False, help_text='Check this to publish method to FB json')
    online_voting_start = models.DateField('Online Voting Method Start', null=True, blank=True,)
    online_voting_end = models.DateField('Online Voting Method End', null=True, blank=True,)
    online_voting_instructions = models.TextField('Online Voting Method Instructions', blank=True, null=True)
    online_voting_excuse_required  = models.BooleanField('Online Voting Method Excuse Required?', default=False)

    #step-two-fields migration 008
    legal_consultant_comments = models.TextField('Consultant Comments', blank=True)
    legal_consultant_confirmation = models.BooleanField('Legal Consultant Confirmation', default=False, help_text='Check if confirmed')
    legal_consultant_confirmation_date = models.DateField('Legal Consultant Confirmation Date', null=True, blank=True,)
    legal_consultant_name = models.CharField('Legal Consultant Name', max_length=250, null=True, blank=True)
    cso_comments = models.TextField('CSO Comments', blank=True)
    cso_confirmation = models.BooleanField('CSO Confirmation', default=False, help_text='Check if confirmed')
    cso_confirmation_date = models.DateField('CSO Confirmation Date', null=True, blank=True,)
    cso_confirmation_name = models.CharField('CSO Confirmation Name', max_length=250, null=True, blank=True)
    embassy_comments = models.TextField('EMB Comments', blank=True)
    embassy_confirmation = models.BooleanField('EMB Confirmation', default=False, help_text='Check if confirmed')
    embassy_confirmation_date = models.DateField('EMB Confirmation Date', null=True, blank=True,)
    embassy_confirmation_name = models.CharField('EMB Confirmation Name', max_length=250, null=True, blank=True)
    ifes_comments = models.TextField('IFES Comments', blank=True)
    ifes_confirmation = models.BooleanField('IFES Confirmation', default=False, help_text='Check if confirmed')
    ifes_confirmation_date = models.DateField('IFES Confirmation Date', null=True, blank=True,)
    ifes_confirmation_name = models.CharField('IFES Confirmation Name', max_length=250, null=True, blank=True)

    #step-three-migrated migration 009
    voter_registration_deadline = models.DateField('Voter Registration Deadline', null=True, blank=True,)

    #step-three-migrated migration 010
    election_scope = models.ForeignKey(Election_scope, null=True, blank=True, default=1, help_text="*NEW*")
    is_national_exec = models.BooleanField('NATIONAL_EXEC', default=False, help_text='Check if applicable')
    is_national_upper = models.BooleanField('NATIONAL_UPPER', default=False, help_text='Check if applicable')
    is_national_lower = models.BooleanField('NATIONAL_LOWER', default=False, help_text='Check if applicable')
    is_national_legislative = models.BooleanField('NATIONAL_LEGISLATIVE', default=False, help_text='Check if applicable')

    is_delayed_covid19 = models.BooleanField('Election Delayed by Covid-19', default=False, help_text='Check if true')
    original_election_year = models.IntegerField('Original Election Year', choices=YEAR_RANGE, null=True, blank=True,
                                                   help_text='Original Year of the Election')
    is_submitted = models.BooleanField('Submitted for Approval', default=False)
    submitted_by = models.IntegerField('Submitted by', null=True, blank=True)
    is_published = models.BooleanField('Approved for Publication', default=False)
    published_by = models.IntegerField('Published by', null=True, blank=True)
    primary_voting_method = models.IntegerField('Primary Voting Method', choices=VOTING_METHODS, null=True, blank=True,)
    #0018
    election_range_notes = models.TextField('Election Date Range Notes', blank=True)
    election_candidate_filing_deadline_notes = models.TextField('Candidate Filing Deadline Notes', blank=True)
    submitted_by_name = models.CharField('Person Name submitting for publication', max_length=250, null=True, blank=True)
    published_by_name = models.CharField('Person  Name publisher', max_length=250, null=True, blank=True)
    #0019
    yn_support_electoral_rights = models.IntegerField('Support Electoral Rights?', choices=YESNONULL, null=True, blank=True)
    yn_restrict_electoral_rights = models.IntegerField('Restrict Electoral Rights?', choices=YESNONULL, null=True, blank=True,)
    yn_hate_speech_prohibited = models.IntegerField('Is Hate Speech Prohibited?', choices=YESNONULL, null=True, blank=True)
    yn_disinformation_prohibited = models.IntegerField('Is Disinformation Prohibited?', choices=YESNONULL, null=True, blank=True)
    yn_inperson_voting_excuse_required  = models.IntegerField('In Person Voting Method Excuse Required?', choices=YESNONULL, null=True, blank=True)
    yn_early_voting_excuse_required  = models.IntegerField('Early Voting Method Excuse Required?', choices=YESNONULL, null=True, blank=True)
    yn_mail_voting_excuse_required  = models.IntegerField('Mail Voting Method Excuse Required?', choices=YESNONULL, null=True, blank=True)
    yn_online_voting_excuse_required  = models.IntegerField('Online Voting Method Excuse Required?', choices=YESNONULL, null=True, blank=True)

    #0020
    api_access_date  = models.DateTimeField('Last Facebook Download Date', null=True, blank=True, help_text='',)
    #0021  revert declared start to date
    #0022  revert rest of datetime to date
    #0023  add time fields below
    inperson_voting_start_time = models.TimeField('In Person Voting Start Time', null=True, blank=True, help_text='Optional',)
    inperson_voting_end_time = models.TimeField('In Person Voting End Time', null=True, blank=True, help_text='Optional',)
    mail_voting_start_time = models.TimeField('Mail Voting Start Time', null=True, blank=True, help_text='Optional',)
    mail_voting_end_time = models.TimeField('Mail Voting End Time', null=True, blank=True, help_text='Optional',)
    early_voting_start_time = models.TimeField('Early Voting Start Time', null=True, blank=True, help_text='Optional',)
    early_voting_end_time = models.TimeField('Early Voting End Time', null=True, blank=True, help_text='Optional',)
    online_voting_start_time = models.TimeField('Early Voting  Start Time', null=True, blank=True, help_text='Optional',)
    online_voting_end_time = models.TimeField('Early Voting End Time', null=True, blank=True, help_text='Optional',)
    election_declared_start_time = models.TimeField('Declared Start Time', null=True, blank=True, help_text='Optional',)
    election_declared_end_time = models.TimeField('Declared End Time', null=True, blank=True, help_text='Optional',)   
    election_blackout_start_time = models.TimeField('Blackout  Start Time', null=True, blank=True, help_text='Optional',)
    election_blackout_end_time = models.TimeField('Blackout End Time', null=True, blank=True, help_text='Optional',)
    voter_registration_deadline_time = models.TimeField('Voter Registration Deadline Time', null=True, blank=True, help_text='Optional',)
    election_candidate_filing_deadline_time = models.TimeField('Candidate Filing  Deadline Time', null=True, blank=True, help_text='Optional',)


#     class Meta:
#         unique_together = ('name', 'institution')

    def __unicode__(self):
            return self.name
#
#     def get_absolute_url(self):
#         return reverse('election', args=[str(self.id)])
    def countryname(self):
        queryset = Country.objects.get(id=self.country_id).\
                   only('id', 'name', 'alpha2')

        return  queryset.name
   
    def calcelectiondate(self):
        if self.election_declared_start_date:
            calcdate = self.election_declared_start_date
        elif self.election_range_start_date:
            calcdate = self.election_range_start_date
        elif date:
            calcdate = self.date
        else:
            calcdate = None

        return calcdate

    #def get_absolute_url(self):
    #    return reverse('viewelection', kwargs={'election_id': self.pk})

  

class Election_Demo(CommonInfo):

    election_key = None
    election_id = None
    election_name = None
    original_election_year = None
    election_range_start_date = None
    election_range_end_date = None
    is_delayed_covid19 = None
    election_declared_start_date = None
    election_declared_end_date = None
    election_type = None
    electoral_system = None
    electoral_system_other = None
    administering_election_commission_website = None
    source = None
    district = None
    election_candidate_filing_deadline = None
    voter_registration_deadline = None
    voting_age_minimum_inclusive = None
    voting_methods = None
    third_party_verified = None

    def __unicode__(self):
            return self.name

    def clear(self):
        self.election_key = None
        self.election_id = None
        self.election_name = None
        self.original_election_year = None
        self.election_range_start_date = None
        self.election_range_end_date = None
        self.is_delayed_covid19 = None
        self.election_declared_start_date = None
        self.election_declared_end_date = None
        self.election_type = None
        self.electoral_system = None
        self.electoral_system_other = None
        self.administering_election_commission_website = None
        self.source = None
        self.district = None
        self.election_candidate_filing_deadline = None
        self.voter_registration_deadline = None
        self.voting_age_minimum_inclusive = None
        self.voting_methods = None
        self.third_party_verified = None

class Election_API(CommonInfo):

    election_name = None

    def __unicode__(self):
            return self.name

    def clear(self):
        self.election_name = None




class Party_type(CommonInfo):
    name = models.CharField('Party Type', help_text='Type of the party, e.g. alliance', max_length=400)

    class Meta:
        verbose_name = "Party Type"

    def __unicode__(self):
            return self.name


class Party(CommonInfo):
    name = models.CharField('Party Name', max_length=250, help_text='Name of the party, e.g. Socialist Party',)
    foreign_name = models.CharField('Foreign Name', max_length=400, help_text='Name of the party in the local ' +
                                    'langauge, e.g. Parti socialiste',)
    url = models.CharField('URL', max_length=400, blank=True,
                           help_text='Party\'s official website. make sure to include http:// in front of the ' +
                           'address. e.g. http://www.google.com',)
    description = models.TextField('Description', blank=True, help_text='Description of the party',)
    country = models.CharField('Country', max_length=200)
    type = models.ForeignKey(Party_type, blank=True, null=True)
    legacy_id = models.IntegerField(blank=True, null=True, unique=True)

    class Meta:
        verbose_name = "Party"
        verbose_name_plural = "Parties"

    def __unicode__(self):
            return self.country + ' | ' + self.name


class Person(CommonInfo):

    GENDER_LIST = (
        ('f', 'Female'),
        ('m', 'Male'),
    )

    name = models.CharField('Firstname', max_length=250, help_text='Firstname of the person in English, e.g. ' +
                            'Vladimir',)
    lastname = models.CharField('Lastname', help_text='Lastname of the person in English, e.g. Putin', max_length=250)
    gender = models.CharField('Gender', max_length=400, choices=GENDER_LIST, null=True, blank=True)
    party = models.ForeignKey(Party, blank=True, null=True)
    url = models.CharField('URL', max_length=400, blank=True, help_text='Person\'s official website. make sure ' +
                           'to include http:// in front of the address. e.g. http://www.google.com',)
    description = models.TextField('Description', help_text='Description of the person', blank=True)
    country = models.CharField('Country', max_length=200)
    legacy_id = models.IntegerField(blank=True, null=True, unique=True)

    def __unicode__(self):
            return self.country + ' | ' + self.lastname


class Party_votes(CommonInfo):
    party = models.ForeignKey(Party)
    election = models.ForeignKey(Election)
    seats_won = models.IntegerField('Seats won', help_text='Number of seats won, e.g. 34', null=True, blank=True)
    votes = models.IntegerField('Votes', null=True, blank=True, help_text='Votes for this party with no commas ' +
                                'or separators, e.g. 39456123',)
    percentage = models.DecimalField('Percentage', max_digits=12, decimal_places=2, null=True, blank=True,
                                     help_text='Percentage of votes for this choice with no commas and only two ' +
                                     'decimals, e.g. 23.12',)
    description = models.TextField('Description', help_text='Description of the person', blank=True)
    legacy_id = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = "Party Vote"

    def __unicode__(self):
#             return self.party.country.name+': '+self.party.name
        return self.party.name


class Candidate_votes(CommonInfo):
    candidate = models.ForeignKey(Person)
    election = models.ForeignKey(Election)
    votes = models.IntegerField('Votes', null=True, blank=True,
                                help_text='Votes for this candidate with no commas or separators, e.g. 39456123',)
    percentage = models.DecimalField('Percentage', max_digits=12, decimal_places=2, null=True, blank=True,
                                     help_text='Percentage of votes for this candidate with no commas and only ' +
                                     'two decimals, e.g. 23.12',)
    legacy_id = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = "Candidate Vote"
#         unique_together = ('candidate', 'election',)

    # def __unicode__(self):
    #         return self.candidate


class Provision_votes(CommonInfo):
    election = models.ForeignKey(Election)
    provision = models.TextField('Referendum question', help_text='Name of the provision in English', blank=True)
    comment = models.TextField('Comment', blank=True)
    cast_votes = models.IntegerField('Cast Votes', null=True, blank=True,
                                     help_text='Number of cast votes with no commas or separators, e.g. 39456123',)
    valid_votes = models.IntegerField('Valid Votes', null=True, blank=True,
                                      help_text='Number of valid votes with no commas or separators, e.g. 39456123',)
    invalid_votes = models.IntegerField('Invalid Votes', null=True, blank=True, help_text='Number of invalid ' +
                                        'votes with no commas or separators, e.g. 39456123',)
    legacy_id = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = "Provision"

    def __unicode__(self):
        return self.election.name

    def electionname(self):
        queryset = Election.objects.get(id=self.election.id).only('id', 'name')

        return  queryset.name


    #or i thought something like this in the provision model
    def getChoices(self):
        choices = Choice.objects.all().filter(provision_id = self.pk)
        if len(choices) > 0:
            return  choices
        else:
            return None




class Choice(CommonInfo):
    name = models.CharField('Provision choice', help_text='Provision choice, e.g. Yes', max_length=250)
    votes = models.IntegerField('Votes', null=True, blank=True,
                                help_text='Votes for this choice with no commas or separators, e.g. 39456123',)
    percentage = models.DecimalField('Precentage', max_digits=12, decimal_places=2, null=True, blank=True,
                                     help_text='Percentage of votes for this choice with no commas and only two ' +
                                     'decimals, e.g. 23.12',)
    provision = models.ForeignKey(Provision_votes)

#     class Meta:
#         unique_together = ('name', 'provision',)

    def __unicode__(self):
            return self.name


class Newsletter(CommonInfo):
    subject = models.CharField('Newsletter\'s Subject', max_length=400)
    to = models.CharField('To:', max_length=400)
    cc = models.CharField('CC:', max_length=400, null=True, blank=True)
    bcc = models.CharField('BCC:', max_length=400, null=True, blank=True)
    body = models.TextField('Newsletter\'s body')
    status = models.CharField('Status', max_length=250, null=True, blank=True)
    delivered = models.IntegerField(null=True, blank=True)
    complained = models.IntegerField(null=True, blank=True)
    clicked = models.IntegerField(null=True, blank=True)
    opened = models.IntegerField(null=True, blank=True)
    dropped = models.IntegerField(null=True, blank=True)
    bounced = models.IntegerField(null=True, blank=True)
    sent = models.IntegerField(null=True, blank=True)
    unsubscribed = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
            return self.subject


class Author(CommonInfo):
    name = models.CharField('Author Full Name', help_text='e.g. Ernest Hemingway', max_length=250)
    email = models.CharField('Author\'s Email Address', help_text='e.g. hemingway@gmail.com', max_length=350,
                             null=True, blank=True)
    biography = models.TextField('Short Biography', null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class Category(CommonInfo):
    name = models.CharField('Category Name', max_length=250)
    slug = models.CharField('Slug', max_length=255, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Categories"

    def __unicode__(self):
            return self.name


class Digest(CommonInfo):
    title = models.CharField('Title', max_length=250)
    slug = models.CharField('slug', max_length=255, unique=True)
    body = models.TextField('Body', null=True, blank=True)
    excerpt = models.TextField('Excerpt', null=True, blank=True)
    post_date = models.DateTimeField('Date Posted')
    post_modified = models.DateTimeField('Date Modified')
    image = models.ImageField('Image', help_text='Accepted image files are JPG, PNG and GIF', upload_to='digest')
    author = models.ForeignKey(Author)
    country = models.ManyToManyField(Country, blank=True, )
    category = models.ManyToManyField(Category, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Digest"
        ordering = ['-post_date']

    def __unicode__(self):
            return self.title


class Page(CommonInfo):
    title = models.CharField('Title', max_length=250)
    slug = models.CharField('slug', max_length=250, unique=True)
    body = models.TextField('Body', null=True, blank=True)

    def __unicode__(self):
            return self.title

from django.contrib.auth.models import AbstractUser, UserManager


class EguideUser(AbstractUser):
    AGE_GROUP = (
        ('Under 18', 'Under 18'),
        ('18-25', '18-25'),
        ('26-29', '26-29'),
        ('30-39', '30-39'),
        ('40-49', '40-49'),
        ('50-59', '50-59'),
        ('Over 60', 'Over 60'),
    )

    GENDER_LIST = (
        ('Male', 'Female'),
        ('Female', 'Male'),
    )

    EDUCATION_LIST = (
        ('Grammar/Middle School', 'Grammar/Middle School'),
        ('High School Diploma', 'High School Diploma'),
        ('Some College', 'Some College'),
        ('Bachelor\'s Degree', 'Bachelor\'s Degree'),
        ('Some Graduate School', 'Some Graduate School'),
        ('Graduate Degree', 'Graduate Degree'),
        ('PhD', 'PhD'),
        ('Other', 'Other'),
    )

    OCCUPATION_LIST = (
        ('Accounting/Finance', 'Accounting/Finance'),
        ('Executive/Senior Management', 'Executive/Senior Management'),
        ('Professional/Managerial', 'Professional/Managerial'),
        ('Technical/Engineering', 'Technical/Engineering'),
        ('Administrative/Secretarial', 'Administrative/Secretarial'),
        ('Sales/Marketing/Advertising', 'Sales/Marketing/Advertising'),
        ('Customer Service/Support', 'Customer Service/Support'),
        ('College/University Faculty', 'College/University Faculty'),
        ('College/University Student', 'College/University Student'),
        ('K-12 Student', 'K-12 Student'),
        ('Writer/Journalist', 'Writer/Journalist'),
        ('Homemaker', 'Homemaker'),
        ('Retired', 'Retired'),
        ('Currently Not Employed', 'Currently Not Employed'),
        ('Other', 'Other'),
    )

    ORGANIZATION_TYPE_LIST = (
        ('Advertising/Media/Public Relation', 'Advertising/Media/Public Relation'),
        ('Agriculture/Forestry', 'Agriculture/Forestry'),
        ('Agriculture/Forestry', 'Agriculture/Forestry'),
        ('Architecture/Engineering/Construction', 'Architecture/Engineering/Construction'),
        ('Consulting', 'Consulting'),
        ('Entertainment', 'Entertainment'),
        ('Finance/Banking/Accounting', 'Finance/Banking/Accounting'),
        ('Government', 'Government'),
        ('Hospitality/Travel', 'Hospitality/Travel'),
        ('Internet-Related Services', 'Internet-Related Services'),
        ('Legal Services', 'Legal Services'),
        ('Manufacturing/distribution', 'Manufacturing/distribution'),
        ('Marketing/Communications', 'Marketing/Communications'),
        ('Medical Services', 'Medical Services'),
        ('Nonprofit', 'Nonprofit'),
        ('Printing/Graphics', 'Printing/Graphics'),
        ('Sales', 'Sales'),
        ('Software Development', 'Software Development'),
        ('Television/Radio/Print Publishing', 'Television/Radio/Print Publishing'),
        ('Transportation/Utilities', 'Transportation/Utilities'),
        ('Wholesale/Retail', 'Wholesale/Retail'),
        ('Other', 'Other'),
    )

    age = models.CharField('Age', max_length=400, choices=AGE_GROUP, null=True, blank=True)
    gender = models.CharField('Gender', max_length=400, choices=GENDER_LIST, null=True, blank=True)
    education = models.CharField('Education', max_length=400, choices=EDUCATION_LIST, null=True, blank=True)
#     country = models.ForeignKey(Country, null=True, blank=True, related_name='cont+')
    country_name = models.CharField('Where are you from?', max_length=250, null=True, blank=True)
    occupation = models.CharField('Occupation', max_length=400, choices=OCCUPATION_LIST, null=True, blank=True)
    organization = models.CharField('Organization', max_length=400, null=True, blank=True)
    organization_type = models.CharField('Organization Type', max_length=400, choices=ORGANIZATION_TYPE_LIST,
                                         null=True, blank=True)
    favorite_country = models.ManyToManyField(Country, verbose_name='Favorite Countries', blank=True,
                                              related_name='fav+')

    objects = UserManager()

    
    # i was trying to create a method to see if I (current user) was assigned to Data Entry group (group_id =1 )
    # having trouble with the query and how to chack this from both the view and template.
    def isdataentry(self):
        mygroups = self.groups.all()
        if len(mygroups) > 0:
            for mygroup in mygroups:
                if mygroup.name == 'data_entry':
                    return True
        return False


@receiver(post_save, sender=Newsletter)
def create_campaign(sender, instance, created, **kwargs):
    mailgun = Mailgun()
    method = 'post' if created else 'put'
    mailgun.create_update_campaign(instance.subject, instance.id, method)


@receiver(post_delete, sender=Newsletter)
def delete_campaign(sender, instance, **kwargs):
    mailgun = Mailgun()
    mailgun.delete_campaign(instance.id)


@receiver(email_confirmed)
def add_to_mailinglist(sender, **kwargs):
    mailgun = Mailgun()
    mailgun.add_member_mailinglist(address=kwargs['email_address'].email)


@receiver(post_save, sender=Election)
def invalidate_election_cache(sender, **kwargs):
    print('Im here')
    eguide_cache.invalidate_keys(eguide_cache.election_keys)


@receiver(post_save, sender=Country)
def invalidate_country_cache(sender, **kwargs):
    eguide_cache.invalidate_keys(eguide_cache.country_keys)


@receiver(post_save, sender=Digest)
def invalidate_digest_cache(sender, **kwargs):
    eguide_cache.invalidate_keys(eguide_cache.digest_keys)


@receiver(post_save, sender=Institution_type)
def invalidate_institution_type_cache(sender, **kwargs):
    eguide_cache.invalidate_keys(eguide_cache.institution_type_keys)


@receiver(post_save, sender=Category)
def invalidate_category_cache(sender, **kwargs):
    eguide_cache.invalidate_keys(eguide_cache.category_keys)


@receiver(post_save, sender=Page)
def invalidate_page_cache(sender, **kwargs):
    slug = kwargs.get('instance').slug

    cache.delete('page_%s' % slug)
