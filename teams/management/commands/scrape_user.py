from django.contrib.auth.models import User
from django.core.management import BaseCommand
from teams.management.commands.create_league import get_scraper
from teams.models import EspnUser
from teams.scraper.SqlStore import SqlStore
from teams.scraper.scraper import LeagueScraper
import django_rq

__author__ = 'bprin'

def defer_espn_user_scrape(espn_user):
    store = SqlStore()
    scraper = get_scraper(espn_user)
    league_scraper = LeagueScraper(scraper, store)
    league_scraper.scrape_espn_user_leagues(espn_user)
    league_scraper.load_espn_user_leagues(espn_user)

"""
import django_rq

def test(request):

    django_rq.enqueue(jobs.count_words_at_url, 'http://nvie.com')
    return HttpResponse("GOOD TO GO : ")

"""

class Command(BaseCommand):
    def handle(self, *args, **options):
        email = args[0]
        store = SqlStore()
        user = User.objects.get(username=email)
        espn_users = EspnUser.objects.filter(user=user)
        for espn_user in espn_users:
            scraper = get_scraper(espn_user)



