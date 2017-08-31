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

Molex Picoflex THT top-entry connectors
http://www.molex.com/pdm_docs/sd/530470610_sd.pdf
"""

pitch = 1.27

#pincounts
pincount = (4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26)

#Molex part number
#with plastic PCB retainer, 
part_code = "90325" #n = number of circuits

part_name = "Molex_Picoflex_{part}_{n:02}x{p:.2f}mm_Straight"

#FP description and tags
description = "Molex Picoflex, single row, top entry type, through hole, PN:{pn}"
tags = "connector molex picoflex"

drill = 0.8
size = 1.2


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
        		
        GuideHoleDrillSize = 1.6

        GuideHoleX1 = -1.48
        GuideHoleY1 = -1.8
		
        GuideHoleY2 = (pins - 1) * pitch - GuideHoleY1
		

        SilkRef_X = 0.5
        SilkRef_Y = GuideHoleY1 - GuideHoleDrillSize - 0.5
		
        FabRef_X = pitch
        FabRef_Y = ((pins * pitch) / 2) - 0.5
		
        FabValue_X = pitch
        FabValue_Y = ((pins - 1) * pitch) + 4
		
        StartFX = GuideHoleX1
        StartFY = 0 - 2.755
		
        # set general values
        footprint.append(Text(type='reference', text='REF**', at=[SilkRef_X, SilkRef_Y], layer='F.SilkS'))
        footprint.append(Text(type='value', text=fp_name, at=[FabValue_X, FabValue_Y], layer='F.Fab'))
            
        # add ref-des
        footprint.append(Text(type='user',text='%R', at=[FabRef_X, FabRef_Y],layer='F.Fab'))
            
        # generate the pads
        tpc = int(pins / 2)
        footprint.append(PadArray(start=[0,0], pincount=tpc, initial=1, increment=2, x_spacing=0,  y_spacing=2*pitch, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE, size=size, drill=drill, layers=Pad.LAYERS_THT))
        footprint.append(PadArray(start=[2*pitch, pitch], pincount=tpc, initial=2, increment=2, x_spacing=0,  y_spacing=2*pitch, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE, size=size, drill=drill, layers=Pad.LAYERS_THT))

        # Generate the drill holes
        stx = (pins - 1) * pitch + 1.8
        footprint.append(Pad(at=[GuideHoleX1, GuideHoleY1],type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE, size=GuideHoleDrillSize,drill=GuideHoleDrillSize, layers=["*.Cu"]))
        footprint.append(Pad(at=[GuideHoleX1, GuideHoleY2],type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE, size=GuideHoleDrillSize,drill=GuideHoleDrillSize, layers=["*.Cu"]))
		
		
        #
        # Add F.Fab lines
        #
        x1 = StartFX
        y1 = StartFY
        x2 = x1 + 5
        y2 = y1
        footprint.append(PolygoneLine(polygone=[[x1, y1], [x2, y2]], layer='F.Fab',width=0.1))
        footprint.append(PolygoneLine(polygone=[[x1, y1 - 0.13], [x2 + 0.13, y2 - 0.13]], layer='F.SilkS',width=0.12))
        footprint.append(PolygoneLine(polygone=[[round(x1, 2), round(y1 - 0.25, 2)], [round(x2 + 0.25, 2), round(y2 - 0.25, 2)]], layer='F.CrtYd',width=0.05))

        x1 = x2
        y1 = y2
        x2 = x2
        y2 = ((pins - 1) * pitch) + 2.755
        footprint.append(PolygoneLine(polygone=[[x1, y1], [x2, y2]], layer='F.Fab',width=0.1))
        footprint.append(PolygoneLine(polygone=[[x1 + 0.13, y1 - 0.13], [x2 + 0.13, y2 + 0.13]], layer='F.SilkS',width=0.12))
        footprint.append(PolygoneLine(polygone=[[round(x1 + 0.25, 2), round(y1 - 0.25, 2)], [round(x2 + 0.25, 2), round(y2 + 0.25, 2)]], layer='F.CrtYd',width=0.05))
		
        x1 = x2
        y1 = y2
        x2 = StartFX
        y2 = y2
        footprint.append(PolygoneLine(polygone=[[x1, y1], [x2, y2]], layer='F.Fab',width=0.1))
        footprint.append(PolygoneLine(polygone=[[x1 + 0.13, y1 + 0.13], [x2, y2 + 0.13]], layer='F.SilkS',width=0.12))
        footprint.append(PolygoneLine(polygone=[[round(x1 + 0.25, 2), round(y1 + 0.25, 2)], [round(x2, 2), round(y2 + 0.25, 2)]], layer='F.CrtYd',width=0.05))

        ccx = GuideHoleX1
        ccy = GuideHoleY1
        csx = GuideHoleX1
        csy = -0.85
        footprint.append(Arc(center=[ccx, ccy], start=[csx, csy], angle=180, layer='F.Fab',width=0.1))
        ccx = GuideHoleX1
        ccy = GuideHoleY1
        csx = -1.61
        csy = -0.72
        footprint.append(Arc(center=[ccx, ccy], start=[csx, csy], angle=180, layer='F.SilkS',width=0.12))
        ccx = GuideHoleX1
        ccy = GuideHoleY1
        csx = -1.73
        csy = -0.62
        footprint.append(Arc(center=[ccx, ccy], start=[round(csx, 2), round(csy, 2)], angle=168, layer='F.CrtYd',width=0.05))

        x1 = GuideHoleX1
        y1 = GuideHoleY1 + (GuideHoleY1 - StartFY)
        x2 = GuideHoleX1
        y2 = GuideHoleY2 - (GuideHoleY1 - StartFY)
        x3 = 2
        y3 = -0.5		
        footprint.append(PolygoneLine(polygone=[[x1,y1], [x2, -0.5]], layer='F.Fab',width=0.1))
        footprint.append(PolygoneLine(polygone=[[x2, -0.5], [x2 + 0.5, 0]], layer='F.Fab',width=0.1))
        footprint.append(PolygoneLine(polygone=[[x2 + 0.5, 0], [x2, 0.5]], layer='F.Fab',width=0.1))
        footprint.append(PolygoneLine(polygone=[[x2, 0.5], [x2, y2]], layer='F.Fab',width=0.1))
		
        footprint.append(PolygoneLine(polygone=[[x1 - 0.13, y1 + 0.13], [x2 - 0.13, y2 - 0.13]], layer='F.SilkS',width=0.12))
        footprint.append(PolygoneLine(polygone=[[round(x1 - 0.25, 2), round(y1 + 0.25, 2)], [round(x2 - 0.25, 2), round(y2 - 0.25, 2)]], layer='F.CrtYd',width=0.05))
		
        ccx = GuideHoleX1
        ccy = GuideHoleY2
        csx = GuideHoleX1
        csy = ((pins - 1) * pitch) + 2.755
        footprint.append(Arc(center=[ccx, ccy], start=[csx, csy], angle=180, layer='F.Fab',width=0.1))
        ccx = GuideHoleX1
        ccy = GuideHoleY2
        csx = -1.47
        csy = ((pins - 1) * pitch) + 2.755 + 0.13
        footprint.append(Arc(center=[ccx, ccy], start=[csx, csy], angle=170, layer='F.SilkS',width=0.12))
        ccx = GuideHoleX1
        ccy = GuideHoleY2
        csx = -1.47
        csy = ((pins - 1) * pitch) + 2.755 + 0.25
        footprint.append(Arc(center=[ccx, ccy], start=[round(csx, 2), round(csy, 2)], angle=168, layer='F.CrtYd',width=0.05))
		
        # courtyard
#        footprint.append(RectLine(start=[x1,y1],end=[x2,y2],layer='F.CrtYd',width=0.05))
        
        # outline on Fab
#        footprint.append(RectLine(start=[x1,y1],end=[x2,y2],layer='F.Fab'))
        
#        footprint.append(Circle(center=[x1+T,y2-T],radius=0.2,layer='F.Fab'))
        
        # outline on SilkScreen
#        footprint.append(RectLine(start=[x1,y1],end=[x2,y2],offset=0.15))

        #Add a model
        footprint.append(Model(filename="${KISYS3DMOD}/Connectors_Molex.3dshapes/" + fp_name + ".wrl", at=[0,0], scale=[0,0], rotate=[0,0,0]))
        
        #filename
        filename = output_dir + fp_name + ".kicad_mod"

        file_handler = KicadFileHandler(footprint)
        file_handler.writeFile(filename)
