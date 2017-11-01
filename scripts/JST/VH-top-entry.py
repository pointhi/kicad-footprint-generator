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

This script generates both the standard and PBT top entry types

"""
pitch = 3.96

pincount = range(2, 11) #number of pins in each row

#FP name strings
part = "B{n}P-VH" #JST part number format string

prefix = "JST_VH_"
suffix = "_{n}x{p:.2f}mm_Straight"

if __name__ == '__main__':

    # the tuple for series is: [<max pincount + 1>, <PN suffix>,<series name>,<series tag>]
    for series in [(11, "VH", "VH", "vh"), (12, "VH-B", "VH PBT", "vh pbt")]:
    
        pitch = 3.96

        pincount = range(2, series[0]) #number of pins in each row

        #FP name strings
        part = "B{n}P-" + series[1] #JST part number format string

        prefix = "JST_VH_"
        suffix = "_{n}x{p:.2f}mm_Vertical"
        
        for pins in pincount:
            
            #calculate dimensions
            A = (pins - 1) * pitch
            B = A + 3.9
        
            #generate name
            fp_name = prefix + part.format(n=pins) + suffix.format(n=pins, p=pitch)
            print(fp_name)
            footprint = Footprint(fp_name)
            
            #set description
            description = "JST " + series[2] + " series connector, " + part.format(n=pins) + ", 3.96mm pitch, top entry type, through hole"
            footprint.setDescription(description)
            
            #set tags
            tags = "connector jst " + series[3] + " vertical"
            footprint.setTags(tags)

            #place text
            footprint.append(Text(type='reference', text='REF**', at=[A/2,-4.8], layer='F.SilkS'))
            footprint.append(Text(type='user', text='%R', at=[A/2,2.5], layer='F.Fab'))
            footprint.append(Text(type='value', text=fp_name, at=[A/2,6], layer='F.Fab'))
            
            #coordinate locations
            #    x1 x3                  x4 x2
            # y3    ____________________
            # y1 __|____________________|__
            #    | 1  2  3  4  5  6  7  8 |
            # y2 |________________________|
            
            #draw the component outline
            x1 = A/2 - B/2
            x2 = x1 + B
            y2 = 4.8
            y1 = y2 - 6.8
            y3 = y1 - 1.7
            
            #draw outline on F.Fab layer
            footprint.append(RectLine(start=[x1,y1],end=[x2,y2],layer='F.Fab',width=0.1))

            #draw rectangle on F.Fab for latch
            x3 = -0.75
            x4 = pitch * (pins - 1) + 0.75
            footprint.append(PolygoneLine(polygone=[{'x':x3,'y':y1},{'x':x3,'y':y3},{'x':x4,'y':y3},{'x':x4,'y':y1}],layer='F.Fab',width=0.1))
            
            #draw pin1 mark on F.Fab
            footprint.append(PolygoneLine(polygone=[{'x':x1,'y':-1},{'x':(x1+1),'y':0}],layer='F.Fab',width=0.1))
            footprint.append(PolygoneLine(polygone=[{'x':x1,'y':1},{'x':(x1+1),'y':0}],layer='F.Fab',width=0.1))
            
            #draw courtyard
            cy = RectLine(start=[x1,y1-1.7],end=[x2,y2],offset=0.5,layer='F.CrtYd',width=0.05,grid=0.05)
            footprint.append(cy)
            
            #draw silk outline
            off = 0.12
            x1 -= off
            y1 -= off
            x2 += off
            y2 += off
            x3 -= off
            y3 -= off
            x4 += off
            
            footprint.append(PolygoneLine(polygone=[{'x':x1,'y':y2},{'x':x1,'y':y1},{'x':x3,'y':y1},{'x':x3,'y':y3},{'x':x4,'y':y3},{'x':x4,'y':y1},{'x':x2,'y':y1},{'x':x2,'y':y2},{'x':x1,'y':y2}],layer='F.SilkS'))
            
            #add pin1 mark on silk
            px = x1 - 0.2
            m = 0.3
            
            marker = [{'x': px,'y': 0},{'x': px-2*m,'y': m},{'x': px-2*m,'y': -m},{'x': px,'y': 0}]
            footprint.append(PolygoneLine(polygone=marker,width=0.12))
            
            #generate tht pads (1.65mm drill with 2.35x3mm oval pads)
            pa = PadArray(pincount=pins, x_spacing=pitch, type=Pad.TYPE_THT, shape=Pad.SHAPE_OVAL, size=[2.35,3], drill=1.65, layers=['*.Cu','*.Mask'])
            footprint.append(pa)
            
            #add 3D model
            footprint.append(Model(filename="${KISYS3DMOD}/Connectors_JST.3dshapes/" + fp_name + ".wrl"))
            
            #filename
            filename = output_dir + fp_name + ".kicad_mod"
            
            file_handler = KicadFileHandler(footprint)
            file_handler.writeFile(filename)
