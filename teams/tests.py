from django.utils import unittest
from teams.management.commands.create_league import *
from teams.models import User, League, Team

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
        browser = FileBrowser()
        html = browser.scrape_standings()
        league = League.objects.create(name="test league", espn_id='12345', year=2012)
        load_teams_from_standings(html, league)
        teams = Team.objects.all()

        logger.info(teams)
        self.assertEqual(len(teams), 12)
        self.assertTrue(any(team.team_name == 'Gotham City Rogues' and team.espn_id == '6' and team.owner_name == 'bill prin' for team in teams))

    @clear_test_database
    def test_load_games_from_scoreboard(self):
        browser = FileBrowser()

        html = browser.scrape_scoreboard(None, 1)

        league = League.objects.create(name='test league 2', espn_id='54321', year=2012)
        standings_html = browser.scrape_standings()
        load_teams_from_standings(standings_html, league)

        load_games_from_scoreboard(html, league, 1)
        games = Game.objects.all()
        self.assertEqual(len(games), 6)
        self.assertTrue(any(game.first_scorecard.team.espn_id=='6' and game.second_scorecard.team.espn_id=='1' for game in games))
        self.assertFalse(any(game.first_scorecard.team.espn_id=='6' and game.second_scorecard.team.espn_id=='2' for game in games))

    @clear_test_database
    def test_parse_entrance(self):
        browser = FileBrowser()
        html = browser.scrape_entrance()


        user = init_user()
        load_league_from_entrance(html, user)
        league = League.objects.get(name='Inglorious Basterds')
        self.assertEqual(league.name, 'Inglorious Basterds')
        self.assertEqual(league.year, 2012)
        self.assertEqual(league.espn_id, '930248')


    @clear_test_database
    def test_parse_scores(self):
        browser = FileBrowser()
        html = browser.scrape_all_games(1)[2]
        league = League.objects.create(name="test league", espn_id='12345', year=2013)
        replacements_team = Team.objects.create(league=league, espn_id='1', team_name='My Vick in a Box')
        rogues_team = Team.objects.create(league=league, espn_id='3', team_name='Gotham City Rogues', owner_name='Bill Prin')
        first_scorecard = Scorecard.objects.create(team=rogues_team)
        second_scorecard = Scorecard.objects.create(team=replacements_team)
        game = Game.objects.create(league=league, week=1, first_scorecard=first_scorecard, second_scorecard=second_scorecard)

        load_scores(html, game)

        first_score = sum(entry.points for entry in ScorecardEntry.objects.filter(scorecard=first_scorecard).exclude(slot='Bench'))
        self.assertEqual(first_score, 140)
        second_score = sum(entry.points for entry in ScorecardEntry.objects.filter(scorecard=second_scorecard).exclude(slot='Bench'))
        self.assertEqual(second_score, 96)

    @clear_test_database
    def test_parse_playersheets(self):
        browser = FileBrowser()
        htmls = browser.scrape_all_players('6')
        league = League.objects.create(name="test league", espn_id='12345', year=2013)
        for html in htmls:
            load_scores_from_playersheet(html, league)
        brees = Player.objects.get(espn_id='2580')
        self.assertEqual(brees.name, 'Drew Brees')
        self.assertEquals(brees.position, 'QB')

        entries = ScoreEntry.objects.filter(player=brees)
        self.assertEqual(len(entries), 17)
        self.assertEqual(entries.get(week=1).points, 20)
        self.assertEqual(entries.get(week=17).points, 37)

    @clear_test_database
    def test_parse_defenses(self):
        browser = FileBrowser()
        defenses = browser.scrape_all_players('defenses')
        league = League.objects.create(name="test league", espn_id='12345', year=2013)
        for defense in defenses:
            load_scores_from_playersheet(defense[1], league, defense[0])

        falconsd = Player.objects.get(espn_id='60001')
        self.assertEqual(falconsd.name, 'Falcons D/ST')
        self.assertEquals(falconsd.position, 'D/ST')

        entries = ScoreEntry.objects.filter(player=falconsd)
        self.assertEqual(len(entries), 17)
        self.assertEqual(entries.get(week=1).points, 1)
        self.assertEqual(entries.get(week=17).points, 7)

    @clear_test_database
    def test_parse_translog(self):
        league = League.objects.create(name="test league", espn_id='12345', year=2013)
        rogues_team = Team.objects.create(league=league, espn_id='6', team_name='Gotham City Rogues', owner_name='Bill Prin')
        browser = FileBrowser()
        players = browser.scrape_all_players('6')
        players = players + browser.scrape_all_players('defenses')
        for player in players:
            load_scores_from_playersheet(player[1], league, player[0])
        html = browser.scrape_translogs('6')

        load_transactions(html, 2013)

        draft_transactions = DraftClaim.objects.filter(player='6')
        self.assertEquals(len(draft_transactions), 16)






"""
    @clear_test_database
    def test_parse_scores(self):
        browser = FileBrowser()
        html = browser.scrape_all_games(1)[2]
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
"""

