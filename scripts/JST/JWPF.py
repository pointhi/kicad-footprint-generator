#!/usr/bin/env python

import sys
import os

sys.path.append(os.path.join(sys.path[0],"..",".." )) #"kicad_mod")) # load kicad_mod path

# export PYTHONPATH="${PYTHONPATH}<path to kicad-footprint-generator directory>"
from KicadModTree import *

LAYERS_SMT = ['F.Cu','F.Mask','F.Paste']
LAYERS_THT = ['*.Cu','*.Mask']
LAYERS_NPTH = ['*.Cu', '*.Mask']

output_dir = os.getcwd()

_3dshapes = "${KISYS3DMOD}/Connectors_JST.3dshapes/"
ref_on_ffab = False
main_ref_on_silk = True
fab_line_width = 0.1
silk_line_width = 0.15
value_fontsize = [1,1]
value_fontwidth=0.15
silk_reference_fontsize=[1,1]
silk_reference_fontwidth=0.15
fab_reference_fontsize=[1, 1]
fab_reference_fontwidth=0.15

CrtYd_offset = 0.5
CrtYd_linewidth = 0.05
CrtYd_grid = 0.01

pin1_marker_offset = 0.3
pin1_marker_linelen = 1.25
fab_pin1_marker_type = 1

pad_size=[1.2, 1.7]
drill_size = 0.75 #Datasheet: 0.7 +0.1/-0.0 => It might be better to assume 0.75 +/-0.05mm

def round_to(n, precision):
    correction = 0.5 if n >= 0 else -0.5
    return int( n/precision+correction ) * precision

def round_crty_point(point):
    return [round_to(point[0],CrtYd_grid),round_to(point[1],CrtYd_grid)]

if len(sys.argv) > 3:
    _3dshapes = sys.argv[2]
    if _3dshapes.endswith(".3dshapes"):
        _3dshapes += os.sep
    if not _3dshapes.endswith(".3dshapes"+os.sep):
        _3dshapes += ".3dshapes"+os.sep

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

if not os.path.isdir(output_dir): #returns false if path does not yet exist!! (Does not check path validity)
    os.makedirs(output_dir)

"""
Datasheet: http://www.jst-mfg.com/product/pdf/eng/eJWPF1.pdf
Naming: JST_JWPF_BXXB-JWPF-SK-R_XxXX_Pitch2.00mm
"""
part = "B{n:02}B-JWPF-SK-R" #JST part number format string

prefix = "JST_JWPF_"

pitch = 2.00

# Connector Dimensions
tab_width = 7.0
row_spacing = 4.0
pad_drill = 1.0
mount_hole_size = 1.1
mount_hole_offset_x = 1.5
pad_y = 1.5
pad_x = 2.5

# Width of connector
jwpf_widths = {
    2 : 8.1,
    3 : 8.4,
    4 : 8.4,
    6 : 12.8,
    8 : 12.5
}

jwpf_lengths = {
    2 : 7,
    3 : 9,
    4 : 11,
    6 : 9.8,
    8 : 11.8
}

for pincount in [2, 3, 4, 6, 8]:

    if pincount in [6, 8]:
        rows = 2
        pin_per_row = int(pincount / 2)
        pn = "2x{n:02}".format(n=pin_per_row)
    else:
        rows = 1
        pin_per_row = pincount
        pn = "1x{n:02}".format(n=pincount)

    pin_info = "_{x}_P{p:.2f}mm_Vertical".format(x=pn, p=pitch)

    footprint_name = prefix + part.format(n=pincount) + pin_info

    print(footprint_name)

    conn_width = jwpf_widths[pincount]
    conn_length = jwpf_lengths[pincount]

    mount_hole_offset_y = 2.05 if rows == 1 else 2.45

    kicad_mod = Footprint(footprint_name)
    description = "JST JWPF series connector, " + part.format(n=pincount) + ", top entry type, through hole, Datasheet: http://www.jst-mfg.com/product/pdf/eng/eJWPF1.pdf"
    kicad_mod.setDescription(description)
    kicad_mod.setTags('connector JST JWPF')

    # Add texts
    x_mid = (rows-1) * row_spacing / 2
    y_mid = (pin_per_row - 1) * pitch / 2.0

    # Connector outline
    y1 = y_mid - conn_length / 2
    y2 = y_mid + conn_length / 2

    x1 = -5.4 # measured from 3D model alignment
    x2 = x1 + conn_width

    y_ref = -3 if rows == 1 else -4

    kicad_mod.append(Text(type='reference', text='REF**', layer='F.SilkS', at=[x_mid, y_ref ], thickness=silk_reference_fontwidth, size=silk_reference_fontsize))
    kicad_mod.append(Text(type='user', text='%R', at=[-2.5, y_mid], layer='F.Fab', thickness=fab_reference_fontwidth, size=fab_reference_fontsize, rotation='90'))
    kicad_mod.append(Text(type='value', text=footprint_name, at=[x_mid, y2 + 1.5], layer='F.Fab', size=value_fontsize, thickness=value_fontwidth))

    # Create pins
    for i in range(rows):
        kicad_mod.append(PadArray(initial=1+i*pin_per_row, start=[i*row_spacing, 0], pincount=pin_per_row, y_spacing=pitch, type=Pad.TYPE_THT, shape=Pad.SHAPE_OVAL, size=[pad_x, pad_y], drill=pad_drill, layers=Pad.LAYERS_THT))

    # Add mounting hole
    mx = -mount_hole_offset_x
    my = (pin_per_row - 1) * pitch + mount_hole_offset_y
    kicad_mod.append(Pad(at=[mx, my], size=mount_hole_size, drill=mount_hole_size, shape=Pad.SHAPE_CIRCLE, type=Pad.TYPE_NPTH, layers=Pad.LAYERS_NPTH))

    # Tab dimensions
    tw = 7
    tt = 0.5

    # Couryard
    kicad_mod.append(RectLine(start=[x1,y1], end=[x2,y2], layer='F.CrtYd', width='0.05', offset=0.5))

    def draw_outline(offset=0, layer='F.Fab', width=0.1):
        O = offset
        R = 1.0

        if pincount == 2:
            poly = [
                {'x': x2 + O - R, 'y': y1 - O},
                {'x': x1 - O, 'y': y1 - O},
                {'x': x1 - O, 'y': y2 + O},
                {'x': x2 + O - R, 'y': y2 + O},
            ]

            kicad_mod.append(PolygoneLine(polygone=poly, layer=layer, width=width))
        else:
            # top line
            kicad_mod.append(Line(start=[tt+x1-O+R, y1-O], end=[x2+O-R, y1-O], layer=layer, width=width))
            # bottom line
            kicad_mod.append(Line(start=[tt+x1-O+R, y2+O], end=[x2+O-R, y2+O], layer=layer, width=width))

            # left line (including tab)
            poly = [
                {'x': tt+x1-O, 'y': y1-O+R},
                {'x': tt+x1-O, 'y': y_mid - tw/2.0 - O},
                {'x': x1-O, 'y': y_mid - tw/2.0 - O},
                {'x': x1-O, 'y': y_mid + tw/2.0 + O},
                {'x': tt+x1-O, 'y': y_mid + tw/2.0 + O},
                {'x': tt+x1-O, 'y': y2+O-R}
            ]

            kicad_mod.append(PolygoneLine(polygone=poly, width=width, layer=layer))

            # top left
            kicad_mod.append(Arc(center=[tt+x1-O+R, y1-O+R], start=[tt+x1-O, y1-O+R], angle=90.0, layer=layer, width=width))
            # bottom left
            kicad_mod.append(Arc(center=[tt+x1-O+R, y2+O-R], start=[tt+x1-O+R, y2+O], angle=90.0, layer=layer, width=width))


        # right line
        kicad_mod.append(Line(start=[x2+O, y1-O+R], end=[x2+O, y2+O-R], layer=layer, width=width))

        # top right
        kicad_mod.append(Arc(center=[x2+O-R, y1-O+R], start=[x2+O-R, y1-O], angle=90.0, layer=layer, width=width))

        # bottom right
        kicad_mod.append(Arc(center=[x2+O-R, y2+O-R], start=[x2+O, y2+O-R], angle=90.0, layer=layer, width=width))


    draw_outline()
    draw_outline(offset=0.1, layer='F.SilkS', width=0.12)

    # Add pin-1 marker on F.SilkS
    Q = 0.35 # offset
    L = 1.5
    p1 = [
        {'x': x1 - Q, 'y': y1 - Q + L},
        {'x': x1 - Q, 'y': y1 - Q},
        {'x': x1 - Q + L, 'y': y1 - Q},
    ]

    kicad_mod.append(PolygoneLine(polygone=p1, layer='F.SilkS', width=0.12))

    # Add pin-1 marker on F.Fab
    D = -0.5 - pad_y / 2
    M = 0.75
    p1 = [
        {'x': -M/2, 'y': D - M},
        {'x': M/2, 'y': D - M},
        {'x': 0, 'y': D},
        {'x': -M/2, 'y': D - M},
    ]

    kicad_mod.append(PolygoneLine(polygone=p1, layer='F.Fab', width=0.10))

    #Add a model
    kicad_mod.append(Model(filename=_3dshapes + footprint_name + ".wrl", at=[0,0,0], scale=[1,1,1], rotate=[0,0,0]))


    #filename
    filename = output_dir + footprint_name + ".kicad_mod"
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile(filename)
