from teams.scraper.FileBrowser import FileBrowser

__author__ = 'bill'


from django.utils import unittest
import logging

logger = logging.getLogger(__name__)

from scraper import get_league_id_from_entrance, get_num_weeks_from_scoreboard


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
