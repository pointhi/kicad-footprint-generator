#!/usr/bin/env python3

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

series = "Micro-Fit_3.0"
series_long = 'Micro-Fit 3.0 Connector System'
manufacturer = 'Molex'
orientation = 'H'
number_of_rows = 2
variants = {'non-clip': '0', 'clip': '2'}
datasheet = 'https://www.molex.com/pdm_docs/sd/4304502{s}1_sd.pdf'

#Molex part number
#n = number of circuits per row
part_code = "43045-{n:02}{s}{finish}"

pins_per_row_range = range(1,13)
pitch = 3.0
drill = 1.02
peg_drill = 3.0
clip_drill = 2.41
clip_pad = [clip_drill + 1, clip_drill + 1]
pad_to_pad_clearance = 1.5 # Voltage rating is up to 600V (http://www.molex.com/pdm_docs/ps/PS-43045.pdf)

pad_size = [pitch - pad_to_pad_clearance, pitch - pad_to_pad_clearance]

def generate_one_footprint(pins, configuration, variant):
    pins_per_row = pins

    mpn = part_code.format(n=pins*2,s=variants[variant],finish=max(int(variants[variant]) - 1, 0))
    alt_mpn = part_code.format(n=pins*2,s=variants[variant],finish='x')

    # handle arguments
    orientation_str = configuration['orientation_options'][orientation]
    footprint_name = configuration['fp_name_format_string'].format(man=manufacturer,
        series=series,
        mpn=mpn, num_rows=number_of_rows, pins_per_row=pins_per_row, mounting_pad = '-1MP' if variant == 'clip' else "",
        pitch=pitch, orientation=orientation_str)

    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription("Molex {:s}, {:s} (alternative finishes: {:s}), {:d} Pins per row ({:s}), generated with kicad-footprint-generator".format(series_long, mpn, alt_mpn, pins_per_row, datasheet.format(s=variants[variant])))
    kicad_mod.setTags(configuration['keyword_fp_string'].format(series=series,
        orientation=orientation_str, man=manufacturer,
        entry=configuration['entry_direction'][orientation]))

    ########################## Dimensions ##############################
    B = (pins_per_row-1)*pitch
    A = B + 6.65

    #Puts first pin on 0,0 and second row 0, pitch
    pad_row_1_y = 0
    pad_row_2_y = pad_row_1_y + pitch
    pad1_x = 0

    peg_clip_y_offset = 4.32
    peg_x_offset = 2.16
    clip_x_offset = -2.15
    peg_C = 1.7 + pitch*(pins-3) #1º need be 4.7mm
    clip_C = 4.3 + pitch*(pins-1)

    body_edge={
        'left':-3.325-0.25,
        'right':A-3.325+0.25,
        'top': -12.24+3+0.64/2
        }
    body_edge['bottom'] = body_edge['top'] + 9.91
    
    bevel = 1

    ############################# Pads ##################################
    #
    # Pegs
    #
    if variant == 'non-clip':
        if pins_per_row == 1:
            kicad_mod.append(Pad(at=[0, pad_row_1_y - peg_clip_y_offset], number="",
                type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE, size=peg_drill,
                drill=peg_drill, layers=Pad.LAYERS_NPTH))
        elif pins_per_row == 2:
            kicad_mod.append(Pad(at=[pitch/2, pad_row_1_y - peg_clip_y_offset], number="",
                type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE, size=peg_drill,
                drill=peg_drill, layers=Pad.LAYERS_NPTH))
        elif pins_per_row == 3:
            kicad_mod.append(Pad(at=[pitch, pad_row_1_y - peg_clip_y_offset], number="",
                type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE, size=peg_drill,
                drill=peg_drill, layers=Pad.LAYERS_NPTH))
        else:
            kicad_mod.append(Pad(at=[pad1_x + peg_x_offset, pad_row_1_y - peg_clip_y_offset], number="",
                type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE, size=peg_drill,
                drill=peg_drill, layers=Pad.LAYERS_NPTH))
            kicad_mod.append(Pad(at=[pad1_x + peg_x_offset + peg_C, pad_row_1_y - peg_clip_y_offset], number="",
                type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE, size=peg_drill,
                drill=peg_drill, layers=Pad.LAYERS_NPTH))
    elif variant == 'clip':
        kicad_mod.append(Pad(at=[pad1_x + clip_x_offset, pad_row_1_y - peg_clip_y_offset], number="MP",
            type=Pad.TYPE_THT, shape=Pad.SHAPE_OVAL, size=clip_pad,
            drill=clip_drill, layers=Pad.LAYERS_THT))
        kicad_mod.append(Pad(at=[pad1_x + clip_x_offset + clip_C, pad_row_1_y - peg_clip_y_offset], number="MP",
            type=Pad.TYPE_THT, shape=Pad.SHAPE_OVAL, size=clip_pad,
            drill=clip_drill, layers=Pad.LAYERS_THT))
    
    #
    # Add pads
    #
    optional_pad_params = {}
    if configuration['kicad4_compatible']:
        optional_pad_params['tht_pad1_shape'] = Pad.SHAPE_RECT
    else:
        optional_pad_params['tht_pad1_shape'] = Pad.SHAPE_ROUNDRECT

    kicad_mod.append(PadArray(start=[pad1_x, pad_row_1_y], initial=1,
        pincount=pins_per_row, increment=1,  x_spacing=pitch, size=pad_size,
        type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE, layers=Pad.LAYERS_THT, drill=drill,
        **optional_pad_params))

    kicad_mod.append(PadArray(start=[pad1_x, pad_row_2_y], initial=pins_per_row+1,
        pincount=pins_per_row, increment=1, x_spacing=pitch, size=pad_size,
        type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE, layers=Pad.LAYERS_THT, drill=drill,
        **optional_pad_params))

    ######################## Clip copper keepout ###########################
    if variant == 'clip':
        keepout_width = 2.45
        keepout_height = 1.6
        keepout_center_x = [body_edge['left'] - 0.75 + keepout_width / 2, body_edge['right'] + 0.75 - keepout_width / 2]
        keepout_center_y = body_edge['bottom'] - 3.25 + keepout_height / 2
        keepout_text = 'CU KEEPOUT'
        keepout_text_width = keepout_width / len(keepout_text)
        keepout_text_thickness = keepout_text_width * 0.15
        kicad_mod.append(PolygoneLine(polygone=[[keepout_center_x[0] - keepout_width/2, keepout_center_y - keepout_height/2],
            [keepout_center_x[0] - keepout_width/2, keepout_center_y + keepout_height/2],
            [keepout_center_x[0] + keepout_width/2, keepout_center_y + keepout_height/2],
            [keepout_center_x[0] + keepout_width/2, keepout_center_y - keepout_height/2],
            [keepout_center_x[0] - keepout_width/2, keepout_center_y - keepout_height/2]],
            layer='Dwgs.User', width=0.1))
        kicad_mod.append(PolygoneLine(polygone=[[keepout_center_x[1] - keepout_width/2, keepout_center_y - keepout_height/2],
            [keepout_center_x[1] - keepout_width/2, keepout_center_y + keepout_height/2],
            [keepout_center_x[1] + keepout_width/2, keepout_center_y + keepout_height/2],
            [keepout_center_x[1] + keepout_width/2, keepout_center_y - keepout_height/2],
            [keepout_center_x[1] - keepout_width/2, keepout_center_y - keepout_height/2]],
            layer='Dwgs.User', width=0.1))
        kicad_mod.append(Text(type='user', text='CU KEEPOUT', at=[keepout_center_x[0], keepout_center_y],
            layer='Cmts.User', size=[keepout_text_width, keepout_text_width], thickness=keepout_text_thickness))
        kicad_mod.append(Text(type='user', text='CU KEEPOUT', at=[keepout_center_x[1], keepout_center_y],
            layer='Cmts.User', size=[keepout_text_width, keepout_text_width], thickness=keepout_text_thickness))


    ######################## Fabrication Layer ###########################
    main_body_poly= [
        {'x': body_edge['left'], 'y': body_edge['bottom']},
        {'x': body_edge['left'], 'y': body_edge['top'] + bevel},
        {'x': body_edge['left'] + bevel, 'y': body_edge['top']},
        {'x': body_edge['right'] - bevel, 'y': body_edge['top']},
        {'x': body_edge['right'], 'y': body_edge['top'] + bevel},
        {'x': body_edge['right'], 'y': body_edge['bottom']},
        {'x': body_edge['left'], 'y': body_edge['bottom']}
    ]
    kicad_mod.append(PolygoneLine(polygone=main_body_poly,
        width=configuration['fab_line_width'], layer="F.Fab"))

    main_arrow_poly= [
        {'x': -.75, 'y': body_edge['bottom']},
        {'x': 0, 'y': 0},
        {'x': 0.75, 'y': body_edge['bottom']}
    ]
    kicad_mod.append(PolygoneLine(polygone=main_arrow_poly,
        width=configuration['fab_line_width'], layer="F.Fab"))

    ######################## SilkS Layer ###########################
    if variant == 'non-clip':
        poly_s_t= [
            {'x': body_edge['left'] - configuration['silk_fab_offset'], 'y': body_edge['bottom'] + configuration['silk_fab_offset']},
            {'x': body_edge['left'] - configuration['silk_fab_offset'], 'y': body_edge['top'] + bevel - configuration['silk_fab_offset']},
            {'x': body_edge['left'] + bevel - configuration['silk_fab_offset'], 'y': body_edge['top'] - configuration['silk_fab_offset']},
            {'x': body_edge['right'] - bevel + configuration['silk_fab_offset'], 'y': body_edge['top'] - configuration['silk_fab_offset']},
            {'x': body_edge['right'] + configuration['silk_fab_offset'], 'y': body_edge['top'] + bevel - configuration['silk_fab_offset']},
            {'x': body_edge['right'] + configuration['silk_fab_offset'], 'y': body_edge['bottom'] + configuration['silk_fab_offset']},
            {'x': body_edge['left'] - configuration['silk_fab_offset'], 'y': body_edge['bottom'] + configuration['silk_fab_offset']},
        ]
        kicad_mod.append(PolygoneLine(polygone=poly_s_t,
            width=configuration['silk_line_width'], layer="F.SilkS"))
    if variant == 'clip':
        # top side (away from pins)
        poly_s_t= [
            {'x': body_edge['left'] - configuration['silk_fab_offset'], 'y': pad_row_1_y - peg_clip_y_offset - clip_pad[1]/2 + configuration['silk_fab_offset']},
            {'x': body_edge['left'] - configuration['silk_fab_offset'], 'y': body_edge['top'] + bevel - configuration['silk_fab_offset']},
            {'x': body_edge['left'] + bevel - configuration['silk_fab_offset'], 'y': body_edge['top'] - configuration['silk_fab_offset']},
            {'x': body_edge['right'] - bevel + configuration['silk_fab_offset'], 'y': body_edge['top'] - configuration['silk_fab_offset']},
            {'x': body_edge['right'] + configuration['silk_fab_offset'], 'y': body_edge['top'] + bevel - configuration['silk_fab_offset']},
            {'x': body_edge['right'] + configuration['silk_fab_offset'], 'y':  pad_row_1_y - peg_clip_y_offset - clip_pad[1]/2 + configuration['silk_fab_offset']},
            #{'x': body_edge['left'] - configuration['silk_fab_offset'], 'y': body_edge['bottom'] + configuration['silk_fab_offset']},
        ]
        kicad_mod.append(PolygoneLine(polygone=poly_s_t,
            width=configuration['silk_line_width'], layer="F.SilkS"))
        # bottom side (closest to pins)
        poly_s_t= [
            {'x': body_edge['left'] - configuration['silk_fab_offset'], 'y': pad_row_1_y - peg_clip_y_offset + clip_pad[1]/2 - configuration['silk_fab_offset']},
            {'x': body_edge['left'] - configuration['silk_fab_offset'], 'y': body_edge['bottom'] + configuration['silk_fab_offset']},
            #{'x': body_edge['left'] + bevel - configuration['silk_fab_offset'], 'y': body_edge['top'] - configuration['silk_fab_offset']},
            #{'x': body_edge['right'] - bevel + configuration['silk_fab_offset'], 'y': body_edge['top'] - configuration['silk_fab_offset']},
            #{'x': body_edge['right'] + configuration['silk_fab_offset'], 'y': body_edge['top'] + bevel - configuration['silk_fab_offset']},
            {'x': body_edge['right'] + configuration['silk_fab_offset'], 'y': body_edge['bottom'] + configuration['silk_fab_offset']},
            {'x': body_edge['right'] + configuration['silk_fab_offset'], 'y': pad_row_1_y - peg_clip_y_offset + clip_pad[1]/2 - configuration['silk_fab_offset']}
            #{'x': body_edge['left'] - configuration['silk_fab_offset'], 'y': body_edge['bottom'] + configuration['silk_fab_offset']},
        ]
        kicad_mod.append(PolygoneLine(polygone=poly_s_t,
            width=configuration['silk_line_width'], layer="F.SilkS"))

    ######################## CrtYd Layer ###########################
    CrtYd_offset = configuration['courtyard_offset']['connector']
    CrtYd_grid = configuration['courtyard_grid']
    CrtYd_left = pad1_x + clip_x_offset - clip_pad[0]/2 if variant == 'clip' else body_edge['left']
    CrtYd_right = pad1_x + clip_x_offset + clip_C + clip_pad[0]/2 if variant == 'clip' else body_edge['right']

    poly_yd = [
        {'x': roundToBase(CrtYd_left - CrtYd_offset, CrtYd_grid), 'y': roundToBase(body_edge['bottom'] + CrtYd_offset, CrtYd_grid)},
        {'x': roundToBase(CrtYd_left - CrtYd_offset, CrtYd_grid), 'y': roundToBase(body_edge['top'] - CrtYd_offset, CrtYd_grid)},
        {'x': roundToBase(CrtYd_right + CrtYd_offset, CrtYd_grid), 'y': roundToBase(body_edge['top'] - CrtYd_offset, CrtYd_grid)},
        {'x': roundToBase(CrtYd_right + CrtYd_offset, CrtYd_grid), 'y': roundToBase(body_edge['bottom'] + CrtYd_offset, CrtYd_grid)},
        {'x': roundToBase(B + pad_to_pad_clearance/2 + CrtYd_offset, CrtYd_grid), 'y': roundToBase(body_edge['bottom'] + CrtYd_offset, CrtYd_grid)},
        {'x': roundToBase(B + pad_to_pad_clearance/2 + CrtYd_offset, CrtYd_grid), 'y': roundToBase(pitch + pad_to_pad_clearance/2 + CrtYd_offset, CrtYd_grid)},
        {'x': roundToBase(- pad_to_pad_clearance/2 - CrtYd_offset, CrtYd_grid), 'y': roundToBase(pitch + pad_to_pad_clearance/2 + CrtYd_offset, CrtYd_grid)},
        {'x': roundToBase(- pad_to_pad_clearance/2 - CrtYd_offset, CrtYd_grid), 'y': roundToBase(body_edge['bottom'] + CrtYd_offset, CrtYd_grid)},
        {'x': roundToBase(CrtYd_left - CrtYd_offset, CrtYd_grid), 'y': roundToBase(body_edge['bottom'] + CrtYd_offset, CrtYd_grid)}
    ]

    kicad_mod.append(PolygoneLine(polygone=poly_yd,
        layer='F.CrtYd', width=configuration['courtyard_line_width']))

    ######################### Text Fields ###############################
    cy1 = roundToBase(body_edge['top'] - configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])
    cy2 = roundToBase(pad_row_2_y + pad_size[1] + configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])

    addTextFields(kicad_mod=kicad_mod, configuration=configuration, body_edges=body_edge,
        courtyard={'top':cy1, 'bottom':cy2}, fp_name=footprint_name, text_y_inside_position='top')

    ##################### Write to File and 3D ############################
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

    for pincount in pins_per_row_range:
        for variant in variants:
            generate_one_footprint(pincount, configuration, variant)
