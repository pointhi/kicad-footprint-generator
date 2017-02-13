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

Datasheet: http://www.jst-mfg.com/product/pdf/eng/ePUD.pdf

"""
pitch = 2.0

pincount = [4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20] #number of pins in each row
rows = 2
row_pitch = 2

#FP name strings
part = "B{n:02}B-PUDSS" #JST part number format string

prefix = "JST_PUD_"
suffix = "_2x{n:02}x{p:.2f}mm_Straight"

#FP description and tags

if __name__ == '__main__':

    for pins in pincount:
        
        #calculate fp dimensions
        A = (pins - 1) * pitch
        B = A + 4
    
        #generate the name
        fp_name = prefix + part.format(n=2*pins) + suffix.format(n=pins, p=pitch)

        print(fp_name)
        
        footprint = Footprint(fp_name)
        
        description = "JST PUD series connector, dual row, " + part.format(n=2*pins) + ", top entry type, through hole"
        
        #set the FP description
        footprint.setDescription(description)
        
        tags = "connector jst pud vertical"
        
        #set the FP tags
        footprint.setTags(tags)

        # set general values
        footprint.append(Text(type='reference', text='REF**', at=[A/2,-5.2], layer='F.SilkS'))
        #footprint.append(Text(type='user', text='%R', at=[A/2,-5.2], layer='F.Fab'))
        footprint.append(Text(type='value', text=fp_name, at=[A/2,5.8], layer='F.Fab'))
        
        #draw the component outline
        x1 = A/2 - B/2
        x2 = x1 + B
        y2 = 2 + 2.4
        y1 = y2 - 8.3
        
        #draw simple outline on F.Fab layer
        footprint.append(RectLine(start=[x1,y1],end=[x2,y2],layer='F.Fab'))
        
        #wall thickness t
        t = 0.75
        
        #draw inside tab
        T = A/2 + 0.5
        footprint.append(RectLine(start=[A/2-T/2,y1+t],end=[A/2+T/2,y1+2*t])) #,layer='F.Fab'))
        
        #offset off
        off = 0.15
        
        #outline
        side = [
        {'x': A/2-T/2-t,'y': y1-off},
        {'x': A/2-T/2-t,'y': y1 + 2 * t},
        {'x': A/2-T/2-2*t,'y': y1 + 2 * t},
        {'x': A/2-T/2-2*t,'y': y1 + t},
        {'x': x1 + t,'y': y1 + t},
        {'x': x1 + t,'y': y2 - t},
        {'x': A/2,'y': y2 - t},
        ]
        
        footprint.append(PolygoneLine(polygone=side)) #,  layer='F.Fab'))
        footprint.append(PolygoneLine(polygone=side,x_mirror=A/2))# ,layer='F.Fab'))
        
        
        x1 -= off
        y1 -= off
        x2 += off
        y2 += off
        
        #draw outline
        footprint.append(RectLine(start=[x1,y1],end=[x2,y2]))
        
        #courtyard
        cy = RectLine(start=[x1,y1],end=[x2,y2],offset=0.5,layer='F.CrtYd',width=0.05,grid=0.05)
        footprint.append(cy)
        
        #add p1 marker
        px = x1 - 0.2
        m = 0.3
        
        marker = [
        {'x': px,'y': 0},
        {'x': px-2*m,'y': m},
        {'x': px-2*m,'y': -m},
        {'x': px,'y': 0},
        ]
        
        footprint.append(PolygoneLine(polygone=marker))
        footprint.append(PolygoneLine(polygone=marker,layer='F.Fab'))
        
        #generate the pads (row 1)
        
        drill = 0.7
        size = 1.3
        pa1 = PadArray(pincount=pins, x_spacing=pitch, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE, increment=2, size=size, drill=drill, layers=['*.Cu','*.Mask'])
        pa2 = PadArray(pincount=pins, x_spacing=pitch, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE, start=[0,row_pitch], initial=2, increment=2, size=size, drill=drill, layers=['*.Cu','*.Mask'])
        
        footprint.append(pa1)
        footprint.append(pa2)
        
        #Add a model
        footprint.append(Model(filename="Connectors_JST.3dshapes/" + fp_name + ".wrl"))
        
        #filename
        filename = output_dir + fp_name + ".kicad_mod"
        
        file_handler = KicadFileHandler(footprint)
        file_handler.writeFile(filename)
