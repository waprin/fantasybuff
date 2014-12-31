from django.core.management import BaseCommand

from teams.models import EspnUser, League, Team
from teams.scraper.FileBrowser import FileBrowser
from teams.scraper.SqlStore import SqlStore
from teams.scraper.utils import real_num_weeks


__author__ = 'bprin'

from teams.scraper.html_scrapes import get_teams_from_matchups

import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):

        store = SqlStore()
        filesystem = FileBrowser()

        # # entrance
        for espn_user in EspnUser.objects.all():
            if store.has_entrance(espn_user):
                filesystem.write_entrance(espn_user, store.get_entrance(espn_user))

        for league in League.objects.all():
            ## standings
            if store.has_standings(league):
                filesystem.write_standings(league, store.get_standings(league))

            ## settings
            if store.has_settings(league.espn_id, league.year):
                filesystem.write_settings(league.espn_id, league.year, store.get_settings(league.espn_id, league.year))

            for team in Team.objects.filter(league=league):
                ## translog
                if store.has_translog(league.espn_id, league.year, team.espn_id):
                    filesystem.write_translog(league.espn_id, league.year, team.espn_id,
                                              store.get_translog(league.espn_id, league.year, team.espn_id)
                    )

            ## matchups
            for week in range(0, real_num_weeks() + 1):
                if store.has_matchups(league, week):
                    logger.info("loading week %d" % week)
                    html = store.get_matchups(league, week)
                    filesystem.write_matchups(league, week, html)
                    games = get_teams_from_matchups(html)

                    ## games
                    for game in games:
                        if store.has_game(league, game[0], week):
                            html = store.get_game(league, game[0], week)
                            filesystem.write_game(league, game[0], week, html)







