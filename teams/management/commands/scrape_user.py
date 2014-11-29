import traceback

from django.core.cache import cache
from django.core.management import BaseCommand
import django_rq

from teams.management.commands.create_league import get_scraper
from teams.models import League, Team
from teams.scraper.SqlStore import SqlStore
from teams.scraper.report_card import league_report_cache_key, get_team_report_card_json, league_summary_cache_key, \
    get_league_request_context
from teams.scraper.scraper import LeagueScraper


__author__ = 'bprin'

import logging

logger = logging.getLogger(__name__)


def reset_league(league):
    league.pages_scraped = 0
    league.total_pages = 0
    league.loaded = False
    league.loading = False
    league.failed = False
    league.calculating = False
    league.save()


def defer_league_scrape(espn_user, league, load_only=False):
    reset_league(league)

    store = SqlStore()
    scraper = get_scraper(espn_user)
    league_scraper = LeagueScraper(scraper, store)
    try:
        league.failed = False
        league.loading = True
        league.calculating = False
        league.save()
        if not load_only:
            league_scraper.scrape_league(league)
        league_scraper.load_league(league)

        teams = Team.objects.filter(league=league)
        for team in teams:
            cache_key = league_report_cache_key(league.espn_id, league.year, team.espn_id)
            cache.delete(cache_key)
            get_team_report_card_json(league.espn_id, league.year, team.espn_id)
        cache.delete(league_summary_cache_key(league.espn_id, league.year))
        get_league_request_context(league)

    except Exception as e:
        logger.error("caught excepting scraping league %s %s, resetting: %s" % (
        league.espn_id, league.year, traceback.format_exc()))
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
        if team.league.loaded is True:
            logger.info("league %s already loaded, skipping" % str(team.league))
            continue
        if team.league.year == '2014':
            queue = django_rq.get_queue('default')
            queue.enqueue(defer_league_scrape, espn_user, team.league)

    espn_user.loaded = True
    espn_user.save()


class Command(BaseCommand):
    def handle(self, *args, **options):
        espn_id = args[0]
        year = args[1]
        load_only = args[2] == 'True'

        if not espn_id or not year:
            logger.error("must specify espn id and year")
            return
        league = League.objects.get(year=year, espn_id=espn_id)
        team = Team.objects.filter(league=league).exclude(espn_user=None)[0]
        defer_league_scrape(team.espn_user, league, load_only)



