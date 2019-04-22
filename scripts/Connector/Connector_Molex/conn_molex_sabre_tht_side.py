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

series = "Sabre"
series_long = 'Sabre Power Connector'
manufacturer = 'Molex'
orientation = 'H'
number_of_rows = 1


#pins_per_row per row
pins_per_row_range = [2, 3, 4, 5, 6]

#Molex part number
#n = number of circuits per row

pitch = 7.49
drill = 1.78

offset_second_pad = 3.18

pad_to_pad_clearance = 3
max_annular_ring = 1
min_annular_ring = 0.15

#locating pins
ret_dy = 13.13
ret_dx = 4.75
ret_drill = 3.00
ret_size = 4.00



pad_size = [pitch - pad_to_pad_clearance, offset_second_pad + 0.25]
if pad_size[0] - drill < 2*min_annular_ring:
    pad_size[0] = drill + 2*min_annular_ring
if pad_size[0] - drill > 2*max_annular_ring:
    pad_size[0] = drill + 2*max_annular_ring

version_params = {
    'with_thermals_lock':{
        'mpn': '43160-11{n:02d}',
        'datasheet': 'http://www.molex.com/pdm_docs/sd/431605304_sd.pdf',
        'description': ', With thermal vias in pads',
        'fp_name_suffix': '_ThermalVias',
        'thermals': True,
        'lock': True
    },
    'only_pads_lock':{
        'mpn': '43160-11{n:02d}',
        'datasheet': 'http://www.molex.com/pdm_docs/sd/431605304_sd.pdf',
        'description': '',
        'fp_name_suffix': '',
        'thermals': False,
        'lock': True
    },
    'with_thermals':{
        'mpn': '46007-11{n:02d}',
        'datasheet': 'http://www.molex.com/pdm_docs/sd/460071105_sd.pdf',
        'description': ', With thermal vias in pads',
        'fp_name_suffix': '_ThermalVias',
        'thermals': True,
        'lock': False
    },
    'only_pads':{
        'mpn': '46007-11{n:02d}',
        'datasheet': 'http://www.molex.com/pdm_docs/sd/460071105_sd.pdf',
        'description': '',
        'fp_name_suffix': '',
        'thermals': False,
        'lock': False
    }
}



def generate_one_footprint(pins, params, configuration):
    pad_silk_off = configuration['silk_pad_clearance'] + configuration['silk_line_width']/2
    off = configuration['silk_fab_offset']

    mpn = params['mpn'].format(n=pins*number_of_rows)

    # handle arguments
    orientation_str = configuration['orientation_options'][orientation]
    footprint_name = configuration['fp_name_format_string'].format(man=manufacturer,
        series=series,
        mpn=mpn, num_rows=number_of_rows, pins_per_row=pins_per_row, mounting_pad = "",
        pitch=pitch, orientation=orientation_str)
    footprint_name += params['fp_name_suffix']

    kicad_mod = Footprint(footprint_name)
    desc_format_str = "Molex {:s}, {:s}{:s}, {:d} Pins per row ({:s}), generated with kicad-footprint-generator"
    kicad_mod.setDescription(desc_format_str.format(series_long, mpn, params['description'], pins, params['datasheet']))
    kicad_mod.setTags(configuration['keyword_fp_string'].format(series=series,
        orientation=orientation_str, man=manufacturer,
        entry=configuration['entry_direction'][orientation]))



    # Dimensions
    P = (pins - 1) * pitch
    B = P + 2*6.79 # connector length
    W = 14.76 # connector width

    body_edge={}
    body_edge['left'] = (P-B)/2
    body_edge['right'] = body_edge['left'] + B
    body_edge['top'] =  0.925
    body_edge['bottom'] = body_edge['top'] + 14.76

    bounding_box = body_edge.copy()
    bounding_box['top'] = -offset_second_pad - pad_size[1]/2

    ##################################  Pins ##################################
    kicad_mod.append(PadArray(pincount=pins, start=[0,0],
        x_spacing=pitch, size=pad_size, drill=drill,
        type=Pad.TYPE_THT, shape=Pad.SHAPE_RECT, layers=Pad.LAYERS_THT))
    kicad_mod.append(PadArray(pincount=pins, start=[0, -offset_second_pad],
        x_spacing=pitch, size=pad_size, drill=drill,
        shape=Pad.SHAPE_RECT, type=Pad.TYPE_THT, layers=Pad.LAYERS_THT))

    d_small = 0.3
    s_small = d_small + 2*min_annular_ring
    thermal_to_pad_edge = s_small/2 + 0.15

    if params['thermals']:
        for xi in range(pins):
            n = xi + 1
            pad_center_y = -offset_second_pad/2
            pad_center_x = xi*pitch
            pad_h = offset_second_pad + pad_size[1]
            dx = (pad_size[0] - 2*thermal_to_pad_edge)/2
            dy = (pad_h - 2*thermal_to_pad_edge)/4

            #draw rectangle on F.Fab layer

            # kicad_mod.append(RectLine(
            #     start=[pad_center_x - pad_l/2, pad_center_y - pad_size[1]/2],
            #     end=[pad_center_x + pad_l/2, pad_center_y + pad_size[1]/2],
            #     layer='F.Fab', width=configuration['fab_line_width']))

            kicad_mod.append(PadArray(center=[pad_center_x, pad_center_y],
                pincount=3, y_spacing=dy*2,
                drill=d_small, size=s_small, initial=n, increment=0,
                shape=Pad.SHAPE_CIRCLE, type=Pad.TYPE_THT, layers=Pad.LAYERS_THT))
            kicad_mod.append(PadArray(center=[pad_center_x - dx, pad_center_y],
                pincount=5, y_spacing=dy,
                drill=d_small, size=s_small, initial=n, increment=0,
                type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE, layers=Pad.LAYERS_THT))
            kicad_mod.append(PadArray(center=[pad_center_x + dx, pad_center_y],
                pincount=5, y_spacing=dy,
                drill=d_small, size=s_small, initial=n, increment=0,
                type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE, layers=Pad.LAYERS_THT))

    if params['lock']:
        kicad_mod.append(Pad(at=[-ret_dx, ret_dy], type=Pad.TYPE_THT,
            shape=Pad.SHAPE_CIRCLE, size=ret_size, drill=ret_drill, layers=Pad.LAYERS_THT))
        kicad_mod.append(Pad(at=[P+ret_dx, ret_dy], type=Pad.TYPE_THT,
            shape=Pad.SHAPE_CIRCLE, size=ret_size, drill=ret_drill, layers=Pad.LAYERS_THT))

    kicad_mod.append(RectLine(start=[-pad_size[0]/2, -offset_second_pad-pad_size[1]/2],
        end=[pad_size[0]/2,pad_size[1]/2],offset=pad_silk_off,
        width=configuration['silk_line_width'], layer='B.SilkS'))

    ############################ Outline ##############################
    #kicad_mod.append(RectLine(start=[xl1, yt1], end=[xr1, yb1], layer='F.Fab', width=configuration['fab_line_width']))
    kicad_mod.append(RectLine(
        start=[body_edge['left'], body_edge['top']],
        end=[body_edge['right'], body_edge['bottom']],
        layer='F.Fab', width=configuration['fab_line_width']))

    if params['lock']:
        silk1 = [
            {'x': -pad_size[0]/2 - pad_silk_off, 'y': body_edge['top']-off},
            {'x': body_edge['left']-off, 'y': body_edge['top']-off},
            {'x': body_edge['left']-off, 'y': ret_dy-ret_size/2},
        ]
        kicad_mod.append(PolygoneLine(polygone=silk1, layer='F.SilkS', width=configuration['silk_line_width']))
        kicad_mod.append(PolygoneLine(polygone=silk1, layer='F.SilkS', width=configuration['silk_line_width'], x_mirror=P/2))
        silk2 = [
            {'x': body_edge['left']-off, 'y': ret_dy+ret_size/2},
            {'x': body_edge['left']-off, 'y': body_edge['bottom']+off},
            {'x': P/2, 'y': body_edge['bottom']+off},
        ]
        kicad_mod.append(PolygoneLine(polygone=silk2,
            layer='F.SilkS', width=configuration['silk_line_width']))
        kicad_mod.append(PolygoneLine(polygone=silk2,
            layer='F.SilkS', width=configuration['silk_line_width'], x_mirror=P/2))
    else:
        kicad_mod.append(RectLine(
            start=[body_edge['left'], body_edge['top']],
            end=[body_edge['right'], body_edge['bottom']],
            offset = off,
            layer='F.SilkS', width=configuration['silk_line_width']))

    for i in range(pins - 1):
        kicad_mod.append(Line(
            start=[i*pitch+pad_size[0]/2+pad_silk_off, body_edge['top']-off],
            end=[(i+1)*pitch-pad_size[0]/2-pad_silk_off, body_edge['top']-off],
            layer='F.SilkS', width=configuration['silk_line_width']))

    for i in range(pins):
        w_pin = 1
        kicad_mod.append(RectLine(start=[i*pitch-w_pin/2, body_edge['top']],
        end=[i*pitch+w_pin/2, -offset_second_pad-drill/2],
        layer='F.Fab', width=configuration['fab_line_width']))

    ############################ Pin 1 ################################
    # Pin 1 designator
    pin1_sl = 2.4
    pin1 = [
        {'x': -pin1_sl/2, 'y': body_edge['top']},
        {'x': 0, 'y': body_edge['top'] + pin1_sl/sqrt(2)},
        {'x': pin1_sl/2, 'y': body_edge['top']}
    ]
    kicad_mod.append(PolygoneLine(polygone=pin1,
        layer='F.Fab', width=configuration['fab_line_width']))

    pin1 = [
        {'x': -pad_size[0]/2 - pad_silk_off, 'y': body_edge['top']-off},
        {'x': -pad_size[0]/2 - pad_silk_off, 'y': -offset_second_pad-pad_size[1]/2}
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
