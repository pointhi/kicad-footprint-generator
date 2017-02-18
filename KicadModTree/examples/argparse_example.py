#!/usr/bin/env python

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
'''

import sys
import os

sys.path.append(os.path.join(sys.path[0], "../.."))  # enable package import from parent directory

from KicadModTree import *  # NOQA


def example_footprint(args):
    print("now we can create a footprint using the following parameters:")
    print(args)


if __name__ == '__main__':
    parser = ModArgparser(example_footprint)
    parser.addParam("name", type=str, required=True)  # the root node of .yml files is parsed as name
    parser.addParam("datasheet", type=str, required=False)
    parser.addParam("courtjard", type=float, required=False, default=0.25)
    parser.addParam("diameter", type=float, required=True)
    parser.addParam("pad_length", type=float, required=True)
    parser.addParam("pad_width", type=float, required=True)

    parser.run()  # now run our script which handles the whole part of parsing the files
