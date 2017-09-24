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

Molex Picoflex SMD top-entry connectors
http://www.molex.com/pdm_docs/sd/908140004_sd.pdf
"""

pitch = 1.27

#pincounts
pincount = (4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26)

#Molex part number
#with plastic PCB retainer, 
part_code = "90814" #n = number of circuits

part_name = "Molex_Picoflex_{part}_{n:02}x{p:.2f}mm_Straight"

#FP description and tags
description = "Molex Picoflex, single row, top entry type, SMD, PN:{pn}"
tags = "connector molex picoflex"


if __name__ == '__main__':

    for pins in pincount:
        
        pn = part_code.format(n=pins)
        
        #generate the name
        fp_name = part_name.format(n=pins, p=pitch, part=pn)
        footprint = Footprint(fp_name)
        
        print(fp_name)
        
        #
        #set the FP description
        #
        footprint.setDescription(description.format(pn=pn)) 
        
        #
        #set the FP tags
        #
        footprint.setTags(tags)
        footprint.setAttribute('smd')

        #
        # Add a model
        #
        footprint.append(Model(filename="${KISYS3DMOD}/Connectors_Molex.3dshapes/" + fp_name + ".wrl", at=[0, 0, 0], scale=[1, 1, 1], rotate=[0, 0, 0]))
        
        #
        # Filename
        #
        filename = output_dir + fp_name + ".kicad_mod"

        #
        # Draw all graphical objects
        #
        BodyWidth = 4.1
        BodyHeight = ((pins - 1) * pitch) + (2 * 2.525)
        #
        HalfBodyWidth = BodyWidth / 2
        HalfBodyHeight = BodyHeight / 2

        PadWidth = 2
        PadHeight = 1.2
		#
        AllPadsWidth = 6
        AllPadsHeight = ((pins - 1) * pitch)
        #
        HalfAllPadsWidth = AllPadsWidth / 2
        HalfAllPadsHeight = AllPadsHeight / 2

        GuideHoleDrillSize = 1.9
		
        GuideHoleX1 = 1.1 - HalfAllPadsWidth
        GuideHoleY1 = -1.925 - HalfAllPadsHeight
		
        GuideHoleX1 = 1.1 - HalfAllPadsWidth
        GuideHoleY2 = 1.925 + HalfAllPadsHeight

        FabRef_X = 0
        FabRef_Y = 0

        SilkRef_X = 0
        SilkRef_Y = GuideHoleY1 - 2.5

        FabValue_X = pitch - HalfAllPadsWidth
        FabValue_Y = (HalfAllPadsHeight + 5)

        KeepOutAreaWidth = 7.9
        KeepOutAreaHeight = BodyHeight
        #
        # Set general values
        #
        footprint.append(Text(type='reference', text='REF**', at=[round(SilkRef_X, 2),  round(SilkRef_Y, 2)],  layer='F.SilkS'))
        footprint.append(Text(type='value',     text=fp_name, at=[round(FabValue_X, 2), round(FabValue_Y, 2)], layer='F.Fab'))
        footprint.append(Text(type='user',      text='%R',    at=[round(FabRef_X, 2),   round(FabRef_Y, 2)],   rotation=90., layer='F.Fab'))
        footprint.append(Text(type='user',      text='KEEPOUT', at=[round(0, 2),  round(KeepOutAreaHeight / 4, 2)],  layer='Cmts.User'))

        #
        # Generate the pads
        #
        tpc = int(pins / 2)
        footprint.append(PadArray(start=[round(0 - HalfAllPadsWidth, 2), round(0 - HalfAllPadsHeight, 2)],     pincount=tpc, initial=1, increment=2, x_spacing=0,  y_spacing=2*pitch, size=[PadWidth, PadHeight], type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, layers=Pad.LAYERS_SMT))
        footprint.append(PadArray(start=[round(HalfAllPadsWidth, 2),     round(pitch - HalfAllPadsHeight, 2)], pincount=tpc, initial=2, increment=2, x_spacing=0,  y_spacing=2*pitch, size=[PadWidth, PadHeight], type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, layers=Pad.LAYERS_SMT))

        #
        # Generate the drill holes
        #
        footprint.append(Pad(at=[GuideHoleX1, GuideHoleY1],type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE, size=GuideHoleDrillSize,drill=GuideHoleDrillSize, layers=["*.Cu"]))
        footprint.append(Pad(at=[GuideHoleX1, GuideHoleY2],type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE, size=GuideHoleDrillSize,drill=GuideHoleDrillSize, layers=["*.Cu"]))

        #
        # Add the Fab line
        #
        # Start in upper right corner
        x1 = HalfBodyWidth
        y1 = 0 - HalfBodyHeight
        x2 = x1
        y2 = y1 + BodyHeight
        footprint.append(PolygoneLine(polygone=[[round(x1, 2), round(y1, 2)],        [round(x2, 2),        round(y2, 2)]],        layer='F.Fab',width=0.1))
        #
        # Bottom line to bottom drill hole
        x1 = x2
        y1 = y2
        x2 = GuideHoleX1 + (GuideHoleDrillSize / 2)
        y2 = y2
        footprint.append(PolygoneLine(polygone=[[round(x1, 2), round(y1, 2)],        [round(x2, 2),        round(y2, 2)]],        layer='F.Fab',width=0.1))
        # Arc around bottom drill hole
        ccx = GuideHoleX1
        ccy = GuideHoleY2
        csx = x2
        csy = HalfAllPadsHeight + 2.525
        footprint.append(Arc(center=[round(ccx, 2), round(ccy, 2)], start=[round(csx, 2), round(csy, 2)], angle=230.0, layer='F.Fab',width=0.1))
        # Left line from bottom drill hole to top drill hole including the Fab Pin 1 marker
        x1 = -HalfBodyWidth
        y1 = GuideHoleY2 - (GuideHoleDrillSize / 2) - 0.17
        x2 = x1
        y2 = 0 - (HalfAllPadsHeight - (PadHeight / 2))
        footprint.append(PolygoneLine(polygone=[[round(x1, 2), round(y1, 2)],        [round(x2, 2),        round(y2, 2)]],        layer='F.Fab',width=0.1))
        x1 = x2
        y1 = y2
        x2 = x1 + (PadHeight / 2)
        y2 = y2 - (PadHeight / 2)
        footprint.append(PolygoneLine(polygone=[[round(x1, 2), round(y1, 2)],        [round(x2, 2),        round(y2, 2)]],        layer='F.Fab',width=0.1))
        x1 = x2
        y1 = y2
        x2 = x1 - (PadHeight / 2)
        y2 = y2 - (PadHeight / 2)
        footprint.append(PolygoneLine(polygone=[[round(x1, 2), round(y1, 2)],        [round(x2, 2),        round(y2, 2)]],        layer='F.Fab',width=0.1))
        x1 = x2
        y1 = y2
        x2 = x1
        y2 = GuideHoleY1 + (GuideHoleDrillSize / 2) + 0.17
        footprint.append(PolygoneLine(polygone=[[round(x1, 2), round(y1, 2)],        [round(x2, 2),        round(y2, 2)]],        layer='F.Fab',width=0.1))

        # Arc around top drill hole
        ccx = GuideHoleX1
        ccy = GuideHoleY1
        csx = x1
        csy = y2
        footprint.append(Arc(center=[round(ccx, 2), round(ccy, 2)], start=[round(csx, 2), round(csy, 2)], angle=230.0, layer='F.Fab',width=0.1))
        # Top line to top drill hole
        x1 = HalfBodyWidth
        y1 = 0 - HalfBodyHeight
        x2 = GuideHoleX1 + (GuideHoleDrillSize / 2) + 0.02
        y2 = y1
        footprint.append(PolygoneLine(polygone=[[round(x1, 2), round(y1, 2)],        [round(x2, 2),        round(y2, 2)]],        layer='F.Fab',width=0.1))
		
        #
        # Add the Silk line
        #
        # Start in upper right corner
        x1 = HalfBodyWidth + 0.13
        y1 = 0 - HalfBodyHeight - 0.13
        x2 = x1
        y2 = 0 - ((HalfAllPadsHeight - pitch) + (PadHeight / 2) + 0.3)
        footprint.append(PolygoneLine(polygone=[[round(x1, 2), round(y1, 2)],        [round(x2, 2),        round(y2, 2)]],        layer='F.SilkS',width=0.12))
        y1 = 0 - ((HalfAllPadsHeight - pitch) - (PadHeight / 2) - 0.4)
        y2 = 0 - ((HalfAllPadsHeight - (3 *pitch)) + (PadHeight / 2) + 0.4)
        footprint.append(PolygoneLine(polygone=[[round(x1, 2), round(y1, 2)],        [round(x2, 2),        round(y2, 2)]],        layer='F.SilkS',width=0.12))
        if (pins > 3):
            for halfpins in range(int((pins / 2)) - 2):
              y1 = y1 + (2 * pitch)
              y2 = y2 + (2 * pitch)
              footprint.append(PolygoneLine(polygone=[[round(x1, 2), round(y1 + 0.06, 2)],        [round(x2, 2),        round(y2 - 0.06, 2)]],        layer='F.SilkS',width=0.12))

        x1 = x1
        y1 = HalfAllPadsHeight + (PadHeight / 2) + 0.3
        x2 = HalfBodyWidth + 0.13
        y2 = HalfBodyHeight + 0.13
        footprint.append(PolygoneLine(polygone=[[round(x1, 2), round(y1, 2)],        [round(x2, 2),        round(y2, 2)]],        layer='F.SilkS',width=0.12))
        #
        # Bottom line to bottom drill hole
        x1 = x2
        y1 = y2
        x2 = GuideHoleX1 + (GuideHoleDrillSize / 2) + 0.1
        y2 = y2
        footprint.append(PolygoneLine(polygone=[[round(x1, 2), round(y1, 2)],        [round(x2, 2),        round(y2, 2)]],        layer='F.SilkS',width=0.12))
        # Arc around bottom drill hole
        ccx = GuideHoleX1
        ccy = GuideHoleY2
        csx = x2
        csy = y2
        footprint.append(Arc(center=[round(ccx, 2), round(ccy, 2)], start=[round(csx, 2), round(csy, 2)], angle=222.8, layer='F.SilkS',width=0.12))
        # Left line from bottom drill hole to top drill hole
        x1 = -HalfBodyWidth - 0.13
        y1 = GuideHoleY2 - (GuideHoleDrillSize / 2) - 0.3
        x2 = x1
        y2 = y1 - 0.5
        y2 = HalfAllPadsHeight - pitch + (PadHeight / 2) + 0.3
        footprint.append(PolygoneLine(polygone=[[round(x1, 2), round(y1, 2)],        [round(x2, 2),        round(y2, 2)]],        layer='F.SilkS',width=0.12))
        y1 = ((HalfAllPadsHeight - pitch) - (PadHeight / 2) - 0.4)
        y2 = ((HalfAllPadsHeight - (3 *pitch)) + (PadHeight / 2) + 0.4)
        footprint.append(PolygoneLine(polygone=[[round(x1, 2), round(y1, 2)],        [round(x2, 2),        round(y2, 2)]],        layer='F.SilkS',width=0.12))
        # Add small lines between pads
        if (pins > 3):
            for halfpins in range(int((pins / 2)) - 2):
                y1 = y1 - (2 * pitch)
                y2 = y2 - (2 * pitch)
                footprint.append(PolygoneLine(polygone=[[round(x1, 2), round(y1 + 0.06, 2)],        [round(x2, 2),        round(y2 - 0.06, 2)]],        layer='F.SilkS',width=0.12))


        # Arc around top drill hole
        y2 = GuideHoleY1 + (GuideHoleDrillSize / 2) + 0.3
        ccx = GuideHoleX1
        ccy = GuideHoleY1
        csx = x1 - 0.63
        csy = y2 -0.35
        #
        # xxx, yyy is the new pin 1 marker
        #
        xxx1 = csx
        yyy1 = csy
        xxx2 = xxx1
        yyy2 = 0 - (HalfAllPadsHeight + (PadHeight / 2) + 0.3)
        footprint.append(PolygoneLine(polygone=[[round(xxx1, 2), round(yyy1, 2)],        [round(xxx2, 2),        round(yyy2, 2)]],        layer='F.SilkS',width=0.12))
        xxx1 = xxx2
        yyy1 = yyy2
        xxx2 = 0 - (HalfAllPadsWidth + (PadWidth / 2))
        yyy2 = yyy1
        footprint.append(PolygoneLine(polygone=[[round(xxx1, 2), round(yyy1, 2)],        [round(xxx2, 2),        round(yyy2, 2)]],        layer='F.SilkS',width=0.12))
        #
        footprint.append(Arc(center=[round(ccx, 2), round(ccy, 2)], start=[round(csx, 2), round(csy, 2)], angle=191.0, layer='F.SilkS',width=0.12))
        # Top line to top drill hole
        x1 = HalfBodyWidth + 0.13
        y1 = 0 - HalfBodyHeight - 0.13
        x2 = GuideHoleX1 + (GuideHoleDrillSize / 2) + 0.13
        y2 = y1
        footprint.append(PolygoneLine(polygone=[[round(x1, 2), round(y1, 2)],        [round(x2, 2),        round(y2, 2)]],        layer='F.SilkS',width=0.12))
		
        #
        # Add the courtyard line
        #
        # Start in upper right corner
        x1 = HalfAllPadsWidth + (PadWidth / 2) + 0.25
        y1 = 0 - HalfBodyHeight - 0.25
        x2 = x1
        y2 = y1 + BodyHeight + 0.5
        footprint.append(PolygoneLine(polygone=[[round(x1, 2), round(y1, 2)],        [round(x2, 2),        round(y2, 2)]],        layer='F.CrtYd',width=0.05))
        # Bottom line to bottom drill hole
        x1 = x2
        y1 = y2
        x2 = GuideHoleX1 + (GuideHoleDrillSize / 2) + 0.18
        y2 = y2
        footprint.append(PolygoneLine(polygone=[[round(x1, 2), round(y1, 2)],        [round(x2, 2),        round(y2, 2)]],        layer='F.CrtYd',width=0.05))
        # Arc around bottom drill hole
        ccx = GuideHoleX1
        ccy = GuideHoleY2
        csx = x2
        csy = y2
        footprint.append(Arc(center=[round(ccx, 2), round(ccy, 2)], start=[round(csx, 2), round(csy, 2)], angle=143.1, layer='F.CrtYd',width=0.05))
        # Bottom line from bottom drill hole to left line
        x1 = GuideHoleX1 - (GuideHoleDrillSize / 2) - 0.47
        y1 = GuideHoleY2
        x2 = 0 - (HalfAllPadsWidth + (PadWidth / 2) + 0.25)
        y2 = GuideHoleY2
        footprint.append(PolygoneLine(polygone=[[round(x1, 2), round(y1, 2)],        [round(x2, 2),        round(y2, 2)]],        layer='F.CrtYd',width=0.05))
        # Left line from bottom drill hole to top drill hole
        x1 = 0 - (HalfAllPadsWidth + (PadWidth / 2) + 0.25)
        y1 = GuideHoleY2
        x2 = x1
        y2 = GuideHoleY1
        footprint.append(PolygoneLine(polygone=[[round(x1, 2), round(y1, 2)],        [round(x2, 2),        round(y2, 2)]],        layer='F.CrtYd',width=0.05))
        # Top line from left line to top drill hole
        x1 = GuideHoleX1 - (GuideHoleDrillSize / 2) - 0.47
        y1 = GuideHoleY1
        x2 = 0 - (HalfAllPadsWidth + (PadWidth / 2) + 0.25)
        y2 = GuideHoleY1
        footprint.append(PolygoneLine(polygone=[[round(x1, 2), round(y1, 2)],        [round(x2, 2),        round(y2, 2)]],        layer='F.CrtYd',width=0.05))
        # Arc around top drill hole
        ccx = GuideHoleX1
        ccy = GuideHoleY1
        csx = x1
        csy = y2
        footprint.append(Arc(center=[round(ccx, 2), round(ccy, 2)], start=[round(csx, 2), round(csy, 2)], angle=143.5, layer='F.CrtYd',width=0.05))
        # Top line to top drill hole
        x1 = HalfAllPadsWidth + (PadWidth / 2) + 0.25
        y1 = 0 - HalfBodyHeight - 0.25
        x2 = GuideHoleX1 + (GuideHoleDrillSize / 2) + 0.185
        y2 = y1
        footprint.append(PolygoneLine(polygone=[[round(x1, 2), round(y1, 2)],        [round(x2, 2),        round(y2, 2)]],        layer='F.CrtYd',width=0.05))

        #
        # Add the pin 1 marker
        #
        # Start in upper right corner
#        x1 = 0 - (HalfAllPadsWidth + (PadWidth / 2) + 0.25 + 0.25)
#        y1 = 0 - HalfAllPadsHeight - 1
#        x2 = x1
#        y2 = round(y1 + 3, 0)
#        footprint.append(PolygoneLine(polygone=[[round(x1, 2), round(y1, 2)],        [round(x2, 2),        round(y2, 2)]],        layer='F.SilkS',width=0.12))

        #
        # Add the keep out area
        #
        x1 = 0 - (KeepOutAreaWidth / 2)
        y1 = 0 - (KeepOutAreaHeight / 2)
        x2 = x1 + KeepOutAreaWidth
        y2 = y1 + KeepOutAreaHeight
        footprint.append(RectLine(start=[round(x1, 2), round(y1, 2)], end=[round(x2, 2),        round(y2, 2)],        layer='Dwgs.User',width=0.1))
        x1 = 0 - (KeepOutAreaWidth / 2)
        y1 = 0 - (KeepOutAreaHeight / 2)
        x2 = 0 - (KeepOutAreaWidth / 2)
        y2 = 0 - (KeepOutAreaHeight / 2)
        GridDelta = 2 * pitch
        dx1 = 0
        dy1 = GridDelta
        yy1 = y1;
        while (x1 < (KeepOutAreaWidth / 2)):
            y1 = y1 + GridDelta
            yy1 = yy1 + dy1
            if (y1 > ((KeepOutAreaHeight / 2))):
                yy1 = (KeepOutAreaHeight / 2)
                dy1 = 0
                dx1 = y1 - (KeepOutAreaHeight / 2)
                x1 = (0 - (KeepOutAreaWidth / 2)) + dx1
            x2 = x2 + GridDelta
            if (x2 >= ((KeepOutAreaWidth / 2))):
                x2 = (KeepOutAreaWidth / 2)
                y2 = y1 - KeepOutAreaWidth
            if (x1 < (KeepOutAreaWidth / 2)):
                footprint.append(PolygoneLine(polygone=[[round(x1, 2), round(yy1, 2)],        [round(x2, 2),        round(y2, 2)]],        layer='Dwgs.User',width=0.1))


		
        #
        # Write to the file
        #
        file_handler = KicadFileHandler(footprint)
        file_handler.writeFile(filename)
