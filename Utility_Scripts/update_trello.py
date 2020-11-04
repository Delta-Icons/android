"""
A script to update the projects Trello boards ToDo list with icons from a JSON file.

Usage: python update_trello.py path_to.json 'YOUR_TRELLO_API_KEY' 'YOUR_TRELLO_API_TOKEN'

JSON is to be formatted as follows: [
	{
		"name": "AppName",
		"appfilter": "example.package/package.activity",
		"url": "Play Store URL goes here",
		"count": 0 (number of times requested)
	}, ...
]
"""
import sys
from ratelimit import limits
from trello import TrelloClient, Card
import json

# Load file and parse json
new_apps = json.load(open(sys.argv[1]))
new_apps = sorted(new_apps, key=lambda x: x["count"], reverse=True)

# connect to Trello API
client = TrelloClient(
	api_key=sys.argv[2],
	token=sys.argv[3]
)

# The ToDO list
todo = client.get_list('5f7f8dd1238edd7ceea5f81d')

# Method to create card (rate limited as to specification)
@limits(calls=100, period=10)
def sendCardCreationCall(trellist, name, appfilter):
	trellist.add_card(
		name=name,
		desc=appfilter,
		position="bottom"
	)

# loop over apps to add
for app in new_apps:
	sendCardCreationCall(
		todo,
		app["name"],
		"ComponentInfo:\n{appfilter}\n\nPlay Store:\n{url}\n\nRequested {count} times".format(**app)
	)