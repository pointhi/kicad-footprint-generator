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

Datasheet: http://www.jst-mfg.com/product/pdf/eng/eXH.pdf

"""
pitch = 2.00

pincount = range(2,16)

#Molex part number
part = "53254-{n:02}70"

prefix = "Molex_MicroLatch-{pn}_"
suffix = "{n:02}x{p:.2f}mm_Angled"

drill = 0.8
size = 1.5

#FP description and tags

if __name__ == '__main__':

    for pins in pincount:
        
        pn = part.format(n=pins)

        #generate the name
        fp_name = prefix.format(pn=pn) + suffix.format(n=pins, p=pitch)

        print(fp_name)
        
        footprint = Footprint(fp_name)
        
        description = "Molex Micro-Latch connector, PN:" + pn + ", side entry type, through hole"
        
        #set the FP description
        footprint.setDescription(description)
        
        tags = "conn molex micro latch"
        
        #set the FP tags
        footprint.setTags(tags)

        #calculate fp dimensions
        A = (pins - 1) * pitch
        B = A + 3.1
        C = A + 4
        
        # set general values
        footprint.append(Text(type='reference', text='REF**', at=[A/2,3.6], layer='F.SilkS'))
        #footprint.append(Text(type='user', text='%R', at=[A/2,-3], layer='F.Fab'))
        footprint.append(Text(type='value', text=fp_name, at=[A/2,-7.2], layer='F.Fab'))
        
        
        #connector thickness
        T = 5.75
        
        #corners
        x1 = -2
        x2 = x1 + C
        
        y1 = -6
        y2 = y1 + 7.3
        
        #add simple outline to F.Fab layer
        footprint.append(RectLine(start=[x1,y1],end=[x2,y2],layer='F.Fab'))
        
        #wall-thickness W
        w = 0.45
        
        #offset 
        o = 0.15
        x1 -= o
        y1 -= o
        x2 += o
        y2 += o
        
        
            
        #generate the pads
        footprint.append(PadArray(pincount=pins, x_spacing=pitch, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE, size=size, drill=drill, layers=['*.Cu','*.Mask']))
        
        
        #draw the courtyard
        cy = RectLine(start=[x1,y1],end=[x2,y2],layer='F.CrtYd',width=0.05,offset = 0.5,grid=0.05)
        footprint.append(cy)
        
        #draw the connector outline
        out = [
        {'x': -0.3,'y': 1},
        {'x': -0.5,'y': y2},
        {'x': x1+0.6,'y': y2},
        {'x': x1+0.1,'y': 0.5},
        {'x': x1+0.1,'y': 0},
        {'x': x1,'y': 0},
        {'x': x1,'y': y1},
        {'x': A/2,'y': y1},
        ]
        
        footprint.append(PolygoneLine(polygone=out))
        footprint.append(PolygoneLine(polygone=out,x_mirror=A/2))
        
        #draw the pin tab bits
        for i in range(pins-1):
            x = i * pitch
            tab = [
            {'x': x-0.3,'y': 1},
            {'x': x+0.3,'y': 1},
            {'x': x+0.5,'y': y2},
            {'x': x+pitch-0.5,'y': y2},
            {'x': x+pitch-0.3,'y': 1},
            ]
            
            footprint.append(PolygoneLine(polygone=tab))
            
        #add the final tab line
        x = (pins-1) * pitch
        footprint.append(Line(start=[x - 0.3,1],end=[x+0.3,1]))
        
        #pin-1 marker
        y =  y2 + 0.5
        m = 0.3
        
        pin = [
        {'x': 0,'y': y},
        {'x': -m,'y': y+2*m},
        {'x': m,'y': y+2*m},
        {'x': 0,'y': y},
        ]
        
        footprint.append(PolygoneLine(polygone=pin))
        
        #wall
        wall = [
        {'x': x1+w,'y': y1},
        {'x': x1+w,'y': -2.1},
        {'x': x2-w,'y': -2.1},
        {'x': x2-w,'y': y1},
        ]
        
        footprint.append(PolygoneLine(polygone=wall))
        
        #draw each pin
        for i in range(pins):
            x = i * pitch
            ya = -2.1
            yb = ya - 3.3
            
            pin = [
            {'x': x-0.25,'y': ya},
            {'x': x-0.25,'y': yb + 0.25},
            {'x': x,'y': yb},
            {'x': x+0.25,'y': yb + 0.25},
            {'x': x+0.25,'y': ya},
            ]
            
            footprint.append(PolygoneLine(polygone=pin))
            
            
        
        
        #Add a model
        footprint.append(Model(filename="Connectors_Molex.3dshapes/" + fp_name + ".wrl"))
        
        #filename
        filename = output_dir + fp_name + ".kicad_mod"
        

        file_handler = KicadFileHandler(footprint)
        file_handler.writeFile(filename)
