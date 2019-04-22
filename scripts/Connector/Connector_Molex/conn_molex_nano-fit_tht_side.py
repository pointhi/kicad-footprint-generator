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

series = "Nano-Fit"
series_long = 'Nano-Fit Power Connectors'
manufacturer = 'Molex'
orientation = 'H'

#pins_per_row per row
pins_per_row_range = range(2,9)

#Molex part number
#n = number of circuits per row


pitch = 2.5
drill = 1.2

pitch_row = 2.5

pad_to_pad_clearance = 0.8
max_annular_ring = 0.5
min_annular_ring = 0.15

version_params = {
    'dual':{
        'number_of_rows': 2,
        'datasheet': 'http://www.molex.com/pdm_docs/sd/1053141208_sd.pdf',
        'mpn': "105314-xx{n:02}"
    },
    'single':{
        'number_of_rows': 1,
        'datasheet': 'http://www.molex.com/pdm_docs/sd/1053131208_sd.pdf',
        'mpn': "105313-xx{n:02}"
    }
}

def generate_one_footprint(pins, params, configuration):
    pad_silk_off = configuration['silk_pad_clearance'] + configuration['silk_line_width']/2
    mpn = params['mpn'].format(n=pins*params['number_of_rows'])

    # handle arguments
    orientation_str = configuration['orientation_options'][orientation]
    footprint_name = configuration['fp_name_format_string'].format(man=manufacturer,
        series=series,
        mpn=mpn, num_rows=params['number_of_rows'], pins_per_row=pins_per_row, mounting_pad = "",
        pitch=pitch, orientation=orientation_str)

    kicad_mod = Footprint(footprint_name)
    desc_format_str = "Molex {:s}, {:s}, {:d} Pins per row ({:s}), generated with kicad-footprint-generator"
    kicad_mod.setDescription(desc_format_str.format(series_long, mpn, pins, params['datasheet']))
    kicad_mod.setTags(configuration['keyword_fp_string'].format(series=series,
        orientation=orientation_str, man=manufacturer,
        entry=configuration['entry_direction'][orientation]))

    if params['number_of_rows'] == 2:
        pad_size = [pitch_row - pad_to_pad_clearance, pitch - pad_to_pad_clearance]
    else:
        pad_size = [drill + 2*max_annular_ring, pitch - pad_to_pad_clearance]

    if pad_size[1] - drill < 2*min_annular_ring:
        pad_size[1] = drill + 2*min_annular_ring
    if pad_size[1] - drill > 2*max_annular_ring:
        pad_size[1] = drill + 2*max_annular_ring

    if pad_size[0] - drill < 2*min_annular_ring:
        pad_size[0] = drill + 2*min_annular_ring
    if pad_size[0] - drill > 2*max_annular_ring:
        pad_size[0] = drill + 2*max_annular_ring

    pad_shape=Pad.SHAPE_OVAL
    if pad_size[0] == pad_size[1]:
        pad_shape=Pad.SHAPE_CIRCLE

    #A = connector length
    A = pins * pitch + 0.94

    #B = pin center distance
    B = (pins - 1) * pitch

    #W = thickness of plastic base
    W = 8.46

    #locating pin position
    C = B

    #corner positions for plastic housing outline
    y1 = -(A-B)/2
    y2 = y1 + A

    x2 = (params['number_of_rows'] - 1) * pitch_row + 10.38
    x1 = x2 - W

    off = configuration['silk_fab_offset']
    pad_silk_off = configuration['silk_pad_clearance'] + configuration['silk_line_width']/2

    body_edge={
        'left':x1,
        'right':x2,
        'bottom':y2,
        'top': y1
        }
    bounding_box = body_edge.copy()

    bounding_box['left'] = -pad_size[0]/2

    pad_silk_off = configuration['silk_pad_clearance'] + configuration['silk_line_width']/2

    #generate the pads
    optional_pad_params = {}
    if configuration['kicad4_compatible']:
        optional_pad_params['tht_pad1_shape'] = Pad.SHAPE_RECT
    else:
        optional_pad_params['tht_pad1_shape'] = Pad.SHAPE_ROUNDRECT

    for r in range(params['number_of_rows']):
        kicad_mod.append(PadArray(
            pincount=pins, initial=r*pins+1, start=[r*pitch_row,0],
            y_spacing=pitch, type=Pad.TYPE_THT, shape=pad_shape,
            size=pad_size, drill=drill, layers=Pad.LAYERS_THT,
            **optional_pad_params))

    #add the locating pins
    y_loc_a = B/2 - C/2
    y_loc_b = B/2 + C/2
    x_loc = (params['number_of_rows']-1)*pitch_row+7.18
    r_loc = 1.7
    kicad_mod.append(Pad(at=[x_loc,y_loc_a],size=r_loc,drill=r_loc,type=Pad.TYPE_NPTH,shape=Pad.SHAPE_CIRCLE, layers=Pad.LAYERS_NPTH))
    kicad_mod.append(Pad(at=[x_loc,y_loc_b],size=r_loc,drill=r_loc,type=Pad.TYPE_NPTH,shape=Pad.SHAPE_CIRCLE, layers=Pad.LAYERS_NPTH))

    #add outline to F.Fab
    kicad_mod.append(RectLine(start=[x1,y1],end=[x2,y2],layer='F.Fab', width=configuration['fab_line_width']))

    kicad_mod.append(RectLine(start=[x1,y1],end=[x2,y2],offset=off, width=configuration['silk_line_width'], layer="F.SilkS"))

    #draw the pins
    for i in range(pins):
        y = i * pitch
        x = (params['number_of_rows'] - 1) * pitch_row + pad_size[0]/2 + pad_silk_off
        w = 0.15
        kicad_mod.append(RectLine(start=[x1-off,y+w],end=[x,y-w], width=configuration['silk_line_width'], layer="F.SilkS"))

    #pin-1 marker
    y = - pad_size[1]/2- pad_silk_off
    m = 0.3

    pin = [
    {'x': 0,'y': y},
    {'x': m,'y': y-m*sqrt(2)},
    {'x': -m,'y': y-m*sqrt(2)},
    {'x': 0,'y': y},
    ]

    kicad_mod.append(PolygoneLine(polygone=pin, width=configuration['silk_line_width'], layer="F.SilkS"))
    kicad_mod.append(PolygoneLine(polygone=pin, width=configuration['fab_line_width'], layer='F.Fab'))

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

    for version in version_params:
        for pins_per_row in pins_per_row_range:
            generate_one_footprint(pins_per_row, version_params[version], configuration)
