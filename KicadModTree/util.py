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
