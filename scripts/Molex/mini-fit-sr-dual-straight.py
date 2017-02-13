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

Molex Mini Fit SR top-entry dual-row connectors
e.g. http://www.molex.com/pdm_docs/sd/439151404_sd.pdf
"""

pitch = 10.0

#pins per row
pincount = [3, 4, 5, 6, 7]

part_code = "43915-xx{n:02}"

part_name = "Molex_MiniFit-SR-{part}_2x{n:02}x{p:.2f}mm_Straight"

drill = 2.8
x_size = 6
y_size = 5

#FP description and tags

if __name__ == '__main__':

    for pins in pincount:
        
        pn = part_code.format(n=pins*2)
        
        #generate the name
        fp_name = part_name.format(n=pins, p=pitch, part=pn)
        footprint = Footprint(fp_name)
        
        print(fp_name)
        
        description = "Molex MiniFit-Sr, dual row, top entry type, through hole"
        
        #set the FP description
        footprint.setDescription(description)
        
        tags = "connector molex mini-fit-sr"
        
        #set the FP tags
        footprint.setTags(tags)
        
        #calculate fp dimensions
        #ref: http://www.molex.com/pdm_docs/sd/439151404_sd.pdf
        #A = distance between mounting holes
        A = pins * pitch + 1.41
        
        #B = distance between end pin centers
        B = (pins - 1) * pitch
        
        #E = length of part
        E = pins * pitch + 0.9
        
        #connector width
        W = 19.16
        
        #corner positions
        x1 = -(E-B)/2
        x2 = x1 + E
        
        y2 = 1.15
        y1 = y2 - W

        # set general values
        footprint.append(Text(type='reference', text='REF**', at=[B/2,4], layer='F.SilkS'))
        footprint.append(Text(type='value', text=fp_name, at=[B/2,-20.5], layer='F.Fab'))
            
        #generate the pads
        #top row(s)
        footprint.append(PadArray(pincount=pins, x_spacing=pitch, start=[0,0], type=Pad.TYPE_THT, shape=Pad.SHAPE_RECT, size=[x_size,y_size], drill=drill, layers=['*.Cu','B.Mask']))
        footprint.append(PadArray(pincount=pins, x_spacing=pitch, start=[0,-4.4], type=Pad.TYPE_THT, shape=Pad.SHAPE_RECT, size=[x_size,y_size], drill=drill, layers=['*.Cu','B.Mask']))
                
        #bottom row(s)
        footprint.append(PadArray(pincount=pins, initial=pins+1, start=[0, -12.46], x_spacing=pitch, type=Pad.TYPE_THT, shape=Pad.SHAPE_RECT, size=[x_size,y_size], drill=drill, layers=['*.Cu','B.Mask']))
        footprint.append(PadArray(pincount=pins, initial=pins+1, start=[0, -16.86], x_spacing=pitch, type=Pad.TYPE_THT, shape=Pad.SHAPE_RECT, size=[x_size,y_size], drill=drill, layers=['*.Cu','B.Mask']))

        #thermal vias
        d = 2.2
        d_small = 0.3
        s_small = 0.5
        
        dy1 = -2.2
        dy2 = -14.66
        
        
        for i in range(pins):
        
            x = i * pitch
            n = i + 1
            
            #draw rectangle on F.Fab layer
            w = 0.4 * pitch
            footprint.append(RectLine(start=[x-w/2,dy2-w/2],end=[x+w/2,dy1+w/2],layer='F.Fab'))
        
            footprint.append(Pad(at=[x,dy1],drill=d_small,size=s_small,shape=Pad.SHAPE_CIRCLE,type=Pad.TYPE_THT, layers=["*.Cu","B.Mask"]))
            footprint.append(PadArray(center=[x-d,dy1],pincount=5,y_spacing=2,drill=d_small,size=s_small,initial=n,increment=0,type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE, layers=["*.Cu","B.Mask"]))
            footprint.append(PadArray(center=[x+d,dy1],pincount=5,y_spacing=2,drill=d_small,size=s_small,initial=n,increment=0,type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE, layers=["*.Cu","B.Mask"]))
        
            n = i + 1 + pins
            footprint.append(Pad(at=[x,dy2],drill=d_small,size=s_small,shape=Pad.SHAPE_CIRCLE,type=Pad.TYPE_THT, layers=["*.Cu","B.Mask"]))
            footprint.append(PadArray(center=[x-d,dy2],pincount=5,y_spacing=2,drill=d_small,size=s_small,initial=n,increment=0,type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE, layers=["*.Cu","B.Mask"]))
            footprint.append(PadArray(center=[x+d,dy2],pincount=5,y_spacing=2,drill=d_small,size=s_small,initial=n,increment=0,type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE, layers=["*.Cu","B.Mask"]))
            
        #locating pins
        y_loc = -8.43
        r_loc = 3.0
        footprint.append(Pad(at=[5,y_loc],type=Pad.TYPE_THT,shape=Pad.SHAPE_CIRCLE,size=r_loc+0.25,drill=r_loc, layers=["*.Cu","*.Mask"]))
        footprint.append(Pad(at=[B/2-A/2,y_loc],type=Pad.TYPE_THT,shape=Pad.SHAPE_CIRCLE,size=r_loc+0.25,drill=r_loc, layers=["*.Cu","*.Mask"]))
        footprint.append(Pad(at=[B/2+A/2,y_loc],type=Pad.TYPE_THT,shape=Pad.SHAPE_CIRCLE,size=r_loc+0.25,drill=r_loc, layers=["*.Cu","*.Mask"]))
        
        #mark pin-1 (bottom layer)
        footprint.append(RectLine(start=[-x_size/2, y_size/2],end=[x_size/2,-4.4-y_size/2],offset=0.4,layer='B.SilkS'))
        
        #draw connector outline (basic)
        footprint.append(RectLine(start=[x1,y1],end=[x2,y2],layer='F.Fab'))

        #connector outline on F.SilkScreen
        off = 0.25
        corner = [
        {'x': -x_size/2 - off, 'y': y1-off},
        {'x': x1 - off, 'y': y1-off},
        {'x': x1 - off, 'y': y_loc-r_loc/2-0.5},
        ]
        
        footprint.append(PolygoneLine(polygone=corner))
        footprint.append(PolygoneLine(polygone=corner,x_mirror=B/2))
        footprint.append(PolygoneLine(polygone=corner,y_mirror=y_loc))
        footprint.append(PolygoneLine(polygone=corner,x_mirror=B/2))
        
        #silk-screen between each pad
        for i in range(pins-1):
            xa = i * pitch + x_size/2 + off
            xb = (i+1) * pitch - x_size/2 - off
            
            footprint.append(Line(start=[xa,y1-off],end=[xb,y1-off]))
            footprint.append(Line(start=[xa,y2+off],end=[xb,y2+off]))
        
        #draw the tabs at each end
        TL = 5
        TW = 13
        
        tab = [
            {'x': x1-off,'y': y_loc-TW/2-off},
            {'x': x1-off-TL,'y': y_loc-TW/2-off},
            {'x': x1-off-TL,'y': y_loc+TW/2+off},
            {'x': x1-off,'y': y_loc+TW/2+off},
        ]
        
        footprint.append(PolygoneLine(polygone=tab))
        footprint.append(PolygoneLine(polygone=tab, x_mirror=B/2))
        
        #inner-tab
        T = 2
        tab = [
            {'x': x1-off,'y': y_loc-TW/2-off+T},
            {'x': x1-off-TL+T,'y': y_loc-TW/2-off+T},
            {'x': x1-off-TL+T,'y': y_loc+TW/2+off-T},
            {'x': x1-off,'y': y_loc+TW/2+off-T},
        ]
        
        footprint.append(PolygoneLine(polygone=tab))
        footprint.append(PolygoneLine(polygone=tab,x_mirror=B/2))
        
        #pin-1 marker
        x = x1 - 1
        m = 0.4
        
        pin = [
        {'x': x,'y': 0},
        {'x': x-2*m,'y': -m},
        {'x': x-2*m,'y': +m},
        {'x': x,'y': 0},
        ]
        
        footprint.append(PolygoneLine(polygone=pin))
            
        #draw the courtyard
        footprint.append(RectLine(
            start=[x1-TL-0.3,-16.86-y_size/2],
            end=[x2+TL+0.3,y_size/2],
            width=0.05,
            layer='F.CrtYd',
            offset=0.5,
            grid=0.05))
        
        #Add a model
        footprint.append(Model(filename="Connectors_Molex.3dshapes/" + fp_name + ".wrl"))
        
        #filename
        filename = output_dir + fp_name + ".kicad_mod"

        file_handler = KicadFileHandler(footprint)
        file_handler.writeFile(filename)
