from django.contrib.auth.models import User
from teams.models import EspnUser, ScoreEntry, PlayerScoreStats, DraftClaim, TradeEntry, AddDrop, League
from teams.scraper.FileBrowser import FileBrowser
from teams.scraper.SqlStore import SqlStore
from django.utils import unittest
from teams.scraper.html_scrapes import get_leagues_from_entrance
from teams.utils.db_utils import clearDb

__author__ = 'bill'

import logging
logger = logging.getLogger(__name__)

from scraper import *

class IntegrationTest(unittest.TestCase):

    def setUp(self):
        clearDb()
        self.browser = FileBrowser()
        self.sqlstore = SqlStore()
        self.league_scraper = LeagueScraper(self.browser, self.sqlstore)


    def test_entire_load_league(self):
        league = League.objects.create(espn_id='930248',year='2013')
        self.league_scraper.scrape_league(league)

        self.assertTrue(self.sqlstore.has_roster(league, '1', 1))
        self.assertTrue(self.sqlstore.has_roster(league, '12', 2))

        self.assertTrue(self.sqlstore.has_player(league, '1428'))
        self.assertTrue(self.sqlstore.has_player(league, '5362'))

        self.league_scraper.load_league(league)
        team = Team.objects.get(league=league, espn_id='1')
        scorecard = Scorecard.objects.get(team=team, week=1, actual=True)
        self.assertEquals(scorecard.points, 96)

    def test_entire_load_league_2014(self):
        league2 = League.objects.create(espn_id='930248',year='2014')
        self.league_scraper.scrape_league(league2)
        self.assertTrue(self.sqlstore.has_game(league2, '1', 1))

        self.league_scraper.load_league(league2)

        team = Team.objects.get(league=league2, espn_id='1')
        scorecard = Scorecard.objects.get(team=team, week=1, actual=True)
        self.assertEquals(scorecard.points, 104)


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

    def test_load_espn_user_leagues(self):
        user = User.objects.create_user('waprin@gmail.com', 'waprin@gmail.com', 'sincere1')
        espn_user = EspnUser.objects.create(pk=1, user=user, username='gothamcityrogues', password='sincere1')
        self.assertFalse(self.sqlstore.has_entrance(espn_user))
        self.league_scraper.scrape_espn_user_leagues(espn_user)
        self.league_scraper.load_espn_user_leagues(espn_user)

        self.assertGreater(len(Team.objects.filter(espn_user=espn_user)), 0)


    def test_load_legacy_entire_lineup(self):
        league = League.objects.create(espn_id='930248',year='2013')
        team_id='1'
        week=1
        team = Team.objects.create(league=league, espn_id=team_id)
        roster_html = self.browser.get_roster(league, team_id, week
        )
        player_ids = get_player_ids_from_lineup(roster_html)
        for player_id in player_ids:
            player_html = self.browser.get_player(player_id)
            load_scores_from_playersheet(player_html, player_id, league.year)
        load_week_from_lineup(roster_html, week, team)

        scorecard = Scorecard.objects.get(team=team, week=1)
        self.assertEquals(scorecard.points, 96)

    def test_load_player(self):
        html = self.browser.get_player('2580', year='2014')
        brees = Player.objects.create(name='Drew Brees', espn_id='2580', position='QB')
        load_scores_from_playersheet(html, '2580', '2014')
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

    def test_load_teams(self):
        league = League.objects.create(espn_id='930248',year='2014')
        user = User.objects.create_user('waprin@gmail.com', 'waprin@gmail.com', 'sincere1')
        espn_user = EspnUser.objects.create(pk=1, user=user, username='gothamcityrogues', password='sincere1')
        team = Team.objects.create(league=league, espn_user=espn_user, team_name='Gotham City Rogues', owner_name='William Prin', espn_id='6')
        html = self.browser.get_standings(league)

        logger.debug("test_load_teams(): ")
        load_teams_from_standings(html, league)

        teams = Team.objects.filter(league=league)
        self.assertEqual(len(teams), 12)
        rogues = Team.objects.get(league=league, espn_id='6')
        self.assertEqual(espn_user, rogues.espn_user)
        self.assertEquals(rogues.abbreviation, 'GCR')

    def test_load_game(self):
        league = League.objects.create(espn_id='930248',year='2014')
        team = Team.objects.create(espn_id='11', league=league)
        team2 = Team.objects.create(espn_id='3', league=league)
        game_html = self.browser.get_game(league, '11', 3)
        load_scores_from_game(league, 3, game_html)

        scorecard = Scorecard.objects.get(team=team, week=3)
        scorecard2 = Scorecard.objects.get(team=team2, week=3)
        self.assertEquals(scorecard.points, 84)
        self.assertEquals(scorecard2.points, 105)

    def test_load_game_on_error(self):
        league = League.objects.create(espn_id='976898',year='2014')
        team = Team.objects.create(espn_id='2', league=league)
        team2 = Team.objects.create(espn_id='9', league=league)
        game_html = open('new_error.html')
        load_scores_from_game(league, 3, game_html)

        scorecard = Scorecard.objects.get(team=team, week=3)
        scorecard2 = Scorecard.objects.get(team=team2, week=3)
        self.assertEquals(scorecard.points, Decimal('129.2'))
        self.assertEquals(scorecard2.points, Decimal('115.4'))

    def test_load_translog_error(self):
        user = User.objects.create_user('waprin@gmail.com', 'waprin@gmail.com', 'sincere1')
        espn_user = EspnUser.objects.create(pk=1, user=user, username='gothamcityrogues', password='sincere1')
        league = League.objects.create(espn_id='976898', year='2014')
        team = Team.objects.create(espn_id='7', league=league)
        filebrowser = FileBrowser()
        html = filebrowser.get_translog('976898', '2014', '7')
        load_transactions_from_translog(html, '2014', team)

    def test_load_translog_error_eli_manning(self):
        user = User.objects.create_user('waprin@gmail.com', 'waprin@gmail.com', 'sincere1')
        espn_user = EspnUser.objects.create(pk=1, user=user, username='gothamcityrogues', password='sincere1')
        league = League.objects.create(espn_id='976898', year='2014')

        team = Team.objects.create(espn_id='7', league=league)
        filebrowser = FileBrowser()
        html = filebrowser.get_translog('976898', '2014', '8')
        load_transactions_from_translog(html, '2014', team)

        eli_manning = AddDrop.objects.filter(player__name='Eli Manning')
        self.assertGreater(eli_manning.count(), 0)

    def test_load_translog_error_allen_robinson(self):
        user = User.objects.create_user('waprin@gmail.com', 'waprin@gmail.com', 'sincere1')
        espn_user = EspnUser.objects.create(pk=1, user=user, username='gothamcityrogues', password='sincere1')
        league = League.objects.create(espn_id='976898', year='2014')

        team = Team.objects.create(espn_id='5', league=league)
        filebrowser = FileBrowser()
        html = filebrowser.get_translog('976898', '2014', '5')
        load_transactions_from_translog(html, '2014', team)

        allen_robinson = AddDrop.objects.filter(player__name='Allen Robinson')
        self.assertGreater(allen_robinson.count(), 0)

    def test_load_translog_error_toby_gerhart(self):
        user = User.objects.create_user('waprin@gmail.com', 'waprin@gmail.com', 'sincere1')
        espn_user = EspnUser.objects.create(pk=1, user=user, username='gothamcityrogues', password='sincere1')
        league = League.objects.create(espn_id='976898', year='2014')

        team = Team.objects.create(espn_id='2', league=league, abbreviation='WAGN')
        team = Team.objects.create(espn_id='5', league=league, abbreviation='BART')
        filebrowser = FileBrowser()
        html = filebrowser.get_translog('976898', '2014', '2')
        load_transactions_from_translog(html, '2014', team)

        toby_gerhart = TradeEntry.objects.filter(players_added__name='Toby Gerhart')
        self.assertGreater(toby_gerhart.count(), 0)

    def test_load_translog_error_toby_gerhart_2(self):
        user = User.objects.create_user('waprin@gmail.com', 'waprin@gmail.com', 'sincere1')
        espn_user = EspnUser.objects.create(pk=1, user=user, username='gothamcityrogues', password='sincere1')
        league = League.objects.create(espn_id='976898', year='2014')

        team1 = Team.objects.create(espn_id='2', league=league, abbreviation='BART')
        team2 = Team.objects.create(espn_id='10', league=league, abbreviation='WAGN')
        filebrowser = FileBrowser()
        html = filebrowser.get_translog('976898', '2014', '10')
        load_transactions_from_translog(html, '2014', team2)

        toby_gerhart = TradeEntry.objects.filter(players_removed__name='Toby Gerhart')
        self.assertGreater(toby_gerhart.count(), 0)

    def test_load_translog_error_alex_smith(self):
        user = User.objects.create_user('waprin@gmail.com', 'waprin@gmail.com', 'sincere1')
        espn_user = EspnUser.objects.create(pk=1, user=user, username='gothamcityrogues', password='sincere1')
        league = League.objects.create(espn_id='976898', year='2014')

        team2 = Team.objects.create(espn_id='11', league=league, abbreviation='WAGN')
        filebrowser = FileBrowser()
        html = filebrowser.get_translog('930248', '2014', '11')
        load_transactions_from_translog(html, '2014', team2)

        alex_smith = AddDrop.objects.filter(player__name='Alex Smith')
        self.assertGreater(alex_smith.count(), 0)

    def test_load_translog_error_mohammed(self):
        user = User.objects.create_user('waprin@gmail.com', 'waprin@gmail.com', 'sincere1')
        espn_user = EspnUser.objects.create(pk=1, user=user, username='gothamcityrogues', password='sincere1')
        league = League.objects.create(espn_id='1044126', year='2014')

        team2 = Team.objects.create(espn_id='11', league=league, abbreviation='WAGN')
        filebrowser = FileBrowser()
        html = filebrowser.get_translog('1044126', '2014', '7')
        load_transactions_from_translog(html, '2014', team2)

        mo_sanu = AddDrop.objects.filter(player__name='Mohamed Sanu')
        self.assertGreater(mo_sanu.count(), 0)




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

    def test_load_translog(self):
        league = League.objects.create(espn_id='930248',year='2014')
        self.league_scraper.scrape_league(league)
        self.league_scraper.load_league(league)
        team = Team.objects.get(espn_id='6', league=league)
        self.assertEquals(16, len(DraftClaim.objects.filter(team=team)))

        team2 = Team.objects.get(espn_id='3', league=league)
        self.assertEquals(16, len(DraftClaim.objects.filter(team=team2)))

        team3 = Team.objects.get(espn_id='2', league=league)
        trade_count = TradeEntry.objects.filter(team=team3).count()
        trade_count_other = TradeEntry.objects.filter(other_team=team3).count()
        self.assertEquals(1, trade_count)
        self.assertEquals(1, trade_count_other)


        team6 = Team.objects.get(espn_id=6, league=league)
        hoyer = Player.objects.get(name="Brian Hoyer")
        waiver_add = AddDrop.objects.get(team=team6, player=hoyer)
        self.assertEquals(waiver_add.added, True)

        """
        all = AddDrop.objects.filter(team=team3)
        self.assertGreater(len(all), 0)

        before_week2 = AddDrop.objects.get_before_week(team3, 2)
        self.assertEquals(len(before_week2), 10)

        before_week3 = AddDrop.objects.get_before_week(team3, 3)
        self.assertEquals(len(before_week3), 12)

        logger.debug("test_translog:  get waiver points")
        waiver_score = team3.get_waiver_points(4)
        self.assertEquals(waiver_score, 3)
        """
        davis = Player.objects.get(name='Austin Davis')
        davis_entry = ScorecardEntry.objects.filter(player=davis, week=6)[0]
        self.assertEquals(davis_entry.source, 'W')

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
        self.assertIn(('Inglorious Basterds', '930248', '2013', '6'), leagues)
        self.assertIn(('Inglorious Basterds', '930248', '2014', '6'), leagues)
        self.assertIn(('Bizarro League III', '1880759', '2014', '9'), leagues)


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










