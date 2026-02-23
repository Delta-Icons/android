#!/usr/bin/env python

from re import compile, sub, search
from argparse import ArgumentParser, BooleanOptionalAction

from os.path import basename, join, relpath

from semver import VersionInfo

from shared import paths


PATH = join(paths['root'], 'app/build.gradle')

def create_parser():
    parser = ArgumentParser()

    parser.add_argument('-c', '--custom',
                        dest='custom',
                        help='custom version name and code (format: \'name|code\')')
    parser.add_argument('-r', '--release',
                        dest='release',
                        help='bump specific position',
                        choices=['beta', 'promote', 'patch', 'minor', 'major'],
                        default='beta')
    parser.add_argument('-e', '--env',
                        dest='env',
                        help='print variables for shell exporting',
                        default=False,
                        action=BooleanOptionalAction)
    parser.add_argument('-i',
                        dest='input',
                        metavar='PATH',
                        help=f"path to {basename(PATH)} to process (default: '{relpath(PATH)}')",
                        default=PATH)
    parser.add_argument('-w', '--write',
                        dest='write',
                        help='write to file',
                        default=False,
                        action=BooleanOptionalAction)
    return parser


def bump_version():

    regexp_version_code = compile(r'versionCode (\d+)')
    regexp_version_name = compile(r'versionName "((\d+\.\d+\.\d+)(-beta\.?(\d+))?)"')
    is_beta = 'true' if args.release == 'beta' else 'false'

    def build_version_code(version):
        major = str(version.major)
        minor = str(version.minor).zfill(2)
        patch = str(version.patch)
        beta = '00' if version.prerelease is None else \
            ''.join(filter(str.isdigit, version_name.prerelease)).zfill(2)
        return int(major + minor + patch + beta)

    with open(args.input, 'r+') as file:
        content = file.read()

        if args.custom:
            version_name, version_code = args.custom.split('|')
        else:
            version_code = search(regexp_version_code, content).group(1)
            version_name = VersionInfo.parse(search(regexp_version_name, content).group(1))

            if args.release == 'promote':
                if version_name.prerelease:
                    version_name = version_name.bump_prerelease(token='beta')
                    version_code = build_version_code(version_name)
                version_name = version_name.finalize_version()

            else:
                match args.release:
                    case 'major': version_name = version_name.bump_major()
                    case 'minor': version_name = version_name.bump_minor()
                    case 'patch': version_name = version_name.bump_patch()
                    case 'beta':
                        if not version_name.prerelease: 
                            version_name = version_name.bump_minor()
                        version_name = version_name.bump_prerelease(token='beta')
                
                version_code = build_version_code(version_name)
        
            if args.env:
                print(f'is_beta={is_beta}')
                print(f'version=v{version_name}')
                print(f'version_code={version_code}')
                print(f'version_name={version_name}')
                print(f'version_next={version_name.bump_minor()}')
            else:
                print(f'Name: {version_name}')
                print(f'Code: {version_code}')

            if args.write:
                content = sub(regexp_version_code, f'versionCode {version_code}', content)
                content = sub(regexp_version_name, f'versionName "{version_name}"', content)
                file.seek(0)
                file.write(content)
                file.truncate()


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    bump_version()
