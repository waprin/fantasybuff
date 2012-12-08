from django.core.management.base import BaseCommand, CommandError
from teams.models import User, League

from bs4 import BeautifulSoup
import re

from teams.util import get_name
import logging

logger = logging.getLogger(__name__)

"""

class Team(models.Model):
    league = models.ForeignKey(League)
    espn_id = models.CharField(max_length=5)
    team_name = models.CharField(max_length=100, null=True)
    owner_name = models.CharField(max_length=100, null=True)


class League(models.Model):
    users = models.ManyToManyField(User)
    name = models.CharField(max_length=200)
    espn_id = models.CharField(max_length=30)
    year = models.IntegerField()

class User(models.Model):
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
"""

def init_user():
    try:
        user = User.objects.get(email='waprin@gmail.com')
    except User.DoesNotExist:
        user = User.objects.create(email='waprin@gmail.com', password='terrible')
    return user

def load_team_from_standings(html, league):
    pool = BeautifulSoup(html)
    header = pool.find('div', 'games-pageheader')
    standings = header.findNextSibling('table')
    bodies = standings.findAll('tr', 'tableBody')

    for body in bodies:
        fullname = body.td.a['title']
        href = body.td.a['href']
        info = re.search("teamId=(\d+)", href)
        matchedname = re.search("(.*)\s*\((.*)\)", fullname)
        team_name = matchedname.group(1)
        owner_name = matchedname.group(2)
        team = Team(team_name=team_name.strip(), espn_id = info.group(1), owner_name=owner_name)
        team.save()


def load_league_from_entrance(html, user):
    m = re.search(r'leagueId=(\d*)&teamId=(\d*)&seasonId=(\d*)', html)
    league_id= m.group(1)
    team_id = m.group(2)
    season_id = m.group(3)

    pool = BeautifulSoup(html)
    logger.debug('pool successfully initialized')
    league_name = pool.find('a', 'leagueoffice-link').string
    logger.debug('league name found is ' + league_name)
    
    try:
        league = League.objects.get(espn_id=league_id)
    except League.DoesNotExist:
        league = League(espn_id=league_id, year=2012, name=league_name)
        league.save()
        league.users.add(user)
        league.save()
    return league

class Command(BaseCommand):

    def handle(self, *args, **options):
        user = init_user()
        browser = EspnBrower()
        browser.login(user.team_name, user.password)
        html = browser.scrape_entrance()
        league = load_league_from_entrance(html)
        html = browser.scrape_standings()
        load_team_from_standings(html, league)

