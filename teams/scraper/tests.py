from teams.models import User
from teams.scraper.FileBrowser import FileBrowser
from teams.scraper.SqlStore import SqlStore
from teams.scraper.html_scrapes import get_leagues_from_entrance

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
    def test_create_league_directory(self):
        self.user = User.objects.create(id=1,email='waprin@gmail.com', password='sincere1')
        self.assertFalse(self.sqlstore.has_entrance(self.user))
        self.league_scraper.create_league_directory(self.user)
        self.assertTrue(self.sqlstore.has_entrance(self.user))

    @clear_test_database
    def test_scrape_entrance(self):
        self.user = User.objects.create(id=1,email='waprin@gmail.com', password='sincere1')
        self.assertTrue(self.browser.has_entrance(self.user))
        html = self.browser.get_entrance(self.user)

        leagues = get_leagues_from_entrance(html)
        self.assertEquals(len(leagues), 3)
        self.assertIn(('Inglorious Basterds', '930248', '2013'), leagues)
        self.assertIn(('Inglorious Basterds', '930248', '2014'), leagues)
        self.assertIn(('Bizarro League III', '1880759', '2014'), leagues)
    """
    def test_get_num_weeks(self):
        html = self.browser.scrape_scoreboard(None, 1)
        num_weeks = get_num_weeks_from_scoreboard(html)
        self.assertEqual(num_weeks, 13)

    def test_get_players_from_roster(self):
        html = open('rostersummary.html').read()
        players = get_players_from_roster(html)
        self.assertEqual(players[0][0], '2580')
        self.assertEquals(players[0][1], 'Drew Brees')

    def test_get_players_from_lineup(self):
        html = open('lineup.html').read()
        players = get_player_ids_from_lineup(html)
        print players
        self.assertEquals(players[0], '2580')
        self.assertEquals(len(players), 16)


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





