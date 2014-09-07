from teams.utils.league_files import choose_league_directory
import os
import re

__author__ = 'bill'

def listdir_nohidden(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f

class FileBrowser(object):

    def __init__(self):
        leagues_dir = choose_league_directory(os.listdir(os.path.join(os.getcwd(), 'leagues')))
        self.d = os.path.join('leagues', leagues_dir)

    def scrape_entrance(self):
        return open(os.path.join(self.d, 'entrance.html')).read()

    def scrape_scoreboard(self, espn_id, week_num):
        return open(os.path.join(self.d, 'week_%d' % week_num, 'scoreboard.html')).read()

    def scrape_standings(self):
        return open(os.path.join(self.d, "standings.html"))

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

    def scrape_lineup(self):
        return open(os.path.join(self.d, 'lineup.html')).read()

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





