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

Molex MicroClasp top-entry single-row connectors
e.g. http://www.molex.com/pdm_docs/sd/559320530_sd.pdf

"""
pitch = 2.00

pincount = range(2,16)

#Molex part number
#with boss, suffix = 10
#no boss, suffix = 30
part = "53932-{n:02}{boss}"

prefix = "Molex_MicroClasp_"
suffix = "{n:02}x{p:.2f}mm_Straight"

drill = 0.8
size = 1.5

#FP description and tags

if __name__ == '__main__':

    for boss in [True, False]:
        for pins in pincount:
            
            # example datasheet - http://www.molex.com/pdm_docs/sd/559320530_sd.pdf
            if boss:
                suf = 10
            else:
                suf = 30
            pn = part.format(n=pins,boss=suf)
            
            #calculate fp dimensions
            
            #B = distance between end-point pins
            B = (pins - 1) * pitch
            #A = total connector length
            A = B + 6
            #C = internal length of connector
            C = B + 3
            
            #T = length of tab
            
            if pins == 2:
                T = 5
            else:
                T = 6.8
                
            #wall-thickness w
            w = 0.6
            
            #corners
            x1 = -(A-B) / 2
            x2 = x1 + A
            
            y2 = 3
            y1 = y2 - 5.8
            
            #y-pos of tab
            yt = y2 - 6.7
            
            #apply offset to the coordinates
            
            #offset 
            o = 0.1
            x1 -= o
            y1 -= o
            x2 += o
            y2 += o

            #generate the name
            fp_name = prefix + pn + "_" + suffix.format(n=pins, p=pitch)

            footprint = Footprint(fp_name)
            

            
            description = "Molex Micro-Clasp connector, PN:" + pn + ", top entry type, through hole"
            
            if boss:
                description += ", with PCB locator"
            
            #set the FP description
            footprint.setDescription(description)
            
            tags = "conn molex microclasp"
            
            #set the FP tags
            footprint.setTags(tags)

            # set general values
            footprint.append(Text(type='reference', text='REF**', at=[B/2,4.3], layer='F.SilkS'))
            footprint.append(Text(type='value', text=fp_name, at=[B/2,-4.8], layer='F.Fab'))
                
            #generate the pads
            footprint.append(PadArray(pincount=pins, x_spacing=pitch, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE, size=size, drill=drill, layers=['*.Cu','*.Mask']))
            
            #add PCB locator if needed
            if boss:
                footprint.append(Pad(at=[B+2,-1.9],size=1.3,drill=1.3, type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE, layers=["*.Cu"]))
            
            
            #draw the courtyard
            cy = RectLine(start=[x1,yt],end=[x2,y2],layer='F.CrtYd',width=0.05,offset = 0.5,grid=0.05)
            footprint.append(cy)
            
            #draw the outline
            out = [
            {'x': B/2, 'y': yt},
            {'x': B/2 - T/2, 'y': yt},
            {'x': B/2 - T/2, 'y': y1},
            {'x': x1, 'y': y1},
            {'x': x1, 'y': y2},
            {'x': B/2, 'y': y2},
            ]
            
            footprint.append(PolygoneLine(polygone=out))
            footprint.append(PolygoneLine(polygone=out,x_mirror=B/2))
            
            #draw the inner wall
            wall = [
            {'x': B/2, 'y': yt + 2*w},
            {'x': B/2 - pitch / 2, 'y': yt + 2*w},
            {'x': B/2 - pitch / 2, 'y': yt + w},
            {'x': B/2 - T/2 + w, 'y': yt + w},
            {'x': B/2 - T/2 + w, 'y': y1 + 2*w},
            {'x': -0.25, 'y': y1 + 2*w},
            {'x': -0.25, 'y': y1 + w},
            {'x': -(C-B)/2, 'y': y1 + w},
            {'x': -(C-B)/2, 'y': y2 - 3*w},
            {'x': x1+w, 'y': y2 - 3*w},
            {'x': x1+w, 'y': y2 - w},
            {'x': B/2, 'y': y2 - w},
            ]
            
            footprint.append(PolygoneLine(polygone=wall))
            footprint.append(PolygoneLine(polygone=wall,x_mirror=B/2))
            
            #pin-1 marker
            y =  3.5
            m = 0.3
            
            pin = [
            {'x': 0,'y': y},
            {'x': -m,'y': y+2*m},
            {'x': m,'y': y+2*m},
            {'x': 0,'y': y},
            ]
            
            footprint.append(PolygoneLine(polygone=pin))
            
            #Add a model
            footprint.append(Model(filename="Connectors_Molex.3dshapes/" + fp_name + ".wrl"))
            
            #filename
            filename = output_dir + fp_name + ".kicad_mod"
            

            file_handler = KicadFileHandler(footprint)
            file_handler.writeFile(filename)
