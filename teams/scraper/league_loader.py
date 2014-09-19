from teams.models import League, Player, ScoreEntry
from teams.scraper.html_scrapes import get_leagues_from_entrance

import re
from bs4 import BeautifulSoup

__author__ = 'bprin'

import logging
logger = logging.getLogger(__name__)

def get_player_id_from_playerpage(html):
     return re.findall(r'playerId=(\d+)', html)[0]

def get_player_name_from_playerpage(html):
    pool = BeautifulSoup(html)
    return pool.find_all('div','player-name')[0].string

def get_player_position_from_playerpage(html):
    pool = BeautifulSoup(html)
    return pool.find('span', {"title" : "Position Eligibility"}).contents[1].strip()


def load_leagues_from_entrance(html, espn_user):
    league_tuples = get_leagues_from_entrance(html)
    leagues = []
    for league_tuple in league_tuples:
        try:
            league = League.objects.get(espn_id=league_tuple[1], year=league_tuple[2])
        except League.DoesNotExist:
            league = League.objects.create(espn_id=league_tuple[1], year=league_tuple[2], name=league_tuple[0])

        league.users.add(espn_user)
        league.save()
        leagues.append(league)
    return leagues

def load_scores_from_playersheet(html, league):
    pool = BeautifulSoup(html)

    name = get_player_name_from_playerpage(html)
    player_id = get_player_id_from_playerpage(html)
    position = get_player_position_from_playerpage(html)

    (player, new) = Player.objects.get_or_create(name=name, espn_id=player_id, position=position)

    if new:
        logger.debug("added new player %s: %s" % (player.name, player.espn_id))
        rows = pool.find_all('table')[2].find_all('tr')[1:]
        scores = [row.find_all('td')[-1].string for row in rows]
        scores = map(lambda x : 0 if x == '-' else float(x), scores)

        for week, score in enumerate(scores):
            sc = ScoreEntry(week=week+1, player=player, points=float(score), league=league)
            sc.save()
