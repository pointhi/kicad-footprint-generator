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

series = "SL"
series_long = 'Stackable Linear Connector'
manufacturer = 'Molex'
orientation = 'V'
number_of_rows = 1

#pins_per_row_per_row per row
pins_per_row_range = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]

#Molex part number
#n = number of circuits per row
# Boss ist ohne zusätzliche Befestigungslöcher. Dafür gibt es eine komische zusätzliche Bohrung
variant_params = {
    'boss':{
        'mount_pins': False,
        'datasheet': 'https://www.molex.com/pdm_docs/sd/1719710002_sd.pdf',
        'part_code': "171971-00{n:02d}",
        'alternative_codes': [
            "171971-01{n:02d}",
            "171971-02{n:02d}"
            ]
        }
}

pitch = 2.54
drill = 1.09
start_pos_x = 0 # Where should pin 1 be located.
pad_to_pad_clearance = 0.8
max_annular_ring = 0.95 #How much copper should be in y direction?
min_annular_ring = 0.15

row = 2.54

size = row - pad_to_pad_clearance
if size - drill < 2 * min_annular_ring:
    size = drill + 2 * min_annular_ring
if size - drill > 2 * max_annular_ring:
    size = drill + 2 * max_annular_ring

# print("size", size)

def generate_one_footprint(pins_per_row, variant, configuration):
    mpn = variant_params[variant]['part_code'].format(n = pins_per_row)
    alt_mpn = [code.format(n=pins_per_row) for code in variant_params[variant]['alternative_codes']]

    # handle arguments
    orientation_str = configuration['orientation_options'][orientation]
    footprint_name = configuration['fp_name_format_string'].format(man = manufacturer,
        series = series,
        mpn = mpn, num_rows = number_of_rows, pins_per_row = pins_per_row, mounting_pad = "",
        pitch = pitch, orientation = orientation_str)

    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription("Molex {:s}, {:s} (compatible alternatives: {:s}), {:d} Pins per row ({:s}), generated with kicad-footprint-generator".format(series_long, mpn, ', '.join(alt_mpn), pins_per_row, variant_params[variant]['datasheet']))
    kicad_mod.setTags(configuration['keyword_fp_string'].format(series=series,
        orientation = orientation_str, man = manufacturer,
        entry = configuration['entry_direction'][orientation]))

    #calculate fp dimensions

    #connector length
    if pins_per_row == 2:
        A = 7.38
    else:
        A = pins_per_row * pitch + 2.46

    #pin centers
    P = (pins_per_row - 1) * pitch

    #connector width
    W = 5.1

    #corner positions
    x1 = -(A - P) / 2
    x2 = x1 + A

    y2 = W / 2
    y1 = y2 - W

    #tab length
    if pins_per_row == 2:
        tab_l = 6.86
    else:
        tab_l = 7.62
    #tab width
    tab_w = 1.50

    body_edge = {
        'left': x1,
        'right': x2,
        'bottom': y2,
        'top': y1
        }
    bounding_box = body_edge.copy()
    bounding_box['bottom'] = y2 + tab_w

    optional_pad_params = {}
    if configuration['kicad4_compatible']:
        optional_pad_params['tht_pad1_shape'] = Pad.SHAPE_RECT
    else:
        optional_pad_params['tht_pad1_shape'] = Pad.SHAPE_ROUNDRECT

    #generate the pads
    kicad_mod.append(PadArray(
        pincount = pins_per_row, initial = 1,
        start = [0, 0], x_spacing=pitch, type = Pad.TYPE_THT,
        shape = Pad.SHAPE_CIRCLE, size = size, drill = drill, layers = Pad.LAYERS_THT,
        **optional_pad_params))

    off = configuration['silk_fab_offset']
    silk_pad_off = configuration['silk_pad_clearance'] + configuration['silk_line_width'] / 2

    #draw the outline of the shape
    kicad_mod.append(PolygoneLine(polygone = [
            { 'x': body_edge['left'], 'y': body_edge['top'] },
            { 'x': body_edge['left'], 'y': body_edge['top'] + 2.31 },
            { 'x': body_edge['left'] + 0.13, 'y': body_edge['top'] + 2.31 },
            { 'x': body_edge['left'] + 0.13, 'y': body_edge['bottom'] - 0.76 },
            { 'x': body_edge['left'], 'y': body_edge['bottom'] - 0.76 },
            { 'x': body_edge['left'], 'y': body_edge['bottom'] },
            { 'x': body_edge['right'], 'y': body_edge['bottom'] },
            { 'x': body_edge['right'], 'y': body_edge['bottom'] - 0.76 },
            { 'x': body_edge['right'] - 0.13, 'y': body_edge['bottom'] - 0.76 },
            { 'x': body_edge['right'] - 0.13, 'y': body_edge['top'] + 2.31 },
            { 'x': body_edge['right'], 'y': body_edge['top'] + 2.31 },
            { 'x': body_edge['right'], 'y': body_edge['top'] },
            { 'x': body_edge['left'], 'y': body_edge['top'] },
        ],
        layer = 'F.Fab', width = configuration['fab_line_width']))

    #draw the outline of the tab
    kicad_mod.append(PolygoneLine(polygone = [
            { 'x': P / 2 - tab_l / 2,'y': y2} ,
            { 'x': P / 2 - tab_l / 2,'y': y2 + tab_w },
            { 'x': P / 2 + tab_l / 2,'y': y2 + tab_w },
            { 'x': P / 2 + tab_l / 2,'y': y2 },
        ], layer = 'F.Fab', width = configuration['fab_line_width']))

    #draw the outline of the connector on the silkscreen 
    kicad_mod.append(PolygoneLine(polygone = [
            { 'x': body_edge['left'] - off, 'y': body_edge['top'] - off },
            { 'x': body_edge['left'] - off, 'y': body_edge['top'] + 2.31 + off },
            { 'x': body_edge['left'] + 0.13 - off, 'y': body_edge['top'] + 2.31 + off },
            { 'x': body_edge['left'] + 0.13 - off, 'y': body_edge['bottom'] - 0.76 - off },
            { 'x': body_edge['left'] - off, 'y': body_edge['bottom'] - 0.76 - off },
            { 'x': body_edge['left'] - off, 'y': body_edge['bottom'] + off },
            { 'x': P / 2 - tab_l / 2 - off, 'y': y2 + off} ,
            { 'x': P / 2 - tab_l / 2 - off, 'y': y2 + tab_w + off },
            { 'x': P / 2 + tab_l / 2 + off,'y': y2 + tab_w + off },
            { 'x': P / 2 + tab_l / 2 + off,'y': y2 + off},
            { 'x': body_edge['right'] + off, 'y': body_edge['bottom'] + off },
            { 'x': body_edge['right'] + off, 'y': body_edge['bottom'] - 0.76 - off },
            { 'x': body_edge['right'] - 0.13 + off, 'y': body_edge['bottom'] - 0.76 - off },
            { 'x': body_edge['right'] - 0.13 + off, 'y': body_edge['top'] + 2.31 + off },
            { 'x': body_edge['right'] + off, 'y': body_edge['top'] + 2.31 + off },
            { 'x': body_edge['right'] + off, 'y': body_edge['top'] - off },
            { 'x': body_edge['left'] - off, 'y': body_edge['top'] - off },
        ], layer = 'F.SilkS', width = configuration['silk_line_width']))

    #pin-1 marker
    p1m_off = 0.3 + off
    p1m_sl = 2
    pin = [
        { 'x': body_edge['left'] - p1m_off, 'y': body_edge['top'] + p1m_sl },
        { 'x': body_edge['left'] - p1m_off, 'y': body_edge['top'] - p1m_off },
        { 'x': body_edge['left'] + p1m_sl, 'y': body_edge['top'] - p1m_off },
    ]
    kicad_mod.append(PolygoneLine(polygone = pin, layer = 'F.SilkS', width = configuration['silk_line_width']))

    sl = 1
    pin = [
        {'y': body_edge['top'], 'x':  sl / 2 },
        {'y': body_edge['top'] + sl / sqrt(2), 'x': 0 },
        {'y': body_edge['top'], 'x':  -sl / 2 }
    ]
    kicad_mod.append(PolygoneLine(polygone = pin, width = configuration['fab_line_width'], layer = 'F.Fab'))

    ########################### CrtYd #################################
    cx1 = roundToBase(bounding_box['left'] - configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])
    cy1 = roundToBase(bounding_box['top'] - configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])

    cx2 = roundToBase(bounding_box['right'] + configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])
    cy2 = roundToBase(bounding_box['bottom'] + configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])

    if variant_params[variant]['mount_pins']:
       pass
    else:
        kicad_mod.append(RectLine(
            start = [cx1, cy1], end = [cx2, cy2],
            layer = 'F.CrtYd', width = configuration['courtyard_line_width']))

    ######################### Text Fields ###############################
    addTextFields(kicad_mod = kicad_mod, configuration = configuration, body_edges = body_edge,
        courtyard = { 'top': cy1, 'bottom': cy2 }, fp_name = footprint_name, text_y_inside_position = 'bottom')

    ##################### Output and 3d model ############################
    model3d_path_prefix = configuration.get('3d_model_prefix','${KISYS3DMOD}/')

    lib_name = configuration['lib_name_format_string'].format(series=series, man=manufacturer)
    model_name = '{model3d_path_prefix:s}{lib_name:s}.3dshapes/{fp_name:s}.wrl'.format(
        model3d_path_prefix = model3d_path_prefix, lib_name = lib_name, fp_name = footprint_name)
    kicad_mod.append(Model(filename = model_name))

    output_dir = '{lib_name:s}.pretty/'.format(lib_name = lib_name)
    if not os.path.isdir(output_dir): #returns false if path does not yet exist!! (Does not check path validity)
        os.makedirs(output_dir)
    filename = '{outdir:s}{fp_name:s}.kicad_mod'.format(outdir = output_dir, fp_name = footprint_name)

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
