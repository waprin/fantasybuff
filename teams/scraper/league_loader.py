from teams.models import League
from teams.scraper.html_scrapes import get_leagues_from_entrance

__author__ = 'bprin'

def load_leagues_from_entrance(html, espn_user):
    league_tuples = get_leagues_from_entrance(html)
    leagues = []
    for league_tuple in league_tuples:
        try:
            league = League.objects.get(espn_id=league_tuple[1], year=league_tuple[2])
        except League.DoesNotExist:
            league = League.objects.create(espn_id=league_tuple[1], year=league_tuple[2], name=league_tuple[0])

        league.users.add(espn_user)
        league.save()
        leagues.append(league)
    return leagues
