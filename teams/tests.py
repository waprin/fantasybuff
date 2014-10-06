from django.contrib.auth.models import User
from django.utils import unittest
from teams.models import League, EspnUser
from teams.utils.db_utils import clearDb
from teams.views import get_all_leagues_json

__author__ = 'bprin'

class IntegrationTest(unittest.TestCase):

    def setUp(self):
        clearDb()

    def test_get_all_leagues_json(self):
        class FakeRequest():
            def __init__(self):
                self.user = User.objects.create_user('waprin@gmail.com', 'waprin@gmail.com', 'sincere1')
                espn_user = EspnUser.objects.create(pk=1, user=self.user, username='gothamcityrogues', password='sincere1')
                league = League.objects.create(espn_id='930248',year='2013')
        get_all_leagues_json(FakeRequest())

