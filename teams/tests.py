from django.utils import unittest
from teams.management.commands.create_league import *
from teams.models import User, League, Team

import time
import os
from django.db import connection

from django.conf import settings

import logging
logger = logging.getLogger(__name__)


def clear_test_database(fn):
    def wrapper(self):
        logger.info("clearing: conncetion queries is %s" % str(connection.queries))
        for user in User.objects.all():
            logger.info("user is %s" % user.email)
            user.delete()
        for league in League.objects.all():
            league.delete()
        for game in Game.objects.all():
            game.delete()
        fn(self)
    return wrapper

def hits_live_site(fn):
    def wrapper(self):
        if settings.LIVE_SCRAPE:
            fn(self)
        else:
            logger.info("skipping live scrape " + fn.__name__)
    return wrapper

class ScrapeTest(unittest.TestCase):
    @hits_live_site
    def test_create_league(self):
        browser = FileCachedBrowser()
        browser.reload()
        browser.create_league('gothamcityrogues', 'sincere1')

    def test_new_loads_weeks(self):
        d = choose_league_directory(os.listdir(os.path.join(os.getcwd(), 'leagues')))
        logger.info('test_get_num_weeks')
        f = open(os.path.join('leagues', d, 'week_1', 'scoreboard.html'))
        html = f.read()
        num_weeks = get_num_weeks_from_scoreboard(html)
        self.assertEqual(num_weeks, 13)

    #@hits_live_site
    def test_loads_game(self):
        browser = FileCachedBrowser()
        browser.create_cached_league('gothamcityrogues', 'sincere1')
        games = Game.objects.all()

        for game in games:
            browser.create_game(game)

        self.assertTrue(any(game.first_scorecard.team.espn_id=='6' and game.second_scorecard.team.espn_id=='1' for game in games))
        self.assertFalse(any(game.first_scorecard.team.espn_id=='6' and game.second_scorecard.team.espn_id=='2' for game in games))

        logger.info("test_loads_game(): displaying games %d " % len(games))

class UtilsTest(unittest.TestCase):
    def test_choose_league_directory(self):
        logger.info('test_choose_directory(): begin() ... ')
        league1 = 'league_000_2012_12'
        league2 = 'league_001_2012_11'

        listings = ['something', '..', '.', league1, league2 ]
        d = choose_league_directory(listings)
        self.assertEquals(d, league2)

        d = choose_league_directory([])
        self.assertEqual(d, None)

        l1 = 'league_000_2012_12_24_00_57_16'
        #l2 = 'league_001_2012_12_24_00_57_16'
        l3 = 'league_000_2012_12_24_00_58_05'
        l4 = 'league_001_2012_12_24_00_58_05'
        l5 = 'league_000_2012_12_24_00_58_53'
        #l6 = 'league_001_2012_12_24_00_58_53'
        listings = [l1, l3, l4, l5]
        d = choose_league_directory(listings)
        self.assertEquals(d, l4)

class TeamsTest(unittest.TestCase):

    def test_init_user(self):
        logger.info('test_init_users')
        init_user()
        u = User.objects.get(email='waprin@gmail.com')
        self.assertEqual(u.password, 'terrible')

    @clear_test_database
    def test_parse_standings(self):
        """
        Tests that our sample standings page is parsed correctly
        """
        logger.info('test_parse_standings')
        f = open('local_scrapes/standings.html', 'r')
        html = f.read()
        league = League.objects.create(name="test league", espn_id='12345', year=2012)
        load_teams_from_standings(html, league)
        teams = Team.objects.all()

        logger.info(teams)
        self.assertEqual(len(teams), 10)
        self.assertTrue(any(team.team_name == 'Gotham City Rogues' and team.espn_id == '6' and team.owner_name == 'bill prin' for team in teams))

    @clear_test_database
    def test_get_num_weeks(self):
        logger.info('test_get_num_weeks')
        f = open('local_scrapes/realboard.html')
        html = f.read()
        num_weeks = get_num_weeks_from_scoreboard(html)
        self.assertEqual(num_weeks, 13)

    @clear_test_database
    def test_load_games_from_scoreboard(self):
        logger.info('test_load_games_from_scoreboard(): begin')
        f = open('local_scrapes/realboard.html')
        html = f.read()
        league = League.objects.create(name='test league 2', espn_id='54321', year=2012)
        standings_html = open('local_scrapes/standings.html').read()
        load_teams_from_standings(standings_html, league)
        load_games_from_scoreboard(html, league, 1)
        games = Game.objects.all()
        self.assertEqual(len(games), 5)
        self.assertTrue(any(game.first_scorecard.team.espn_id=='6' and game.second_scorecard.team.espn_id=='1' for game in games))
        self.assertFalse(any(game.first_scorecard.team.espn_id=='6' and game.second_scorecard.team.espn_id=='2' for game in games))

    @clear_test_database
    def test_parse_entrance(self):
        logger.info('test_parse_entrance')
        f = open('local_scrapes2/entrance.html', 'r')
        html = f.read()
        user = init_user()
        load_league_from_entrance(html, user)
        league = League.objects.get(name='Inglorious Basterds')
        self.assertEqual(league.name, 'Inglorious Basterds')
        self.assertEqual(league.year, 2012)
        self.assertEqual(league.espn_id, '930248')

    @clear_test_database
    def test_parse_scores(self):
        logger.info('test_parse_scores')
        f = open('local_scrapes/scoreboard.html')
        html = f.read()
        league = League.objects.create(name="test league", espn_id='12345', year=2012)
        rogues_team = Team.objects.create(league=league, espn_id='3', team_name='Gotham City Rogues', owner_name='Bill Prin')
        replacements_team = Team.objects.create(league=league, espn_id='4', team_name='The Replacements')
        first_scorecard = Scorecard.objects.create(team=rogues_team)
        second_scorecard = Scorecard.objects.create(team=replacements_team)
        game = Game.objects.create(league=league, week=1, first_scorecard=first_scorecard, second_scorecard=second_scorecard)
        load_scores(html, game)

        first_score = sum(entry.points for entry in ScorecardEntry.objects.filter(scorecard=first_scorecard).exclude(slot='Bench'))
        self.assertEqual(first_score, 74)
        second_score = sum(entry.points for entry in ScorecardEntry.objects.filter(scorecard=second_scorecard).exclude(slot='Bench'))
        self.assertEqual(second_score, 62)

class TestSaveGame(unittest.TestCase):
    @clear_test_database
    @hits_live_site
    def test_save_game(self):
        user = init_user()

        logger.info('handling command')
        f = open('local_scrapes/realboard.html', 'r')
        html = f.read()
        league, created = League.objects.get_or_create(name='test league 2', espn_id=54321, year=2012)
        standings_html = open('local_scrapes/standings.html')
        load_teams_from_standings(standings_html, league)
        load_games_from_scoreboard(html, league, 1)

        games = Game.objects.all()
        logger.info("handle(): %d games loaded" % (len(games)))

        browser = EspnScraper()
        browser.login(user.email, user.password)

        logger.info("handles(): successfully logged in")
        browser.save_week(games[0])

        #html = browser.scrape_entrance()
        #league = load_league_from_entrance(html)

        #  load_team_from_standings(html, league)
        #  html = browser.scrape_week(league, 1ma)


