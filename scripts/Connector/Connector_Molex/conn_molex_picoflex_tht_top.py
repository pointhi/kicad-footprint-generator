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

series = "Picoflex"
series_long = 'Picoflex Ribbon-Cable Connectors'
manufacturer = 'Molex'
orientation = 'V'
number_of_rows = 2
datasheet = 'http://www.molex.com/pdm_docs/sd/903250004_sd.pdf'

#pins_per_row per row
pins_range = (4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26)

#Molex part number
#n = number of circuits per row
part_code = "90325-00{n:02}"

pitch = 1.27
pitch_row = 2.54
drill = 0.8

pad_to_pad_clearance = 0.8
max_annular_ring = 0.5
min_annular_ring = 0.15



pad_size = [drill + 0.5*2, drill + 0.25*2]
pad_shape = Pad.SHAPE_OVAL


def generate_one_footprint(pins, configuration):
    mpn = part_code.format(n=pins)

    CrtYd_off = configuration['courtyard_offset']['connector']
    CrtYd_grid = configuration['courtyard_grid']
    body_edge = {}
    bounding_box = {}

    # handle arguments
    orientation_str = configuration['orientation_options'][orientation]
    footprint_name = configuration['fp_name_format_string'].format(man=manufacturer,
        series=series,
        mpn=mpn, num_rows=number_of_rows, pins_per_row=pins//2, mounting_pad = "",
        pitch=pitch, orientation=orientation_str)

    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription("Molex {:s}, {:s}, {:d} Pins ({:s}), generated with kicad-footprint-generator".format(series_long, mpn, pins, datasheet))
    kicad_mod.setTags(configuration['keyword_fp_string'].format(series=series,
        orientation=orientation_str, man=manufacturer,
        entry=configuration['entry_direction'][orientation]))

    GuideHoleDrillSize = 1.5

    GuideHoleX1 = -1.48
    GuideHoleY1 = -1.8

    GuideHoleY2 = (pins - 1) * pitch - GuideHoleY1

    StartFX = GuideHoleX1
    StartFY = 0 - 2.755

    # generate the pads
    optional_pad_params = {}
    if configuration['kicad4_compatible']:
        optional_pad_params['tht_pad1_shape'] = Pad.SHAPE_RECT
    else:
        optional_pad_params['tht_pad1_shape'] = Pad.SHAPE_ROUNDRECT

    tpc = int(pins / 2)
    for row_idx in range(2):
        kicad_mod.append(PadArray(
            start=[2*row_idx*pitch, row_idx*pitch], pincount=tpc, initial=row_idx+1,
            increment=2, x_spacing=0,  y_spacing=2*pitch, type=Pad.TYPE_THT,
            shape=pad_shape, size=pad_size, drill=drill, layers=Pad.LAYERS_THT,
            **optional_pad_params))

    # Generate the drill holes
    stx = (pins - 1) * pitch + 1.8
    kicad_mod.append(Pad(at=[GuideHoleX1, GuideHoleY1],type=Pad.TYPE_NPTH,
        shape=Pad.SHAPE_CIRCLE, size=GuideHoleDrillSize,
        drill=GuideHoleDrillSize, layers=Pad.LAYERS_NPTH))
    kicad_mod.append(Pad(at=[GuideHoleX1, GuideHoleY2],type=Pad.TYPE_NPTH,
        shape=Pad.SHAPE_CIRCLE, size=GuideHoleDrillSize,
        drill=GuideHoleDrillSize, layers=Pad.LAYERS_NPTH))


    #
    # Top lines
    #
    x1 = StartFX
    y1 = StartFY
    x2 = x1 + 5
    y2 = y1
    kicad_mod.append(PolygoneLine(
        polygone=[[x1, y1], [x2, y2]],
        layer='F.Fab', width=configuration['fab_line_width']))
    kicad_mod.append(PolygoneLine(
        polygone=[[x1, y1 - 0.13], [x2 + 0.13, y2 - 0.13]],
        layer='F.SilkS', width=configuration['silk_line_width']))
    body_edge['top'] = y1
    bounding_box['top'] = y1

    #
    # Right lines
    #
    x1 = x2
    y1 = y2
    x2 = x2
    y2 = ((pins - 1) * pitch) + 2.755
    kicad_mod.append(PolygoneLine(
        polygone=[[x1, y1], [x2, y2]],
        layer='F.Fab', width=configuration['fab_line_width']))
    kicad_mod.append(PolygoneLine(
        polygone=[[x1 + 0.13, y1 - 0.13], [x2 + 0.13, y2 + 0.13]],
        layer='F.SilkS', width=configuration['silk_line_width']))
    body_edge['right'] = x1
    bounding_box['right'] = x1

    #
    # Bottom lines
    #
    x1 = x2
    y1 = y2
    x2 = StartFX
    y2 = y2
    kicad_mod.append(PolygoneLine(
        polygone=[[x1, y1], [x2, y2]],
        layer='F.Fab', width=configuration['fab_line_width']))
    kicad_mod.append(PolygoneLine(
        polygone=[[x1 + 0.13, y1 + 0.13], [x2, y2 + 0.13]],
        layer='F.SilkS', width=configuration['silk_line_width']))
    body_edge['bottom'] = y1
    bounding_box['bottom'] = y1

    #
    # Upper arcs
    #
    ccx = GuideHoleX1
    ccy = GuideHoleY1
    csx = GuideHoleX1
    csy = -0.85
    kicad_mod.append(Arc(center=[ccx, ccy], start=[csx, csy], angle=180,
        layer='F.Fab', width=configuration['fab_line_width']))
    ccx = GuideHoleX1
    ccy = GuideHoleY1
    csx = -1.61
    csy = -0.72
    kicad_mod.append(Arc(center=[ccx, ccy], start=[csx, csy], angle=180,
        layer='F.SilkS', width=configuration['silk_line_width']))

    #
    # Left lines
    #
    x1 = GuideHoleX1
    y1 = GuideHoleY1 + (GuideHoleY1 - StartFY)
    x2 = GuideHoleX1
    y2 = GuideHoleY2 - (GuideHoleY1 - StartFY)
    x3 = 2
    y3 = -0.5
    kicad_mod.append(PolygoneLine(polygone=[[x1,y1], [x2, -0.5]],
        layer='F.Fab', width=configuration['fab_line_width']))
    kicad_mod.append(PolygoneLine(polygone=[[x2, -0.5], [x2 + 0.5, 0]],
        layer='F.Fab', width=configuration['fab_line_width']))
    kicad_mod.append(PolygoneLine(polygone=[[x2 + 0.5, 0], [x2, 0.5]],
        layer='F.Fab', width=configuration['fab_line_width']))
    kicad_mod.append(PolygoneLine(polygone=[[x2, 0.5], [x2, y2]],
        layer='F.Fab', width=configuration['fab_line_width']))

    kicad_mod.append(PolygoneLine(
        polygone=[[x1 - 0.13, y1 + 0.13], [x2 - 0.13, y2 - 0.13]],
        layer='F.SilkS', width=configuration['silk_line_width']))
    body_edge['left'] = x1

    #
    # Bottom arcs
    #
    ccx = GuideHoleX1
    ccy = GuideHoleY2
    csx = GuideHoleX1
    csy = ((pins - 1) * pitch) + 2.755
    radius = abs(csy - ccy)
    kicad_mod.append(Arc(center=[ccx, ccy], start=[csx, csy], angle=180,
        layer='F.Fab', width=configuration['fab_line_width']))
    bounding_box['left'] = ccx - radius

    ccx = GuideHoleX1
    ccy = GuideHoleY2
    csx = -1.47
    csy = ((pins - 1) * pitch) + 2.755 + 0.13
    kicad_mod.append(Arc(center=[ccx, ccy], start=[csx, csy], angle=170,
        layer='F.SilkS', width=configuration['silk_line_width']))

    # pin 1
    x = body_edge['left'] - 0.3
    m = 0.3

    pin = [
    {'x': x,'y': 0},
    {'x': x-2*m,'y': -m},
    {'x': x-2*m,'y': +m},
    {'x': x,'y': 0},
    ]

    kicad_mod.append(PolygoneLine(polygone=pin,
        width=configuration['silk_line_width'], layer='F.SilkS'))

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
        courtyard={'top':cy1, 'bottom':cy2},
        fp_name=footprint_name, text_y_inside_position='top')

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

    for pins in pins_range:
        generate_one_footprint(pins, configuration)
