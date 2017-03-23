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
# (C) 2017 by @SchrodingersGat
# (C) 2017 by Thomas Pointhuber, <thomas.pointhuber@gmx.at>

import sys
sys.path.append('../..')  # enable package import from parent directory

from KicadModTree import *  # NOQA

if __name__ == '__main__':
    footprint_name = "pad_array_footprint"

    # Init kicad footprint
    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription("An example footprint")
    kicad_mod.setTags("example")

    # Set general values
    kicad_mod.append(Text(type='reference', text='REF**', at=[0, -3], layer='F.SilkS'))
    kicad_mod.append(Text(type='value', text=footprint_name, at=[1.5, 3], layer='F.Fab'))

    # Add model
    kicad_mod.append(Model(filename="example.3dshapes/example_footprint.wrl",
                           at=[0, 0, 0],
                           scale=[1, 1, 1],
                           rotate=[0, 0, 0]))

    # Create a pad array with a large horizontal spacing, and a smaller vertical spacing
    # centered at the origin
    pa = PadArray(pincount=10,
                  spacing=[2.54, -0.2],
                  center=[0, 0],
                  initial=5,
                  increment=2,
                  type=Pad.TYPE_SMT,
                  shape=Pad.SHAPE_RECT,
                  size=[1, 2],
                  layers=Pad.LAYERS_SMT)

    kicad_mod.append(pa)

    # Calculate the border of the pad array
    border = pa.calculateOutline()

    # Create a courtyard around the pad array
    kicad_mod.append(RectLine(start=border['min'], end=border['max'], layer='F.Fab', width=0.05, offset=0.5))

    # Write file
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile('example_footprint.kicad_mod')
