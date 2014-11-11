import traceback
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

def reset_league(league):
    league.pages_scraped = 0
    league.total_pages = 0
    league.loaded = False
    league.loading = False
    league.failed = True
    league.save()


def defer_league_scrape(espn_user, league):
    store = SqlStore()
    scraper = get_scraper(espn_user)
    league_scraper = LeagueScraper(scraper, store)
    try:
        league.failed = False
        league.save()
        league_scraper.scrape_league(league)
        league_scraper.load_league(league)
    except Exception as e:
        logger.error("caught excepting scraping league %s %s, resetting: %s" % (league.espn_id, league.year, traceback.format_exc()))
        reset_league(league)
        raise e

def defer_espn_user_scrape(espn_user):
    store = SqlStore()
    scraper = get_scraper(espn_user)

    league_scraper = LeagueScraper(scraper, store)
    league_scraper.create_leagues(espn_user)

    teams = Team.objects.filter(espn_user=espn_user)
    for team in teams:
        logger.debug("scraping league %s" % team.league.name)
        team.league.loading = True
        team.league.loaded = False
        team.league.failed = False
        team.league.save()
        if team.league.year == '2014':
            queue = django_rq.get_queue('default')
        else:
            queue = django_rq.get_queue('low')
        queue.enqueue(defer_league_scrape, espn_user, team.league)



class Command(BaseCommand):
    def handle(self, *args, **options):
        espn_user = EspnUser.objects.all()[0]
        leagues = League.objects.filter(year='2014', espn_id='930248')
        for league in leagues:
            defer_league_scrape(espn_user, league)



