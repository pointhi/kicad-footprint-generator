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

Molex PicoBlade SMD side-entry connectors
http://www.molex.com/pdm_docs/sd/532610671_sd.pdf
"""

pitch = 1.25

#pincounts
pincount = [i for i in range(2,16)] + [17]

#Molex part number
#with plastic PCB retainer, 
part_code = "53261-{n:02}71" #n = number of circuits

part_name = "Molex_PicoBlade_{part}_{n:02}x{p:.2f}mm_Angled"

#FP description and tags
description = "Molex PicoBlade, single row, side entry type, surface mount, PN:{pn}"
tags = "connector molex picoblade smt"

#pad size
pw = 0.8
ph = 1.7

#mechanical pad size
mw = 2.2
mh = 3.1

#calculate the various y-positions
#center point of pads
YP = 1.6 / 2
YM = 1.6 + 0.6 + 3 / 2

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
        C = A + 3
        D = A + 6
        E = A + 6.4
        
        # set general values
        footprint.append(Text(type='reference', text='REF**', at=[0,-3.5], layer='F.SilkS'))
        footprint.append(Text(type='value', text=fp_name, at=[0,5], layer='F.Fab'))
        
        #add ref-des to F.Fab
        #footprint.append(Text(type='user', text='%R', at=[0,2.5], layer='F.Fab'))
        
        #draw the pins
        footprint.append(PadArray(center=[0,py],size=[pw,ph],pincount=pins,x_spacing=pitch,type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, layers=Pad.LAYERS_SMT))

        #mechanical pins
        mx = A / 2 + 3.6 - mw / 2
        footprint.append(Pad(at=[-mx,my],size=[mw,mh],type=Pad.TYPE_SMT,shape=Pad.SHAPE_RECT,layers=Pad.LAYERS_SMT))
        footprint.append(Pad(at=[ mx,my],size=[mw,mh],type=Pad.TYPE_SMT,shape=Pad.SHAPE_RECT,layers=Pad.LAYERS_SMT))
        
        #connector outline on F.Fab layer
        xf = A/2 + 3.6 - 2.1
        yf2 = py + 0.8
        yf1 = yf2 + 4.2
        
        footprint.append(RectLine(start=[-xf,yf1],end=[xf,yf2],layer='F.Fab'))
        
        #connector 'ear'
        ear = [
            {'x': xf,'y': yf2 + 1},
            {'x': xf + 1.5,'y': yf2 + 1},
            {'x': xf + 1.5,'y': yf2 + 3.8},
            {'x': xf,'y': yf2 + 3.8},
        ]
        
        footprint.append(PolygoneLine(polygone=ear,layer='F.Fab'))
        footprint.append(PolygoneLine(polygone=ear,layer='F.Fab',x_mirror=0))
        
        #add silkscreen where appropriate
        o = 0.15
        po = 0.3
        side = [
            {'x': A/2 + pw/2 + po,'y': yf2 - o},
            {'x': xf + o,'y': yf2 - o},
            {'x': xf + o,'y': my - mh/2 - po},
        ]
        
        footprint.append(PolygoneLine(polygone=side))
        footprint.append(PolygoneLine(polygone=side,x_mirror=0))
        
        bottom = [
            #{'x': xf + 1.5 + o,'y': my + mh/2 + po},
            {'x': xf + o,'y': my + mh/2 + po},
            {'x': xf + o,'y': yf1 + o},
            {'x': 0 ,'y': yf1 + o},
        ]
        
        footprint.append(PolygoneLine(polygone=bottom))
        footprint.append(PolygoneLine(polygone=bottom,x_mirror=0))
        
        #pin-1 marker
        p1_start = [-A/2-pw/2-po,yf2-o]
        p1_end   = [-A/2-pw/2-po,py-ph/2]
        footprint.append(Line(start=p1_start,end=p1_end))
        
        # Add pin-1 marker to F.Fab
        m = pw / 2
        x = -A/2
        y = yf2
        
        pin = [
        {'x': x - m,'y': y},
        {'x': x,'y': y + 2 * m},
        {'x': x + m,'y': y},
        {'x': x - m,'y': y},
        ]
         
        footprint.append(PolygoneLine(polygone=pin, layer='F.Fab'))
        
        #courtyard
        off = 0.6
        xc = mx + mw/2
        yc1 = yf1
        yc2 = py - ph/2
        
        cy = [
            {'x': 0,'y': yc2 - off},
            {'x': -A/2 - pw/2 - 0.2 - off,'y': yc2 - off},
            {'x': -A/2 - pw/2 - 0.2 - off,'y': yf2 - off},
            {'x': -xc - off,'y': yf2 - off},
            {'x': -xc - off,'y': yf1 + off},
            {'x': 0,'y': yf1 + off},
        ]
        
        footprint.append(PolygoneLine(polygone=cy, layer='F.CrtYd', width=0.05, grid=0.05))
        footprint.append(PolygoneLine(polygone=cy, layer='F.CrtYd', width=0.05, grid=0.05, x_mirror=0))

        #Add a model
        footprint.append(Model(filename="Connectors_Molex.3dshapes/" + fp_name + ".wrl"))
        
        #filename
        filename = output_dir + fp_name + ".kicad_mod"

        file_handler = KicadFileHandler(footprint)
        file_handler.writeFile(filename)
