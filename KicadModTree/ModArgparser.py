# KicadModTree is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# KicadModTree is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with kicad-footprint-generator. If not, see < http://www.gnu.org/licenses/ >.
#
# (C) 2017 by Thomas Pointhuber, <thomas.pointhuber@gmx.at>

import sys
import argparse
import csv

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


class ParserException(Exception):
    def __itruediv__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class ModArgparser(object):
    r"""A general data loading class, which allows us to specify parts using .yml or .csv files.

    Using this class allows us to seperate between the implementation of a footprint generator, and the data which
    represents a single footprint. To do so, we need to define which parameters are expected in those data-files.

    To improve the usablity of this class, it is able to do type checks of provided parameters, as well as defining
    default values and do a simple check if a parameter can be considered as required or optional.

    :param footprint_function:
        A function which is called for every footprint we want to generate
    :type footprint_function: ``function reference``

    :Example:

    >>> from KicadModTree import *
    >>> def footprint_gen(args):
    ...    print("create footprint: {}".format(args['name']))
    ...
    >>> parser = ModArgparser(footprint_gen)
    >>> parser.add_parameter("name", type=str, required=True)  # the root node of .yml files is parsed as name
    >>> parser.add_parameter("datasheet", type=str, required=False)
    >>> parser.add_parameter("courtyard", type=float, required=False, default=0.25)
    >>> parser.add_parameter("pincount", type=int, required=True)
    >>> parser.run()  # now run our script which handles the whole part of parsing the files
    """

    def __init__(self, footprint_function):
        self._footprint_function = footprint_function
        self._params = {}

    def add_parameter(self, name, **kwargs):
        r"""Add a parameter to the ModArgparser

        :param name:
            name of the argument
        :param \**kwargs:
            See below
        :type name: ``str``

        :Keyword Arguments:
            * *type* (``type``) --
              type of the argument
            * *required* (``bool``) --
              is the argument required or optional
            * *default* --
              a default value which is used when there is no value defined

        :Example:

        >>> from KicadModTree import *
        >>> def footprint_gen(args):
        ...    print("create footprint: {}".format(args['name']))
        ...
        >>> parser = ModArgparser(footprint_gen)
        >>> parser.add_parameter("name", type=str, required=True)  # the root node of .yml files is parsed as name
        >>> parser.add_parameter("datasheet", type=str, required=False)
        >>> parser.add_parameter("courtyard", type=float, required=False, default=0.25)
        """

        self._params[name] = kwargs

    def run(self):
        r"""Execute the ModArgparser and run all tasks defined via the commandline arguments of this script

        This method parses the commandline arguments to determine which actions to take. Beside of parsing .yml and .csv
        files, it also allows us to output example files.

        >>> from KicadModTree import *
        >>> def footprint_gen(args):
        ...    print("create footprint: {}".format(args['name']))
        ...
        >>> parser = ModArgparser(footprint_gen)
        >>> parser.add_parameter("name", type=str, required=True)  # the root node of .yml files is parsed as name
        >>> parser.run()  # now run our script which handles the whole part of parsing the files
        """

        parser = argparse.ArgumentParser(description='Parse footprint defintion file(s) and create matching footprints')
        parser.add_argument('files', metavar='file', type=str, nargs='*', help='.yml or .csv files which contains data')
        parser.add_argument('-v', '--verbose', help='show some additional information', action='store_true')  # TODO
        parser.add_argument('--print_yml', help='print example .yml file', action='store_true')
        parser.add_argument('--print_csv', help='print example .csv file', action='store_true')

        # TODO: allow writing into sub dir

        args = parser.parse_args()

        if args.print_yml:
            self._print_example_yml()
            return

        if args.print_csv:
            self._print_example_csv()
            return

        if len(args.files) == 0:
            parser.print_help()
            return

        for filepath in args.files:
            print("use file: {0}".format(filepath))
            if filepath.endswith('.yml') or filepath.endswith('.yaml'):
                self._parse_and_execute_yml(filepath)
            elif filepath.endswith('.csv'):
                self._parse_and_execute_csv(filepath)
            else:
                print("unexpected filetype: {0}".format(filepath))

    def _parse_and_execute_yml(self, filepath):
        if not YAML_AVAILABLE:
            print("pyyaml not available!")
            sys.exit(1)

        with open(filepath, 'r') as stream:
            try:
                parsed = yaml.load(stream)  # parse file

                if parsed is None:
                    print("empty file!")
                    return

                for footprint in parsed:
                    kwargs = parsed.get(footprint)

                    # name is a reserved key
                    if 'name' in kwargs:
                        print("ERROR: name is already used for root name!")
                        continue
                    kwargs['name'] = footprint

                    self._execute_script(**kwargs)  # now we can execute the script

            except yaml.YAMLError as exc:
                print(exc)

    def _create_example_data_required(self, **kwargs):
        params = {}
        for k, v in self._params.items():
            if kwargs.get('include_name', False) is False and k == "name":
                continue
            if v.get('required', False):
                params[k] = self._create_example_datapoint(v.get('type', str), v.get('default'))

        return params

    def _create_example_data_full(self, **kwargs):
        params = {}
        for k, v in self._params.items():
            if kwargs.get('include_name', False) is False and k == "name":
                continue
            params[k] = self._create_example_datapoint(v.get('type', str), v.get('default'))

        return params

    def _create_example_datapoint(self, type, default):
        if default:
            return type(default)

        if type is bool:
            return False
        elif type is int:
            return 0
        elif type is float:
            return 0.0
        elif type is str:
            return "some string"
        else:
            return "??"

    def _print_example_yml(self):
        if not YAML_AVAILABLE:
            print("pyyaml not available!")
            sys.exit(1)

        data = {'footprint_required': self._create_example_data_required(),
                'footprint_full': self._create_example_data_full()}
        print(yaml.dump(data, default_flow_style=False))

    def _parse_and_execute_csv(self, filepath):
        with open(filepath, 'r') as stream:
            # dialect = csv.Sniffer().sniff(stream.read(1024))  # check which type of formating the csv file likel has
            # stream.seek(0)

            reader = csv.DictReader(stream, dialect=csv.excel)  # parse file

            for row in reader:
                # we wan't to remove spaces before and after the fields
                kwargs = {}
                for k, v in row.items():
                    kwargs[k.strip()] = v.strip()

                self._execute_script(**kwargs)  # now we can execute the script

    def _print_example_csv(self):
        writer = csv.DictWriter(sys.stdout, fieldnames=self._params.keys())

        writer.writeheader()
        writer.writerow(self._create_example_data_required(include_name=True))
        writer.writerow(self._create_example_data_full(include_name=True))

    def _execute_script(self, **kwargs):
        parsed_args = {}
        error = False

        for k, v in self._params.items():
            try:
                if kwargs.get(k) not in [None, '']:
                    parsed_args[k] = v.get('type', str)(kwargs[k])
                elif v.get('required', False):
                    raise ParserException("parameter expected: {}".format(k))
                else:
                    type = v.get('type', str)
                    if type is bool:
                        parsed_args[k] = type(v.get('default', False))
                    elif type is int:
                        parsed_args[k] = type(v.get('default', 0))
                    elif type is float:
                        parsed_args[k] = type(v.get('default', 0.0))
                    elif type is str:
                        parsed_args[k] = type(v.get('default', ''))
                    else:
                        parsed_args[k] = type(v.get('default'))
            except (ValueError, ParserException) as e:
                error = True
                print("ERROR: {}".format(e))

        print("  - generate {name}.kicad_mod".format(name=kwargs.get('name', '<anon>')))

        if error:
            return

        self._footprint_function(parsed_args)
