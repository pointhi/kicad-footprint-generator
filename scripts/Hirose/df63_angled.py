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

Hirose DF63

URL:
https://www.hirose.com/product/en/products/DF63/

Datasheet:
https://www.hirose.com/product/en/download_file/key_name/DF63/category/Catalog/doc_file_id/51104/?file_category_id=4&item_id=47&is_series=1
"""

manu = "Hirose"

series = "DF63"

pitch = 3.96

drill = 1.8

pad_size = 3

mount_size = 1.6

#vertical center of connector
y2 = 3.25 + mount_size / 2
y1 = y2 - 7.05
yt = y2 - 8

desc = "{manu} {series} connector, {code}, {p}mm pitch, side entry THT"
tags = "connector hirose df63 horizontal through hole"

pins = [2,3]

for pincount in pins:

    part = "DF63-{pincount}P-3.96DS".format(series=series,pincount=pincount)
    
    footprint_name = "{manu}_{pn}_{n:02}x{pitch:.2f}mm_Angled".format(
        manu = manu,
        pn = part,
        n = pincount,
        pitch = pitch
    )

    print(footprint_name)
    
    fp = Footprint(footprint_name)
    
    #description
    fp.setDescription(desc.format(manu=manu, series=series, p=pitch, code=part))
    fp.setTags(tags)
    
    # text
    fp.append(Text(type='reference', text='REF**', at=[0, -5.2], layer='F.SilkS'))
    fp.append(Text(type='value', text=footprint_name, at=[0,5.4 ], layer='F.Fab'))
    
    #Major dimensions
    B = ( pincount - 1 ) * pitch
    A = B + 4.7
    
    #pins
    fp.append(
        PadArray(
                pincount=pincount,
                initial = 1,
                start = [0, 0],
                x_spacing = pitch,
                type = Pad.TYPE_THT,
                layers = Pad.LAYERS_THT,
                shape = Pad.SHAPE_CIRCLE,
                size = pad_size,
                drill = drill,
                )
    )
    
    #calculate major dimensions
    x1 = (B - A) / 2
    x2 = x1 + A
    
    #courtyard
    fp.append(RectLine(start=[x1,yt],end=[x2,y2],layer='F.CrtYd',width=0.05,grid=0.05,offset=0.5))
    
    #mounting hole
    if pincount > 1:
        fp.append(Pad(at=[-1.5,3.25],type=Pad.TYPE_NPTH,layers=Pad.LAYERS_NPTH,shape=Pad.SHAPE_CIRCLE,size=mount_size,drill=mount_size))
    
    #connector outline
    
    #tab thickness
    t = 1.2
    
    def outline(offset=0):    
        outline = [
        {'x': B/2, 'y': y2 + offset},
        {'x': x1 - offset, 'y': y2 + offset},
        {'x': x1 - offset, 'y': yt - offset},
        {'x': x1 + t + offset, 'y': yt - offset},
        {'x': x1 + t + offset, 'y': y1 - offset},
        {'x': B/2, 'y': y1 - offset},
        ]
        
        return outline
    
    fp.append(PolygoneLine(polygone=outline(),layer='F.Fab'))
    fp.append(PolygoneLine(polygone=outline(),layer='F.Fab',x_mirror=B/2))
    
    fp.append(PolygoneLine(polygone=outline(offset=0.15)))
    fp.append(PolygoneLine(polygone=outline(offset=0.15),x_mirror=B/2))
    
    #draw lines between pads on F.Fab
    for i in range(pincount - 1):
        x = (i + 0.5) * pitch
        
        fp.append(Line(start=[x,y1],end=[x,y2],layer='F.Fab'))
    
    """
    
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
    ya = -2
    fp.append(PolygoneLine(polygone=[
        {'x': -B/2, 'y': ya},
        {'x': -B/2 - a/2, 'y': ya - a},
        {'x': -B/2 + a/2, 'y': ya - a},
        {'x': -B/2, 'y': ya},
        ]))
    
    #silkscreen
    #offset from pads
    op = 0.3
    #offset from F.fab
    of = 0.15
    
    #Sides
    silk = [
    {'x': -B/2 - pw/2 - op, 'y': yt - of},
    {'x': -B/2 - of - pitch, 'y': yt - of},
    {'x': -B/2 - of - pitch, 'y': yt - of + yn},
    {'x': -A/2 - of, 'y': yt - of + yn},
    {'x': -A/2 - of, 'y': ym - mh / 2 - op},
    ]
    
    fp.append(PolygoneLine(polygone = silk))
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
    
    """
        
    #add a 3D model reference
    fp.append(Model(filename="Connectors_Hirose.3dshapes/" + footprint_name + ".wrl"))
            
    #filename
    filename = output_dir + footprint_name + ".kicad_mod"

    file_handler = KicadFileHandler(fp)
    file_handler.writeFile(filename)
    
    
    
    
    