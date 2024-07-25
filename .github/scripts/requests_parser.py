#!/usr/bin/env python3

from datetime import datetime

import yaml

from natsort import natsorted as sorted


class CustomDumper(yaml.SafeDumper):
    # https://github.com/yaml/pyyaml/issues/127#issuecomment-525800484
    def write_line_break(self, data=None):
        super().write_line_break(data)
        if len(self.indents) == 1:
            super().write_line_break()

    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow, False)


def read(path):
    with open(path, 'r+') as file:
        loaded = yaml.safe_load(file)
        return loaded if loaded is not None else {}


def write(path, data):
    with open(path, 'r+') as file:
        data = dict(sorted(data.items(),
                           # sort by number of requests, then by last request time
                           key=lambda k: (k[1]['reqt'], k[1]['reql']),
                           # reverse array to set new requests at top of the list
                           reverse=True))
        # header message with total number of requested icons and last time update
        header = (f"# {len(data)} requested apps pending \n"
                  f"# updated {datetime.today().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        dump = yaml.dump(data, Dumper=CustomDumper, allow_unicode=True, indent=4, sort_keys=False)
        file.seek(0)
        file.write(header + dump)
        file.truncate()
