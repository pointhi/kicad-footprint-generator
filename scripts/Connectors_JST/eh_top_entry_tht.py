#!/usr/bin/env python

import sys
import os

from kicad_mod.kicad_mod import KicadMod, createNumberedPadsTHT

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

# http://www.jst-mfg.com/product/pdf/eng/ePH.pdf

pitch = 2.50

for pincount in range(2,16):

    jst = "B{pincount:02}B-EH-A".format(pincount=pincount)

    # Through-hole type shrouded header, Top entry type
    footprint_name = "JST_EH_" + jst + "_{pincount:02}x2.50mm_Straight".format(pincount=pincount)

    print(footprint_name)

    A = (pincount - 1) * pitch
    B = A + 5.0

    kicad_mod = KicadMod(footprint_name)
    kicad_mod.setDescription("JST EH series connector, " + jst + ", 2.50mm pitch, top entry")
    kicad_mod.setTags('connector jst eh top vertical straight')

    # set general values
    ref_1_y=-3
    ref_2_y=-0.5
    if ref_on_ffab and not main_ref_on_silk:
        kicad_mod.addText('user', '%R', {'x':A/2, 'y':ref_1_y}, layer='F.SilkS', fontsize=silk_reference_fontsize, fontwidth=silk_reference_fontwidth)
        kicad_mod.addText('reference', 'REF**', {'x':A/2, 'y':ref_2_y}, layer='F.Fab', fontsize=fab_reference_fontsize, fontwidth=fab_reference_fontwidth)
    elif ref_on_ffab and main_ref_on_silk:
        kicad_mod.addText('user', '%R', {'x':A/2, 'y':ref_2_y}, layer='F.Fab', fontsize=fab_reference_fontsize, fontwidth=fab_reference_fontwidth)
        kicad_mod.addText('reference', 'REF**', {'x':A/2, 'y':ref_1_y}, layer='F.SilkS', fontsize=silk_reference_fontsize, fontwidth=silk_reference_fontwidth)
    else:
        kicad_mod.addText('reference', 'REF**', {'x':A/2, 'y':ref_1_y}, layer='F.SilkS', fontsize=silk_reference_fontsize, fontwidth=silk_reference_fontwidth)

    if value_inside:
        value_pos_y=1.5
    else:
        value_pos_y=3.5

    kicad_mod.addText('value', footprint_name, {'x':A/2, 'y':value_pos_y}, layer='F.Fab', fontsize=value_fontsize, fontwidth=value_fontwidth)

    if pincount == 2:
        drill = 1.0
    else:
        drill = 0.95

    dia = 1.85 #maximum size to get a trace between tracs for 0.2mm clearance and 0.25 min width

    # create pads
    createNumberedPadsTHT(kicad_mod, pincount, pitch, drill, {'x':dia, 'y':dia})



    x1 = -2.5
    y1 = -1.6
    x2 = x1 + B
    y2 = y1 + 3.8

    #draw the main outline on F.Fab layer
    kicad_mod.addRectLine({'x':x1,'y':y1},{'x':x2,'y':y2}, layer='F.Fab', width=fab_line_width)

    #line offset
    off = 0.15

    x1 -= off
    y1 -= off

    x2 += off
    y2 += off

    #draw the main outline around the footprint
    kicad_mod.addRectLine({'x':x1,'y':y1},{'x':x2,'y':y2}, width=silk_line_width)

    T = 0.5

    #add top line
    kicad_mod.addPolygoneLine([{'x': x1,'y': 0},
                               {'x': x1 + T,'y': 0},
                               {'x': x1 + T,'y': y1 + T},
                               {'x': x2 - T,'y': y1 + T},
                               {'x': x2 - T,'y': 0},
                               {'x': x2,'y':0}], width=silk_line_width)

    #add bottom line (left)
    kicad_mod.addPolygoneLine([{'x':x1,'y':y2-3*T},
                               {'x':x1+2*T,'y':y2-3*T},
                               {'x':x1+2*T,'y':y2}], width=silk_line_width)

    #add bottom line (right)
    kicad_mod.addPolygoneLine([{'x':x2,'y':y2-3*T},
                               {'x':x2-2*T,'y':y2-3*T},
                               {'x':x2-2*T,'y':y2}], width=silk_line_width)

    #add pin-1 marker
    D = 0.3
    L = 2.5
    pin = [
        {'x': x1-D,'y': y2+D-L},
        {'x': x1-D,'y': y2+D},
        {'x': x1-D+L,'y': y2+D},
    ]

    kicad_mod.addPolygoneLine(pin)
    kicad_mod.addPolygoneLine(pin, layer='F.Fab', width=fab_line_width)

    #add a courtyard
    cy = CrtYd_offset

    kicad_mod.addRectLine({'x':x1-cy,'y':y1-cy},{'x':x2+cy,'y':y2+cy}, layer="F.CrtYd", width=CrtYd_linewidth)

    kicad_mod.model = _3dshapes + footprint_name + ".wrl"

    # output kicad model
    f = open(output_dir+footprint_name + ".kicad_mod","w")


    f.write(kicad_mod.__str__())

    f.close()
