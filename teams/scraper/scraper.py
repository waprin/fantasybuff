from management.commands.create_league import get_num_weeks_from_scoreboard, load_league_from_entrance, \
    load_teams_from_standings

__author__ = 'bill'

import re, time, os
import logging
logger = logging.getLogger(__name__)
import scrape

def get_league_id_from_entrance(html):
    m = re.search(r'leagueId=(\d*)&teamId=(\d*)&seasonId=(\d*)', html)
    return m.group(1)


def choose_league_directory(listings):
    r = re.compile(r'league_(\d+)')
    l = [int(re.search(r, o).group(1)) for o in listings if re.search(r, o)]
    logger.debug("league directory is %s" % str(l))
    if len(l) == 0:
        logger.debug("no leagues matched")
        return None
    l.sort(reverse=True)
    logger.info("choose_directory(): %s" % (str(l)))
    n = str(l[0])
    n = n.zfill(3)
    for listing in listings:
        search = 'league_' + n
        logger.debug('choose_directory(): trying to match on ' + search)
        if re.search(search, listing):
            logger.debug("choose_directory(): found match on %s " % listing)
            return listing
    return None

def create_league_directory(number):
    logger.debug('create_league_directory(): begin .. %d ' % number)
    datestr = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
    logger.debug('create_league_directory(): date str is  ' + datestr)
    numberstr = str(number).zfill(3)
    name = 'league_' + numberstr + '_' + datestr
    leagues_dir = os.path.join(os.getcwd(), 'leagues')
    if not os.path.exists(leagues_dir):
        os.mkdir(leagues_dir)
    league_path = os.path.join(leagues_dir, name)
    logger.debug('create_league_directory(): creating league dir %s ' % league_path)
    if not os.path.isdir(league_path):
        if os.path.exists(league_path):
            raise Exception("league path %s already exists " % league_path)
        os.mkdir(league_path)
    return league_path



class LeagueScraper(object):

    def __init__(self):
        logger.debug("FiledCachedBrowser(): __init__ begin")
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

    def create_cached_league(self, username, password):
        self.username = username
        self.password = password

        entrance_html = self.scrape_entrance()
        logger.debug('create_cached_league() scraped entrance')


        logger.debug('create_cached_league(): loaded league %s' % self.league.name)
        standings_html = self.scrape_standings(self.league)

        logger.debug('create_cached_league(): loaded team from standings')

        first_scoreboard_html = self.scrape_scoreboard(self.league, 1)
        self.num_weeks = get_num_weeks_from_scoreboard(first_scoreboard_html)
        logger.debug('create_cached_league(): num weeks is %d' % self.num_weeks)

#        for i in range(1, self.num_weeks+1):
#            load_games_from_scoreboard(first_scoreboard_html, self.league, i)


    def create_league(self, username, password):
        self.browser = scrape.get_scraper(False)
        logger.debug("create_league(): created browser")
        self.browser.login(username, password)
        logger.debug("create_league(): sucessfully logged in")
        filepath = os.path.join(self.d, 'entrance.html')
        logger.debug("create_league(): entrance filepath is " + filepath)
        f = open(filepath, 'w')
        entrance_html = self.browser.scrape_entrance()
        logger.debug("create_league(): writing entrance")
        f.write(entrance_html)

        logger.debug("create_league(): loading league")
        league = get_league_id_from_entrance(entrance_html)
        logger.debug("create_league(): loaded league %s" % league.name)
        filepath = os.path.join(self.d, 'standings.html')
        f = open(filepath, 'w')
        standings_html = self.browser.scrape_standings()
        f.write(standings_html)

        logger.debug("create_league(): loading teams from standings")

        first_scoreboard_html = self.browser.scrape_scoreboard(league, 1)
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
            html = self.browser.scrape_scoreboard(league, week=i)
            logger.debug('html for week scraped')
            f = open(filepath, 'w')
            f.write(html)

    def create_game(self, game):
        self.browser = scrape.get_scraper(False)
        logger.debug("create_game(): created browser")
        self.browser.login(self.username, self.password)
        logger.debug("create_game(): logged in successfully")

        filepath = os.path.join(self.d, 'week_%d' % game.week, 'game_%s.html' % game.first_scorecard.team.espn_id)
        f = open(filepath, 'w')

        game_html = self.browser.scrape_game(game)
        logger.debug("create_game(): scaped game")
        f.write(game_html)


