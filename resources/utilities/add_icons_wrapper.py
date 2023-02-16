#!/usr/bin/env python3

from os import system as execute
from os.path import abspath, basename, dirname, realpath

from yaml import safe_load as yaml


work_dir = dirname(realpath(__file__))
delta_dir = abspath(f'{work_dir}/../..')
target_file = abspath(f'{work_dir}/../new_icons.yaml')
target_script = abspath(f'{work_dir}/add_icons.py')


content = '''\
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
'''


with open(target_file) as file:
    try:
        icons = [(k,v) for k,v in yaml(file).items()]
    except:
        print(f"'{basename(target_file)}' seems to be empty")
        exit(1)


for icon in icons:
    drawable = icon[0]
    compinfos = ' '.join(icon[1])
    # print(f'[draw] {drawable}')
    command = f'python {target_script} -P {delta_dir} -raidI -n {drawable}'
    if compinfos: command += f' -c {compinfos}'
    execute(command)
    if not icons[-1][0] == drawable: print()


with open(target_file, 'w', newline='') as file:
    file.write(content)
