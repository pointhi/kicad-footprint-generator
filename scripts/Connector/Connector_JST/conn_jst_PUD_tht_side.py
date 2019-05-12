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
from math import sqrt

sys.path.append(os.path.join(sys.path[0], "..", "..", "tools"))  # load parent path of tools
from footprint_text_fields import addTextFields

series = "PUD"
manufacturer = 'JST'
orientation = 'H'
number_of_rows = 2
datasheet = 'http://www.jst-mfg.com/product/pdf/eng/ePUD.pdf'

pitch = 2.0
row_pitch = 2
drill = 0.75 # 0.7 +0.1/-0 -> 0.75+/-0.05
pad_to_pad_clearance = 0.8
pad_copper_y_solder_length = 0.5 #How much copper should be in y direction?
min_annular_ring = 0.15

mh_drill = 1.65
mh_y = row_pitch + 7.7

pin_range = range(4,21) #number of pins in each row

#FP name strings
part_base = "S{n:02}B-PUDSS-1" #JST part number format string

#FP description and tags

def generate_one_footprint(pins, configuration):
    mpn = part_base.format(n=pins*number_of_rows) #JST part number format string
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
    B = A + 4

    #generate the pads (row 1)
    size = [pitch - pad_to_pad_clearance, row_pitch - pad_to_pad_clearance]
    if size[0] - drill < 2*min_annular_ring:
        size[0] = drill + 2*min_annular_ring
    if size[0] - drill > 2*pad_copper_y_solder_length:
        size[0] = drill + 2*pad_copper_y_solder_length

    if size[1] - drill < 2*min_annular_ring:
        size[1] = drill + 2*min_annular_ring
    if size[1] - drill > 2*pad_copper_y_solder_length:
        size[1] = drill + 2*pad_copper_y_solder_length

    if size[0] == size[1]:
        pad_shape = Pad.SHAPE_CIRCLE
    else:
        pad_shape = Pad.SHAPE_OVAL

    optional_pad_params = {}
    if configuration['kicad4_compatible']:
        optional_pad_params['tht_pad1_shape'] = Pad.SHAPE_RECT
    else:
        optional_pad_params['tht_pad1_shape'] = Pad.SHAPE_ROUNDRECT

    for row_idx in range(2):
        kicad_mod.append(PadArray(
            pincount=pins, x_spacing=pitch,
            type=Pad.TYPE_THT, shape=pad_shape,
            start=[0, row_idx*row_pitch], initial=row_idx+1, increment=2,
            size=size, drill=drill, layers=Pad.LAYERS_THT,
            **optional_pad_params))

    #draw the component outline
    x1 = A/2 - B/2
    x2 = x1 + B
    y2 = row_pitch + 7.7 + 2.4
    y1 = y2 - 12.7
    body_edge={'left':x1, 'right':x2, 'top':y1, 'bottom':y2}

    #draw simple outline on F.Fab layer
    kicad_mod.append(RectLine(start=[x1,y1],end=[x2,y2],layer='F.Fab',width=configuration['fab_line_width']))
    ########################### CrtYd #################################
    cx1 = roundToBase(x1-configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])
    if y1 < -size[1]/2:
        cy1 = roundToBase(y1-configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])
    else:
        cy1 = roundToBase(-size[1]/2-configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])


    cx2 = roundToBase(x2+configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])
    cy2 = roundToBase(y2+configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])

    kicad_mod.append(RectLine(
        start=[cx1, cy1], end=[cx2, cy2],
        layer='F.CrtYd', width=configuration['courtyard_line_width']))

    #offset off
    off = configuration['silk_fab_offset']

    x1 -= off
    y1 -= off
    x2 += off
    y2 += off

    #outline
    side = [
    {'x': -1,'y': y1},
    {'x': x1,'y': y1},
    {'x': x1,'y': y2},
    {'x': A/2,'y': y2},
    ]

    kicad_mod.append(PolygoneLine(polygone=side, width=configuration['silk_line_width'], layer='F.SilkS'))
    kicad_mod.append(PolygoneLine(polygone=side, x_mirror=A/2, width=configuration['silk_line_width'], layer='F.SilkS'))

    #add mounting holes
    m1 = Pad(at=[-0.9,mh_y],layers=Pad.LAYERS_NPTH,shape=Pad.SHAPE_CIRCLE,type=Pad.TYPE_NPTH,size=mh_drill, drill=mh_drill)
    m2 = Pad(at=[A+0.9,mh_y],layers=Pad.LAYERS_NPTH,shape=Pad.SHAPE_CIRCLE,type=Pad.TYPE_NPTH,size=mh_drill, drill=mh_drill)

    kicad_mod.append(m1)
    kicad_mod.append(m2)

    D = 0.3
    L = 2.5

    #add p1 marker
    marker = [
        {'x': pitch/2 , 'y': y1-D+0.25},
        {'x': pitch/2 , 'y': y1-D},
        {'x': x1-D,'y': y1-D},
        {'x': x1-D,'y': y1-D+L}
    ]

    kicad_mod.append(PolygoneLine(polygone=marker,width=configuration['silk_line_width'],layer='F.SilkS'))
    sl = 1
    marker =[
        {'x': sl/2 , 'y': body_edge['top']},
        {'x': 0 , 'y': body_edge['top']+sl/sqrt(2)},
        {'x': -sl/2 , 'y': body_edge['top']}
    ]
    kicad_mod.append(PolygoneLine(polygone=marker,layer='F.Fab',width=configuration['fab_line_width']))

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
