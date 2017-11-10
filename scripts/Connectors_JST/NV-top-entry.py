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

http://www.jst-mfg.com/product/pdf/eng/eNV.pdf

"""
pitch = 5.0

pincount = range(2, 5) #number of pins in each row

#FP name strings
part = "B{n:02}P-NV" #JST part number format string

prefix = "JST_NV_"
suffix = "_{n}x{p:.2f}mm_Vertical"

if __name__ == '__main__':

    for pins in pincount:
        
        #calculate dimensions
        A = (pins - 1) * pitch
        B = A + 5
    
        #generate name
        fp_name = prefix + part.format(n=pins) + suffix.format(n=pins, p=pitch)
        print(fp_name)
        footprint = Footprint(fp_name)
        
        #set description
        description = "JST NV series connector, " + part.format(n=pins) + ", 5.00mm pitch, top entry type, through hole"
        footprint.setDescription(description)
        
        #set tags
        tags = "connector jst nv vertical"
        footprint.setTags(tags)

        #place text
        footprint.append(Text(type='reference', text='REF**', at=[A/2,-4.8], layer='F.SilkS'))
        footprint.append(Text(type='user', text='%R', at=[A/2,2.5], layer='F.Fab'))
        footprint.append(Text(type='value', text=fp_name, at=[A/2,6], layer='F.Fab'))
        
        #draw the component outline
        x1 = A/2 - B/2
        x2 = x1 + B
        y2 = 4.8
        y1 = y2 - 8.5
        
        #draw outline on F.Fab layer
        footprint.append(RectLine(start=[x1,y1],end=[x2,y2],layer='F.Fab',width=0.1))

        #draw horizontal line for latch
        footprint.append(PolygoneLine(polygone=[{'x':x1,'y':(y1+1.7)},{'x':x2,'y':(y1+1.7)}],layer='F.Fab',width=0.1))
		
		#draw pin1 mark on F.Fab
        footprint.append(PolygoneLine(polygone=[{'x':x1,'y':-1},{'x':(x1+1),'y':0}],layer='F.Fab',width=0.1))
        footprint.append(PolygoneLine(polygone=[{'x':x1,'y':1},{'x':(x1+1),'y':0}],layer='F.Fab',width=0.1))
		
        #draw courtyard
        cy = RectLine(start=[x1,y1],end=[x2,y2],offset=0.5,layer='F.CrtYd',width=0.05,grid=0.05)
        footprint.append(cy)
        
        #draw silk outline
        off = 0.12
        x1 -= off
        y1 -= off
        x2 += off
        y2 += off
        
        footprint.append(RectLine(start=[x1,y1],end=[x2,y2],layer='F.SilkS'))
        
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
