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



#sizes,shapes,etc]
#prefix, serie, Type, W, L, H, PDiam, pin1x, pin1y, pin2x, pin2y, pin3x, pin3y, pin4x, pin4y
converters = [
    ["ACDC-Conv_Vigortronix", "VTX-214-010-XXX",            0,   56.0, 36.0, 25.5,   1.5,   0, 0,   12, 0,    0, 48,    5, 48 ],
    ["ACDC-Conv_Vigortronix", "VTX-214-010-XXX_Miniature",  0,   45.5, 30.0, 24.0,   1.5,   0, 0,   12, 0,   12, 39,    5, 39,],
]

import sys
import os
import math

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



for converter in converters:
    prefix,Serie,Type,W,L,H,PDiam,pin1x, pin1y, pin2x, pin2y, pin3x, pin3y, pin4x, pin4y=converter

    if Type == 0:

        desc = "Vigortronix " + Serie + " serie of ACDC converter"
        tags = "Vigortronix " + Serie + " serie of ACDC converter"
        TargetDir = "Converters_DCDC_ACDC.3dshapes"
        Datasheet = "http://www.vigortronix.com/10WattACDCPCBPowerModule.aspx"
        PadSize = 2.0 * PDiam
    
        fp_name = prefix + "_" + Serie
        fp = Footprint(fp_name)
        description = desc + ", " + Datasheet

        x1 = 0
        y1 = 0
        x2 = 0
        y2 = 0
        #
        # Add the component outline
        #
        # Top line
        Layer = ['F.Fab', 'F.SilkS', 'F.CrtYd']
        LayerW = [0.1, 0.12, 0.05]
        LayerD = [0, 0.12, 0.25]
        for i in range(0, 3):
            myLayer = Layer[i]
            myLayerW = LayerW[i]
            myLayerD = LayerD[i]
            #
            # Top line
            if (i == 0):
                x1 = 0 - ((L - (pin2x - pin1x)) / 2.0) - myLayerD
                y1 = 0 - ((W - (pin3y - pin1y)) / 2.0) - myLayerD
                x2 = -1
                y2 = y1
                fp.append(Line(start=[round(x1, 2), round(y1, 2)],end=[round(x2, 2), round(y2, 2)],layer=myLayer,width=myLayerW))
                #
                x1 = x2;
                y1 = y2
                x2 = 0
                y2 = y1 + 1
                fp.append(Line(start=[round(x1, 2), round(y1, 2)],end=[round(x2, 2), round(y2, 2)],layer=myLayer,width=myLayerW))
                #
                x1 = x2;
                y1 = y2
                x2 = 1
                y2 = y1 - 1
                fp.append(Line(start=[round(x1, 2), round(y1, 2)],end=[round(x2, 2), round(y2, 2)],layer=myLayer,width=myLayerW))
                #
                x1 = x2;
                y1 = y2
                x2 = L - ((L - (pin2x - pin1x)) / 2.0) + myLayerD
                y2 = y1
                fp.append(Line(start=[round(x1, 2), round(y1, 2)],end=[round(x2, 2), round(y2, 2)],layer=myLayer,width=myLayerW))
                #
            else:
                x1 = 0 - ((L - (pin2x - pin1x)) / 2.0) - myLayerD
                y1 = 0 - ((W - (pin3y - pin1y)) / 2.0) - myLayerD
                x2 = L - ((L - (pin2x - pin1x)) / 2.0) + myLayerD
                y2 = y1
                fp.append(Line(start=[round(x1, 2), round(y1, 2)],end=[round(x2, 2), round(y2, 2)],layer=myLayer,width=myLayerW))
            #
            # Right Line
            #
            x1 = x2
            y1 = y2
            x2 = x1
            y2 = W - ((W - (pin3y - pin1y)) / 2.0) + myLayerD
            fp.append(Line(start=[round(x1, 2), round(y1, 2)],end=[round(x2, 2), round(y2, 2)],layer=myLayer,width=myLayerW))
            #
            # Bottom Line
            #
            x1 = x2
            y1 = y2
            x2 = 0 - ((L - (pin2x - pin1x)) / 2.0) - myLayerD
            y2 = y2
            fp.append(Line(start=[round(x1, 2), round(y1, 2)],end=[round(x2, 2), round(y2, 2)],layer=myLayer,width=myLayerW))
            #
            # Left Line
            #
            x1 = x2
            y1 = y2
            x2 = 0 - ((L - (pin2x - pin1x)) / 2.0) - myLayerD
            y2 = 0 - ((W - (pin3y - pin1y)) / 2.0) - myLayerD
            fp.append(Line(start=[round(x1, 2), round(y1, 2)],end=[round(x2, 2), round(y2, 2)],layer=myLayer,width=myLayerW))
            #
            #
            # Add holes
            #
            if (i == 0):
                fp.append(Pad(number=1,at=[pin1x, pin1y], layers=Pad.LAYERS_THT, shape=Pad.SHAPE_RECT,   type=Pad.TYPE_THT,  size=[PadSize,PadSize], drill=round(PDiam, 2)))
                fp.append(Pad(number=2,at=[pin2x, pin2y], layers=Pad.LAYERS_THT, shape=Pad.SHAPE_CIRCLE, type=Pad.TYPE_THT,  size=[PadSize,PadSize], drill=round(PDiam, 2)))
                fp.append(Pad(number=3,at=[pin3x, pin3y], layers=Pad.LAYERS_THT, shape=Pad.SHAPE_CIRCLE, type=Pad.TYPE_THT,  size=[PadSize,PadSize], drill=round(PDiam, 2)))
                fp.append(Pad(number=4,at=[pin4x, pin4y], layers=Pad.LAYERS_THT, shape=Pad.SHAPE_CIRCLE, type=Pad.TYPE_THT,  size=[PadSize,PadSize], drill=round(PDiam, 2)))

    fp.setTags(tags)
    fp.setDescription(description)
    #
    # Set general values
    #
    cx = 0 - ((L - (pin2x - pin1x)) / 2.0) + 2
    cy = 0 - ((W - (pin3y - pin1y)) / 2.0) - 1.5
    fp.append(Text(type='reference', text='REF**', at=[round(cx, 2), round(cy, 2)], layer='F.SilkS'))
    #
    cx = (pin2x - pin1x) / 2.0
    cy = ((pin3y - pin1y)) - ((L - (pin3y - pin1y)) / 2.0)
    fp.append(Text(type='value', text=fp_name,     at=[round(cx, 2), round(cy, 2)], layer='F.Fab'))
    #
    cx = (L / 2.0) + (0 - ((L - (pin2x - pin1x)) / 2.0) - myLayerD)
    cy = (pin3y - pin1y) / 2.0
    fp.append(Text(type='user', text="%R",         at=[round(cx, 2), round(cy, 2)], layer='F.Fab'))
    
    #
    # Add 3D model
    #
    fp.append(Model(filename="${KISYS3DMOD}/" + TargetDir + "/" + fp_name + ".wrl", at=[0, 0, 0], scale=[1, 1, 1], rotate=[0, 0, 0]))
    

    #filename
    filename = output_dir + fp_name + ".kicad_mod"
    
    file_handler = KicadFileHandler(fp)
    file_handler.writeFile(filename)
    