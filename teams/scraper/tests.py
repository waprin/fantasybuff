from teams.models import League, EspnUser
from teams.scraper.FileBrowser import FileBrowser
from teams.scraper.SqlStore import SqlStore
from teams.scraper.html_scrapes import get_leagues_from_entrance, get_teams_from_standings, get_num_weeks_from_matchups, \
    get_player_ids_from_lineup

__author__ = 'bill'


from django.utils import unittest
import logging

logger = logging.getLogger(__name__)

from scraper import *
from teams.utils.db_utils import clear_test_database

class ScraperTest(unittest.TestCase):

    def setUp(self):
        self.browser = FileBrowser()
        self.sqlstore = SqlStore()
        self.league_scraper = LeagueScraper(self.browser, self.sqlstore)

    @clear_test_database
    def test_create_leagues(self):
        user = EspnUser.objects.create(id=1,email='waprin@gmail.com', password='sincere1')
        self.assertFalse(self.sqlstore.has_entrance(user))
        self.league_scraper.create_leagues(user)
        self.assertTrue(self.sqlstore.has_entrance(user))

    @clear_test_database
    def test_create_league(self):
        league = League.objects.create(espn_id='930248',year='2014')
        self.league_scraper.create_league(league)

        self.assertTrue(self.sqlstore.has_roster(league, '1', 1))
        self.assertTrue(self.sqlstore.has_roster(league, '12', 2))

        self.assertTrue(self.sqlstore.has_player(league, '1428'))
        self.assertTrue(self.sqlstore.has_player(league, '5362'))


    @clear_test_database
    def test_get_real_num_weeks(self):
        user = EspnUser.objects.create(id=1,email='waprin@gmail.com', password='sincere1')
        self.assertFalse(self.sqlstore.has_entrance(user))
        self.league_scraper.create_leagues(user)
        old_league = League.objects.filter(year='2013')[0]

        old_num_weeks = self.league_scraper.get_real_num_weeks(13, league=old_league)
        self.assertEquals(old_num_weeks, 13)

        # TODO - better protect this from time changes
        current_league = League.objects.filter(year=2014)[0]
        current_num_weeks = self.league_scraper.get_real_num_weeks(13, league=current_league)
        print current_num_weeks
        self.assertLess(current_num_weeks, 13)


    @clear_test_database
    def test_scrape_entrance(self):
        user = EspnUser.objects.create(id=1,email='waprin@gmail.com', password='sincere1')
        self.assertTrue(self.browser.has_entrance(user))
        html = self.browser.get_entrance(user)

        leagues = get_leagues_from_entrance(html)
        self.assertEquals(len(leagues), 3)
        self.assertIn(('Inglorious Basterds', '930248', '2013'), leagues)
        self.assertIn(('Inglorious Basterds', '930248', '2014'), leagues)
        self.assertIn(('Bizarro League III', '1880759', '2014'), leagues)

    @clear_test_database
    def test_scrape_players_from_lineup(self):
        league = League.objects.create(name='ib', espn_id='930248', year='2014')
        html = self.browser.get_roster(league, '1', 1)
        players = get_player_ids_from_lineup(html)
        self.assertIn('14874', players)
        self.assertEquals(len(players), 16)

    @clear_test_database
    def test_scrape_teams_from_standings(self):
        league = League.objects.create(name='ib', espn_id='930248', year='2013')
        self.assertTrue(self.browser.has_standings(league))

        teams = get_teams_from_standings(self.browser.get_standings(league))
        self.assertEquals(len(teams), 12)
        self.assertIn(('5', 'Not a  Prinhead ', 'Matthew Prin'), teams)
        self.assertIn(('4', "Geno's Cheesesteaks ", 'Matt Secko'), teams)

    @clear_test_database
    def test_get_num_weeks_from_matchups(self):
        league = League.objects.create(name='ib', espn_id='930248', year='2013')
        self.assertTrue(self.browser.has_matchups(league, 1))

        num_weeks = get_num_weeks_from_matchups(self.browser.get_matchups(league, 1))
        self.assertEquals(num_weeks, 13)

        league = League.objects.create(name='ib', espn_id='930248', year='2014')
        self.assertTrue(self.browser.has_matchups(league, 1))

        num_weeks = get_num_weeks_from_matchups(self.browser.get_matchups(league, 1))
        self.assertEquals(num_weeks, 13)

    """
    def test_get_players_from_roster(self):
        html = open('rostersummary.html').read()
        players = get_players_from_roster(html)
        self.assertEqual(players[0][0], '2580')
        self.assertEquals(players[0][1], 'Drew Brees')



    def test_get_defenses_from_roster(self):
        browser = FileBrowser()
        html = browser.scrape_defense()
        defenses = get_defenses_from_roster(html)
        self.assertEquals(defenses[0], '60026')
        self.assertEquals(len(defenses), 32)

    def test_file_cache(self):
        browser = FileBrowser()
        self.assertTrue(browser.contains_player('2580'))
        self.assertFalse(browser.contains_player('2581'))
    """





