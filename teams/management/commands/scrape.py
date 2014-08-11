import mechanize
import cookielib
import os

import logging
logger = logging.getLogger(__name__)

DEFAULT_DIRECTORY = 'local_scrapes/'

class EspnScraper:

    def __init__(self):
        self.br = mechanize.Browser()
        self.cj = cookielib.LWPCookieJar()
        self.br.set_cookiejar(self.cj)

        self.br.set_handle_equiv(True)
        self.br.set_handle_gzip(True)
        self.br.set_handle_redirect(True)
        self.br.set_handle_referer(True)

        self.br.set_handle_robots(False)
        self.br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

        self.br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

        self.d = DEFAULT_DIRECTORY

    def scrape_entrance(self):
        r = self.br.open("http://games.espn.go.com/frontpage/football")
        html = r.read()
        return html

    def scrape_game(self, game):
        time.sleep(1)
        logger.debug('scrape week(): begin .. ')
        team_id = game.first_scorecard.team.espn_id
        url = "http://games.espn.go.com/ffl/boxscorefull?leagueId=%s&teamId=%s&scoringPeriodId=%d&seasonId=2012&view=scoringperiod&version=full" % (game.league.espn_id, team_id, game.week)
        logger.info("scrape_week(): scraping url %s" % url)
        r = self.br.open(url)
        html = r.read()
        return html

    def save_week(self, game):
        logger.debug('save_week(): begin .. ')
        html = self.scrape_week(game)
        team_id = game.first_scorecard.team.espn_id
        weeks_dir = os.path.join(self.d, 'weeks')
        if not os.path.exists(weeks_dir):
            os.mkdir(weeks_dir)
        filename = os.path.join(weeks_dir, "%d-%s.html" % (game.week, team_id))
        logger.debug('save_week(): saving scraped week to file %s ' % (filename))
        f = open(filename, 'w')
        f.write(html)

    def login(self, username, password):
        self.br.open("http://m.espn.go.com/wireless/login")
        self.br.select_form(nr=0)
        self.br.form['username'] = username
        self.br.form['gspw'] = password
        self.br.submit()

    def scrape_standings(self, espn_id):
        url = "http://games.espn.go.com/ffl/standings?leagueId=%s&seasonId=2012" % (espn_id)
        logger.debug("scrape_standings(): url is %s" % url)
        r = self.br.open(url)
        html = r.read()
        return html

    def scrape_scoreboard(self, league, week):
        r = self.br.open("http://games.espn.go.com/ffl/scoreboard?leagueId=%s&matchupPeriodId=%d" % (league.espn_id, week))
        html = r.read()
        return html

    def save_realboard(self):
        r = self.br.open("http://games.espn.go.com/ffl/scoreboard?leagueId=930248&matchupPeriodId=1")
        html = r.read()
        f = open("realboard.html", "w")
        f.write(html)

class FileScraper:

    def __init__(self):
        self.d = DEFAULT_DIRECTORY

    def scrape_entrance(self):
        filename = os.path.join(self.d, "entrance.html")
        return open(filename).read()

    def scrape_realboard(self):
        filename = os.path.join(self.d, "realboard.html")
        return open(filename).read()

    def scrape_standings(self):
        filename = os.path.join(self.d, "leagues/")
        return open(filename).read()


def get_scraper(local):
    if local:
        return FileScraper()
    else:
        return EspnScraper()



if __name__ == '__main__':
    scraper = EspnScraper()
    scraper.login('gothamcityrogues', 'sincere1')
    scraper.save_scoreboard()

