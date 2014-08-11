from django.utils import unittest
from teams.management.commands.create_league import *
from teams.models import User, League, Team

import time
import os
from django.db import connection
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

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



class FileCachedBrowser(object):

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
        user = User.objects.create(email='waprin@gmail.com', password='terrible')

        logger.debug('create_cached_league(): loading league')
        self.league = load_league_from_entrance(entrance_html, user)

        logger.debug('create_cached_league(): loaded league %s' % self.league.name)
        standings_html = self.scrape_standings(self.league)

        load_teams_from_standings(standings_html, self.league)
        logger.debug('create_cached_league(): loaded team from standings')

        first_scoreboard_html = self.scrape_scoreboard(self.league, 1)
        self.num_weeks = get_num_weeks_from_scoreboard(first_scoreboard_html)
        logger.debug('create_cached_league(): num weeks is %d' % self.num_weeks)

        for i in range(1, self.num_weeks+1):
            load_games_from_scoreboard(first_scoreboard_html, self.league, i)

    def create_league(self, username, password):
        self.browser = EspnScraper()
        logger.debug("create_league(): created browser")
        self.browser.login(username, password)
        logger.debug("create_league(): sucessfully logged in")
        filepath = os.path.join(self.d, 'entrance.html')
        logger.debug("create_league(): entrance filepath is " + filepath)
        f = open(filepath, 'w')
        entrance_html = self.browser.scrape_entrance()
        logger.debug("create_league(): writing entrance")
        f.write(entrance_html)
        user = User.objects.create(email='waprin@gmail.com', password='terrible')
        logger.debug("create_league(): loading league")
        league = load_league_from_entrance(entrance_html, user)
        logger.debug("create_league(): loaded league %s" % league.name)
        filepath = os.path.join(self.d, 'standings.html')
        f = open(filepath, 'w')
        standings_html = self.browser.scrape_standings(league)
        f.write(standings_html)
        logger.debug("create_league(): loading teams from standings")
        load_teams_from_standings(standings_html, league)
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
        self.browser = EspnScraper()
        logger.debug("create_game(): created browser")
        self.browser.login(self.username, self.password)
        logger.debug("create_game(): logged in successfully")

        filepath = os.path.join(self.d, 'week_%d' % game.week, 'game_%s.html' % game.first_scorecard.team.espn_id)
        f = open(filepath, 'w')

        game_html = self.browser.scrape_game(game)
        logger.debug("create_game(): scaped game")
        f.write(game_html)

    def scrape_game(self, username, password, game):
        if not self.initialized:
            raise Exception('cache not initalized for game')
        f = open(os.path.join(self.d, 'week_%d' % game.week, 'game_%s.html' % game.first_scorecard.team.espn_id), 'r')
        return f.read()

    def scrape_scoreboard(self, league, week):
        if not self.initialized:
            raise Exception('cache not initialized for scoreboard')
        f = open(os.path.join(self.d, 'week_%d' % week, 'scoreboard.html'), 'r')
        return f.read()

    def scrape_page(self, page):
        if not self.initialized:
            raise Exception('cache not initialialized for page ' + page)
        f = open(os.path.join(self.d, page), 'r')
        return f.read()

    def scrape_entrance(self):
        return self.scrape_page('entrance.html')

    def scrape_standings(self, league):
        return self.scrape_page('standings.html')

    def scrape_game(self, leagues):

        pass


def clear_test_database(fn):
    def wrapper(self):
        logger.info("clearing: conncetion queries is %s" % str(connection.queries))
        for user in User.objects.all():
            logger.info("user is %s" % user.email)
            user.delete()
        for league in League.objects.all():
            league.delete()
        for game in Game.objects.all():
            game.delete()
        fn(self)
    return wrapper

def hits_live_site(fn):
    def wrapper(self):
        if settings.LIVE_SCRAPE:
            fn(self)
        else:
            logger.info("skipping live scrape " + fn.__name__)
    return wrapper

class ScrapeTest(unittest.TestCase):
    @hits_live_site
    def test_create_league(self):
        browser = FileCachedBrowser()
        browser.reload()
        browser.create_league('gothamcityrogues', 'sincere1')

    def test_new_loads_weeks(self):
        d = choose_league_directory(os.listdir(os.path.join(os.getcwd(), 'leagues')))
        logger.info('test_get_num_weeks')
        f = open(os.path.join('leagues', d, 'week_1', 'scoreboard.html'))
        html = f.read()
        num_weeks = get_num_weeks_from_scoreboard(html)
        self.assertEqual(num_weeks, 13)

    #@hits_live_site
    def test_loads_game(self):
        browser = FileCachedBrowser()
        browser.create_cached_league('gothamcityrogues', 'sincere1')
        games = Game.objects.all()

        for game in games:
            browser.create_game(game)

        self.assertTrue(any(game.first_scorecard.team.espn_id=='6' and game.second_scorecard.team.espn_id=='1' for game in games))
        self.assertFalse(any(game.first_scorecard.team.espn_id=='6' and game.second_scorecard.team.espn_id=='2' for game in games))

        logger.info("test_loads_game(): displaying games %d " % len(games))

class UtilsTest(unittest.TestCase):
    def test_choose_league_directory(self):
        logger.info('test_choose_directory(): begin() ... ')
        league1 = 'league_000_2012_12'
        league2 = 'league_001_2012_11'

        listings = ['something', '..', '.', league1, league2 ]
        d = choose_league_directory(listings)
        self.assertEquals(d, league2)

        d = choose_league_directory([])
        self.assertEqual(d, None)

        l1 = 'league_000_2012_12_24_00_57_16'
        #l2 = 'league_001_2012_12_24_00_57_16'
        l3 = 'league_000_2012_12_24_00_58_05'
        l4 = 'league_001_2012_12_24_00_58_05'
        l5 = 'league_000_2012_12_24_00_58_53'
        #l6 = 'league_001_2012_12_24_00_58_53'
        listings = [l1, l3, l4, l5]
        d = choose_league_directory(listings)
        self.assertEquals(d, l4)

class TeamsTest(unittest.TestCase):

    def test_init_user(self):
        logger.info('test_init_users')
        init_user()
        u = User.objects.get(email='waprin@gmail.com')
        self.assertEqual(u.password, 'terrible')

    @clear_test_database
    def test_parse_standings(self):
        """
        Tests that our sample standings page is parsed correctly
        """
        logger.info('test_parse_standings')
        f = open('local_scrapes/standings.html', 'r')
        html = f.read()
        league = League.objects.create(name="test league", espn_id='12345', year=2012)
        load_teams_from_standings(html, league)
        teams = Team.objects.all()

        logger.info(teams)
        self.assertEqual(len(teams), 10)
        self.assertTrue(any(team.team_name == 'Gotham City Rogues' and team.espn_id == '6' and team.owner_name == 'bill prin' for team in teams))

    @clear_test_database
    def test_get_num_weeks(self):
        logger.info('test_get_num_weeks')
        f = open('local_scrapes/realboard.html')
        html = f.read()
        num_weeks = get_num_weeks_from_scoreboard(html)
        self.assertEqual(num_weeks, 13)

    @clear_test_database
    def test_load_games_from_scoreboard(self):
        logger.info('test_load_games_from_scoreboard(): begin')
        f = open('local_scrapes/realboard.html')
        html = f.read()
        league = League.objects.create(name='test league 2', espn_id='54321', year=2012)
        standings_html = open('local_scrapes/standings.html').read()
        load_teams_from_standings(standings_html, league)
        load_games_from_scoreboard(html, league, 1)
        games = Game.objects.all()
        self.assertEqual(len(games), 5)
        self.assertTrue(any(game.first_scorecard.team.espn_id=='6' and game.second_scorecard.team.espn_id=='1' for game in games))
        self.assertFalse(any(game.first_scorecard.team.espn_id=='6' and game.second_scorecard.team.espn_id=='2' for game in games))

    @clear_test_database
    def test_parse_entrance(self):
        logger.info('test_parse_entrance')
        f = open('local_scrapes/entrance.html', 'r')
        html = f.read()
        user = init_user()
        load_league_from_entrance(html, user)
        league = League.objects.get(name='Inglorious Basterds')
        self.assertEqual(league.name, 'Inglorious Basterds')
        self.assertEqual(league.year, 2012)
        self.assertEqual(league.espn_id, '930248')

    @clear_test_database
    def test_parse_scores(self):
        logger.info('test_parse_scores')
        f = open('local_scrapes/scoreboard.html')
        html = f.read()
        league = League.objects.create(name="test league", espn_id='12345', year=2012)
        rogues_team = Team.objects.create(league=league, espn_id='3', team_name='Gotham City Rogues', owner_name='Bill Prin')
        replacements_team = Team.objects.create(league=league, espn_id='4', team_name='The Replacements')
        first_scorecard = Scorecard.objects.create(team=rogues_team)
        second_scorecard = Scorecard.objects.create(team=replacements_team)
        game = Game.objects.create(league=league, week=1, first_scorecard=first_scorecard, second_scorecard=second_scorecard)
        load_scores(html, game)

        first_score = sum(entry.points for entry in ScorecardEntry.objects.filter(scorecard=first_scorecard).exclude(slot='Bench'))
        self.assertEqual(first_score, 74)
        second_score = sum(entry.points for entry in ScorecardEntry.objects.filter(scorecard=second_scorecard).exclude(slot='Bench'))
        self.assertEqual(second_score, 62)

class TestSaveGame(unittest.TestCase):
    @clear_test_database
    @hits_live_site
    def test_save_game(self):
        user = init_user()

        logger.info('handling command')
        f = open('local_scrapes/realboard.html', 'r')
        html = f.read()
        league, created = League.objects.get_or_create(name='test league 2', espn_id=54321, year=2012)
        standings_html = open('local_scrapes/standings.html')
        load_teams_from_standings(standings_html, league)
        load_games_from_scoreboard(html, league, 1)

        games = Game.objects.all()
        logger.info("handle(): %d games loaded" % (len(games)))

        browser = EspnScraper()
        browser.login(user.email, user.password)

        logger.info("handles(): successfully logged in")
        browser.save_week(games[0])

        #html = browser.scrape_entrance()
        #league = load_league_from_entrance(html)

        #  load_team_from_standings(html, league)
        #  html = browser.scrape_week(league, 1ma)


