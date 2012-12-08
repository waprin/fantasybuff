from django.utils import unittest
from teams.management.commands.create_league import process_entrance, init_user

from teams.parsers.standings import parse_standings
from teams.models import User, League

import logging
import re

logger = logging.getLogger(__name__)

"""
class Team(models.Model):
    league = models.ForeignKey(League)
    espn_id = models.CharField(max_length=5)
    team_name = models.CharField(max_length=100, null=True)
    owner_name = models.CharField(max_length=100, null=True)
"""



class TeamsTest(unittest.TestCase):

    def test_init_user(self):
        logger.info('test_init_users')
        init_user()
        u = User.objects.get(email='waprin@gmail.com')
        self.assertEqual(u.password, 'terrible')

    def test_parse_standings(self):
        """
        Tests that our sample standings page is parsed correctly
        """
        logger.info('test_parse_standings')
        f = open('local_scrapes/standings.html', 'r')
        html = f.read()
        teams = parse_standings(html)

        logger.info(teams)
        self.assertEqual(len(teams), 10)    
        self.assertTrue(any(team.team_name == 'Gotham City Rogues' and team.espn_id == '6' and team.owner_name == 'bill prin' for team in teams))

    def test_parse_entrance(self):
        logger.info('test_parse_entrance')
        f = open('local_scrapes/entrance.html', 'r')
        html = f.read()
        user = init_user()
        process_entrance(html, user) 
        league = League.objects.get(name='Inglorious Basterds')
        self.assertEqual(league.name, 'Inglorious Basterds')
        self.assertEqual(league.year, 2012)
        self.assertEqual(league.espn_id, '930248')





