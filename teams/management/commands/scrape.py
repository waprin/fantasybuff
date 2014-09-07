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


    def scrape_entrance(self):
        r = self.br.open("http://games.espn.go.com/frontpage/football")
        html = r.read()
        return html

    def scrape_game(self, espn_id, team_id, week):
        time.sleep(1)
        logger.debug('scrape game(): begin .. ')
#        team_id = game.first_scorecard.team.espn_id
        url = "http://games.espn.go.com/ffl/boxscorefull?leagueId=%s&teamId=%s&scoringPeriodId=%d&seasonId=2013&view=scoringperiod&version=full" % (espn_id, team_id, week)
        logger.info("scrape_game(): scraping url %s" % url)
        r = self.br.open(url)
        html = r.read()
        return html

    def scrape_standings(self, espn_id):
        time.sleep(1)
        url = "http://games.espn.go.com/ffl/standings?leagueId=%s&seasonId=2013" % (espn_id)
        logger.debug("scrape_standings(): url is %s" % url)
        r = self.br.open(url)
        html = r.read()
        return html

    def scrape_scoreboard(self, espn_id, week):
        time.sleep(1)
        r = self.br.open("http://games.espn.go.com/ffl/scoreboard?leagueId=%s&matchupPeriodId=%d" % (espn_id, week))
        html = r.read()
        return html

    def scrape_translog(self, espn_id, team_id):
        time.sleep(1)
        r = self.br.open("http://games.espn.go.com/ffl/recentactivity?leagueId=%s&seasonId=2013&activityType=2&startDate=20130805&endDate=20140909&teamId=%d&tranType=-1" % (espn_id, team_id))
        html = r.read()
        return html

    def scrape_roster_summary(self, espn_id, team_id):
        time.sleep(1)
        #930248&teamId=6")
        request = "http://games.espn.go.com/ffl/activestats?leagueId=%s&teamId=%d" % (espn_id, team_id)
        print "request is " + request
        self.br.open("http://games.espn.go.com/ffl/clubhouse?leagueId=%s&teamId=%d&seasonId=2013" % (espn_id, team_id))
        r = self.br.open(request)
        html = r.read()
        return html

    def scrape_player(self, espn_id, player_id, year):
        time.sleep(1)
        request = "http://games.espn.go.com/ffl/format/playerpop/overview?leagueId=%s&playerId=%s&playerIdType=playerId&seasonId=%s" % (espn_id, player_id, year)
        r = self.br.open(request)
        html = r.read()
        return html

    def scrape_defenses(self, espn_id, year):
        time.sleep(1)
        request = "http://games.espn.go.com/ffl/freeagency?leagueId=%s&teamId=1&seasonId=%s#&seasonId=%s&slotCategoryId=16" % (espn_id, year, year)
        logger.debug('making request: ' + request)
        request = "http://games.espn.go.com/ffl/playertable/prebuilt/freeagency?leagueId=930248&teamId=6&seasonId=2013&=undefined&view=overview&context=freeagency&slotCategoryId=16&r=47510218"
        #request = "http://games.espn.go.com/ffl/playertable/prebuilt/freeagency?leagueId=%s&teamId=6&seasonId=%s&=undefined&view=overview&context=freeagency&slotCategoryGroup=null&r=49073861" % (espn_id, year)
        #self.br.open("http://games.espn.go.com/ffl/clubhouse?leagueId=%s&teamId=%d&seasonId=2013" % (espn_id, 6))
        r = self.br.open(request)
        html = r.read()
        return html

    def scrape_lineup(self, league_id, team_id, week, year):
        time.sleep(1)
        self.br.open("http://games.espn.go.com/ffl/clubhouse?leagueId=%s&teamId=1&seasonId=%s" % (league_id, year))
        time.sleep(1)
        r = self.br.open("http://games.espn.go.com/ffl/playertable/prebuilt/manageroster?leagueId=%s&teamId=%s&scoringPeriodId=%d&view=overview&context=clubhouse&ajaxPath=playertable/prebuilt/manageroster&managingIr=false&droppingPlayers=false&asLM=false&r=28027522" % (league_id, team_id, week))
        return r.read()


if __name__ == '__main__':
    scraper = EspnScraper()
    scraper.login('gothamcityrogues', 'sincere1')
    scraper.save_scoreboard()


