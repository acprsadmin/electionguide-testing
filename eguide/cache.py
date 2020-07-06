from django.core.cache import cache

election_keys = [
    'election_feed',
    'legacy_election_feed',
    'calendar_legacy_rss',
    'recent_results',
    'total_elections',
    'total_votes',
    'home_election',
    'elections_upcoming',
    'elections_upcoming_count',
    'elections_past',
    'elections_past_count',
    'ifesmap',
    'legacy_election_feed'
]

country_keys = [
    'search_box_countries',
    'countries',
    'countries_count'
]

digest_keys = [
    'digest_box',
    'home_digest',
    'digest_entry_list'
]

institution_type_keys = [
    'search_box_institution_type'
]

category_keys = [
    'nav_category'
]


def invalidate_keys(keys):
    for key in keys:
        cache.delete(key)
