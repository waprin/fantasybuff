import mechanize
import cookielib

from teams.models import MatchupPage

import logging
logger = logging.getLogger(__name__)

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
     
    def scrape_entrance(self):
        r = self.br.open("http://games.espn.go.com/frontpage/football")
        html = r.read()
        return html

    def save_week(self, league, week):
        logger.info('save week(): begin .. ')
        r = self.br.open("http://games.espn.go.com/ffl/boxscorefull?leagueId=%s&teamId=6&scoringPeriodId=%d&seasonId=2012&view=scoringperiod&version=full" % (league.espn_id, week))
        html = r.read()
        MatchupPage.objects.create(html=html, week=week,league=league)
        logger.info("save week(): saved match-up page")
        pass

    def login(self, username, password):
        r = self.br.open("http://m.espn.go.com/wireless/login")
        self.br.select_form(nr=0)
        self.br.form['username'] = username
        self.br.form['gspw'] = password
        self.br.submit()

    def save_scoreboard(self):
        r = self.br.open("http://games.espn.go.com/ffl/boxscorefull?leagueId=930248&teamId=6&scoringPeriodId=11&seasonId=2012&view=scoringperiod&version=full")
        html = r.read()
        f = open("scoreboard.html", "w")
        f.write(html)

    def scrape_standings(self, league_id):
        r = self.br.open("http://games.espn.go.com/ffl/standings?leagueId=%s&seasonId=2012", league_id)
        html = r.read()
        return html

    def save_realboard(self):
        r = self.br.open("http://games.espn.go.com/ffl/scoreboard?leagueId=930248&matchupPeriodId=1")
        html = r.read()
        f = open("realboard.html", "w")
        f.write(html)

