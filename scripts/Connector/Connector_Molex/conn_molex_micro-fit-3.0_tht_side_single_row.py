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

series = "Micro-Fit_3.0"
series_long = 'Micro-Fit 3.0 Connector System'
manufacturer = 'Molex'
orientation = 'H'
number_of_rows = 1
datasheet = 'https://www.molex.com/pdm_docs/sd/436500300_sd.pdf'

#Molex part number
#n = number of circuits per row
part_code = "43650-{n:02}00"

alternative_codes = [
"43650-{n:02}01",
"43650-{n:02}02"
]

pins_per_row_range = range(2,13)
pitch = 3.0
drill = 1.02
peg_drill = 3.0
pad_to_pad_clearance = 1.5 # Voltage rating is up to 600V (http://www.molex.com/pdm_docs/ps/PS-43045.pdf)
max_annular_ring = 0.5
min_annular_ring = 0.15


pad_size = [pitch - pad_to_pad_clearance, drill + 2*max_annular_ring]
if pad_size[0] - drill < 2*min_annular_ring:
    pad_size[0] = drill + 2*min_annular_ring
if pad_size[0] - drill > 2*max_annular_ring:
    pad_size[0] = drill + 2*max_annular_ring

if pad_size[1] - drill < 2*min_annular_ring:
    pad_size[1] = drill + 2*min_annular_ring
if pad_size[1] - drill > 2*max_annular_ring:
    pad_size[1] = drill + 2*max_annular_ring

pad_shape=Pad.SHAPE_OVAL
if pad_size[1] == pad_size[0]:
    pad_shape=Pad.SHAPE_CIRCLE

def generate_one_footprint(pins, configuration):
    pins_per_row = pins

    mpn = part_code.format(n=pins)
    alt_mpn = [code.format(n=pins) for code in alternative_codes]

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

    ########################## Dimensions ##############################
    B = (pins_per_row-1)*pitch
    A = B + 6.65

    #Centra os pinos em metade do pitch
    pad_row_1_y = 0
    pad_row_2_y = pad_row_1_y + pitch
    pad1_x = 0

    C = 1.7 + pitch*(pins-3) #1º need be 4.7mm

    body_edge={
        'left':-3.325,
        'right':A-3.325,
        'top': -8.92
        }
    body_edge['bottom'] = body_edge['top'] + 9.90

    ############################# Pads ##################################
    #
    # Pegs
    #
    if pins_per_row == 2:
        kicad_mod.append(Pad(at=[pitch/2, pad_row_1_y - 4.32], number="",
            type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE, size=peg_drill,
            drill=peg_drill, layers=Pad.LAYERS_NPTH))
    elif pins_per_row == 3:
        kicad_mod.append(Pad(at=[pitch, pad_row_1_y - 4.32], number="",
            type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE, size=peg_drill,
            drill=peg_drill, layers=Pad.LAYERS_NPTH))
    else:
        kicad_mod.append(Pad(at=[pad1_x + 2.15, pad_row_1_y - 4.32], number="",
            type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE, size=peg_drill,
            drill=peg_drill, layers=Pad.LAYERS_NPTH))
        kicad_mod.append(Pad(at=[pad1_x + 2.15 + C, pad_row_1_y - 4.32], number="",
            type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE, size=peg_drill,
            drill=peg_drill, layers=Pad.LAYERS_NPTH))

    #
    # Add pads
    #
    optional_pad_params = {}
    if configuration['kicad4_compatible']:
        optional_pad_params['tht_pad1_shape'] = Pad.SHAPE_RECT
    else:
        optional_pad_params['tht_pad1_shape'] = Pad.SHAPE_ROUNDRECT

    kicad_mod.append(PadArray(start=[pad1_x, pad_row_1_y], initial=1,
        pincount=pins_per_row, increment=1,  x_spacing=pitch, size=pad_size,
        type=Pad.TYPE_THT, shape=pad_shape, layers=Pad.LAYERS_THT, drill=drill,
        **optional_pad_params))

    ######################## Fabrication Layer ###########################
    main_body_poly= [
        {'x': body_edge['left'], 'y': body_edge['bottom']},
        {'x': body_edge['left'], 'y': body_edge['top']+1},
        {'x': body_edge['left']+1, 'y': body_edge['top']},
        {'x': body_edge['right']-1, 'y': body_edge['top']},
        {'x': body_edge['right'], 'y': body_edge['top']+1},
        {'x': body_edge['right'], 'y': body_edge['bottom']},
        {'x': body_edge['left'], 'y': body_edge['bottom']}
    ]
    kicad_mod.append(PolygoneLine(polygone=main_body_poly,
        width=configuration['fab_line_width'], layer="F.Fab"))

    main_arrow_poly= [
        {'x': -.75, 'y': body_edge['bottom']},
        {'x': 0, 'y': 0},
        {'x': 0.75, 'y': body_edge['bottom']}
    ]
    kicad_mod.append(PolygoneLine(polygone=main_arrow_poly,
        width=configuration['fab_line_width'], layer="F.Fab"))

    ######################## SilkS Layer ###########################

    off = configuration['silk_fab_offset']
    pad_silk_off = configuration['silk_line_width']/2 + configuration['silk_pad_clearance']

    r_no_silk = max(pad_size)/2 + pad_silk_off # simplified to circle instead of oval
    dy = abs(body_edge['bottom']) + off
    pin_center_silk_x = 0 if dy >= r_no_silk else sqrt(r_no_silk**2-dy**2)
    pin1_center_silk_x = pad_size[0]/2 + pad_silk_off # simplified to rectangle instead of rounded rect

    poly_s_t= [
        {'x': body_edge['left'] - off, 'y': body_edge['bottom'] + off},
        {'x': body_edge['left'] - off, 'y': body_edge['top'] + 1 - off},
        {'x': body_edge['left'] + 1 - off, 'y': body_edge['top'] - off},
        {'x': body_edge['right'] - 1 + off, 'y': body_edge['top'] - off},
        {'x': body_edge['right'] + off, 'y': body_edge['top'] + 1 - off},
        {'x': body_edge['right'] + off, 'y': body_edge['bottom'] + off}
    ]
    kicad_mod.append(PolygoneLine(polygone=poly_s_t,
        width=configuration['silk_line_width'], layer="F.SilkS"))

    if pin_center_silk_x == 0:
        kicad_mod.append(Line(
            start=[body_edge['left']-off, body_edge['bottom']],
            end=[body_edge['right']-off, body_edge['bottom']],
            layer="F.SilkS", width=configuration['silk_line_width']
        ))
    else:
        kicad_mod.append(Line(
            start=[body_edge['left']-off, body_edge['bottom']+off],
            end=[-pin1_center_silk_x, body_edge['bottom']+off],
            layer="F.SilkS", width=configuration['silk_line_width']
        ))
        kicad_mod.append(Line(
            start=[body_edge['right']+off, body_edge['bottom']+off],
            end=[(pins_per_row-1)*pitch + pin_center_silk_x, body_edge['bottom']+off],
            layer="F.SilkS", width=configuration['silk_line_width']
        ))
        kicad_mod.append(Line(
            start=[pin1_center_silk_x, body_edge['bottom']+off],
            end=[pitch - pin_center_silk_x, body_edge['bottom']+off],
            layer="F.SilkS", width=configuration['silk_line_width']
        ))
        for i in range(1, pins_per_row-1):
            xl = i*pitch + pin_center_silk_x
            xr = (i+1)*pitch - pin_center_silk_x
            kicad_mod.append(Line(
                start=[xl, body_edge['bottom']+off],
                end=[xr, body_edge['bottom']+off],
                layer="F.SilkS", width=configuration['silk_line_width']
            ))

    ######################## CrtYd Layer ###########################
    CrtYd_offset = configuration['courtyard_offset']['connector']
    CrtYd_grid = configuration['courtyard_grid']

    poly_yd = [
        {'x': roundToBase(body_edge['left'] - CrtYd_offset, CrtYd_grid), 'y': roundToBase(body_edge['bottom'] + CrtYd_offset, CrtYd_grid)},
        {'x': roundToBase(body_edge['left'] - CrtYd_offset, CrtYd_grid), 'y': roundToBase(body_edge['top'] - CrtYd_offset, CrtYd_grid)},
        {'x': roundToBase(body_edge['right'] + CrtYd_offset, CrtYd_grid), 'y': roundToBase(body_edge['top'] - CrtYd_offset, CrtYd_grid)},
        {'x': roundToBase(body_edge['right'] + CrtYd_offset, CrtYd_grid), 'y': roundToBase(body_edge['bottom'] + CrtYd_offset, CrtYd_grid)},
        {'x': roundToBase(body_edge['left'] - CrtYd_offset, CrtYd_grid), 'y': roundToBase(body_edge['bottom'] + CrtYd_offset, CrtYd_grid)}
    ]

    kicad_mod.append(PolygoneLine(polygone=poly_yd,
        layer='F.CrtYd', width=configuration['courtyard_line_width']))

    ######################### Text Fields ###############################
    cy1 = roundToBase(body_edge['top'] - configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])
    cy2 = roundToBase(pad_size[1] + configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])

    addTextFields(kicad_mod=kicad_mod, configuration=configuration, body_edges=body_edge,
        courtyard={'top':cy1, 'bottom':cy2}, fp_name=footprint_name, text_y_inside_position='top')

    ##################### Write to File and 3D ############################
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

    for pincount in pins_per_row_range:
        generate_one_footprint(pincount, configuration)
