#! /usr/bin/env python

import argparse, re

from os.path import join

from resolve_paths import paths


argparser = argparse.ArgumentParser(description='Bump release version')
argparser.add_argument('-t', '--type',
                       dest='type',
                       help='type of release [beta|prod]',
                       default='beta')
argparser.add_argument('-p', '--print',
                       dest='print',
                       help='print variables for shell exporting',
                       default=False,
                       action=argparse.BooleanOptionalAction)
args = argparser.parse_args()


target = join(paths['root'], 'app/build.gradle')

regexp_version_code = re.compile('versionCode (\d+)')
regexp_version_name = re.compile('versionName "((\d+\.\d+\.\d+)(-beta(\d+))?)"')
is_beta = 'true' if args.type == 'beta' else 'false'

with open(target, 'r+') as file:

    content = file.read()
    latest_version = re.search(regexp_version_name, content)

    full_version = latest_version.group(1)
    base_version = latest_version.group(2)
    beta_version = str(int(latest_version.group(4) if latest_version.group(4) else '-1') + 1)
    build_number = str(int(re.search(regexp_version_code, content).group(1)[-3:]) + 1)

    if args.type == 'prod':
        if not 'beta' in full_version:
            base_version = list(map(int, base_version.split('.')))
            base_version[2] += 1
            for n in range(2):
                if base_version[2-n] > 9:
                    base_version[2-n] = 0
                    base_version[1-n] += 1
            new_version = '.'.join(str(x) for x in base_version)
            build_number = '0'
        else:
            new_version = base_version
        version_code = new_version.replace('.', '') + build_number.rjust(3, '0')
        version_name = new_version
    else:
        base_version = list(map(int, base_version.split('.')))
        if not 'beta' in full_version:
            build_number = '0'
            base_version[2] += 1
        for n in range(2):
            if base_version[2-n] > 9:
                base_version[2-n] = 0
                base_version[1-n] += 1
        new_version = '.'.join(str(x) for x in base_version)
        version_code = new_version.replace('.', '') + build_number.rjust(3, '0')
        version_name = new_version + '-beta' + beta_version

    content = re.sub(regexp_version_code, f'versionCode {version_code}', content)
    content = re.sub(regexp_version_name, f'versionName "{version_name}"', content)

    file.seek(0)
    file.write(content)
    file.truncate()

if args.print:
    print(f'is_beta={is_beta}')
    print(f'filename=delta-v{version_name}')
    print(f'version=v{version_name}')
    print(f'version_code={version_code}')
    print(f'version_name={version_name}')
