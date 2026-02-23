#! /usr/bin/env python

import xml.etree.ElementTree as ET

from argparse import ArgumentParser
from re import sub
from sys import argv
from os.path import abspath, dirname, realpath, join


stores = [
    'https://play.google.com/store/apps/details?id={}',
    'https://f-droid.org/en/packages/{}/',
    'https://apkpure.com/delta/{}/',
    'https://google.com/search?q={}',
]


def create_parser():
    parser = ArgumentParser()

    parser.add_argument('-p', '--paths',
                        dest='paths',
                        help='output paths as variables for shell exporting',
                        action='store_true')
    return parser


def format_paths():
    root = abspath(f'{dirname(realpath(__file__))}/../..')
    scripts = abspath(dirname(realpath(__file__)))
    contribs = join(root, 'contribs')
    icons = join(contribs, 'icons')
    return {
        'root': root,
        'scripts': scripts,
        'contribs': contribs,
        'icons': join(contribs, 'icons.yml'),
        'emails': join(scripts, 'emails'),
        'requests': join(contribs, 'requests.yml'),
        'vectors': join(root, 'resources/vectors'),
        'src': {
            'dir': icons,
            'svg': join(icons, f'{{}}.svg'),
            'png': join(icons, f'{{}}.png')
        },
        'dst': {
            'svg': join(root, f'resources/vectors/{{}}.svg'),
            'png': join(root, f'app/src/main/res/drawable-nodpi/{{}}.png')
        },
        'a1': join(root, 'app/src/main/res/xml/appfilter.xml'),
        'a2': join(root, 'app/src/main/assets/appfilter.xml'),
        'd1': join(root, 'app/src/main/res/xml/drawable.xml'),
        'd2': join(root, 'app/src/main/assets/drawable.xml'),
    }


paths = format_paths()


def transform_xml(xml):
    if '</category>' in xml:
        xml = sub('\t</category>', '', xml) # remove </category> tags
        xml = sub(r'\n(</resources>)', r'\1\n', xml) # remove \n before </resources> and add it after
        xml = sub(r'(<category title=".*")>', r'\1 />', xml) # <category> -> </category>
    else:
        xml = sub(r'/>\n(\n\t<)', r'/>\1/category>\1', xml) # add </category> after latest <item/>
        xml = sub(r'(</resources>)', r'\t</category>\n\1', xml) # add </category> before </resources>
        xml = sub(r'(<category title=".*") />', r'\1>', xml) # remove slash from <category/>
    return xml


def list_categories(input=paths['d1']):
    with open(input) as file:
        xml = transform_xml(file.read().rstrip())
    root = ET.fromstring(xml)
    elements = root.findall('category')
    return [x.get('title') for x in elements]


if __name__ == '__main__':
    parser = create_parser()
    if len(argv) > 1:
        args = parser.parse_args()
    else:
        parser.print_help()
        exit(1)

    if args.paths:
        print(f"wd={paths['root']}")
        print(f"sd={paths['scripts']}")
        print(f"id={paths['src']['dir']}")
        print(f"vd={paths['vectors']}")
        print(f"rq={paths['requests']}")
        print(f"a1={paths['a1']}")
        print(f"a2={paths['a2']}")
        print(f"d1={paths['d1']}")
        print(f"d2={paths['d2']}")
