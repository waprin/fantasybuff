from django.contrib.auth.models import User
from django.db import connection
from teams.models import League, EspnUser, Player, ScoreEntry, Team, ScorecardEntry, Scorecard, PlayerScoreStats
from teams.scraper.FileBrowser import FileBrowser
from teams.scraper.SqlStore import SqlStore
from teams.scraper.html_scrapes import get_leagues_from_entrance, get_teams_from_standings, get_num_weeks_from_matchups, \
    get_player_ids_from_lineup
from teams.scraper.league_loader import load_scores_from_game

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
    for player_stats in PlayerScoreStats.objects.all():
        player_stats.delete()



class LeagueCreatorTest(unittest.TestCase):

    def setUp(self):
        clearDb()
        self.browser = FileBrowser()
        self.sqlstore = SqlStore()
        self.league_scraper = LeagueScraper(self.browser, self.sqlstore)
        #logging.disable(logging.CRITICAL)

    def test_create_espn_user_leagues(self):
        user = User.objects.create_user('waprin@gmail.com', 'waprin@gmail.com', 'sincere1')
        espn_user = EspnUser.objects.create(pk=1, user=user, username='gothamcityrogues', password='sincere1')
        self.assertFalse(self.sqlstore.has_entrance(espn_user))
        self.league_scraper.scrape_espn_user_leagues(espn_user)
        self.assertTrue(self.sqlstore.has_entrance(espn_user))

    @unittest.skip("will fix in a bit")
    def test_scrape_league(self):
        league = League.objects.create(espn_id='930248',year='2014')
        self.league_scraper.scrape_league(league)
        self.league_scraper.scrape_players(league)

        self.assertTrue(self.sqlstore.has_roster(league, '1', 1))
        self.assertTrue(self.sqlstore.has_roster(league, '12', 2))

        self.assertTrue(self.sqlstore.has_player(league, '1428'))
        self.assertTrue(self.sqlstore.has_player(league, '5362'))


    def test_load_player(self):
        html = self.browser.get_player('2580', None)
        brees = Player.objects.create(name='Drew Brees', espn_id='2580', position='QB')
        load_scores_from_playersheet(html, '2014')
        self.assertEquals(17, PlayerScoreStats.objects.all().count())

        sc = ScoreEntry.objects.get(week=1, year='2014', player=brees)
        ps1 = sc.player_score_stats
        self.assertEquals(ps1.pass_yards, 333)
        self.assertEquals(ps1.pass_td, 1)
        self.assertEquals(ps1.default_points, 15)

        sc2 = ScoreEntry.objects.get(week=2, year='2014', player=brees)
        ps2 = sc2.player_score_stats
        self.assertEquals(ps2.pass_yards, 237)
        self.assertEquals(ps2.pass_td, 2)
        self.assertEquals(ps2.default_points, 15)

    @unittest.skip("will fix in a bit")
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

    @unittest.skip("will fix in a bit")
    def test_load_lineups(self):
        league = League.objects.create(espn_id='930248',year='2014')

        self.league_scraper.scrape_league(league)

        self.league_scraper.load_teams(league)
        self.league_scraper.load_players(league)
        self.league_scraper.load_lineups(league)


        edelman = Player.objects.get(name='Julian Edelman')
        team_1 = Team.objects.get(espn_id='1')

        scorecard = Scorecard.objects.get(team=team_1, week=1)
        scorecard_entry = ScorecardEntry.objects.get(player=edelman, scorecard=scorecard)
        self.assertEquals(scorecard_entry.slot, 'Bench')
        self.assertEquals(scorecard_entry.points, 11)

    def test_load_game(self):
        league = League.objects.create(espn_id='930248',year='2014')
        team = Team.objects.create(espn_id='11', league=league, league_espn_id='930248')
        team2 = Team.objects.create(espn_id='3', league=league, league_espn_id='930248')
        game_html = self.browser.get_game(league, '11', 3)
        load_scores_from_game(league, 3, game_html)

        scorecard = Scorecard.objects.get(team=team, week=3)
        scorecard2 = Scorecard.objects.get(team=team2, week=3)
        self.assertEquals(scorecard.points, 84)
        self.assertEquals(scorecard2.points, 105)

    @unittest.skip("will fix in a bit")
    def test_entire_load_league(self):
        league = League.objects.create(espn_id='930248',year='2014')
        self.league_scraper.load_league(league)

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

    def test_get_matchups_from_matchups_page(self):
        league = League.objects.create(name='ib', espn_id='930248', year='2014')
        self.assertTrue(self.browser.has_matchups(league, 1))

        matchups = get_teams_from_matchups(self.browser.get_matchups(league, 1))
        self.assertEquals(len(matchups), 6)
        for i in range(1, 13):
            self.assertTrue(str(i) in [item for sublist in matchups for item in sublist])








