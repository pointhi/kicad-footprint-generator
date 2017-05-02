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


from KicadModTree import *

if __name__ == '__main__':

    footprint_name = "example_footprint"

    # init kicad footprint
    kicad_mod = Footprint(footprint_name)

    # set up list of chamfers for nested rectangles
    test_chamfers = [{'corner': 'topleft', 'size': 1.0}, 
                     {'corner': 'bottomleft', 'size': 0.5},
                     {'corner': 'bottomright', 'size': 2.5}]

    # rectangle without chamfers
    kicad_mod.append(RectLine(start=[-2.5, -1], end=[-0.5, 1], layer='F.Fab', width=0.1))

    # same rectangle chamfered all corners (same size)
    kicad_mod.append(RectLine(start=[0.5,-1], end=[2.5, 1], layer='F.Fab', width=0.1, chamfers=[{'corner': 'all', 'size': 0.5}]))

    # different size chamfer on each corner 
    kicad_mod.append(RectLine(start=[-4,-2], end=[5,2], layer='F.Fab', width=0.1, chamfers=test_chamfers))

    # nested polygon (same X and Y offsets)
    kicad_mod.append(RectLine(start=[-4,-2], end=[5,2], layer='F.SilkS', width=0.12, offset=(0.2, 0.2), chamfers=test_chamfers))

    # nested polygon (different X and Y offsets)
    kicad_mod.append(RectLine(start=[-4,-2], end=[5,2], layer='F.SilkS', width=0.12, offset=(0.4, 0.6), chamfers=test_chamfers))

    # print render tree
    print(kicad_mod.getRenderTree())
    # print(kicad_mod.getCompleteRenderTree())

    # write file
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile('example_footprint.kicad_mod')

