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

Datasheet: http://www.jst-mfg.com/product/pdf/eng/eXH.pdf

"""
pitch = 2.50
boss = True

variants = ["A","A-1"]

#FP name strings
part_base = "S{n:02}B-XH-" #JST part number format string

prefix = "JST_XH_"
suffix = "_{n:02}x{p:.2f}mm_Angled"

#FP description and tags

if __name__ == '__main__':

    for variant in variants:
        #variant offset V
        V = 0
        if variant is "A-1":
            pincount = range(2,16)
            V = 7.6
        else:
            pincount = range(2,17)
            V = 9.2
        for pins in pincount:
            
            
            #calculate fp dimensions
            A = (pins - 1) * pitch
            B = A + 4.9
            
            #Thickness of connector
            T = 11.5
            
            #corners
            x1 = -2.45
            x2 = x1 + B
            
            x_mid = (x1 + x2) / 2
            
            y1 = -V
            y2 = y1 + T
            
            #y at which the plastic tabs end
            y3 = y1 + 7
        
            #generate the name
            part = part_base + variant
            fp_name = prefix + part.format(n=pins) + suffix.format(n=pins, p=pitch)

            footprint = Footprint(fp_name)
            
            description = "JST XH series connector, " + part.format(n=pins) + ", side entry type, through hole"
            
            #set the FP description
            footprint.setDescription(description)
            
            tags = "connector jst xh tht side horizontal angled 2.50mm"
            
            #set the FP tags
            footprint.setTags(tags)

            # set general values
            footprint.append(Text(type='reference', text='REF**', at=[x_mid,y2 + 2], layer='F.SilkS'))
            footprint.append(Text(type='value', text=fp_name, at=[x_mid,y1 - 1], layer='F.Fab'))

            drill = 0.9
                
            #generate the pads
            pa = PadArray(pincount=pins, x_spacing=pitch, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE, size=1.5, drill=drill, layers=['*.Cu','*.Mask'])
            
            footprint.append(pa)

            
            #draw the courtyard
            cy = RectLine(start=[x1,y1],end=[x2,y2],layer='F.CrtYd',width=0.05,offset = 0.5)
            footprint.append(cy)
            
            #offset the outline around the connector
            off = 0.15
            
            xo1 = x1 - off
            yo1 = y1 - off
            
            xo2 = x2 + off
            yo2 = y2 + off
            
            #thickness of the notches
            notch = 1.5
            
            #wall thickness of the outline
            wall = 1
            
            #draw the outline of the connector
            outline = [
            {'x': x_mid,'y': yo1},
            {'x': xo1,'y': yo1},
            {'x': xo1,'y': yo2},
            {'x': xo1+wall,'y': yo2},
            {'x': xo1+wall,'y': y3 + off},
            #{'x': -1.1,'y': y3 + off}
            ]
            
            footprint.append(PolygoneLine(polygone = outline))
            footprint.append(PolygoneLine(polygone = outline,x_mirror=x_mid))
            
            #add lines between pads!
            #pad offset
            po = 1
            #line height
            h = 1
            for i in range(pins-1):
                xpa = pitch * i
                xp1 = pitch * i + po
                xp2 = pitch * (1 + i) - po
                xpb = pitch * (i + 1)
                yp2 = y3 + off
                yp1 = y3 - h
                
                line = [
                {'x': xpa, 'y': yp1},
                {'x': xp1, 'y': yp1},
                {'x': xp1, 'y': yp2},
                {'x': xp2, 'y': yp2},
                {'x': xp2, 'y': yp1},
                {'x': xpb, 'y': yp1},
                ]
                
                footprint.append(PolygoneLine(polygone=line))
            
            #add pin-1 designator
            px = 0
            py = yo2 + 0.5
            m = 0.3
            
            pin1 = [
            {'x': px,'y': py},
            {'x': px-m,'y': py+2*m},
            {'x': px+m,'y': py+2*m},
            {'x': px,'y': py},
            ]
            
            footprint.append(PolygoneLine(polygone=pin1))
            
            #add the end bits
            end = [
            {'x': xo1 + wall,'y': y3 + off},
            {'x': xo1 + wall,'y': y3 - h},
            {'x': 0,'y': y3-h},
            ]
            
            footprint.append(PolygoneLine(polygone=end))
            footprint.append(PolygoneLine(polygone=end,x_mirror=x_mid))
            
            
            """
            outline = [
            {'x': xo1,'y': yo2-wall - 1},
            {'x': xo1 + wall,'y': yo2-wall - 1},
            {'x': xo1 + wall,'y': yo1+wall},
            {'x': x_mid,'y': yo1+wall},
            ]
                
            footprint.append(PolygoneLine(polygone=outline))
            
            footprint.append(PolygoneLine(polygone=outline,x_mirror=x_mid))
          
            
            footprint.append(RectLine(start=[xo1,yo2-wall],end=[xo1+notch,yo2]))
            footprint.append(RectLine(start=[xo2,yo2-wall],end=[xo2-notch,yo2]))
            
            #draw the middle tab
            nx1 = -0.5 + notch
            nx2 = A + 0.5 - notch
            footprint.append(RectLine(start=[nx1, yo2 - wall],end=[nx2,yo2]))
            """ 
            #Add a model
            footprint.append(Model(filename="Connectors_JST.3dshapes/" + fp_name + ".wrl"))
            
            #filename
            filename = output_dir + fp_name + ".kicad_mod"
            

            file_handler = KicadFileHandler(footprint)
            file_handler.writeFile(filename)
