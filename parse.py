import re
from bs4 import BeautifulSoup
from bs4 import Tag
import itertools

p = re.compile("added(.*?),", re.IGNORECASE)

def containsAdd(tag):
    if tag.name == "td":
        if any(isinstance(d, Tag) and d.name=="td" for d in list(tag.descendants)):
            return False

        text = ''.join(tag.strings)
        print text
        m = p.search(text)
        print "m is none %s " % (m is None)
        return m is not None
        """
        print tag.contents
        s = ''.join(tag.contents)
        m = p.search(s)
        return m is not None
        """
    return False
  
test = "GCR dropped Jared Cook, Ten TE to WaiversGCR added Martellus Bennett, NYG TE from Waivers to Bench "

f = open("waivers.html")
html = f.read()
m = p.search(html)
#print m.group(0)

pool = BeautifulSoup(html)
a = pool.find_all(containsAdd)
print "========================================"
print '\n'.join([''.join(e.strings) for e in a])
