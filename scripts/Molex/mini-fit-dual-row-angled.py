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

Molex Mini Fit JR top-entry dual-row connectors
http://www.molex.com/pdm_docs/sd/026013127_sd.pdf

"""

pitch = 4.20

#pins per row
pincount = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

#Molex part number
#with plastic PCB retainer, 
code = "5569-{n:02}A{mount}"
#n = number of circuits per row
#mount - 1 = screw mount
#      - 2 = peg mount

part_name = "Molex_MiniFit-JR-{part}_2x{n:02}x{p:.2f}mm_Angled"

drill = 1.80
size = 3

row = 5.5

#FP description and tags

if __name__ == '__main__':

    for peg in [True, False]:
        for pins in pincount:
            
            if peg:
                mount_option = "2"
            else:
                mount_option = "1"
                
            pn = code.format(n=pins*2, mount=mount_option)
            
            #generate the name
            fp_name = part_name.format(n=pins, p=pitch, part=pn)
            footprint = Footprint(fp_name)
            
            print(fp_name)
            
            description = "Molex Mini-Fit JR, PN:" + pn + ", dual row, side entry type, through hole"
            
            if peg:
                description += ", with plastic peg mount"
            else:
                description += ", with screw mount"
            
            #set the FP description
            footprint.setDescription(description)
            
            tags = "connector molex mini-fit 5569"
            
            #set the FP tags
            footprint.setTags(tags)
            
            #calculate fp dimensions
            
            #connector length
            A = pins * pitch + 1.2
            
            #pin centers
            B = (pins - 1) * pitch
            
            #plasic pin-lock
            C = A + 4
            
            #connector width
            W = 9.6
            
            #corner positions
            x1 = -(A-B)/2
            x2 = x1 + A
            
            y1 = -7.3 - 6.6
            y2 = y1 + 12.8
            
            # set general values
            footprint.append(Text(type='reference', text='REF**', at=[B/2,8.5], layer='F.SilkS'))
            #footprint.append(Text(type='user', text='%R', at=[B/2,-4.5], layer='F.Fab'))
            footprint.append(Text(type='value', text=fp_name, at=[B/2,10], layer='F.Fab'))
                
            #generate the pads
            footprint.append(PadArray(pincount=pins, x_spacing=pitch, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE, size=size, drill=drill, layers=['*.Cu','*.Mask']))
            footprint.append(PadArray(pincount=pins, initial=pins+1, start=[0, row], x_spacing=pitch, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE, size=size, drill=drill, layers=['*.Cu','*.Mask']))
            
            #draw the 'peg' version
            #http://www.molex.com/pdm_docs/sd/026013127_sd.pdf
            if peg:
                loc = 3.00
                if pins > 2: # two mounting holes
                    footprint.append(Pad(at=[0,-7.3],type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE, size=loc,drill=loc, layers=["*.Cu"]))
                    #footprint.append(Circle(center=[0,-7.3],radius=loc/2+0.1))
                    footprint.append(Pad(at=[B,-7.3],type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE, size=loc,drill=loc, layers=["*.Cu"]))                    
                    #footprint.append(Circle(center=[B,-7.3],radius=loc/2+0.1))
                else: #single hole
                    footprint.append(Pad(at=[B/2,-7.3],type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE, size=loc,drill=loc, layers=["*.Cu"]))                    
                    #footprint.append(Circle(center=[B/2,-7.3],radius=loc/2+0.1))
                
                #draw courtyard
                footprint.append(RectLine(start=[x1,y1],end=[x2,row+size/2],layer='F.CrtYd',width=0.05,offset=0.5,grid=0.05))
                
                #draw the outline of the connector on the silkscreen
                o = 0.15
                poly = [
                {'x': -2,'y': y2+o},
                {'x': x1-o,'y': y2+o},
                {'x': x1-o,'y': y1-o},
                {'x': B/2,'y': y1-o},
                ]
                
                footprint.append(PolygoneLine(polygone=poly))
                footprint.append(PolygoneLine(polygone=poly,x_mirror=B/2))
                
                #draw the outline of the shape
                footprint.append(RectLine(start=[x1,y1],end=[x2,y2],layer='F.Fab'))
            
            #draw the 'screw' version
            #http://www.molex.com/pdm_docs/sd/039291027_sd.pdf
            else:
                loc = 3.2
                footprint.append(Pad(at=[-4.5,  -4.2],type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE, size=loc, drill=loc, layers=["*.Cu"]))
                footprint.append(Pad(at=[B+4.5, -4.2],type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE, size=loc, drill=loc, layers=["*.Cu"]))
            
                #draw the connector outline on silkscreen layer
                o = 0.15
                poly = [
                {'x': B/2,'y': y1-o},
                {'x': x1-o,'y': y1-o},
                {'x': x1-o,'y': y2-6.2-o},
                {'x': -15.4/2 - o,'y': y2-6.2-o},
                {'x': -15.4/2 - o,'y': y2+o},
                {'x': -2,'y': y2+o},
                ]
                
                footprint.append(PolygoneLine(polygone=poly))
                footprint.append(PolygoneLine(polygone=poly,x_mirror=B/2))
                
                #draw the outline of the connector
                out = [
                {'x': B/2,'y': y1},
                {'x': x1,'y': y1},
                {'x': x1,'y': y2-6.2},
                {'x': -15.4/2,'y': y2-6.2},
                {'x': -15.4/2,'y': y2},
                {'x': B/2,'y': y2},
                ]
                
                footprint.append(PolygoneLine(polygone=out,layer='F.Fab'))
                footprint.append(PolygoneLine(polygone=out,layer='F.Fab',x_mirror=B/2))
                
                #draw courtyard
                footprint.append(RectLine(
                    start=[-15.4/2,y1],
                    end=[B+15.4/2,row+size/2],
                    layer='F.CrtYd',width=0.05,offset=0.5,grid=0.05))
            
            
            
            #draw the pins on the Silkscreen layer
            o = size/2 + 0.3
            w = 0.3
            for i in range(pins):
                x = i * pitch
                ya = o
                yb = row - o
                footprint.append(Line(start=[x-w,ya],end=[x-w,yb]))
                footprint.append(Line(start=[x+w,ya],end=[x+w,yb]))
            
            #draw lines between each pin
            off = 0.1
            for i in range(pins-1):
                xa = i * pitch + size / 2 + 0.3
                xb = (i+1) * pitch - size / 2 - 0.3
            
                footprint.append(Line(start=[xa,y2+off],end=[xb,y2+off]))
                
            #pin-1 marker
            x =  -2
            m = 0.3
            
            pin = [
            {'x': x,'y': 0},
            {'x': x-2*m,'y': +m},
            {'x': x-2*m,'y': -m},
            {'x': x,'y': 0},
            ]
            
            footprint.append(PolygoneLine(polygone=pin))
            """
            #draw the courtyard
            if boss:
                W = C + 3
            else:
                W = A
                
            footprint.append(RectLine(start=[B/2-W/2,y1],end=[B/2+W/2,y2 + tab_w], width=0.05, layer='F.CrtYd', offset=0.5, grid=0.05))
            """
            #Add a model
            footprint.append(Model(filename="Connectors_Molex.3dshapes/" + fp_name + ".wrl"))
            
            #filename
            filename = output_dir + fp_name + ".kicad_mod"

            file_handler = KicadFileHandler(footprint)
            file_handler.writeFile(filename)
