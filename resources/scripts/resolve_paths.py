#! /usr/bin/env python

import argparse, sys

from os.path import abspath, dirname, realpath, join


parser = argparse.ArgumentParser(description='Process drawable.xml file')

parser.add_argument('-p', '--print',
                    dest='print',
                    help='Print paths for shell exporting',
                    default=False,
                    action=argparse.BooleanOptionalAction)


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
        'appfilter': [
            join(root, 'app/src/main/res/xml/appfilter.xml'),
            join(root, 'app/src/main/assets/appfilter.xml')
        ],
        'drawable': [
            join(root, 'app/src/main/res/xml/drawable.xml'),
            join(root, 'app/src/main/assets/drawable.xml')
        ]
    }

paths = format_paths()


if __name__ == '__main__':
    args = parser.parse_args()
    if len(sys.argv) > 1:
        args = parser.parse_args()
    else:
        parser.print_help()
        sys.exit(1)
    if args.print:
        print(f"wd={paths['root']}")
        print(f"sd={paths['scripts']}")
        print(f"id={paths['src']['dir']}")
        print(f"vd={paths['vectors']}")
        print(f"rq={paths['requests']}")
        print(f"a1={paths['appfilter'][0]}")
        print(f"a2={paths['appfilter'][1]}")
        print(f"d1={paths['drawable'][0]}")
        print(f"d2={paths['drawable'][1]}")
