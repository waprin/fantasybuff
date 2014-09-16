from teams.utils.league_files import choose_league_directory, create_league_directory
import os, errno, re

import logging
logger = logging.getLogger(__name__)

__author__ = 'bill'

def listdir_nohidden(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

class FileBrowser(object):

    def __init__(self):
        self.d = choose_league_directory(os.listdir(os.path.join(os.getcwd(), 'leagues')))

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

    def has_entrance(self, user):
        return os.path.exists(os.path.join(self.d, 'entrance_%d.html' % user.id))

    def get_entrance(self, user):
        return open(os.path.join(self.d, 'entrance_%d.html' % user.id)).read()

    def write_entrance(self, user, html):
        filepath = os.path.join(self.d, 'entrance_%d.html' % user.id)
        logger.debug("create_league(): entrance filepath is " + filepath)
        f = open(filepath, 'w')
        logger.debug("create_league(): writing entrance")
        f.write(html)

    def create_instance_directory(self, espn_id, year):
        instance_path = os.path.join(self.d, 'league_%s_%s' % (espn_id, year))
        if not os.path.exists(instance_path):
            os.mkdir(instance_path)
        return instance_path

    def standings_path(self, league):
        instance_dir = self.create_instance_directory(league.espn_id, league.year)
        return os.path.join(instance_dir, 'standings.html')

    def has_standings(self, league):
        return os.path.exists(self.standings_path(league))

    def get_standings(self, league):
        return open(self.standings_path(league)).read()

    def write_standings(self, league, html):
        with open(self.matchup_path(league), 'w') as f:
            f.write(html)

    def matchup_path(self, league, week):
        instance_dir = self.create_instance_directory(league.espn_id, league.year)
        return os.path.join(instance_dir, 'matchups_%d.html' % week)

    def has_matchups(self, league, week):
        return os.path.exists(self.matchup_path(league, week))

    def get_matchups(self, league, week):
        return open(self.matchup_path(league, week)).read()

    def write_matchups(self, league, week, html):
        with open(self.matchup_path(league, week), 'w') as f:
            f.write(html)

    def roster_path(self, league, team_id, week):
        instance_dir = self.create_instance_directory(league.espn_id, league.year)
        dirpath = os.path.join(instance_dir, "team_%s" % team_id)
        mkdir_p(dirpath)
        return os.path.join(dirpath, "roster_%d.html" % week)

    def has_roster(self, league, team_id, week):
        return os.path.exists(self.roster_path(league, team_id, week))

    def get_roster(self, league, team_id, week):
        return open(self.roster_path(league, team_id, week)).read()

    def write_roster(self, league, team_id, week, html):
        with open(self.roster_path(league, team_id, week), 'w') as f:
            f.write(html)








    def scrape_all_games(self, week_num):
        path = os.path.join(self.d, 'week_%d' % week_num, 'games')
        game_files = os.listdir(path)
        htmls = []
        for game_file in game_files:
            game_file_path = os.path.join(path, game_file)
            html = open(game_file_path).read()
            htmls.append(html)
        return htmls


    def scrape_translogs(self, team_id):
        return open('translog.html').read()

    def scrape_roster_summary(self):
        return open(os.path.join(self.d, 'rostersummary.html')).read()

    def scrape_lineup(self, team_id, week):
        path = os.path.join(self.d, 'team_%s' % team_id, 'week_%d.html' % week)
        return open(path).read()


    def scrape_all_players(self):
        path = os.path.join(self.d, "players")
        player_files = listdir_nohidden(path)
        htmls = []
        for player_file in player_files:
            player_file_path = os.path.join(path, player_file)
            espn_id = re.match(r'player_(\d*).*', player_file).group(1)
            html = open(player_file_path).read()
            htmls.append((espn_id, html))
        return htmls

    def contains_player(self, player_id):
        players_path = os.path.join(self.d, "players")
        player_files = listdir_nohidden(players_path)
        player_str = "player_" + player_id + ".html"
        return player_str in player_files






