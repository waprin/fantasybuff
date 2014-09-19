from django.contrib.auth.models import User
from django.db import connection
from teams.models import League, EspnUser, Player, ScoreEntry, Team, ScorecardEntry, Scorecard
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

def clearDb():
    logger.info("clearing: conncetion queries is %s" % str(connection.queries))
    for user in User.objects.all():
        user.delete()
    for user in EspnUser.objects.all():
        user.delete()
    for league in League.objects.all():
        league.delete()


class LeagueCreatorTest(unittest.TestCase):

    def setUp(self):
        clearDb()
        self.browser = FileBrowser()
        self.sqlstore = SqlStore()
        self.league_scraper = LeagueScraper(self.browser, self.sqlstore)

    def test_create_espn_user_leagues(self):
        user = User.objects.create_user('waprin@gmail.com', 'waprin@gmail.com', 'sincere1')
        espn_user = EspnUser.objects.create(pk=1, user=user, username='gothamcityrogues', password='sincere1')
        self.assertFalse(self.sqlstore.has_entrance(espn_user))
        self.league_scraper.scrape_espn_user_leagues(espn_user)
        self.assertTrue(self.sqlstore.has_entrance(espn_user))

    def test_scrape_league(self):
        league = League.objects.create(espn_id='930248',year='2014')
        self.league_scraper.scrape_league(league)
        self.league_scraper.scrape_players(league)

        self.assertTrue(self.sqlstore.has_roster(league, '1', 1))
        self.assertTrue(self.sqlstore.has_roster(league, '12', 2))

        self.assertTrue(self.sqlstore.has_player(league, '1428'))
        self.assertTrue(self.sqlstore.has_player(league, '5362'))

    def test_load_players(self):
        league = League.objects.create(espn_id='930248',year='2014')

        self.league_scraper.scrape_league(league)
        self.league_scraper.scrape_players(league)
        self.league_scraper.load_players(league)

        brees = Player.objects.get(espn_id='2580')
        self.assertEqual(brees.name, 'Drew Brees')
        self.assertEquals(brees.position, 'QB')

        entries = ScoreEntry.objects.filter(player=brees)
        self.assertEqual(len(entries), 17)
        self.assertEqual(entries.get(week=1).points, 15)
        self.assertEqual(entries.get(week=17).points, 0)

    def test_load_teams(self):
        league = League.objects.create(espn_id='930248',year='2014')

        self.league_scraper.scrape_league(league)
        self.league_scraper.scrape_players(league)
        self.league_scraper.load_teams(league)

        teams = Team.objects.filter(league=league)
        self.assertEqual(len(teams), 12)

    def test_load_lineups(self):
        league = League.objects.create(espn_id='930248',year='2014')

        self.league_scraper.scrape_league(league)
        self.league_scraper.scrape_players(league)
        self.league_scraper.load_teams(league)
        self.league_scraper.load_players(league)
        self.league_scraper.load_lineups(league)


        edelman = Player.objects.get(name='Julian Edelman')
        team_1 = Team.objects.get(espn_id='1')

        scorecard = Scorecard.objects.get(team=team_1, week=1)
        scorecard_entry = ScorecardEntry.objects.get(player=edelman, scorecard=scorecard)
        self.assertEquals(scorecard_entry.slot, 'Bench')
        self.assertEquals(scorecard_entry.points, 11)



    def test_get_real_num_weeks(self):
        user = User.objects.create_user('waprin@gmail.com', 'waprin@gmail.com', 'sincere1')
        espn_user = EspnUser.objects.create(pk=1, user=user, username='gothamcityrogues', password='sincere1')
        self.assertFalse(self.sqlstore.has_entrance(espn_user))
        self.league_scraper.create_leagues(espn_user)
        old_league = League.objects.filter(year='2013')[0]

        old_num_weeks = get_real_num_weeks(13, league=old_league)
        self.assertEquals(old_num_weeks, 13)

        # TODO - better protect this from time changes
        current_league = League.objects.filter(year=2014)[0]
        current_num_weeks = get_real_num_weeks(13, league=current_league)
        print current_num_weeks
        self.assertLess(current_num_weeks, 13)



class ScraperTest(unittest.TestCase):

    def setUp(self):
        clearDb()
        self.browser = FileBrowser()
        self.sqlstore = SqlStore()


    def test_scrape_entrance(self):
        user = User.objects.create_user('waprin@gmail.com', 'waprin@gmail.com', 'sincere1')
        espn_user = EspnUser.objects.create(pk=1, user=user, username='gothamcityrogues', password='sincere1')
        self.assertTrue(self.browser.has_entrance(espn_user))
        html = self.browser.get_entrance(espn_user)

        leagues = get_leagues_from_entrance(html)
        self.assertEquals(len(leagues), 3)
        self.assertIn(('Inglorious Basterds', '930248', '2013'), leagues)
        self.assertIn(('Inglorious Basterds', '930248', '2014'), leagues)
        self.assertIn(('Bizarro League III', '1880759', '2014'), leagues)


    def test_scrape_players_from_lineup(self):
        league = League.objects.create(name='ib', espn_id='930248', year='2014')
        html = self.browser.get_roster(league, '1', 1)
        players = get_player_ids_from_lineup(html)
        self.assertIn('14874', players)
        self.assertEquals(len(players), 16)

    def test_scrape_teams_from_standings(self):
        league = League.objects.create(name='ib', espn_id='930248', year='2013')
        self.assertTrue(self.browser.has_standings(league))

        teams = get_teams_from_standings(self.browser.get_standings(league))
        self.assertEquals(len(teams), 12)
        self.assertIn(('5', 'Not a  Prinhead ', 'Matthew Prin'), teams)
        self.assertIn(('4', "Geno's Cheesesteaks ", 'Matt Secko'), teams)


    def test_get_num_weeks_from_matchups(self):
        league = League.objects.create(name='ib', espn_id='930248', year='2013')
        self.assertTrue(self.browser.has_matchups(league, 1))

        num_weeks = get_num_weeks_from_matchups(self.browser.get_matchups(league, 1))
        self.assertEquals(num_weeks, 13)

        league = League.objects.create(name='ib', espn_id='930248', year='2014')
        self.assertTrue(self.browser.has_matchups(league, 1))

        num_weeks = get_num_weeks_from_matchups(self.browser.get_matchups(league, 1))
        self.assertEquals(num_weeks, 13)





