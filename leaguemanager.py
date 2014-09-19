from teams.models import *
from teams.scraper.scraper import *
from teams.scraper.FileBrowser import *
from teams.scraper.SqlStore import *

league_scraper = LeagueScraper(FileBrowser(), SqlStore())
