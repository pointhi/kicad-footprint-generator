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

Molex Nano Fit top-entry connectors
Single Row: http://www.molex.com/pdm_docs/sd/1053091203_sd.pdf
Double Row: http://www.molex.com/pdm_docs/sd/1053101208_sd.pdf
"""


#pins per row
pincount = range(2,9)

#Molex part numbers
pn_1_row = "105309-xx{n:02}"
pn_2_row = "105310-xx{n:02}"

#part description format strings
part_name = "Molex_NanoFit_{r}x{n:02}x{p:.2f}mm_Straight"
part_description = "Molex Nano Fit, {row}, top entry, through hole, Datasheet:{ds}"
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
            datasheet = "http://www.molex.com/pdm_docs/sd/1053091203_sd.pdf"
        else:
            code = pn_2_row
            datasheet = "http://www.molex.com/pdm_docs/sd/1053101208_sd.pdf"
    
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
            W = rows * pitch + 0.98
            
            #locating pin position
            if pins in [3,5,7]:
                C = B/2 - 1.25
            else:
                C = B/2
            
            #corner positions for plastic housing outline
            x1 = -(A-B)/2
            x2 = x1 + A
            
            y2 = (W - (rows-1) * pitch) / 2
            y1 = y2 - W

            # set general values
            footprint.append(Text(type='reference', text='REF**', at=[B/2,-3-(rows-1)*pitch], layer='F.SilkS'))
            #footprint.append(Text(type='user', text='%R', at=[B/2,-3-(rows-1)*pitch], layer='F.Fab'))
            footprint.append(Text(type='value', text=fp_name, at=[B/2,-4.5-(rows-1)*pitch], layer='F.Fab'))
                
            #generate the pads
            for r in range(rows):
                footprint.append(PadArray(pincount=pins, initial=r*pins+1, start=[0,-r*row], x_spacing=pitch, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE, size=size, drill=drill, layers=['*.Cu','*.Mask']))
            
            #add the locating pin
            footprint.append(Pad(at=[C,1.34],size=1.3,drill=1.3,type=Pad.TYPE_NPTH,shape=Pad.SHAPE_CIRCLE, layers=["*.Cu"]))
            
            #add outline to F.Fab
            #footprint.append(RectLine(start=[x1,y1],end=[x2,y2],layer='F.Fab'))
            
            off = 0.15
            #and to the silkscreen
            #and draw the tab
            TL = 5.2
            TW = 2.86
            
            def outline(off=0):
                out = [
                {'x': B/2,'y': y1-off},
                {'x': x1-off,'y': y1-off},
                {'x': x1-off,'y': y2+off},
                {'x': B/2-TL/2-off,'y': y2+off},
                {'x': B/2-TL/2-off,'y': y2+TW+off},
                {'x': B/2,'y': y2+TW+off}
                ]
                
                return out
            
            footprint.append(PolygoneLine(polygone=outline(), layer='F.Fab'))
            footprint.append(PolygoneLine(polygone=outline(), layer='F.Fab', x_mirror=B/2))
            
            footprint.append(PolygoneLine(polygone=outline(off = 0.15)))
            footprint.append(PolygoneLine(polygone=outline(off = 0.16), x_mirror=B/2))
            
            footprint.append(RectLine(start=[B/2-TL/2,y2+2*off],end=[B/2+TL/2,y2+TW],offset=-0.5))
            
            #add the courtyard
            footprint.append(PolygoneLine(layer='F.CrtYd',width=0.05,grid=0.05,polygone=[
            {'x': x1-0.5,'y': y1-0.5},
            {'x': x1-0.5,'y': y2+0.5},
            {'x': B/2-TL/2-0.5,'y': y2+0.5},
            {'x': B/2-TL/2-0.5,'y': y2+TW+0.5},
            {'x': B/2+TL/2+0.5,'y': y2+TW+0.5},
            {'x': B/2+TL/2+0.5,'y': y2+0.5},
            {'x': x2+0.5,'y': y2+0.5},
            {'x': x2+0.5,'y': y1-0.5},
            {'x': x1-0.5,'y': y1-0.5},
            ]))
            
            #draw the pins!
            o = 0.475 * pitch
            for i in range(pins):
                for j in range(rows):
                    x = i * pitch
                    y = -j * pitch
                    
                    footprint.append(RectLine(start=[x-o,y-o],end=[x+o,y+o], layer='F.Fab'))
            
            #pin-1 marker
            x = x1 - 0.5
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
