from decimal import Decimal
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction
from league import settings
from teams.metrics.lineup_calculator import calculate_optimal_lineup, get_lineup_score
from teams.scraper.FileBrowser import FileBrowser
from teams.scraper.SqlStore import SqlStore
from teams.scraper.scraper import LeagueScraper
from scrape import EspnScraper
from teams.models import EspnUser, League, Team, Player, ScorecardEntry, Scorecard, Game, ScoreEntry, TransLogEntry, DraftClaim
from bs4 import BeautifulSoup
import re
import logging
import datetime

logger = logging.getLogger(__name__)


def load_transactions(html, year):
    soup = BeautifulSoup(html)
    rows = soup.find_all('table')[0].find_all('tr')[3:]
    rows.reverse()
    draft_round = 1
    for row in rows:
        player_name = row.contents[2].b.string
        transaction_type = rows[0].contents[1].contents[-1]

        date_str = ' '.join(list(rows[0].contents[0].strings))
        date = datetime.datetime.strptime(date_str, '%a, %b %d %I:%M %p')
        date.replace(year=year)

        player = Player.objects.get(name=str(player_name))
        team = Team.objects.get(espn_id='6')

        if transaction_type == 'Draft':
            draft_entry = DraftClaim(date=date,round=draft_round, player_added=player, player=team)
            draft_round = draft_round + 1
            draft_entry.save()

def get_scraper(espn_user):
    if settings.LOCAL != True:
        scraper = EspnScraper()
        scraper.login(espn_user.username, espn_user.password)
        logger.debug("returning espn scraper")
        return scraper
    else:
        if settings.DB_SCRAPE:
            logger.debug("returning file scraper")
            return FileBrowser()
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
        league = League.objects.get(espn_id='930248', year='2014')
        league_scraper.scrape_league(league)