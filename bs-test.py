from BeautifulSoup import BeautifulSoup
Soup = BeautifulSoup
import BeautifulSoup

import urllib2
import configparser

import os
from flask import Flask
from flask.json import jsonify

from slackclient import SlackClient

import schedule
import time

from CodernityDB.database import Database

STATUSES = ('Confirmed','Likely','Unconfirmed')
app = Flask(__name__)

@app.route("/")
def hello():
	return "Hello!"

@app.route("/refresh")
def refresh():
	page = urllib2.urlopen('http://www2.dailyfaceoff.com/starting-goalies/').read()
	soup = Soup(page)

	for g_a in soup.findAll("div", {"class" : ["goalie away", "goalie home"]}):
	    for name in g_a.findAll("h5"):
	    	goalie_name = name.text
	    for status in g_a.findAll("dl"):
	    	goalie_status = [s for s in STATUSES if s in status.text][0]
	    #for team in g_a.findAll('span', attrs={'class':'logo'}):
	    #	print team.string
	    slack.api_call("chat.postMessage",channel='#general', text=goalie_name + ":" + goalie_status)

	return "Done"

@app.route("/channels")
def channels():
	channels_call = slack.api_call("channels.list")
	if channels_call['ok']:
		return jsonify({'data':channels_call})
	return None


#db = Database('./db')
#db.create()
config = configparser.ConfigParser()
config.read('properties')
slack = SlackClient(config['DEFAULT']['SLACK_TOKEN'])

schedule.every(10).minutes.do(refresh);

while True:
	schedule.run_pending()
	time.sleep(1)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)