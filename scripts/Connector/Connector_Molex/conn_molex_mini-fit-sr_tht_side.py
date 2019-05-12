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

series = "Mini-Fit_Sr"
series_long = 'Mini-Fit Sr. Power Connectors'
manufacturer = 'Molex'
orientation = 'H'
number_of_rows = 1
datasheet = 'http://www.molex.com/pdm_docs/sd/428202214_sd.pdf'

#pins_per_row per row
pins_per_row_range = [2, 3, 4, 5, 6]

#Molex part number
#n = number of circuits per row
part_code = "42820-{n}2XX"

pitch = 10
drill = 2.8

offset_second_pad = 5

pad_to_pad_clearance = 3
max_annular_ring = 1
min_annular_ring = 0.15

#locating pins
ret_dy = 5.73
ret_dx = 9.00 + offset_second_pad
ret_drill = 3.00
ret_size = 4.00



pad_size = [offset_second_pad + 0.1, pitch - pad_to_pad_clearance]
if pad_size[1] - drill < 2*min_annular_ring:
    pad_size[1] = drill + 2*min_annular_ring
if pad_size[1] - drill > 2*max_annular_ring:
    pad_size[1] = drill + 2*max_annular_ring

version_params = {
    'with_thermals':{
        'description': ', With thermal vias in pads',
        'fp_name_suffix': '_ThermalVias',
        'thermals': True
    },
    'only_pads':{
        'description': '',
        'fp_name_suffix': '',
        'thermals': False
    }
}



def generate_one_footprint(pins, params, configuration):
    pad_silk_off = configuration['silk_pad_clearance'] + configuration['silk_line_width']/2
    mpn = part_code.format(n=pins*number_of_rows)

    # handle arguments
    orientation_str = configuration['orientation_options'][orientation]
    footprint_name = configuration['fp_name_format_string'].format(man=manufacturer,
        series=series,
        mpn=mpn, num_rows=number_of_rows, pins_per_row=pins_per_row, mounting_pad = "",
        pitch=pitch, orientation=orientation_str)
    footprint_name += params['fp_name_suffix']

    kicad_mod = Footprint(footprint_name)
    desc_format_str = "Molex {:s}, {:s}{:s}, {:d} Pins per row ({:s}), generated with kicad-footprint-generator"
    kicad_mod.setDescription(desc_format_str.format(series_long, mpn, params['description'], pins, datasheet))
    kicad_mod.setTags(configuration['keyword_fp_string'].format(series=series,
        orientation=orientation_str, man=manufacturer,
        entry=configuration['entry_direction'][orientation]))



    # Dimensions
    P = (pins - 1) * pitch
    B = pins * pitch + 0.90 # connector length
    W = 21.00 # connector width

    tab_side_w = 1.46

    yt1 = 0 - (B - P) / 2 # left
    yt2 = yt1 - tab_side_w
    yb1 = P + (B - P) / 2 # right
    yb2 = yb1 + tab_side_w
    xr1 = ret_dx + 13.56 # bottom
    xl1 = xr1 - W # top
    xl2 = xl1 - 7.6

    body_edge={
        'left':xl1,
        'right':xr1,
        'bottom':yb1,
        'top': yt1
        }
    bounding_box = {
        'top': -(ret_dy + ret_size/2),
        'bottom': P + (ret_dy + ret_size/2),
        'left': -pad_size[0]/2,
        'right': body_edge['right']
    }

    ##################################  Pins ##################################
    for row_idx in range(2):
        kicad_mod.append(PadArray(pincount=pins, start=[row_idx*offset_second_pad, 0],
            y_spacing=pitch, size=pad_size, drill=drill,
            shape=Pad.SHAPE_RECT, type=Pad.TYPE_THT, layers=Pad.LAYERS_THT,
            tht_pad1_shape=Pad.SHAPE_RECT))

    d_small = 0.3
    s_small = d_small + 2*min_annular_ring
    thermal_to_pad_edge = s_small/2 + 0.15

    if params['thermals']:
        for yi in range(pins):
            n = yi + 1
            pad_center_x = offset_second_pad/2
            pad_center_y = yi*pitch
            pad_l = offset_second_pad + pad_size[0]
            dy = (pad_size[1] - 2*thermal_to_pad_edge)/2
            dx = (pad_l - 2*thermal_to_pad_edge)/4

            #draw rectangle on F.Fab layer

            # kicad_mod.append(RectLine(
            #     start=[pad_center_x - pad_l/2, pad_center_y - pad_size[1]/2],
            #     end=[pad_center_x + pad_l/2, pad_center_y + pad_size[1]/2],
            #     layer='F.Fab', width=configuration['fab_line_width']))

            kicad_mod.append(PadArray(center=[pad_center_x, pad_center_y],
                pincount=3, x_spacing=dx*2,
                drill=d_small, size=s_small, initial=n, increment=0,
                shape=Pad.SHAPE_CIRCLE, type=Pad.TYPE_THT, layers=Pad.LAYERS_THT))
            kicad_mod.append(PadArray(center=[pad_center_x, pad_center_y - dy],
                pincount=5, x_spacing=dx,
                drill=d_small, size=s_small, initial=n, increment=0,
                type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE, layers=Pad.LAYERS_THT))
            kicad_mod.append(PadArray(center=[pad_center_x, pad_center_y + dy],
                pincount=5, x_spacing=dx,
                drill=d_small, size=s_small, initial=n, increment=0,
                type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE, layers=Pad.LAYERS_THT))

    kicad_mod.append(Pad(at=[ret_dx, -ret_dy], type=Pad.TYPE_THT,
        shape=Pad.SHAPE_CIRCLE, size=ret_size, drill=ret_drill, layers=Pad.LAYERS_THT))
    kicad_mod.append(Pad(at=[ret_dx, P+ret_dy], type=Pad.TYPE_THT,
        shape=Pad.SHAPE_CIRCLE, size=ret_size, drill=ret_drill, layers=Pad.LAYERS_THT))

    kicad_mod.append(RectLine(start=[-pad_size[0]/2, -pad_size[1]/2],
        end=[offset_second_pad + pad_size[0]/2,pad_size[1]/2],offset=pad_silk_off,
        width=configuration['silk_line_width'], layer='B.SilkS'))

    ############################ Outline ##############################
    #kicad_mod.append(RectLine(start=[xl1, yt1], end=[xr1, yb1], layer='F.Fab', width=configuration['fab_line_width']))
    kicad_mod.append(RectLine(start=[xl1, yt2], end=[xr1, yb2], layer='F.Fab', width=configuration['fab_line_width']))
    kicad_mod.append(Line(start=[xl1, yt1], end=[xr1, yt1], layer='F.Fab', width=configuration['fab_line_width']))
    kicad_mod.append(Line(start=[xl1, yb1], end=[xr1, yb1], layer='F.Fab', width=configuration['fab_line_width']))

    off = configuration['silk_fab_offset']
    silk1 = [
        {'y': -pad_size[1]/2 - pad_silk_off, 'x': xl1-off},
        {'y': yt2-off, 'x': xl1-off},
        {'y': yt2-off, 'x': ret_dx-ret_size/2},
    ]
    kicad_mod.append(PolygoneLine(polygone=silk1, layer='F.SilkS', width=configuration['silk_line_width']))
    kicad_mod.append(PolygoneLine(polygone=silk1, layer='F.SilkS', width=configuration['silk_line_width'], y_mirror=P/2))
    silk2 = [
        {'y': yt2-off, 'x': ret_dx+ret_size/2},
        {'y': yt2-off, 'x': xr1+off},
        {'y': P/2, 'x': xr1+off},
    ]
    kicad_mod.append(PolygoneLine(polygone=silk2, layer='F.SilkS', width=configuration['silk_line_width']))
    kicad_mod.append(PolygoneLine(polygone=silk2, layer='F.SilkS', width=configuration['silk_line_width'], y_mirror=P/2))

    for i in range(pins - 1):
        kicad_mod.append(Line(start=[xl1-off, i*pitch+pad_size[1]/2+pad_silk_off],
            end=[xl1-off, (i+1)*pitch-pad_size[1]/2-pad_silk_off],
            layer='F.SilkS', width=configuration['silk_line_width']))

    for i in range(pins):
        w_pin = 3.8
        kicad_mod.append(RectLine(start=[xl1, i*pitch-w_pin/2], end=[xl2, i*pitch+w_pin/2],
        layer='F.Fab', width=configuration['fab_line_width']))

    ############################ Pin 1 ################################
    # Pin 1 designator
    pin1_sl = 2.4
    pin1 = [
        {'x': body_edge['left'], 'y': -pin1_sl/2},
        {'x': body_edge['left'] - pin1_sl/sqrt(2), 'y': 0},
        {'x': body_edge['left'], 'y': pin1_sl/2}
    ]
    kicad_mod.append(PolygoneLine(polygone=pin1, layer='F.Fab', width=configuration['fab_line_width']))
    kicad_mod.append(PolygoneLine(polygone=pin1, layer='F.Fab', width=configuration['fab_line_width'],
        x_mirror=(body_edge['left']+xl2)/2))

    pin1 = [
        {'y': -pad_size[1]/2 - pad_silk_off, 'x': xl1-off},
        {'y': -pad_size[1]/2 - pad_silk_off, 'x': -pad_size[0]/2}
    ]
    kicad_mod.append(PolygoneLine(polygone=pin1, layer='F.SilkS', width=configuration['silk_line_width']))

    # pin1 = [
    #     {'x': 0, 'y': 8},
    #     {'x': 0.5, 'y': 9},
    #     {'x': -0.5, 'y': 9},
    #     {'x': 0, 'y': 8},
    # ]
    # kicad_mod.append(PolygoneLine(polygone=pin1, layer='F.SilkS', width=configuration['silk_line_width']))

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
    for version in version_params:
        for pins_per_row in pins_per_row_range:
            generate_one_footprint(pins_per_row, version_params[version], configuration)
