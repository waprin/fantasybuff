from django.contrib.auth.models import User
from django.core.management import BaseCommand
from teams.management.commands.create_league import get_scraper
from teams.models import EspnUser
from teams.scraper.SqlStore import SqlStore
from teams.scraper.scraper import LeagueScraper

__author__ = 'bprin'

class Command(BaseCommand):
    def handle(self, *args, **options):
        email = args[0]
        store = SqlStore()
        user = User.objects.get(username=email)
        espn_users = EspnUser.objects.filter(user=user)
        for espn_user in espn_users:
            scraper = get_scraper(espn_user)
            league_scraper = LeagueScraper(scraper, store)
            league_scraper.load_leagues(espn_user)

