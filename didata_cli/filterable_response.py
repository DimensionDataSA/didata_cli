import json
from tabulate import tabulate
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

VALID_PRINT_TYPES = ('pretty', 'json', 'plain', 'simple', 'grid', 'fancy_grid', 'pipe',
                     'orgtbl', 'rst', 'mediawiki', 'html', 'latex', 'latex_booktabs')


class DiDataCLIFilter(object):
    def __init__(self, filter_string):
        self._raw_filter = filter_string
        self.return_count = None
        self.return_keys = None
        self.parse_filter()

    def parse_filter(self):
        items = self._raw_filter.split('|')
        for item in items:
            (key, value) = item.split(':')
            if key == 'ReturnCount':
                self.return_count = int(value)
            elif key == 'ReturnKeys':
                self.return_keys = value.split(',')
            elif key == 'Where':
                pass


class DiDataCLIFilterableResponse(object):
    def __init__(self):
        self._list = []

    def add(self, item):
        if not isinstance(item, OrderedDict):
            raise TypeError("Item to add for CLIPrint must be an OrderedDict")
        self._list.append(item)

    @staticmethod
    def is_valid_print_type(print_type):
        if print_type not in VALID_PRINT_TYPES:
            return False
        return True

    def is_empty(self):
        if len(self._list) > 0:
            return False
        return True

    def do_filter(self, filter_string):
        cli_filter = DiDataCLIFilter(filter_string)
        if cli_filter.return_count is not None:
            self._list = self._list[0:cli_filter.return_count]
        if cli_filter.return_keys is not None:
            if len(cli_filter.return_keys) == 0:
                pass
            else:
                for item in self._list:
                    # This is hacky for python 3.5
                    keys_to_delete = []
                    for key in item:
                        if key not in cli_filter.return_keys:
                            keys_to_delete.append(key)
                    for key in keys_to_delete:
                        del item[key]

    def to_string(self, print_type, headers=True):
        if not self.is_valid_print_type(print_type):
            raise ValueError("Unknown print type {0}".format(print_type))
        print_function = getattr(self, '_to_' + print_type + '_string')
        return print_function(headers)

    def _to_json_string(self, headers):
        return json.dumps(self._list, indent=4, separators=(',', ': '))

    def _to_pretty_string(self, headers):
        output = ""
        for item in self._list:
            for key in item:
                output = output + "{0}: {1}\n".format(key, item[key])
            output = output + "\n"
        return output[:-2]

    def _to_tabulate(self, name, headers):
        if headers is True:
            return tabulate(self._list, headers='keys', tablefmt=name)
        else:
            return tabulate(self._list, tablefmt=name)

    def _to_plain_string(self, headers):
        return self._to_tabulate('plain', headers)

    def _to_simple_string(self, headers):
        return self._to_tabulate('simple', headers)

    def _to_grid_string(self, headers):
        return self._to_tabulate('grid', headers)

    def _to_fancy_grid_string(self, headers):
        return self._to_tabulate('fancy_grid', headers)

    def _to_pipe_string(self, headers):
        return self._to_tabulate('pipe', headers)

    def _to_orgtbl_string(self, headers):
        return self._to_tabulate('orgtbl', headers)

    def _to_rst_string(self, headers):
        return self._to_tabulate('rst', headers)

    def _to_mediawiki_string(self, headers):
        return self._to_tabulate('mediawiki', headers)

    def _to_html_string(self, headers):
        return self._to_tabulate('html', headers)

    def _to_latex_string(self, headers):
        return self._to_tabulate('latex', headers)

    def _to_latex_booktabs_string(self, headers):
        return self._to_tabulate('latex_booktabs', headers)
