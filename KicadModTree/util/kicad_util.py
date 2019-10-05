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
# (C) 2016-2018 by Thomas Pointhuber, <thomas.pointhuber@gmx.at>

import time
import re


def formatFloat(val):
    '''
    return well formated float
    '''
    result = ('%f' % val).rstrip('0').rstrip('.')
    if result == '-0':
        result = '0'
    return result


def lispString(string):
    '''
    add quotation marks to string, when it include a white space or is empty
    '''
    if type(string) is not str:
        string = str(string)

    if len(string) == 0 or re.match(".*\s.*", string):
        return '"{}"'.format(string.replace('"', '\\"'))  # escape text

    return string


def lispTokenizer(input):
    '''
    Convert a string of characters into a list of tokens.
    '''
    input = input.replace('(', ' ( ').replace(')', ' ) ')

    # split input, including whitespaces
    base_tokens = re.split(r'(\s+)', input)

    tokens = []
    in_string = False

    for token in base_tokens:
        if not in_string and token.isspace():
            continue

        if len(token) == 0:
            continue

        if token[0] == '"':
            if in_string:
                tokens[-1] += token[1:]
                in_string = False
            else:
                tokens.append(token[1:])
                in_string = True

        elif token[-1] == '"':
            if in_string:
                tokens[-1] += token[:-1]
                in_string = False
            else:
                tokens.append(token[:-1])
                in_string = True

        else:
            if in_string:
                tokens[-1] += token
            else:
                tokens.append(token)

    if in_string:
        raise RuntimeError("missing closing quotation mark")

    # TOOD: remove invalid spaces from quotation (when having brackets inside)

    return tokens


def parseLispString(input):
    syntax_tree = []
    current_node = syntax_tree
    scope = [syntax_tree]

    for token in lispTokenizer(input):
        if token == "(":
            scope.append([])
            current_node.append(scope[-1])
            current_node = scope[-1]

        elif token == ")":
            if len(scope) <= 1:
                raise RuntimeError("missing opening brackets")

            scope.pop()
            current_node = scope[-1]

        else:
            current_node.append(token)

    if len(scope) > 1:
        raise RuntimeError("missing closing brackets")

    if len(syntax_tree) == 1:
        syntax_tree = syntax_tree[0]

    return syntax_tree


class SexprSerializer(object):
    '''
    Converts a nested python list into a sexpr syntax which can be parsed by KiCad
    '''

    NEW_LINE = object

    def __init__(self, sexpr):
        '''
        :param sexpr: A list of lists and primitive values representing the file
        '''
        self.sexpr = sexpr

    def primitive_to_string(self, primitive):
        pType = type(primitive)
        if pType is int:
            return str(primitive)
        elif pType is float:
            return formatFloat(primitive)
        elif pType is str:
            return lispString(primitive)
        else:
            raise RuntimeError("unexpected type: {}".format(pType))

    def sexpr_to_string(self, sexpr, prefix=None):
        if prefix is None:
            prefix = ""

        serial_string = "("

        # see: https://stackoverflow.com/questions/3190706/nonlocal-keyword-in-python-2-x
        loop_ctrl = {'first': True, 'indentation': False}

        def get_separator():
            if loop_ctrl['first']:
                loop_ctrl['first'] = False
                return_str = ""
            else:
                return_str = " "

            if loop_ctrl['indentation']:
                return_str += " "
                loop_ctrl['indentation'] = False

            return return_str

        for attr in sexpr:
            if isinstance(attr, (tuple, list)):
                return_string = self.sexpr_to_string(attr, prefix + " ")

                if loop_ctrl['indentation']:
                    return_string = return_string.replace('\n', '\n ')
                serial_string += get_separator()

                serial_string += return_string
            elif attr == SexprSerializer.NEW_LINE:
                serial_string += "\n"
                serial_string += prefix
                loop_ctrl['indentation'] = True
            else:
                serial_string += get_separator()
                serial_string += self.primitive_to_string(attr)

        serial_string += ")"
        return serial_string

    def __str__(self):
        '''
        :return: A string which respresents the sexpr
        '''
        return self.sexpr_to_string(self.sexpr)


def parseTimestamp(timestamp):
    raise NotImplemented()
    return time.time()  # TOOD


def formatTimestamp(timestamp=None):
    if timestamp is None:
        timestamp = time.time()

    return "{timestamp:X}".format(timestamp=int(timestamp))
