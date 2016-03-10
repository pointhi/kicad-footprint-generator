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

(C) 2016 by Thomas Pointhuber, <thomas.pointhuber@gmx.at>
'''

import time
import re
from string import whitespace as WHITESPACE_CHARACTERS


def formatFloat(val):
    '''
    return well formated float
    '''
    return ('%f' % val).rstrip('0').rstrip('.')


def lispString(string):
    '''
    add quotation marks to string, when it include a white space
    '''
    if type(string) is not str:
        string = str(string)

    for character in string:
        if character in WHITESPACE_CHARACTERS:
            return '"{}"'.format(string)

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

        if token[0]=='"':
            if in_string:
                tokens[-1] += token[1:]
                in_string = False
            else:
                tokens.append(token[1:])
                in_string = True

        elif token[-1]=='"':
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

    # TOOD: remove invalid spaces from qotation (when having brackets inside)

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


def parseTimestamp(timestamp):
    raise NotImplemented()
    return time.time() # TOOD


def formatTimestamp(timestamp=None):
    if not timestamp:
        timestamp = time.time()

    return "{timestamp:X}".format(timestamp=int(timestamp))
