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

series = ""
series_long = 'LSHM 0.50 mm Razor Beam High-Speed Hermaphroditic Terminal/Socket Strip'
manufacturer = 'Samtec'
orientation = 'V'
number_of_rows = 2
datasheet = 'http://suddendocs.samtec.com/prints/lshm-1xx-xx.x-x-dv-a-x-x-tr-footprint.pdf'

#pins_per_row per row
pins_per_row_range = [5,10,20,30,40,50]

#Molex part number
#n = number of circuits per row
part_code = "LSHM-1{n:02d}-xx.x-x-DV-{shield:s}"

variant_params = {
    'shileded': {
        'mpn_option': 'S',
        'shield_pad': True,
    },
    'plain': {
        'mpn_option': 'N',
        'shield_pad': False,
    }
}

pitch = 0.5

pad_size = [0.3, 1.5]
boss_drill = 1.45

shield_pad_drill = 1
shield_pad_size = 1.5

pin_number_shield = "SH"

def generate_one_footprint(pins_per_row, params, configuration):
    mpn = part_code.format(n=pins_per_row, shield=params['mpn_option'])

    CrtYd_off = configuration['courtyard_offset']['connector']
    CrtYd_grid = configuration['courtyard_grid']
    off = configuration['silk_fab_offset']
    pad_silk_off = configuration['silk_pad_clearance'] + configuration['silk_line_width']/2
    body_edge = {}
    bounding_box = {}

    # handle arguments
    orientation_str = configuration['orientation_options'][orientation]
    if params['shield_pad']:
        footprint_name = configuration['fp_name_format_string_shielded'].format(man=manufacturer,
            series=series,
            mpn=mpn, num_rows=number_of_rows, pins_per_row=pins_per_row,
            pitch=pitch, orientation=orientation_str, shield_pins=1)
    else:
    footprint_name = configuration['fp_name_format_string'].format(man=manufacturer,
        series=series,
        mpn=mpn, num_rows=number_of_rows, pins_per_row=pins_per_row, mounting_pad = "",
        pitch=pitch, orientation=orientation_str)

    footprint_name = footprint_name.replace('__','_')

    kicad_mod = Footprint(footprint_name)
    kicad_mod.setAttribute('smd')
    kicad_mod.setDescription("Molex {:s}, {:s}, {:d} Pins per row ({:s}), generated with kicad-footprint-generator".format(series_long, mpn, pins_per_row, datasheet))
    kicad_mod.setTags(configuration['keyword_fp_string'].format(series=series,
        orientation=orientation_str, man=manufacturer,
        entry=configuration['entry_direction'][orientation]))

    A = (pins_per_row-1)*pitch
    B = A + 2.5
    C = A + 5.45
    D = A + 6.75
    E = A + 5.2

    pad_to_pad_inside = 1.95+0.25
    pad_y = (pad_to_pad_inside + pad_size[1])/2

    boss_x = B/2
    boss_y = -pad_y + pad_size[1]/2 + 0.25

    shield_pad_x = C/2
    shield_pad_y = boss_y + 2

    body_chamfer = 0.3


    body_edge['left'] = -D/2 if params['shield_pad'] else -E/2
    body_edge['right'] = -body_edge['left']
    body_edge['top'] = -4.98/2
    body_edge['bottom'] = -body_edge['top']

    bounding_box['left'] = (-shield_pad_x - shield_pad_size/2) if params['shield_pad'] else body_edge['left']
    bounding_box['right'] = -bounding_box['left']
    bounding_box['top'] = -pad_y - pad_size[1]/2
    bounding_box['bottom'] = -bounding_box['top']


    ################################ Pads #####################################

    kicad_mod.append(PadArray(initial=1, increment=2,
        center=[0, -pad_y], x_spacing=pitch, pincount=pins_per_row,
        size=pad_size, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, layers=Pad.LAYERS_SMT))
    kicad_mod.append(PadArray(initial=2, increment=2,
        center=[0, pad_y], x_spacing=pitch, pincount=pins_per_row,
        size=pad_size, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, layers=Pad.LAYERS_SMT))

    kicad_mod.append(Pad(number ='""', type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                        at=[boss_x, boss_y],
                        size=boss_drill, drill=boss_drill,
                        layers=Pad.LAYERS_NPTH))
    kicad_mod.append(Pad(number ='""', type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                        at=[-boss_x, boss_y],
                        size=boss_drill, drill=boss_drill,
                        layers=Pad.LAYERS_NPTH))

    if params['shield_pad']:
        kicad_mod.append(Pad(number = pin_number_shield,
                            type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
                            at=[shield_pad_x, shield_pad_y],
                            size=shield_pad_size, drill=shield_pad_drill,
                            layers=Pad.LAYERS_THT))
        kicad_mod.append(Pad(number = pin_number_shield,
                            type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
                            at=[-shield_pad_x, shield_pad_y],
                            size=shield_pad_size, drill=shield_pad_drill,
                            layers=Pad.LAYERS_THT))

    ########################### Outline ################################
    poly_fab = [
        {'x': 0, 'y': body_edge['top']},
        {'x': body_edge['left']+body_chamfer, 'y': body_edge['top']},
        {'x': body_edge['left'], 'y': body_edge['top']+body_chamfer},
        {'x': body_edge['left'], 'y': body_edge['bottom']-body_chamfer},
        {'x': body_edge['left']+body_chamfer, 'y': body_edge['bottom']},
        {'x': 0, 'y': body_edge['bottom']}
    ]
    kicad_mod.append(PolygoneLine(polygone=poly_fab,
        layer='F.Fab', width=configuration['fab_line_width']))
    kicad_mod.append(PolygoneLine(polygone=poly_fab, x_mirror=0,
        layer='F.Fab', width=configuration['fab_line_width']))

    pad_x_outside_edge = A/2 + pad_size[0]/2 + pad_silk_off
    if not params['shield_pad']:
        poly_silk = [
            {'x': -pad_x_outside_edge, 'y': body_edge['top']-off},
            {'x': body_edge['left']+body_chamfer-off, 'y': body_edge['top']-off},
            {'x': body_edge['left']-off, 'y': body_edge['top']+body_chamfer-off},
            {'x': body_edge['left']-off, 'y': body_edge['bottom']-body_chamfer+off},
            {'x': body_edge['left']+body_chamfer-off, 'y': body_edge['bottom']+off},
            {'x': -pad_x_outside_edge, 'y': body_edge['bottom']+off}
        ]
        kicad_mod.append(PolygoneLine(polygone=poly_silk,
            layer='F.SilkS', width=configuration['silk_line_width']))
        kicad_mod.append(PolygoneLine(polygone=poly_silk, x_mirror=0,
            layer='F.SilkS', width=configuration['silk_line_width']))

    else:
        r = (shield_pad_size/2 + pad_silk_off)
        x = (D-C)/2
        dy = sqrt(r**2 - x**2)
        poly_silk_top = [
            {'x': -pad_x_outside_edge, 'y': body_edge['top']-off},
            {'x': body_edge['left']+body_chamfer-off, 'y': body_edge['top']-off},
            {'x': body_edge['left']-off, 'y': body_edge['top']+body_chamfer-off},
            {'x': body_edge['left']-off, 'y': shield_pad_y-dy},
        ]
        kicad_mod.append(PolygoneLine(polygone=poly_silk_top,
            layer='F.SilkS', width=configuration['silk_line_width']))
        kicad_mod.append(PolygoneLine(polygone=poly_silk_top, x_mirror=0,
            layer='F.SilkS', width=configuration['silk_line_width']))

        poly_silk_bottom = [
            {'x': body_edge['left']-off, 'y': shield_pad_y+dy},
            {'x': body_edge['left']-off, 'y': body_edge['bottom']-body_chamfer+off},
            {'x': body_edge['left']+body_chamfer-off, 'y': body_edge['bottom']+off},
            {'x': -pad_x_outside_edge, 'y': body_edge['bottom']+off}
        ]
        kicad_mod.append(PolygoneLine(polygone=poly_silk_bottom,
            layer='F.SilkS', width=configuration['silk_line_width']))
        kicad_mod.append(PolygoneLine(polygone=poly_silk_bottom, x_mirror=0,
            layer='F.SilkS', width=configuration['silk_line_width']))

    ########################### Pin 1 #################################
    p1s_sl = 0.4
    p1s_y = -pad_y - pad_size[1]/2 - pad_silk_off
    p1_x = -A/2
    p1s_poly = [
        {'x': p1_x, 'y':p1s_y},
        {'x': p1_x-p1s_sl/2, 'y':p1s_y-p1s_sl/sqrt(2)},
        {'x': p1_x+p1s_sl/2, 'y':p1s_y-p1s_sl/sqrt(2)},
        {'x': p1_x, 'y':p1s_y}
    ]
    kicad_mod.append(PolygoneLine(polygone=p1s_poly,
        layer='F.SilkS', width=configuration['silk_line_width']))

    p1f_sl = 2*pitch
    p1f_poly = [
        {'x': p1_x-p1f_sl/2, 'y':body_edge['top']},
        {'x': p1_x, 'y':body_edge['top']+p1f_sl/sqrt(2)},
        {'x': p1_x+p1f_sl/2, 'y':body_edge['top']}
    ]
    kicad_mod.append(PolygoneLine(polygone=p1f_poly,
        layer='F.Fab', width=configuration['fab_line_width']))

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
        fp_name=footprint_name, text_y_inside_position='center')

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
    for variant in variant_params:
        for pins_per_row in pins_per_row_range:
            generate_one_footprint(pins_per_row, variant_params[variant], configuration)
