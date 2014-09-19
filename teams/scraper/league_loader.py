from decimal import Decimal
from teams.models import League, Player, ScoreEntry, Team, Scorecard, ScorecardEntry
from teams.scraper.html_scrapes import get_leagues_from_entrance

import re
from bs4 import BeautifulSoup

__author__ = 'bprin'

import logging
logger = logging.getLogger(__name__)

def __get_player_id_from_playerpage(html):
     return re.findall(r'playerId=(\d+)', html)[0]

def __get_player_name_from_playerpage(html):
    pool = BeautifulSoup(html)
    return pool.find_all('div','player-name')[0].string

def __get_player_position_from_playerpage(html):
    pool = BeautifulSoup(html)
    return pool.find('span', {"title" : "Position Eligibility"}).contents[1].strip()


def load_leagues_from_entrance(html, espn_user):
    league_tuples = get_leagues_from_entrance(html)
    leagues = []
    for league_tuple in league_tuples:
        try:
            league = League.objects.get(espn_id=league_tuple[1], year=league_tuple[2])
        except League.DoesNotExist:
            league = League.objects.create(espn_id=league_tuple[1], year=league_tuple[2], name=league_tuple[0], loaded=False)

        league.users.add(espn_user)
        league.save()
        leagues.append(league)
    return leagues

def load_scores_from_playersheet(html, league, overwrite=False):
    pool = BeautifulSoup(html)

    name = __get_player_name_from_playerpage(html)
    player_id = __get_player_id_from_playerpage(html)
    position = __get_player_position_from_playerpage(html)

    (player, new) = Player.objects.get_or_create(name=name, espn_id=player_id, position=position)

    if not new:
        entries = ScoreEntry.objects.filter(player=player, league=league)
        if len(entries) > 0:
            if not overwrite:
                return
            else:
                entries.delete()

    logger.debug("updating scores for player %s: %s" % (player.name, player.espn_id))
    rows = pool.find_all('table')[2].find_all('tr')[1:]
    scores = [row.find_all('td')[-1].string for row in rows]
    scores = map(lambda x : 0 if x == '-' else float(x), scores)

    for week, score in enumerate(scores):
        sc = ScoreEntry(week=week+1, player=player, points=float(score), league=league)
        sc.save()

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
        team, created = Team.objects.get_or_create(team_name=team_name.strip(), espn_id = info.group(1), owner_name=owner_name, league=league, league_espn_id=league.espn_id)
        if not created:
            logger.warn("created duplicate team %s %s" % (league.espn_id, team.espn_id))



def __get_players_from_lineup(html):
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

def load_week_from_lineup(html, week, team):
    scorecard, created = Scorecard.objects.get_or_create(team=team, week=week, actual=True)
    if not created:
            logger.warn("created lineup %s %s %s %d" % (team.league.espn_id, team.league.year, team.espn_id, week))
    players = __get_players_from_lineup(html)
    total_points = Decimal(0)
    for player_id in players:
        try:
            player = Player.objects.get(espn_id=player_id[1])
        except Player.DoesNotExist:
            logger.error("could not find player id %s" % str(player_id))
            raise
        try:
            points = ScoreEntry.objects.get(player=player, week=week).points
        except ScoreEntry.DoesNotExist:
            logger.error("could not find scoreentry for player id %s" % str(player_id))
            raise

        slot = player_id[0]
        if slot != 'Bench':
            total_points = total_points + points
        ScorecardEntry.objects.create(scorecard=scorecard, player=player, slot=slot, points=points)
    scorecard.points = total_points
    scorecard.save()