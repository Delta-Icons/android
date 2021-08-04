"""
Script Usage:
python (or python3) delta_email_parser.py ./path/to/emlFolder ./path/to/appfilter.xml (./path/to/requests.txt)

Arguments
0: Path to folder containing .eml files of requests
1: Path to existing appfilter.xml to recognize potentially updatable appfilters
3 (optional): existing requests.txt file to augment with new info

Output
If only two arguments are given the script will generate 'requests.txt' and 'updatable.txt'.
If the third argument is given the file will be overwritten with the updated info.
"""

import datetime
from email.parser import BytesParser
from email import policy
from email.utils import parsedate
# from datetime import strftime
from datetime import date
from os import close
from time import mktime
import glob
import re
from sys import argv

# Check for path and add trailing slash
path = argv[1]
if not path.endswith('/'):
	path += '/'


# List of e-mail files
filelist = glob.glob(path + '*.eml')
# Initialization
requestlimit = 1 #Limit of requests per person
apps = {} #Dictionary of requested apps and according info
addresses = {} #E-Mail addresses with number of requests
appInfoQuery = re.compile(r'(?P<Name>[\w\d\@\?\/\(\)\!]+)\s?(?P<ComponentInfo>[\w\.\/\d]+)\shttps://play\.google\.com/store/apps/details\?id=(?P<PackageName>[\w\.]+)', re.M)
eMailQuery = re.compile(r'<(.+)>$')
updatable = []
newApps = []

# Filters to limit backlog
currentDate = date.today()
monthsLimit = 6
minRequests = 5

# Remove people sending more than X requests
def removeGreedy(address, element):
	if address in element['senders']:
		element['count'] = element['count'] - 1
		element['senders'] = [x for x in element['senders'] if x is not address]
	return element

def parseExisting():
	requestBlockQuery = re.compile(r'(?P<Name>.+)\s(?P<ComponentInfo>.+)\shttps:\/\/play.google.com\/store\/apps\/details\?id=.+\sRequested (?P<count>\d+) times\s?(Last requested (?P<requestDate>\d+\.?\d+?))?')
	with open(argv[3], 'r', encoding="utf8") as existingFile:
		contents = existingFile.read()
		existingRequests = re.finditer(requestBlockQuery, contents)
		for req in existingRequests:
			elementInfo = req.groupdict()
			apps[elementInfo['ComponentInfo']] = elementInfo
			apps[elementInfo['ComponentInfo']]['requestDate'] = float(elementInfo['requestDate']) if elementInfo['requestDate'] is not None else mktime(currentDate.timetuple())
			apps[elementInfo['ComponentInfo']]['count'] = int(elementInfo['count'])
			apps[elementInfo['ComponentInfo']]['senders'] = []

def parseMails():
	for mail in filelist:
		with open(mail, 'rb') as msg:
			# Convert Message to String
			msg = BytesParser(policy=policy.default).parse(msg)
			parsed= msg.get_body(preferencelist=('plain'))
			# Skip if body is empty
			if parsed is None:
				continue
			emailBody = parsed.get_content()

			# Check if sender exists
			sender = re.search(eMailQuery, msg['From'])
			if sender is None:
				continue

			# check if sender crossed limit
			if sender.groups()[0] not in addresses:
				addresses[sender.groups()[0]] = 1
			elif addresses[sender.groups()[0]] == requestlimit:
				print('XXXXXX ---- We have a greedy one: ', sender.groups()[0])
				for key, value in apps.items():
					value = removeGreedy(sender.groups()[0], value)
				continue
			else:
				addresses[sender.groups()[0]] += 1

			appInfo = re.search(appInfoQuery, emailBody)

			# AppInfo could not automatically be extracted
			if appInfo is None:
				# Search for String appearance of existing ComponentInfos in E-Mail body
				for key, value in apps.items():
					if key in emailBody:
						apps[key]['count'] += 1
						apps[key]['senders'].append(sender.groups()[0])
						continue
				print('\n/// The following message could not be handled:\n',emailBody,'\n')
			else:
				tempDict = appInfo.groupdict()
				if tempDict['ComponentInfo'] in apps:
					apps[tempDict['ComponentInfo']]['count'] = apps[tempDict['ComponentInfo']]['count'] + 1
					apps[tempDict['ComponentInfo']]['senders'].append(sender.groups()[0])
				else:
					tempDict['count'] = 1
					tempDict['senders'] = [sender.groups()[0]]
					apps[tempDict['ComponentInfo']] = tempDict
				#Update date of last request
				if 'requestDate' not in apps[tempDict['ComponentInfo']] or apps[tempDict['ComponentInfo']]['requestDate'] < mktime(parsedate(msg['date'])):
						apps[tempDict['ComponentInfo']]['requestDate'] = mktime(parsedate(msg['Date']))

def diffMonth(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month

def filterOld():
	global apps
	apps = {k: v for k, v in apps.items() if v['count'] > minRequests or diffMonth(currentDate, datetime.datetime.fromtimestamp(v['requestDate'])) < monthsLimit}

def separateupdatable():
	objectBlock = """
{name}
{component}
https://play.google.com/store/apps/details?id={packageName}
Requested {count} times
Last requested {reqDate}
	"""
	with open(argv[2]) as appfilter:
		appfilter = appfilter.read()
		for (componentInfo, values) in apps.items():
			if appfilter.find(componentInfo) == -1 and ''.join(newApps).find(componentInfo) == -1:
				# newApps.append(app['Name'] + '\n' + app['ComponentInfo'] + '\nhttps://play.google.com/store/apps/details?id=' + componentInfo + '\nRequested ' + str(app['count']) + ' times\nLast requested \n\n')
				newApps.append(objectBlock.format(
					name = values["Name"],
					component = values["ComponentInfo"],
					packageName = values["ComponentInfo"][0:values["ComponentInfo"].index('/')],
					count = values["count"],
					reqDate = values["requestDate"],
				))
			elif appfilter.find(componentInfo) != -1 and ''.join(updatable).find(componentInfo) == -1:
				updatable.append(values['Name'] + '\n' + values['ComponentInfo'] + '\n\n')

def writeOutput():
	newListHeader = """-------------------------------------------------------
{totalCount} Requests Pending ({date})
-------------------------------------------------------
"""
	newList = newListHeader.format( totalCount = sum(ele['count'] for ele in apps.values()), date = date.today().strftime("%d-%m-%Y"))
	newList += ''.join(newApps)

	requestsFilePath = 'requests.txt' if len(argv) < 4 else argv[3]
	with open(requestsFilePath, 'w', encoding='utf-8') as file:
		file.write(newList)
	if len(updatable):
		with open('updatable.txt', 'w', encoding='utf-8') as fileTwo:
			fileTwo.write(''.join(updatable))

def main():
	if len(argv) > 2:
		parseExisting()
	filterOld()
	parseMails()
	sorted(apps.values(), key=lambda item: item['count'], reverse=True)
	separateupdatable()
	writeOutput()


if __name__ == "__main__":
	main()
