#! /usr/bin/env python

import argparse, re, sys
import xml.etree.ElementTree as ET

from natsort import natsorted as sorted

from resolve_paths import paths


class XmlKeepComments(ET.TreeBuilder):
    # https://gist.github.com/jamiejackson/a37e8d3dacb33b2dcbc1
    def __init__(self, *args, **kwargs):
        super(XmlKeepComments, self).__init__(*args, **kwargs)

    def comment(self, data):
        self.start(ET.Comment, {})
        self.data(data)
        self.end(ET.Comment)

xml_parser = ET.XMLParser(target=XmlKeepComments())


filename = 'drawable.xml'


parser = argparse.ArgumentParser(description=f'sort {filename}')

parser.add_argument('-i', '--input',
                    dest='input',
                    help=f'path to {filename}',
                    default=paths['drawable'][0])
parser.add_argument('-o', '--output',
                    dest='output',
                    help=f'output to file (default: app/src/main/res/xml/{filename})',
                    nargs='?',
                    const=paths['drawable'][0])
parser.add_argument('-p', '--print',
                    dest='print',
                    help='output to console',
                    default=False,
                    action=argparse.BooleanOptionalAction)


def transform(xml):
    if '</category>' in xml:
        xml = re.sub('\t</category>', '', xml) # remove </category> tags
        xml = re.sub(r'\n(</resources>)', r'\1\n', xml) # remove \n before </resources> and add it after
        xml = re.sub(r'(<category title=".*")>', r'\1 />', xml) # <category> -> </category>
    else:
        xml = re.sub(r'/>\n(\n\t<)', r'/>\1/category>\1', xml) # add </category> after latest <item/>
        xml = re.sub(r'(</resources>)', r'\t</category>\n\1', xml) # add </category> before </resources>
        xml = re.sub(r'(<category title=".*") />', r'\1>', xml) # remove slash from <category/>
    return xml


def main():
    with open(args.input) as file:
        xml = file.read().rstrip() # read drawable.xml to string

    root = ET.fromstring(transform(xml), parser=xml_parser) # transform to true XML format and convert it from string to ET

    for category in root.findall('category'):
        items = category.findall('item') # get all items from category
        children = sorted(items, key=lambda item: item.get('drawable')) # sort category items by drawable name
        category[:] = children # rewrite category items

    xml = ET.tostring(root, encoding='unicode', xml_declaration=True) # convert ET to string
    xml = re.sub("'", '"', transform(xml)) # convert ' to " and transform to default format

    if args.output: # if -o passed
        try:
            with open(args.output, 'w', encoding='utf-8') as file:
                file.write(xml)
        except IsADirectoryError:
            print("Path must be a file!")

    if args.print: # if -p passed
        print(xml)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        args = parser.parse_args()
    else:
        parser.print_help()
        sys.exit(1)
    main()