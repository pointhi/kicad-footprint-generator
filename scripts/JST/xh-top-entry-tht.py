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
boss = False
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
        
        y1 = -2.35
        y2 = y1 + T

        #generate the name
        fp_name = prefix + part.format(n=pins) + suffix.format(n=pins, p=pitch)

        footprint = Footprint(fp_name)
        
        print(fp_name)
        
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
        
        #draw simple outline on F.Fab layer
        footprint.append(RectLine(start=[x1,y1],end=[x2,y2],layer='F.Fab'))

        # set general values
        footprint.append(Text(type='reference', text='REF**', at=[x_mid,-3.5], layer='F.SilkS'))
        footprint.append(Text(type='value', text=fp_name, at=[x_mid,4.5], layer='F.Fab'))

        if pins == 2:
            drill = 1.0
        else:
            drill = 0.9
            
        #generate the pads
        pa = PadArray(pincount=pins, x_spacing=pitch, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE, size=1.75, drill=drill, layers=['*.Cu','*.Mask'])
        
        footprint.append(pa)
        
        #draw the courtyard
        cy = RectLine(start=[x1,y1],end=[x2,y2],layer='F.CrtYd',width=0.05,offset = 0.5,grid=0.05)
        footprint.append(cy)
        
        #draw the connector outline
        out = RectLine(start=[x1,y1],end=[x2,y2],offset=0.1)
        footprint.append(out)
        
        #wall thickness w 
        w = 0.75
        
        #gap size g
        g = 1.5
        
        off = 0.1
        
        x1 -= off
        y1 -= off
        
        x2 += off
        y2 += off
        
        #draw the center tab
        footprint.append(RectLine(start=[g/2,y1],end=[A-g/2,y1+w]))
        
        #add left tab
        footprint.append(RectLine(start=[x1,y1],end=[-g/2,y1+w]))
        #right tab
        footprint.append(RectLine(start=[A+g/2,y1],end=[x2,y1+w]))
        
        #add other line
        line = [
        {'x': x1,'y': y1+w+g},
        {'x': x1+w,'y': y1+w+g},
        {'x': x1+w,'y': y2-w},
        {'x': A/2,'y': y2-w},
        ]
        
        footprint.append(PolygoneLine(polygone=line))
        footprint.append(PolygoneLine(polygone=line,x_mirror=A/2))
        
        #pin-1 marker
        D = 0.3
        L = 2.5
        
        pin = [
            {'x': x1-D+L,'y': y1-D},
            {'x': x1-D,'y': y1-D},
            {'x': x1-D,'y': y1-D+L},
        ]
        footprint.append(PolygoneLine(polygone=pin))
        footprint.append(PolygoneLine(polygone=pin,layer='F.Fab'))
        
        #Add a model
        footprint.append(Model(filename="Connectors_JST.3dshapes/" + fp_name + ".wrl"))
        
        
        #filename
        filename = output_dir + fp_name + ".kicad_mod"
        

        file_handler = KicadFileHandler(footprint)
        file_handler.writeFile(filename)
