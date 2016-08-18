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
pitch = 2.50
boss = True
if boss:
    pincount = range(2,13)
else:
    pincount = [i for i in range(2,17)] + [20]


#FP name strings
part = "B{n:02}B-XH-A" #JST part number format string

if boss:
    part += "M"

prefix = "JST_XH_"
suffix = "_{n:02}x{p:.2f}mm_Straight"

#FP description and tags

if __name__ == '__main__':

    for pins in pincount:
        
        #calculate fp dimensions
        A = (pins - 1) * pitch
        B = A + 4.9
        
        #connector thickness
        T = 5.75
        
        #corners
        x1 = -2.45
        x2 = x1 + B
        
        x_mid = (x1 + x2) / 2
        
        y1 = -3.4
        y2 = y1 + T
    
        #generate the name
        fp_name = prefix + part.format(n=pins) + suffix.format(n=pins, p=pitch)

        footprint = Footprint(fp_name)
        
        description = "JST XH series connector, " + part.format(n=pins) + ", top entry type, through hole"

        if boss:
            description += ", with boss"
        
        #set the FP description
        footprint.setDescription(description)
        
        tags = "connector jst xh tht top vertical 2.50mm"
        
        if boss:
            tags += " boss"
        #set the FP tags
        footprint.setTags(tags)

        # set general values
        footprint.append(Text(type='reference', text='REF**', at=[x_mid,-5], layer='F.SilkS'))
        footprint.append(Text(type='value', text=fp_name, at=[x_mid,4], layer='F.Fab'))

        if pins == 2:
            drill = 1.0
        else:
            drill = 0.9
            
        #generate the pads
        pa = PadArray(pincount=pins, x_spacing=pitch, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE, size=1.5, drill=drill, layers=['*.Cu','*.Mask'])
        
        footprint.append(pa)
        
        #draw the courtyard
        cy = RectLine(start=[x1,y1],end=[x2,y2],layer='F.CrtYd',width=0.05,offset = 0.5)
        footprint.append(cy)
        
        #offset the outline around the connector
        off = 0.15
        
        xo1 = x1 - off
        yo1 = y1 - off
        
        xo2 = x2 + off
        yo2 = y2 + off
        
        #thickness of the notches
        notch = 1.5
        
        #wall thickness of the outline
        wall = 0.6
        
        #draw the outline of the connector
        
        footprint.append(RectLine(start=[xo1,yo1],end=[xo2,yo2]))
        
        outline = [
        {'x': xo1,'y': yo2-wall - 1},
        {'x': xo1 + wall,'y': yo2-wall - 1},
        {'x': xo1 + wall,'y': yo1+wall},
        {'x': x_mid,'y': yo1+wall},
        ]
        
        if not boss:
            
            footprint.append(PolygoneLine(polygone=outline))
            
            footprint.append(PolygoneLine(polygone=outline,x_mirror=x_mid))
        else:
            
            outline.append({'x': xo2-wall,'y': yo1+wall})
            footprint.append(PolygoneLine(polygone=outline))
        
            outline = [
            {'x': xo2,'y': yo2-wall-1},
            {'x': xo2-wall,'y': yo2-wall-1},
            {'x': xo2-wall,'y': -1},
            ]

            footprint.append(PolygoneLine(polygone=outline))
        
        footprint.append(RectLine(start=[xo1,yo2-wall],end=[xo1+notch,yo2]))
        footprint.append(RectLine(start=[xo2,yo2-wall],end=[xo2-notch,yo2]))
        
        #draw the middle tab
        nx1 = -0.5 + notch
        nx2 = A + 0.5 - notch
        footprint.append(RectLine(start=[nx1, yo2 - wall],end=[nx2,yo2]))
        
        #add a boss (maybe)
        if boss:
            footprint.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE, at=[A+1.6,-2], size=1.1, drill=1.1, layers=["*.Cu"]))
        
        #Add a model
        footprint.append(Model(filename="Connectors_JST.3dshapes/" + fp_name + ".wrl"))
        
        
        #filename
        filename = output_dir + fp_name + ".kicad_mod"
        

        file_handler = KicadFileHandler(footprint)
        file_handler.writeFile(filename)
