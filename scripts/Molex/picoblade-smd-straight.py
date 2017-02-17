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

Molex PicoBlade SMD top-entry connectors
http://www.molex.com/pdm_docs/sd/533980671_sd.pdf
"""

pitch = 1.25

#pincounts
pincount = range(2,16)

#Molex part number
part_code = "53398-{n:02}71" #n = number of circuits

part_name = "Molex_PicoBlade_{part}_{n:02}x{p:.2f}mm_Straight"

#FP description and tags
description = "Molex PicoBlade, single row, top entry type, surface mount, PN:{pn}"
tags = "connector molex picoblade smt"

#pad size
pw = 0.8
ph = 1.5

#mechanical pad size
mw = 2.2
mh = 3.1

#calculate the various y-positions
#center point of pads
YP = 1.3 / 2
YM = 1.3 + 0.6 + 3 / 2

#center point between pads
YC = (YP + YM) / 2

#offset the values
py = YP - YC #center of the numbered pads
my = YM - YC #center of the mechanical pads

if __name__ == '__main__':

    for pins in pincount:
        
        pn = part_code.format(n=pins)
        
        #generate the name
        fp_name = part_name.format(n=pins, p=pitch, part=pn)
        footprint = Footprint(fp_name)
        
        print(fp_name)
        
        #set the FP description
        footprint.setDescription(description.format(pn=pn)) 
        
        #set the FP tags
        footprint.setTags(tags)
        footprint.setAttribute('smd')
        
        #calculate fp dimensions
        
        A = (pins - 1) * pitch
        B = A + 1.8
        C = A + 1.1
        D = A + 3
        E = A + 6
        F = A + 6.4
        
        # set general values
        footprint.append(Text(type='reference', text='REF**', at=[0,-3.25], layer='F.SilkS'))
        footprint.append(Text(type='value', text=fp_name, at=[0,4.25], layer='F.Fab'))
        
        #footprint.append(Text(type='user', text='%R', at=[0,1.5], layer='F.Fab'))
        
        #draw the pins
        footprint.append(PadArray(center=[0,py],size=[pw,ph],pincount=pins,x_spacing=pitch,type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, layers=Pad.LAYERS_SMT))

        #mechanical pins
        mx = A / 2 + 3.6 - mw / 2
        footprint.append(Pad(at=[-mx,my],size=[mw,mh],type=Pad.TYPE_SMT,shape=Pad.SHAPE_RECT,layers=Pad.LAYERS_SMT))
        footprint.append(Pad(at=[ mx,my],size=[mw,mh],type=Pad.TYPE_SMT,shape=Pad.SHAPE_RECT,layers=Pad.LAYERS_SMT))
        
        #connector outline on F.Fab layer
        xf = D / 2
        yf1 = py - 1.3/2 + 0.3 + 0.5
        yf2 = yf1 + 3.7
        
        footprint.append(RectLine(start=[-xf,yf1],end=[xf,yf2],layer='F.Fab'))
        
        #connector 'ear'
        ear = [
            {'x': xf,'y': yf2},
            {'x': E/2 ,'y': yf2},
            {'x': E/2 ,'y': yf2 - 2.8},
            {'x': xf ,'y': yf2 - 2.8},
        ]
        
        footprint.append(PolygoneLine(polygone=ear,layer='F.Fab'))
        footprint.append(PolygoneLine(polygone=ear,layer='F.Fab',x_mirror=0))
        
        #add silkscreen where appropriate
        o = 0.15
        po = 0.3
        side = [
            {'x': A/2 + pw/2 + po,'y': yf1 - o},
            {'x': xf + o,'y': yf1 - o},
            {'x': xf + o,'y': my - mh/2 - po},
            {'x': E/2 + o,'y': my - mh/2 - po},
            #{'x': mx + mw/2 + po,'y': my + mh/2 + po},
            #{'x': mx - mw/2 - po,'y': my + mh/2 + po},
            #{'x': mx - mw/2 - po,'y': yf2 + o},
            #{'x': 0,'y': yf2 + o},
        ]
        
        footprint.append(PolygoneLine(polygone=side))
        footprint.append(PolygoneLine(polygone=side,x_mirror=0))
        
        # Draw bottom line
        footprint.append(Line(start=[-mx+mw/2+po,yf2+o],end=[mx-mw/2-po,yf2+o]))
        
        #pin-1 marker
        p1_start = [-A/2-pw/2-po,yf1-o]
        p1_end   = [-A/2-pw/2-po,py-ph/2]
        footprint.append(Line(start=p1_start,end=p1_end))
        #footprint.append(Line(start=p1_start,end=p1_end,layer='F.Fab'))

        # Add pin-1 marker to F.Fab
        m = pw / 2
        x = -A/2
        y = yf1
        
        pin = [
        {'x': x - m,'y': y},
        {'x': x,'y': y + 2 * m},
        {'x': x + m,'y': y},
        {'x': x - m,'y': y},
        ]
         
        footprint.append(PolygoneLine(polygone=pin, layer='F.Fab'))
        
        #courtyard
        
        xc = mx + mw / 2
        yc1 = py - ph / 2
        yc2 = my + mh / 2
        
        off = 0.6
        
        cy = [
            {'x': 0,'y': yc1 - off},
            {'x': xf + off,'y': yc1 - off},
            {'x': xf + off,'y': yf2 - 2.8 - off},
            {'x': xc + off,'y': yf2 - 2.8 - off},
            {'x': xc + off,'y': yc2 + off},
            {'x': 0,'y': yc2 + off},
        ]
        
        footprint.append(PolygoneLine(polygone=cy,grid=0.05,width=0.05,layer='F.CrtYd'))
        footprint.append(PolygoneLine(polygone=cy,grid=0.05,width=0.05,layer='F.CrtYd',x_mirror=0))
        
        
        #Add a model
        footprint.append(Model(filename="Connectors_Molex.3dshapes/" + fp_name + ".wrl"))
        
        #filename
        filename = output_dir + fp_name + ".kicad_mod"

        file_handler = KicadFileHandler(footprint)
        file_handler.writeFile(filename)
