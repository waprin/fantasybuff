import re
from bs4 import BeautifulSoup
from bs4 import Tag
import itertools
import sys
  
f = open("local_scrapes/realboard.html")
html = f.read()

pool = BeautifulSoup(html)
matchups = pool.find_all("table", "matchup")

for matchup in matchups:
    teams = matchup.find_all(id=re.compile('teamscrg'))
    print "================================="
    for team in teams:
        print team["id"]
