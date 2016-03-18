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
sys.path.append(os.path.join(sys.path[0],".."))
#sys.path.append('../..') # enable package import from parent directory

from KicadModTree import *
from KicadModTree.nodes.specialized.PadArray import PadArray

if __name__ == '__main__':
    footprint_name = "example_footprint"

    # init kicad footprint
    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription("A example footprint")
    kicad_mod.setTags("example")

    # set general values
    kicad_mod.append(Text(type='reference', text='REF**', at=[0,-3], layer='F.SilkS'))
    kicad_mod.append(Text(type='value', text=footprint_name, at=[1.5,3], layer='F.Fab'))

    # create silscreen
    kicad_mod.append(RectLine(start=[-2,-2], end=[5,2], layer='F.SilkS', width=0.15))

    # create courtyard
    kicad_mod.append(RectLine(start=[-2.25,-2.25], end=[5.25,2.25], layer='F.CrtYd', width=0.05, offset=2))

    # create pads
    kicad_mod.append(Pad(number=7, type=Pad.TYPE_THT, shape=Pad.SHAPE_RECT, at=[0,0], size=[2,2], drill=1.2, layers=['*.Cu', '*.Mask', 'F.SilkS']))
    kicad_mod.append(Pad(number=22, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE, at=[3,0], size=[2,2], drill=1.2, layers=['*.Cu', '*.Mask', 'F.SilkS']))
    
    kicad_mod.append(Pad(number=12, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, at=[3,0], size=[2,2], drill=1.2, layers=['*.Cu', '*.Mask', 'F.SilkS']))

    # add model
    kicad_mod.append(Model(filename="example.3dshapes/example_footprint.wrl"
                          ,at=[0,0,0]
                          ,scale=[1,1,1]
                          ,rotate=[0,0,0]))
    
    kicad_mod.append(PadArray(pincount=10,spacing=[1,-1],center=[0,0], initial=5, increment=2, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, size=[1,2], layers=["*.Cu"]))
                          
    # output kicad model
    #print(kicad_mod)

    # print render tree
    #print(kicad_mod.getRenderTree())
    #print(kicad_mod.getCompleteRenderTree())

    # write file
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile('example_footprint.kicad_mod')

    
    