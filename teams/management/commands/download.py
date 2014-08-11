__author__ = 'bprin'
from django.core.management.base import BaseCommand
from teams.models import User, League, Team
import scrape

import logging
logger = logging.getLogger(__name__)

class Command(BaseCommand):

	def handle(self, *args, **options):
	   scraper = scrape.EspnScraper()
	   scraper.login('gothamcityrogues', 'sincere1')
 	   entrance = scraper.scrape_entrance()
	   user = User.objects.create(email='waprin@gmail.com', password='terrible')
	   logger.debug("create_league(): loading league")
	   league = load_league_from_entrance(entrance_html, user)
	   logger.debug("create_league(): loaded league %s" % league.name)

