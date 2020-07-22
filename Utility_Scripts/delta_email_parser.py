"""
This Script reads .eml files of Candybar Dashboard and parses their first result
compares it to an appfilter.xml file and structures it into a list of packages
that are already included and need an update and the ones not yet included.

Arguments to be passed to the file are first the path of the folder containing
the .eml files and second the path of the desired appfilter.xml.
"""

import email
from email.parser import BytesParser
from email import policy
import glob
import re
from sys import argv
from warnings import warn

path = argv[1]
if not path.endswith('/'):
	path += '/'

filelist = glob.glob(path + '*.eml')

apps = []
query = re.compile(r'(?P<Name>[\w\d\@\?\/\(\)]+)\s(?P<ComponentInfo>[\w\.\/]+)\shttps://play\.google\.com/store/apps/details\?id=(?P<PackageName>[\w\.]+)', re.M)

for mail in filelist:
	with open(mail, 'rb') as msg:
		msg = BytesParser(policy=policy.default).parse(msg)
		text = msg.get_body(preferencelist=('plain')).get_content()

		info = re.search(query, text)

		if info is None:
			warn("Couldn't handle the following message:\n\n")
			warn(text)
		else:
			apps.append(info.groupdict())


updateable = []
new_apps = []

with open(argv[2]) as appfilter:
	appfilter = appfilter.read()
	for app in apps:
		if appfilter.find(app['PackageName']) is -1 and ''.join(new_apps).find(app['PackageName']) is -1:
			new_apps.append(app['Name'] + '\n' + app['ComponentInfo'] + '\nhttps://play.google.com/store/apps/details?id=' + app['PackageName'] + '\n\n')
		elif appfilter.find(app['PackageName']) is not -1 and ''.join(updateable).find(app['PackageName']) is -1:
			updateable.append(app['Name'] + '\n' + app['ComponentInfo'] + '\n\n')


new_list = '---------------------------------UPDATE---------------------------------\n\n'
new_list += ''.join(updateable)
new_list += '\n\n\n\n---------------------------------NEW---------------------------------\n\n'
new_list += ''.join(new_apps)


with open('new_apps.txt', 'w') as file:
	file.write(new_list)