#!/usr/bin/env python3

from os.path import abspath, dirname, realpath


def format_paths():
    cwd = dirname(realpath(__file__))
    root = abspath(f'{cwd}/../..')
    contribs = f'{root}/contribs'
    icons = f'{contribs}/icons'
    return {
        'root': root,
        'scripts': cwd,
        'contribs': contribs,
        'icons': f'{contribs}/icons.yml',
        'requests': f'{contribs}/requests.yml',
        'src': {
            'dir': f'{icons}',
            'svg': f'{icons}/{{}}.svg',
            'png': f'{icons}/{{}}.png'
        },
        'dst': {
            'svg': f'{root}/resources/vectors/{{}}.svg',
            'png': f'{root}/app/src/main/res/drawable-nodpi/{{}}.png'
        },
        'appfilter': [
            f'{root}/app/src/main/assets/appfilter.xml',
            f'{root}/app/src/main/res/xml/appfilter.xml'
        ],
        'drawable': [
            f'{root}/app/src/main/assets/drawable.xml',
            f'{root}/app/src/main/res/xml/drawable.xml'
        ]
    }


paths = format_paths()
