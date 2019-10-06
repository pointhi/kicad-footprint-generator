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

series = "SPOX"
series_long = 'SPOX Connector System'
manufacturer = 'Molex'
orientation = 'H'
number_of_rows = 1
datasheet = 'https://www.molex.com/pdm_docs/sd/022057045_sd.pdf'

#pins_per_row per row
pins_per_row_range = range(2, 16)

#Molex part number
#n = number of circuits per row
part_code = "5268-{n:02}A"

pitch = 2.5
drill = 0.85

pad_to_pad_clearance = 0.8
max_annular_ring = 0.5
min_annular_ring = 0.15

pad_size = [pitch - pad_to_pad_clearance, drill + 2 * max_annular_ring]
if pad_size[0] - drill < 2 * min_annular_ring:
    pad_size[0] = drill + 2 * min_annular_ring
if pad_size[0] - drill > 2 * max_annular_ring:
    pad_size[0] = drill + 2 * max_annular_ring

pad_shape = Pad.SHAPE_OVAL
if pad_size[1] == pad_size[0]:
    pad_shape=Pad.SHAPE_CIRCLE

def generate_one_footprint(pins_per_row, configuration):
    mpn = part_code.format(n = pins_per_row * number_of_rows)

    # handle arguments
    orientation_str = configuration['orientation_options'][orientation]
    footprint_name = configuration['fp_name_format_string'].format(man = manufacturer,
        series = series,
        mpn = mpn, num_rows = number_of_rows, pins_per_row = pins_per_row, mounting_pad = "",
        pitch = pitch, orientation = orientation_str)

    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription("Molex {:s}, {:s}, {:d} Pins per row ({:s}), generated with kicad-footprint-generator".format(series_long, mpn, pins_per_row, datasheet))
    kicad_mod.setTags(configuration['keyword_fp_string'].format(series = series,
        orientation = orientation_str, man = manufacturer,
        entry = configuration['entry_direction'][orientation]))

    A = (pins_per_row - 1) * pitch
    C = A + 2 * 2.45

    #connector width
    W = 7.9
    chamfer_pin_n = {'x': 1, 'y': 1}

    off = configuration['silk_fab_offset']
    pad_silk_off = configuration['silk_pad_clearance'] + configuration['silk_line_width'] / 2

    body_edge = {}
    body_edge['left'] = (A - C) / 2
    body_edge['right'] = body_edge['left'] + C
    body_edge['top'] = -(7.9 - 6.6)
    body_edge['bottom'] = body_edge['top'] + W

    bounding_box = body_edge.copy()

    # generate the pads
    optional_pad_params = {}
    if configuration['kicad4_compatible']:
        optional_pad_params['tht_pad1_shape'] = Pad.SHAPE_RECT
    else:
        optional_pad_params['tht_pad1_shape'] = Pad.SHAPE_ROUNDRECT

    kicad_mod.append(PadArray(start = [0, 0], pincount = pins_per_row, x_spacing = pitch,
        type = Pad.TYPE_THT, shape = pad_shape, size = pad_size, drill = drill,
        layers = Pad.LAYERS_THT,
        **optional_pad_params))

    def generateOutline(off = 0, grid = 0):
        poly = [
                {'x': body_edge['left'] - off, 'y': body_edge['top'] - off},
                {'x': body_edge['left'] - off, 'y': body_edge['bottom'] + off},
                {'x': body_edge['right']+off, 'y':body_edge['bottom'] +off},
                {'x': body_edge['right'] + off, 'y': body_edge['top'] - off},
                {'x': body_edge['left'] - off, 'y': body_edge['top'] - off},
            ]
        if grid == 0:
            return poly
        else:
            return [{'x': roundToBase(p['x'], grid), 'y': roundToBase(p['y'], grid)} for p in poly]

    # outline on Fab
    kicad_mod.append(PolygoneLine(polygone = generateOutline(),
        layer = 'F.Fab', width = configuration['fab_line_width']))

    # outline on SilkScreen
    kicad_mod.append(PolygoneLine(polygone = generateOutline(off = off),
        layer = 'F.SilkS', width = configuration['silk_line_width']))

    #pin-1 mark
    sl = 2
    o = off + 0.3
    pin = [
        {'y': body_edge['top'] + sl, 'x': body_edge['left'] - o},
        {'y': body_edge['top'] - o, 'x': body_edge['left'] - o},
        {'y': body_edge['top'] - o, 'x': body_edge['left'] + sl}
    ]
    kicad_mod.append(PolygoneLine(polygone = pin,
        layer = 'F.SilkS', width = configuration['silk_line_width']))

    sl = 1
    pin = [
        {'y': sl / 2, 'x': body_edge['left']},
        {'y': 0, 'x': body_edge['left'] + sl / sqrt(2)},
        {'y': -sl / 2, 'x': body_edge['left']}
    ]
    kicad_mod.append(PolygoneLine(polygone = pin,
        width = configuration['fab_line_width'], layer = 'F.Fab'))

    ########################### CrtYd #################################
    poly_crtyd = generateOutline(configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])
    cy1 = poly_crtyd[0]['y']
    cy2 = poly_crtyd[1]['y']
    kicad_mod.append(PolygoneLine(
        polygone = poly_crtyd,
        layer = 'F.CrtYd', width = configuration['courtyard_line_width']))

    ######################### Text Fields ###############################
    addTextFields(kicad_mod = kicad_mod, configuration = configuration, body_edges = body_edge,
        courtyard = {'top': cy1, 'bottom': cy2},
        fp_name = footprint_name, text_y_inside_position = 'bottom')

    ##################### Output and 3d model ############################
    model3d_path_prefix = configuration.get('3d_model_prefix', '${KISYS3DMOD}/')

    lib_name = configuration['lib_name_format_string'].format(series = series, man = manufacturer)
    model_name = '{model3d_path_prefix:s}{lib_name:s}.3dshapes/{fp_name:s}.wrl'.format(
        model3d_path_prefix = model3d_path_prefix, lib_name = lib_name, fp_name = footprint_name)
    kicad_mod.append(Model(filename = model_name))

    output_dir = '{lib_name:s}.pretty/'.format(lib_name = lib_name)
    if not os.path.isdir(output_dir): #returns false if path does not yet exist!! (Does not check path validity)
        os.makedirs(output_dir)
    filename =  '{outdir:s}{fp_name:s}.kicad_mod'.format(outdir = output_dir, fp_name = footprint_name)

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

    for pins_per_row in pins_per_row_range:
        generate_one_footprint(pins_per_row, configuration)
