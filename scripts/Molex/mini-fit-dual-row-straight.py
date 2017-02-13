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

pitch = 4.20

#pins per row
pincount = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

#Molex part number
#with plastic PCB retainer, 
part_w_retainer = "5556-{n:02}B" #n = number of circuits per row

#without plastic PCB retainer:
part_no_retainer = "5556-{n:02}A" #n = number of circuits per row

part_name = "Molex_MiniFit-JR-{part}_2x{n:02}x{p:.2f}mm_Straight"

drill = 1.40
size = 2.8

row = 5.5

#FP description and tags

if __name__ == '__main__':

    for boss in [True, False]:
        for pins in pincount:
            
            if boss:
                pn = part_w_retainer
            else:
                pn = part_no_retainer
                
            pn = pn.format(n=pins*2)
            
            #generate the name
            fp_name = part_name.format(n=pins, p=pitch, part=pn)
            footprint = Footprint(fp_name)
            
            print(fp_name)
            
            description = "Molex Mini-Fit JR, PN:" + pn + ", dual row, top entry type, through hole"
            
            if boss:
                description += ", with plastic PCB locators"
            
            #set the FP description
            footprint.setDescription(description)
            
            tags = "connector molex mini-fit 5556"
            
            #set the FP tags
            footprint.setTags(tags)
            
            #calculate fp dimensions
            
            #connector length
            A = pins * pitch + 1.2
            
            #pin centers
            B = (pins - 1) * pitch
            
            #plasic pin-lock
            C = A + 4
            
            #connector width
            W = 9.6
            
            #corner positions
            x1 = -(A-B)/2
            x2 = x1 + A
            
            y1 = -(W-row) / 2 - 0.2
            y2 = y1 + W + 0.1
            
            #tab length
            tab_l = 3.4
            #tab width
            tab_w = 1.4

            # set general values
            footprint.append(Text(type='reference', text='REF**', at=[B/2,10], layer='F.SilkS'))
            #footprint.append(Text(type='user', text='%R', at=[B/2,10], layer='F.Fab'))
            footprint.append(Text(type='value', text=fp_name, at=[B/2,-4], layer='F.Fab'))
                
            #generate the pads
            footprint.append(PadArray(pincount=pins, x_spacing=pitch, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE, size=size, drill=drill, layers=['*.Cu','*.Mask']))
            footprint.append(PadArray(pincount=pins, initial=pins+1, start=[0, row], x_spacing=pitch, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE, size=size, drill=drill, layers=['*.Cu','*.Mask']))
            
            #add PCB locators if needed
            if boss:
                loc = 3.00
                footprint.append(Pad(at=[B/2-C/2, row - 0.46],type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE, size=loc,drill=loc, layers=["*.Cu"]))
                footprint.append(Pad(at=[B/2+C/2, row - 0.46],type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE, size=loc,drill=loc, layers=["*.Cu"]))
                
                footprint.append(Circle(center=[B/2-C/2, row-0.46],radius=loc/2+0.1))
                footprint.append(Circle(center=[B/2+C/2, row-0.46],radius=loc/2+0.1))
            
            #draw the outline of the shape
            footprint.append(RectLine(start=[x1,y1],end=[x2,y2],layer='F.Fab'))
            
            #draw the outline of the tab
            footprint.append(PolygoneLine(polygone=[
                {'x': B/2 - tab_l/2,'y': y2},
                {'x': B/2 - tab_l/2,'y': y2 + tab_w},
                {'x': B/2 + tab_l/2,'y': y2 + tab_w},
                {'x': B/2 + tab_l/2,'y': y2},
            ], layer='F.Fab'))
            
            #draw the outline of each pin slot (alternating shapes)
            #slot size
            S = 3.5
            
            def square_slot(x,y):
                footprint.append(RectLine(start=[x-S/2,y-S/2],end=[x+S/2,y+S/2],layer='F.Fab'))
                
            def notch_slot(x,y):
                footprint.append(PolygoneLine(polygone=[
                {'x': x-S/2, 'y': y+S/2},
                {'x': x-S/2, 'y': y-S/4},
                {'x': x-S/4, 'y': y-S/2},
                {'x': x+S/4, 'y': y-S/2},
                {'x': x+S/2, 'y': y-S/4},
                {'x': x+S/2, 'y': y+S/2},
                {'x': x-S/2, 'y': y+S/2},
                ], layer='F.Fab'))
            
            q = 1
            notch = True
            for i in range(pins):
                if notch:
                    y_square = 0
                    y_notch = row
                else:
                    y_square = row
                    y_notch = 0
                    
                square_slot(i * pitch, y_square)
                notch_slot(i*pitch, y_notch)
                
                q -= 1
                
                if (q == 0):
                    q = 2
                    notch = not notch
            
            
            #draw the outline of the connector on the silkscreen
            off = 0.1
            outline = [
            {'x': B/2,'y': y1-off},
            {'x': x1-off,'y': y1-off},
            {'x': x1-off,'y': y2+off},
            {'x': B/2 - tab_l/2 - off,'y': y2+off},
            {'x': B/2 - tab_l/2 - off,'y': y2 + off + tab_w},
            {'x': B/2, 'y': y2 + off + tab_w},
            ]
            
            footprint.append(PolygoneLine(polygone=outline))
            footprint.append(PolygoneLine(polygone=outline, x_mirror=B/2))
            
            #pin-1 marker
            x =  -(A-B)/2 - 0.5
            m = 0.3
            
            pin = [
            {'x': x,'y': 0},
            {'x': x-2*m,'y': +m},
            {'x': x-2*m,'y': -m},
            {'x': x,'y': 0},
            ]
            
            footprint.append(PolygoneLine(polygone=pin))
            
            #draw the courtyard
            if boss:
                W = C + 3
            else:
                W = A
                
            footprint.append(RectLine(start=[B/2-W/2,y1],end=[B/2+W/2,y2 + tab_w], width=0.05, layer='F.CrtYd', offset=0.5, grid=0.05))
            
            #Add a model
            footprint.append(Model(filename="Connectors_Molex.3dshapes/" + fp_name + ".wrl"))
            
            #filename
            filename = output_dir + fp_name + ".kicad_mod"

            file_handler = KicadFileHandler(footprint)
            file_handler.writeFile(filename)
