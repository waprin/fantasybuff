import re
from bs4 import BeautifulSoup

__author__ = 'bprin'

def get_leagues_from_entrance(html):
    pool = BeautifulSoup(html)
    league_elements = pool.find_all('a', 'leagueoffice-link')
    leagues = []
    for element in league_elements:
        name = element.string
        m = re.search(r'leagueId=(\d*)&teamId=\d*&seasonId=(\d*)', element['href'])
        espn_id = m.group(1)
        year = m.group(2)
        leagues.append((name, espn_id, year))
    return leagues