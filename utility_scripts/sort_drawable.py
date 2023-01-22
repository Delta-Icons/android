#! /usr/bin/env python

#  that old script needs to be rewritten; remember we had real app names? :(

from os.path import abspath, basename
from re import compile, search
from string import ascii_uppercase as alphabet
from sys import argv as arg
from unicodedata import normalize

from natsort import natsorted as sorted

target_file = abspath(arg[1])

categories = [
	"New",
	"Google",
	"System",
	"Folders",
	"Calendar",
	"Alts",
	"#"
]

categories_no_encode = [
	"Calendar"
]

categories += list(alphabet)

def build_category(cat, array):
	output = f'\n\t<category title="{cat}" />\n'
	template_half = '\t<item drawable="{0}" />\n'
	template_full = '<item name="{0}" drawable="{1}" />\n\t'
	for entry in array:
		try: output += template_full.format(entry['name'], entry['drawable'])
		except: output += template_half.format(entry['name'])
	return output

def parse_category(title, target):
	array = []
	regex_cat = compile(fr'<category title="{title}" />')
	regex_draw = compile(r'(name="(.*)" )?drawable="(.*)"')
	number = 0
	while target:
		category_found = search(regex_cat, target[number])
		if category_found: break
		number += 1
	item = True
	number += 1
	while item:
		item = search(regex_draw, target[number])
		if item:
			try:
				name = normalize("NFKD", item.groups(2)[1])
				drawable = item.groups(3)[1]
				array.append({"drawable": drawable, "name": name})
				number += 1
			except:
				drawable = item.groups(2)[2]
				array.append({"name": drawable})
				number += 1

	array = [i for n, i in enumerate(array) if i not in array[n + 1:]]

	if any(category in title for category in categories_no_encode):
		return sorted(array, key=lambda x: x["name"])
	else:
		return sorted(array, key=lambda x: x["name"].encode("ascii", "ignore").lower())


with open(target_file, "r") as file:
	xml = file.readlines()

	content = '<?xml version="1.0" encoding="utf-8"?>\n' \
			  "<resources>\n" \
		      "\t<version>1</version>\n" \
			  "\t<!--Please avoid automatically sorting categories to keep the current order in place-->\n"

	for category in categories:
		content += build_category(category, parse_category(category, xml))

	content += "</resources>\n"

	new_file = "new_" + basename(target_file)
	with open(new_file, "w", encoding="UTF-8") as file: file.write(content)

exit(0)