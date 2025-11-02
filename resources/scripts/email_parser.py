#!/usr/bin/env python3

import base64
import copy
import io
import re
import os

from datetime import datetime
from hashlib import sha1
from zipfile import ZipFile

import mailparser
import xmltodict

from requests_parser import read, write
from resolve_paths import paths

DATE_NOW = datetime.now()

EMAILS_DIR = os.path.join(paths['scripts'], 'emails')
REQUESTS_FILE = paths['requests']

GREEDY_COUNTER = 1
REQUEST_LIFETIME = 90 # days

STORES = [
    'https://play.google.com/store/apps/details?id={}',
    'https://f-droid.org/en/packages/{}/',
    # 'https://apkpure.com/delta/{}/',
    'https://google.com/search?q={}',
]

greedy_users = {}

requests_diff = read(REQUESTS_FILE)
requests = copy.deepcopy(requests_diff)


def decode_zip(data):
    decoded = base64.urlsafe_b64decode(data.encode('UTF-8'))
    return ZipFile(io.BytesIO(decoded))


for key, value in requests_diff.items():
    insertion_date = value['reql']
    delta = DATE_NOW - insertion_date
    if delta.days > REQUEST_LIFETIME:
        requests.pop(key)
        print(f'[DEL] [{insertion_date}] {key}')


for file in os.listdir(EMAILS_DIR):
    file = os.path.join(EMAILS_DIR, file)

    if not file.endswith('.eml'): continue
    if not os.path.isfile(file): continue

    try:
        with open(file, 'rb') as file:
            mail = mailparser.parse_from_bytes(file.read())

            sender = mail.from_[0][1]

            if sender in greedy_users:
                if greedy_users[sender] > GREEDY_COUNTER: continue

            date = mail.date

            attachments = decode_zip(mail.attachments[0]['payload'])
            xml = xmltodict.parse(attachments.read('appfilter.xml'), process_comments=True)['resources']

            name = xml['#comment']
            compinfo = re.search('ComponentInfo{(.*)}', xml['item']['@component'], re.IGNORECASE).group(1)
            id = compinfo.split('/')[0]

            if sender not in greedy_users: greedy_users[sender] = 1

            if compinfo not in requests:
                requests[compinfo] = {
                    'name': name,
                    'reqt': 1,
                    'reql': date,
                    'hash': sha1(compinfo.encode()).hexdigest(),
                    'urls': [url.format(id) for url in STORES]
                }
                print(f'[NEW] [{date}] {compinfo}')
            else:
                greedy_users[sender] += 1
                requests[compinfo]['reqt'] += 1
                if requests[compinfo]['reql'] < date:
                    requests[compinfo]['reql'] = date
                print(f'[N++] [{date}] {compinfo}')
    except:
        continue


write(REQUESTS_FILE, requests)
