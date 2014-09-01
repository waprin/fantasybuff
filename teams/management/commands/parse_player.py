__author__ = 'bprin'

from bs4 import BeautifulSoup
f = open('player_2580.html')
html = f.read()

def parse_scores_from_playersheet(html):
    pool = BeautifulSoup(html)
    rows = pool.find_all('table')[2].find_all('tr')[1:]
    return [row.find_all('td')[-1].string for row in rows]

