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

# export PYTHONPATH="${PYTHONPATH}<path to kicad-footprint-generator directory>"
sys.path.append(os.path.join(sys.path[0], "..", "..", ".."))  # load parent path of KicadModTree
import argparse
import yaml
from helpers import *
from KicadModTree import *

sys.path.append(os.path.join(sys.path[0], "..", "..", "tools"))  # load parent path of tools
from footprint_text_fields import addTextFields

series = "VH"
manufacturer = 'JST'
orientation = 'H'
number_of_rows = 1
datasheet = 'http://www.jst-mfg.com/product/pdf/eng/eVH.pdf'

pitch = 3.96
pad_to_pad_clearance = 0.8
pad_copper_y_solder_length = 0.5 #How much copper should be in y direction?
min_annular_ring = 0.15
drill = 1.7 # 1.65 +0.1/-0.0 -> 1.7 +/-0.05

pin_range = range(2, 11) #number of pins in each row

#FP name strings
part_base = "B{n}PS-VH" #JST part number format string


#FP description and tags

def generate_one_footprint(pins, configuration):
    mpn = part_base.format(n=pins)
    orientation_str = configuration['orientation_options'][orientation]
    footprint_name = configuration['fp_name_format_string'].format(man=manufacturer,
        series=series,
        mpn=mpn, num_rows=number_of_rows, pins_per_row=pins, mounting_pad = "",
        pitch=pitch, orientation=orientation_str)

    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription("JST {:s} series connector, {:s} ({:s}), generated with kicad-footprint-generator".format(series, mpn, datasheet))
    kicad_mod.setTags(configuration['keyword_fp_string'].format(series=series,
        orientation=orientation_str, man=manufacturer,
        entry=configuration['entry_direction'][orientation]))

    #calculate fp dimensions
    A = (pins - 1) * pitch
    B = A + 3.9

    #coordinate locations
    #    x1 x3                x4 x2
    #       1  2  3  4  5  6  7
    # y1  _______________________
    # y2 |_|                  |__|
    #      |                  |
    # y3   |__________________|
    # y4   || || || || || || ||

    #generate pads
    pad_size = [pitch - pad_to_pad_clearance, drill + 2*pad_copper_y_solder_length]
    if pad_size[0] - drill < 2*min_annular_ring:
        pad_size[0] = drill + 2*min_annular_ring
    if pad_size[0] - drill > 2*pad_copper_y_solder_length:
        pad_size[0] = drill + 2*pad_copper_y_solder_length

    shape=Pad.SHAPE_OVAL
    if pad_size[1] == pad_size[0]:
        shape=Pad.SHAPE_CIRCLE

    optional_pad_params = {}
    if configuration['kicad4_compatible']:
        optional_pad_params['tht_pad1_shape'] = Pad.SHAPE_RECT
    else:
        optional_pad_params['tht_pad1_shape'] = Pad.SHAPE_ROUNDRECT

    kicad_mod.append(PadArray(
        pincount=pins, x_spacing=pitch,
        type=Pad.TYPE_THT, shape=shape, size=pad_size,
        drill=drill, layers=Pad.LAYERS_THT,
        **optional_pad_params))

    #draw the component outline
    x1 = A/2 - B/2
    x2 = x1 + B
    x3 = -0.9
    x4 = pitch * (pins - 1) + 0.9
    y1 = 14.9 - 7.7 - 3.2
    y2 = y1 + 3.2
    y3 = y1 + 9.4
    y4 = 14.9
    body_edge={'left':x1, 'right':x2, 'top':y1, 'bottom':y4}

    #draw shroud outline on F.Fab layer
    kicad_mod.append(RectLine(start=[x3,y1],end=[x4,y3],layer='F.Fab',width=configuration['fab_line_width']))
    kicad_mod.append(PolygoneLine(polygone=[{'x':x4,'y':y1},{'x':x2,'y':y1},{'x':x2,'y':y2},{'x':x4,'y':y2}],
        layer='F.Fab',width=configuration['fab_line_width']))
    kicad_mod.append(PolygoneLine(polygone=[{'x':x3,'y':y2},{'x':x1,'y':y2},{'x':x1,'y':y1},{'x':x3,'y':y1}],
        layer='F.Fab',width=configuration['fab_line_width']))

    #draw pin1 mark on F.Fab
    kicad_mod.append(PolygoneLine(polygone=[{'x':-0.8,'y':y1},{'x':0,'y':y1+0.8},{'x':0.8,'y':y1}],
        layer='F.Fab',width=configuration['fab_line_width']))

    #draw pin outlines on F.Fab (pin width is 1.4mm, so 0.7mm is half the pin width)
    for pin in range(pins):
        kicad_mod.append(PolygoneLine(polygone=[{'x':pin * pitch - 0.7,'y':y1},
                                                {'x':pin * pitch - 0.7,'y':0},
                                                {'x':pin * pitch + 0.7,'y':0},
                                                {'x':pin * pitch + 0.7,'y':y1}],
                                            layer='F.Fab',width=configuration['fab_line_width']))
        kicad_mod.append(PolygoneLine(polygone=[{'x':pin * pitch - 0.7,'y':y3},
                                                {'x':pin * pitch - 0.7,'y':y4},
                                                {'x':pin * pitch + 0.7,'y':y4},
                                                {'x':pin * pitch + 0.7,'y':y3}],
                                            layer='F.Fab',width=configuration['fab_line_width']))

    ########################### CrtYd #################################
    cx1 = roundToBase(x1-configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])
    cy1 = roundToBase(-pad_size[1]/2-configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])

    cx2 = roundToBase(x2+configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])
    cy2 = roundToBase(y4+configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])

    kicad_mod.append(RectLine(
        start=[cx1, cy1], end=[cx2, cy2],
        layer='F.CrtYd', width=configuration['courtyard_line_width']))

    #draw silk outlines
    off = configuration['silk_fab_offset']
    x1 -= off
    y1 -= off
    x2 += off
    y2 += off
    x3 -= off
    y3 += off
    x4 += off
    y4 += off

    kicad_mod.append(PolygoneLine(polygone=[{'x':x1,'y':y1},
                                            {'x':x2,'y':y1},
                                            {'x':x2,'y':y2},
                                            {'x':x4,'y':y2},
                                            {'x':x4,'y':y3},
                                            {'x':x3,'y':y3},
                                            {'x':x3,'y':y2},
                                            {'x':x1,'y':y2},
                                            {'x':x1,'y':y1}],
                                        layer='F.SilkS', width=configuration['silk_line_width']))

    #pin silk (half of pin width is 0.7mm, so adding 0.12mm silk offset gives 0.82mm about pin center)
    for pin in range(pins):
        kicad_mod.append(PolygoneLine(polygone=[{'x':pin * pitch - 0.82,'y':y3},
                                                {'x':pin * pitch - 0.82,'y':y4},
                                                {'x':pin * pitch + 0.82,'y':y4},
                                                {'x':pin * pitch + 0.82,'y':y3}],
                                            layer='F.SilkS', width=configuration['silk_line_width']))

    #add pin1 marker on F.FilkS
    p1_y1 = -pad_size[1]/2 - configuration['silk_pad_clearance'] - configuration['silk_line_width']/2
    p1_x1 = -pad_size[0]/2 - configuration['silk_pad_clearance'] - configuration['silk_line_width']/2

    kicad_mod.append(PolygoneLine(polygone=[{'x':0,'y':p1_y1},{'x':p1_x1,'y':p1_y1},{'x':p1_x1,'y':0}],
            layer='F.SilkS', width=configuration['silk_line_width']))


    ######################### Text Fields ###############################
    addTextFields(kicad_mod=kicad_mod, configuration=configuration, body_edges=body_edge,
        courtyard={'top':cy1, 'bottom':cy2}, fp_name=footprint_name, text_y_inside_position='center')

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

    for pincount in pin_range:
        generate_one_footprint(pincount, configuration)
