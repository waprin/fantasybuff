from decimal import Decimal
from django.core.exceptions import ObjectDoesNotExist
from teams.models import League, Player, ScoreEntry, Team, Scorecard, ScorecardEntry, PlayerScoreStats
from teams.scraper.html_scrapes import get_leagues_from_entrance

import re
from bs4 import BeautifulSoup

__author__ = 'bprin'

import logging
logger = logging.getLogger(__name__)

def __get_player_id_from_playerpage(html):
    try:
        return re.findall(r'playerId=(\d+)', html)[0]
    except IndexError:
        f = open('error_html' , 'w')
        f.write(html)
        raise

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

def get_passing_stats(player_score_stats, stats):
    player_score_stats.pass_yards = int(stats[2])
    player_score_stats.pass_td = int(stats[3])
    (interceptions, fumbles) = stats[4].split('/') if stats[4] != 0 else ('0', '0')
    player_score_stats.interceptions = int(interceptions.strip())
    player_score_stats.fumbles = int(fumbles.strip())
    player_score_stats.default_points = Decimal(stats[5])
    player_score_stats.save()

def get_running_stats(player_score_stats, stats):
    player_score_stats.run_yards = int(stats[3])
    player_score_stats.run_td = int(stats[3])
    player_score_stats.default_points = Decimal(stats[5])
    player_score_stats.save()

def get_receiving_stats(player_score_stats, stats):
    player_score_stats.receptions = int(stats[2])
    player_score_stats.receiving_yards = int(stats[3])
    player_score_stats.receving_td = int(stats[4])
    player_score_stats.save()

def get_special_stats(player_score_stats, stats):
    player_score_stats.blocked_kr = int(stats[2])
    player_score_stats.int_td = int(stats[3])
    player_score_stats.fr_td = int(stats[4])
    player_score_stats.save()

def get_kicking_stats(player_score_stats, stats):
    player_score_stats.pat_made = Decimal(stats[4])
    fg_made = Decimal(stats[2])
    fg_attempted = Decimal(stats[3])
    fg_missed = fg_attempted - fg_made
    player_score_stats.fg_missed = fg_missed
    player_score_stats.save()

def get_fg_distance_stats(player_score_stats, stats):
    player_score_stats.fg_0 = Decimal(stats[2])
    player_score_stats.fg_40 = Decimal(stats[3])
    player_score_stats.fg_50 = Decimal(stats[4])
    player_score_stats.save()

def get_stats_function(headers):
    if headers == ['WK', 'OPP', 'YDS', 'TD', 'I/F', 'PTS']:
        return get_passing_stats
    elif headers == [u'WK', u'OPP', u'ATT', u'YDS', u'TD', u'PTS']:
        return get_running_stats
    elif headers == [u'WK', u'OPP', u'REC', u'YDS', u'TD', u'PTS']:
        return get_receiving_stats
    elif headers == [u'WK', u'OPP', u'BLKKRTD', u'INTTD', u'FRTD', u'PTS']:
        return get_special_stats
    elif headers == [u'WK', u'OPP', u'FGM', u'FGA', u'XPM', u'PTS']:
        return get_kicking_stats
    elif headers == [u'WK', u'OPP', u'1-39', u'40-49', u'50+', u'PTS']:
        return get_fg_distance_stats
    elif headers == [u'WK', u'OPP', u'PA', u'I', u'FR', u'TD', u'PTS']:
        pass
    elif headers == [u'WK', u'OPP', u'PTD', u'KTD', u'SCK', u'PTS']:
        pass
    else:
        raise Exception("unknown headers %s" % str(headers))


def load_scores_from_playersheet(html, player_id, year, overwrite=False):
    pool = BeautifulSoup(html)

    name = __get_player_name_from_playerpage(html)
    #player_id = __get_player_id_from_playerpage(html)
    position = __get_player_position_from_playerpage(html)

    (player, new) = Player.objects.get_or_create(name=name, espn_id=player_id, position=position)

    if not new:
        entries = ScoreEntry.objects.filter(player=player, year=year)
        if len(entries) > 0:
            if not overwrite:
                return
            else:
                entries.delete()

    stats_tables = pool.find_all(id=re.compile('moreStatsView.*'))
    for stats_table in stats_tables:
        headers = [tr.string.strip()  for tr in stats_table.find_all('tr')[0].find_all('td')]
        stats_function = get_stats_function(headers)
        for i, row in enumerate(stats_table.find_all('tr')[1:]):
            week = i + 1
            sc = ScoreEntry.objects.get_or_create(week=week, year=year, player=player)[0]
            stats = [td.string for td in row]
            stats = map(lambda stat: 0 if stat == '-' else stat, stats)
            pss = PlayerScoreStats.objects.get_or_create(score_entry=sc)[0]
            if stats_function:
                stats_function(pss, stats)
            if not pss.default_points:
                pss.default_points = Decimal(stats[5])
                pss.save()


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
        team, created = Team.objects.get_or_create(team_name=team_name.strip(), espn_id = info.group(1), owner_name=owner_name, league=league)
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
        logger.debug("loading score entry for player %s" % str(player_id))
        try:
            player = Player.objects.get(espn_id=player_id[1])
        except Player.DoesNotExist:
            logger.error("could not find player id %s" % str(player_id))
            raise
        try:
            points = ScoreEntry.objects.get(player=player, week=week).player_score_stats.default_points
        except ScoreEntry.DoesNotExist:
            logger.error("could not find scoreentry for player id %s" % str(player_id))
            raise

        slot = player_id[0]
        if slot != 'Bench':
            total_points = total_points + points
        ScorecardEntry.objects.create(scorecard=scorecard, player=player, slot=slot, points=points)
    scorecard.points = total_points
    scorecard.save()


def load_scores_from_game(league, week, html):
    logger.debug('load scores(): begin ... ')
    pool = BeautifulSoup(html)

    team_id_blocks = pool.find(id='teamInfos').find_all('a', href=re.compile(r'.*teamId.*'))
    team_ids = []
    for block in team_id_blocks:
        team_id = re.match('.*teamId=(\d*)', block['href']).group(1)
        team_ids.append(team_id)

    second_team_block = pool.find_all('div', {'style' : 'clear: both;'})[1].previous_sibling
    first_team_block = second_team_block.previous_sibling

    team_blocks = [(team_ids[0], first_team_block), (team_ids[1], second_team_block)]

    for team_block in team_blocks:
        team = Team.objects.get(league=league, espn_id=team_block[0])
        scorecard = Scorecard.objects.create(team=team, week=week, actual=True)

        player_rows = team_block[1].find_all('tr', id=re.compile(r'plyr\d*'))
        total_points = Decimal(0)
        for player_row in player_rows:
            slot = player_row.td.string
            player_link = player_row.find('td', 'playertablePlayerName').a
            player_id = player_link['playerid']
            points = player_row.find('td', 'appliedPoints').string
            if points == '--':
                points = '0'
            points = Decimal(points)
            try:
                player = Player.objects.get(espn_id=player_id)
            except Player.DoesNotExist:
                name = player_link.string
                position = player_link.next_sibling.split()[-1]
                player = Player.objects.create(espn_id=player_id, name=name, position=position)
            ScorecardEntry.objects.create(scorecard=scorecard, player=player, slot=slot, points=points)
            if slot != 'Bench':
                total_points += points
        scorecard.points = total_points
        scorecard.save()
