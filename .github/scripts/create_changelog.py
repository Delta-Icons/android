#! /usr/bin/env python

import html, re
import base64
import xml.etree.ElementTree as ET
import argparse
from count_icons import main as count_icons


parser = argparse.ArgumentParser(description=f'create changelog')

parser.add_argument('-d', '--data',
                    dest='data',
                    help='changelog b64 encoded')
parser.add_argument('-r', '--release-type',
                    dest='release_type',
                    help='type of release',
                    choices=['prod', 'beta', 'foss'],
                    default='beta')
parser.add_argument('-p', '--print',
                    dest='print',
                    help='output to console',
                    default=False,
                    action=argparse.BooleanOptionalAction)
parser.add_argument('-w', '--write',
                    dest='write',
                    help='write to files',
                    default=False,
                    action=argparse.BooleanOptionalAction)
parser.add_argument('-t', '--txt',
                    dest='txt',
                    help='path to txt changelog',
                    default='changelog.txt')
parser.add_argument('-x', '--xml',
                    dest='xml',
                    help='path to xml changelog',
                    default='changelog.xml')
args = parser.parse_args()


def main():
    icons_total = count_icons()
    icons_new = count_icons('New')

    txt = []

    try:
        data = base64.b64decode(args.data).decode()
    except:
        data = ''

    resources = ET.Element('resources')

    ET.SubElement(resources, 'string', name='changelog_date')
    changelog = ET.SubElement(resources, 'string-array', name='changelog')

    if args.release_type != 'foss':
        text = f'{icons_new} new icons, {icons_total} in total'
        ET.SubElement(changelog, 'item').text = text
        txt.append('- ' + text)

    match args.release_type:
        case 'prod':
            text = f'Fixed icons not applying properly'
            ET.SubElement(changelog, 'item').text = text
            txt.append('- ' + text)

            for line in data.splitlines():
                line = line.strip()
                if not line: continue
                line = re.sub('^-+', '', line).strip()
                ET.SubElement(changelog, 'item').text = line
                txt.append('- ' + line)
        case 'beta':
            text = 'Full changelog will be published upon release!'
            ET.SubElement(changelog, 'item').text = text
            txt.append('- ' + text)
        case 'foss':
            text = 'This is a FOSS build for testing purposes!'
            ET.SubElement(changelog, 'item').text = text
            txt.append('- ' + text)


    tree = ET.ElementTree(resources)
    ET.indent(tree, space="\t", level=0)

    tree = tree.getroot()

    xml = ET.tostring(tree, encoding='unicode', xml_declaration=True, short_empty_elements=False)

    xml = html.unescape(re.sub(r"(\w+)='(.*?)'", r'\1="\2"', xml))

    if args.print: print(xml)

    if args.write:
        with open(args.xml, 'w', encoding='utf-8') as file:
            file.write(xml)

        with open(args.txt, 'w', encoding='utf-8') as file:
            file.write('\n'.join(txt))

if __name__ == '__main__':
    main()