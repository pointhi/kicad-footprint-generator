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

series = "Mega-Fit"
series_long = 'Mega-Fit Power Connectors'
manufacturer = 'Molex'
orientation = 'H'
number_of_rows = 2
datasheet = 'http://www.molex.com/pdm_docs/sd/1720640002_sd.pdf'

#pins_per_row per row
pins_per_row_range = [1, 2, 3, 4, 5, 6]

#Molex part number
#n = number of circuits per row
part_code = "76825-00{n:02d}"

alternative_codes = [
"172064-00{n:02d}",
"172064-10{n:02d}"
]

pitch = 5.7
drill = 1.8
start_pos_x = 0 # Where should pin 1 be located.
pad_to_pad_clearance = 1.75
max_annular_ring = 0.95 #How much copper should be in y direction?
min_annular_ring = 0.15


row = 5.5

size = row - pad_to_pad_clearance
if size - drill < 2*min_annular_ring:
    size = drill + 2*min_annular_ring
if size - drill > max_annular_ring:
    size = drill + 2*max_annular_ring



def generate_one_footprint(pins_per_row, configuration):
    mpn = part_code.format(n=pins_per_row*2)
    alt_mpn = [code.format(n=pins_per_row*2) for code in alternative_codes]

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
    #http://www.molex.com/pdm_docs/sd/768250010_sd.pdf

    #connector length
    if pins_per_row == 1:
        A = 8.35
    else:
        A = pins_per_row * pitch + 0.65

    if pins_per_row == 1 or pins_per_row == 2:
        B = 0
    else:
        B = A - 6.35

    #pin centers
    P = (pins_per_row - 1) * pitch

    #corner positions for plastic housing outline

    x1 = -(A-P)/2
    x2 = x1 + A

    y2 = -1.1
    y1 = y2 - 14.8

    body_edge={
        'left':x1,
        'right':x2,
        'bottom':y2,
        'top': y1
        }

    #generate the pads
    optional_pad_params = {}
    if configuration['kicad4_compatible']:
        optional_pad_params['tht_pad1_shape'] = Pad.SHAPE_RECT
    else:
        optional_pad_params['tht_pad1_shape'] = Pad.SHAPE_ROUNDRECT

    for row_idx in range(2):
        kicad_mod.append(PadArray(
            pincount=pins_per_row, initial=row_idx*pins_per_row+1,
            start=[0, row_idx*row], x_spacing=pitch, type=Pad.TYPE_THT,
            shape=Pad.SHAPE_CIRCLE, size=size, drill=drill, layers=Pad.LAYERS_THT,
            **optional_pad_params))

    off = configuration['silk_fab_offset']
    silk_pad_off = configuration['silk_pad_clearance'] + configuration['silk_line_width']/2

    #add PCB locators
    r_loc = 3.00
    y_loc = -7.3

    #two locators
    if pins_per_row > 2:
        lx1 = P/2 - B/2
        lx2 = P/2 + B/2

        kicad_mod.append(Pad(at=[lx1, y_loc],type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE, size=r_loc,drill=r_loc, layers=Pad.LAYERS_NPTH))
        kicad_mod.append(Pad(at=[lx2, y_loc],type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE, size=r_loc,drill=r_loc, layers=Pad.LAYERS_NPTH))

        kicad_mod.append(Circle(center=[lx1, y_loc],radius=r_loc/2+silk_pad_off, layer='F.SilkS', width=configuration['silk_line_width']))
        kicad_mod.append(Circle(center=[lx2, y_loc],radius=r_loc/2+silk_pad_off, layer='F.SilkS', width=configuration['silk_line_width']))
    else:
        #one locator
        kicad_mod.append(Pad(at=[P/2,y_loc],type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE, size=r_loc, drill=r_loc, layers=Pad.LAYERS_NPTH))

        kicad_mod.append(Circle(center=[P/2,y_loc], radius=r_loc/2+silk_pad_off, layer='F.SilkS', width=configuration['silk_line_width']))

    #draw the outline of the shape
    kicad_mod.append(RectLine(start=[x1,y1],end=[x2,y2], layer='F.Fab', width=configuration['fab_line_width']))

    outline = [
    {'x': P/2,'y': y1-off},
    {'x': x1-off,'y': y1-off},
    {'x': x1-off,'y': y2+off},
    {'x': -size/2 - silk_pad_off,'y': y2+off},
    ]

    kicad_mod.append(PolygoneLine(polygone=outline, layer='F.SilkS', width=configuration['silk_line_width']))
    kicad_mod.append(PolygoneLine(polygone=outline,x_mirror=P/2 if P != 0 else 0.00000001, layer='F.SilkS', width=configuration['silk_line_width']))

    #draw lines between each pin
    for i in range(pins_per_row-1):
        xa = i * pitch + size / 2 + silk_pad_off
        xb = (i+1) * pitch - size / 2 - silk_pad_off

        kicad_mod.append(Line(start=[xa,y2+off],end=[xb,y2+off], layer='F.SilkS', width=configuration['silk_line_width']))

    #draw the pins!

    o = size/2 + silk_pad_off
    w = 0.3
    for i in range(pins_per_row):
        x = i * pitch
        ya = o
        yb = row - o
        kicad_mod.append(Line(start=[x-w,ya],end=[x-w,yb], layer='F.SilkS', width=configuration['silk_line_width']))
        kicad_mod.append(Line(start=[x+w,ya],end=[x+w,yb], layer='F.SilkS', width=configuration['silk_line_width']))

    #pin-1 marker
    x =  -2.5
    m = 0.3

    pin = [
    {'x': x,'y': 0},
    {'x': x-2*m,'y': +m},
    {'x': x-2*m,'y': -m},
    {'x': x,'y': 0},
    ]

    kicad_mod.append(PolygoneLine(polygone=pin, layer='F.SilkS', width=configuration['silk_line_width']))

    sl = 2
    pin = [
        {'x': -sl/2, 'y': body_edge['bottom']},
        {'x': 0, 'y': body_edge['bottom']-sl/sqrt(2)},
        {'x': sl/2, 'y': body_edge['bottom']},
    ]
    kicad_mod.append(PolygoneLine(polygone=pin, width=configuration['fab_line_width'], layer='F.Fab'))

    ########################### CrtYd #################################
    cx1 = roundToBase(body_edge['left']-configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])
    cy1 = roundToBase(body_edge['top']-configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])

    cx2 = roundToBase(body_edge['right']+configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])
    cy2 = roundToBase(row + size/2 + configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])

    kicad_mod.append(RectLine(
        start=[cx1, cy1], end=[cx2, cy2],
        layer='F.CrtYd', width=configuration['courtyard_line_width']))

    ######################### Text Fields ###############################
    addTextFields(kicad_mod=kicad_mod, configuration=configuration, body_edges=body_edge,
        courtyard={'top':cy1, 'bottom':cy2}, fp_name=footprint_name, text_y_inside_position='top')

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
