import yaml

from datetime import datetime

from natsort import natsorted as sorted


class CustomDumper(yaml.SafeDumper):
    # https://github.com/yaml/pyyaml/issues/127#issuecomment-525800484
    def write_line_break(self, data=None):
        super().write_line_break(data)
        if len(self.indents) == 1:
            super().write_line_break()

    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow, False)


def unixtime(date):
    formatted = datetime.strptime(str(date), '%Y-%m-%d %H:%M:%S')
    return int(datetime.timestamp(formatted))


def read(path):
    with open(path, 'r+') as file:
        loaded = yaml.safe_load(file)
        return loaded if loaded is not None else {}


def write(path, data):
    with open(path, 'r+') as file:
        sort = lambda x: (x[1]['reqt'], unixtime(x[1]['reql']))
        data = dict(sorted(data.items(), reverse=True, key=lambda x: sort(x)))
        header = (f"# {len(data)} requested apps pending \n"
                  f"# updated {datetime.today().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        dump = yaml.dump(data, Dumper=CustomDumper, allow_unicode=True, sort_keys=False, indent=4)
        file.seek(0)
        file.write(header + dump)
        file.truncate()
