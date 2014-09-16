__author__ = 'bprin'

import logging
logger = logging.getLogger(__name__)

from teams.models import UserHtmlScrape, LeagueHtmlScrape, LeagueWeekHtmlScrape

class SqlStore:

## entrance

    def has_entrance(self, user):
        return len(UserHtmlScrape.objects.filter(type='entrance', user=user)) > 0

    def write_entrance(self, user, entrance_html):
        UserHtmlScrape.objects.create(type='entrance', user=user, html=entrance_html)

    def get_entrance(self, user):
        return UserHtmlScrape.objects.filter(type='entrance', user=user)[0].html

## matchups

    def has_matchups(self, league, week):
        return len(LeagueWeekHtmlScrape.objects.filter(type='matchups', league=league, week=week)) > 0

    def write_matchups(self, league, week, html):
        LeagueWeekHtmlScrape.objects.create(type="matchups", html=html, league=league, week=week)

    def get_matchups(self, league, week):
        return LeagueWeekHtmlScrape.objects.filter(type='matchups', league=league, week=week)[0].html

## standings

    def has_standings(self, league):
        return len(LeagueHtmlScrape.objects.filter(type='standings', league=league)) > 0

    def write_standings(self, league, html):
        LeagueHtmlScrape.objects.create(type='standings', html=html, league=league)

    def get_standings(self, league):
        return LeagueHtmlScrape.objects.filter(type='standings', league=league)[0].html


