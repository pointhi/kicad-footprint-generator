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

    # create fab
    kicad_mod.append(RectChamfer(start=[-2,-2], end=[5,2], layer='F.Fab', width=0.15,
        chamfers=[{'corner': 'topleft',     'size': 1.0}, 
                  {'corner': 'bottomleft',  'size': 0.5},
                  {'corner': 'topright',    'size': 0.5},
                  {'corner': 'bottomright', 'size': 2.5} ]))
                          
    # create silkscreen
    kicad_mod.append(RectChamfer(start=[-2,-2], end=[5,2], layer='F.SilkS', width=0.15, offset=0.15,
        chamfers=[{'corner': 'topleft',     'size': 1.0}, 
                  {'corner': 'bottomleft',  'size': 0.5},
                  {'corner': 'topright',    'size': 0.5},
                  {'corner': 'bottomright', 'size': 2.5} ]))
    # print render tree
    print(kicad_mod.getRenderTree())
    #print(kicad_mod.getCompleteRenderTree())

    # write file
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile('example_footprint.kicad_mod')

    
    
