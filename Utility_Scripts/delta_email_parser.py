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

path = argv[1]
if not path.endswith('/'):
	path += '/'

filelist = glob.glob(path + '*.eml')

apps = {}
addresses = []
query = re.compile(r'(?P<Name>[\w\d\@\?\/\(\)\!]+)\s?(?P<ComponentInfo>[\w\.\/\d]+)\shttps://play\.google\.com/store/apps/details\?id=(?P<PackageName>[\w\.]+)', re.M)
eMailQuery = re.compile(r'<(.+)>$')

def removeTraitors(traitorAddress, element):
	if traitorAddress in element['senders']:
		element['count'] = element['count'] - 1
		element['senders'] = [x for x in element['senders'] if x is not traitorAddress]
	return element


for mail in filelist:
	with open(mail, 'rb') as msg:
		msg = BytesParser(policy=policy.default).parse(msg)
		parsed= msg.get_body(preferencelist=('plain'))
		if parsed is None:
			continue
		text = parsed.get_content()

		sender = re.search(eMailQuery, msg['From'])
		if sender is None:
			continue
		if sender.groups()[0] in addresses:
			print('XXXXXX ---- We have a traitor: ', sender.groups()[0])
			for key, value in apps.items():
				value = removeTraitors(sender.groups()[0], value)
			continue
		else:
			addresses.append(sender.groups()[0])
		info = re.search(query, text)

		if info is None:
			for key, value in apps.items():
				if key in text:
					apps[key]['count'] = apps[key]['count'] + 1
					apps[key]['senders'].append(sender.groups()[0])
					continue
			print('\n/// The following message could not be handled:\n',text,'\n')
		else:
			tempDict = info.groupdict()
			if tempDict['ComponentInfo'] in apps:
				apps[tempDict['ComponentInfo']]['count'] = apps[tempDict['ComponentInfo']]['count'] + 1
				apps[tempDict['ComponentInfo']]['senders'].append(sender.groups()[0])
			else:
				tempDict['count'] = 1
				tempDict['senders'] = [sender.groups()[0]]
				apps[tempDict['ComponentInfo']] = tempDict


apps = sorted(apps.values(), key=lambda item: item['count'], reverse=True)

updateable = []
new_apps = []

with open(argv[2]) as appfilter:
	appfilter = appfilter.read()
	for app in apps:
		if appfilter.find(app['PackageName']) == -1 and ''.join(new_apps).find(app['PackageName']) == -1:
			new_apps.append(app['Name'] + '\n' + app['ComponentInfo'] + '\nhttps://play.google.com/store/apps/details?id=' + app['PackageName'] + '\nRequested ' + str(app['count']) + ' times\n\n')
		elif appfilter.find(app['PackageName']) != -1 and ''.join(updateable).find(app['PackageName']) == -1:
			updateable.append(app['Name'] + '\n' + app['ComponentInfo'] + '\n\n')


new_list = '---------------------------------UPDATE---------------------------------\n\n'
new_list += ''.join(updateable)
new_list += '\n\n\n\n---------------------------------NEW---------------------------------\n\n'
new_list += ''.join(new_apps)


with open('new_apps.txt', 'w') as file:
	file.write(new_list)