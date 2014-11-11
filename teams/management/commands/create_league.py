from django.core.management.base import BaseCommand
from league import settings
from teams.scraper.FileBrowser import FileBrowser
from teams.scraper.scraper import LeagueScraper
from scrape import EspnScraper
from teams.models import  League
import logging

logger = logging.getLogger(__name__)

def get_scraper(espn_user):
    if settings.LOCAL != True:
        scraper = EspnScraper()
        scraper.login(espn_user.username, espn_user.password)
        logger.debug("returning espn scraper")
        return scraper
    else:
        if settings.DB_SCRAPE:
            logger.debug("returning file scraper")
            fb =  FileBrowser()
            fb.sleep = 0.1
            return fb
        else:
            scraper = EspnScraper()
            scraper.login(espn_user.username, espn_user.password)
            logger.debug("returning espn scraper")
            return scraper

class Command(BaseCommand):
    def handle(self, *args, **options):
        scraper = EspnScraper()
        scraper.login('gothamcityrogues', 'sincere1')
        file_browser = FileBrowser()
        league_scraper = LeagueScraper(scraper, file_browser)
        leagues = League.objects.filter(year='2014')
        for league in leagues:
            league_scraper.scrape_league(league)