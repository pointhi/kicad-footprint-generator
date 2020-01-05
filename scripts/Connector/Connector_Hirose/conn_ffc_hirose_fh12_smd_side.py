#!/usr/bin/env python3

import sys
import os
#sys.path.append(os.path.join(sys.path[0],"..","..","kicad_mod")) # load kicad_mod path

# export PYTHONPATH="${PYTHONPATH}<path to kicad-footprint-generator directory>"
sys.path.append(os.path.join(sys.path[0], "..", "..", ".."))  # load parent path of KicadModTree
from math import sqrt
import argparse
import yaml
from helpers import *
from KicadModTree import *

sys.path.append(os.path.join(sys.path[0], "..", "..", "tools"))  # load parent path of tools
from footprint_text_fields import addTextFields
from footprint_keepout_area import addRectangularKeepout

series = 'FH12'
series_long = 'FH12, FFC/FPC connector'
manufacturer = 'Hirose'
orientation = 'H'
number_of_rows = 1
datasheet = 'https://www.hirose.com/product/en/products/FH12/FH12-24S-0.5SH(55)/'

conn_category = "FFC-FPC"

lib_by_conn_category = True

#pins_per_row per row
pins_per_row_range = [6,8,10,11,12,13,14,15,16,17,18,19,20,22,24,25,26,28,30,32,33,34,35,36,40,45,50,53]

part_code = "FH12-{n:d}S-0.5SH"

# x position mounting inner mounting pad edge relative to nearest pad center
center_pad_to_mounting_pad_edge = 1
# y dimensions for pad given relative to mounting pad edge
rel_pad_y_outside_edge = 5
rel_pad_y_inside_edge = 3.7
pad_size_x = 0.3
# y position for body edge relative to mounting pad edge (positive -> body extends outside bounding box)
rel_body_edge_y = 1.9
body_size_y = 5.6
# body_fin_protrusion: 1.6
# body_fin_width: 0.8
# x body edge relative to nearest pin
rel_body_edge_x = 1.8


pitch = 0.5
pad_size = [pad_size_x, rel_pad_y_outside_edge - rel_pad_y_inside_edge]
mp_size = [1.8, 2.2]

def generate_one_footprint(pins, configuration):
    mpn = part_code.format(n=pins)
    pad_silk_off = configuration['silk_line_width']/2 + configuration['silk_pad_clearance']
    off = configuration['silk_fab_offset']
    # handle arguments
    orientation_str = configuration['orientation_options'][orientation]
    footprint_name = configuration['fp_name_no_series_format_string'].format(man=manufacturer,
        series=series,
        mpn=mpn, num_rows=number_of_rows, pins_per_row=pins, mounting_pad = "-1MP",
        pitch=pitch, orientation=orientation_str)

    footprint_name = footprint_name.replace("__",'_')

    kicad_mod = Footprint(footprint_name)
    kicad_mod.setAttribute('smd')
    kicad_mod.setDescription("{:s} {:s}, {:s}, {:d} Pins per row ({:s}), generated with kicad-footprint-generator".format(manufacturer, series_long, mpn, pins_per_row, datasheet))
    kicad_mod.setTags(configuration['keyword_fp_string'].format(series=series,
        orientation=orientation_str, man=manufacturer,
        entry=configuration['entry_direction'][orientation]))

    A = (pins - 1) * pitch
    B = A + 2*rel_body_edge_x
    pad_y = -rel_pad_y_outside_edge/2 + pad_size[1]/2
    mpad_y = rel_pad_y_outside_edge/2 - mp_size[1]/2
    mpad_x = A/2 + center_pad_to_mounting_pad_edge + mp_size[0]/2

    kicad_mod.append(Pad(number=configuration['mounting_pad_number'], type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
                        at=[mpad_x, mpad_y], size=mp_size, layers=Pad.LAYERS_SMT))
    kicad_mod.append(Pad(number=configuration['mounting_pad_number'], type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
                        at=[-mpad_x, mpad_y], size=mp_size, layers=Pad.LAYERS_SMT))

    # create pads
    #createNumberedPadsTHT(kicad_mod, pincount, pitch, drill, {'x':x_dia, 'y':y_dia})
    kicad_mod.append(PadArray(center=[0,pad_y], pincount=pins, x_spacing=pitch,
        type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, size=pad_size, layers=Pad.LAYERS_SMT))


    x1 = -B/2
    x2 = x1 + B
    y2 = mpad_y + mp_size[1]/2 + rel_body_edge_y
    y1 = y2 - body_size_y

    body_edge={
        'left':x1,
        'right':x2,
        'bottom':y2,
        'top': y1
        }

    bounding_box = body_edge.copy()
    bounding_box['top'] = pad_y - pad_size[1]/2
    bb_x = mpad_x + mp_size[0]/2
    if  bb_x > x2:
        bounding_box['left'] = -bb_x
        bounding_box['right'] = bb_x


    main_body_bottom = body_edge['top'] + 4.6
    gap_body_hatch = 0.3
    gab_body_hatch_depth = 0.6
    hatch_reduced_width = 0.2

    poly_outline = [
        {'x': 0, 'y':  body_edge['top']},
        {'x': body_edge['left'], 'y':  body_edge['top']},
        {'x': body_edge['left'], 'y':  main_body_bottom},
        {'x': body_edge['left'] + gab_body_hatch_depth, 'y':  main_body_bottom},
        {'x': body_edge['left'] + gab_body_hatch_depth, 'y':  main_body_bottom + gap_body_hatch},
        {'x': body_edge['left'] + hatch_reduced_width/2, 'y':  main_body_bottom + gap_body_hatch},
        {'x': body_edge['left'] + hatch_reduced_width/2, 'y':  body_edge['bottom']},
        {'x': 0, 'y':  body_edge['bottom']}
    ]
    kicad_mod.append(PolygoneLine(
        polygone=poly_outline,
        layer='F.Fab', width=configuration['fab_line_width']))
    kicad_mod.append(PolygoneLine(
        polygone=poly_outline, x_mirror = 0.0000000001,
        layer='F.Fab', width=configuration['fab_line_width']))

    #line offset
    off = 0.1

    x1 -= off
    y1 -= off

    x2 += off
    y2 += off

    #draw the main outline around the footprint
    silk_pad_x_left = -A/2 - pad_size[0]/2 - pad_silk_off
    silk_mp_top = mpad_y - mp_size[1]/2 - pad_silk_off
    silk_mp_bottom = mpad_y + mp_size[1]/2 + pad_silk_off
    kicad_mod.append(PolygoneLine(
        polygone=[
            {'x': silk_pad_x_left,'y':y1},
            {'x': x1,'y':y1},
            {'x': x1,'y':silk_mp_top}
        ],
        layer='F.SilkS', width=configuration['silk_line_width']))

    kicad_mod.append(PolygoneLine(
        polygone=[
            {'x': -silk_pad_x_left,'y':y1},
            {'x': x2,'y':y1},
            {'x': x2,'y':silk_mp_top}
        ],
        layer='F.SilkS', width=configuration['silk_line_width']))

    kicad_mod.append(PolygoneLine(
        polygone=[
            {'x': x1,'y':silk_mp_bottom},
            {'x': x1,'y':y2},
            {'x': x2,'y':y2},
            {'x': x2,'y':silk_mp_bottom}
        ],
        layer='F.SilkS', width=configuration['silk_line_width']))


    #add pin-1 marker

    kicad_mod.append(Line(
        start=[silk_pad_x_left, y1], end=[silk_pad_x_left, pad_y - pad_size[1]/2],
                layer='F.SilkS', width=configuration['silk_line_width']))

    sl=1
    pin = [
        {'y': body_edge['top'], 'x': -A/2-sl/2},
        {'y': body_edge['top'] + sl/sqrt(2), 'x': -A/2},
        {'y': body_edge['top'], 'x': -A/2+sl/2}
    ]
    kicad_mod.append(PolygoneLine(polygone=pin,
        width=configuration['fab_line_width'], layer='F.Fab'))


    ########################### KEEPOUT #################################

    # k_top = pad_y + pad_size[1]/2 + 0.1
    # k_size = [A + pad_size[0], 2.37]
    # addRectangularKeepout(kicad_mod, [0, k_top+k_size[1]/2], k_size)


    ########################### CrtYd #################################
    cx1 = roundToBase(bounding_box['left']-configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])
    cy1 = roundToBase(bounding_box['top']-configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])

    cx2 = roundToBase(bounding_box['right']+configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])
    cy2 = roundToBase(bounding_box['bottom'] + configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])

    kicad_mod.append(RectLine(
        start=[cx1, cy1], end=[cx2, cy2],
        layer='F.CrtYd', width=configuration['courtyard_line_width']))

    ######################### Text Fields ###############################
    addTextFields(kicad_mod=kicad_mod, configuration=configuration, body_edges=body_edge,
        courtyard={'top':cy1, 'bottom':cy2}, fp_name=footprint_name, text_y_inside_position='bottom')

    ##################### Output and 3d model ############################
    model3d_path_prefix = configuration.get('3d_model_prefix','${KISYS3DMOD}/')


    if lib_by_conn_category:
        lib_name = configuration['lib_name_specific_function_format_string'].format(category=conn_category)
    else:
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
    for pins_per_row in pins_per_row_range:
        generate_one_footprint(pins_per_row, configuration)
