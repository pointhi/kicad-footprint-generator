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

"""
footprint specific details to go here

Hirose DF63

URL:
https://www.hirose.com/product/en/products/DF63/

Datasheet:
https://www.hirose.com/product/document?clcode=&productname=&series=DF63&documenttype=Catalog&lang=en&documentid=D31622_en
"""

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

series = 'DF63'
series_long = 'DF63 through hole'
manufacturer = 'Hirose'
orientation = 'V'
number_of_rows = 1
datasheet = 'https://www.hirose.com/product/en/products/DF63/'

#pins_per_row per row
pins_per_row_range = [1,2,3,4,5,6]

types = ['M', 'R']

#Hirose part number
#n = number of circuits per row
part_code = "DF63{f:s}-{n:d}P-3.96DSA"

pitch = 3.96
drill = 1.8
mount_size = 1.6

pad_to_pad_clearance = 1.5
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



def generate_one_footprint(pins, form_type, configuration):
    mpn = part_code.format(n=pins, f=form_type)
    off = configuration['silk_fab_offset']
    pad_silk_off = configuration['silk_line_width']/2 + configuration['silk_pad_clearance']

    pad_silk_off = configuration['silk_line_width']/2 + configuration['silk_pad_clearance']
    # handle arguments
    orientation_str = configuration['orientation_options'][orientation]
    footprint_name = configuration['fp_name_no_series_format_string'].format(man=manufacturer,
        mpn=mpn, num_rows=number_of_rows, pins_per_row=pins, mounting_pad = "",
        pitch=pitch, orientation=orientation_str)

    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription("Hirose {:s}, {:s}, {:d} Pins per row ({:s}), generated with kicad-footprint-generator".format(series_long, mpn, pins, datasheet))
    kicad_mod.setTags(configuration['keyword_fp_string'].format(series=series,
        orientation=orientation_str, man=manufacturer,
        entry=configuration['entry_direction'][orientation]))



    #vertical center of connector
    y2 = 3.25 + mount_size / 2
    y1 = y2 - 7.05
    yt = y2 - 8

    #Major dimensions
    B = ( pins - 1 ) * pitch
    A = B + 4.7
    if pins == 1:
        A = 6.2

    #calculate major dimensions
    x1 = (B - A) / 2
    x2 = x1 + A

    body_edge={
        'left':x1,
        'right':x2,
        'bottom':y2,
        'top': y1
        }
    bounding_box = body_edge.copy()
    bounding_box['top'] = yt

    #pins

    optional_pad_params = {}
    if configuration['kicad4_compatible']:
        optional_pad_params['tht_pad1_shape'] = Pad.SHAPE_RECT
    else:
        optional_pad_params['tht_pad1_shape'] = Pad.SHAPE_ROUNDRECT

    kicad_mod.append(
        PadArray(
                pincount=pins,
                initial = 1,
                start = [0, 0],
                x_spacing = pitch,
                type = Pad.TYPE_THT,
                layers = Pad.LAYERS_THT,
                shape = pad_shape,
                size = pad_size,
                drill = drill,
                **optional_pad_params
                )
    )

    #mounting hole
    if form_type in ['M', '']:
        peg_location = [-1.5, 3.25]
    else:
        peg_location = [B+1.5, 3.25]
    kicad_mod.append(Pad(at=peg_location,type=Pad.TYPE_NPTH,layers=Pad.LAYERS_NPTH,shape=Pad.SHAPE_CIRCLE,size=mount_size,drill=mount_size))

    #connector outline

    #tab thickness
    t = 1.2

    def outline(offset=0):
        outline = [
        {'x': B/2, 'y': y2 + offset},
        {'x': x1 - offset, 'y': y2 + offset},
        {'x': x1 - offset, 'y': yt - offset},
        {'x': x1 + t + offset, 'y': yt - offset},
        {'x': x1 + t + offset, 'y': y1 - offset},
        {'x': B/2, 'y': y1 - offset},
        ]

        return outline

    kicad_mod.append(PolygoneLine(polygone=outline(),layer='F.Fab', width=configuration['fab_line_width']))
    kicad_mod.append(PolygoneLine(polygone=outline(),x_mirror=B/2,
        layer='F.Fab', width=configuration['fab_line_width']))

    kicad_mod.append(PolygoneLine(polygone=outline(offset=off),
        layer='F.SilkS', width=configuration['silk_line_width']))
    kicad_mod.append(PolygoneLine(polygone=outline(offset=off),x_mirror=B/2,
        layer='F.SilkS', width=configuration['silk_line_width']))

    #draw lines between pads on F.Fab
    for i in range(pins - 1):
        x = (i + 0.5) * pitch

        kicad_mod.append(Line(start=[x,y1], end=[x,y2],
            layer='F.Fab', width=configuration['fab_line_width']))

    #pin-1 indicator
    kicad_mod.append(Circle(center=[0,-3.75], radius=0.25,
        layer='F.SilkS', width=configuration['silk_line_width']))

    sl=2
    pin = [
        {'y': body_edge['top'], 'x': -sl/2},
        {'y': body_edge['top'] + sl/sqrt(2), 'x': 0},
        {'y': body_edge['top'], 'x': sl/2}
    ]
    kicad_mod.append(PolygoneLine(polygone=pin,
        width=configuration['fab_line_width'], layer='F.Fab'))

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
        courtyard={'top':cy1, 'bottom':cy2}, fp_name=footprint_name, text_y_inside_position=-3.75)

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
        for form_type in types:
            if form_type is 'R' and pins_per_row is 6:
                continue
            if form_type is 'M' and pins_per_row in [5,6]:
                form_type = ''
            generate_one_footprint(pins_per_row, form_type, configuration)
