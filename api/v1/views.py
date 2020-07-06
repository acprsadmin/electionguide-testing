import datetime

from django.db.models import Sum
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from api.v1 import serializer
from eguide.models import Election, Country, Digest






class ClientViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List Elections
    alpha3 -- filter elections by country alpha3 code
    alpha2 -- filter elections by country alpha2 code
    """

    queryset = Election.objects.all()
    serializer_class = serializer.ClientSerializer

    def get_queryset(self):

        queryset = self.queryset


        return queryset

class ElectionViewSet(viewsets.ReadOnlyModelViewSet):

    """
    List Elections
    alpha3 -- filter elections by country alpha3 code
    alpha2 -- filter elections by country alpha2 code
    """

    queryset = Election.objects.all()
    serializer_class = serializer.ElectionSerializer

    def get_queryset(self):

        queryset = self.queryset

        if 'alpha3' in self.request.GET:

            queryset = queryset.filter(country__alpha3=self.request.GET.get('alpha3'))

        if 'alpha2' in self.request.GET:

            queryset = queryset.filter(country__alpha2=self.request.GET.get('alpha2'))

        return queryset


class ElectionApiViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)

    queryset = Election.objects.all()
    serializer_class = serializer.ElectionApiSerializer

    def get_queryset(self):
        queryset = Election.objects.filter(is_published=True)
        a = []
        class PObject(object):
            pass

        for e in queryset:
            r = PObject()
            r.election_name = e.name
         

            a.append(r)
        
        return a




class ElectionDemoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List Elections
    alpha3 -- filter elections by country alpha3 code
    alpha2 -- filter elections by country alpha2 code


    URL formats:
        1) get by id:
            [domain]/api/v1/elections_demo/?format=api&id=[ID]
        2) get first records with limit
            [domain]/api/v1/elections_demo/?format=api&limit=[limit]
        3) get records with start number and limit (start can be 0)
            [domain]/api/v1/elections_demo/?format=api&limit=[limit]&start=[start]
        4) pending.... start and end date (note to myself   wait for client input)
        OK

    """

    permission_classes = (IsAuthenticated,)

    queryset = Election.objects.all()
    serializer_class = serializer.ElectionDemoSerializer

    def get_queryset(self):

        queryset = Election.objects.filter(is_published=True)

        elections_id = self.request.query_params.get('id')
        limit = self.request.query_params.get('limit')
        start=self.request.query_params.get('start')
        year = self.request.query_params.get('year')

        country = self.request.query_params.get('country')

        country_id = -1
        if country != None:
            countries = Country.objects.filter(alpha2=country)
            if len(countries) > 0:
                country_id = countries[0].id


        # length=self.request.query_params.get('length')
        
        if elections_id != None:
            queryset = queryset.filter(id=elections_id)
        else:
            if year != None and year.isnumeric:
                if country_id != -1:
                    queryset = queryset.filter(original_election_year=year, country_id=country_id)
                else:
                    queryset = queryset.filter(original_election_year=year)
            else:
                if country_id != -1:
                    queryset = queryset.filter(country_id=country_id)

        limit_flag = False

        record_count = 0

        if start != None:
            if start.isnumeric:
                record_count = int(start)


        if limit != None:
            if limit.isnumeric():
                limit_flag = True
                limit = int(limit)

        a = []

        class PObject(object):
            pass


        
        index = 0

        for e in queryset:

            if index < record_count:
                index += 1
                continue


            r = PObject()



            alpha2 = e.country.alpha2

            highest_level = ''

            if e.is_national_exec:
                highest_level = 'national_exec'
            elif e.is_national_legislative:
                highest_level = 'national_legislative'
            elif e.is_national_upper:
                highest_level = 'national_upper'
            elif e.is_national_lower:
                highest_level = 'national_lower'
            else:
                highest_level = 'undefined'

            try:
                scope_name = e.election_scope.name
            except:
                scope_name = 'Null'

            try:
                r.original_election_year = e.original_election_year
            except:
                r.original_election_year = None     
            
            date_year = r.original_election_year
            if date_year == None:
                date_year = 'Null'

            r.election_key = str(alpha2) + '-' + highest_level + '-' + scope_name + '-' + str(date_year) + '-0'

            r.election_key = r.election_key.lower()

            r.election_id = e.id

            r.election_name = {'en_US': e.name}

            try:
                r.election_range_start_date = e.election_range_start_date
            except:
                r.election_range_start_date = None
            try:
                r.election_range_end_date = e.election_range_end_date
            except:
                r.election_range_end_date = None
            try:
                r.is_delayed_covid19 = e.is_delayed_covid19
            except:
                r.is_delayed_covid19 = None

            try:
                r.election_declared_start_date = e.election_declared_start_date.date()
            except:
                r.election_declared_start_date = None
            try:
                r.election_declared_end_date = e.election_declared_end_date
            except:
                r.election_declared_end_date = None
            try:
                r.election_type = e.election_scope.name
            except:
                r.election_type = None
            try:
                r.electoral_system = e.electoral_system.name
            except:
                r.electoral_system = None
            # try:
            r.electoral_system_other = None
            try:
                r.administering_election_commission_website = e.administering_election_commission_website
            except:
                r.administering_election_commission_website = None
            try:
                r.source = e.source_website
            except:
                r.source = None
            try:

                r.district = {
                    'district_ocd_id': "ocd-division/country:" + str(e.country.alpha2).lower(),
                    'district_name': e.country.name,
                    'district_country': str(e.country.alpha2).upper(),
                    'district_type': highest_level
                }
            except:
                r.district = None
            try:
                r.election_candidate_filing_deadline = e.election_candidate_filing_deadline.date()
            except:
                r.election_candidate_filing_deadline = None
            try:
                r.voter_registration_deadline = e.voter_registration_deadline.date()
            except:
                r.voter_registration_deadline = None
            try:
                r.voting_age_minimum_inclusive = e.voting_age_minimum_inclusive
            except:
                r.voting_age_minimum_inclusive = None
            r.voting_methods = None

            
            try:
                try:
                    if e.inperson_voting_enabled:
                        try:
                            if e.primary_voting_method == 1:
                                inperson_voting_isprimary = True
                            else:
                                inperson_voting_isprimary = False
                        except:
                            inperson_voting_isprimary = None
                        try:
                            inperson_voting_start = e.inperson_voting_start.date()
                        except:
                            inperson_voting_start = None
                        try:
                            inperson_voting_end = e.inperson_voting_end.date()
                        except:
                            inperson_voting_end = None
                        try:
                           if e.yn_inperson_voting_excuse_required == 1:
                            inperson_voting_excuse_required = 'Yes'
                           elif e.yn_inperson_voting_excuse_required == 2:
                            inperson_voting_excuse_required = 'No'
                           else:
                            inperson_voting_excuse_required = None
                        except:
                            inperson_voting_excuse_required = None
                        try:
                            instructions = {
                                "voting-id": {
                                    "en_US": e.inperson_voting_instructions
                                }
                            }
                        except:
                            instructions = None

                        r.voting_methods = [
                            {
                                'primary': inperson_voting_isprimary,
                                'start': inperson_voting_start,
                                'end': inperson_voting_end,
                                'type': 'in-person',
                                'excuse-required': inperson_voting_excuse_required,
                                'instructions': instructions
                            }
                        ]
                except:
                    pass
                try:
                    if e.early_voting_enabled:
                        try:
                            if e.primary_voting_method == 2:
                                early_voting_isprimary = True
                            else:
                                early_voting_isprimary = False
                        except:
                            early_voting_isprimary = None
                        try:
                            early_voting_start = e.early_voting_start.date()
                        except:
                            early_voting_start = None
                        try:
                            early_voting_end = e.early_voting_end.date()
                        except:
                            early_voting_end = None
                        try:
                           if e.yn_early_voting_excuse_required == 1:
                            early_voting_excuse_required = 'Yes'
                           elif e.yn_early_voting_excuse_required == 2:
                            early_voting_excuse_required = 'No'
                           else:
                            early_voting_excuse_required = None
                        except:
                            early_voting_excuse_required = None
                        try:
                            instructions = {
                                "voting-id": {
                                    "en_US": e.early_voting_instructions
                                }
                            }
                        except:
                            instructions = None
                        if r.voting_methods == None: 
                            r.voting_methods = [
                                {
                                    'primary': early_voting_isprimary,
                                    'start': early_voting_start,
                                    'end': early_voting_end,
                                    'type': 'early-voting',
                                    'excuse-required': early_voting_excuse_required,
                                    'instructions': instructions
                                }
                            ]
                        else:
                            r.voting_methods.append(
                                {
                                    'primary': early_voting_isprimary,
                                    'start': early_voting_start,
                                    'end': early_voting_end,
                                    'type': 'early-voting',
                                    'excuse-required': early_voting_excuse_required,
                                    'instructions': instructions
                                }
                            )
                except:
                    pass
                try:
                    if e.mail_voting_enabled:
                        try:
                            if e.primary_voting_method == 3:
                                mail_voting_isprimary = True
                            else:
                                mail_voting_isprimary = False
                        except:
                            mail_voting_isprimary = None
                        try:
                            mail_voting_start = e.mail_voting_start.date()
                        except:
                            mail_voting_start = None
                        try:
                            mail_voting_end = e.mail_voting_end.date()
                        except:
                            mail_voting_end = None
                        try:
                           if e.yn_mail_voting_excuse_required == 1:
                            mail_voting_excuse_required = 'Yes'
                           elif e.yn_mail_voting_excuse_required == 2:
                            mail_voting_excuse_required = 'No'
                           else:
                            mail_voting_excuse_required = None
                        except:
                            mail_voting_excuse_required = None
                        try:
                            instructions = {
                                "voting-id": {
                                    "en_US": e.mail_voting_instructions
                                }
                            }
                        except:
                            instructions = None
                        if r.voting_methods == None:
                            r.voting_methods = [
                                {
                                    'primary': mail_voting_isprimary,
                                    'start': mail_voting_start,
                                    'end': mail_voting_end,
                                    'type': 'mail-person',
                                    'excuse-required': mail_voting_excuse_required,
                                    'instructions': instructions
                                }
                            ]
                        else:
                            r.voting_methods.append(
                                {
                                    'primary': mail_voting_isprimary,
                                    'start': mail_voting_start,
                                    'end': mail_voting_end,
                                    'type': 'mail-person',
                                    'excuse-required': mail_voting_excuse_required,
                                    'instructions': instructions
                                }
                            )
                except:
                    pass
                try:
                    if e.online_voting_enabled:
                        try:
                            if e.primary_voting_method == 4:
                                online_voting_isprimary = True
                            else:
                                online_voting_isprimary = False
                        except:
                            online_voting_isprimary = None
                        try:
                            online_voting_start = e.online_voting_start.date()
                        except:
                            online_voting_start = None
                        try:
                            online_voting_end = e.online_voting_end.date()
                        except:
                            online_voting_end = None
                        try:
                           if e.yn_online_voting_excuse_required == 1:
                            online_voting_excuse_required = 'Yes'
                           elif e.yn_online_voting_excuse_required == 2:
                            online_voting_excuse_required = 'No'
                           else:
                            online_voting_excuse_required = None
                        except:
                            online_voting_excuse_required = None
                        try:
                            instructions = {
                                "voting-id": {
                                    "en_US": e.online_voting_instructions
                                }
                            }
                        except:
                            instructions = None

                        if r.voting_methods == None:
                            r.voting_methods = [
                                {
                                    'primary': online_voting_isprimary,
                                    'start': online_voting_start,
                                    'end': online_voting_end,
                                    'type': 'online-voting',
                                    'excuse-required': online_voting_excuse_required,
                                    'instructions': instructions
                                }
                            ]
                        else:
                            r.voting_methods.append(
                                {
                                    'primary': online_voting_isprimary,
                                    'start': online_voting_start,
                                    'end': online_voting_end,
                                    'type': 'online-voting',
                                    'excuse-required': online_voting_excuse_required,
                                    'instructions': instructions
                                }
                            )
                except:
                    pass
            except:
                r.voting_methods = None

            try:
                r.ifes_confirmation = e.ifes_confirmation
            except:
                r.ifes_confirmation = None

            try:
                r.ifes_confirmation_date = e.ifes_confirmation_date
            except:
                r.ifes_confirmation_date = None

            r.third_party_verified = {
                'is_verified': r.ifes_confirmation,
                'date': r.ifes_confirmation_date
            }




            a.append(r)

            index += 1
            if limit_flag:
                if len(a) >= limit:
                    break


        return a


class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List Countries
    alpha3 -- filter by country alpha3 code
    alpha2 -- filter by country alpha2 code
    """

    queryset = Country.objects.all()
    serializer_class = serializer.CountrySerializer

    def get_queryset(self):

        queryset = self.queryset

        if 'alpha3' in self.request.GET:

            queryset = queryset.filter(alpha3=self.request.GET.get('alpha3'))

        if 'alpha2' in self.request.GET:

            queryset = queryset.filter(alpha2=self.request.GET.get('alpha2'))

        return queryset


class DigestViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Digest List
    """

    queryset = Digest.objects.all()
    serializer_class = serializer.DigestSerializer


class MetadataViewSet(viewsets.ViewSet):
    """
    Returns Meta data
    """

    def list(self, request):

        year = datetime.date.today().year
        start = datetime.datetime.strptime('0101%s' % year, "%d%m%Y").date()
        end = datetime.datetime.strptime('3112%s' % year, "%d%m%Y").date()
        elections = Election.objects.filter(date__gt=start, date__lt=end, active=1)

        votes = elections.aggregate(total_votes=Sum('cast_votes'))
        numbers = elections.count()

        response = {'metadata': {
            'total_votes': votes['total_votes'],
            'total_elections': numbers
        }}

        return Response(response)
