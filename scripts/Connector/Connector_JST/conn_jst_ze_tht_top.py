#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(sys.path[0],"..","..","kicad_mod"))

from math import floor,ceil

# export PYTHONPATH="${PYTHONPATH}<path to kicad-footprint-generator directory>"
sys.path.append(os.path.join(sys.path[0], "..", "..", ".."))  # load parent path of KicadModTree
import argparse
import yaml
from helpers import *
from KicadModTree import *

sys.path.append(os.path.join(sys.path[0], "..", "..", "tools"))  # load parent path of tools
from footprint_text_fields import addTextFields

series = "ZE"
manufacturer = 'JST'
orientation = 'V'
number_of_rows = 1
datasheet = 'http://www.jst-mfg.com/product/pdf/eng/eZE.pdf'

#ZE connector, top-entry THT, NO BOSS

pitch = 1.5
y_spacing = 2.0

drill = 0.75 # 0.7 +0.1/-0.0 -> 0.75 +/-0.05
mh_drill = 0.85

pad_size = [1.4, 1.75] # Measurements from freecad sketch (pad to pad clearance > 0.8 for a 45° trace.)

variant_parameters = {
    '1D': {
        'boss':True,
        'pin_range':range(2,17),
        'descr_str':', with boss'
        },
    'D': {
        'boss':False,
        'pin_range':range(3,17),
        'descr_str':''
        }
}
def generate_one_footprint(pincount, variant, configuration):
    mpn = "B{pincount:02}B-ZESK-{suff}".format(pincount=pincount,suff=variant)
    boss = variant_parameters[variant]['boss']

    orientation_str = configuration['orientation_options'][orientation]
    footprint_name = configuration['fp_name_format_string'].format(man=manufacturer,
        series=series,
        mpn=mpn, num_rows=number_of_rows, pins_per_row=pincount, mounting_pad = "",
        pitch=pitch, orientation=orientation_str)

    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription("JST {:s} series connector, {:s}{:s} ({:s}), generated with kicad-footprint-generator"\
        .format(series, mpn, variant_parameters[variant]['descr_str'], datasheet))

    tags = configuration['keyword_fp_string'].format(series=series,
        orientation=orientation_str, man=manufacturer,
        entry=configuration['entry_direction'][orientation])
    if boss:
        tags += ' boss'
    kicad_mod.setTags(tags)

    #dimensions
    A = (pincount - 1) * 1.5
    B = A + 4.5

    #outline
    x1 = -1.55 - 0.7
    x2 = x1 + B

    xMid = x1 + B/2

    y2 = 0.65
    y1 = y2 - 5.75
    body_edge={'left':x1, 'right':x2, 'top':y1, 'bottom':y2}

    #add outline to F.Fab
    kicad_mod.append(RectLine(
        start={'x': x1, 'y': y1},
        end={'x': x2, 'y': y2},
        layer='F.Fab', width=configuration['fab_line_width']
        ))

    ########################### CrtYd #################################
    cx1 = roundToBase(x1-configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])
    if y1 < -pad_size[1]/2:
        cy1 = roundToBase(y1-configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])
    else:
        cy1 = roundToBase(-pad_size[1]/2-configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])

    cx2 = roundToBase(x2+configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])
    cy2 = roundToBase(y2+configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])

    kicad_mod.append(RectLine(
        start=[cx1, cy1], end=[cx2, cy2],
        layer='F.CrtYd', width=configuration['courtyard_line_width']))


    # create odd numbered pads
    # createNumberedPadsTHT(kicad_mod, ceil(pincount/2), pitch * 2, drill, {'x':dia, 'y':dia},  increment=2)
    #special treatment for pin 1 (rectangular pad alone would reduce the clearance too much)
    if configuration['kicad4_compatible']:
        kicad_mod.append(Pad(number=1, at=[0, 0],
            size=pad_size, drill=drill,
            type=Pad.TYPE_THT, shape=Pad.SHAPE_OVAL, layers=Pad.LAYERS_THT))

        kicad_mod.append(Pad(number=1, at=[-pad_size[0]/4, 0],
            size=[pad_size[0]/2,pad_size[1]],
            type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, layers=['F.Cu', 'F.Mask']))
        kicad_mod.append(Pad(number=1, at=[-pad_size[0]/4, 0],
            size=[pad_size[0]/2,pad_size[1]],
            type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, layers=['B.Cu', 'B.Mask']))

    else:
        kicad_mod.append(ChamferedPad(number=1, at=[0, 0],
            size=pad_size, drill=drill,
            type=Pad.TYPE_THT, shape=Pad.SHAPE_OVAL, layers=Pad.LAYERS_THT,
            chamfer_size=0.4, radius_ratio=0.25, maximum_radius=0.25,
            corner_selection=CornerSelection({CornerSelection.TOP_RIGHT:True})))

    if pincount > 2:
        kicad_mod.append(PadArray(initial=3, start=[2*pitch, 0],
            x_spacing=pitch*2, pincount=ceil(pincount/2)-1,
            size=pad_size, drill=drill, increment=2,
            type=Pad.TYPE_THT, shape=Pad.SHAPE_OVAL, layers=Pad.LAYERS_THT))

    #create even numbered pads
    # createNumberedPadsTHT(kicad_mod, floor(pincount/2), pitch * 2, drill, {'x':dia, 'y':dia}, starting=2, increment=2, y_off=y_spacing, x_off=pitch)
    kicad_mod.append(PadArray(initial=2, start=[pitch, -y_spacing],
        x_spacing=pitch*2, pincount=floor(pincount/2),
        size=pad_size, drill=drill, increment=2,
        type=Pad.TYPE_THT, shape=Pad.SHAPE_OVAL, layers=Pad.LAYERS_THT))

    #expand the outline a little bit
    out = configuration['silk_fab_offset']
    x1 -= out
    x2 += out
    y1 -= out
    y2 += out

    silk_pad_offset = configuration['silk_line_width']/2 + configuration['silk_pad_clearance']
    if y2 > (pad_size[1]/2 + silk_pad_offset):
        kicad_mod.append(RectLine(start={'x':x1,'y':y1}, end={'x':x2,'y':y2},
            width=configuration['silk_line_width'], layer="F.SilkS"))
    else:
        num_odd_pins = ceil(pincount/2)
        pos_last_odd_pad = (num_odd_pins-1) * 2*pitch
        poly_silk = [
            {'x': -(pad_size[0]/2 + silk_pad_offset), 'y': y2},
            {'x': x1, 'y': y2},
            {'x': x1, 'y': y1},
            {'x': x2, 'y': y1},
            {'x': x2, 'y': y2},
            {'x': pos_last_odd_pad + (pad_size[0]/2 + silk_pad_offset), 'y': y2},
        ]
        kicad_mod.append(PolygoneLine(polygone=poly_silk,
            width=configuration['silk_line_width'], layer="F.SilkS"))
        for i in range(num_odd_pins-1):
            kicad_mod.append(Line(start=[i * 2*pitch + (pad_size[0]/2 + silk_pad_offset), y2],
                end=[(i+1) * 2*pitch - (pad_size[0]/2 + silk_pad_offset), y2],
                width=configuration['silk_line_width'], layer="F.SilkS"))


    #add mounting hole (only for the -1D option which has the boss)
    if boss:
        #     kicad_mod.append(MountingHole(
        #     {'x': -1.65, 'y': -3.8},
        #     1.1
        # )
        kicad_mod.append(Pad(at={'x': -1.65, 'y': -3.8}, type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE, layers=Pad.LAYERS_NPTH,
            drill=mh_drill, size=mh_drill))

    #thicknes t of sidewalls
    t = 0.8
    xa = xMid - A/2 - 0.25 + out
    xb = xMid + A/2 + 0.25 - out
    y3 = y1 + 1.7

    q = 0.4 #inner rect offset

    #outer rect
    kicad_mod.append(RectLine(
        start={'x': xa,'y': y1},
        end={'x': xb,'y': y3},
        width=configuration['silk_line_width'], layer="F.SilkS"
        ))

    #inner rect
    kicad_mod.append(RectLine(
        start={'x': xa+q,'y': y1+q},
        end={'x': xb-q,'y': y3-q},
        width=configuration['silk_line_width'], layer="F.SilkS"
        ))

    #left side
    if not boss:
        kicad_mod.append(PolygoneLine(polygone=[
            {'x': xa,'y': y3},
            {'x': x1+t,'y':y3},
            {'x': x1+t,'y':y2-t},
            {'x': -1,'y':y2-t},
        ], width=configuration['silk_line_width'], layer="F.SilkS"))
    else: #boss were declared
        kicad_mod.append(Line(
            start={'x': xa,'y': y3},
            end={'x': -0.9,'y': y3},
            width=configuration['silk_line_width'], layer="F.SilkS"
            ))

        kicad_mod.append(PolygoneLine(polygone=[
            {'x': x1+t,'y': -3},
            {'x': x1+t,'y': y2-t},
            {'x': -1,'y': y2-t},
        ], width=configuration['silk_line_width'], layer="F.SilkS"))
    #right side

    if pincount %2 == 0: #even number of pins
        xEnd = (pincount / 2 - 1) * (2 * pitch) + 1
    else:
        xEnd = floor(pincount / 2) * (2 * pitch) + 1

    kicad_mod.append(PolygoneLine(polygone=[
        {'x': xb,'y': y3},
        {'x': x2-t,'y': y3},
        {'x': x2-t,'y': y2-t},
        {'x': xEnd,'y': y2-t},
    ], width=configuration['silk_line_width'], layer="F.SilkS"))

    #draw lines between pads
    for i in range(0, ceil(pincount/2) - 1):

        X1 = i * 2 * pitch + pad_size[1]/2 + silk_pad_offset
        X2 = (i + 1) * 2 * pitch - (pad_size[1]/2 + silk_pad_offset)
        kicad_mod.append(Line(
            start={'x': X1,'y': y2-t},
            end={'x': X2,'y': y2-t},
            width=configuration['silk_line_width'], layer='F.SilkS'))

    #draw the 'vertical' lines where the actual pinny bits go

    #width of each slot w
    w = 0.15
    #clearance distance d
    d = 0.3
    # for i in range(pincount):
    #
    #     x = i * pitch
    #
    #     Y1 = y3 + d
    #     Y2 = -pad_size[1]/2 - d
    #
    #     kicad_mod.append(RectLine(start={'x':x-w, 'y': Y1},
    #     end={'x':x+w, 'y': Y2},
    #     width=configuration['fab_line_width'], layer='F.Fab'))

    # add pin-1 marking above the pin1

    d = 0.3
    l = 1.5
    xp1 = x1 - d
    xp2 = xp1 + l

    yp2 = y2 + d
    yp1 = yp2 - l

    pin1 = [
        {'x': xp1,'y': yp1},
        {'x': xp1,'y': yp2},
        {'x': xp2,'y': yp2},
    ]

    kicad_mod.append(PolygoneLine(polygone=pin1,width=configuration['silk_line_width'], layer='F.SilkS'))
    kicad_mod.append(PolygoneLine(polygone=pin1,layer='F.Fab', width=configuration['fab_line_width']))

    ######################### Text Fields ###############################
    addTextFields(kicad_mod=kicad_mod, configuration=configuration, body_edges=body_edge,
        courtyard={'top':cy1, 'bottom':cy2}, fp_name=footprint_name, text_y_inside_position='top')

    ##################### Output and 3d model ############################
    model3d_path_prefix = configuration.get('3d_model_prefix','${KISYS3DMOD}/')

    lib_name = configuration['lib_name_format_string'].format(series=series, man=manufacturer)
    model_name = '{model3d_path_prefix:s}{lib_name:s}.3dshapes/{fp_name:s}.wrl'.format(
        model3d_path_prefix=model3d_path_prefix, lib_name=lib_name, fp_name=footprint_name)
    kicad_mod.append(Model(filename=model_name))

    output_dir = '{lib_name:s}.pretty/'.format(lib_name=lib_name)
    if not os.path.isdir(output_dir): #returns false if path does not yet exist!! (Does not check path validity)
        os.makedirs(output_dir)
    filename =  '{outdir:s}{fp_name:s}.kicad_mod'.format(outdir=output_dir, fp_name=footprint_name)

    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile(filename)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='use confing .yaml files to create footprints.')
    parser.add_argument('--global_config', type=str, nargs='?', help='the config file defining how the footprint will look like. (KLC)', default='../../tools/global_config_files/config_KLCv3.0.yaml')
    parser.add_argument('--series_config', type=str, nargs='?', help='the config file defining series parameters.', default='../conn_config_KLCv3.yaml')
    parser.add_argument('--kicad4_compatible', action='store_true', help='Create footprints kicad 4 compatible')
    args = parser.parse_args()

    with open(args.global_config, 'r') as config_stream:
        try:
            configuration = yaml.safe_load(config_stream)
        except yaml.YAMLError as exc:
            print(exc)

    with open(args.series_config, 'r') as config_stream:
        try:
            configuration.update(yaml.safe_load(config_stream))
        except yaml.YAMLError as exc:
            print(exc)

    configuration['kicad4_compatible'] = args.kicad4_compatible

    for variant in variant_parameters:
        for pincount in variant_parameters[variant]['pin_range']:
            generate_one_footprint(pincount, variant, configuration)
