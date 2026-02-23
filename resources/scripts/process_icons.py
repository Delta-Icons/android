#!/usr/bin/env python

import re
import logging as log
import xml.etree.ElementTree as ET

from argparse import ArgumentParser
from copy import deepcopy
from os import environ, unlink
from os.path import basename, isfile, relpath
from shutil import copy, move

from natsort import natsorted as sorted
from termcolor import colored as color

from process_requests import read
from shared import paths, transform_xml

ACTIONS = ('none', 'remake', 'rebrand', 'remove')

PATTERN_ALT = re.compile(r'^.*_alt_\d+$')
PATTERN_CI = re.compile(r'^[a-zA-Z0-9._]+/[a-zA-Z0-9._$]+$')
PATTERN_DRAWABLE = re.compile(r'^[a-z0-9_]+$')

ICONS_HEADER = '''\
# # action: none|remake|rebrand|remove|rename > new_name
# #   none    - default, new icon
# #   remake  - overwrite existing images, add to new category
# #   rebrand - existing icon -> alt_x, new icon -> main
# #   remove  - remove existing icon (files + xml)
# #   rename  - rename existing icon (files + xml)
#
# new_icon_1: com.example.icon/com.example.icon.MainActivity
#
# new_icon_2:
#   - com.example.icon/com.example.icon.MainActivity
#   - com.example.icon/com.example.icon.SplashActivity
#
# new_icon_3_alt_1: {}
#
# new_icon_4: {}
#
# signal:
#   action: rebrand
#   category: Google
#   compinfo:
#     - com.google.app/com.google.app.MainActivity
#
'''

args = ArgumentParser()
args.add_argument('-d', '--dry-run', action='store_true', help='do things without changing any files')
args.add_argument('-v', '--verbose', action='store_true', help='verbose')
args.add_argument('-n', '--no-color', action='store_true', help='disable colors')
args.add_argument('-s', '--sort', action='store_true', help='sort xml files only, skip icons.yml')
args = args.parse_args()

if args.no_color:
    environ['NO_COLOR'] = '1'

log.addLevelName(log.DEBUG, color('d', 'magenta'))
log.addLevelName(log.INFO, color('i', 'blue'))
log.addLevelName(log.WARNING, color('w', 'yellow'))
log.addLevelName(log.ERROR, color('e', 'red'))
log.addLevelName(log.CRITICAL, color('c', 'red'))
log.basicConfig(
    level=log.DEBUG if args.verbose else log.INFO,
    datefmt='%H:%M:%S',
    format='%(levelname)s %(message)s',
)


def log_sep(name):
    print(color(f'\n<------- {name} ------->', 'dark_grey'))


def xml_parser():
    return ET.XMLParser(target=ET.TreeBuilder(insert_comments=True))


def write_file(target, content):
    with open(target, 'w') as file:
        file.write(content)


def parse_action(raw):
    match raw:
        case True:
            return 'rebrand', None, None
        case False | None:
            return 'none', None, None
        case str():
            if '>' in raw:
                action, _, rename = raw.partition('>')
                action, rename = action.strip(), rename.strip()
                if action != 'rename':
                    return 'none', None, f"action {color(action, 'cyan')} doesn't support {color('>', 'cyan')} syntax"
                if not rename:
                    return 'none', None, f"rename requires a target, e.g. {color('rename > new_name', 'cyan')}"
                return 'rename', rename, None
            if raw == 'rename':
                return 'none', None, f"rename requires a target, e.g. {color('rename > new_name', 'cyan')}"
            if raw in ACTIONS:
                return raw, None, None
            return 'none', None, f"action {color(raw, 'cyan')} is invalid, expected: {color(', '.join((*ACTIONS, 'rename > name')), 'cyan')}"
        case _:
            return 'none', None, f"action {color(str(raw), 'cyan')} is invalid, expected: {color(', '.join((*ACTIONS, 'rename > name')), 'cyan')}"


def parse_compinfos(value):
    result = []
    for key in ('compinfo', 'compinfos'):
        entries = value.get(key, [])
        if isinstance(entries, list):
            result.extend(entries)
        else:
            result.append(entries)
    return result


def check_source_files(key, extensions=('png', 'svg')):
    missing = []
    for ext in extensions:
        if not isfile(paths['src'][ext].format(key)):
            missing.append(ext)
    return missing


def move_images(src_name, dst_name=None, from_dst=False, header=True):
    if dst_name is None:
        dst_name = src_name
    src_paths = paths['dst'] if from_dst else paths['src']
    if header:
        found = any(isfile(src_paths[fmt].format(src_name)) for fmt in ('png', 'svg'))
        if found:
            log.info(f"images{color(':', 'dark_grey')}")
    for fmt in ('png', 'svg'):
        src = src_paths[fmt].format(src_name)
        dst = paths['dst'][fmt].format(dst_name)
        if isfile(src):
            if not args.dry_run:
                move(src, dst)
            print(f"  {color(f'~ {relpath(src)} -> {relpath(dst)}', 'blue')}")


def remove_images(name):
    found = any(isfile(paths['dst'][fmt].format(name)) for fmt in ('png', 'svg'))
    if found:
        log.info(f"images{color(':', 'dark_grey')}")
    for fmt in ('png', 'svg'):
        path = paths['dst'][fmt].format(name)
        if isfile(path):
            if not args.dry_run:
                unlink(path)
            print(f"  {color(f'– {relpath(path)}', 'red')}")


def parse_icons(icons_yml, root_drawable):
    entries = []
    errors = dict()

    categories = [
        x.get('title')
        for x in root_drawable.findall('category')
        if x.get('title') != 'New'
    ]

    for key, value in icons_yml.items():
        entry_errors = []

        if not PATTERN_DRAWABLE.fullmatch(key):
            entry_errors.append(f"name {color(key, 'cyan')} looks invalid")
            errors[key] = True

        action = 'none'
        rename = None
        compinfos = []

        category = key[0].upper()
        if key.startswith('_'):
            category = '#'
        if PATTERN_ALT.fullmatch(key):
            category = 'Alts'

        match value:
            case dict():
                compinfos = parse_compinfos(value)
                category = value.get('category', category).capitalize()
                action, rename, action_error = parse_action(value.get('action', 'none'))
                if action_error:
                    entry_errors.append(action_error)
                    errors[key] = True
                if action == 'remove':
                    if not any(isfile(paths['dst'][fmt].format(key)) for fmt in ('png', 'svg')):
                        entry_errors.append(f"action is {color('remove', 'cyan')}, but {key} doesn't exist in destination")
                        errors[key] = True
                if rename:
                    if not PATTERN_DRAWABLE.fullmatch(rename):
                        entry_errors.append(f"rename target {color(rename, 'cyan')} looks invalid")
                        errors[key] = True
                    elif not any(isfile(paths['dst'][fmt].format(key)) for fmt in ('png', 'svg')):
                        entry_errors.append(f"action is {color('rename', 'cyan')}, but {key} doesn't exist in destination")
                        errors[key] = True
                    elif 'category' not in value:
                        category = rename[0].upper()
                        if rename.startswith('_'):
                            category = '#'
                        if PATTERN_ALT.fullmatch(rename):
                            category = 'Alts'
            case list():
                compinfos = list(dict.fromkeys(value))
            case str():
                compinfos = [value]

        if category not in categories and action != 'remove':
            entry_errors.append(f"category {color(category.lower(), 'cyan')} doesn't exist")
            errors[key] = True

        if action in ('remake', 'rebrand'):
            for ext in check_source_files(key):
                entry_errors.append(f"action is {color(action, 'cyan')}, but {key}.{ext} not found")
                errors[key] = True

        compinfos = list(dict.fromkeys(x for x in compinfos if isinstance(x, str) and x))

        if not compinfos and category == 'Alts' and action not in ('rename', 'remove'):
            for ext in check_source_files(key):
                entry_errors.append(f"category is Alts but {key}.{ext} not found")
                errors[key] = True

        for compinfo in compinfos:
            if not PATTERN_CI.fullmatch(compinfo):
                entry_errors.append(f"compinfo {color(compinfo, 'cyan')} looks invalid")
                errors[key] = True

        if entry_errors:
            log_sep(key)
            for error in entry_errors:
                log.error(error)

        entries.append((key, {
            'category': category,
            'compinfos': compinfos,
            'action': action,
            'rename': rename,
        }))

    if errors:
        log_sep('result')
        log.critical('fix issues with the next icons:\n' + '\n'.join(
            '  - ' + color(x, 'magenta') for x in errors
        ))
        print()
        exit(1)

    return entries


def main():
    if not args.sort:
        icons_yml = read(paths['icons'])

        if not icons_yml:
            log.warning(f'{basename(paths["icons"])} is empty')

    with open(paths['d1']) as file:
        xml_drawable = file.read().rstrip()

    with open(paths['a1']) as file:
        xml_appfilter = file.read().rstrip()

    root_drawable = ET.fromstring(transform_xml(xml_drawable), parser=xml_parser())
    root_appfilter = ET.fromstring(xml_appfilter, parser=xml_parser())

    scale = root_appfilter[0]
    root_appfilter.remove(scale)

    category_new = root_drawable.find("category[@title='New']")
    category_alt = root_drawable.find("category[@title='Alts']")

    if args.sort:
        log.info('sorting xml files')

    for drawable, values in (parse_icons(icons_yml, root_drawable) if not args.sort else []):
        log_sep(drawable)

        renamed_drawable = []
        renamed_appfilter = []
        added_drawable = []
        old_drawable = drawable

        if values['rename']:
            new_name = values['rename']
            log.info(f"action {color('=', 'dark_grey')} {color('rename', 'magenta')}{color(':', 'dark_grey')} {color(drawable, 'cyan')} {color('->', 'dark_grey')} {color(new_name, 'cyan')}")

            for item in root_appfilter.findall('item'):
                if item.get('drawable') == drawable:
                    renamed_appfilter.append((ET.tostring(item).decode().strip(), new_name))
                    item.set('drawable', new_name)

            for cat in root_drawable.findall('category'):
                for item in list(cat.findall('item')):
                    if item.get('drawable') == drawable:
                        renamed_drawable.append(ET.tostring(item).decode().strip())
                        cat.remove(item)

            drawable = new_name
        elif values['action'] != 'none':
            log.info(f"action {color('=', 'dark_grey')} {color(values['action'], 'magenta')}")

        if values['action'] != 'remove':
            log.info(f"category {color('=', 'dark_grey')} {color(values['category'].lower(), 'magenta')}")

        match values['action']:
            case 'rename':
                move_images(old_drawable, drawable, from_dst=True)
            case 'remove':
                remove_images(drawable)
                removed_drawable = []
                for cat in root_drawable.findall('category'):
                    for item in list(cat.findall('item')):
                        if item.get('drawable') == drawable:
                            removed_drawable.append(ET.tostring(item).decode().strip())
                            cat.remove(item)
                if removed_drawable:
                    log.info(f"drawable.xml{color(':', 'dark_grey')}")
                    for entry in removed_drawable:
                        print(f"  {color(f'– {entry}', 'red')}")
                removed_appfilter = []
                for item in list(root_appfilter.findall('item')):
                    if item.get('drawable') == drawable:
                        removed_appfilter.append(ET.tostring(item).decode().strip())
                        root_appfilter.remove(item)
                if removed_appfilter:
                    log.info(f"appfilter.xml{color(':', 'dark_grey')}")
                    for entry in removed_appfilter:
                        print(f"  {color(f'– {entry}', 'red')}")
            case 'rebrand':
                counter = 1
                targets = []
                for item in root_appfilter.findall('item'):
                    if item.get('drawable') == drawable:
                        targets.append(item)
                    if item.get('drawable').startswith(drawable + '_alt_'):
                        alt_num = int(re.split(r'_', item.get('drawable'))[-1]) + 1
                        if alt_num > counter:
                            counter = alt_num
                new_name = f'{drawable}_alt_{counter}'
                if values['compinfos']:
                    for target in targets:
                        renamed_appfilter.append((ET.tostring(target).decode().strip(), new_name))
                        target.set('drawable', new_name)
                item = ET.Element('item')
                item.set('drawable', new_name)
                item.tail = '\n\t'
                category_alt.append(item)
                move_images(drawable, new_name, from_dst=True)
                move_images(drawable, header=False)
                added_drawable.append(f'<item drawable="{new_name}" /> {color(f'(alts)', 'dark_grey')}')
            case 'remake':
                move_images(drawable)
            case _:
                move_images(drawable)

        if values['action'] not in ('remove',):
            category = root_drawable.find(f"category[@title='{values['category']}']")
            add_drawable = drawable not in [item.get('drawable') for item in category]

            add_new = drawable not in [item.get('drawable') for item in category_new]

            if renamed_drawable or added_drawable or add_drawable or (values['action'] == 'remake' and add_new):
                log.info(f"drawable.xml{color(':', 'dark_grey')}")
                for entry in renamed_drawable:
                    print(f"  {color(f'– {entry}', 'red')}")
                for entry in added_drawable:
                    print(f"  {color(f'+ {entry}', 'green')}")
                if add_drawable:
                    item = ET.Element('item')
                    item.set('drawable', drawable)
                    cat_name = values['category'].lower()
                    item.tail = '\n\t'
                    category.append(item)
                    category_new.append(deepcopy(item))
                    print(f"  {color(f'+ {ET.tostring(item).decode()}', 'green')} {color(f'(new, {cat_name})', 'dark_grey')}")
                elif values['action'] == 'remake' and add_new:
                    item = ET.Element('item')
                    item.set('drawable', drawable)
                    item.tail = '\n\t'
                    category_new.append(item)
                    print(f"  {color(f'+ {ET.tostring(item).decode()}', 'green')} {color('(new)', 'dark_grey')}")

            if renamed_appfilter or values['compinfos']:
                log.info(f"appfilter.xml{color(':', 'dark_grey')}")
                for old_entry, new_drawable in renamed_appfilter:
                    print(f"  {color(f'– {old_entry}', 'red')}")
                    new_entry = old_entry.replace(f'drawable="{old_drawable}"', f'drawable="{new_drawable}"')
                    print(f"  {color(f'+ {new_entry}', 'green')}")

            for compinfo in values['compinfos']:
                component = f'ComponentInfo{{{compinfo}}}'
                if any(item.get('drawable') == drawable and item.get('component') == component for item in root_appfilter):
                    log.warning(f"duplicate ci: {color(compinfo, 'cyan')}")
                    continue
                item = ET.Element('item')
                item.set('component', component)
                item.set('drawable', drawable)
                print(f"  {color(f'+ {ET.tostring(item).decode()}', 'green')}")
                item.tail = '\n\t'
                root_appfilter.append(item)

    for category in root_drawable.findall('category'):
        category[:] = sorted(category.findall('item'), key=lambda item: item.get('drawable'))

    xml_drawable = ET.tostring(root_drawable, encoding='unicode', short_empty_elements=True, xml_declaration=True)
    xml_drawable = re.sub("'", '"', transform_xml(xml_drawable))

    root_appfilter[:] = sorted(root_appfilter, key=lambda item: (item.tag, item.get('component')))
    root_appfilter.insert(0, scale)

    ET.indent(root_appfilter, space='\t')
    xml_appfilter = ET.tostring(root_appfilter, encoding='unicode', xml_declaration=True)
    xml_appfilter = re.sub("'", '"', xml_appfilter)

    if not args.dry_run:
        write_file(paths['a1'], xml_appfilter)
        copy(paths['a1'], paths['a2'])

        write_file(paths['d1'], xml_drawable)
        copy(paths['d1'], paths['d2'])

        if not args.sort:
            write_file(paths['icons'], ICONS_HEADER)

    print()


if __name__ == '__main__':
    main()
