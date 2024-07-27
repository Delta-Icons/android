#!/usr/bin/env python3

import argparse
import xml.etree.ElementTree as ET
import re

from difflib import SequenceMatcher

from requests_parser import read, write
from resolve_paths import paths


parser = argparse.ArgumentParser(description='Find similar strings between appfilter.xml and requests.yml')
parser.add_argument('-x', '--xml',
                    dest='xml',
                    help='Output in xml format',
                    default=False,
                    action=argparse.BooleanOptionalAction)
parser.add_argument('-r', '--remove',
                    dest='remove',
                    help='Remove existing compinfos from requests.yml',
                    default=False,
                    action=argparse.BooleanOptionalAction)
parser.add_argument('-p', '--percent',
                    dest='percent',
                    help='Sort by percentage',
                    default=False,
                    action=argparse.BooleanOptionalAction)
args = parser.parse_args()

requests_file = paths['requests']
requests = read(requests_file)
updatable = {}
duplicates = []

with open(paths['appfilter'][0], 'r') as file:
    appfilter = ET.ElementTree(ET.fromstring(file.read())).getroot()


for item in appfilter:
    try:
        compinfo = re.search('ComponentInfo{(.*)}', item.attrib['component']).group(1)
        id = compinfo.split('/')[0]
        name = item.attrib['drawable']

        if compinfo in duplicates:
            print(f'found duplicate: {compinfo}')
        else:
            duplicates.append(compinfo)

        for request in requests:
            if id not in request: continue
            diff = SequenceMatcher(None, request, compinfo).ratio()
            ratio = round(diff, 2)

            if ratio == 1.0:
                requests.pop(compinfo)
                continue
            
            if ratio >= 0.75:
                if request in updatable:
                    if updatable[request]['ratio'] < ratio:
                        ratio = updatable[request]['ratio']

                updatable[request] = {
                    'name': name,
                    'ratio': ratio
                }
    except:
        continue

sort = lambda x: x[1]['ratio' if args.percent else 'name']
updatable = dict(sorted(updatable.items(), key=lambda x: sort(x)))

for [key, value] in updatable.items():
    name = value['name']
    percent = int(value['ratio'] * 100)
    if args.xml:
        print(f'<item component="ComponentInfo{{{key}}}" drawable="{name}" />')
    else:
        print(f'[{percent}%] {name} -> {key}')

if args.remove:
    write(requests_file, requests)
