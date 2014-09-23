import mechanize
import cookielib
import os

import logging
logger = logging.getLogger(__name__)

import time

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

    def login(self, username, password):
        self.br.open("http://m.espn.go.com/wireless/login")
        self.br.select_form(nr=0)
        self.br.form['username'] = username
        self.br.form['gspw'] = password
        self.br.submit()


    def get_entrance(self, user):
        r = self.br.open("http://games.espn.go.com/frontpage/football")
        html = r.read()
        return html


    def get_roster(self, league, team_id, week):
        time.sleep(3)
        logger.debug("requesting page to get to correct year")
        self.br.open("http://games.espn.go.com/ffl/clubhouse?leagueId=%s&teamId=1&seasonId=%s" % (league.espn_id, league.year))
        time.sleep(3)
        request = "http://games.espn.go.com/ffl/playertable/prebuilt/manageroster?leagueId=%s&teamId=%s&scoringPeriodId=%d&view=overview&context=clubhouse&ajaxPath=playertable/prebuilt/manageroster&managingIr=false&droppingPlayers=false&asLM=false&r=28027522" % (league.espn_id, team_id, week)
        logger.debug('making request: ' + request)
        r = self.br.open(request)
        return r.read()

    def get_standings(self, league):
        time.sleep(1)
        url = "http://games.espn.go.com/ffl/standings?leagueId=%s&seasonId=%s" % (league.espn_id, league.year)
        logger.debug("get_standings(): url is %s" % url)
        r = self.br.open(url)
        html = r.read()
        return html

    def get_player(self, player_id, league):
        time.sleep(3)
        request = "http://games.espn.go.com/ffl/format/playerpop/overview?leagueId=%s&playerId=%s&playerIdType=playerId&seasonId=%s" % (league.espn_id, player_id, league.year)
        logger.debug("get_player(): url is %s" % request)
        r = self.br.open(request)
        html = r.read()
        return html

    def get_game(self, league, team_id, week):
        time.sleep(1)
        logger.debug('scrape game(): begin .. ')
        url = "http://games.espn.go.com/ffl/boxscorefull?leagueId=%s&teamId=%s&scoringPeriodId=%d&seasonId=%s&view=scoringperiod&version=full" % (league.espn_id, team_id, week, league.year)
        logger.debug("scrape_game(): scraping url %s" % url)
        r = self.br.open(url)
        html = r.read()
        return html

    def get_matchups(self, league, week):
        time.sleep(1)
        self.br.open("http://games.espn.go.com/ffl/clubhouse?leagueId=%s&teamId=%s&seasonId=%s" % (league.espn_id, 1, league.year))
        r = self.br.open("http://games.espn.go.com/ffl/scoreboard?leagueId=%s&matchupPeriodId=%d" % (league.espn_id, week))
        html = r.read()
        return html

    def get_season_totals(self, index):
        time.sleep(1)
        r = self.br.open("http://games.espn.go.com/ffl/leaders?&seasonTotals=true&seasonId=2013&startIndex=%d" % index)
        return r.read()


    """
    def scrape_translog(self, espn_id, team_id):
        time.sleep(1)
        r = self.br.open("http://games.espn.go.com/ffl/recentactivity?leagueId=%s&seasonId=2013&activityType=2&startDate=20130805&endDate=20140909&teamId=%d&tranType=-1" % (espn_id, team_id))
        html = r.read()
        return html
    """


if __name__ == '__main__':
    scraper = EspnScraper()
    scraper.login('gothamcityrogues', 'sincere1')
    scraper.save_scoreboard()


