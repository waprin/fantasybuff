__author__ = 'bprin'

from django.contrib.auth.models import User
from django.core.management import BaseCommand
from teams.management.commands.create_league import get_scraper
from teams.models import EspnUser, League
from teams.scraper.SqlStore import SqlStore
from teams.scraper.scraper import LeagueScraper

__author__ = 'bprin'

class Command(BaseCommand):
    def handle(self, *args, **options):
        espn_id = args[0]
        year= args[1]
        store = SqlStore()
        league = League.objects.get(espn_id=espn_id, year=year)
        scraper = get_scraper(league.users.all()[0])
        league_scraper = LeagueScraper(scraper, store)
        league_scraper.scrape_players(league)


