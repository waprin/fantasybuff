from teams.scraper.FileBrowser import FileBrowser

__author__ = 'bill'


from django.utils import unittest
import logging

logger = logging.getLogger(__name__)

from scraper import *


class ScraperTest(unittest.TestCase):

    def test_scrape_entrance(self):
        browser = FileBrowser()
        html = browser.scrape_entrance()
        espn_id = get_league_id_from_entrance(html)
        self.assertEquals(espn_id, "930248")

    def test_get_num_weeks(self):
        browser = FileBrowser()
        html = browser.scrape_scoreboard(None, 1)
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






