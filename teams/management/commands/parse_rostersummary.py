__author__ = 'bprin'

from bs4 import BeautifulSoup

f = open('rostersummary.html')
html = f.read()
soup = BeautifulSoup(html)
soup.find('table', 'playerTableTable').find_all('tr')[2:][0].contents[0].a.string
soup.find('table', 'playerTableTable').find_all('tr')[2:][0].contents[0].a['playerid']