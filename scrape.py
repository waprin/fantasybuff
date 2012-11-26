import mechanize
import cookielib
import re
from bs4 import BeautifulSoup
import json
import sys


br = mechanize.Browser()

cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

username='gothamcityrogues'
password='sincere1'



r = br.open("http://m.espn.go.com/wireless/login")
br.select_form(nr=0)
br.form['username'] = username
br.form['gspw'] = password
br.submit()

def save_scoreboard():
    r = br.open("http://games.espn.go.com/ffl/boxscorefull?leagueId=930248&teamId=6&scoringPeriodId=11&seasonId=2012&view=scoringperiod&version=full")
    html = r.read()
    f = open("scoreboard.html", "w")
    f.write(html)



#save_scoreboard()

def save_standings():
    r = br.open("http://games.espn.go.com/ffl/standings?leagueId=930248&seasonId=2012")
    html = r.read()
    f = open("standings.html", "w")
    f.write(html)

#save_standings()
def save_realboard():
    r = br.open("http://games.espn.go.com/ffl/scoreboard?leagueId=930248&matchupPeriodId=1")
    html = r.read()
    f = open("realboard.html", "w")
    f.write(html)

#save_realboard()

r = br.open("http://games.espn.go.com/frontpage/football")
html = r.read()

f = open("entrance.html", "w")
f.write(html)
sys.exit()

p = re.compile(r"leagueId=(\d*)&teamId=(\d*)&seasonId=(\d*)")
m = p.search(html)

"""
link_pool = BeautifulSoup(html)
link = ad_pool.find('a', attrs = {'class' : 'clubhouse-link' })
link_url = link["href"]
"""
print m.group(0)
leagueId= m.group(1)
teamId = m.group(2)
seasonId = m.group(3)

r = br.open("http://games.espn.go.com/ffl/clubhouse?leagueId=%s&teamId=%s&seasonId=%s" % (leagueId, teamId, seasonId))
html = r.read()


#page = BeautifulSoup(html)
p = re.compile("pncInitPlayersAndSlots.*script>")
m = p.search(html)
roster = m.group(0)

p = re.compile("rosterManager.createPlayer\((.*?)\)")
m = p.finditer(roster)
players = []

for match in  m:
    players.append(match.group(1))

print players

transactions = "http://games.espn.go.com/ffl/recentactivity?leagueId=%s&seasonId=%s&activityType=2&startDate=20120825&endDate=20121120&teamId=%s&tranType=-1" % (leagueId, seasonId, teamId)

r = br.open(transactions)
html = r.read()

f = open('waivers.html', 'w')
f.write(html)

