#!/usr/bin/env python3

# KicadModTree is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# KicadModTree is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with kicad-footprint-generator. If not, see < http://www.gnu.org/licenses/ >.
#
# (C) 2016 by Thomas Pointhuber, <thomas.pointhuber@gmx.at>

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

series = ""
series_long = '734 Male header (for PCBs); Straight solder pin 1 x 1 mm'
manufacturer = 'Wago'
orientation = 'V'
number_of_rows = 1
datasheet = 'http://www.farnell.com/datasheets/2157639.pdf'

pinrange= [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 18, 20, 24]


# Connector voltage ratings:
# Rated voltage  (III / 3) [V]           160 V
# Rated impulse voltage (III / 3) [kV]   2.5 kV

# Rated voltage (III/2) [V]              160 V
# Rated impulse voltage (III / 2) [kV]   2.5 kV

# Rated voltage (II / 2) [V]             320 V
# Rated impulse voltage (II / 2) [kV]    2.5 kV

# VDE 0110-1/4.97 2.5kV -> 1.5mm clearance
pad_to_pad_clearance = 1.5

pitch = 3.5
drill = 1.6 # square pins:1mm -> touching circle: √(2)mm ~ 1.4mm -> minimum drill accourding to KLC: 1.6mm

start_pos_x = 0
max_annular_ring = 0.5
min_annular_ring = 0.15

pad_size = [pitch - pad_to_pad_clearance, drill + 2*max_annular_ring]
if pad_size[0] - drill < 2*min_annular_ring:
    pad_size[0] = drill + 2*min_annular_ring
if pad_size[0] - drill > 2*max_annular_ring:
    pad_size[0] = drill + 2*max_annular_ring

pad_shape=Pad.SHAPE_OVAL
if pad_size[1] == pad_size[0]:
    pad_shape=Pad.SHAPE_CIRCLE

mpn_format = '734-1{n_plus_30:02d}'

def generate_one_footprint(pincount, configuration):

    mpn = mpn_format.format(n_plus_30=pincount+30)

    # handle arguments
    orientation_str = configuration['orientation_options'][orientation]
    footprint_name = configuration['fp_name_format_string'].format(man=manufacturer,
        series=series,
        mpn=mpn, num_rows=number_of_rows, pins_per_row=pincount, mounting_pad = "",
        pitch=pitch, orientation=orientation_str)

    footprint_name = footprint_name.replace("__", '_')

    kicad_mod = Footprint(footprint_name)
    descr_format_str = "Molex {:s}, {:s} , {:d} Pins ({:s}), generated with kicad-footprint-generator"
    kicad_mod.setDescription(descr_format_str.format(series_long, mpn, pincount, datasheet))
    kicad_mod.setTags(configuration['keyword_fp_string'].format(series=series,
        orientation=orientation_str, man=manufacturer,
        entry=configuration['entry_direction'][orientation]))

    # calculate working values
    end_pos_x = (pincount-1) * pitch
    centre_x = (end_pos_x - start_pos_x) / 2.0
    nudge = configuration['silk_fab_offset']
    silk_w = configuration['silk_line_width']
    fab_w = configuration['fab_line_width']


    body_edge={
        'left':start_pos_x - 2.8,
        'right':end_pos_x + 3.1,
        'bottom':4.35
        }
    body_edge['top'] = body_edge['bottom']-8.5

    # create pads
    optional_pad_params = {}
    if configuration['kicad4_compatible']:
        optional_pad_params['tht_pad1_shape'] = Pad.SHAPE_RECT
    else:
        optional_pad_params['tht_pad1_shape'] = Pad.SHAPE_ROUNDRECT

    kicad_mod.append(PadArray(initial=1, start=[start_pos_x, 0],
        x_spacing=pitch, pincount=pincount,
        size=pad_size, drill=drill,
        type=Pad.TYPE_THT, shape=Pad.SHAPE_OVAL, layers=Pad.LAYERS_THT,
        **optional_pad_params))

    # create fab outline
    kicad_mod.append(RectLine(start=[body_edge['left'], body_edge['top']],\
        end=[body_edge['right'], body_edge['bottom']], layer='F.Fab', width=fab_w))

    # create silkscreen
    kicad_mod.append(RectLine(start=[body_edge['left']-nudge, body_edge['top']-nudge],\
        end=[body_edge['right']+nudge, body_edge['bottom']+nudge], layer='F.SilkS', width=silk_w))

    # Inner silk:
    T = 0.5
    w1 = body_edge['right'] - end_pos_x - T
    y1 = body_edge['top'] + 1.5
    y2 = body_edge['bottom'] - 1.5
    y3 = body_edge['bottom'] - T
    x1 = body_edge['left'] + T
    x2 = start_pos_x
    x3 = x2 + w1
    x4 = end_pos_x
    x5 = x4 + w1

    poly_inside = [
        {'x': x1, 'y':y1},
        {'x': x1, 'y':y2},
        {'x': x2, 'y':y2},
        {'x': x2, 'y':y3},
        {'x': x3, 'y':y3},
        {'x': x3, 'y':y2},
        {'x': x4, 'y':y2},
        {'x': x4, 'y':y3},
        {'x': x5, 'y':y3},
        {'x': x5, 'y':y1},
        {'x': x1, 'y':y1}
    ]

    kicad_mod.append(PolygoneLine(polygone=poly_inside, layer='F.SilkS', width=silk_w))

    p1s_off = configuration['silk_fab_offset'] + 0.3
    p1s_L = 2
    # pin 1 markers
    kicad_mod.append(PolygoneLine(
        polygone=[
            {'x': body_edge['left'] - p1s_off, 'y': body_edge['top'] + p1s_L},
            {'x': body_edge['left'] - p1s_off, 'y': body_edge['top'] - p1s_off},
            {'x': body_edge['left'] + p1s_L, 'y': body_edge['top'] - p1s_off}
        ],
        layer='F.SilkS', width=silk_w))

    sl = 1
    poly_pin1_marker = [
        {'y': body_edge['top'], 'x': -sl/2},
        {'y': body_edge['top'] + sl/sqrt(2), 'x': 0},
        {'y': body_edge['top'], 'x': sl/2}
    ]
    kicad_mod.append(PolygoneLine(polygone=poly_pin1_marker, layer='F.Fab', width=fab_w))

    ########################### CrtYd #################################
    cx1 = roundToBase(body_edge['left']-configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])
    cy1 = roundToBase(body_edge['top']-configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])

    cx2 = roundToBase(body_edge['right']+configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])
    cy2 = roundToBase(body_edge['bottom']+configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])

    kicad_mod.append(RectLine(
        start=[cx1, cy1], end=[cx2, cy2],
        layer='F.CrtYd', width=configuration['courtyard_line_width']))

    ######################### Text Fields ###############################
    addTextFields(kicad_mod=kicad_mod, configuration=configuration, body_edges=body_edge,
        courtyard={'top':cy1, 'bottom':cy2}, fp_name=footprint_name, text_y_inside_position='bottom')

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

    for pincount in pinrange:
        generate_one_footprint(pincount, configuration)
