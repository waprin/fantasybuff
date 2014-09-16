__author__ = 'bprin'

import logging
logger = logging.getLogger(__name__)

from teams.models import EntranceHtmlScrape, MatchupsWeekHtmlScrape, RosterHtmlScrape, StandingsHtmlScrape


class SqlStore:

## entrance

    def has_entrance(self, user):
        return len(EntranceHtmlScrape.objects.filter(user=user)) > 0

    def write_entrance(self, user, entrance_html):
        EntranceHtmlScrape.objects.create(user=user, html=entrance_html)

    def get_entrance(self, user):
        return EntranceHtmlScrape.objects.filter(user=user)[0].html

## matchups

    def has_matchups(self, league, week):
        return len(MatchupsWeekHtmlScrape.objects.filter(league=league, week=week)) > 0

    def write_matchups(self, league, week, html):
        MatchupsWeekHtmlScrape.objects.create(html=html, league=league, week=week)

    def get_matchups(self, league, week):
        return MatchupsWeekHtmlScrape.objects.filter(league=league, week=week)[0].html

## standings

    def has_standings(self, league):
        return len(StandingsHtmlScrape.objects.filter(league=league)) > 0

    def write_standings(self, league, html):
        StandingsHtmlScrape.objects.create(html=html, league=league)

    def get_standings(self, league):
        return StandingsHtmlScrape.objects.filter(league=league)[0].html

## rosters

    def has_roster(self, league, team_id, week):
        return len(RosterHtmlScrape.objects.filter(team_id=team_id, week=week, league=league)) > 0

    def write_roster(self, league, team_id, week, html):
        RosterHtmlScrape.objects.create(html=html, league=league, week=week, team_id=team_id)

    def get_roster(self, league, team_id, week):
        return RosterHtmlScrape.objects.filter(league=league, team_id=team_id, week=week)[0].html

