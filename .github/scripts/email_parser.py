import argparse
import base64
import io
import re
import os 

from hashlib import sha1
from zipfile import ZipFile

import mailparser
import xmltodict

from requests_parser import read, write


WORK_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + '../../../')
EMAILS_DIR = f'{WORK_DIR}/.github/scripts/emails'
REQUESTS_FILE = f'{WORK_DIR}/contribs/requests.yml'

GREEDY_COUNTER = 1

STORES = [
    'https://play.google.com/store/apps/details?id={}',
    'https://f-droid.org/en/packages/{}/',
    'https://google.com/search?q={}',
]

requests = read(REQUESTS_FILE)
greedy_users = {}


def decode_zip(data):
    decoded = base64.urlsafe_b64decode(data.encode('UTF-8'))
    return ZipFile(io.BytesIO(decoded))


for file in os.listdir(EMAILS_DIR):
    file = os.path.join(EMAILS_DIR, file)

    if not file.endswith('.eml'): continue
    if not os.path.isfile(file): continue

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
        else:
            greedy_users[sender] += 1
            requests[compinfo]['reqt'] += 1
            if requests[compinfo]['reql'] < date:
                requests[compinfo]['reql'] = date

        print(f'[{date}] {compinfo}')

write(REQUESTS_FILE, requests)
