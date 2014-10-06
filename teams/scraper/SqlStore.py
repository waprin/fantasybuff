import os

__author__ = 'bprin'

import logging
logger = logging.getLogger(__name__)

from django.db.models import Q

from teams.models import EntranceHtmlScrape, MatchupsWeekHtmlScrape, RosterHtmlScrape, StandingsHtmlScrape, \
    PlayerHtmlScrape, GameHtmlScrape, SettingsHtmlScrape, TranslogHtmlScrape


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

## settings

    def has_settings(self, league_id, year):
        return SettingsHtmlScrape.objects.filter(league_id=league_id, year=year).count() > 0

    def write_settingss(self, league_id, year, html):
        SettingsHtmlScrape.objects.create(html=html, league_id=league_id, year=year)

    def get_settings(self, league_id, year):
        return SettingsHtmlScrape.objects.filter(league_id=league_id, year=year)[0].html

## rosters

    def has_roster(self, league, team_id, week):
        return RosterHtmlScrape.objects.filter(team_id=team_id, week=week, league=league).count() > 0

    def write_roster(self, league, team_id, week, html):
        RosterHtmlScrape.objects.create(html=html, league=league, week=week, team_id=team_id)

    def get_roster(self, league, team_id, week):
        return RosterHtmlScrape.objects.filter(league=league, team_id=team_id, week=week)[0].html

## translog

    def has_translog(self, league_id, year, team_id):
        return TranslogHtmlScrape.objects.filter(league_id=league_id, year=year, team_id=team_id).count() > 0

    def write_translog(self, league_id, year, team_id, html):
        TranslogHtmlScrape.objects.create(league_id=league_id, year=year, team_id=team_id, html=html)

    def get_translog(self, league_id, year, team_id):
        return TranslogHtmlScrape.objects.filter(league_id=league_id, year=year, team_id=team_id)[0].html

## players

    def has_player(self, league, player_id):
        return PlayerHtmlScrape.objects.filter(player_id=player_id, league=league).count() > 0

    def get_player(self, player_id, league):
        return PlayerHtmlScrape.objects.filter(league=league, player_id=player_id)[0].html

    def write_player(self, league, player_id, html):
        PlayerHtmlScrape.objects.create(html=html, league=league, player_id=player_id)

    def get_all_player_htmls(self, league):
        htmls = []
        for player_scrape in PlayerHtmlScrape.objects.filter(league=league):
            htmls.append((player_scrape.player_id, player_scrape.html))
        return htmls

## games
    def has_game(self, league, team_id, week):
        return GameHtmlScrape.objects.filter(Q(first_team=team_id) | Q(second_team=team_id) , league=league, week=week).count() > 0

    def get_game(self, league, team_id, week):
        return GameHtmlScrape.objects.filter(Q(first_team=team_id) | Q(second_team=team_id), league=league, week=week)[0].html

    def write_game(self, league, team_id, week, html):
        GameHtmlScrape.objects.create(first_team=team_id, html=html, league=league, week=week)

    def get_all_games(self, league, week):
        htmls = []
        for game_html in GameHtmlScrape.objects.filter(league=league, week=week):
            htmls.append(game_html.html)
        return htmls

