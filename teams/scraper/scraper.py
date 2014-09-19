import datetime
from decimal import Decimal
from teams.metrics.lineup_calculator import calculate_optimal_lineup, get_lineup_score
from teams.models import League, Team, Scorecard, ScorecardEntry, Player
from teams.scraper.html_scrapes import get_teams_from_standings, get_num_weeks_from_matchups, get_player_ids_from_lineup, \
    get_leagues_from_entrance
from teams.scraper.league_loader import load_leagues_from_entrance, load_scores_from_playersheet, \
    load_teams_from_standings, load_week_from_lineup

__author__ = 'bill'

import re, os
from bs4 import BeautifulSoup
import logging
logger = logging.getLogger(__name__)
from teams.management.commands import scrape
from teams.utils.league_files import choose_league_directory, create_league_directory


def get_real_num_weeks(num_weeks, league):
    if int(league.year) < 2014:
        return num_weeks
    now = datetime.datetime.now()

    start = datetime.datetime(year=2014, month=9, day=9)
    week = datetime.timedelta(days=7)
    start_days = [start + (weeknum * week) for weeknum in range(0, 13)]
    for i in range(0, num_weeks):
        if now < start_days[i]:
            return i
    return num_weeks

def is_scraped(espn_user, store):
    return store.has_entrance(espn_user)

def is_loaded(espn_user, store):
    leagues = get_leagues_from_entrance(store.get_entrance(espn_user))
    return len(leagues) == len(League.objects.filter(users=espn_user))

def is_league_teams_scraped(league, store):
    teams = get_teams_from_standings(store.get_standings(league))
    num_weeks = get_num_weeks_from_matchups(store.get_matchups(league, 1))
    num_weeks = get_real_num_weeks(num_weeks, league)
    roster_htmls = []
    all_player_ids = []
    for team in teams:
        for week in range(1, num_weeks + 1):
            if not store.has_roster(league, team[0], week):
                logger.info("missing team %s week %d" % (team[0], week))
            roster_html = store.get_roster(league, team[0], week)
            player_ids = get_player_ids_from_lineup(roster_html)
            all_player_ids = all_player_ids + player_ids
    return True

def is_league_players_scraped(league, store):
    teams = get_teams_from_standings(store.get_standings(league))
    num_weeks = get_num_weeks_from_matchups(store.get_matchups(league, 1))
    num_weeks = get_real_num_weeks(num_weeks, league)
    all_player_ids = []
    for team in teams:
        for week in range(1, num_weeks + 1):
            player_ids = get_player_ids_from_lineup(store.get_roster(league, team[0], week))
            all_player_ids = all_player_ids + player_ids
    all_player_ids = list(set(all_player_ids))
    for player_id in all_player_ids:
        if not store.has_player(league, player_id):
            logger.info("missing player %s" % player_id)
            return False
    return True


def is_league_loaded(league, store):
    return False

class LeagueScraper(object):

    def __init__(self, scraper, store, overwrite=False):
        self.scraper = scraper
        self.store = store
        self.overwrite = overwrite

    def create_welcome_page(self, user):
        if not self.overwrite and self.store.has_entrance(user):
            return False
        entrance_html = self.scraper.get_entrance(user)
        self.store.write_entrance(user, entrance_html)
        return True

    def create_standings_page(self, league):
        if not self.overwrite and self.store.has_standings(league):
            return False
        standings_html = self.scraper.get_standings(league)
        self.store.write_standings(league, standings_html)
        return True

    def create_matchups_page(self, league, week):
        if not self.overwrite and self.store.has_matchups(league, week):
            return False
        matchups_html = self.scraper.get_matchups(league, week)
        self.store.write_matchups(league, week, matchups_html)
        return True

    def create_team_week_roster(self, league, team_id, week):
        if not self.overwrite and self.store.has_roster(league, team_id, week):
            return False
        roster_html = self.scraper.get_roster(league, team_id, week)
        self.store.write_roster(league, team_id, week, roster_html)
        return True

    def create_player(self, league, player_id):
        if not self.overwrite and self.store.has_player(league, player_id):
            return False
        player_html = self.scraper.get_player(league, player_id)
        self.store.write_player(league, player_id, player_html)
        return True

    def create_players_from_roster(self, league, team_id, week):
        html = self.store.get_roster(league, team_id, week)
        player_ids = get_player_ids_from_lineup(html)
        for player_id in player_ids:
            self.create_player(league, player_id)


    def scrape_league(self, league):
        league.league_scrape_start_time = datetime.datetime.now()
        league.save()
        self.create_standings_page(league)
        self.create_matchups_page(league, 1)
        teams = get_teams_from_standings(self.store.get_standings(league))
        num_weeks = get_num_weeks_from_matchups(self.store.get_matchups(league, 1))
        num_weeks = get_real_num_weeks(num_weeks, league)
        for team in teams:
            for week in range(1, num_weeks + 1):
                self.create_team_week_roster(league, team[0], week)
        league.lineups_scrape_finish_time = datetime.datetime.now()
        league.save()

    def scrape_players(self, league):
        teams = get_teams_from_standings(self.store.get_standings(league))
        num_weeks = get_num_weeks_from_matchups(self.store.get_matchups(league, 1))
        num_weeks = get_real_num_weeks(num_weeks, league)
        all_player_ids = []
        for team in teams:
            for week in range(1, num_weeks + 1):
                player_ids = get_player_ids_from_lineup(self.store.get_roster(league, team[0], week))
                all_player_ids = all_player_ids + player_ids
        all_player_ids = list(set(all_player_ids))
        for player_id in all_player_ids:
            self.create_player(league, player_id)
        league.players_scrape_finish_time = datetime.datetime.now()
        league.save()

    def scrape_espn_user_leagues(self, espn_user):
        self.create_welcome_page(espn_user)

    def load_espn_user_leagues(self, espn_user):
        load_leagues_from_entrance(self.store.get_entrance(espn_user), espn_user)

    def create_leagues(self, espn_user):
        self.scrape_espn_user_leagues(espn_user)
        self.load_espn_user_leagues(espn_user)

    def load_league(self, league):
        self.scrape_league(league)
        self.scrape_players(league)

        self.load_players(league)
        self.load_teams(league)
        self.load_lineups(league)
        self.load_optimal_lineups(league)
        league.league_loaded_finish_time = datetime.datetime.now()
        league.loaded = True
        league.save()



    def load_players(self, league):
        logger.debug("loading players for league %s" % league)
        player_htmls = self.store.get_all_player_htmls(league)
        for player_html in player_htmls:
            load_scores_from_playersheet(player_html, league)
        logger.debug("%d players loaded" % (len(Player.objects.all())))

    def load_teams(self, league):
        logger.debug("loading teams for league %s" % league)
        standings_html = self.store.get_standings(league)
        load_teams_from_standings(standings_html, league)

    def load_lineups(self, league):
        logger.debug("loading linups for league %s" % league)
        num_weeks = get_num_weeks_from_matchups(self.store.get_matchups(league, 1))
        num_weeks = get_real_num_weeks(num_weeks, league)
        teams = Team.objects.filter(league=league)
        for team in teams:
            for week in range(1, num_weeks+1):
                lineup_html = self.store.get_roster(league, team.espn_id, week)
                load_week_from_lineup(lineup_html, week, team)

    def load_optimal_lineups(self, league):
        logger.debug("loading optimal lineups for league %s" % league)
        teams = Team.objects.filter(league=league)
        for team in teams:
            weeks = [entry.week for entry in Scorecard.objects.filter(team=team)]
            for week in weeks:
                scorecard = Scorecard.objects.get(team=team, week=week)
                scorecard_entries = ScorecardEntry.objects.filter(scorecard=scorecard)
                optimal_entries = calculate_optimal_lineup(scorecard_entries)
                total_points = get_lineup_score(optimal_entries)
                optimal_scorecard = Scorecard.objects.create(team=team, week=week, actual=False, points=total_points)
                for entry in optimal_entries:
                    entry.scorecard = optimal_scorecard
                    entry.save()

        for team in teams:
            actual_weeks = list(Scorecard.objects.filter(team=team, actual=True))
            if not actual_weeks:
                continue
            optimal_weeks = list(Scorecard.objects.filter(team=team, actual=False))
            actual_weeks.sort(key=lambda x: x.week)
            optimal_weeks.sort(key=lambda x: x.week)

            deltas = []
            for i, week in enumerate(actual_weeks):
                optimal_points = optimal_weeks[i].points
                delta = optimal_points - week.points
                deltas.append(delta)
            average_delta = sum(deltas) / Decimal(len(deltas))
            team.average_delta = average_delta
            team.save()

    def create_games(self, file_browser, espn_id, week_num):
        self.browser =  scrape.EspnScraper()
        logger.debug("create_games(): created browser")
        self.browser.login(self.username, self.password)
        logger.debug("create_games(): sucessfully logged in")

        scoreboard_html = file_browser.scrape_scoreboard(espn_id, week_num)
        team_ids = get_teams_from_scoreboard(scoreboard_html)

#        print "team ids: "
#        print team_ids
        os.makedirs(os.path.join(self.d, 'week_%d' % week_num, 'games'))
        for team_id in team_ids:
            html = self.browser.scrape_game(espn_id, team_id, week_num)
            print "team id is %s" % team_id
            filepath = os.path.join(self.d, 'week_%d' % week_num, 'games', 'game_%s.html' % team_id)
            logger.debug("writing game html to filepath %s" % filepath)
            f = open(filepath, 'w')
            f.write(html)

    def create_trans_logs(self, file_browser, espn_id):
        self.browser =  scrape.EspnScraper()
        logger.debug("create_trans_logs(): created browser")
        self.browser.login(self.username, self.password)
        logger.debug("create_trans_logs(): sucessfully logged in")

        scoreboard_html = file_browser.scrape_scoreboard(espn_id, 1)
        team_ids = get_teams_from_scoreboard(scoreboard_html)

        print "team ids: "
        print team_ids
        os.makedirs(os.path.join(self.d, 'translogs'))

        for team_id in team_ids:
            pass
            #self.browser.scrape_translog()



















