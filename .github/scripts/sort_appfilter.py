import xml.etree.ElementTree as ET

from re import sub
from os.path import abspath, basename
from sys import argv as arg


src_file = abspath(arg[1]) 
dst_file = 'new_' + basename(src_file)

declaration = '<?xml version="1.0" encoding="UTF-8"?>\n'

with open(src_file, 'r') as file:
    content = file.read()

fromstring = ET.fromstring(content)
tree = ET.ElementTree(fromstring)
root = tree.getroot()

scale = root[0]
root.remove(scale)

root[:] = sorted(root, key=lambda item: (item.tag, item.get('component')))

root.insert(0, scale)

tostring = ET.tostring(root, encoding='utf-8', method='xml').decode('utf-8')
output = declaration + sub('\t</resources>', '</resources>\n', tostring)

with open(dst_file, 'w', encoding='utf-8') as file:
    file.write(output)
