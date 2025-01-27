#! /usr/bin/env python

import argparse, re
import xml.etree.ElementTree as ET

from os.path import join

from resolve_paths import paths


target = paths['drawable'][0]


parser = argparse.ArgumentParser(description=f'count icons')

parser.add_argument('-i', '--input',
                    dest='input',
                    help=f'path to drawable.xml',
                    default=target)
parser.add_argument('-c', '--category',
                    dest='category',
                    help=f'count icons in category',
                    default=None)
parser.add_argument('-w', '--write',
                    dest='write',
                    help='write to files',
                    default=False,
                    action=argparse.BooleanOptionalAction)
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


def main(category = None):

    try:
        category = args.category
    except:
        pass
    
    with open(target) as file:
        xml = file.read().rstrip() # read drawable.xml to string

    root = ET.fromstring(transform(xml)) # transform to true XML format and convert it from string to ET

    if category:
        try:
            category = len(root.find(f'.//category[@title="{category}"]'))
        except:
            print(f'{category} does not exist')    
            exit(1)
        return category
    else:
        count = 0
        for category in root.findall('category'):
            count += len(category)
        count -= len(root.find(f'.//category[@title="New"]'))
        
        try:
            if args.write:
                for type in ['play', 'foss']:
                    path = join(paths['root'], f'app/src/{type}/java/website/leifs/delta/applications/CandyBar.java')
                    with open(path, 'r+') as file:
                        content = file.read()
                        content = re.sub(r'setCustomIconsCount\(.*\)', f'setCustomIconsCount({count})', content)
                        file.seek(0)
                        file.write(content)
                        file.truncate()
        except:
            pass

        return count
    

if __name__ == '__main__':
    args = parser.parse_args()
    count = main()
    if args.print:
        print(count)