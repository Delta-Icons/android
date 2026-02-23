#!/usr/bin/env python

from argparse import ArgumentParser
import argparse, re, sys
import xml.etree.ElementTree as ET
from datetime import datetime
from difflib import SequenceMatcher
from copy import deepcopy
from os.path import basename, relpath
import yaml
from natsort import natsorted as sorted

from shared import paths, stores


class YamlNewLines(yaml.SafeDumper):
    # https://github.com/yaml/pyyaml/issues/127#issuecomment-525800484
    def write_line_break(self, data=None):
        super().write_line_break(data)
        if len(self.indents) == 1:
            super().write_line_break()

    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow, False)


PATH = paths['requests']

FORMATS = ['txt', 'xml', 'yml']
FORMATS_DEFAULT = FORMATS[2]

SORTS = ['name', 'ratio', 'request']
SORTS_DEFAULT = SORTS[1]

RATIO_RANGE = {'min': 0.25, 'default': 0.75, 'max': 1.0}


def create_parser():
    parser = ArgumentParser()

    parser.add_argument('-i',
                        dest='input',
                        metavar='PATH',
                        help=f"path to {basename(PATH)} to process (default: '{relpath(PATH)}')",
                        default=PATH)
    parser.add_argument('-f',
                        dest='format',
                        metavar=f"[{'|'.join(FORMATS)}]",
                        choices=FORMATS,
                        help=f"output in specific format (default: '{FORMATS_DEFAULT}')",
                        default=FORMATS_DEFAULT)
    parser.add_argument('-r',
                        dest='ratio',
                        metavar='VALUE',
                        help=f"custom ratio value from {RATIO_RANGE['min']} to {RATIO_RANGE['max']} (default: {RATIO_RANGE['default']})",
                        default=RATIO_RANGE['default'])
    parser.add_argument('-H',
                        dest='hide_ratios',
                        help='hide ratios in output',
                        action='store_true')
    parser.add_argument('-s',
                        dest='sort',
                        metavar=f"[{'|'.join(SORTS)}]",
                        help=f"sort by specific value (default: '{SORTS_DEFAULT}')",
                        choices=SORTS,
                        default=SORTS_DEFAULT)
    parser.add_argument('-u', '--update',
                        dest='update',
                        help=f'update and remove entries in {basename(PATH)}',
                        action='store_true')
    parser.add_argument('--urls',
                        dest='urls',
                        help=f'update store urls (use with -u)',
                        action='store_true')
    parser.add_argument('-q',
                        dest='quiet',
                        help='do not print anything',
                        action='store_true')
    return parser

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


def parse_requests(
        input=PATH,
        format=FORMATS_DEFAULT,
        ratio=RATIO_RANGE['default'],
        sort=SORTS_DEFAULT,
        hide_ratios=False,
        update=False,
        urls=False,
        quiet=False,
    ):

    requests = read(input)
    requests_copy = deepcopy(requests)
    
    updatable = {}

    RATIO = float(ratio) if RATIO_RANGE['min'] <= float(ratio) <= RATIO_RANGE['max'] else RATIO_RANGE['default']

    with open(paths['a1'], 'r') as file:
        appfilter = ET.ElementTree(ET.fromstring(file.read().rstrip())).getroot()

    if urls:
        for request in requests_copy:
            id, activity = request.split('/')
            requests[request]['urls'] = [url.format(id) for url in stores]

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

    updatable = dict(sorted(updatable.items(), key=lambda x: x[1][sort]))

    if update:
        if requests != requests_copy:
            write(input, requests)

    if not quiet:
        for [key, value] in updatable.items():
            name = value['name']
            ratio = int(value['ratio'] * 100)

            match format:
                case 'xml':
                    ratios = f'<!-- {ratio}% --> ' if not hide_ratios else ''
                    print(ratios + f'<item component="ComponentInfo{{{key}}}" drawable="{name}" />')
                case 'yml':
                    ratios = f' # {ratio}%' if not hide_ratios else ''
                    print(f'{name}:'+ ratios)
                    print(f'  - {key}\n')
                case 'txt':
                    ratios = f'[{ratio}%] ' if not hide_ratios else ''
                    print(ratios + f'{name} -> {key}')


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    parse_requests(
        input=args.input,
        format=args.format,
        ratio=args.ratio,
        sort=args.sort,
        hide_ratios=args.hide_ratios,
        update=args.update,
        urls=args.urls,
        quiet=args.quiet,
    )