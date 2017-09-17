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


pitch = 3.0
pincount = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24]

#Molex part number
part = "43045-{n:02}{serie:02}"

prefix = "Molex_MicroFit_3.0-{pn}_"
suffix = "{n:02}x{p:.2f}mm_Angled"

PadSiseX = 1.27
PadSiseY = 2.92
PadDist = 1.71 + PadSiseY

DrillSize = 2.41


serieA =   [[10, 0, "http://www.molex.com/pdm_docs/sd/430450210_sd.pdf"], 
            [11, 0, "http://www.molex.com/pdm_docs/sd/430450211_sd.pdf"]]


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
            C = B + 11.2
            D = PadDist + PadSiseY
            
            # Center
            cx = 0
            cy = 0

            #
            # Set general values
            RRY  = round(-5.305)
            ValY = round(cy + ((PadDist / 2 ) + (PadSiseY / 2)) + 2, 2)
            RefX = round(0 - ((A / 2) - 4), 2)
            RefY = round(cy - (11.56 - ((PadDist / 2 ) + (PadSiseY / 2)) + 6), 2)
            #
            footprint.append(Text(type='user', text='%R', at=[cx, RRY], layer='F.Fab'))
            footprint.append(Text(type='reference', text='REF**', at=[RefX, RefY], layer='F.SilkS'))
            footprint.append(Text(type='value', text=fp_name, at=[0, ValY], layer='F.Fab'))
            # Add 3D model
            footprint.append(Model(filename="${KISYS3DMOD}/Connectors_Molex.3dshapes/" + fp_name + ".wrl", at=[0,0], scale=[0,0], rotate=[0,0,0]))
            #
            # Add solder nails
            #
            x1 = ((C - 3.42) / 2)
            snx = x1
            y1 = cx - (7.785)
            sny = y1
            footprint.append(Pad(at=[round((0 - x1), 2), round(y1, 2)], number="", increment=0,  x_spacing=0,  y_spacing=0, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, size=[3.43, 1.65], drill=[0, 0], layers=Pad.LAYERS_SMT))                
            footprint.append(Pad(at=[round(x1, 2), round(y1, 2)], number="", increment=0,  x_spacing=0,  y_spacing=0, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,       size=[3.43, 1.65], drill=[0, 0], layers=Pad.LAYERS_SMT))                
            
            #
            # Add pads
            #
            pinsi = int(pins / 2)
            footprint.append(PadArray(start=[round((0 - (B / 2)), 2), round(0 - (PadDist / 2), 2)], pincount=pinsi, initial=1,    increment=1,  x_spacing=pitch,  y_spacing=0, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, size=[PadSiseX, PadSiseY], drill=[0, 0], layers=Pad.LAYERS_SMT))
            footprint.append(PadArray(start=[round((0 - (B / 2)), 2), round((PadDist / 2), 2)],     pincount=pinsi, initial=pins, increment=-1, x_spacing=pitch,  y_spacing=0, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, size=[PadSiseX, PadSiseY], drill=[0, 0], layers=Pad.LAYERS_SMT))
            #
            
            #
            # Add F.Fab
            #
            tty = 0
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

                x1 = cx
                y1 = cy - (11.56 - ((PadDist / 2 ) + (PadSiseY / 2)) + 4.6 + LineDX)
                if (i == 0):
                    tty = y1
                points.append([round(x1, 2), round(y1, 2)])
                #
                x1 = (A / 2) - 1 + LineDX
                y1 = y1
                points.append([round(x1, 2), round(y1, 2)])
                #
                x1 = (A / 2) + LineDX
                y1 = y1 + 2
                points.append([round(x1, 2), round(y1, 2)])
                #
                x1 = x1
                y1 = sny - ((1.65 / 2) + LineDX + LindeDelta)
                points.append([round(x1, 2), round(y1, 2)])
                #
                if (i == 1):
                    footprint.append(PolygoneLine(polygone=points, layer=Layer, width=LineWidth))
                    #
                    # Need to do something ugly here, becosue we will do points = [] 
                    # We need to reflect these points already here
                    #
                    points2 = []
                    for pp in points:
                        points2.append([0 - pp[0], pp[1]])
                    footprint.append(PolygoneLine(polygone=points2, layer=Layer, width=LineWidth))
                    #
                    #
                    points = [] 
                    x1 = x1
                    y1 =sny + ((1.65 / 2) + LineDX + LindeDelta)
                    points.append([round(x1, 2), round(y1, 2)])
                elif (i == 2):
                    x1 = snx + (3.43 / 2) +  LineDX + LindeDelta
                    y1 = y1
                    points.append([round(x1, 2), round(y1, 2)])
                    #
                    x1 = x1
                    y1 =sny + ((1.65 / 2) + LineDX + LindeDelta)
                    points.append([round(x1, 2), round(y1, 2)])
                    #
                    x1 = (A / 2) + LineDX
                    y1 = y1
                    points.append([round(x1, 2), round(y1, 2)])
                #
                x1 = x1
                y1 = tty + 9.91 + LineDX
                points.append([round(x1, 2), round(y1, 2)])
                #
                x1 = (B / 2) + (PadSiseX / 2) + LineDX  + LindeDelta
                y1 = y1
                points.append([round(x1, 2), round(y1, 2)])
                #
                if (i == 1):
                    ttx1 = x1
                    tty1 = ((PadDist / 2) + (PadSiseY / 2) + LineDX + LindeDelta)
                    
                if (i == 0) or (i == 2):
                    x1 = x1
                    y1 = ((PadDist / 2) + (PadSiseY / 2) + LineDX + LindeDelta)
                    ttx1 = x1
                    tty1 = y1
                    points.append([round(x1, 2), round(y1, 2)])
                    #
                    #
                    x1 = 0
                    y1 = y1
                    points.append([round(x1, 2), round(y1, 2)])
                #
                # Reflect right part around the X-axis
                #
                points2 = []
                for pp in points:
                    points2.append([0 - pp[0], pp[1]])
                #
                #
                if (i == 0):
                    # Add pin 1 marker
                    tt = len(points2)
                    p0 = points2[tt - 1]
                    p1 = points2[tt - 2]
                    p2 = points2[tt - 3]
                    p2 = [p2[0] - 1, p2[1]]
                    pp2 = [p1[0], p2[1] + 1]
                    points2[tt - 3] = p2
                    points2[tt - 2] = pp2
                    points2[tt - 1] = p1
                    points2.append(p0)
                elif (i == 1):
                    points2.append([round(0 - ttx1, 2), round(tty1, 2)])
                    
                #
                #
                footprint.append(PolygoneLine(polygone=points, layer=Layer, width=LineWidth))
                #
                footprint.append(PolygoneLine(polygone=points2, layer=Layer, width=LineWidth))                
            
            #
            # Pin 1 marker
            #
#            pp = points2[8]
#            Fab1X = round(pp[0] - 0.25, 2)
#            Fab1Y = round(pp[1] + 0.25, 2)
#            Fabpoints = [[Fab1X - 2, Fab1Y], 
#                        [Fab1X,  Fab1Y], 
#                        [Fab1X,  Fab1Y + 2]]
#            footprint.append(PolygoneLine(polygone=Fabpoints, layer='F.SilkS', width=0.12))
               
            
            
            #filename
            filename = output_dir + fp_name + ".kicad_mod"
            
            file_handler = KicadFileHandler(footprint)
            file_handler.writeFile(filename)
