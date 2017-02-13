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

Hirose DF

Datasheet:
https://www.hirose.com/product/en/download_file/key_name/DF52/category/Catalog/doc_file_id/51171/?file_category_id=4&item_id=283&is_series=1
"""

pitch = 0.80

#body width
Wb = 2.77

#total width
Wt = 3.22
    
#pad dimensions
pw, ph = 0.5, 1

pad_size = [pw, ph]

#mechanical pad dimensions
mw, mh = 0.9, 1.6
#work out the 'center' of the connector
yc = ((mh / 2) + (Wt - (ph / 2))) / 2

ym = yc - (mh / 2)
yp = yc - (Wt - (ph / 2))

desc = "Hirose DF52 connector, {code}, {p}mm pitch, side entry SMT"
tags = "connector hirose df52 side right-angle horizontal surface mount"

pins = [2,3,4,5,6,8,10,12,14,15,16,17,20]

for pincount in pins:

    part = "DF52-{pincount}S-0.8H".format(pincount=pincount)
    
    footprint_name = "Hirose_{pn}_{n:02}x{pitch:.2f}mm_Angled".format(
        pn = part,
        n = pincount,
        pitch = pitch
    )

    print(footprint_name)
    
    fp = Footprint(footprint_name)
    
    #description
    fp.setDescription(desc.format(p=pitch, code=part))
    fp.setTags(tags)
    fp.setAttribute('smd')
    
    # text
    fp.append(Text(type='reference', text='REF**', at=[0, -2.5], layer='F.SilkS'))
    #fp.append(Text(type='user', text='%R', at=[0, -2.5], layer='F.Fab'))
    fp.append(Text(type='value', text=footprint_name, at=[0,3], layer='F.Fab'))
    
    #Major dimensions
    B = ( pincount - 1 ) * pitch
    A = B + 3
    C = A - 0.6
    
    #pins
    fp.append(
        PadArray(
                pincount=pincount,
                initial = 1,
                center = [0, yp],
                x_spacing = pitch,
                type = Pad.TYPE_SMT,
                layers = Pad.LAYERS_SMT,
                shape = Pad.SHAPE_RECT,
                size = pad_size
                )
    )
    
    #mechanical pads
    xm = B/2 + 0.8 + mw / 2
    fp.append(Pad(at=[xm,ym],shape=Pad.SHAPE_RECT,type=Pad.TYPE_SMT,layers=Pad.LAYERS_SMT,size=[mw,mh]))
    fp.append(Pad(at=[-xm,ym],shape=Pad.SHAPE_RECT,type=Pad.TYPE_SMT,layers=Pad.LAYERS_SMT,size=[mw,mh]))
    
    #connector outline (f.fab layer)
    #y-top
    yt = yp - ph / 2 + 0.3
    #y-bottom
    yb = yt + 2.77
    #y-notch
    yn = 0.5
    
    outline = [
        {'x': 0,'y': yt},
        {'x': -B/2 - pitch,'y': yt},
        {'x': -B/2 - pitch,'y': yt},
        {'x': -B/2 - pitch,'y': yt + yn},
        {'x': -A/2,'y': yt + yn},
        {'x': -A/2,'y': yb},
        {'x': 0,'y': yb},
    ]
    
    fp.append(PolygoneLine(polygone=outline,layer='F.Fab'))
    fp.append(PolygoneLine(polygone=outline,layer='F.Fab',x_mirror=0))
    
    #draw pin-1 indicator on F.Fab
    #size of arrow a
    a = 0.6
    fp.append(PolygoneLine(polygone=[
        {'x': -B/2, 'y': yt + a},
        {'x': -B/2 - a/2, 'y': yt},
        {'x': -B/2 + a/2, 'y': yt},
        {'x': -B/2, 'y': yt + a}], layer='F.Fab'))
        
    #draw pin-1 indicator on Silk.S
    
    fp.append(Circle(center=[-B/2 - 1.4, yp - 0.3], radius=0.2))
    
    #silkscreen
    #offset from pads
    op = 0.3
    #offset from F.fab
    of = 0.15
    
    #Sides
    silk = [
        {'x': B/2 + pw/2 + op, 'y': yt - of},
        {'x': B/2 + of + pitch, 'y': yt - of},
        {'x': B/2 + of + pitch, 'y': yt - of + yn},
        {'x': A/2 + of, 'y': yt - of + yn},
        {'x': A/2 + of, 'y': ym - mh / 2 - op},
    ]
    
    # Right hand side
    fp.append(PolygoneLine(polygone = silk))
    
    # Left hand side (pin 1)
    silk= [{'x': B/2 + pw/2 + op,'y': yp - ph/2 - 0.15}] + silk
    fp.append(PolygoneLine(polygone = silk, x_mirror = 0))
    
    #bottom line
    fp.append(Line(
        start=[-xm + mw/2 + op, yb + of],
        end  =[ xm - mw/2 - op, yb + of]))
        
    #courtyard
    y1 = yp - ph / 2
    y2 = ym + mh / 2
    x1 = xm + mw / 2
    
    fp.append(RectLine(start=[-x1,y1],end=[x1,y2],layer='F.CrtYd',width=0.05,grid=0.05,offset=0.5))
    
        
    #add a 3D model reference
    fp.append(Model(filename="Connectors_Hirose.3dshapes/" + footprint_name + ".wrl"))
            
    #filename
    filename = output_dir + footprint_name + ".kicad_mod"

    file_handler = KicadFileHandler(fp)
    file_handler.writeFile(filename)
    
    
    
    
    