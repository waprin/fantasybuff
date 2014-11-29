import time
import os
import errno
import re
import logging

from teams.utils.league_files import choose_league_directory, create_league_directory
from teams.models import League


logger = logging.getLogger(__name__)

__author__ = 'bill'


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


class FileBrowser(object):
    def __init__(self):
        self.d = choose_league_directory(os.listdir(os.path.join(os.getcwd(), 'leagues')))

        if self.d == None:
            self.d = create_league_directory(0)
            self.initialized = False
        else:
            self.initialized = True
        self.d = os.path.join('leagues', self.d)
        self.sleep = 0

    def reload(self):
        logger.debug("reloading file cached browser")
        n = int(re.search(r'league_(\d+)', self.d).group(1))
        logger.debug("moving to new directory %d " % n)
        self.d = create_league_directory(n + 1)
        self.initialized = False

    def has_entrance(self, espn_user):
        return os.path.exists(os.path.join(self.d, 'entrance_%d.html' % espn_user.id))

    def get_entrance(self, espn_user):
        time.sleep(self.sleep)
        return open(os.path.join(self.d, 'entrance_1.html')).read()

    def write_entrance(self, espn_user, html):
        filepath = os.path.join(self.d, 'entrance_%d.html' % espn_user.id)
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
        with open(self.standings_path(league), 'w') as f:
            f.write(html)

    def settings_path(self, league_id, year):
        instance_dir = self.create_instance_directory(league_id, year)
        return os.path.join(instance_dir, 'settings.html')

    def has_settings(self, league_id, year):
        return os.path.exists(self.settings_path(league_id, year))

    def get_settings(self, league_id, year):
        return open(self.settings_path(league_id, year)).read()

    def write_settings(self, league_id, year, html):
        with open(self.settings_path(league_id, year), 'w') as f:
            f.write(html)

    def matchup_path(self, league, week):
        instance_dir = self.create_instance_directory(league.espn_id, league.year)
        return os.path.join(instance_dir, 'matchups_%d.html' % week)

    def has_matchups(self, league, week):
        return os.path.exists(self.matchup_path(league, week))

    def get_matchups(self, league, week):
        time.sleep(self.sleep)
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
        time.sleep(self.sleep)
        return open(self.roster_path(league, team_id, week)).read()

    def write_roster(self, league, team_id, week, html):
        with open(self.roster_path(league, team_id, week), 'w') as f:
            f.write(html)

    def player_path(self, league, player_id):
        instance_dir = self.create_instance_directory(league.espn_id, league.year)
        dirpath = os.path.join(instance_dir, "players")
        mkdir_p(dirpath)
        return os.path.join(dirpath, "player_%s.html" % player_id)

    def has_player(self, league, player_id):
        return os.path.exists(self.player_path(league, player_id))

    def get_player(self, player_id, league=None, year='2013'):
        if league is None:
            league = League(espn_id='930248', year=year)
        return open(self.player_path(league, player_id)).read()

    def write_player(self, league, player_id, html):
        with open(self.player_path(league, player_id), 'w') as f:
            f.write(html)

    def get_all_player_htmls(self, league):
        instance_dir = self.create_instance_directory(league.espn_id, league.year)
        htmls = []
        dirpath = os.path.join(instance_dir, "players")
        mkdir_p(dirpath)
        player_files = os.listdir(dirpath)
        for player_html in player_files:
            id = re.match(r'player_(\d*).html', player_html).group(1)
            htmls.append((id, open(player_html).read()))
        return htmls

    def game_path(self, league, team_id, week):
        instance_dir = self.create_instance_directory(league.espn_id, league.year)
        dirpath = os.path.join(instance_dir, "week_%d" % week)
        mkdir_p(dirpath)
        logger.debug("team id is " + str(team_id))
        return os.path.join(dirpath, "game_%s.html" % team_id)

    def has_game(self, league, team_id, week):
        return os.path.exists(self.game_path(league, team_id, week))

    def get_game(self, league, team_id, week):
        time.sleep(self.sleep)
        return open(self.game_path(league, team_id, week)).read()

    def write_game(self, league, team_id, week, html):
        with open(self.game_path(league, team_id, week), 'w') as f:
            f.write(html)

    def get_all_games(self, league, week):
        instance_dir = self.create_instance_directory(league.espn_id, league.year)
        dirpath = os.path.join(instance_dir, "week_%d" % week)
        mkdir_p(dirpath)
        game_files = os.listdir(dirpath)
        htmls = []
        for game_file in game_files:
            htmls.append(open(game_file).read())
        return htmls

    def translog_path(self, league_id, year, team_id):
        instance_dir = self.create_instance_directory(league_id, year)
        return os.path.join(instance_dir, "translog_%s.html" % team_id)

    def has_translog(self, league_id, year, team_id):
        return os.path.exists(self.translog_path(league_id, year, team_id))

    def get_translog(self, league_id, year, team_id):
        return open(self.translog_path(league_id, year, team_id)).read()

    def write_translog(self, league_id, year, team_id, html):
        with open(self.translog_path(league_id, year, team_id), 'w') as f:
            f.write(html)






