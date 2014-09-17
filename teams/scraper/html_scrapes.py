import re
from bs4 import BeautifulSoup

import logging
logger = logging.getLogger(__name__)

__author__ = 'bprin'

def get_leagues_from_entrance(html):
    pool = BeautifulSoup(html)
    league_elements = pool.find_all('a', 'leagueoffice-link')
    leagues = []
    for element in league_elements:
        name = element.string
        m = re.search(r'leagueId=(\d*)&teamId=\d*&seasonId=(\d*)', element['href'])
        espn_id = m.group(1)
        year = m.group(2)
        leagues.append((name, espn_id, year))
    logger.debug("get_leagues_from_entrance returning " + str(leagues))
    return leagues

def get_teams_from_standings(html):
    pool = BeautifulSoup(html)
    header = pool.find('div', 'games-pageheader')
    standings = header.findNextSibling('table')
    bodies = standings.find_all('tr', 'tableBody')

    team_tuples = []
    for body in bodies:
        fullname = body.td.a['title']
        href = body.td.a['href']
        info = re.search("teamId=(\d+)", href)
        team_id = info.group(1)
        matched_name = re.search("(.*)\s*\((.*)\)", fullname)
        team_name = matched_name.group(1)
        owner_name = matched_name.group(2)
        team_tuples.append( (team_id, team_name, owner_name) )
    return team_tuples

def get_num_weeks_from_matchups(html):
    pool = BeautifulSoup(html)
    body_copy = pool.find('div', 'bodyCopy')
    matchups = body_copy.find_all('a', title=re.compile(r'Week'))
    for matchup in matchups:
        m = matchup
    return int(m.string)

def get_player_ids_from_lineup(html):
    soup = BeautifulSoup(html)
    player_rows = soup.find_all('td', 'playertablePlayerName')
    ids = []
    for player_row in player_rows:
        ids.append(re.match(r'playername_(\d*)', player_row['id']).group(1))
    return ids

def parse_scores_from_playersheet(html):
    pool = BeautifulSoup(html)
    rows = pool.find_all('table')[2].find_all('tr')[1:]
    return [row.find_all('td')[-1].string for row in rows]


"""
    rows = soup.find('table', 'playerTableTable').find_all('tr')[2:-1]
    players = []
    for row in rows:
        playerId = row.contents[0].a['playerid']
        playerName = row.contents[0].a.string
        players.append((playerId, playerName))

"""

"""
def get_teams_from_scoreboard(html):
    soup = BeautifulSoup(html)
    matchups = soup.find_all('table', 'matchup')

    games = []
    for matchup in matchups:
        teams = matchup.find_all(id=re.compile('teamscrg'))
        logger.debug("teams is " + str(teams))
        first_id_string = teams[0]['id']
        first_id = re.search(r'teamscrg_(\d*)_', first_id_string).group(1)
        games.append(first_id)
    return games
"""