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

Molex Picoblade THT top-entry connectors
http://www.molex.com/pdm_docs/sd/530470610_sd.pdf
"""

pitch = 1.25

#pincounts
pincount = range(2,16)

#Molex part number
#with plastic PCB retainer, 
part_code = "53047-{n:02}10" #n = number of circuits

part_name = "Molex_PicoBlade_{part}_{n:02}x{p:.2f}mm_Straight"

#FP description and tags
description = "Molex PicoBlade, single row, top entry type, through hole, PN:{pn}"
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
        
        A = (pins - 1) * pitch
        B = A + 1.8
        C = A + 3
        
        #connector width
        W = 3.2
        
        #side thickness
        T = 0.4
        
        #corner positions
        x1 = (A - C) / 2
        x2 = x1 + C
        
        y2 = 0.725 + T
        y1 = y2 - W

        # set general values
        footprint.append(Text(type='reference', text='REF**', at=[A/2,2.5], layer='F.SilkS'))
        footprint.append(Text(type='value', text=fp_name, at=[A/2,-3.25], layer='F.Fab'))
            
        # add ref-des
        #footprint.append(Text(type='user',text='%R', at=[A/2,-1.25],layer='F.Fab'))
            
        # generate the pads
        footprint.append(PadArray(start=[0,0], pincount=pins, x_spacing=pitch, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE, size=size, drill=drill, layers=Pad.LAYERS_THT))
        
        # courtyard
        footprint.append(RectLine(start=[x1,y1],end=[x2,y2],layer='F.CrtYd',width=0.05,grid=0.05,offset=0.5))
        
        # outline on Fab
        footprint.append(RectLine(start=[x1,y1],end=[x2,y2],layer='F.Fab'))
        
        footprint.append(Circle(center=[x1+T,y2-T],radius=0.2,layer='F.Fab'))
        
        # outline on SilkScreen
        footprint.append(RectLine(start=[x1,y1],end=[x2,y2],offset=0.15))
        
        inline = [
        {'x': A/2,'y': y2 - T},
        {'x': x1 + T,'y': y2 - T},
        {'x': x1 + T,'y': 0},
        {'x': x1 + T/2,'y': 0},
        {'x': x1 + T/2,'y': -2*T},
        {'x': x1 + T,'y': -2*T},
        {'x': x1 + T,'y': y1 + T},
        {'x': A/2,'y': y1 + T},
        ]
        
        footprint.append(PolygoneLine(polygone=inline))
        footprint.append(PolygoneLine(polygone=inline,x_mirror=A/2))
                
        #pin-1 mark
        
        L = 1
        footprint.append(Line(start=[x1-0.4,y2+0.4],end=[x1-0.4,y2+0.4-L]))
        footprint.append(Line(start=[x1-0.4,y2+0.4],end=[x1-0.4+L,y2+0.4]))
        """
        #add PCB locators
        loc = 3.00
        offset = -0.33
        
        lx1 = P/2 - C/2
        lx2 = P/2 + C/2
        
        footprint.append(Pad(at=[lx1, row - offset],type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE, size=loc,drill=loc, layers=["*.Cu"]))
        footprint.append(Pad(at=[lx2, row - offset],type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE, size=loc,drill=loc, layers=["*.Cu"]))
        
        footprint.append(Circle(center=[lx1, row-offset],radius=loc/2+0.1))
        footprint.append(Circle(center=[lx2, row-offset],radius=loc/2+0.1))
        
        #draw the outline of the shape
        footprint.append(RectLine(start=[x1,y1],end=[x2,y2],layer='F.Fab'))
        
        #draw the outline of the tab
        footprint.append(PolygoneLine(polygone=[
            {'x': P/2 - tab_l/2,'y': y2},
            {'x': P/2 - tab_l/2,'y': y2 + tab_w},
            {'x': P/2 + tab_l/2,'y': y2 + tab_w},
            {'x': P/2 + tab_l/2,'y': y2},
        ], layer='F.Fab'))
        
        
        #draw the outline of the connector on the silkscreen
        off = 0.15
        outline = [
        {'x': P/2,'y': y1-off},
        {'x': x1-off,'y': y1-off},
        {'x': x1-off,'y': y2+off},
        {'x': P/2 - tab_l/2 - off,'y': y2+off},
        {'x': P/2 - tab_l/2 - off,'y': y2 + off + tab_w},
        {'x': P/2, 'y': y2 + off + tab_w},
        ]
        
        footprint.append(PolygoneLine(polygone=outline))
        footprint.append(PolygoneLine(polygone=outline, x_mirror=P/2))
        
        #draw outline around the PCB locators
        #arc distance from pin            
        arc = 1.25 * (B/2 - C/2)
            
        footprint.append(Arc(center=[lx1,row-offset],start=[lx1,row-offset+arc],angle=180))
        footprint.append(Arc(center=[lx2,row-offset],start=[lx2,row-offset-arc],angle=180))
        
        footprint.append(Line(start=[lx1,row-offset-arc],end=[x1-off,row-offset-arc]))
        footprint.append(Line(start=[lx1,row-offset+arc],end=[x1-off,row-offset+arc]))
        
        footprint.append(Line(start=[lx2,row-offset-arc],end=[x2+off,row-offset-arc]))
        footprint.append(Line(start=[lx2,row-offset+arc],end=[x2+off,row-offset+arc]))
        
        #draw square around each pin
        for i in range(pins):
            for j in range(2):
                x = i * pitch
                y = j * row
                s = 0.4 * pitch
                footprint.append(RectLine(start=[x-s,y-s],end=[x+s,y+s]))
        
        #pin-1 marker
        x =  -(A-P)/2 - 0.5
        m = 0.3
        
        pin = [
        {'x': x,'y': 0},
        {'x': x-2*m,'y': +m},
        {'x': x-2*m,'y': -m},
        {'x': x,'y': 0},
        ]
        
        footprint.append(PolygoneLine(polygone=pin))
            
        #draw the courtyard
        footprint.append(RectLine(start=[P/2-B/2,y1],end=[P/2+B/2,y2 + tab_w], width=0.05, layer='F.CrtYd', offset=0.5, grid=0.05))
        
        """
        #Add a model
        footprint.append(Model(filename="Connectors_Molex.3dshapes/" + fp_name + ".wrl"))
        
        #filename
        filename = output_dir + fp_name + ".kicad_mod"

        file_handler = KicadFileHandler(footprint)
        file_handler.writeFile(filename)
