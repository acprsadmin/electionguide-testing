from django.forms import ModelForm, ModelMultipleChoiceField, CharField
from django import forms
from eguide.models import EguideUser, Country, Election, Provision_votes, Party_votes, Candidate_votes, Person, Party
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms.extras.widgets import SelectDateWidget

#
from ckeditor.widgets import CKEditorWidget
#from django.forms.extras.widgets import RadioSelect
import autocomplete_light



class EguideUserForm(ModelForm):
    favorite_country = ModelMultipleChoiceField(
                            Country.objects.all(),
                            widget=FilteredSelectMultiple("Countries",
                                                          False,attrs={'rows':'10'}
                                                          )
                            )
    
    country_name = CharField(
                        widget=autocomplete_light.TextWidget('CountryAutocomplete')
                        )
    
    class Meta:
        model = EguideUser
        
        fields = ['email',
                  'id',
                  'first_name', 
                  'last_name',
                  'favorite_country',
                  'age', 
                  'gender', 
                  'education', 
                  'country_name',
                  'organization',
                  'organization_type'
                  ]






class ElectionCreateForm(ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'size': '80'}))
    description = forms.CharField(widget=CKEditorWidget()) 
    election_declared_start_date = forms.DateField(widget=forms.TextInput(attrs={'data-provide': "datepicker"}), required=False)
    election_declared_end_date = forms.DateField(widget=forms.TextInput(attrs={'data-provide': "datepicker"}), required=False)
    election_range_start_date = forms.DateField(widget=forms.TextInput(attrs={'data-provide': "datepicker"}), required=False) 
    election_range_end_date = forms.DateField(widget=forms.TextInput(attrs={'data-provide': "datepicker"}), required=False) 
    election_declared_start_time = forms.TimeField(required=False)
    election_declared_end_time = forms.TimeField(required=False)


    class Meta:
        model = Election
        
        fields = ['name',
        'country',
        'institution',
        'original_election_year',
        'election_range_start_date', 
        'election_range_end_date',
        'election_declared_start_date', 
        'election_declared_start_time', 
        'election_declared_end_date',
        'election_declared_end_time', 
        'election_scope',
        'is_national_exec', 
        'is_national_legislative',
        'is_national_upper',
        'is_national_lower',
        'electoral_system',
        'electoral_system_other',
        'electoral_system_source',
        'election_scope',
        'election_status',
        'election_type',
        'description']



class ElectionEditForm(ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'size': '80'}))
    description = forms.CharField(widget=CKEditorWidget(), required=False)
    
    election_declared_start_date = forms.DateField(widget=forms.TextInput(attrs={'data-provide': "datepicker"}), required=False)
    election_declared_end_date = forms.DateField(widget=forms.TextInput(attrs={'data-provide': "datepicker"}), required=False)
    election_range_start_date = forms.DateField(widget=forms.TextInput(attrs={'data-provide': "datepicker"}), required=False) 
    election_range_end_date = forms.DateField(widget=forms.TextInput(attrs={'data-provide': "datepicker"}), required=False) 
    election_blackout_start_date = forms.DateField(widget=forms.TextInput(attrs={'data-provide': "datepicker"}), required=False) 
    election_blackout_end_date = forms.DateField(widget=forms.TextInput(attrs={'data-provide': "datepicker"}), required=False) 

    registered_voters_date = forms.DateField(widget=forms.TextInput(attrs={'data-provide': "datepicker"}), required=False) 
    registered_voters_source = forms.CharField(widget=forms.Textarea(attrs={'cols': '80', 'rows': '3'}), required=False)
    election_candidate_filing_deadline = forms.DateField(widget=forms.TextInput(attrs={'data-provide': "datepicker"}), required=False) 
    voter_registration_deadline = forms.DateField(widget=forms.TextInput(attrs={'data-provide': "datepicker"}), required=False) 

    election_range_notes = forms.CharField(widget=CKEditorWidget(config_name='custom_newsletter'), required=False)
    election_range_source= forms.CharField(widget=forms.TextInput(attrs={'size': '80'}), required=False)
    election_declared_source= forms.CharField(widget=forms.TextInput(attrs={'size': '80'}), required=False)
    blackout_date_source= forms.CharField(widget=forms.TextInput(attrs={'size': '80'}), required=False)
    administering_election_commission_website= forms.CharField(widget=forms.TextInput(attrs={'size': '80'}), required=False)
    source_website= forms.CharField(widget=forms.TextInput(attrs={'size': '80'}), required=False)
    election_candidate_filing_deadline_notes = forms.CharField(widget=forms.Textarea(attrs={'cols': '80', 'rows': '3'}), required=False)
    election_candidate_filing_deadline_source = forms.CharField(widget=forms.TextInput(attrs={'size': '80'}), required=False)
    ballot_description = forms.CharField(widget=CKEditorWidget(config_name='custom_newsletter'), required=False)

 
 
    election_declared_start_time = forms.TimeField(required=False)
    election_declared_end_time = forms.TimeField(required=False)
    election_blackout_start_time = forms.TimeField(required=False) 
    election_blackout_end_time = forms.TimeField(required=False) 
    election_candidate_filing_deadline_time = forms.TimeField(required=False) 
    voter_registration_deadline_time = forms.TimeField(required=False) 

    class Meta:
        model = Election

        fields = ['is_delayed_covid19',
        'original_election_year',
           'country',
           'institution',
           'name',
           'description',
           'election_range_start_date',
           'election_range_end_date',
           'election_range_notes',
           'election_range_source',
           'election_declared_start_date',
           'election_declared_start_time',
           'election_declared_end_date',
           'election_declared_end_time',
           'election_declared_source',
           'election_blackout_start_date',
           'election_blackout_start_time',
           'election_blackout_end_date',
           'election_blackout_end_time',
           'blackout_date_source',
           'administering_election_commission_website',
           'source_website',
           'voter_registration_deadline',
           'election_candidate_filing_deadline',
           'election_candidate_filing_deadline_notes',
           'election_candidate_filing_deadline_source',
           'voting_age_minimum_inclusive',
           'voting_age_minimum_source',
           'is_national_exec',
           'is_national_legislative',
           'is_national_upper',
           'is_national_lower',
           'election_scope',
           'election_status',
           'election_type',
           'electoral_system',
           'electoral_system_other',
           'electoral_system_source',
           'female_elected',
           'registered_voters',
           'registered_voters_male',
           'registered_voters_female',
           'registered_voters_date',
           'registered_voters_source',
           'cast_votes',
           'valid_votes',
           'invalid_votes',
           'ballot_description',
           'ballot_file']



class ElectionRightsForm(ModelForm):

    class Meta:
        model = Election

        fields = ['yn_support_electoral_rights',
        'support_electoral_rights_details',
        'yn_restrict_electoral_rights',
        'restrict_electoral_rights_details',
        'electoral_rights_info_source',
        'yn_hate_speech_prohibited',
        'hate_speech_prohibition',
        'hate_speech_prohibition_source',
        'yn_disinformation_prohibited',
        'disinformation_prohibition',
        'disinformation_prohibition_source']



class ElectionMethodForm(ModelForm):
    inperson_voting_instructions = forms.CharField(widget=CKEditorWidget(config_name='custom_newsletter'), required=False) 
    early_voting_instructions = forms.CharField(widget=CKEditorWidget(config_name='custom_newsletter'), required=False) 
    mail_voting_instructions = forms.CharField(widget=CKEditorWidget(config_name='custom_newsletter'), required=False) 
    online_voting_instructions = forms.CharField(widget=CKEditorWidget(config_name='custom_newsletter'), required=False) 
   
    inperson_voting_start = forms.DateField(widget=forms.TextInput(attrs={'data-provide': "datepicker"}), required=False) 
    inperson_voting_end = forms.DateField(widget=forms.TextInput(attrs={'data-provide': "datepicker"}), required=False) 
    early_voting_start = forms.DateField(widget=forms.TextInput(attrs={'data-provide': "datepicker"}), required=False) 
    early_voting_end = forms.DateField(widget=forms.TextInput(attrs={'data-provide': "datepicker"}), required=False) 
    mail_voting_start = forms.DateField(widget=forms.TextInput(attrs={'data-provide': "datepicker"}), required=False) 
    mail_voting_end = forms.DateField(widget=forms.TextInput(attrs={'data-provide': "datepicker"}), required=False) 
    online_voting_start = forms.DateField(widget=forms.TextInput(attrs={'data-provide': "datepicker"}), required=False) 
    online_voting_end = forms.DateField(widget=forms.TextInput(attrs={'data-provide': "datepicker"}), required=False) 
    voter_registration_deadline = forms.DateField(widget=forms.TextInput(attrs={'data-provide': "datepicker"}), required=False) 

    inperson_voting_start_time  = forms.TimeField(required=False)
    inperson_voting_end_time  = forms.TimeField(required=False) 
    early_voting_start_time  = forms.TimeField(required=False)
    early_voting_end_time = forms.TimeField(required=False) 
    mail_voting_start_time = forms.TimeField(required=False) 
    mail_voting_end_time = forms.TimeField(required=False) 
    online_voting_start_time = forms.TimeField(required=False) 
    online_voting_end_time = forms.TimeField(required=False) 
        
    class Meta:
        model = Election

        fields = ['primary_voting_method',
        'inperson_voting_enabled',
        'inperson_voting_start',
        'inperson_voting_start_time',
        'inperson_voting_end',
        'inperson_voting_end_time',
        'inperson_voting_instructions',
        'yn_inperson_voting_excuse_required',
        'early_voting_enabled',
        'early_voting_start',
        'early_voting_start_time',
        'early_voting_end',
        'early_voting_end_time',
        'early_voting_instructions',
        'yn_early_voting_excuse_required',
        'mail_voting_enabled',
        'mail_voting_start',
        'mail_voting_start_time',
        'mail_voting_end',
        'mail_voting_end_time',
        'mail_voting_instructions',
        'yn_mail_voting_excuse_required',
        'online_voting_enabled',
        'online_voting_start',
        'online_voting_start_time',
        'online_voting_end',
        'online_voting_end_time',
        'online_voting_instructions',
        'yn_online_voting_excuse_required']




class IfesReviewForm(ModelForm):
    legal_consultant_comments = forms.CharField(widget=CKEditorWidget(config_name='custom_newsletter'), required=False) 
    cso_comments = forms.CharField(widget=CKEditorWidget(config_name='custom_newsletter'), required=False) 
    embassy_comments = forms.CharField(widget=CKEditorWidget(config_name='custom_newsletter'), required=False) 
    ifes_comments = forms.CharField(widget=CKEditorWidget(config_name='custom_newsletter'), required=False) 
    legal_consultant_confirmation_date = forms.DateField(widget=forms.TextInput(attrs={'data-provide': "datepicker"}), required=False) 
    cso_confirmation_date = forms.DateField(widget=forms.TextInput(attrs={'data-provide': "datepicker"}), required=False) 
    embassy_confirmation_date = forms.DateField(widget=forms.TextInput(attrs={'data-provide': "datepicker"}), required=False) 
    ifes_confirmation_date = forms.DateField(widget=forms.TextInput(attrs={'data-provide': "datepicker"}), required=False) 
         
    class Meta:
        model = Election
        
        fields = ['show_results','show_seat_shares',
        'is_submitted', 'submitted_by', 'is_published', 'published_by',
        'legal_consultant_comments',
        'legal_consultant_confirmation',
        'legal_consultant_confirmation_date',
        'legal_consultant_name',
        'cso_comments',
        'cso_confirmation',
        'cso_confirmation_date',
        'cso_confirmation_name',
        'embassy_comments',
        'embassy_confirmation',
        'embassy_confirmation_date',
        'embassy_confirmation_name',
        'ifes_comments',
        'ifes_confirmation',
        'ifes_confirmation_date',
        'ifes_confirmation_name',
        'submitted_by_name',
        'published_by_name'
        ]


class ProvisionLinkForm(ModelForm):
    provision = forms.CharField(widget=CKEditorWidget(config_name='custom_newsletter'), required=False) 
    comments = forms.CharField(widget=CKEditorWidget(config_name='custom_newsletter'), required=False) 
    
    class Meta:  
        
        model = Provision_votes
        fields = ['provision', 'comment', 'cast_votes', 'valid_votes', 'invalid_votes', 'election']
        widgets = {
          'provision': forms.Textarea(attrs={'rows':10, 'cols':80}),
          'comment': forms.Textarea(attrs={'rows':10, 'cols':80})
        }    


class CandidateLinkForm(ModelForm):
    class Meta:
        model = Candidate_votes
        fields = ['candidate', 'votes', 'percentage', 'election']


class PersonLinkForm(ModelForm):
    description = forms.CharField(widget=CKEditorWidget(config_name='custom_newsletter'), required=False)    
    class Meta:
        model = Person
        fields = ['name', 'lastname', 'gender', 'party', 'url', 'description', 'country']        




class PartyLinkForm(ModelForm):
    description = forms.CharField(widget=CKEditorWidget(config_name='custom_newsletter'), required=False)    
    #party = forms.ChoiceField(Country.objects.all(), attrs={'class':'chosen-select'})
        
    class Meta:
        model = Party_votes
        fields = ['party', 'election', 'seats_won', 'votes', 'percentage', 'description' ]




class PartyForm(ModelForm):
    description = forms.CharField(widget=CKEditorWidget(config_name='custom_newsletter'), required=False)    

    class Meta:
        model = Party
        fields = ['name', 'foreign_name', 'url', 'description', 'country', 'type']        

