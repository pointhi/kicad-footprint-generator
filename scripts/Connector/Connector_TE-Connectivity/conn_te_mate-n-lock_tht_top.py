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

draw_inner_details = False

series = "MATE-N-LOK"
series_long = 'Mini-Universal MATE-N-LOK'
man_lib = 'TE-Connectivity'
man_short_fp_name = 'TE'
orientation = 'V'
datasheet = "http://www.te.com/commerce/DocumentDelivery/DDEController?Action=srchrtrv&DocNm=82181_SOFTSHELL_HIGH_DENSITY&DocType=CS&DocLang=EN"

#Molex part number
#n = number of circuits per row
variant_params = {
    'in_line':{
        'pins_per_row_range': [2,3],
        'number_of_rows': 1,
        'style': 'in_line',
        'number_pegs': 1,
        'width': 5.58,
        'part_code': {
                2: '1-770866-x',
                3: '1-770870-x'
            }
        },
    'dual1':{
        'pins_per_row_range': range(2,7),
        'number_of_rows': 2,
        'style': 'dual_row',
        'number_pegs': 1,
        'width': 9.83,
        'part_code': {
                4: '1-770874-x',
                6: '1-770875-x',
                8: '1-794073-x',
                10: '1-770858-x',
                12: '1-770621-x'
            }
        },
    'dual2':{
        'pins_per_row_range': range(7,13),
        'number_of_rows': 2,
        'style': 'dual_row',
        'number_pegs': 2,
        'width': 9.83,
        'part_code': {
                14: '1-794067-x',
                16: '1-794068-x',
                18: '1-794069-x',
                20: '1-794070-x',
                22: '1-794071-x',
                24: '1-794072-x'
            }
        },
    'matrix':{
        'pins_per_row_range': [3,4,5],
        'number_of_rows': 3,
        'style': 'matrix',
        'number_pegs': 1,
        'width': 13.97,
        'part_code': {
                9: '1-770182-x',
                12: '1-770186-x',
                15: '1-770190-x'
            }
        },
}

pitch = 4.14
drill = 1.4
pad_to_pad_clearance = 1.5
max_annular_ring = 0.95
min_annular_ring = 0.15
row = 4.14

peg_drill = 3.18
peg_to_nearest_pin = 4.44


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

    peg_pos = [[0, -peg_to_nearest_pin if variant_param['style'] != 'in_line' else (first_to_last_pad_y + peg_to_nearest_pin)]]
    if variant_param['number_pegs'] == 2:
        peg_pos.append([0, first_to_last_pad_y + peg_to_nearest_pin])

    mpn = variant_param['part_code'][pins_per_row*number_of_rows].format(n=pins_per_row*2)

    orientation_str = configuration['orientation_options'][orientation]
    footprint_name = configuration['fp_name_format_string'].format(man=man_short_fp_name,
        series=series,
        mpn=mpn, num_rows=number_of_rows, pins_per_row=pins_per_row,
        pitch=pitch, orientation=orientation_str)

    kicad_mod = Footprint(footprint_name)
    descr_format_str = "Molex {:s}, old mpn/engineering number: {:s}, {:d} Pins per row ({:s}), generated with kicad-footprint-generator"
    kicad_mod.setDescription(descr_format_str.format(
        series_long, mpn, pins_per_row, datasheet))
    tags = configuration['keyword_fp_string'].format(series=series,
        orientation=orientation_str, man=man_short_fp_name,
        entry=configuration['entry_direction'][orientation])
    kicad_mod.setTags(tags)

    x1 = -(variant_param['width']-first_to_last_pad_x)/2
    x2 = x1 + variant_param['width']
    body_lenght = (9.83-pitch)+first_to_last_pad_y
    y1 = -(body_lenght - first_to_last_pad_y)/2
    y2 = y1 + body_lenght

    peg_predrusion = 2.591 # from 3d model
    peg_d = 3.94 # from 3d model, rounded
    peg_from_body = 0.66 # from 3d model
    peg_conn_w = 1.6 # from 3d model, rounded
    TW = 3 # from 3d model, rounded
    TL = 1.3 # from 3d model, rounded
    BW = 1.14 # from 3d model, rounded
    BL = 0.76 # from 3d model, rounded

    #calculate fp dimensions
    body_edge={
        'left':x1,
        'right':x2,
        'bottom':y2,
        'top': y1
        }
    bounding_box = {}
    if variant_param['style'] != 'in_line':
        print(peg_pos)
        bounding_box['top'] = peg_pos[0][1]-peg_drill/2
        bounding_box['left'] = body_edge['left'] - TL
        bounding_box['right'] = body_edge['right'] + BL
        if variant_param['number_pegs'] == 2:
            bounding_box['bottom'] = peg_pos[1][1]+peg_drill/2
        else:
            bounding_box['bottom'] = body_edge['bottom'] + peg_predrusion
    else:
        bounding_box['bottom'] = peg_pos[0][1]+peg_drill/2
        bounding_box['top'] = body_edge['top'] - TL
        bounding_box['left'] = body_edge['left'] - BL
        bounding_box['right'] = body_edge['right']


    off = configuration['silk_fab_offset']


    #generate the pads
    for row_idx in range(variant_param['number_of_rows']):
        initial = row_idx*pins_per_row + 1
        kicad_mod.append(PadArray(pincount=pins_per_row, initial=initial, start=[row_idx*row, 0],
            y_spacing=pitch, type=Pad.TYPE_THT, shape=pad_shape,
            size=pad_size, drill=drill, layers=Pad.LAYERS_THT))

    for peg in peg_pos:
        kicad_mod.append(Pad(at=peg, type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
            size=peg_drill, drill=peg_drill, layers=Pad.LAYERS_NPTH))

    #add PCB locators if needed
    # pad_silk_offset = configuration['silk_pad_clearance']+configuration['silk_line_width']/2
    # if peg:
    #     loc = 3.00
    #     mounting_pin_y = row - 0.46
    #     lx1 = B/2-C/2
    #     lx2 = B/2+C/2
    #     kicad_mod.append(Pad(at=[lx1, mounting_pin_y],type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE, size=loc,drill=loc, layers=Pad.LAYERS_NPTH))
    #     kicad_mod.append(Pad(at=[lx2, mounting_pin_y],type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE, size=loc,drill=loc, layers=Pad.LAYERS_NPTH))
    #
    #     bounding_box['left'] = lx1-loc/2
    #     bounding_box['right'] = lx2+loc/2
    #     ######################## Fab ############################
    #     mount_pin_radius = loc/2
    #
    #     kicad_mod.append(Arc(center=[lx1,mounting_pin_y],
    #         start=[lx1,mounting_pin_y+mount_pin_radius], angle=180,
    #         layer='F.Fab', width=configuration['fab_line_width']))
    #
    #     kicad_mod.append(Line(start=[lx1,mounting_pin_y-mount_pin_radius],
    #         end=[x1,mounting_pin_y-mount_pin_radius],
    #         layer='F.Fab', width=configuration['fab_line_width']))
    #     kicad_mod.append(Line(start=[lx1,mounting_pin_y+mount_pin_radius],
    #         end=[x1,mounting_pin_y+mount_pin_radius],
    #         layer='F.Fab', width=configuration['fab_line_width']))
    #
    #
    #     kicad_mod.append(Arc(center=[lx2,mounting_pin_y],
    #         start=[lx2,mounting_pin_y-mount_pin_radius], angle=180,
    #         layer='F.Fab', width=configuration['fab_line_width']))
    #
    #     kicad_mod.append(Line(start=[lx2,mounting_pin_y-mount_pin_radius],
    #         end=[x2,mounting_pin_y-mount_pin_radius],
    #         layer='F.Fab', width=configuration['fab_line_width']))
    #     kicad_mod.append(Line(start=[lx2,mounting_pin_y+mount_pin_radius],
    #         end=[x2,mounting_pin_y+mount_pin_radius],
    #         layer='F.Fab', width=configuration['fab_line_width']))
    #
    #     ######################## Silk ############################
    #     mount_pin_radius = loc/2 + silk_pad_off
    #     kicad_mod.append(Arc(center=[lx1,mounting_pin_y],
    #         start=[lx1,mounting_pin_y+mount_pin_radius], angle=180,
    #         layer='F.SilkS', width=configuration['silk_line_width']))
    #
    #     kicad_mod.append(Line(start=[lx1,mounting_pin_y-mount_pin_radius],
    #         end=[x1-off,mounting_pin_y-mount_pin_radius],
    #         layer='F.SilkS', width=configuration['silk_line_width']))
    #     kicad_mod.append(Line(start=[lx1,mounting_pin_y+mount_pin_radius],
    #         end=[x1-off,mounting_pin_y+mount_pin_radius],
    #         layer='F.SilkS', width=configuration['silk_line_width']))
    #
    #
    #     kicad_mod.append(Arc(center=[lx2,mounting_pin_y],
    #         start=[lx2,mounting_pin_y-mount_pin_radius], angle=180,
    #         layer='F.SilkS', width=configuration['silk_line_width']))
    #
    #     kicad_mod.append(Line(start=[lx2,mounting_pin_y-mount_pin_radius],
    #         end=[x2+off,mounting_pin_y-mount_pin_radius],
    #         layer='F.SilkS', width=configuration['silk_line_width']))
    #     kicad_mod.append(Line(start=[lx2,mounting_pin_y+mount_pin_radius],
    #         end=[x2+off,mounting_pin_y+mount_pin_radius],
    #         layer='F.SilkS', width=configuration['silk_line_width']))
    #
    #draw the outline of the shape
    kicad_mod.append(RectLine(start=[x1,y1],end=[x2,y2],layer='F.Fab',width=configuration['fab_line_width']))
    #
    # #draw the outline of the tab
    # kicad_mod.append(PolygoneLine(polygone=[
    #     {'x': B/2 - tab_l/2,'y': y2},
    #     {'x': B/2 - tab_l/2,'y': y2 + tab_w},
    #     {'x': B/2 + tab_l/2,'y': y2 + tab_w},
    #     {'x': B/2 + tab_l/2,'y': y2},
    # ], layer='F.Fab', width=configuration['fab_line_width']))
    #
    # #draw the outline of each pin slot (alternating shapes)
    # #slot size
    # S = 3.3
    #
    # def square_slot(x,y):
    #     kicad_mod.append(RectLine(start=[x-S/2,y-S/2], end=[x+S/2,y+S/2],
    #         layer='F.Fab', width=configuration['fab_line_width']))
    #
    # def notch_slot(x,y):
    #     kicad_mod.append(PolygoneLine(polygone=[
    #     {'x': x-S/2, 'y': y+S/2},
    #     {'x': x-S/2, 'y': y-S/4},
    #     {'x': x-S/4, 'y': y-S/2},
    #     {'x': x+S/4, 'y': y-S/2},
    #     {'x': x+S/2, 'y': y-S/4},
    #     {'x': x+S/2, 'y': y+S/2},
    #     {'x': x-S/2, 'y': y+S/2},
    #     ], layer='F.Fab', width=configuration['fab_line_width']))
    #
    # q = 1
    # notch = True
    # for i in range(pins_per_row):
    #     if notch:
    #         y_square = row/2 - 4.2/2
    #         y_notch = row/2 + 4.2/2
    #     else:
    #         y_square = row/2 + 4.2/2
    #         y_notch = row/2 - 4.2/2
    #
    #     square_slot(i * pitch, y_square)
    #     notch_slot(i*pitch, y_notch)
    #
    #     q -= 1
    #
    #     if (q == 0):
    #         q = 2
    #         notch = not notch
    #
    #
    # #draw the outline of the connector on the silkscreen
    # outline = [
    # {'x': B/2,'y': y1-off},
    # {'x': x1-off,'y': y1-off},
    # {'x': x1-off,'y': y2+off},
    # {'x': B/2 - tab_l/2 - off,'y': y2+off},
    # {'x': B/2 - tab_l/2 - off,'y': y2 + off + tab_w},
    # {'x': B/2, 'y': y2 + off + tab_w},
    # ]
    #
    # kicad_mod.append(PolygoneLine(polygone=outline, layer="F.SilkS", width=configuration['silk_line_width']))
    # kicad_mod.append(PolygoneLine(polygone=outline, x_mirror=B/2 if B/2 != 0 else 0.00000001, layer="F.SilkS", width=configuration['silk_line_width']))
    #
    # #pin-1 marker
    #
    # L = 2.5
    # O = 0.35
    #
    # pin = [
    #     {'x': x1 + L,'y': y1 - O},
    #     {'x': x1 - O,'y': y1 - O},
    #     {'x': x1 - O,'y': y1 + L},
    # ]
    #
    # kicad_mod.append(PolygoneLine(polygone=pin, layer="F.SilkS", width=configuration['silk_line_width']))
    # kicad_mod.append(PolygoneLine(polygone=pin, width=configuration['fab_line_width'], layer='F.Fab'))

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
    args = parser.parse_args()

    with open(args.global_config, 'r') as config_stream:
        try:
            configuration = yaml.load(config_stream)
        except yaml.YAMLError as exc:
            print(exc)

    with open(args.series_config, 'r') as config_stream:
        try:
            configuration.update(yaml.load(config_stream))
        except yaml.YAMLError as exc:
            print(exc)

    for variant in variant_params:
        variant_param = variant_params[variant]

        for pins_per_row in variant_param['pins_per_row_range']:
            generate_one_footprint(pins_per_row, variant_param, configuration)
