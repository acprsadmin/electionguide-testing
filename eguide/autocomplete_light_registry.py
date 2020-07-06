import autocomplete_light

from eguide.models import Party, Person, Country

# autocomplete_light.register(Person, search_fields=('name', 'lastname'),)
# 
# autocomplete_light.register(Party, search_fields=('name', 'foreign_name'),)

autocomplete_light.register(Party, search_fields=('name',),
    autocomplete_js_attributes={'placeholder': 'Search for Paries...'})

autocomplete_light.register(Person, search_fields=('name', 'lastname',),
    autocomplete_js_attributes={'placeholder': 'Search for Candidates...'})

autocomplete_light.register(Country,
    autocomplete_js_attributes={'placeholder': 'Search for Countries ...'})