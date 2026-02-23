#!/usr/bin/env python

from argparse import ArgumentParser
from re import compile, search, IGNORECASE

from base64 import urlsafe_b64decode
from copy import deepcopy
from datetime import datetime
from hashlib import sha1
from io import BytesIO
from os import listdir, mkdir
from os.path import exists, isfile, join, relpath
from sys import argv
from zipfile import ZipFile
from xmltodict import parse as xmlparse

from html2text import HTML2Text
from mailparser import parse_from_bytes
from redbox import EmailBox as redbox

from shared import paths, stores
from process_requests import read, write


GREEDY_COUNTER = 1
REQUEST_LIFETIME = 90 # days

HOST = 'imap.gmail.com'
PORT = 993
LOCAL = paths['emails']
REMOTE = 'Requests'


def create_parser():
    parser = ArgumentParser()
    
    parser.add_argument('-d',
                        dest='dump',
                        help='dump emails',
                        action='store_true')
    parser.add_argument('--host',
                        dest='host',
                        help=f"IMAP host (default: '{HOST}')",
                        default=HOST)
    parser.add_argument('--port',
                        dest='port',
                        help=f"IMAP port (default: '{PORT}')",
                        default=PORT)
    parser.add_argument('--user',
                        dest='username',
                        help='IMAP username',
                        required='-d' in argv)
    parser.add_argument('--pass',
                        dest='password',
                        help='IMAP password',
                        required='-d' in argv)
    parser.add_argument('--remote',
                        dest='remote',
                        help=f"remote email folder to parse (default: '{REMOTE}')",
                        default='Requests')
    parser.add_argument('--unread',
                        dest='unread',
                        help='keep emails unread in remote folder',
                        action='store_true')
    parser.add_argument('--local',
                        dest='local',
                        help=f"local folder where to dump/parse emails (default: '{relpath(LOCAL)}')",
                        default=paths['emails'])
    parser.add_argument('-p',
                        dest='parse',
                        help='parse dumped emails',
                        action='store_true')
    return parser

def dump_emails(
        host=HOST,
        port=PORT,
        username=None,
        password=None,
        local=LOCAL,
        remote=REMOTE,
    ):

    if not username or not password:
        print('username/password cannot be None')
        exit(1)

    mail = redbox(
        host=host,
        port=port,
        username=username,
        password=password,
    )

    messages = mail[args.remote].search(unseen=True)
    date_now = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

    if len(messages) > 0:
        print(f'[{date_now}] Found {len(messages)} emails')
    else:
        print(f'[{date_now}] No new requests!')
        exit(0)

    if not exists(args.local):
        mkdir(args.local)

    for index, message in enumerate(messages, 1):
        try:
            output = join(args.local, f'{index}.eml')
            date = message.date.strftime('%Y-%m-%d %H:%M:%S')
            with open(output, 'w', newline='') as file:
                file.write(message.content)
                print(f'[{date}] Saved to {index}.eml')
        except Exception:
            continue
        finally:
            if args.unread:
                message.unread()


def parse_emails(local=LOCAL):

    date_now = datetime.now()

    requests_file = paths['requests']

    greedy_users = {}

    requests_diff = read(requests_file)
    requests = deepcopy(requests_diff)

    html2text = HTML2Text()
    html2text.ignore_links = True
    pattern_ci = compile(r'^[a-zA-Z0-9._]+/[a-zA-Z0-9._$]')

    def decode_zip(data):
        decoded = urlsafe_b64decode(data.encode('UTF-8'))
        return ZipFile(BytesIO(decoded))


    for key, value in requests_diff.items():
        insertion_date = value['reql']
        delta = date_now - insertion_date
        if delta.days > REQUEST_LIFETIME:
            requests.pop(key)
            print(f'[DEL] [{insertion_date}] {key}')


    for file in listdir(local):
        file = join(local, file)

        if not file.endswith('.eml'): continue
        if not isfile(file): continue

        try:
            with open(file, 'rb') as file:
                mail = parse_from_bytes(file.read())

                sender = mail.from_[0][1]

                if sender in greedy_users:
                    if greedy_users[sender] > GREEDY_COUNTER: continue

                date = mail.date.replace(tzinfo=None)

                if mail.attachments:
                    attachments = decode_zip(mail.attachments[0]['payload'])
                    xml = xmlparse(attachments.read('appfilter.xml'), process_comments=True)['resources']
                    name = xml['#comment']
                    compinfo = search('ComponentInfo{(.*)}', xml['item']['@component'], IGNORECASE).group(1)
                else:
                    body_plain = html2text.handle(mail.body).strip().split()
                    compinfo = [*{*list(filter(lambda s: pattern_ci.search(s), body_plain))}][0]
                
                id = compinfo.split('/')[0]

                if sender not in greedy_users: greedy_users[sender] = 1

                if compinfo not in requests:
                    requests[compinfo] = {
                        'name': name,
                        'reqt': 1,
                        'reql': date,
                        'hash': sha1(compinfo.encode()).hexdigest(),
                        'urls': [url.format(id) for url in stores]
                    }
                    print(f'[NEW] [{date}] {compinfo}')
                else:
                    greedy_users[sender] += 1
                    requests[compinfo]['reqt'] += 1
                    if requests[compinfo]['reql'] < date:
                        requests[compinfo]['reql'] = date
                    print(f'[N++] [{date}] {compinfo}')
        except Exception as error:
            # print(file, error)
            continue

    write(requests_file, requests)


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()

    if args.dump:
        dump_emails(
            host=args.host,
            port=args.port,
            username=args.username,
            password=args.password,
            local=args.local,
            remote=args.remote,
        )
    
    if args.parse:
        parse_emails(
            local=args.local
        )