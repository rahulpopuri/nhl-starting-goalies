from BeautifulSoup import BeautifulSoup
Soup = BeautifulSoup
import BeautifulSoup
import urllib2

from slacker import Slacker

slack = Slacker('INSERT SLACK API TOKEN HERE')

STATUSES = ('Confirmed','Likely','Unconfirmed')

page = urllib2.urlopen('http://www2.dailyfaceoff.com/starting-goalies/').read()
soup = Soup(page)

for g_a in soup.findAll("div", {"class" : ["goalie away", "goalie home"]}):
    for name in g_a.findAll("h5"):
    	goalie_name = name.text
    for status in g_a.findAll("dl"):
    	goalie_status = [s for s in STATUSES if s in status.text][0]
    slack.chat.post_message('#general', goalie_name + ":" + goalie_status)
