#!/usr/bin/env python3

import argparse
import re

from os import system as execute
from os import name as platform
from os.path import basename, join
from shlex import quote

from requests_parser import read, write
from resolve_paths import paths


work_dir = paths['scripts']
delta_dir = paths['root']

add_icons = join(work_dir, 'add_icons.py')

icons_file = paths['icons']
requests_file = paths['requests']


header = '''\
#
# new_icon_1:
#   - com.example/com.example.MainActivity
#
# new_icon_2:
#   - com.example.1/com.example.MainActivity
#   - com.example.2/com.example.MainActivity
#
# new_icon_2_alt_1: {}
#
# new_icon_3:
#   category: Google
#   compinfos:
#     - com.google.app/com.google.app.MainActivity
'''


parser = argparse.ArgumentParser()
parser.add_argument('-D', '--dry-run', action='store_true', help='do things without changing any files')
options = parser.parse_args()


icons_yml = read(icons_file) 

if icons_yml is None:
    print(f'warn: looks like {basename(icons_file)} is empty')
    exit(1)

requests = read(requests_file)

if icons_yml is None:
    print(f'warn: looks like {basename(icons_file)} is empty')
    exit(1)


errors = []

icons = [(key, value) for key, value in icons_yml.items()]


command_base = f"python '{add_icons}' -P '{delta_dir}' -aidI"

if options.dry_run: command_base += ' -D'


for icon in icons:
    
    name = icon[0]
    data = icon[1]

    category = None
    compinfos = None


    if isinstance(data, dict):
        if len(data) == 0: 
            print()
        else:
            category = data.get('category', None)
            compinfos = data.get('compinfos', None)

    elif isinstance(data, list):
        compinfos = icon[1]
    else:
        print('isinstance error')
        exit(2)
        

    command = f"{command_base} -n '{name}'"

    if compinfos:
        for compinfo in compinfos:
            command += f" -c '{compinfo}'"
            if compinfo in requests:
                requests.pop(compinfo)
    else:
        if re.match('^.*_alt_[0-9]+$', name):
            category = 'Alts'

    if category: command += f" -C '{quote(category)}'"
    print(command)

    print(f'[icon] {name}')
    status = execute(f'{command}')
    print()


    if status != 0:
        errors.append(name)
    
    if status == 0:
        icons_yml.pop(name)


if errors:
    errors.sort()
    print(f'Issues with the next icons: {", ".join(errors)}')
    exit(1)

if options.dry_run: exit(0)

with open(icons_file, 'w', newline='') as file:
    file.write(header)

write(requests_file, requests)
