from django.core.management.base import BaseCommand
from django.db import transaction
from teams.management.commands.scrape import EspnScraper
from teams.models import User, League, Team, Player, ScorecardEntry, Scorecard, Game
from bs4 import BeautifulSoup
import re
import logging

logger = logging.getLogger(__name__)

def init_user():
    try:
        user = User.objects.get(email='waprin@gmail.com')
    except User.DoesNotExist:
        user = User.objects.create(email='waprin@gmail.com', password='terrible')
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
        team = Team(team_name=team_name.strip(), espn_id = info.group(1), owner_name=owner_name, league=league)
        team.save()

def get_num_weeks_from_scoreboard(html):
    pool = BeautifulSoup(html)
    body_copy = pool.find('div', 'bodyCopy')
    matchups = body_copy.find_all('a')
    for matchup in matchups:
        m = matchup
    return int(m.string)

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
    logger.debug('found ' + str(len(team_tables)) + ' teams')
    for team_table in team_tables:
        # TODO find by team ID, not team name
        team_name = team_table[:team_table.find('Box')].strip()
        logger.debug('team name is ' + team_name + '.')
        team = Team.objects.get(team_name=team_name)

        if team == game.first_scorecard.team:
            logger.debug('team matched first scorecard')
            scorecard = game.first_scorecard
        elif team == game.second_scorecard.team:
            logger.debug('team matched second scorecard')
            scorecard = game.second_scorecard
        else:
            logger.error('team matched neither scorecard')
            assert False

        logger.debug("team_name is " + team_name)
        player_table = team_table.findParent('div')
        player_rows = player_table.find_all('td', 'playertablePlayerName')
        for player_row in player_rows:
            slot = player_row.previous_sibling.string
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

def save_week(html, browser, league, week):
    num_weeks = get_num_weeks_from_scoreboard(html)
    for week_num in range(1, num_weeks+1):
        week_html = browser.scrape_week(league, week_num)

class Command(BaseCommand):

    def handle(self, *args, **options):
        user = init_user()
        browser = EspnScraper()
        browser.login(user.team_name, user.password)
        html = browser.scrape_entrance()
        league = load_league_from_entrance(html)
        html = browser.scrape_standings()
      #  load_team_from_standings(html, league)
       #  html = browser.scrape_week(league, 1)



