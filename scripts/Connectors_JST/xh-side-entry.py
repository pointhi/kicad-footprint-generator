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
_3dshapes = "${KISYS3DMOD}/Connectors_JST.3dshapes"+os.sep
ref_on_ffab = False
main_ref_on_silk = True

allow_silk_below_part = True

fab_line_width = 0.1
silk_line_width = 0.12
value_fontsize = [1,1]
value_fontwidth=0.15
value_inside = False
silk_reference_fontsize=[1,1]
silk_reference_fontwidth=0.15
fab_reference_fontsize=[1,1]
fab_reference_fontwidth=0.15

CrtYd_offset = 0.5
CrtYd_linewidth = 0.05
CrtYd_grid = 0.01

pin1_marker_offset = 0.3
pin1_marker_linelen = 1.25
fab_pin1_marker_type = 1

pad_to_silk = 0.275

def round_to(n, precision):
    correction = 0.5 if n >= 0 else -0.5
    return int( n/precision+correction ) * precision

def round_crty_point(point):
    return [round_to(point[0],CrtYd_grid),round_to(point[1],CrtYd_grid)]

config_to_use = "KLCv2.0"

if len(sys.argv) > 1:
    if sys.argv[1].lower() == "tera":
        config_to_use = "TERA"
    elif sys.argv[1].lower() == "klcv1.1":
        config_to_use = "KLCv1.1"
    elif sys.argv[1].lower() == "klcv2.0":
        config_to_use = "KLCv2.0"

print("Used configuration: " + config_to_use)


if config_to_use == "TERA":
    ref_on_ffab = True
    main_ref_on_silk = False
    fab_line_width = 0.05
    silk_line_width = 0.15
    _3dshapes = "${KISYS3DMOD}/tera_Connectors_JST.3dshapes"+os.sep
    value_fontsize = [0.6,0.6]
    value_fontwidth = 0.1
    fab_pin1_marker_type = 2
    value_inside = True
    allow_silk_below_part = True
elif config_to_use == "KLCv1.1":
    _3dshapes = "${KISYS3DMOD}/Connectors_JST.3dshapes"+os.sep
    ref_on_ffab = False
    main_ref_on_silk = True
    fab_line_width = 0.1
    silk_line_width = 0.15
    value_fontsize = [1,1]
    value_fontwidth=0.15
    value_inside = False
    allow_silk_below_part = True
elif config_to_use == "KLCv2.0":
    _3dshapes = "${KISYS3DMOD}/Connectors_JST.3dshapes"+os.sep
    ref_on_ffab = True
    main_ref_on_silk = True
    fab_line_width = 0.1
    silk_line_width = 0.12
    value_fontsize = [1,1]
    value_fontwidth = 0.15
    value_inside = False
    silk_reference_fontsize=[1,1]
    silk_reference_fontwidth=0.15
    fab_reference_fontsize=[1,1]
    fab_reference_fontwidth=0.15
    allow_silk_below_part = False
else:
    print("Programming error: Unknown config!")
    exit(-1)

out_dir="Connectors_JST.pretty"+os.sep
if len(sys.argv) > 2:
    out_dir = sys.argv[1]
    if out_dir.endswith(".pretty"):
        out_dir += os.sep
    if not out_dir.endswith(".pretty"+os.sep):
        out_dir += ".pretty"+os.sep

if os.path.isabs(out_dir) and os.path.isdir(out_dir):
    output_dir = out_dir
else:
    output_dir = os.path.join(os.getcwd(),out_dir)

if len(sys.argv) > 3:
    _3dshapes = sys.argv[2]
    if _3dshapes.endswith(".3dshapes"):
        _3dshapes += os.sep
    if not _3dshapes.endswith(".3dshapes"+os.sep):
        _3dshapes += ".3dshapes"+os.sep


if output_dir and not output_dir.endswith(os.sep):
    output_dir += os.sep

if not os.path.isdir(output_dir): #returns false if path does not yet exist!! (Does not check path validity)
    os.makedirs(output_dir)

#import KicadModTree files
# export PYTHONPATH="${PYTHONPATH}<path to kicad-footprint-generator directory>"
sys.path.append("..\\..")
from KicadModTree import *
from KicadModTree.nodes.specialized.PadArray import PadArray

"""
footprint specific details to go here

Datasheet: http://www.jst-mfg.com/product/pdf/eng/eXH.pdf

"""
pitch = 2.50
boss = True

variants = ["A"]#,"A-1"]

#FP name strings
part_base = "S{n:02}B-XH-" #JST part number format string

prefix = "JST_XH_"
suffix = "_{n:02}x{p:.2f}mm_Angled"

fab_first_marker_w = 1.25
fab_first_marker_h = 1

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

            y2 = V
            y1= y2 - T


            #y at which the plastic tabs end
            y3 = y2 - 7

            #generate the name
            part = part_base + variant
            fp_name = prefix + part.format(n=pins) + suffix.format(n=pins, p=pitch)

            print(fp_name)
            footprint = Footprint(fp_name)

            description = "JST XH series connector, " + part.format(n=pins) + ", side entry type, through hole"

            #set the FP description
            footprint.setDescription(description)

            tags = "connector jst xh tht side horizontal angled 2.50mm"

            #set the FP tags
            footprint.setTags(tags)

            # set general values
            #footprint.append(Text(type='reference', text='REF**', at=[x_mid,-3.5], layer='F.SilkS'))

            ref_pos_1=[x_mid,-3.5]
            ref_pos_2=[x_mid, 3.5]
            if ref_on_ffab and not main_ref_on_silk:
                footprint.append(Text(type='user', text='%R', at=ref_pos_1, layer='F.SilkS',
                    size=silk_reference_fontsize, thickness=silk_reference_fontwidth))
                footprint.append(Text(type='reference', text='REF**', layer='F.Fab',
                    at=ref_pos_2, size=fab_reference_fontsize, thickness=fab_reference_fontwidth))
            elif ref_on_ffab and main_ref_on_silk:
                footprint.append(Text(type='user', text='%R', at=ref_pos_2, layer='F.Fab',
                    size=silk_reference_fontsize, thickness=silk_reference_fontwidth))
                footprint.append(Text(type='reference', text='REF**', layer='F.SilkS',
                    at=ref_pos_1, size=fab_reference_fontsize, thickness=fab_reference_fontwidth))
            else:
                footprint.append(Text(type='reference', text='REF**', layer='F.SilkS',
                    at=ref_pos_1, size=silk_reference_fontsize, thickness=silk_reference_fontwidth))

            if value_inside:
                value_pos_y = y2-0.5-value_fontsize[0]/2.0
            else:
                value_pos_y = y2+0.5+value_fontsize[0]/2.0

            footprint.append(Text(type='value', text=fp_name, at=[x_mid,value_pos_y], layer='F.Fab',
                size=value_fontsize, thickness=value_fontwidth))

            #draw simple outline on F.Fab layer
            #footprint.append(RectLine(start=[x1,y1],end=[x2,y2],layer='F.Fab', width=fab_line_width))

            if pins == 2:
                drill = 1.0
            else:
                drill = 0.95

            dia = 1.85 #maximum size to get a trace between tracs for 0.2mm clearance and 0.25 min width

            #generate the pads
            pa = PadArray(pincount=pins, x_spacing=pitch, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE, size=dia, drill=drill, layers=['*.Cu','*.Mask','F.SilkS'])

            footprint.append(pa)

            #draw the courtyard
            cy = RectLine(start=[x1,y1],end=[x2,y2],layer='F.CrtYd',width=0.05,offset = 0.5)
            footprint.append(cy)

            #offset the outline around the connector
            off = 0.1

            xo1 = x1 - off
            yo1 = y1 - off

            xo2 = x2 + off
            yo2 = y2 + off

            #thickness of the notches
            notch = 1.5

            #wall thickness of the outline
            wall = 1.2

            #draw the outline of the connector
            outline = [
            {'x': x_mid,'y': yo2},
            {'x': xo1,'y': yo2},
            {'x': xo1,'y': yo1},
            {'x': xo1+wall+2*off,'y': yo1},
            {'x': xo1+wall+2*off,'y': y3 - off},
            {'x': A/2,'y': y3 - off},
            #{'x': -1.1,'y': y3 + off}
            ]

            footprint.append(PolygoneLine(polygone = outline))
            footprint.append(PolygoneLine(polygone = outline,x_mirror=x_mid))

            outline = [
            {'x': x_mid,'y': y2},
            {'x': x1,'y': y2},
            {'x': x1,'y': y1},
            {'x': x1+wall,'y': y1},
            {'x': x1+wall,'y': y3},
            {'x': A/2,'y': y3},
            #{'x': -1.1,'y': y3 + off}
            ]
            footprint.append(PolygoneLine(polygone = outline,layer='F.Fab', width=fab_line_width))
            footprint.append(PolygoneLine(polygone = outline,x_mirror=x_mid,layer='F.Fab', width=fab_line_width))


            #draw the pinsss
            for i in range(pins):

                x = i * pitch
                w = 0.25
                footprint.append(RectLine(start=[x-w,y3+0.5],end=[x+w,y2-0.5]))

            #add pin-1 designator
            px = 0
            py = -1.5
            m = 0.3

            pin1 = [
            {'x': px,'y': py},
            {'x': px-m,'y': py-2*m},
            {'x': px+m,'y': py-2*m},
            {'x': px,'y': py},
            ]

            footprint.append(PolygoneLine(polygone=pin1))
            if fab_pin1_marker_type == 1:
                footprint.append(PolygoneLine(polygone=pin1,layer='F.Fab'))

            if fab_pin1_marker_type == 2:
                fab_marker_left = -fab_first_marker_w/2.0
                fab_marker_bottom = y3 - fab_first_marker_h
                poly_fab_marker = [
                    {'x':fab_marker_left, 'y':y3},
                    {'x':0, 'y':fab_marker_bottom},
                    {'x':fab_marker_left + fab_first_marker_w, 'y':y3}
                ]
                footprint.append(PolygoneLine(polygone=poly_fab_marker, layer='F.Fab', width=fab_line_width))

            #Add a model
            footprint.append(Model(filename=_3dshapes + fp_name + ".wrl"))

            #filename
            filename = output_dir + fp_name + ".kicad_mod"


            file_handler = KicadFileHandler(footprint)
            file_handler.writeFile(filename)
