from django.core.management.base import BaseCommand
from django.db import transaction
from teams.scraper.FileBrowser import FileBrowser
from teams.scraper.scraper import LeagueScraper
from teams.models import User, League, Team, Player, ScorecardEntry, Scorecard, Game
from bs4 import BeautifulSoup
from scrape import EspnScraper
import re
import logging

logger = logging.getLogger(__name__)

def init_user():
    user, created = User.objects.get_or_create(email='waprin@gmail.com', defaults={'password': 'terrible'})
    return user

def load_teams_from_standings(html, league):
    pool = BeautifulSoup(html)
    header = pool.find('div', 'games-pageheader')
    standings = header.findNextSibling('table')
    bodies = standings.find_all('tr', 'tableBody')

    for body in bodies:
        fullname = body.td.a['title']
        href = body.td.a['href']
        info = re.search("teamId=(\d+)", href)
        matched_name = re.search("(.*)\s*\((.*)\)", fullname)
        team_name = matched_name.group(1)
        owner_name = matched_name.group(2)
        team = Team(team_name=team_name.strip(), espn_id = info.group(1), owner_name=owner_name, league=league, league_espn_id=league.espn_id)
        team.save()


def load_league_from_entrance(html, user):
    m = re.search(r'leagueId=(\d*)&teamId=(\d*)&seasonId=(\d*)', html)
    league_id= m.group(1)
    team_id = m.group(2)
    season_id = m.group(3)

    pool = BeautifulSoup(html)
    logger.debug('pool successfully initialized')
    league_name = pool.find('a', 'leagueoffice-link').string
    logger.debug('league name found is ' + league_name)

    try:
        league = League.objects.get(espn_id=league_id)
    except League.DoesNotExist:
        league = League(espn_id=league_id, year=2012, name=league_name)
        league.save()
        league.users.add(user)
        league.save()
    return league

#def scrape_teams_from_scoreboard(html)

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


def command_setup_league():
    logger.info("in create_league command")
    browser = FileBrowser()
    html = browser.scrape_entrance()
    user = User.objects.get(email='waprin@gmail.com')
    load_league_from_entrance(html, user)
    logger.info("finishing create_league command")

def command_setup_teams():
    logger.info("in command_setup_teams")
    browser = FileBrowser()
    html = browser.scrape_standings()
    league = League.objects.get(name='Inglorious Basterds')
    load_teams_from_standings(html, league)
    logger.info("finishing command_setup_teams")

def command_setup_games():
    logger.info("in command_setup_games")

    browser = FileBrowser()
    html = browser.scrape_scoreboard(None, 1)

    league = League.objects.get(name='Inglorious Basterds')
    load_games_from_scoreboard(html, league, 1)


class Command(BaseCommand):
    def handle(self, *args, **options):
        #command_setup_league()
        #command_setup_teams()
        #command_setup_games()
        espn = EspnScraper()
        espn.login('gothamcityrogues', 'sincere1')
        html = espn.scrape_player('930248', '2580', '2013')
        f = open('player_2580.html', 'w')
        f.write(html)
        f.close()
        #html = espn.scrape_roster_summary('930248', 6)
        #f = open('rostersummary.html', 'w')
        #f.write(html)
        #f.close()

"""
        html = espn.scrape_translog('930248', 6)
        f = open('translog.html', 'w')
        f.write(html)
        f.close()
"""


"""
        lc = LeagueScraper('gothamcityrogues', 'sincere1')
        lc.reload()
        lc.create_league_directory()
        lc.create_games(FileBrowser(), "930248", 1)
"""





