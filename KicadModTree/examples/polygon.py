#!/usr/bin/env python

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
# (C) 2016 by Thomas Pointhuber, <thomas.pointhuber@gmx.at>

import sys
import os

sys.path.append(os.path.join(sys.path[0], "../.."))  # enable package import from parent directory

from KicadModTree import *  # NOQA


if __name__ == '__main__':
    footprint_name = "example_footprint"

    # init kicad footprint
    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription("A example footprint")
    kicad_mod.setTags("example")

    # set general values
    kicad_mod.append(Text(type='reference', text='REF**', at=[0, -3], layer='F.SilkS'))
    kicad_mod.append(Text(type='value', text=footprint_name, at=[1.5, 3], layer='F.Fab'))

    # create polygon
    kicad_mod.append(Polygon(nodes=[[-2, 0], [0, -2], [4, 0], [0, 2], [-2, 0], [0, -2], [4, 0], [0, 2]],
                             layer='F.SilkS'))

    # print render tree
    print(kicad_mod.getCompleteRenderTree())

    # write file
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile('example_footprint.kicad_mod')
