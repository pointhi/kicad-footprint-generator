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
orientation = 'V'
number_of_rows = 1

variant_params = {
    'solder_mounting':{
        'mount_pins': 'solder', # remove this
        'datasheet': 'http://www.molex.com/pdm_docs/sd/436500215_sd.pdf',
        'C_minus_B': 6,
        'part_code': "43650-{n:02}15",
        'alternative_codes': [
            "43650-{n:02}16",
            "43650-{n:02}17"
            ]
        },
}

pins_per_row_range = range(2,13)
pitch = 3.0
drill = 1.02
peg_drill = 1.27
pad_to_pad_clearance = 1.5 # Voltage rating is up to 600V (http://www.molex.com/pdm_docs/ps/PS-43650.pdf)
max_annular_ring = 0.5
min_annular_ring = 0.15

pad_size = [pitch - pad_to_pad_clearance, drill + 2*max_annular_ring]
if pad_size[0] - drill < 2*min_annular_ring:
    pad_size[0] = drill + 2*min_annular_ring
if pad_size[0] - drill > 2*max_annular_ring:
    pad_size[0] = drill + 2*max_annular_ring

if pad_size[1] - drill < 2*min_annular_ring:
    pad_size[1] = drill + 2*min_annular_ring
if pad_size[1] - drill > 2*max_annular_ring:
    pad_size[1] = drill + 2*max_annular_ring

pad_shape=Pad.SHAPE_OVAL
if pad_size[1] == pad_size[0]:
    pad_shape=Pad.SHAPE_CIRCLE

def generate_one_footprint(pins_per_row, variant, configuration):
    mpn = variant_params[variant]['part_code'].format(n=pins_per_row*number_of_rows)
    alt_mpn = [code.format(n=pins_per_row*number_of_rows) for code in variant_params[variant]['alternative_codes']]

    # handle arguments
    orientation_str = configuration['orientation_options'][orientation]
    footprint_name = configuration['fp_name_format_string'].format(man=manufacturer,
        series=series,
        mpn=mpn, num_rows=number_of_rows, pins_per_row=pins_per_row, mounting_pad = "",
        pitch=pitch, orientation=orientation_str)

    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription("Molex {:s}, {:s} (compatible alternatives: {:s}), {:d} Pins per row ({:s}), generated with kicad-footprint-generator".format(series_long, mpn, ', '.join(alt_mpn), pins_per_row, variant_params[variant]['datasheet']))
    kicad_mod.setTags(configuration['keyword_fp_string'].format(series=series,
        orientation=orientation_str, man=manufacturer,
        entry=configuration['entry_direction'][orientation]))

    #kicad_mod.setAttribute('smd')

    ########################## Dimensions ##############################
    B = (pins_per_row-1)*pitch
    A = B + 6.65
    C = B + variant_params[variant]['C_minus_B']

    pad_y = 0
    pad1_x = 0

    peg1_x = (B-C)/2
    peg2_x = (B+C)/2
    peg_y = pad_y - 1.96

    tab_w = 1.4
    tab_l = 1.4

    body_edge={
        'left':  (B-A)/2,
        'right': (A+B)/2,
        'top': -2.47+0.5
        }
    body_edge['bottom'] = body_edge['top'] + (4.37-0.5)

    y_top_min = -2.47
    chamfer={'x': 1.2, 'y': 0.63}

    ############################# Pads ##################################
    #
    # Pegs
    #
    kicad_mod.append(Pad(at=[peg1_x, peg_y], number="",
        type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE, size=peg_drill,
        drill=peg_drill, layers=Pad.LAYERS_NPTH))
    kicad_mod.append(Pad(at=[peg2_x, peg_y], number="",
        type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE, size=peg_drill,
        drill=peg_drill, layers=Pad.LAYERS_NPTH))

    #
    # Add pads
    #
    optional_pad_params = {}
    if configuration['kicad4_compatible']:
        optional_pad_params['tht_pad1_shape'] = Pad.SHAPE_RECT
    else:
        optional_pad_params['tht_pad1_shape'] = Pad.SHAPE_ROUNDRECT

    kicad_mod.append(PadArray(start=[pad1_x, pad_y], initial=1,
        pincount=pins_per_row, increment=1,  x_spacing=pitch, size=pad_size,
        type=Pad.TYPE_THT, shape=pad_shape, layers=Pad.LAYERS_THT, drill=drill,
        **optional_pad_params))

    ######################## Fabrication Layer ###########################
    main_body_poly= [
        {'x': body_edge['left'] + chamfer['x'], 'y': body_edge['top']},
        {'x': body_edge['left'] + chamfer['x'], 'y': y_top_min},
        {'x': body_edge['left'], 'y': y_top_min},
        {'x': body_edge['left'], 'y': body_edge['bottom']},
        {'x': body_edge['right'], 'y': body_edge['bottom']},
        {'x': body_edge['right'], 'y': y_top_min},
        {'x': body_edge['right'] - chamfer['x'], 'y': y_top_min},
        {'x': body_edge['right'] - chamfer['x'], 'y': body_edge['top']},
        {'x': body_edge['left'] + chamfer['x'], 'y': body_edge['top']}
    ]
    kicad_mod.append(PolygoneLine(polygone=main_body_poly,
        width=configuration['fab_line_width'], layer="F.Fab"))

    kicad_mod.append(Line(
        start={
            'x': body_edge['left'],
            'y': body_edge['top'] + chamfer['y']
        },
        end={
            'x': body_edge['left'] + chamfer['x'],
            'y': body_edge['top']
        },
        width=configuration['fab_line_width'], layer="F.Fab"
        ))

    kicad_mod.append(Line(
        start={
            'x': body_edge['right'],
            'y': body_edge['top'] + chamfer['y']
        },
        end={
            'x': body_edge['right'] - chamfer['x'],
            'y': body_edge['top']
        },
        width=configuration['fab_line_width'], layer="F.Fab"
        ))


    tab_poly = [
        {'x': B/2-tab_l/2, 'y': body_edge['bottom']},
        {'x': B/2-tab_l/2, 'y': body_edge['bottom'] + tab_w},
        {'x': B/2+tab_l/2, 'y': body_edge['bottom'] + tab_w},
        {'x': B/2+tab_l/2, 'y': body_edge['bottom']},
    ]
    kicad_mod.append(PolygoneLine(polygone=tab_poly,
        width=configuration['fab_line_width'], layer="F.Fab"))

    p1m_sl = 1
    p1m_poly = tab_poly = [
        {'x': pad1_x - p1m_sl/2, 'y': body_edge['top']},
        {'x': pad1_x, 'y': body_edge['top'] + p1m_sl/sqrt(2)},
        {'x': pad1_x + p1m_sl/2, 'y': body_edge['top']}
    ]
    kicad_mod.append(PolygoneLine(polygone=tab_poly,
        width=configuration['fab_line_width'], layer="F.Fab"))

    ############################ SilkS ##################################
    # Top left corner

    silk_pad_off = configuration['silk_pad_clearance'] + configuration['silk_line_width']/2

    xmp_top1 = peg1_x + peg_drill/2 + silk_pad_off
    xmp_top2 = peg2_x - peg_drill/2 - silk_pad_off
    ymp_bottom = peg_y + peg_drill/2 + silk_pad_off
    off = configuration['silk_fab_offset']

    poly_s_b = [
        {'x': body_edge['left'] - off, 'y': ymp_bottom},
        {'x': body_edge['left'] - off, 'y': body_edge['bottom'] + off},
        {'x': body_edge['right'] + off, 'y': body_edge['bottom'] + off},
        {'x': body_edge['right'] + off, 'y': ymp_bottom},
    ]

    kicad_mod.append(PolygoneLine(polygone=poly_s_b,
        width=configuration['silk_line_width'], layer="F.SilkS"))

    poly_s_t = [
        {'x': xmp_top1 + off, 'y': y_top_min - off},
        {'x': body_edge['left'] + chamfer['x'] + off, 'y': y_top_min - off},
        {'x': body_edge['left'] + chamfer['x'] + off, 'y': body_edge['top'] - off},
        {'x': body_edge['right'] - chamfer['x'] - off, 'y': body_edge['top'] - off},
        {'x': body_edge['right'] - chamfer['x'] - off, 'y': y_top_min - off},
        {'x': xmp_top2 - off, 'y': y_top_min - off},
    ]
    kicad_mod.append(PolygoneLine(polygone=poly_s_t,
        width=configuration['silk_line_width'], layer="F.SilkS"))

    ############################ CrtYd ##################################
    CrtYd_offset = configuration['courtyard_offset']['connector']
    CrtYd_grid = configuration['courtyard_grid']

    cy_top = roundToBase(y_top_min - CrtYd_offset, CrtYd_grid)
    cy_bottom = roundToBase(body_edge['bottom'] + tab_w + CrtYd_offset, CrtYd_grid)
    cy_left = roundToBase(body_edge['left'] - CrtYd_offset, CrtYd_grid)
    cy_right = roundToBase(body_edge['right'] + CrtYd_offset, CrtYd_grid)

    poly_cy = [
        {'x': cy_left, 'y':cy_top},
        {'x': cy_right, 'y':cy_top},
        {'x': cy_right, 'y':cy_bottom},
        {'x': cy_left, 'y':cy_bottom},
        {'x': cy_left, 'y':cy_top},
    ]

    kicad_mod.append(PolygoneLine(polygone=poly_cy,
        layer='F.CrtYd', width=configuration['courtyard_line_width']))

    ######################### Text Fields ###############################

    addTextFields(kicad_mod=kicad_mod, configuration=configuration, body_edges=body_edge,
        courtyard={'top':cy_top, 'bottom':cy_bottom}, fp_name=footprint_name, text_y_inside_position='bottom')

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

    for variant in variant_params:
        for pins_per_row in pins_per_row_range:
            generate_one_footprint(pins_per_row, variant, configuration)
