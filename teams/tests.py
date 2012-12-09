from django.utils import unittest
from teams.management.commands.create_league import *
from teams.models import User, League, Team

import logging
logger = logging.getLogger(__name__)

def clear_test_database(fn):
    def wrapper(self):
        Team.objects.all().delete()
        User.objects.all().delete()
        League.objects.all().delete()
        fn(self)
    return wrapper

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
    def test_get_num_games(self):
        logger.info('test_get_num_games')
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
        f = open('local_scrapes/entrance.html', 'r')
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


