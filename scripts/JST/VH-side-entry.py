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

http://www.jst-mfg.com/product/pdf/eng/eVH.pdf

"""
pitch = 3.96

pincount = range(2, 11) #number of pins in each row

#FP name strings
part = "B{n}PS-VH" #JST part number format string

prefix = "JST_VH_"
suffix = "_2x{n}x{p:.2f}mm_Horizontal"

#FP description and tags

if __name__ == '__main__':

    for pins in pincount:
        
        #calculate fp dimensions
        A = (pins - 1) * pitch
        B = A + 3.9
    
        #generate the name
        fp_name = prefix + part.format(n=pins) + suffix.format(n=pins, p=pitch)

        footprint = Footprint(fp_name)
        
        print(fp_name)
        
        description = "JST VH series connector, " + part.format(n=pins) + ", side entry type, through hole"
        
        #set the FP description
        footprint.setDescription(description)
        
        tags = "connector jst vh horizontal"
        
        #set the FP tags
        footprint.setTags(tags)

        # set general values
        footprint.append(Text(type='reference', text='REF**', at=[A/2,-2.6], layer='F.SilkS'))
        footprint.append(Text(type='user', text='%R', at=[A/2,6], layer='F.Fab'))
        footprint.append(Text(type='value', text=fp_name, at=[A/2,16.2], layer='F.Fab'))
        
        #coordinate locations
        #    x1 x3                x4 x2
        #       1  2  3  4  5  6  7
        # y1  _______________________
        # y2 |_|                  |__|
        #      |                  |
        # y3   |__________________|
        # y4   || || || || || || ||
        
        #generate pads
        pa1 = PadArray(pincount=pins, x_spacing=pitch, type=Pad.TYPE_THT, shape=Pad.SHAPE_OVAL, size=[2.35, 3], drill=1.65, layers=['*.Cu','*.Mask'])
        footprint.append(pa1)
        
        #draw the component outline
        x1 = A/2 - B/2
        x2 = x1 + B
        x3 = -0.9
        x4 = pitch * (pins - 1) + 0.9
        y1 = 4.4
        y2 = y1 + 3.2
        y3 = y1 + 9.4
        y4 = 14.9
        
        #draw shroud outline on F.Fab layer
        footprint.append(RectLine(start=[x3,y1],end=[x4,y3],layer='F.Fab'))
        footprint.append(PolygoneLine(polygone=[{'x':x4,'y':y1},{'x':x2,'y':y1},{'x':x2,'y':y2},{'x':x4,'y':y2}],layer='F.Fab',width=0.1))
        footprint.append(PolygoneLine(polygone=[{'x':x3,'y':y2},{'x':x1,'y':y2},{'x':x1,'y':y1},{'x':x3,'y':y1}],layer='F.Fab'))
        
        #draw pin1 mark on F.Fab
        footprint.append(PolygoneLine(polygone=[{'x':-0.8,'y':y1},{'x':0,'y':y1+0.8},{'x':0.8,'y':y1}],layer='F.Fab'))

        #draw pin outlines on F.Fab (pin width is 1.4mm, so 0.7mm is half the pin width)
        for pin in range(pins):
            footprint.append(PolygoneLine(polygone=[{'x':pin * pitch - 0.7,'y':y1},{'x':pin * pitch - 0.7,'y':0},{'x':pin * pitch + 0.7,'y':0},{'x':pin * pitch + 0.7,'y':y1}],layer='F.Fab',width=0.1))
            footprint.append(PolygoneLine(polygone=[{'x':pin * pitch - 0.7,'y':y3},{'x':pin * pitch - 0.7,'y':y4},{'x':pin * pitch + 0.7,'y':y4},{'x':pin * pitch + 0.7,'y':y3}],layer='F.Fab',width=0.1))
        
        #draw silk outlines
        off = 0.12
        x1 -= off
        y1 -= off
        x2 += off
        y2 += off
        x3 -= off
        y3 += off
        x4 += off
        y4 += off

        footprint.append(PolygoneLine(polygone=[{'x':x1,'y':y1},{'x':x2,'y':y1},{'x':x2,'y':y2},{'x':x4,'y':y2},{'x':x4,'y':y3},{'x':x3,'y':y3},{'x':x3,'y':y2},{'x':x1,'y':y2},{'x':x1,'y':y1}],layer='F.SilkS'))
        
        #pin silk (half of pin width is 0.7mm, so adding 0.12mm silk offset gives 0.82mm about pin center)
        for pin in range(pins):
            footprint.append(PolygoneLine(polygone=[{'x':pin * pitch - 0.82,'y':y3},{'x':pin * pitch - 0.82,'y':y4},{'x':pin * pitch + 0.82,'y':y4},{'x':pin * pitch + 0.82,'y':y3}],layer='F.SilkS'))
        
        #add pin1 marker on F.FilkS (magic numbers intended to hit ~0.3mm copper-silk clearance)
        footprint.append(PolygoneLine(polygone=[{'x':0,'y':-1.85},{'x':-1.55,'y':-1.85},{'x':-1.55,'y':0}],layer='F.SilkS'))

        #courtyard (pad Y dimension is 3mm)
        cy = RectLine(start=[x1,-3/2.0],end=[x2,y4],offset=0.5,layer='F.CrtYd',width=0.05,grid=0.05)
        footprint.append(cy)
        
        #Add 3D model
        footprint.append(Model(filename="${KISYS3DMOD}/Connectors_JST.3dshapes/" + fp_name + ".wrl"))
        
        #filename
        filename = output_dir + fp_name + ".kicad_mod"
        
        file_handler = KicadFileHandler(footprint)
        file_handler.writeFile(filename)
