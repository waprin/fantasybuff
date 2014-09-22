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

def load_players_from_playerpage(html):
    pool = BeautifulSoup(html)
    rows = pool.find_all('table')[2].find_all('tr')[1:]
    return [row.find_all('td')[-1].string for row in rows]

@transaction.commit_on_success
def load_games_from_scoreboard(html, league, week):
    logger.debug('load_games_from_scoreboard')
    soup = BeautifulSoup(html)
    matchups = soup.find_all('table', 'matchup')

    games = []
    for matchup in matchups:
        teams = matchup.find_all(id=re.compile('teamscrg'))
        logger.debug("teams is " + str(teams))
        first_id_string = teams[0]['id']
        second_id_string = teams[1]['id']

        logger.debug('matching on team id strings ' + first_id_string)
        first_id = re.search(r'teamscrg_(\d*)_', first_id_string).group(1)
        second_id = re.search(r'teamscrg_(\d*)_', second_id_string).group(1)

        logger.debug('looking up first team with id ' + first_id + '.')
        first_team = Team.objects.get(espn_id=first_id)
        logger.debug('looking up second team with id ' + second_id + '.')
        second_team = Team.objects.get(espn_id=second_id)

        logger.debug('creating scorecards')
        first_scorecard = Scorecard.objects.create(team=first_team)
        second_scorecard = Scorecard.objects.create(team=second_team)
        game = Game.objects.create(league=league, week=week, first_scorecard=first_scorecard, second_scorecard=second_scorecard)

        games.append(game)

    return games



def load_scores(html, game):
    logger.debug('load scores(): begin ... ')
    pool = BeautifulSoup(html)
    team_tables = pool.find_all(text=re.compile(r'(?<!Full)(?<!Quick) Box Score.*'))
    team_tables = filter(lambda t : not 'at' in t, team_tables)
    #
    # logger.debug('found ' + str(len(team_tables)) + ' teams')
    #pool.find(id='teamInfos')
    for team_table in team_tables:
        # TODO find by team ID, not team name
        this_team_name = team_table[:team_table.rfind('Box')]
        this_team_name = this_team_name.strip()

        team = Team.objects.get(team_name=this_team_name)


        if team == game.first_scorecard.team:
            logger.debug('team matched first scorecard')
            scorecard = game.first_scorecard
        elif team == game.second_scorecard.team:
            logger.debug('team matched second scorecard')
            scorecard = game.second_scorecard
        else:
            logger.error('team matched neither scorecard')
            assert False

        player_table = team_table.findParent('div')
        player_rows = player_table.find_all('td', 'playertablePlayerName')
        #player_rows = player_table.find_all('td', 'pncPlayerRow')
        logger.debug(player_rows)
        for player_row in player_rows:
            logger.debug("slot is %s" % player_row.previous_sibling)
            slot = player_row.previous_sibling.string

    #        slot = player_row.string.split()[-1]
            logger.debug("slot cell is " + slot)

            strings = player_row.strings
            player_name = strings.next()
            position = strings.next().split()[-1]
            logger.debug('loading player ' + player_name + ' at position ' + position)
            try:
                player = Player.objects.get(name=str(player_name))
            except Player.DoesNotExist:
                logger.debug('player did not exist, creating')
                player = Player.objects.create(name=str(player_name), position=position)
            logger.debug('created player ' + str(player))

            points = player_row.findNext('td', 'appliedPoints').string
            if points == '--':
                points = 0
            else:
                points = str(points)
            ScorecardEntry.objects.create(scorecard=scorecard, player=player, slot=slot, points=points)

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

        player = Player.objects.get(name='LeSean McCoy')
        player = Player.objects.get(name=str(player_name))

        player = Player.objects.get(name=str(player_name))
        team = Team.objects.get(espn_id='6')

        if transaction_type == 'Draft':
            draft_entry = DraftClaim(date=date,round=draft_round, player_added=player, player=team)
            draft_round = draft_round + 1
            draft_entry.save()


def command_setup_optimal_lineups():
    rogues = Team.objects.get(espn_id='6')


def command_find_average_deltas():
    league = League.objects.get(espn_id='930248')
    teams = Team.objects.filter(league=league)


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
        html = scraper.get_season_totals(0)
        file_browser = FileBrowser()
        file_browser.put_season_totals(0, html)

"""
        email = args[0]
        store = SqlStore()
        user = User.objects.get(username=email)
        espn_users = EspnUser.objects.filter(user=user)
        for espn_user in espn_users:
            scraper = get_scraper(espn_user)
            league_scraper = LeagueScraper(scraper, store)
            league_scraper.scrape_leagues(espn_user)
"""

