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

draw_inner_details = False

series = "826576"
manufacturer = 'TE'
manufacturer_lib = 'TE-Connectivity'
orientation = 'V'
datasheet = 'https://www.te.com/commerce/DocumentDelivery/DDEController?Action=srchrtrv&DocNm=826576&DocType=Customer+Drawing&DocLang=English'
number_of_rows = 1

# only generate active pin counts from TE rev 7 datasheet
#pins_per_row_range = range(1, 37)
pins_per_row_range = [2,3,5,6,7,8,9,13,15,16,17,18,20,36]

# the datasheet has an equation and a table (column 'L') for body length
# the equation of pincount * 3.96 = length is wrong
# the table is roughly correct based on part measurement
# table is nearly pincount * 3.96 - 0.589 but capture the table exactly
body_lengths = {1:3.3, 2:7.3, 3:11.3, 4:15.2, 5:19.2, 6:23.1, 7:27.1, 8:31.1, 9:35.1, 10:39,
                11:43, 12:46.9, 13:50.9, 14:54.8, 15:58.8, 16:62.8, 17:66.7, 18:70.7, 19:74.7, 20:78.6,
                21:82.6, 22:86.5, 23:90.5, 24:94.4, 25:98.4, 26:102.4, 27:106.3, 28:110.3, 29:114.2, 30:118.2,
                31:122.2, 32:126.1, 33:130.1, 34:134, 35:138, 36:141.6}

part_code = "{:s}{:s}826576-{:s}"

pitch = 3.96
drill = 1.4
start_pos_x = 0 # Where should pin 1 be located?
pad_size = [drill + 1, drill + 1]

pad_shape=Pad.SHAPE_OVAL
if pad_size[1] == pad_size[0]:
    pad_shape=Pad.SHAPE_CIRCLE


def generate_one_footprint(pins, configuration):
    mpn = part_code.format(str(pins)[:1] if pins > 9 else '', '-' if pins > 9 else '', str(pins)[-1])

    # handle arguments
    orientation_str = configuration['orientation_options'][orientation]
    footprint_name = configuration['fp_name_no_series_format_string'].format(man=manufacturer,
        mpn=mpn, num_rows=number_of_rows, pins_per_row=pins, mounting_pad = "",
        pitch=pitch, orientation=orientation_str)

    print(footprint_name)
    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription("{:s}, {:s}, {:d} Pins ({:s}), generated with kicad-footprint-generator".format(manufacturer,
        mpn, pins, datasheet))
    kicad_mod.setTags(configuration['keyword_fp_string'].format(series=series,
        orientation=orientation_str, man=manufacturer,
        entry=configuration['entry_direction'][orientation]))

    #calculate fp dimensions

    #B = distance between end-point pins
    B = (pins - 1) * pitch
    #A = total connector length
    A = body_lengths[pins]

    #corners
    x1 = -(A-B) / 2
    x2 = x1 + A

    body_width = 6.4
    y2 = body_width / 2
    y1 = y2 - body_width

    body_edge={
        'left':x1,
        'right':x2,
        'bottom':y2,
        'top': y1
        }
    bounding_box = body_edge.copy()

    out = [
    {'x': B/2, 'y': y1},
    {'x': x1, 'y': y1},
    {'x': x1, 'y': y2},
    {'x': B/2, 'y': y2},
    ]
    kicad_mod.append(PolygoneLine(polygone=out,
        layer="F.Fab", width=configuration['fab_line_width']))
    kicad_mod.append(PolygoneLine(polygone=out,x_mirror=B/2,
        layer="F.Fab", width=configuration['fab_line_width']))

    #offset
    o = configuration['silk_fab_offset']
    x1 -= o
    y1 -= o
    x2 += o
    y2 += o

    out = [
    {'x': B/2, 'y': y1},
    {'x': x1, 'y': y1},
    {'x': x1, 'y': y2},
    {'x': B/2, 'y': y2},
    ]
    kicad_mod.append(PolygoneLine(polygone=out,
        layer="F.SilkS", width=configuration['silk_line_width']))
    kicad_mod.append(PolygoneLine(polygone=out,x_mirror=B/2,
        layer="F.SilkS", width=configuration['silk_line_width']))

    optional_pad_params = {}
    if configuration['kicad4_compatible']:
        optional_pad_params['tht_pad1_shape'] = Pad.SHAPE_RECT
    else:
        optional_pad_params['tht_pad1_shape'] = Pad.SHAPE_ROUNDRECT

    #generate the pads
    kicad_mod.append(PadArray(
        pincount=pins, x_spacing=pitch, type=Pad.TYPE_THT,
        shape=pad_shape, size=pad_size, drill=drill, layers=Pad.LAYERS_THT,
        **optional_pad_params))

    #pin-1 marker
    pin_mark_width = 1
    pin_mark_height = 1
    pin_mask_offset = 0.5
    
    pin = [
        {'x': -pin_mark_width/2,'y': body_edge['bottom']},
        {'x': 0,'y': body_edge['bottom'] - pin_mark_height},
        {'x': pin_mark_width/2,'y': body_edge['bottom']},
    ]
    kicad_mod.append(PolygoneLine(polygone=pin,
        layer="F.Fab", width=configuration['fab_line_width']))

    pin = [
        {'x': -pin_mark_width/2,'y': body_edge['bottom'] + pin_mark_height + pin_mask_offset},
        {'x': 0,'y': body_edge['bottom'] + pin_mask_offset},
        {'x': pin_mark_width/2,'y': body_edge['bottom'] + pin_mark_height + pin_mask_offset},
        {'x': -pin_mark_width/2,'y': body_edge['bottom'] + pin_mark_height + pin_mask_offset}
    ]

    kicad_mod.append(PolygoneLine(polygone=pin,
        layer="F.SilkS", width=configuration['silk_line_width']))


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
        courtyard={'top':cy1, 'bottom':cy2}, fp_name=footprint_name, text_y_inside_position='top')

    ##################### Output and 3d model ############################
    model3d_path_prefix = configuration.get('3d_model_prefix','${KISYS3DMOD}/')

    lib_name = configuration['lib_name_format_string'].format(series=series, man=manufacturer_lib)
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

    for pins_per_row in pins_per_row_range:
        generate_one_footprint(pins_per_row, configuration)
