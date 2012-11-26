import re
from bs4 import BeautifulSoup

f = open('standings.html')
html = f.read()

pool = BeautifulSoup(html)
header = pool.find('div', 'games-pageheader')
standings = header.findNextSibling('table')
bodies = standings.findAll('tr', 'tableBody')

for body in bodies:
    fullname = body.td.a['title']
    href = body.td.a['href']
    info = re.search("teamId=(\d+)", href)
    matchedname = re.search("(.*)\s*\((.*)\)", fullname)
    teamname = matchedname.group(1)
    ownername = matchedname.group(2)
    print teamname
    print ownername
    print href
    print info.group(1)
