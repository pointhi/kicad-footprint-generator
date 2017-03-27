#!/usr/bin/env python

import sys
import os
#sys.path.append(os.path.join(sys.path[0],"..","..","kicad_mod")) # load kicad_mod path


# export PYTHONPATH="${PYTHONPATH}<path to kicad-footprint-generator directory>"
from KicadModTree import *

LAYERS_SMT = ['F.Cu','F.Mask','F.Paste']
LAYERS_THT = ['*.Cu','*.Mask']
LAYERS_NPTH = ['*.Cu', '*.Mask']

output_dir = os.getcwd()
_3dshapes = "${KISYS3DMOD}/Connectors_JST.3dshapes"+os.sep
ref_on_ffab = False
main_ref_on_silk = True
fab_line_width = 0.1
silk_line_width = 0.15
value_fontsize = [1,1]
value_fontwidth=0.15
silk_reference_fontsize=[1,1]
silk_reference_fontwidth=0.15
fab_reference_fontsize=[0.6,0.6]
fab_reference_fontwidth=0.1

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
    drill_size = 0.8
elif config_to_use == "KLCv1.1":
    _3dshapes = "${KISYS3DMOD}/Connectors_JST.3dshapes"+os.sep
    ref_on_ffab = False
    main_ref_on_silk = True
    fab_line_width = 0.1
    silk_line_width = 0.15
    value_fontsize = [1,1]
    value_fontwidth=0.15
    value_inside = False
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

# http://www.jst-mfg.com/product/pdf/eng/ePH.pdf
#JST_PH_B10B-PH-K_10x2.00mm_Straight
part = "B{n}B-PH-K" #JST part number format string

prefix = "JST_PH_"
suffix = "_{n:02}x{p:.2f}mm_Straight"

pitch = 2.00

# Connector Parameters
silk_to_part_offset = 0.1
x_min = -1.95
y_min = -1.7
y_max = y_min + 4.5

silk_x_min = x_min - silk_to_part_offset
silk_y_min = y_min - silk_to_part_offset
silk_y_max = y_max + silk_to_part_offset

for pincount in range (2,17):
    x_mid = (pincount-1)*pitch/2.0
    x_max = (pincount-1)*pitch + 1.95
    silk_x_max = x_max + silk_to_part_offset

    # Through-hole type shrouded header, Top entry type
    footprint_name = prefix + part.format(n=pincount) + suffix.format(n=pincount, p=pitch)

    kicad_mod = Footprint(footprint_name)
    description = "JST PH series connector, " + part.format(n=pincount) + ", top entry type, through hole, Datasheet: http://www.jst-mfg.com/product/pdf/eng/ePH.pdf"
    kicad_mod.setDescription(description)
    kicad_mod.setTags('connector jst ph')



    # set general values
    ref_pos_1=[1.5, silk_y_min-0.5-silk_reference_fontsize[0]/2.0]
    ref_pos_2=[x_mid, 1.5]
    if ref_on_ffab and not main_ref_on_silk:
        kicad_mod.append(Text(type='user', text='%R', at=ref_pos_1, layer='F.SilkS',
            size=silk_reference_fontsize, thickness=silk_reference_fontwidth))
        kicad_mod.append(Text(type='reference', text='REF**', layer='F.Fab',
            at=ref_pos_2, size=fab_reference_fontsize, thickness=fab_reference_fontwidth))
    elif ref_on_ffab and main_ref_on_silk:
        kicad_mod.append(Text(type='user', text='%R', at=ref_pos_2, layer='F.Fab',
            size=silk_reference_fontsize, thickness=silk_reference_fontwidth))
        kicad_mod.append(Text(type='reference', text='REF**', layer='F.SilkS',
            at=ref_pos_1, size=fab_reference_fontsize, thickness=fab_reference_fontwidth))
    else:
        kicad_mod.append(Text(type='reference', text='REF**', layer='F.SilkS',
            at=ref_pos_1, size=silk_reference_fontsize, thickness=silk_reference_fontwidth))

    kicad_mod.append(Text(type='value', text=footprint_name, at=[x_mid,y_max+0.5+value_fontsize[0]/2.0], layer='F.Fab',
        size=value_fontsize, thickness=value_fontwidth))

    # create Silkscreen
    kicad_mod.append(RectLine(start=[silk_x_min,silk_y_min], end=[silk_x_max,silk_y_max],
        layer='F.SilkS', width=silk_line_width))

    silk_inner_left=-1.45
    silk_inner_right=x_max-0.5

    poly_silk_inner_outline = [
        {'x':0.5, 'y':silk_y_min},
        {'x':0.5, 'y':-1.2},
        {'x':silk_inner_left, 'y':-1.2},
        {'x':silk_inner_left, 'y':2.3},
        {'x':silk_inner_right, 'y':2.3},
        {'x':silk_inner_right, 'y':-1.2},
        {'x':x_max-2.45, 'y':-1.2},
        {'x':x_max-2.45, 'y':silk_y_min}
    ]
    kicad_mod.append(PolygoneLine(polygone=poly_silk_inner_outline, layer='F.SilkS', width=silk_line_width))


    kicad_mod.append(Line(start=[silk_x_min, -0.5], end=[silk_inner_left, -0.5], layer='F.SilkS', width=silk_line_width))
    kicad_mod.append(Line(start=[silk_x_min, 0.8], end=[silk_inner_left, 0.8], layer='F.SilkS', width=silk_line_width))

    kicad_mod.append(Line(start=[silk_x_max, -0.5], end=[silk_inner_right, -0.5], layer='F.SilkS', width=silk_line_width))
    kicad_mod.append(Line(start=[silk_x_max, 0.8], end=[silk_inner_right, 0.8], layer='F.SilkS', width=silk_line_width))

    poly_silk_p1_protrusion=[
        {'x':-0.3, 'y':silk_y_min},
        {'x':-0.3, 'y':silk_y_min-0.2},
        {'x':-0.6, 'y':silk_y_min-0.2},
        {'x':-0.6, 'y':silk_y_min}
    ]
    kicad_mod.append(PolygoneLine(polygone=poly_silk_p1_protrusion, layer='F.SilkS', width=silk_line_width))

    kicad_mod.append(Line(start=[-0.3, silk_y_min-0.1], end=[-0.6, silk_y_min-0.1], layer='F.SilkS', width=silk_line_width))

    for i in range(0, pincount-1):
        middle_x = 1+i*2
        start_x = middle_x-0.1
        end_x = middle_x+0.1
        poly_silk_inner_protrusion=[
            {'x':start_x, 'y':2.3},
            {'x':start_x, 'y':1.8},
            {'x':end_x, 'y':1.8},
            {'x':end_x, 'y':2.3}
        ]
        kicad_mod.append(PolygoneLine(polygone=poly_silk_inner_protrusion, layer='F.SilkS', width=silk_line_width))
        kicad_mod.append(Line(start=[middle_x, 2.3], end=[middle_x, 1.8], layer='F.SilkS', width=silk_line_width))

    # Pin 1 Marker
    poly_pin1_marker = [
        {'x':silk_x_min-pin1_marker_offset+pin1_marker_linelen, 'y':silk_y_min-pin1_marker_offset},
        {'x':silk_x_min-pin1_marker_offset, 'y':silk_y_min-pin1_marker_offset},
        {'x':silk_x_min-pin1_marker_offset, 'y':silk_y_min-pin1_marker_offset+pin1_marker_linelen}
    ]
    kicad_mod.append(PolygoneLine(polygone=poly_pin1_marker, layer='F.SilkS', width=silk_line_width))
    if fab_pin1_marker_type == 1:
        kicad_mod.append(PolygoneLine(polygone=poly_pin1_marker, layer='F.Fab', width=fab_line_width))

    if fab_pin1_marker_type == 2:
        poly_pin1_marker_type2 = [
            {'x':-1, 'y':y_min},
            {'x':0, 'y':y_min+1},
            {'x':1, 'y':y_min}
        ]
        kicad_mod.append(PolygoneLine(polygone=poly_pin1_marker_type2, layer='F.Fab', width=fab_line_width))

    # create Fab outline
    kicad_mod.append(RectLine(start=[x_min,y_min], end=[x_max,y_max],
        layer='F.Fab', width=fab_line_width))
    # create Courtyard
    part_x_min = x_min
    part_x_max = x_max
    part_y_min = y_min
    part_y_max = y_max

    kicad_mod.append(RectLine(start=round_crty_point([part_x_min-CrtYd_offset, part_y_min-CrtYd_offset]),
        end=round_crty_point([part_x_max+CrtYd_offset, part_y_max+CrtYd_offset]),
        layer='F.CrtYd', width=CrtYd_linewidth))

    # create pads
    #createNumberedPadsTHT(kicad_mod, pincount, 2, 0.7, {'x':1.2, 'y':1.7})
    #add the pads
    kicad_mod.append(Pad(number=1, type=Pad.TYPE_THT, shape=Pad.SHAPE_RECT,
                        at=[0, 0], size=pad_size,
                        drill=drill_size, layers=LAYERS_THT))
    for p in range(1, pincount):
        Y = 0
        X = p * pitch

        num = p+1
        kicad_mod.append(Pad(number=num, type=Pad.TYPE_THT, shape=Pad.SHAPE_OVAL,
                            at=[X, Y], size=pad_size,
                            drill=drill_size, layers=LAYERS_THT))
    #Add a model
    kicad_mod.append(Model(filename=_3dshapes + footprint_name + ".wrl", at=[0,0,0], scale=[1,1,1], rotate=[0,0,0]))


    #filename
    filename = output_dir + footprint_name + ".kicad_mod"


    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile(filename)
