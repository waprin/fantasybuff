__author__ = 'bill'

import re, os
from bs4 import BeautifulSoup
import logging
import re
logger = logging.getLogger(__name__)
from teams.management.commands import scrape
from teams.utils.league_files import choose_league_directory, create_league_directory

def get_num_weeks_from_scoreboard(html):
    pool = BeautifulSoup(html)
    body_copy = pool.find('div', 'bodyCopy')
    matchups = body_copy.find_all('a', title=re.compile(r'Week'))
    for matchup in matchups:
        m = matchup
    return int(m.string)


def get_league_id_from_entrance(html):
    m = re.search(r'leagueId=(\d*)&teamId=(\d*)&seasonId=(\d*)', html)
    return m.group(1)

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

def get_players_from_roster(html):
    soup = BeautifulSoup(html)
    rows = soup.find('table', 'playerTableTable').find_all('tr')[2:-1]
    players = []
    for row in rows:
        playerId = row.contents[0].a['playerid']
        playerName = row.contents[0].a.string
        players.append((playerId, playerName))
    return players

def get_player_ids_from_lineup(html):
    soup = BeautifulSoup(html)
    player_rows = soup.find_all('td', 'playertablePlayerName')
    ids = []
    for player_row in player_rows:
        ids.append(re.match(r'playername_(\d*)', player_row['id']).group(1))
    return ids


def get_defenses_from_roster(html):
    soup = BeautifulSoup(html)
    return [re.match(r'playername_(\d*)', defense_element["id"]).group(1) for defense_element in soup.find_all('td', 'playertablePlayerName')]


class LeagueScraper(object):

    def __init__(self, username, password):
        logger.debug("FiledCachedBrowser(): __init__ begin")

        self.username = username
        self.password = password

        self.d = choose_league_directory(os.listdir(os.path.join(os.getcwd(), 'leagues')))
        logger.debug("FileCachedBrowser(): __init__ self.d is %s" % self.d)
        if self.d == None:
            self.d = create_league_directory(0)
            self.initialized = False
        else:
            self.initialized = True
        self.d = os.path.join('leagues', self.d)

    def reload(self):
        logger.debug("reloading file cached browser")
        n = int(re.search(r'league_(\d+)', self.d).group(1))
        logger.debug("moving to new directory %d " % n)
        self.d = create_league_directory(n+1)
        self.initialized = False

    def create_league_directory(self):
        if self.initialized:
            raise Exception("trying load already created directory")

        self.browser = scrape.EspnScraper()
        logger.debug("create_league(): created browser")
        self.browser.login(self.username, self.password)
        logger.debug("create_league(): sucessfully logged in")
        filepath = os.path.join(self.d, 'entrance.html')
        logger.debug("create_league(): entrance filepath is " + filepath)
        f = open(filepath, 'w')
        entrance_html = self.browser.scrape_entrance()
        logger.debug("create_league(): writing entrance")
        f.write(entrance_html)

        logger.debug("create_league(): loading league")
        espn_id = get_league_id_from_entrance(entrance_html)

        filepath = os.path.join(self.d, 'standings.html')
        f = open(filepath, 'w')
        standings_html = self.browser.scrape_standings(espn_id)
        f.write(standings_html)

        logger.debug("create_league(): loading teams from standings")

        first_scoreboard_html = self.browser.scrape_scoreboard(espn_id, 1)
        num_weeks = get_num_weeks_from_scoreboard(first_scoreboard_html)
        logger.debug('create_league(): num weeks is %d' % num_weeks)
        week_path = os.path.join(self.d, 'week_1')
        if not os.path.exists(week_path):
            os.mkdir(week_path)
        filepath = os.path.join(week_path, 'scoreboard.html')
        f = open(filepath, 'w')
        f.write(first_scoreboard_html)
        for i in range(2, num_weeks+1):
            week_path = os.path.join(self.d, 'week_%d' % i)
            if not os.path.exists(week_path):
                os.mkdir(week_path)
            filepath = os.path.join(week_path, 'scoreboard.html')
            logger.debug('scraping week %d to path %s' % (i, filepath))
            html = self.browser.scrape_scoreboard(espn_id, week=i)
            logger.debug('html for week scraped')
            f = open(filepath, 'w')
            f.write(html)

    def create_games(self, file_browser, espn_id, week_num):
        self.browser =  scrape.EspnScraper()
        logger.debug("create_games(): created browser")
        self.browser.login(self.username, self.password)
        logger.debug("create_games(): sucessfully logged in")

        scoreboard_html = file_browser.scrape_scoreboard(espn_id, week_num)
        team_ids = get_teams_from_scoreboard(scoreboard_html)

#        print "team ids: "
#        print team_ids
        os.makedirs(os.path.join(self.d, 'week_%d' % week_num, 'games'))
        for team_id in team_ids:
            html = self.browser.scrape_game(espn_id, team_id, week_num)
            print "team id is %s" % team_id
            filepath = os.path.join(self.d, 'week_%d' % week_num, 'games', 'game_%s.html' % team_id)
            logger.debug("writing game html to filepath %s" % filepath)
            f = open(filepath, 'w')
            f.write(html)

    def create_trans_logs(self, file_browser, espn_id):
        self.browser =  scrape.EspnScraper()
        logger.debug("create_trans_logs(): created browser")
        self.browser.login(self.username, self.password)
        logger.debug("create_trans_logs(): sucessfully logged in")

        scoreboard_html = file_browser.scrape_scoreboard(espn_id, 1)
        team_ids = get_teams_from_scoreboard(scoreboard_html)

        print "team ids: "
        print team_ids
        os.makedirs(os.path.join(self.d, 'translogs'))

        for team_id in team_ids:
            pass
            #self.browser.scrape_translog()

    def create_roster(self, file_browser, espn_id, team_id, year):
        self.browser = scrape.EspnScraper()
        self.browser.login(self.username, self.password)

        html = file_browser.scrape_roster_summary()
        players = get_players_from_roster(html)

        print players

        roster_path = os.path.join(self.d, 'roster_%s' % team_id)
        if not os.path.exists(roster_path):
            os.mkdir(os.path.join(self.d, 'roster_%s' % team_id))
        for player in players:
            html = self.browser.scrape_player(espn_id, player[0], year)
            filepath = os.path.join(self.d, 'roster_%s' % team_id, 'player_%s.html' % player[0])
            logger.debug("writing player html to filepath %s" % filepath)
            f = open(filepath, 'w')
            f.write(html)
            f.close()

    def create_defenses(self, file_browser, espn_id, year):
        self.browser = scrape.EspnScraper()
        self.browser.login(self.username, self.password)

        html = file_browser.scrape_defense()
        players = get_defenses_from_roster(html)

        team_id = "defenses"
        roster_path = os.path.join(self.d, 'roster_%s' % team_id)
        if not os.path.exists(roster_path):
            os.mkdir(os.path.join(self.d, 'roster_%s' % team_id))
        for player in players:
            html = self.browser.scrape_player(espn_id, player, year)
            filepath = os.path.join(self.d, 'roster_%s' % team_id, 'player_%s.html' % player)
            logger.debug("writing player html to filepath %s" % filepath)
            f = open(filepath, 'w')
            f.write(html)
            f.close()

    def create_weeks_for_team(self, file_browser, league_id, team_id, year):
        self.browser = scrape.EspnScraper()
        self.browser.login(self.username, self.password)


        scoreboard_html = file_browser.scrape_scoreboard(league_id, 1)
        num_weeks = get_num_weeks_from_scoreboard(scoreboard_html)
        print "got num weeks %d" % num_weeks

        team_path = os.path.join(self.d, 'team_%s' % team_id)
        if not os.path.exists(team_path):
            os.mkdir(team_path)

        for week in range(1, num_weeks+1):
            html = self.browser.scrape_lineup(league_id, team_id, week, '2013')
            filepath = os.path.join(self.d, 'team_%s' % team_id, 'week_%d.html' % week)
            logger.debug('scrape week %d for team %s writing to %s' % (week, team_id, filepath))
            f = open(filepath, 'w')
            f.write(html)
            f.close()

    def get_players_from_lineup(self, file_browser, espn_id, team_id, week, year):
        self.browser = scrape.EspnScraper()
        self.browser.login(self.username, self.password)

        html = file_browser.scrape_lineup(team_id, week)
        player_ids = get_player_ids_from_lineup(html)
        for player_id in player_ids:
            if file_browser.contains_player(player_id):
                logger.info("skipping over existing player %s" % player_id)
                continue
            logger.info("will now scrape new player %s" % player_id)
            html = self.browser.scrape_player(espn_id, player_id, year)
            filepath = os.path.join(self.d, 'players', 'player_%s.html' % player_id)
            f = open(filepath, 'w')
            f.write(html)
            f.close()

















