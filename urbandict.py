import urllib2
from bs4 import BeautifulSoup

def define(word):
    if not type(word) is str:
        return
    words = word.split()
    if len(words) > 1:
        word = words[0]

    url = 'http://www.urbandictionary.com/define.php?term=%s' % word
    try:
        page = urllib2.urlopen(url)
    except:
        return
    html = page.read()
    soup = BeautifulSoup(html)
    definition_div = soup.find("div", {"class" : "definition"})
    if definition_div is None:
        return
    definition = definition_div.get_text()
    return definition

