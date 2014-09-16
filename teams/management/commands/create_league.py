from decimal import Decimal
from django.core.management.base import BaseCommand
from django.db import transaction
from teams.management.commands.parse_player import parse_scores_from_playersheet
from teams.metrics.lineup_calculator import calculate_optimal_lineup, get_lineup_score
from teams.scraper.FileBrowser import FileBrowser
from teams.scraper.scraper import LeagueScraper
from scrape import EspnScraper
from teams.models import User, League, Team, Player, ScorecardEntry, Scorecard, Game, ScoreEntry, TransLogEntry, DraftClaim
from bs4 import BeautifulSoup
import re
import logging
import datetime

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

def load_players_from_playerpage(html):
    pool = BeautifulSoup(html)
    rows = pool.find_all('table')[2].find_all('tr')[1:]
    return [row.find_all('td')[-1].string for row in rows]

def get_player_id_from_playerpage(html):
     return re.findall(r'playerId=(\d+)', html)[0]

def get_player_name_from_playerpage(html):
    pool = BeautifulSoup(html)
    return pool.find_all('div','player-name')[0].string

def get_player_position_from_playerpage(html):
    pool = BeautifulSoup(html)
    return pool.find('span', {"title" : "Position Eligibility"}).contents[1].strip()

def get_players_from_lineup(html):
    pool = BeautifulSoup(html)
    rows = pool.find_all('tr', 'pncPlayerRow')
    players = []
    for row in rows:
        slot = row.contents[0].string
        player_id = None
        if not row.contents[1].a:
            continue
        player_id = row.contents[1].a['playerid']
        players.append((slot, player_id))
    return players


def load_scores_from_playersheet(html, league, espn_id):
    pool = BeautifulSoup(html)

    name = get_player_name_from_playerpage(html)
    #espn_id = get_player_id_from_playerpage(html)
    position = get_player_position_from_playerpage(html)

    (player, new) = Player.objects.get_or_create(name=name, espn_id=espn_id, position=position)

    if new:
        rows = pool.find_all('table')[2].find_all('tr')[1:]
        scores = [row.find_all('td')[-1].string for row in rows]
        scores = map(lambda x : 0 if x == '-' else float(x), scores)

        for week, score in enumerate(scores):
            sc = ScoreEntry(week=week+1, player=player, points=float(score), league=league)
            sc.save()


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

        print "looking for player name " + player_name
        player = Player.objects.get(name='LeSean McCoy')
        print player_name == 'LeSean McCoy'
        player = Player.objects.get(name=str(player_name))
        print player.position

        print Player.objects.all()

        player = Player.objects.get(name=str(player_name))
        team = Team.objects.get(espn_id='6')

        if transaction_type == 'Draft':
            draft_entry = DraftClaim(date=date,round=draft_round, player_added=player, player=team)
            draft_round = draft_round + 1
            draft_entry.save()

def load_week_from_lineup(html, week, team):
    scorecard = Scorecard.objects.create(team=team, week=week, actual=True)
    players = get_players_from_lineup(html)
    print players
    total_points = Decimal(0)
    for player_id in players:
        player = Player.objects.get(espn_id=player_id[1])
        points = ScoreEntry.objects.get(player=player, week=week).points
        slot = player_id[0]
        if slot != 'Bench':
            total_points = total_points + points
        ScorecardEntry.objects.create(scorecard=scorecard, player=player, slot=slot, points=points)
    scorecard.points = total_points
    scorecard.save()


def command_setup_user():
    user = User.objects.create(email='waprin@gmail.com', password='sincere1')



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

def command_setup_players():

    browser = FileBrowser()
    htmls = browser.scrape_all_players()
    league = League.objects.get(name='Inglorious Basterds')
    for html in htmls:
        load_scores_from_playersheet(html[1], league, html[0])

def command_setup_defenses():

    browser = FileBrowser()
    defenses = browser.scrape_all_players('defenses')
    #htmls.append(defense_htmls)
    league = League.objects.get(name='Inglorious Basterds')
    for defense in defenses:
        load_scores_from_playersheet(defense[1], league, defense[0])

def command_setup_lineup():
    browser = FileBrowser()
    #lineup = browser.scrape_lineup()
    team = Team.objects.get(espn_id='6')
    for week in range(1, 12):
        html = browser.scrape_lineup('6', week)
        load_week_from_lineup(html, week, team)
    #load_week_from_lineup(lineup, 1, team)

def command_setup_optimal_lineups():
    rogues = Team.objects.get(espn_id='6')
    weeks = [entry.week for entry in Scorecard.objects.filter(team=rogues)]
    for week in weeks:
        scorecard = Scorecard.objects.get(team=rogues, week=week)
        scorecard_entries = ScorecardEntry.objects.filter(scorecard=scorecard)
        optimal_entries = calculate_optimal_lineup(scorecard_entries)
        total_points = get_lineup_score(optimal_entries)
        optimal_scorecard = Scorecard.objects.create(team=rogues, week=week, actual=False, points=total_points)
        for entry in optimal_entries:
            entry.scorecard = optimal_scorecard
            entry.save()

def command_find_average_deltas():
    league = League.objects.get(espn_id='930248')
    teams = Team.objects.filter(league=league)
    for team in teams:
        actual_weeks = list(Scorecard.objects.filter(team=team, actual=True))
        optimal_weeks = list(Scorecard.objects.filter(team=team, actual=False))
        actual_weeks.sort(key=lambda x: x.week)
        optimal_weeks.sort(key=lambda x: x.week)

        deltas = []
        for i, week in enumerate(actual_weeks):
            optimal_points = optimal_weeks[i].points
            delta = optimal_points - week.points
            deltas.append(delta)
        average_delta = sum(deltas) / Decimal(len(deltas))
        team.average_delta = average_delta
        team.save()



class Command(BaseCommand):
    def handle(self, *args, **options):
        file_browser = FileBrowser()
#        command_setup_lineup()
#        scraper = EspnScraper()
#        scraper.login('gothamcityrogues', 'sincere1')
        """
        lc = LeagueScraper('gothamcityrogues', 'sincere1')
        for week in range(2, 14):
            lc.get_players_from_lineup(file_browser, '930248', '6', week, '2013')
#        lc.create_defenses(FileBrowser(), '930248', '2013'
"""
        """
        scraper = EspnScraper()
        scraper.login('gothamcityrogues', 'sincere1')
        html = scraper.scrape_lineup('930248', '6', 1, '2013')
        f = open('lineup.html', 'w')
        f.write(html)
        f.close()
        """

#        lc = LeagueScraper('gothamcityrogues', 'sincere1')
#        lc.create_roster(FileBrowser(), '930248', '6', '2013')


        #
        # command_setup_defenses()

        command_setup_user()
        command_setup_league()
        command_setup_teams()
#        command_setup_games()
        command_setup_players()
        command_setup_lineup()
        command_setup_optimal_lineups()
        command_find_average_deltas()

        #lc = LeagueScraper('gothamcityrogues', 'sincere1')
        #lc.create_weeks_for_team(FileBrowser(), '930248', '6', '2013')

"""
        espn = EspnScraper()
        espn.login('gothamcityrogues', 'sincere1')
        html = espn.scrape_defenses('930248', '2013')
        f = open('defense.html', 'w')
        f.write(html)
        f.close()
"""
"""
        html = espn.scrape_player('930248', '2580', '2013')
        f = open('player_2580.html', 'w')
        f.write(html)
        f.close()
"""
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





