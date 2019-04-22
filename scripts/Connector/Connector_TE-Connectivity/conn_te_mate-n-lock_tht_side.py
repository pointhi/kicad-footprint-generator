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
from math import sqrt, asin, degrees
import argparse
import yaml
from helpers import *
from KicadModTree import *

sys.path.append(os.path.join(sys.path[0], "..", "..", "tools"))  # load parent path of tools
from footprint_text_fields import addTextFields

draw_inner_details = False

series = "MATE-N-LOK"
series_long = 'Mini-Universal MATE-N-LOK'
man_lib = 'TE-Connectivity'
man_short_fp_name = 'TE'
orientation = 'H'
datasheet = "http://www.te.com/commerce/DocumentDelivery/DDEController?Action=srchrtrv&DocNm=82181_SOFTSHELL_HIGH_DENSITY&DocType=CS&DocLang=EN"

#Molex part number
#n = number of circuits per row
variant_params = {
    'in_line':{
        'pins_per_row_range': [1,2,3],
        'number_of_rows': 1,
        'style': 'in_line',
        'number_pegs': 1,
        'peg_from_center': 0,
        'part_code': {
                1: '1-794374-x',
                2: '1-770966-x',
                3: '1-770967-x'
            }
        },
    'dual1':{
        'pins_per_row_range': range(2,7),
        'number_of_rows': 2,
        'style': 'dual_row',
        'number_pegs': 1,
        'peg_from_center': 0,
        'part_code': {
                4: '1-770968-x',
                6: '1-770969-x',
                8: '1-770970-x',
                10: '1-770971-x',
                12: '1-770972-x'
            }
        },
    'dual2':{
        'pins_per_row_range': [7,9],
        'number_of_rows': 2,
        'style': 'dual_row',
        'number_pegs': 2,
        'peg_from_center': 8.28,
        'part_code': {
                14: '1-770973-x',
                18: '1-794105-x'
            }
        },
    'dual3':{
        'pins_per_row_range': [8,10,12],
        'number_of_rows': 2,
        'style': 'dual_row',
        'number_pegs': 2,
        'peg_from_center': 10.38,
        'part_code': {
                16: '1-770974-x',
                20: '1-794106-x',
                24: '1-794108-x'
            }
        },
    'dual4':{
        'pins_per_row_range': [11],
        'number_of_rows': 2,
        'style': 'dual_row',
        'number_pegs': 2,
        'peg_from_center': 12.42,
        'part_code': {
                22: '1-794107-x'
            }
        },
}

pitch = 4.14
drill = 1.4
pad_to_pad_clearance = 1.5
max_annular_ring = 0.95
min_annular_ring = 0.15
row = 4.14

peg_drill = 3.86
peg_to_nearest_pin = 7.34
width = 12.7

peg_to_body_right = 6.86

def generate_one_footprint(pins_per_row, variant_param, configuration):
    silk_pad_off = configuration['silk_pad_clearance']+configuration['silk_line_width']/2
    off = configuration['silk_fab_offset']

    number_of_rows = variant_param['number_of_rows']

    pad_size = [row - pad_to_pad_clearance, pitch - pad_to_pad_clearance]
    if number_of_rows == 1:
        pad_size[0] = drill + 2*max_annular_ring

    if pad_size[0] - drill < 2*min_annular_ring:
        pad_size[0] = drill + 2*min_annular_ring
    if pad_size[0] - drill > 2*max_annular_ring:
        pad_size[0] = drill + 2*max_annular_ring

    if pad_size[1] - drill < 2*min_annular_ring:
        pad_size[1] = drill + 2*min_annular_ring
    if pad_size[1] - drill > 2*max_annular_ring:
        pad_size[1] = drill + 2*max_annular_ring

    pad_shape = Pad.SHAPE_OVAL
    if pad_size[0] == pad_size[1]:
        pad_shape = Pad.SHAPE_CIRCLE

    first_to_last_pad_y = (pins_per_row-1)*pitch
    first_to_last_pad_x = (number_of_rows-1)*row

    center_y = first_to_last_pad_y/2
    peg_x = (number_of_rows-1)*row + peg_to_nearest_pin
    peg_pos = [[peg_x, center_y + variant_param['peg_from_center']]]
    if variant_param['number_pegs'] == 2:
        peg_pos.append([peg_x, center_y - variant_param['peg_from_center']])

    mpn = variant_param['part_code'][pins_per_row*number_of_rows].format(n=pins_per_row*2)

    orientation_str = configuration['orientation_options'][orientation]
    footprint_name = configuration['fp_name_format_string'].format(man=man_short_fp_name,
        series=series,
        mpn=mpn, num_rows=number_of_rows, pins_per_row=pins_per_row, mounting_pad = "",
        pitch=pitch, orientation=orientation_str)

    kicad_mod = Footprint(footprint_name)
    descr_format_str = "Molex {:s}, old mpn/engineering number: {:s}, {:d} Pins per row ({:s}), generated with kicad-footprint-generator"
    kicad_mod.setDescription(descr_format_str.format(
        series_long, mpn, pins_per_row, datasheet))
    tags = configuration['keyword_fp_string'].format(series=series,
        orientation=orientation_str, man=man_short_fp_name,
        entry=configuration['entry_direction'][orientation])
    kicad_mod.setTags(tags)


    x2 = peg_x + peg_to_body_right
    x1 = x2 - width
    body_lenght = 5.72+first_to_last_pad_y
    y1 = -(body_lenght - first_to_last_pad_y)/2
    y2 = y1 + body_lenght

    #calculate fp dimensions
    body_edge={
        'left':x1,
        'right':x2,
        'bottom':y2,
        'top': y1
        }
    bounding_box = body_edge.copy()
    bounding_box['left'] = -pad_size[0]/2


    #generate the pads
    optional_pad_params = {}
    if configuration['kicad4_compatible']:
        optional_pad_params['tht_pad1_shape'] = Pad.SHAPE_RECT
    else:
        optional_pad_params['tht_pad1_shape'] = Pad.SHAPE_ROUNDRECT

    for row_idx in range(number_of_rows):
        initial = row_idx*pins_per_row + 1
        kicad_mod.append(PadArray(
            pincount=pins_per_row, initial=initial, start=[row_idx*row, 0],
            y_spacing=pitch, type=Pad.TYPE_THT, shape=pad_shape,
            size=pad_size, drill=drill, layers=Pad.LAYERS_THT,
            **optional_pad_params))

    for peg in peg_pos:
        kicad_mod.append(Pad(at=peg, type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
            size=peg_drill, drill=peg_drill, layers=Pad.LAYERS_NPTH))


    #draw the outline of the shape
    kicad_mod.append(RectLine(start=[x1,y1],end=[x2,y2],
        layer='F.Fab',width=configuration['fab_line_width']))

    dx = body_edge['left'] - off - (number_of_rows-1)*row - (pad_size[0] - pad_size[1])/2

    if dx < (pad_size[1]/2 + silk_pad_off):
        dy = sqrt((pad_size[1]/2 + silk_pad_off)**2-dx**2)
    else:
        dy = 0

    dy_rect = pad_size[1]/2 + silk_pad_off

    top_silk_pad = -dy if number_of_rows == 2 else -dy_rect
    bottom_silk_pad = (first_to_last_pad_y + dy) if pins_per_row > 1 else dy_rect

    silk_poly = [
        {'x': body_edge['left']-off,'y': top_silk_pad},
        {'x': body_edge['left']-off,'y': body_edge['top']-off},
        {'x': body_edge['right']+off,'y': body_edge['top']-off},
        {'x': body_edge['right']+off,'y': body_edge['bottom']+off},
        {'x': body_edge['left']-off,'y': body_edge['bottom']+off},
        {'x': body_edge['left']-off,'y': bottom_silk_pad},
    ]
    kicad_mod.append(PolygoneLine(polygone=silk_poly,
        layer='F.SilkS', width=configuration['silk_line_width']))

    for i in range(pins_per_row-1):
        yt = i*pitch + (dy if number_of_rows == 2 or i > 1 else dy_rect)
        yb = (i+1)*pitch - dy
        kicad_mod.append(Line(
            start=[body_edge['left']-off, yt], end=[body_edge['left']-off, yb],
            layer='F.SilkS', width=configuration['silk_line_width']))

    O = silk_pad_off + 0.2

    pin = [
        {'x': 0,'y': -pad_size[1]/2 - O},
        {'x': -pad_size[0]/2 - O,'y': -pad_size[1]/2 - O},
        {'x': -pad_size[0]/2 - O,'y': 0},
    ]

    kicad_mod.append(PolygoneLine(polygone=pin,
        layer="F.SilkS", width=configuration['silk_line_width']))
    kicad_mod.append(PolygoneLine(polygone=pin,
        width=configuration['fab_line_width'], layer='F.Fab'))

    ########################### CrtYd #################################
    CrtYd_offset = configuration['courtyard_offset']['connector']
    CrtYd_grid = configuration['courtyard_grid']

    cx1 = roundToBase(bounding_box['left'] - CrtYd_offset, CrtYd_grid)
    cy1 = roundToBase(bounding_box['top'] - CrtYd_offset, CrtYd_grid)

    cx2 = roundToBase(bounding_box['right'] + CrtYd_offset, CrtYd_grid)
    cy2 = roundToBase(bounding_box['bottom'] + CrtYd_offset, CrtYd_grid)

    kicad_mod.append(RectLine(
        start=[cx1, cy1], end=[cx2, cy2],
        layer='F.CrtYd', width=configuration['courtyard_line_width']))

    ######################### Text Fields ###############################
    addTextFields(kicad_mod=kicad_mod, configuration=configuration, body_edges=body_edge,
        courtyard={'top':cy1, 'bottom':cy2}, fp_name=footprint_name, text_y_inside_position='right')

    ##################### Output and 3d model ############################
    model3d_path_prefix = configuration.get('3d_model_prefix','${KISYS3DMOD}/')

    lib_name = configuration['lib_name_format_string'].format(series=series, man=man_lib)
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
        variant_param = variant_params[variant]

        for pins_per_row in variant_param['pins_per_row_range']:
            generate_one_footprint(pins_per_row, variant_param, configuration)
