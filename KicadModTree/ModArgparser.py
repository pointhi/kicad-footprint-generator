'''
kicad-footprint-generator is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

kicad-footprint-generator is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with kicad-footprint-generator. If not, see < http://www.gnu.org/licenses/ >.

(C) 2017 by Thomas Pointhuber, <thomas.pointhuber@gmx.at>
'''

import argparse
import yaml
import csv


class ParserException(Exception):
    def __itruediv__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class ModArgparser(object):
    def __init__(self, footprint_function):
        self._footprint_function = footprint_function
        self._params = {}

    def addParam(self, name, **kwargs):
        self._params[name] = kwargs

    def run(self):
        parser = argparse.ArgumentParser(description='Parse footprint defintion file(s) and create matching footprints')
        parser.add_argument('files', metavar='file', type=str, nargs='+', help='.yml or .csv files which contains data')
        parser.add_argument('-v', '--verbose', help='show some additional information', action='store_true')  # TODO

        # TODO: allow writing into sub dir

        args = parser.parse_args()
        for filepath in args.files:
            print("use file: {0}".format(filepath))
            if filepath.endswith('.yml') or filepath.endswith('.yaml'):
                self._parse_and_execute_yml(filepath)
            elif filepath.endswith('.csv'):
                self._parse_and_execute_csv(filepath)
            else:
                print("unexpected filetype: {0}".format(filepath))

    def _parse_and_execute_yml(self, filepath):
        with open(filepath, 'r') as stream:
            try:
                parsed = yaml.load(stream)
                if parsed is None:
                    print("file is empty!")
                    return

                for footprint in parsed:
                    kwargs = parsed.get(footprint)
                    if 'name' in kwargs:
                        print("ERROR: name is already used for root name!")
                        continue
                    kwargs['name'] = footprint
                    self._execute_script(**kwargs)
            except yaml.YAMLError as exc:
                print(exc)

    def _parse_and_execute_csv(self, filepath):
        with open(filepath, 'r') as stream:
            reader = csv.DictReader(stream, delimiter=';')

            for row in reader:
                trimmed_dict = {}
                for k, v in row.items():
                    trimmed_dict[k.strip()] = v.strip()
                self._execute_script(**trimmed_dict)

    def _execute_script(self, **kwargs):
        parsed_args = {}
        error = False
        for k, v in self._params.items():
            try:
                if k in kwargs:
                    parsed_args[k] = v.get('type', str)(kwargs[k])
                elif v.get('required', False):
                    raise ParserException("parameter expected: {}".format(k))
                else:
                    parsed_args[k] = v.get('type', str)(v.get('default'))
            except (ValueError, ParserException) as e:
                error = True
                print("ERROR: {}".format(e))

        print("  - generate {name}.kicad_mod".format(name=kwargs.get('name', '<anon>')))

        if error:
            return

        self._footprint_function(parsed_args)
