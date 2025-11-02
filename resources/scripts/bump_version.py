#! /usr/bin/env python

import argparse, re

from os.path import join

import semver

from resolve_paths import paths


argparser = argparse.ArgumentParser(description='Bump release version')

argparser.add_argument('-c', '--custom',
                       dest='custom',
                       help='custom version name and code (format: \'name|code\')')
argparser.add_argument('-r', '--release-type',
                       dest='release_type',
                       help='type of release',
                       choices=['beta', 'prod'],
                       default='beta')
argparser.add_argument('-v', '--version-type',
                       dest='version_type',
                       help='bump specific position',
                       choices=['patch', 'minor', 'major'],
                       default='minor')
argparser.add_argument('-e', '--env',
                       dest='env',
                       help='print variables for shell exporting',
                       default=False,
                       action=argparse.BooleanOptionalAction)
argparser.add_argument('-w', '--write',
                       dest='write',
                       help='write to file',
                       default=False,
                       action=argparse.BooleanOptionalAction)
args = argparser.parse_args()


target = join(paths['root'], 'app/build.gradle')

regexp_version_code = re.compile(r'versionCode (\d+)')
regexp_version_name = re.compile(r'versionName "((\d+\.\d+\.\d+)(-beta\.?(\d+))?)"')
is_beta = 'true' if args.release_type == 'beta' else 'false'


def build_version_code(version):
    major = str(version.major)
    minor = str(version.minor).zfill(2)
    patch = str(version.patch)
    beta = '00' if version.prerelease is None else \
           ''.join(filter(str.isdigit, version_name.prerelease)).zfill(2)
    return int(major + minor + patch + beta)


with open(target, 'r+') as file:
    content = file.read()

    if args.custom:
        version_name, version_code = args.custom.split('|')
    else:
        version_name = semver.VersionInfo.parse(re.search(regexp_version_name, content).group(1))

        if not version_name.prerelease:
            match args.version_type:
                case 'major': version_name = version_name.bump_major()
                case 'minor': version_name = version_name.bump_minor()
                case 'patch': version_name = version_name.bump_patch()

        if args.release_type == 'prod':
            if version_name.prerelease:
                version_name = version_name.bump_prerelease(token='beta')
            version_code = build_version_code(version_name)
            version_name = version_name.finalize_version()
        else:
            version_name = version_name.bump_prerelease(token='beta')
            version_code = build_version_code(version_name)

    if not args.env:
        print(f'Name: {version_name}')
        print(f'Code: {version_code}')

    if args.write:
        content = re.sub(regexp_version_code, f'versionCode {version_code}', content)
        content = re.sub(regexp_version_name, f'versionName "{version_name}"', content)
        file.seek(0)
        file.write(content)
        file.truncate()


if args.env:
    print(f'is_beta={is_beta}')
    print(f'filename=delta-v{version_name}')
    print(f'version=v{version_name}')
    print(f'version_code={version_code}')
    print(f'version_name={version_name}')
    print(f'version_next={version_name.bump_minor()}')
