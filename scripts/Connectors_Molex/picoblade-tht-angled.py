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

output_dir = os.getcwd()

#if specified as an argument, extract the target directory for output footprints
if len(sys.argv) > 1:
    out_dir = sys.argv[1]
    
    if os.path.isabs(out_dir) and os.path.isdir(out_dir):
        output_dir = out_dir
    else:
        out_dir = os.path.join(os.getcwd(),out_dir)
        if os.path.isdir(out_dir):
            output_dir = out_dir

if output_dir and not output_dir.endswith(os.sep):
    output_dir += os.sep
        
#import KicadModTree files
sys.path.append("..\\..")
from KicadModTree import *
from KicadModTree.nodes.specialized.PadArray import PadArray

"""
footprint specific details to go here

Molex Picoblade THT side-entry connectors
http://www.molex.com/pdm_docs/sd/530480610_sd.pdf
"""

pitch = 1.25

#pincounts
pincount = range(2,16)

#Molex part number
#with plastic PCB retainer, 
part_code = "53048-{n:02}10" #n = number of circuits

part_name = "Molex_PicoBlade_{part}_{n:02}x{p:.2f}mm_Angled"

#FP description and tags
description = "Molex PicoBlade, single row, side entry type, through hole, PN:{pn}"
tags = "connector molex picoblade"

drill = 0.5
size = 0.85

if __name__ == '__main__':

    for pins in pincount:
        
        pn = part_code.format(n=pins)
        
        #generate the name
        fp_name = part_name.format(n=pins, p=pitch, part=pn)
        footprint = Footprint(fp_name)
        
        print(fp_name)
        
        #set the FP description
        footprint.setDescription(description.format(pn=pn)) 
        
        #set the FP tags
        footprint.setTags(tags)
        
        #calculate fp dimensions
        
        B = (pins - 1) * pitch
        C = B + 1.8
        A = B + 3
        
        #connector width
        W = 5.5
        
        #corner positions
        x1 = (B-A) / 2
        x2 = x1 + A
        
        y1 = -1.05
        y2 = y1 + W

        # set general values
        footprint.append(Text(type='reference', text='REF**', at=[B/2,-2.25], layer='F.SilkS'))
        footprint.append(Text(type='value', text=fp_name, at=[B/2,5.75], layer='F.Fab'))
            
        # refdes
        #footprint.append(Text(type='user', text='%R', at=[B/2,3], layer='F.Fab'))
            
        # generate the pads
        footprint.append(PadArray(start=[0,0], pincount=pins, x_spacing=pitch, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE, size=size, drill=drill, layers=Pad.LAYERS_THT))
        
        # distance from pins in y dir
        P = 0.75
        
        # thickness of end bosses
        T = 0.85
        
        #pin-1 marker
        o = 0.4
        pin1 = [
        {'x': x1 + T + o,'y': -P - o},
        {'x': x1 + T + o,'y': y1 - o},
        {'x': x1 + T + o - 0.5,'y': y1 - o},
        ]
        
        footprint.append(PolygoneLine(polygone=pin1))
        footprint.append(PolygoneLine(polygone=pin1,layer='F.Fab'))
        
        #component outline (configurable offset)
        def outline(off=0):
            
            
            out = [
            {'x': B/2, 'y': -P - off},
            {'x': x1 + T + off, 'y': -P  - off},
            {'x': x1 + T + off, 'y': y1 - off},
            {'x': x1 - off, 'y': y1 - off},
            {'x': x1 - off, 'y': y2 + off},
            {'x': B/2, 'y': y2 + off},
            ]
            
            return out
        
        #courtyard
        footprint.append(PolygoneLine(polygone=outline(off=0.5),layer='F.CrtYd',width=0.05,grid=0.05))
        footprint.append(PolygoneLine(polygone=outline(off=0.5),layer='F.CrtYd',width=0.05,x_mirror=B/2,grid=0.05))
        
        #outline F.Fab
        footprint.append(PolygoneLine(polygone=outline(),layer='F.Fab'))
        footprint.append(PolygoneLine(polygone=outline(),layer='F.Fab',x_mirror=B/2))
        
        #outline F.SilkS
        footprint.append(PolygoneLine(polygone=outline(off=0.15)))
        footprint.append(PolygoneLine(polygone=outline(off=0.15),x_mirror=B/2))
        
        #pin-1 marker
        
        #Add a model
        footprint.append(Model(filename="Connectors_Molex.3dshapes/" + fp_name + ".wrl"))
        
        #filename
        filename = output_dir + fp_name + ".kicad_mod"

        file_handler = KicadFileHandler(footprint)
        file_handler.writeFile(filename)
