from rest_framework import serializers

from eguide.models import Election, Country, Digest, Election_Demo, Election_API


class ClientSerializer(serializers.ModelSerializer):
    fieldcountryname = serializers.SerializerMethodField('countryname')

    def countryname(self, election):
      country = Country.objects.get(id=self.country_id)
      return country.name 

    class Meta:
        model = Election

        fields = ('name', 'id', 'description', 'country', 'fieldcountryname')




class ElectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Election


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country


class DigestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Digest
        exclude = ['country', 'category']


class ElectionDemoSerializer(serializers.ModelSerializer):

    class Meta:
        
        model = Election_Demo

        # model.clear()
        # id = serializers.IntegerField()
        # name = serializers.CharField()
        fields = [
            'election_id',
            'election_key',
            'election_name',
            'original_election_year',
            'election_range_start_date',
            'election_range_end_date',
            'is_delayed_covid19',
            'election_declared_start_date',
            'election_declared_end_date',
            'election_type',
            'electoral_system',
            'electoral_system_other',
            'administering_election_commission_website',
            'source',
            'district',
            'election_candidate_filing_deadline',
            'voter_registration_deadline',
            'voting_age_minimum_inclusive',
            'voting_methods',
            'third_party_verified'
        ]


class ElectionApiSerializer(serializers.ModelSerializer):

    class Meta:
        
        model = Election_API
      
        fields = [
           'election_name'
        ]
