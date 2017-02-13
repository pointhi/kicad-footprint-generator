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

Molex Nano Fit side-entry connectors
Single Row: http://www.molex.com/pdm_docs/sd/1053131208_sd.pdf
Double Row: http://www.molex.com/pdm_docs/sd/1053141208_sd.pdf
"""


#pins per row
pincount = range(2,9)

#Molex part numbers
pn_1_row = "105313-xx{n:02}"
pn_2_row = "105314-xx{n:02}"

#part description format strings
part_name = "Molex_NanoFit_{r}x{n:02}x{p:.2f}mm_Angled"
part_description = "Molex Nano Fit, {row}, side entry, through hole, Datasheet:{ds}"
part_tags = "connector molex nano-fit"
#major dimensions
#connector pitch
pitch = 2.50
#spacing between rows
row = 2.5
#drill size
drill = 1.2
#pad size
size = 1.9

#FP description and tags

if __name__ == '__main__':

    for rows in [1,2]:
    
        if rows == 1:
            code = pn_1_row
            datasheet = "http://www.molex.com/pdm_docs/sd/1053131208_sd.pdf"
        else:
            code = pn_2_row
            datasheet = "http://www.molex.com/pdm_docs/sd/1053141208_sd.pdf"
    
        for pins in pincount:
            
            pn = code.format(n=pins*2)
            
            #generate the name
            fp_name = part_name.format(
                n=pins,
                p=pitch,
                r = rows)
                
            footprint = Footprint(fp_name)
            
            print(fp_name)
            
            description = part_description.format(
                ds=datasheet,
                row="single row" if rows == 1 else "dual row"
                )
            
            #set the FP description
            footprint.setDescription(description)
            
            tags = part_tags + " " + pn
            
            #set the FP tags
            footprint.setTags(tags)
            
            #A = connector length
            A = pins * pitch + 0.94
            
            #B = pin center distance
            B = (pins - 1) * pitch
            
            #W = thickness of plastic base
            W = 8.46
            
            #locating pin position
            C = B

            #corner positions for plastic housing outline
            x1 = -(A-B)/2
            x2 = x1 + A
            
            y1 = -(rows - 1) * row - 10.38
            y2 = y1 + W

            # set general values
            footprint.append(Text(type='reference', text='REF**', at=[B/2,2.2], layer='F.SilkS'))
            #footprint.append(Text(type='user', text='%R', at=[B/2,-8], layer='F.Fab'))
            footprint.append(Text(type='value', text=fp_name, at=[B/2,3.5], layer='F.Fab'))
                
            #generate the pads
            for r in range(rows):
                footprint.append(PadArray(pincount=pins, initial=r*pins+1, start=[0,-r*row], x_spacing=pitch, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE, size=size, drill=drill, layers=['*.Cu','*.Mask']))
            
            #add the locating pins
            x_loc_a = B/2 - C/2
            x_loc_b = B/2 + C/2
            y_loc = -(rows-1)*row-7.18
            r_loc = 1.6
            footprint.append(Pad(at=[x_loc_a,y_loc],size=r_loc,drill=r_loc,type=Pad.TYPE_NPTH,shape=Pad.SHAPE_CIRCLE, layers=["*.Cu"]))
            footprint.append(Pad(at=[x_loc_b,y_loc],size=r_loc,drill=r_loc,type=Pad.TYPE_NPTH,shape=Pad.SHAPE_CIRCLE, layers=["*.Cu"]))
            
            #add outline to F.Fab
            footprint.append(RectLine(start=[x1,y1],end=[x2,y2],layer='F.Fab'))
            
            footprint.append(RectLine(start=[x1,y1],end=[x2,y2],offset=0.15))
            
            #draw the pins
            for i in range(pins):
                x = i * pitch
                y = -1 * (rows - 1) * row - size/2 - 0.25
                w = 0.15
                footprint.append(RectLine(start=[x-w,y2+0.15],end=[x+w,y-0.1]))
            
            #add the courtyard
            footprint.append(RectLine(start=[x1,y1],end=[x2,size/2],layer='F.CrtYd',width=0.05,grid=0.05,offset=0.5))
            
            #pin-1 marker
            x = -1.4
            m = 0.3
            
            pin = [
            {'x': x,'y': 0},
            {'x': x-2*m,'y': +m},
            {'x': x-2*m,'y': -m},
            {'x': x,'y': 0},
            ]
            
            footprint.append(PolygoneLine(polygone=pin))

            #Add a model
            footprint.append(Model(filename="Connectors_Molex.3dshapes/" + fp_name + ".wrl"))
            
            #filename
            filename = output_dir + fp_name + ".kicad_mod"

            file_handler = KicadFileHandler(footprint)
            file_handler.writeFile(filename)
