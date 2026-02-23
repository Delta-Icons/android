#!/usr/bin/env python

import xml.etree.ElementTree as ET

from argparse import ArgumentParser
from re import sub
from os.path import basename, join, relpath

from shared import paths, transform_xml, list_categories


path = paths['d1']
cat_all = 'All'


def create_parser():
    parser = ArgumentParser()

    parser.add_argument('-i',
                      dest='input',
                      metavar='PATH',
                      help=f"path to {basename(path)} (default: '{relpath(path)}')",
                      default=path)
    parser.add_argument('-c',
                      dest='category',
                      metavar='NAME',
                      help=f"count number of icons in specific category (default: '{cat_all}')",
                      default=cat_all)
    parser.add_argument('-l',
                      dest='list',
                      help=f"list available categories excluding category '{cat_all}'",
                      action='store_true')
    parser.add_argument('-w',
                      dest='write',
                      help=f"write number of icons to CandyBar.java (only works with category '{cat_all}')",
                      action='store_true')
    return parser


def count_icons(input=path, category=cat_all, write=False, list_cats=False):

    categories = list_categories(input)

    if list_cats:
        print('\n'.join(['- ' + x for x in categories]))
        exit()

    with open(input) as file:
        xml = transform_xml(file.read().rstrip())
        root = ET.fromstring(xml)

    elements = root.findall('category')
    category = category.capitalize()
    categories = [cat_all] + categories

    count = 0

    if category not in categories:
        return count

    if category == cat_all:
        for element in elements:
            if element.get('title') in [cat_all, 'New']:
                continue
            count += len(element)

        if write:
            for type in ['play', 'foss']:
                java_path = join(paths['root'], f'app/src/{type}/java/website/leifs/delta/applications/CandyBar.java')
                with open(java_path, 'r+') as file:
                    content = file.read().rstrip()
                    content = sub(r'setCustomIconsCount\(.*\)', f'setCustomIconsCount({count})', content)
                    file.seek(0)
                    file.write(content)
                    file.truncate()
    else:
        count = len(root.find(f'category[@title="{category}"]'))

    return count


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    count = count_icons(
        input=args.input,
        category=args.category,
        write=args.write,
        list_cats=args.list,
    )
    print(count)