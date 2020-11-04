"""
Pass a text file with detected updateable appfilters and appfilter.xml as arguments to this script for it to output a new file with the liens to append to appfilter.xml
"""

import sys, os, re

appfilters = open(sys.argv[2]).readlines()

with open(sys.argv[1]) as file:
	lines = file.readlines()
	new_filters = []

	packagename_regex = re.compile(r'([\w\.]+)/')
	appfilter_regex = re.compile(r'<item component="ComponentInfo{([\w\.\/\-]+)}" drawable="[\w\-\d]+" />')

	for line in lines:
		searchterm = re.search(packagename_regex, line)
		if searchterm:
			# print(searchterm.group(0))
			for appf in appfilters:
				if searchterm.group(0) in appf:
					search_appfilter = re.search(appfilter_regex, appf)
					if search_appfilter:
						new_filters.append(appf.replace(search_appfilter.groups(0)[0], line.strip()))
					else:
						print("Error with", appf, line)
					break


	filters = open('new_appfilters.xml', 'w')
	filters.write(''.join(new_filters))
	filters.close()
