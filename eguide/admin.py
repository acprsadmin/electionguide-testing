from django.contrib import admin
from django.contrib.admin import ModelAdmin, TabularInline, StackedInline
from django.contrib.auth.admin import UserAdmin
from django.forms import ModelForm, Textarea
from django.contrib.staticfiles.storage import staticfiles_storage

from ckeditor.widgets import CKEditorWidget
import autocomplete_light
import newsletter
from mailgun.methods import Mailgun
from eguide.models import (Region, Country, Institution_type, Election_system, Electoral_system, Election_scope, Institution, Election_status, Election_type,
                           Election, Party, Person, Party_votes, Candidate_votes, Provision_votes, EguideUser,
                           Digest, Page, Author, Category, Choice, Newsletter)


class CandidateVotesInline(TabularInline):
    model = Candidate_votes
    form = autocomplete_light.modelform_factory(Candidate_votes)
    extra = 1
    suit_classes = 'suit-tab suit-tab-candidate'
    verbose_name_plural = ''
    readonly_fields = ('legacy_id',)

    def queryset(self, request):
        return Candidate_votes.objects.all().select_related('person')


class PartyVotesInline(StackedInline):
    model = Party_votes
    form = autocomplete_light.modelform_factory(Party_votes)
    extra = 1
    suit_classes = 'suit-tab suit-tab-party'
    verbose_name_plural = ''
    readonly_fields = ('legacy_id',)


class ChoiceInline(StackedInline):
    model = Choice
    extra = 1
    verbose_name_plural = ''


class ProvisionAdmin(ModelAdmin):

    inlines = (ChoiceInline,)
    list_display = ('election', 'provision', 'id', 'active')
    search_fields = ['provision']
    list_filter = ('election__country', 'active')
    list_editable = ('active', )
    readonly_fields = ('legacy_id',)


class ProvisionInline(StackedInline):
    model = Provision_votes
    extra = 1
    suit_classes = 'suit-tab suit-tab-provision'
    verbose_name_plural = ''
    readonly_fields = ('legacy_id',)


class ElectionForm(ModelForm):
    class Meta:
        model = Election
        exclude = ['date_created']

        widgets = {
            'registered_voters_source': Textarea(attrs={'rows': 2, 'cols': 150}),
            'description': CKEditorWidget(),
            'ifes_comments': CKEditorWidget(),
            'embassy_comments': CKEditorWidget(),
            'legal_consultant_comments': CKEditorWidget(),
            'cso_comments': CKEditorWidget(),
            'inperson_voting_instructions': CKEditorWidget(),
            'early_voting_instructions': CKEditorWidget(),
            'mail_voting_instructions': CKEditorWidget(),
            'online_voting_instructions': CKEditorWidget()
            }


class ElectionAdmin(ModelAdmin):

    form = ElectionForm

    search_fields = ['name']
    list_filter = ('election_type',
                   'active',
                   'country')
    list_per_page = 50
    list_editable = ('active',)
    date_hierarchy = 'date'
    list_display = ('name',
                    'date',
                    'country',
                    'election_type',
                    # 'institution',
                    'active')

    readonly_fields = ('legacy_id',)
    list_select_related = True
    inlines = (PartyVotesInline, CandidateVotesInline, ProvisionInline,)

    fieldsets = [
        (None, {
            'classes': ('suit-tab suit-tab-general',),
            'fields': ['name',
                       'country',
                       'institution',
                       'date',
                       'original_election_year',
                       'election_range_start_date',
                       'election_range_end_date', 
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
                       'active',
                       'election_status',
                       'is_delayed_covid19',
                       'election_type',
                       'electoral_system',
                       'electoral_system_other',
                       'electoral_system_source',
                       'election_scope',
                       'show_results',
                       'show_seat_shares',
                       'description',
                       'female_elected',
                       'source_website',
                       'administering_election_commission_website', 
                       'legacy_id']
        }),

      ('Election Level (District Type)', {
            'classes': ('suit-tab suit-tab-general',),
            'fields': ['is_national_exec',
            'is_national_upper',
            'is_national_lower',
            'is_national_legislative'
            ]
        }),



        ('Voter Registration', {
            'classes': ('suit-tab suit-tab-votes',),
            'fields': ['registered_voters',
                       'registered_voters_male',
                       'registered_voters_female',
                       'registered_voters_date',
                       'registered_voters_source',
                       'voter_registration_deadline',
                       'voter_registration_deadline_time',
                       'voting_age_minimum_inclusive',
                       'voting_age_minimum_source']
        }),
        ('Votes Cast', {
            'classes': ('suit-tab suit-tab-votes',),
            'fields': ['cast_votes',
                       'valid_votes',
                       'invalid_votes']
        }),
        (None, {
            'classes': ('suit-tab suit-tab-party',),
            'fields': []
        }),
        (None, {
            'classes': ('suit-tab suit-tab-candidate',),
            'fields': ['election_candidate_filing_deadline',
              'election_candidate_filing_deadline_time',
              'election_candidate_filing_deadline_source'
            ]
        }),
        (None, {
            'classes': ('suit-tab suit-tab-provision',),
            'fields': []
        }),
       
        ('Rights', {
            'classes': ('suit-tab suit-tab-rights',),
            'fields': ['yn_support_electoral_rights',
            'support_electoral_rights_details',
            'yn_restrict_electoral_rights',
            'restrict_electoral_rights_details',
            'electoral_rights_info_source',
            'yn_hate_speech_prohibited',
            'hate_speech_prohibition',
            'hate_speech_prohibition_source',
            'yn_disinformation_prohibited',
            'disinformation_prohibition',
            'disinformation_prohibition_source'
            ]
        }),



        ('Voting Methods', {
            'classes': ('suit-tab suit-tab-methods',),
            'fields': ['primary_voting_method']
        }),


        ('In Person Voting', {
            'classes': ('suit-tab suit-tab-methods',),
            'fields': ['inperson_voting_enabled',
            'inperson_voting_start',
            'inperson_voting_start_time',
            'inperson_voting_end',
            'inperson_voting_end_time',
            'inperson_voting_instructions',
            'yn_inperson_voting_excuse_required'
            ]
        }),

        ('Early Voting', {
            'classes': ('suit-tab suit-tab-methods',),
            'fields': ['early_voting_enabled',
            'early_voting_start',
            'early_voting_start_time',
            'early_voting_end',
            'early_voting_end_time',
            'early_voting_instructions',
            'yn_early_voting_excuse_required'
            ]
        }),

        ('Mail Voting', {
            'classes': ('suit-tab suit-tab-methods',),
            'fields': ['mail_voting_enabled',
            'mail_voting_start',
            'mail_voting_start_time',
            'mail_voting_end',
            'mail_voting_end_time',
            'mail_voting_instructions',
            'yn_mail_voting_excuse_required'
            ]
        }),

        ('Online Voting', {
            'classes': ('suit-tab suit-tab-methods',),
            'fields': ['online_voting_enabled',
            'online_voting_start',
            'online_voting_start_time',
            'online_voting_end',
            'online_voting_end_time',
            'online_voting_instructions',
            'yn_online_voting_excuse_required'
            ]
        }),


        ('IFES Review', {
            'classes': ('suit-tab suit-tab-review',),
            'fields': ['legal_consultant_comments',
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
            'is_submitted',
            'submitted_by',
            'is_published',
            'active',
            'published_by',
            'show_results',
            'show_seat_shares']
        }),

    ]

    suit_form_tabs = (('general', 'Basic Info'),
                      ('votes', 'Results'),
                      ('party', 'Party Votes'),
                      ('candidate', 'Candidate Votes'),
                      ('provision', 'Referendum'),
                      ('rights', 'Rights'),
                      ('methods', 'Voting Methods'),
                      ('review', 'IFES Review'),
                      )

    def get_queryset(self, request):
        return Election.objects.all().select_related('country',
                                                     'institution',
                                                     'election_type',
                                                     'electoral_system',
                                                     'election_scope')


class CountryForm(ModelForm):
    class Meta:
        model = Country
        exclude = ['date_created']

        widgets = {
            'population_source': Textarea(attrs={'rows': 2, 'cols': 50}),
            'description': CKEditorWidget(),
        }


class CountryAdmin(ModelAdmin):

    form = CountryForm

    search_fields = ['name']
    list_filter = ('region',)
    list_per_page = 30
    ordering = ('name',)
    list_display = ('name',
                    'official_name',
                    'region',
                    'population',
                    'active')
    list_select_related = True


class InstitutionAdmin(ModelAdmin):

    search_fields = ['name', 'foriegn_name', 'country__name']
    list_filter = ('country',
                   'system',
                   'institution_type',
                   'active')
    list_per_page = 30
    ordering = ('country',)
    list_display = ('name',
                    'foriegn_name',
                    'country',
                    'institution_type',
                    'active')
    list_select_related = True




class ElectoralSystemAdmin(ModelAdmin):

    search_fields = ['name']
    list_filter = ('name', 'id')
    list_per_page = 30
    ordering = ('name',)
    list_display = ('name', 'id')
    list_select_related = True


class ElectionScopeAdmin(ModelAdmin):

    search_fields = ['name']
    list_filter = ('name', 'id')
    list_per_page = 30
    ordering = ('name',)
    list_display = ('name', 'id')
    list_select_related = True


class PartyForm(ModelForm):
    class Meta:
        model = Party
        exclude = ['date_created']

        widgets = {
            'country': autocomplete_light.TextWidget('CountryAutocomplete'),
        }


class PartyAdmin(ModelAdmin):

    form = PartyForm

    search_fields = ['name', 'foreign_name']
    list_filter = (
                   'country',
                   'type',
                   'active',
                   )
    list_per_page = 30
    ordering = ('country',)
    list_display = (
                    'name',
                    'foreign_name',
                    'country',
                    'type',
                    'active',)
    list_select_related = True
    readonly_fields = ('legacy_id',)


class PersonForm(ModelForm):
    class Meta:
        model = Party
        exclude = ['date_created']

        widgets = {
            'country': autocomplete_light.TextWidget('CountryAutocomplete'),
        }


class PersonAdmin(ModelAdmin):

    form = PersonForm

    search_fields = ['name',
                     'lastname',
                     'party__name']

    list_filter = ('country',
                   'active',
                   )
    list_per_page = 30
    ordering = ('country',)
    list_display = ('lastname',
                    'name',
                    'country',
                    'party',
                    'active',
                    )
    list_select_related = True
    readonly_fields = ('legacy_id',)


class ElectionSystemAdmin(ModelAdmin):

    search_fields = ['name']
    list_per_page = 100
    ordering = ('name',)
    list_display = ('name', 'id')


class PageForm(ModelForm):
    class Meta:
        model = Page
        exclude = ['date_created']

        widgets = {
            'body': CKEditorWidget(),
        }


class PageAdmin(ModelAdmin):

    form = PageForm


class DigestForm(ModelForm):
    class Meta:
        model = Digest
        exclude = ['date_created']

        widgets = {
            'excerpt': Textarea(attrs={'rows': 3, 'cols': 50}),
            'body': CKEditorWidget(),
        }


class DigestAdmin(ModelAdmin):

    form = DigestForm

    search_fields = ['title',
                     'country__name',
                     'author__name']
    list_filter = ('category',
                   'country',
                   'author',
                   'active')
    list_per_page = 30
    list_editable = ('active', )
    ordering = ['-post_date']
    list_display = ('title',
                    'post_date',
                    'author',
                    'active'
                    )
    list_select_related = True
    prepopulated_fields = {"slug": ("title",)}

    fieldsets = [
        (None, {
            'classes': ('suit-tab suit-tab-post',),
            'fields': ['title',
                       'slug',
                       'excerpt',
                       'image',
                       'body'
                       ]
        }),
        (None, {
            'classes': ('suit-tab suit-tab-extra',),
            'fields': ['active',
                       'post_date',
                       'post_modified',
                       'author',
                       'category',
                       'country']
        })

    ]

    suit_form_tabs = (('post', 'Post'),
                      ('extra', 'Options'))


class NewsletterForm(ModelForm):

    class Meta:
        model = Newsletter
        widgets = {
            'excerpt': Textarea(attrs={'rows': 3, 'cols': 50}),
            'body': CKEditorWidget(config_name='custom_newsletter'),
        }
        exclude = ['date_created']

    def __init__(self, *args, **kwargs):
        super(NewsletterForm, self).__init__(*args, **kwargs)
        try:
            self.fields['subject'].initial = newsletter.generate_title()
            self.fields['body'].initial = newsletter.generate_newsletter()
            self.fields['to'].initial = 'newsletter@mg.electionguide.org'
        except KeyError:
            pass


class NewsletterAdmin(ModelAdmin):

    form = NewsletterForm

    list_display = ('subject',
                    'start_campaign',
                    )

    change_form_template = 'newsletter/analytics.html'

    def get_form(self, request, obj=None, **kwargs):
        if obj is None or not obj.active:
            self.fields = ('subject', ('to', 'cc', 'bcc'), 'body')
        else:
            self.pk = obj.id
            self.readonly_fields = ('subject',)
            self.fields = ('subject',)
            mailgun = Mailgun()
            if obj.active:
                try:
                    stats = mailgun.get_campaign_stats(obj.id)
                    obj.status = 'Completed'
                    obj.delivered = stats['total']['delivered']
                    obj.complained = stats['total']['complained']
                    obj.clicked = stats['total']['clicked']
                    obj.opened = stats['total']['opened']
                    obj.dropped = stats['total']['dropped']
                    obj.bounced = stats['total']['bounced']
                    obj.sent = stats['total']['sent']
                    obj.unsubscribed = stats['total']['unsubscribed']
                    obj.save()
                except BaseException:
                    pass

        return super(NewsletterAdmin, self).get_form(request, obj, **kwargs)

    def start_campaign(self, obj):
        if obj.active:
            url = '<div id="campaign-%s" data-id="%s">%s</div>' % (obj.id, obj.id, obj.status)
        elif obj:
            url = '<div id="campaign-%s" data-id="%s"><a data-id="%s" href="#">Click to Start Campaign</a></div>' % (obj.id, obj.id, obj.id)
        return url

    start_campaign.allow_tags = True
    start_campaign.short_description = 'Status'

    class Media:
        js = (staticfiles_storage.url('eguide/js/newsletter.js'), )

admin.site.register(Country, CountryAdmin)
admin.site.register(Region)
admin.site.register(Person, PersonAdmin)
admin.site.register(Institution_type)
admin.site.register(Electoral_system, ElectoralSystemAdmin)
admin.site.register(Election_scope, ElectionScopeAdmin)
admin.site.register(Election_system, ElectionSystemAdmin)
admin.site.register(Institution, InstitutionAdmin)
admin.site.register(Election_status)
admin.site.register(Election, ElectionAdmin)
admin.site.register(Party, PartyAdmin)
admin.site.register(EguideUser, UserAdmin)
admin.site.register(Digest, DigestAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Provision_votes, ProvisionAdmin)
admin.site.register(Newsletter, NewsletterAdmin)
