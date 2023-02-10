#!/usr/bin/env python

import argparse

from os import mkdir
from os.path import dirname, exists, realpath

from redbox import EmailBox


argparser = argparse.ArgumentParser(description='Dump a IMAP folder into .eml files')
argparser.add_argument('-s', dest='host',
                             help='IMAP host',
                             default='imap.gmail.com')
argparser.add_argument('-P', dest='port',
                             help='IMAP port',
                             default=993)
argparser.add_argument('-u', dest='username',
                             help='IMAP username',
                             required=True)
argparser.add_argument('-p', dest='password',
                             help='IMAP password',
                             required=True)
argparser.add_argument('-r', dest='remote',
                             help='Remote folder to download',
                             default='INBOX')
argparser.add_argument('-l', dest='local',
                             help='Local folder where to save .eml files',
                             default=f'{dirname(realpath(__file__))}/emails')
args = argparser.parse_args()

mail = EmailBox(host=args.host,
                port=args.port,
                username=args.username,
                password=args.password)

messages = mail[args.remote].search(unseen=True)
print(f'{len(messages)+1} new emails')
if not exists(args.local): mkdir(args.local)


for message in messages:
    try:
        index = messages.index(message) + 1
        filename = f'{args.local}/{index}.eml'
        with open(filename, 'w', newline='') as file:
            file.write(message.content)
    except:
        continue