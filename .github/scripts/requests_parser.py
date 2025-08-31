#!/usr/bin/env python3

import argparse, re, sys
import xml.etree.ElementTree as ET
from datetime import datetime
from difflib import SequenceMatcher
from copy import deepcopy as copy

import yaml
from natsort import natsorted as sorted

from resolve_paths import paths


class YamlNewLines(yaml.SafeDumper):
    # https://github.com/yaml/pyyaml/issues/127#issuecomment-525800484
    def write_line_break(self, data=None):
        super().write_line_break(data)
        if len(self.indents) == 1:
            super().write_line_break()

    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow, False)

filename = 'requests.yml'


parser = argparse.ArgumentParser(description=f'parse {filename}')

parser.add_argument('-f', '--format',
                    dest='format',
                    choices=['xml', 'yml'],
                    help='output in specific format')
parser.add_argument('-r', '--remove',
                    dest='remove',
                    help=f'remove existing compinfos from {filename}',
                    default=False,
                    action=argparse.BooleanOptionalAction)
parser.add_argument('-R', '--ratio',
                    dest='ratio',
                    help=f'custom ratio from 0.5 to 1.0',
                    default=0.75)
parser.add_argument('-s', '--sort',
                    dest='sort',
                    help='sort by specific value',
                    choices=['name', 'ratio', 'request'],
                    default='ratio')
parser.add_argument('-H', '--hide-ratios',
                    dest='hide_ratios',
                    help='hide ratios in output',
                    default=False,
                    action=argparse.BooleanOptionalAction)


def read(path):
    with open(path, 'r+') as file:
        loaded = yaml.safe_load(file)
        return loaded if loaded is not None else {}


def write(path, data):
    with open(path, 'r+') as file:
        data = dict(sorted(data.items(),
                           # sort by number of requests, then by last request time
                           key=lambda k: (k[1]['reqt'], k[1]['reql']),
                           # reverse array to set new requests at top of the list
                           reverse=True))
        # header message with total number of requested icons and last time update
        header = (f"# {len(data)} requested apps pending \n"
                  f"# updated {datetime.today().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        dump = yaml.dump(data, Dumper=YamlNewLines, allow_unicode=True, indent=4, sort_keys=False)
        file.seek(0)
        file.write(header + dump)
        file.truncate()

def main():
    requests = read(paths['requests'])
    requests_copy = copy(requests)
    
    updatable = {}

    RATIO = float(args.ratio) if 0.5 <= float(args.ratio) <= 1.0 else 0.75

    with open(paths['appfilter'][0], 'r') as file:
        appfilter = ET.ElementTree(ET.fromstring(file.read())).getroot()

    for item in appfilter:
        try:
            compinfo = re.search('ComponentInfo{(.*)}', item.attrib['component']).group(1)
            id, activity = compinfo.split('/')
            name = item.attrib['drawable']

            for request in requests_copy:
                if id not in request: continue

                ratio = 0.0

                if request.startswith(id + '/'):
                    ratio = 1.0
                else: 
                    diff = SequenceMatcher(None, request, compinfo).ratio()
                    ratio = round(diff, 2)

                if ratio >= RATIO:

                    if ratio == 1.0:
                        requests.pop(request)

                    if request in updatable:
                        if updatable[request]['ratio'] < ratio:
                            ratio = updatable[request]['ratio']

                    updatable[request] = {
                        'name': name,
                        'ratio': ratio,
                        'request': request
                    }

        except:
            continue

    updatable = dict(sorted(updatable.items(), key=lambda x: x[1][args.sort]))

    if args.remove:
        write(paths['requests'], requests)

    for [key, value] in updatable.items():
        name = value['name']
        ratio = int(value['ratio'] * 100)

        match args.format:
            case 'xml':
                ratios = f'<!-- {ratio}% --> ' if not args.hide_ratios else ''
                print(ratios + f'<item component="ComponentInfo{{{key}}}" drawable="{name}" />')
            case 'yml':
                ratios = f' # {ratio}%' if not args.hide_ratios else ''
                print(f'{name}:'+ ratios)
                print(f'  - {key}\n')
            case _:
                ratios = f'[{ratio}%] ' if not args.hide_ratios else ''
                print(ratios + f'{name} -> {key}')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        args = parser.parse_args()
    else:
        parser.print_help()
        sys.exit(1)
    main()