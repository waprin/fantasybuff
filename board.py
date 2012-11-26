import re
from bs4 import BeautifulSoup
from bs4 import Tag
import itertools
import sys

"""
def containsAdd(tag):
    if tag.name == "td":
        if any(isinstance(d, Tag) and d.name=="td" for d in list(tag.descendants)):
            return False

        text = ''.join(tag.strings)
        print text
        m = p.search(text)
        print "m is none %s " % (m is None)
        return m is not None
    return False
def isTeamContainer(tag):
    if tag.name != "div":
        return False
    if not tag.has_attr("style"):
        return None

    #print div(tag)
    style = tag["style"]
    m = re.findall(r'width: 100%; margin-bottom: 40px', style)
    return m is not None
"""
    

  
f = open("scoreboard.html")
html = f.read()
#m = p.search(html)
#print m.group(0)

pool = BeautifulSoup(html)
teams = pool.find_all(text=re.compile(r"(?<!Full)(?<!Quick) Box Score.*"))
teams = filter(lambda t : not "at" in t, teams)
for team in teams:
    print team[:team.find("Box")]
    player_table =  team.findParent("div")
    a = player_table.find_all("td", attrs =  { "class" : "playertablePlayerName" })
    for e in a:
        sys.stdout.write("%s " % (''.join(e.strings)))
        print e.findNext('td', 'appliedPoints').string
