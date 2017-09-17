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

Datasheet: http://www.molex.com/pdm_docs/sd/430450215_sd.pdf

"""
pitch = 3.0

pincount = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24]

#Molex part number
part = "43045-{n:02}{serie:02}"

prefix = "Molex_MicroFit_3.0-{pn}_"
suffix = "{n:02}x{p:.2f}mm_Straight"

PadSiseX = 1.27
PadSiseY = 2.54
PadDist = 6.86 + PadSiseY

DrillSize = 2.41


serieA =   [[15, 0, "http://www.molex.com/pdm_docs/sd/430450215_sd.pdf"], 
            [16, 0, "http://www.molex.com/pdm_docs/sd/430450216_sd.pdf"], 
            [17, 0, "http://www.molex.com/pdm_docs/sd/430450217_sd.pdf"],
            [18, 1, "http://www.molex.com/pdm_docs/sd/430450218_sd.pdf"],
            [19, 1, "http://www.molex.com/pdm_docs/sd/430450219_sd.pdf"]]


#FP description and tags

if __name__ == '__main__':


    for serieL in serieA:
        serie = serieL[0]
        socketType = serieL[1]
        datasheet = serieL[2]

        for pins in pincount:
            
            pn = part.format(n=pins, serie=serie)

            #generate the name
            fp_name = prefix.format(pn=pn) + suffix.format(n=pins, p=pitch)
            
            print(fp_name)

            footprint = Footprint(fp_name)
            
            description = "Molex Micro-Fit 3.0 connector, PN:" + pn + ", top entry type, SMD" + datasheet
            
            #set the FP description
            footprint.setDescription(description)
            
            tags = "conn molex micro fit 3.0"
            
            #set the FP tags
            footprint.setTags(tags)
            footprint.setAttribute('smd')
            
            # Calculate dimensions
            if (pins < 4):
                B = 0
            else:
                B = ((pins / 2) - 1) * pitch
            
            A = B + 6.65
            if (socketType == 0):
                C = B + 4.3
            else:
                C = B + 11.2
                
            D = PadDist + PadSiseY
            
            # Center
            cx = 0
            cy = 0

            ValY = 0
            RefX = 0
            RefY = round(0 - ((A / 2) + 2), 2)
            #
            # Set general values
            if (socketType == 0):
                ValY = round(((A / 2) + 2), 2)
                RefX = 0 - (D / 3)
            else:
                ValY = round(((A / 2) + 4), 2)
                RefX = 0 - (D / 3)
            #
            footprint.append(Text(type='user', text='%R', at=[cx, cy], layer='F.Fab'))
            footprint.append(Text(type='reference', text='REF**', at=[RefX, RefY], layer='F.SilkS'))
            footprint.append(Text(type='value', text=fp_name, at=[0, ValY], layer='F.Fab'))
            # Add 3D model
            footprint.append(Model(filename="${KISYS3DMOD}/Connectors_Molex.3dshapes/" + fp_name + ".wrl", at=[0,0], scale=[0,0], rotate=[0,0,0]))
            #
            if (socketType == 0):
                # Add drill hole
                y1 =(cx - (C / 2))
                x1 = 0
                footprint.append(Pad(at=[round(x1, 2), round(y1, 2)],type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE, size=DrillSize,drill=DrillSize, layers=["*.Cu"]))
                y1 = round((cx + (C / 2)), 2)
                footprint.append(Pad(at=[round(x1, 2), round(y1, 2)],type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE, size=DrillSize,drill=DrillSize, layers=["*.Cu"]))
            else:
                y1 = cx - ((C - 3.43) / 2)
                x1 = 0
                footprint.append(Pad(at=[round(x1, 2), round(y1, 2)], number="", increment=0,  x_spacing=0,  y_spacing=(C - 3.43), type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, size=[1.65, 3.43], drill=[0, 0], layers=Pad.LAYERS_SMT))                
                y1 = cx + ((C - 3.43) / 2)
                footprint.append(Pad(at=[round(x1, 2), round(y1, 2)], number="", increment=0,  x_spacing=0,  y_spacing=(C - 3.43), type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, size=[1.65, 3.43], drill=[0, 0], layers=Pad.LAYERS_SMT))                
#                footprint.append(PadArray(start=[round(x1, 2), round(y1, 2)], pincount=2, initial=-1,          increment=0,  x_spacing=0,  y_spacing=(C - 3.43), type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, size=[1.65, 3.43], drill=[0, 0], layers=Pad.LAYERS_SMT))
            
            #
            # Add pads
            #
            pinsi = int(pins / 2)
            footprint.append(PadArray(start=[round(0 - (PadDist / 2), 2), round((0 - (B / 2)), 2)], pincount=pinsi, initial=1,    increment=1,  x_spacing=0,  y_spacing=pitch, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, size=[PadSiseY, PadSiseX], drill=[0, 0], layers=Pad.LAYERS_SMT))
            footprint.append(PadArray(start=[round((PadDist / 2), 2),     round((0 - (B / 2)), 2)], pincount=pinsi, initial=pins, increment=-1, x_spacing=0,  y_spacing=pitch, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, size=[PadSiseY, PadSiseX], drill=[0, 0], layers=Pad.LAYERS_SMT))
            
            #
            # Add F.Fab
            #
            LayerA = ['F.Fab', 'F.SilkS', 'F.CrtYd']
            LineDXA = [0, 0.12, 0.25]
            LindeDeltaA = [0, 0.2, 0.2]
            LineWidthA = [0.1, 0.12, 0.05]
            for i in range(0,3):
                LineDX = LineDXA[i]
                Layer = LayerA[i]
                LineWidth = LineWidthA[i]
                LindeDelta = LindeDeltaA[i]
                points = []
                
                if (socketType == 0):
                    points.append([round(0, 2),                                         round(0 - ((A / 2) + LineDX), 2)])
                    points.append([round(3.43 + LineDX, 2),                             round(0 - ((A / 2) + LineDX), 2)])
                    points.append([round(3.43 + LineDX, 2),                             round(0 - ((B / 2) + (PadSiseX / 2) + LineDX + LindeDelta), 2)])
                else:
                    if (i == 0):
                        # Pass throught the top pad
                        points.append([round(0, 2),                                     round(0 - ((C / 2) - 2.0 + LineDX), 2)])
                        points.append([round(3.43 + LineDX, 2),                         round(0 - ((C / 2) - 2.0 + LineDX), 2)])
                    if (i == 1):
                        # Draw to the top pad
                        points.append([round(1.65 / 2 + LineDX + LindeDelta, 2),        round(0 - ((C / 2) - 2.0 + LineDX), 2)])
                        points.append([round(3.43 + LineDX, 2),                         round(0 - ((C / 2) - 2.0 + LineDX), 2)])
                    elif (i == 2):
                        # Draw around the top pad
                        points.append([round(0, 2),                                     round(0 - ((C / 2) + LineDX + LindeDelta), 2)])
                        points.append([round(1.65 / 2 + LineDX + LindeDelta, 2),        round(0 - ((C / 2) + LineDX + LindeDelta), 2)])
                        points.append([round(1.65 / 2 + LineDX + LindeDelta, 2),        round(0 - ((C / 2) - 2.0 + LineDX), 2)])
                        points.append([round(3.43 + LineDX, 2),                         round(0 - ((C / 2) - 2.0 + LineDX), 2)])

                points.append([round(3.43 + LineDX, 2),                                 round(0 - ((B / 2) + (PadSiseX / 2) + LineDX + LindeDelta), 2)])

                footprint.append(PolygoneLine(polygone=points, layer=Layer, width=LineWidth))
                points = []
                #
                #
                if (i == 0):
                    # Pass throught the right pad
                    points.append([round(3.43 + LineDX, 2),                        round(0 - ((B / 2) + (PadSiseX / 2) + LineDX + LindeDelta), 2)])
                if (i == 1):
                    # Draw to the right pad
                    points.append([round((3.43 + LineDX), 2),                          round(((B / 2) + (PadSiseX / 2) + LineDX + LindeDelta), 2)])
                elif (i == 2):
                    # Draw around the right pad
                    points.append([round(3.43 + LineDX, 2),                        round(0 - ((B / 2) + (PadSiseX / 2) + LineDX + LindeDelta), 2)])
                    points.append([round(((D / 2) + LineDX + LindeDelta), 2),          round(0 - ((B / 2) + (PadSiseX / 2) + LineDX + LindeDelta), 2)])
                    points.append([round(((D / 2) + LineDX + LindeDelta), 2),          round(((B / 2) + (PadSiseX / 2) + LineDX + LindeDelta), 2)]) 
                    points.append([round((3.43 + LineDX), 2),                          round(((B / 2) + (PadSiseX / 2) + LineDX + LindeDelta), 2)])
                 
                #
                #
                if (socketType == 0):
                    points.append([round((3.43 + LineDX), 2),                      round(A / 2 + LineDX, 2)])
                    points.append([round(0, 2),                                    round((A / 2) + LineDX, 2)]) 
                    points.append([round(0 - (3.94 + LineDX), 2),                  round((A / 2) + LineDX, 2)])
                else:
                    if (i == 0):
                        # Pass throught the bottom pad
                        points.append([round(3.43 + LineDX, 2),                        round(((B / 2) + (PadSiseX / 2) + LineDX + LindeDelta), 2)])
                        points.append([round(3.43 + LineDX, 2),                        round(((C / 2) - 2.0 + LineDX), 2)])
                    if (i == 1):
                        # Draw to the bottom pad
                        points.append([round(3.43 + LineDX, 2),                        round(((B / 2) + (PadSiseX / 2) + LineDX + LindeDelta), 2)])
                        points.append([round(3.43 + LineDX, 2),                        round(((C / 2) - 2.0 + LineDX), 2)])
                        points.append([round(1.65 / 2 + LineDX + LindeDelta, 2),       round(((C / 2) - 2.0 + LineDX), 2)])
                        footprint.append(PolygoneLine(polygone=points, layer=Layer, width=LineWidth))
                        points = []
                    elif (i == 2):
                        # Draw around the bottom pad
                        points.append([round(3.43 + LineDX, 2),                        round(((B / 2) + (PadSiseX / 2) + LineDX + LindeDelta), 2)])
                        points.append([round(3.43 + LineDX, 2),                        round(((C / 2) - 2.0 + LineDX), 2)])
                        points.append([round(1.65 / 2 + LineDX + LindeDelta, 2),       round(((C / 2) - 2.0 + LineDX), 2)])
                        points.append([round(1.65 / 2 + LineDX + LindeDelta, 2),       round(((C / 2) + LineDX + LindeDelta), 2)])
                        points.append([round(0, 2),                                    round(((C / 2) + LineDX + LindeDelta), 2)])
                        points.append([round(0 - (1.65 / 2 + LineDX + LindeDelta), 2), round(((C / 2) + LineDX + LindeDelta), 2)])
                
                    points.append([round(0 - (1.65 / 2 + LineDX + LindeDelta), 2), round(((C / 2) - 2.0 + LineDX), 2)])
                    points.append([round(0 - (3.94 + LineDX), 2),                  round(((C / 2) - 2.0 + LineDX), 2)])

                #
                points.append([round(0 - (3.94 + LineDX), 2),                      round(((B / 2) + (PadSiseX / 2) + LineDX + LindeDelta), 2)]) 
                #
                footprint.append(PolygoneLine(polygone=points, layer=Layer, width=LineWidth))
                points = []
                #
                #
                if (i == 0):
                    # Draw line through left pad
                    points.append([round(0 - (3.94 + LineDX), 2),                  round(((B / 2) + (PadSiseX / 2) + LineDX + LindeDelta), 2)]) 
                if (i == 1):
                    # Draw line to left pad
                    points.append([round(0 - ((D / 2) + LineDX + LindeDelta), 2),  round(0 - ((B / 2) + (PadSiseX / 2) + LineDX + LindeDelta), 2)])
                    points.append([round(0 - (3.94 + LineDX), 2),                  round(0 - ((B / 2) + (PadSiseX / 2) + LineDX + LindeDelta), 2)]) 
                elif (i == 2):
                    # Draw line around left pad
                    points.append([round(0 - (3.94 + LineDX), 2),                  round(((B / 2) + (PadSiseX / 2) + LineDX + LindeDelta), 2)]) 
                    points.append([round(0 - ((D / 2) + LineDX + LindeDelta), 2),  round(((B / 2) + (PadSiseX / 2) + LineDX + LindeDelta), 2)])
                    points.append([round(0 - ((D / 2) + LineDX + LindeDelta), 2),  round(0 - ((B / 2) + (PadSiseX / 2) + LineDX + LindeDelta), 2)])
                    points.append([round(0 - (3.94 + LineDX), 2),                  round(0 - ((B / 2) + (PadSiseX / 2) + LineDX + LindeDelta), 2)])
                    
                if (socketType == 0):
                    if (i == 0):
                        # Make the chamfer
                        points.append([round(0 - (3.94 + LineDX), 2),              round(0 - ((A / 2) + LineDX - 1), 2)]);
                        points.append([round(0 - (3.94 + LineDX - 1), 2),          round(0 - ((A / 2) + LineDX), 2)]);
                    else:
                        points.append([round(0 - (3.94 + LineDX), 2),              round(0 - ((A / 2) + LineDX), 2)]);
                        
                    points.append([round(0, 2),                                    round(0 - ((A / 2) + LineDX), 2)]);
                else:
                    if (i == 0):
                        # Make the chamfer
                        points.append([round(0 - (3.94 + LineDX), 2),              round(0 - ((A / 2) + LineDX - 1), 2)]);
                        points.append([round(0 - (3.94 + LineDX - 1), 2),          round(0 - ((C / 2) - 2.0 + LineDX), 2)]);
                        points.append([round(0, 2),                                round(0 - ((C / 2) - 2.0 + LineDX), 2)]);
                    elif (i == 1):
                        # 
                        points.append([round(0 - (3.94 + LineDX), 2),                  round(0 - ((C / 2) - 2.0 + LineDX), 2)]);
                        points.append([round(0 - (3.94 + LineDX), 2),                  round(0 - ((C / 2) - 2.0 + LineDX), 2)]);
                        points.append([round(0 - (1.65 / 2 + LineDX + LindeDelta), 2), round(0 - ((C / 2) - 2.0 + LineDX), 2)])
                    else:
                        points.append([round(0 - (3.94 + LineDX), 2),                  round(0 - ((C / 2) - 2.0 + LineDX), 2)]);
                        points.append([round(0 - (3.94 + LineDX), 2),                  round(0 - ((C / 2) - 2.0 + LineDX), 2)]);
                        points.append([round(0 - (1.65 / 2 + LineDX + LindeDelta), 2), round(0 - ((C / 2) - 2.0 + LineDX), 2)])
                        points.append([round(0 - (1.65 / 2 + LineDX + LindeDelta), 2), round(0 - ((C / 2) + LineDX + LindeDelta), 2)])
                        points.append([round(0, 2),                                    round(0 - ((C / 2) + LineDX + LindeDelta), 2)])
                
                footprint.append(PolygoneLine(polygone=points, layer=Layer, width=LineWidth))
            
            #
            
            #filename
            filename = output_dir + fp_name + ".kicad_mod"
            
            file_handler = KicadFileHandler(footprint)
            file_handler.writeFile(filename)
