from django.contrib.auth.models import User
from django.utils import unittest
import teams
from teams.management.commands.scrape_user import defer_espn_user_scrape, defer_league_scrape
from teams.models import EspnUser, Team
from teams.utils.db_utils import clearDb

__author__ = 'bprin'

import logging
logger = logging.getLogger(__name__)

@unittest.skip("too long")
class DeferJobsTest(unittest.TestCase):

    def test_defer_scrape_espn_user(self):
        clearDb()
        user = User.objects.create_user('waprin@gmail.com', 'waprin@gmail.com', 'sincere1')
        self.espn_user = EspnUser.objects.create(user=user, username='gothamcityrogues', password='sincere1')

        defer_espn_user_scrape(self.espn_user)

        team = Team.objects.filter(espn_user=self.espn_user)[0]
        defer_league_scrape(self.espn_user, team.league)

        self.assertEquals(3,3)




