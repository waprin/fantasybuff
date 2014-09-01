__author__ = 'bprin'

f = open('translog.html')
html = f.read()
from bs4 import BeautifulSoup
soup = BeautifulSoup(html)
soup.find_all('table')
soup.find_all('table').find_all('tr')
soup.find_all('table')
dir(soup.find_all('table').find_all('tr'))
dir(soup.find_all('table'))
len(soup.find_all('table'))
dir(soup.find_all('table')[0])
len(soup.find_all('table')[0].find_all('tr'))
soup.find_all('table')[0].find_all('tr')[73]
soup.find_all('table')[0].find_all('tr')[0]
soup.find_all('table')[0].find_all('tr')[2]
soup.find_all('table')[0].find_all('tr')[3]
soup.find_all('table')[0].find_all('tr')[3:]
rows = soup.find_all('table')[0].find_all('tr')[3:]
for row in rows:
    print row.string
for row in rows:
    print row.string
    print row.strings
rows[0]
rows[0].b
rows[1].b
rows[1]
rows[1].contents
rows[1].contents[1]
rows[1].contents[2]
transaction_type = rows[1].b
rows[1].contents[2].string
rows[1].contents[2].strings
' '.join([s for s in rows[1].contents[2].strings])
' '.join([s for s in rows[2].contents[2].strings])
' '.join([s for s in rows[3].contents[2].strings])
' '.join([s for s in rows[4].contents[2].strings])
' '.join([s for s in rows[5].contents[2].strings])