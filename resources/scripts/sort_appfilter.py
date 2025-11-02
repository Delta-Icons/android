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


filename = 'appfilter.xml'


parser = argparse.ArgumentParser(description=f'sort {filename}')

parser.add_argument('-i', '--input',
                    dest='input',
                    help=f'path to {filename}',
                    default=paths['appfilter'][0])
parser.add_argument('-o', '--output',
                    dest='output',
                    help=f'output to file (default: app/src/main/res/xml/{filename})',
                    nargs='?',
                    const=paths['appfilter'][0])
parser.add_argument('-p', '--print',
                    dest='print',
                    help='output to console',
                    default=False,
                    action=argparse.BooleanOptionalAction)


def main():
    with open(args.input) as file:
        xml = file.read().rstrip() # read appfilter.xml to string

    root = ET.fromstring(xml, parser=xml_parser) # convert string to ET

    scale = root[0] # save <scale/> tag
    root.remove(scale) # remove <scale/> tag

    root[:] = sorted(root, key=lambda item: (item.tag, item.get('component'))) # sort items by tag name then my component attribute
    root.insert(0, scale) # restore <scale/> tag

    xml = ET.tostring(root, encoding='unicode', xml_declaration=True) # convert ET to string
    xml = re.sub("'", '"', xml) # convert ' to " and transform to default format
    xml = re.sub(r'\t(</resources>)', r'\1\n', xml) # remove \t before </resources> and \n after

    if args.output: # if -o passed
        try:
            with open(args.output, 'w', encoding='utf-8') as file:
                file.write(xml)
        except IsADirectoryError:
            print("Must be a file!")

    if args.print: # if -p passed
        print(xml)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        args = parser.parse_args()
    else:
        parser.print_help()
        sys.exit(1)
    main()
