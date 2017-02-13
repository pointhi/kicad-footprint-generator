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

Molex Mini Fit JR side-entry dual-row connectors
e.g. http://www.molex.com/pdm_docs/sd/768250010_sd.pdf
"""

pitch = 5.7

#pins per row
pincount = [1, 2, 3, 4, 5, 6]

#Molex part number
codes = [
"76825-00{n:02}",
"172064-00{n:02}",
"172064-10{n:02}"
]
part_code = "76829-00{n:02}" #n = number of circuits per row

part_name = "Molex_MegaFit_2x{n:02}x{p:.2f}mm_Angled"

drill = 1.8
size = 3.75

row = 5.5

#FP description and tags

if __name__ == '__main__':

    for pins in pincount:
        
        pn = [code.format(n=pins*2) for code in codes]
        
        #generate the name
        fp_name = part_name.format(n=pins, p=pitch)
        footprint = Footprint(fp_name)
        
        print(fp_name)
        
        description = "Molex MegaFit, dual row, side entry type, through hole"
        
        #set the FP description
        footprint.setDescription(description)
        
        tags = "connector molex mega-fit " + " ".join(pn)
        
        #set the FP tags
        footprint.setTags(tags)
        
        #calculate fp dimensions
        #http://www.molex.com/pdm_docs/sd/768250010_sd.pdf
        
        #connector length
        if pins == 1:
            A = 8.35
        else:
            A = pins * pitch + 0.65
        
        if pins == 1 or pins == 2:
            B = 0
        else:
            B = A - 6.35
        
        #pin centers
        P = (pins - 1) * pitch
        
        #corner positions for plastic housing outline
        
        x1 = -(A-P)/2
        x2 = x1 + A
        
        y2 = -1.1
        y1 = y2 - 14.8

        # set general values
        footprint.append(Text(type='reference', text='REF**', at=[P/2,9], layer='F.SilkS'))
        footprint.append(Text(type='value', text=fp_name, at=[P/2,10.5], layer='F.Fab'))
            
        #generate the pads
        footprint.append(PadArray(pincount=pins, x_spacing=pitch, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE, size=size, drill=drill, layers=['*.Cu','*.Mask']))
        footprint.append(PadArray(pincount=pins, initial=pins+1, start=[0, row], x_spacing=pitch, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE, size=size, drill=drill, layers=['*.Cu','*.Mask']))
        
        #add PCB locators
        r_loc = 3.00
        y_loc = -7.3
        
        #two locators
        if pins > 2:
            lx1 = P/2 - B/2
            lx2 = P/2 + B/2
            
            footprint.append(Pad(at=[lx1, y_loc],type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE, size=r_loc,drill=r_loc, layers=["*.Cu"]))
            footprint.append(Pad(at=[lx2, y_loc],type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE, size=r_loc,drill=r_loc, layers=["*.Cu"]))
            
            footprint.append(Circle(center=[lx1, y_loc],radius=r_loc/2+0.1))
            footprint.append(Circle(center=[lx2, y_loc],radius=r_loc/2+0.1))
        else:
            #one locator
            footprint.append(Pad(at=[P/2,y_loc],type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE, size=r_loc, drill=r_loc, layers=["*.Cu"]))
            
            footprint.append(Circle(center=[P/2,y_loc], radius=r_loc/2+0.1))
            
        #draw the outline of the shape
        footprint.append(RectLine(start=[x1,y1],end=[x2,y2],layer='F.Fab'))
        
        off = 0.15
        outline = [
        {'x': P/2,'y': y1-off},
        {'x': x1-off,'y': y1-off},
        {'x': x1-off,'y': y2+off},
        {'x': -2.5,'y': y2+off},
        ]
        
        footprint.append(PolygoneLine(polygone=outline))
        footprint.append(PolygoneLine(polygone=outline,x_mirror=P/2))
        
        #draw lines between each pin
        for i in range(pins-1):
            xa = i * pitch + size / 2 + 0.3
            xb = (i+1) * pitch - size / 2 - 0.3
            
            footprint.append(Line(start=[xa,y2+off],end=[xb,y2+off]))
        
        #draw the pins!
        o = size/2 + 0.3
        w = 0.3
        for i in range(pins):
            x = i * pitch
            ya = o
            yb = row - o
            footprint.append(Line(start=[x-w,ya],end=[x-w,yb]))
            footprint.append(Line(start=[x+w,ya],end=[x+w,yb]))
         
        #pin-1 marker
        x =  -2.5
        m = 0.3
        
        pin = [
        {'x': x,'y': 0},
        {'x': x-2*m,'y': +m},
        {'x': x-2*m,'y': -m},
        {'x': x,'y': 0},
        ]
        
        footprint.append(PolygoneLine(polygone=pin))
            
        #draw the courtyard
        footprint.append(RectLine(start=[x1,y1],end=[x2,row+size/2], width=0.05, layer='F.CrtYd', offset=0.5, grid=0.05))
        
        #Add a model
        footprint.append(Model(filename="Connectors_Molex.3dshapes/" + fp_name + ".wrl"))
        
        #filename
        filename = output_dir + fp_name + ".kicad_mod"

        file_handler = KicadFileHandler(footprint)
        file_handler.writeFile(filename)
