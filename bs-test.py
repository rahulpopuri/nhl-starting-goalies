from BeautifulSoup import BeautifulSoup
Soup = BeautifulSoup
import BeautifulSoup

import urllib2
import configparser

import os
from flask import Flask

from slacker import Slacker

app = Flask(__name__)
config = configparser.ConfigParser()
config.read('properties')

slack = Slacker(config['DEFAULT']['SLACK_TOKEN'])

STATUSES = ('Confirmed','Likely','Unconfirmed')


@app.route("/")
def hello():
	page = urllib2.urlopen('http://www2.dailyfaceoff.com/starting-goalies/').read()
	soup = Soup(page)

	for g_a in soup.findAll("div", {"class" : ["goalie away", "goalie home"]}):
	    for name in g_a.findAll("h5"):
	    	goalie_name = name.text
	    for status in g_a.findAll("dl"):
	    	goalie_status = [s for s in STATUSES if s in status.text][0]
	    slack.chat.post_message('#general', goalie_name + ":" + goalie_status)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)