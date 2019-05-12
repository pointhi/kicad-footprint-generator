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

series = "Micro-Latch"
series_long = 'Micro-Latch Wire-to-Board Connector System'
manufacturer = 'Molex'
orientation = 'V'
number_of_rows = 1
datasheet = 'http://www.molex.com/pdm_docs/sd/532530770_sd.pdf'

#pins_per_row per row
pins_per_row_range = range(2,16)

#Molex part number
#n = number of circuits per row
part_code = "53253-{n:02d}70"

alternative_codes = [
"53253-{n:02d}50"
]

pitch = 2
drill = 0.8
start_pos_x = 0 # Where should pin 1 be located.
pad_to_pad_clearance = 0.8
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



def generate_one_footprint(pins_per_row, configuration):
    mpn = part_code.format(n=pins_per_row*number_of_rows)
    alt_mpn = [code.format(n=pins_per_row*number_of_rows) for code in alternative_codes]

    # handle arguments
    orientation_str = configuration['orientation_options'][orientation]
    footprint_name = configuration['fp_name_format_string'].format(man=manufacturer,
        series=series,
        mpn=mpn, num_rows=number_of_rows, pins_per_row=pins_per_row, mounting_pad = "",
        pitch=pitch, orientation=orientation_str)

    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription("Molex {:s}, {:s} (compatible alternatives: {:s}), {:d} Pins per row ({:s}), generated with kicad-footprint-generator".format(series_long, mpn, ', '.join(alt_mpn), pins_per_row, datasheet))
    kicad_mod.setTags(configuration['keyword_fp_string'].format(series=series,
        orientation=orientation_str, man=manufacturer,
        entry=configuration['entry_direction'][orientation]))

    #calculate fp dimensions
    A = (pins_per_row - 1) * pitch
    B = A + 3.1
    C = A + 4

    #connector thickness
    T = 5.75

    #corners
    x1 = -2
    x2 = x1 + C

    T = 3.65

    y1 = -1.5
    y2 = y1 + T

    off = configuration['silk_fab_offset']
    pad_silk_off = configuration['silk_pad_clearance'] + configuration['silk_line_width']/2

    body_edge={
        'left':x1,
        'right':x2,
        'bottom':y2,
        'top': y1
        }
    bounding_box = body_edge.copy()

    #add simple outline to F.Fab layer
    kicad_mod.append(RectLine(start=[x1,y1],end=[x2,y2],layer='F.Fab', width=configuration['fab_line_width']))

    #wall-thickness W
    w = 0.4

    #offset
    o = configuration['silk_fab_offset']
    x1 -= o
    y1 -= o
    x2 += o
    y2 += o

    #generate the pads
    optional_pad_params = {}
    if configuration['kicad4_compatible']:
        optional_pad_params['tht_pad1_shape'] = Pad.SHAPE_RECT
    else:
        optional_pad_params['tht_pad1_shape'] = Pad.SHAPE_ROUNDRECT

    kicad_mod.append(PadArray(
        pincount=pins_per_row, x_spacing=pitch, type=Pad.TYPE_THT,
        shape=pad_shape, size=pad_size, drill=drill, layers=Pad.LAYERS_THT,
        **optional_pad_params))

    #draw the courtyard

    #draw the connector outline
    out = RectLine(start=[x1,y1], end=[x2,y2],
        width=configuration['silk_line_width'], layer="F.SilkS")
    kicad_mod.append(out)

    #pin-1 marker
    y =  -2
    m = 0.3

    O = 0.3
    L = 2
    pin = [
        {'x': x1 + L, 'y': y1 - O},
        {'x': x1 - O, 'y': y1 - O},
        {'x': x1 - O, 'y': y1 + L},
        ]

    kicad_mod.append(PolygoneLine(polygone=pin,
        width=configuration['silk_line_width'], layer="F.SilkS"))

    p1m_sl = 1
    pin =[
        {'x': -p1m_sl/2, 'y': body_edge['top']},
        {'x': 0, 'y': body_edge['top'] + p1m_sl/sqrt(2)},
        {'x': p1m_sl/2, 'y': body_edge['top']}
    ]
    kicad_mod.append(PolygoneLine(polygone=pin, width=configuration['fab_line_width'], layer='F.Fab'))

    kicad_mod.append(Line(start=[x1,2*w],end=[x1+w,2*w],
        width=configuration['silk_line_width'], layer="F.SilkS"))
    kicad_mod.append(Line(start=[x2,2*w],end=[x2-w,2*w],
        width=configuration['silk_line_width'], layer="F.SilkS"))

    #add the 'wall'
    wall = [
    {'x': A/2,'y': y1+w},
    {'x': x1+w,'y': y1+w},
    {'x': x1+w,'y': 0},
    {'x': x1+2*w,'y': 0},
    {'x': x1+2*w,'y': w},
    {'x': x1+w,'y': w},
    {'x': x1+w,'y': y2},
    ]

    kicad_mod.append(PolygoneLine(polygone=wall,
        width=configuration['silk_line_width'], layer="F.SilkS"))
    kicad_mod.append(PolygoneLine(polygone=wall,x_mirror=A/2,
        width=configuration['silk_line_width'], layer="F.SilkS"))

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
