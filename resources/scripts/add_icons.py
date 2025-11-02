#!/usr/bin/env python3

import argparse
import re

from filecmp import cmp as compare
from itertools import chain
from os import name as platform
from os import system as execute
from os.path import abspath, basename, dirname, exists, realpath
from shutil import copyfile as copy
from shutil import move
from subprocess import check_output as get_output
from sys import argv as args

import requests_parser
from resolve_paths import paths

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--name', metavar='NAME', help='the name of a drawable entry')
parser.add_argument('-c', '--compinfos', metavar='NAME', action='append', default=[], nargs='+', help='include one or multiple compinfos')
parser.add_argument('-a', '--include-appfilter', action='store_true', help='process the appfilter.xml file')
parser.add_argument('-d', '--include-drawable', action='store_true', help='process the drawable.xml file')
parser.add_argument('-C', '--category', metavar='NAME', help='add to a specific category instead of the named one')
parser.add_argument('-r', '--include-requests', action='store_true', help='process the requests.txt file')
parser.add_argument('-i', '--include-icons', action='store_true', help='move icons to the target folders')
parser.add_argument('-o', '--copy-icons', action='store_true', help='copy icons instead of moving')
parser.add_argument('-f', '--force', action='store_true', help='overwrite icons in target folder')
parser.add_argument('-g', '--git-commit', metavar='MESSAGE', help='commit local changes with a specific message')
parser.add_argument('-D', '--dry-run', action='store_true', help='do things without changing any files')
parser.add_argument('-I', '--ignore-errors', action='store_true', help='ignore errors')
parser.add_argument('-P', '--path', metavar='PATH', help='set custom path to delta folder')
parser.add_argument('-p', '--plain-text', action='store_true', help='disable colorized output')
parser.add_argument('-v', '--verbose', action='store_true', help='more debug output')
options = parser.parse_args()

# -----------
# definitions
# -----------

include_appfilter = options.include_appfilter
include_drawable = options.include_drawable
include_requests = options.include_requests
include_icons = options.include_icons
ignore_errors = options.ignore_errors
copy_icons = options.copy_icons
git_commit = options.git_commit
plain_text = options.plain_text
git_commit = options.git_commit
compinfos = list(chain.from_iterable(options.compinfos)) # flatten array
category = options.category
dry_run = options.dry_run
verbose = options.verbose
force = options.force
name = options.name
path = options.path

if path: delta_dir = abspath(path)
else: delta_dir = dirname(realpath(__file__ + '/../..')) # if the script placed in utility_scripts

work_dir = paths['scripts']
icons_dir = paths['src']['dir']
appfilter_files = paths['appfilter']
drawable_files = paths['drawable']
requests_file = paths['requests']
icons_src_files = [
    paths['src']['png'].format(name),
    paths['src']['svg'].format(name)
]
icons_dst_files = [
    paths['dst']['png'].format(name),
    paths['dst']['svg'].format(name)
]

git_arguments = appfilter_files + drawable_files + [requests_file]

blank = ''
changes = False
dry_run_prefix = 'will be ' if dry_run else blank

execute(blank) # enable coloring in PowerShell and cmd (weird, I know)


def write(file, content):
    # used to avoid repeating code
    if not dry_run:
        file.seek(0)
        file.write(content)
        file.truncate()


class out():
    # reject stdlib logging, embrace custom logging without stderr
    reset = '\033[0m'
    def color(text=False, code=blank):
        # 0 gray / 1 red / 2 green / 3 yellow
        # 4 blue / 5 purple / 6 cyan / 7 white
        reset = '\033[0m'
        if plain_text: return text
        if code == blank: code = out.reset
        if code in range(0, 8): code = f'\033[9{code}m'
        else: code = out.reset
        if text: code = f'{code}{text}{reset}'
        return code
    def base(text, level='info', code=4):
        print(f'[{out.color(code=code, text=level)}] {text}')
        if level == 'fail': exit(1)
    info = lambda text: out.base(text)
    fail = lambda text: out.base(text + '', level='fail', code=1)
    done = lambda text: out.base(text, level='done', code=2)
    warn = lambda text: out.base(text, level='warn', code=3)
    def verb(text=False, code=0):
        if verbose:
            if not text: text = '...'
            out.base(out.color(code=code, text=text), level='verb', code=5)
    rem = color(code=1, text=f'- {{0}}')
    add = color(code=2, text=f'+ {{0}}')

# ------------
# testing zone
# ------------

test_files = appfilter_files + drawable_files + [requests_file]
include_all = include_appfilter or include_drawable or include_icons

if len(args) < 2:
    parser.print_usage()
    exit()

for test_file in test_files:
    if not exists(test_file): out.fail(f"file '{test_file}' not found, maybe you forgot to set -P option (simply move the script to utility_scripts dir)")

if not name:
    if include_all: out.fail('use -n option options -a/-d/-i')
    if category:
        out.fail('use -C option together with -n and -d options')
        if not include_drawable: out.warn('-C option is useless without -d option')
    if include_drawable: out.warn('-C option is useless without -d option')

if name:
    if not category:
        category = name[0].upper()
        if category[0] == '_': category = '#'
        if name[0].isdigit(): out.fail(f"drawable name that starts with a number must be prefixed with '_'")
        if name[0] == '_' and name[1].isalpha(): out.fail(f"drawable name must have a leading number after '_'")

if not exists(icons_dir): out.fail(f"dir '{icons_dir}' not found, create it next to the script")

if include_icons and not ignore_errors:
    for test_file in icons_src_files:
        if not exists(test_file): out.fail(f"icon '{test_file}' not found")
    if not force:
        for test_file in icons_dst_files:
            if exists(test_file): out.fail(f"icon '{test_file}' exists in target folder, use -f option to overwrite it")

compinfos = [*{*compinfos}] # https://stackoverflow.com/a/60518033

for compinfo in compinfos:
    match = re.search(r'^(.*?)\/[\w+.$]+', compinfo)
    if not match:
        out.fail(f"compinfo '{compinfo}' not looks valid")

include_all += include_requests

if not dry_run: out.info('started')
else: out.info('started in dry mode')

# -----
# main?
# -----

if include_drawable:
    filename = 'drawable.xml'
    with open(drawable_files[0], 'r+', encoding='utf-8', newline=blank) as file:
        content = file.read()
        drawable_entry = f'<item drawable="{name}" />'
        categories = ['<category title="New" />', f'<category title="{category}" />']
        if category == 'New': out.fail(f"{filename}: category '{category}' can't be used")
        if not re.search(categories[1], content, re.IGNORECASE): out.fail(f"{filename}: category '{category}' not found")
        if re.search(drawable_entry, content, re.IGNORECASE): out.warn(f"{filename}: drawable '{name}' exists")
        else:
            # file.seek(0)
            # content_list = file.readlines()
            # drawables_count = 0
            # entries = []
            # category_name = category
            # for occurence, category in enumerate(categories):
            #     index = False
            #     scroll = False
            #     stop = False
            #     category_sorted = []
            #     category_unsorted = []
            #     for line in content_list:
            #         search = re.search(re.compile(category, re.IGNORECASE), line)
            #         if search:
            #             categories[occurence] = search.group(0)
            #             scroll = True
            #             continue
            #         if re.search('^\t?$', line): scroll = False
            #         if scroll: category_unsorted.append(line.strip())
            #     category_sorted = sorted(category_unsorted + [drawable_entry])
            #     for category in category_unsorted:
            #         if re.search(drawable_entry, category): stop = True
            #     if stop: continue
            #     for line in category_sorted:
            #         if re.search(drawable_entry, line):
            #             index = category_sorted.index(line)
            #             break
            #     if index:
            #         pattern = category_sorted[index-1]
            #         entries += [pattern]
            #         replace = fr'{pattern}\n\t{drawable_entry}'
            #         content = re.sub(pattern, replace, content, occurence + 1)
            #         drawables_count += 1
            file.seek(0)
            content_list = file.readlines()
            drawables_count = 0
            category_name = category
            entries = []

            for category in categories:
                replace = fr'{category}\n\t{drawable_entry}'
                entries += [category]
                content = re.sub(category, replace, content)
                drawables_count += 1

            if drawables_count > 0:
                write(file, content)
                out.done(f'{filename}: {dry_run_prefix + "added"} 2 entries in \'New\' and \'{category_name}\'')
                out.verb()
                for id, entry in enumerate(entries):
                    if verbose:
                        out.verb(categories[id])
                        out.verb(out.add.format(drawable_entry))
                        out.verb()
                changes = True
            else: out.warn(f'{filename}: no new drawables entries to add')


if include_appfilter:
    filename = 'appfilter.xml'
    if not compinfos: out.warn(f'{filename}: no compinfos passed')
    else:
        with open(appfilter_files[0], 'r+', encoding='utf-8', newline=blank) as file:
            content = file.read()
            pattern = '</resources>'
            replace = blank
            appfilter_entries = []
            for compinfo in compinfos:
                appfilter_entry = f'<item component="ComponentInfo{{{compinfo}}}" drawable="{name}" />'
                compinfo_pattern = appfilter_entry.replace('$', '\\$')
                if not re.search(compinfo_pattern, content):
                    appfilter_entries.append(appfilter_entry)
                    replace += f'\t{appfilter_entry}\n'
            if appfilter_entries:
                content = re.sub(pattern, replace + pattern, content)
                write(file, content)
                entry = 'entry' if len(compinfos) == 1 else 'entries'
                out.done(f'{filename}: {dry_run_prefix + "added"} {len(compinfos)} {entry}')
                if verbose:
                    out.verb()
                    for entry in appfilter_entries: out.verb(out.add.format(entry))
                    out.verb(pattern)
                    out.verb()
                changes = True
            else: out.warn(f"{filename}: existing entries found")


if include_requests:
    filename = 'requests.yml'
    if not compinfos: out.warn(f'{filename}: no compinfos passed')
    else:
        requests = requests_parser.read(requests_file)
        lines = []
        for compinfo in compinfos:
            if compinfo in requests:
                lines.append(compinfo)
                requests.pop(compinfo)

        lines_count = len(lines)

        if not dry_run: requests_parser.write(requests_file, requests)

        if lines_count > 0:
            entry = 'entry' if lines_count == 1 else 'entries'
            out.done(f'{filename}: {dry_run_prefix + "removed"} {lines_count} {entry}')
            if verbose:
                out.verb()
                for group in lines:
                    for entry in group: out.verb(out.rem.format(entry))
                    out.verb()
            changes = True
        else:
            out.warn(f'{filename}: no entries found to delete')


try:
    if not dry_run:
        if include_appfilter:
            copy(appfilter_files[0], appfilter_files[1])
        if include_drawable:
            copy(drawable_files[0],  drawable_files[1])
    if include_icons:
        message = dry_run_prefix
        message += 'copied' if copy_icons else 'moved'
        if force: message += ' with overwrite'
        formats = ['png', 'svg']
        for format in formats:
            index = formats.index(format)
            filename = f'{name}.{format}'
            source = icons_src_files[index]
            target = icons_dst_files[index]
            folder = 'vectors' if format == 'svg' else 'drawable-nodpi'
            if not exists(source): out.warn(f"{filename}: not found in '{basename(icons_dir)}'")
            elif exists(target): out.fail(f"{filename}: found in '{folder}'")
            else:
                git_arguments += [target]
                diff = compare(source, target) if exists(target) else False
                if diff:
                    out.warn(f'{filename}: source and target icons are the same')
                else:
                    if not dry_run:
                        if copy_icons: copy(source, target)
                        else: move(source, target)
                    out.done(f"{filename}: '{source}' {message} to '{target}'" if verbose else f'{filename}: {message} to {folder}')
                    changes = True


    if not dry_run and git_commit:
        git_command = f'cd {delta_dir} && git'
        git_arguments = ' '.join(git_arguments)
        null = '>NUL 2>NUL' if platform == 'nt' else '>/dev/null 2>&1'
        if execute(f'{git_command} add --dry-run {git_arguments} {null}') == 0: execute(f'cd {delta_dir} && git add {git_arguments}')
        if execute(f'{git_command} commit --dry-run -m "{git_commit}" {null}') == 0:
            execute(f'{git_command} commit -m "{git_commit}" {null}')
            message = ['git: commited']
            commit = get_output(f'{git_command} log -1 --pretty=format:%h', shell=True, encoding='utf-8')
            message += [out.color(code=6, text=commit)]
            if not verbose: message += ['with', get_output(f'{git_command} diff --staged --shortstat HEAD~1', shell=True, encoding='utf-8').strip()]
            out.done(' '.join(message))
            if verbose:
                diff = filter(None, get_output(f'{git_command} diff {"--color=always" if not plain_text else blank} --staged --stat HEAD~1',
                              shell=True, encoding='utf-8').split('\n'))
                for line in diff: out.verb(text=line.strip(), code=out.reset)
            changes = True
        else: out.warn('git: no changes to commit')
    if not changes: out.fail('nothing to do')
    else:
        if dry_run: out.info(f'yay, I can do something!')
        else: out.info(f'yay, I did something!')
except Exception as message:
    out.fail(message)
