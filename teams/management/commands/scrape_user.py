from django.contrib.auth.models import User
from django.core.management import BaseCommand
from teams.management.commands.create_league import get_scraper
from teams.models import EspnUser, League, Team
from teams.scraper.SqlStore import SqlStore
from teams.scraper.scraper import LeagueScraper
import django_rq

__author__ = 'bprin'

import logging
logger = logging.getLogger(__name__)

def defer_league_scrape(espn_user, league):
    if league.year != '2014' or league.espn_id != '930248':
        logger.debug("skipping load of league %s %s" % (league.year, league.espn_id))
    store = SqlStore()
    scraper = get_scraper(espn_user)
    league_scraper = LeagueScraper(scraper, store)
    league_scraper.scrape_league(league)
    league_scraper.load_league(league)

def defer_espn_user_scrape(espn_user):
    store = SqlStore()
    scraper = get_scraper(espn_user)

    league_scraper = LeagueScraper(scraper, store)
    league_scraper.create_leagues(espn_user)

    teams = Team.objects.filter(espn_user=espn_user)
    for team in teams:
        logger.debug("scraping league %s" % team.league.name)
        django_rq.enqueue(defer_league_scrape, espn_user, team.league)



class Command(BaseCommand):
    def handle(self, *args, **options):
        espn_user = EspnUser.objects.all()[0]
        league = League.objects.get(year='2014', espn_id='930248')
        defer_league_scrape(espn_user, league)



