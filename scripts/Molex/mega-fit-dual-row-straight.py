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

Molex Mini Fit JR top-entry dual-row connectors
e.g. http://www.molex.com/pdm_docs/sd/039288100_sd.pdf
"""

pitch = 5.7

#pins per row
pincount = [1, 2, 3, 4, 5, 6]

#Molex part number
#with plastic PCB retainer, 
part_code = "76829-00{n:02}" #n = number of circuits per row

part_name = "Molex_MegaFit_2x{n:02}x{p:.2f}mm_Straight"

drill = 1.8
size = 3.75

row = 5.7

#FP description and tags

if __name__ == '__main__':

    for pins in pincount:
        
        pn = part_code.format(n=pins*2)
        
        #generate the name
        fp_name = part_name.format(n=pins, p=pitch, part=pn)
        footprint = Footprint(fp_name)
        
        print(fp_name)
        
        description = "Molex MegaFit, dual row, top entry type, through hole"
        
        #set the FP description
        footprint.setDescription(description)
        
        tags = "connector molex mega-fit"
        
        #set the FP tags
        footprint.setTags(tags)
        
        #calculate fp dimensions
        
        #connector length
        if pins == 1:
            A = 8.35
        else:
            A = pins * pitch + 0.65
        
        B = A + 7.05
        
        #pin centers
        P = (pins - 1) * pitch
        
        #plasic pin-lock centre-distance
        C = A + 4
        
        #connector width
        W = 12.48
        
        #corner positions
        x1 = -(A-P)/2
        x2 = x1 + A
        
        y_off = 0.3
        
        y1 = -(W-row) / 2 - 0.2 + y_off
        y2 = y1 + W + 0.1
        
        #tab length
        tab_l = 3.4
        #tab width
        tab_w = 1.55

        # set general values
        footprint.append(Text(type='reference', text='REF**', at=[P/2,12], layer='F.SilkS'))
        footprint.append(Text(type='value', text=fp_name, at=[P/2,-4.7], layer='F.Fab'))
            
        #generate the pads
        footprint.append(PadArray(pincount=pins, x_spacing=pitch, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE, size=size, drill=drill, layers=['*.Cu','*.Mask']))
        footprint.append(PadArray(pincount=pins, initial=pins+1, start=[0, row], x_spacing=pitch, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE, size=size, drill=drill, layers=['*.Cu','*.Mask']))
        
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
        
        #Add a model
        footprint.append(Model(filename="Connectors_Molex.3dshapes/" + fp_name + ".wrl"))
        
        #filename
        filename = output_dir + fp_name + ".kicad_mod"

        file_handler = KicadFileHandler(footprint)
        file_handler.writeFile(filename)
