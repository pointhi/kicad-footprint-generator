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

draw_inner_details = False

series = "MicroClasp"
series_long = 'MicroClasp Wire-to-Board System'
manufacturer = 'Molex'
orientation = 'V'
number_of_rows = 1


#pins_per_row_per_row per row
pins_per_row_range = range(2,16)

#Molex part number
#n = number of circuits per row
#with boss, suffix = 10
#no boss, suffix = 30
part = "55932-{n:02}{boss}"
variant_params = {
    'no_boss':{
        'boss': False,
        'datasheet': 'http://www.molex.com/pdm_docs/sd/559320530_sd.pdf',
        'part_code': "55932-{n:02}30",
        },
    'boss':{
        'boss': True,
        'datasheet': 'http://www.molex.com/pdm_docs/sd/559320210_sd.pdf',
        'part_code': "55932-{n:02}10",
        }
}

pitch = 2
drill = 0.8
start_pos_x = 0 # Where should pin 1 be located.
pad_to_pad_clearance = 0.8
max_annular_ring = 0.5 #How much copper should be in y direction?
min_annular_ring = 0.15

pad_size = [pitch - pad_to_pad_clearance, drill + 2*max_annular_ring]
if pad_size[0] - drill < 2*min_annular_ring:
    pad_size[0] = drill + 2*min_annular_ring
if pad_size[0] - drill > 2*max_annular_ring:
    pad_size[0] = drill + 2*max_annular_ring

pad_shape=Pad.SHAPE_OVAL
if pad_size[1] == pad_size[0]:
    pad_shape=Pad.SHAPE_CIRCLE



def generate_one_footprint(pins, variant, configuration):
    boss = variant_params[variant]['boss']
    mpn = variant_params[variant]['part_code'].format(n=pins)

    # handle arguments
    orientation_str = configuration['orientation_options'][orientation]
    footprint_name = configuration['fp_name_format_string'].format(man=manufacturer,
        series=series,
        mpn=mpn, num_rows=number_of_rows, pins_per_row=pins, mounting_pad = "",
        pitch=pitch, orientation=orientation_str)

    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription("Molex {:s}, {:s}{:s}, {:d} Pins ({:s}), generated with kicad-footprint-generator".format(series_long,
        mpn, ", with PCB locator" if boss else '',
        pins, variant_params[variant]['datasheet']))
    kicad_mod.setTags(configuration['keyword_fp_string'].format(series=series,
        orientation=orientation_str, man=manufacturer,
        entry=configuration['entry_direction'][orientation]))

    #calculate fp dimensions

    #B = distance between end-point pins
    B = (pins - 1) * pitch
    #A = total connector length
    A = B + 6
    #C = internal length of connector
    C = B + 3

    #T = length of tab

    if pins == 2:
        T = 5
    else:
        T = 6.78

    #wall-thickness w
    w = 0.6

    #corners
    x1 = -(A-B) / 2
    x2 = x1 + A

    y2 = 3
    y1 = y2 - (6.3 if pins == 2 else 5.8)

    #y-pos of tab
    yt = y2 - 6.7
    xt = B/2 - T/2

    body_edge={
        'left':x1,
        'right':x2,
        'bottom':y2,
        'top': y1
        }
    bounding_box = body_edge.copy()
    bounding_box['top']=yt

    out = [
    {'x': B/2, 'y': yt},
    {'x': xt, 'y': yt},
    {'x': xt, 'y': y1},
    {'x': x1, 'y': y1},
    {'x': x1, 'y': y2},
    {'x': B/2, 'y': y2},
    ]
    kicad_mod.append(PolygoneLine(polygone=out,
        layer="F.Fab", width=configuration['fab_line_width']))
    kicad_mod.append(PolygoneLine(polygone=out,x_mirror=B/2,
        layer="F.Fab", width=configuration['fab_line_width']))

    #offset
    o = configuration['silk_fab_offset']
    x1 -= o
    y1 -= o
    x2 += o
    y2 += o
    yt -= o
    xt -= o


    out = [
    {'x': B/2, 'y': yt},
    {'x': xt, 'y': yt},
    {'x': xt, 'y': y1},
    {'x': x1, 'y': y1},
    {'x': x1, 'y': y2},
    {'x': B/2, 'y': y2},
    ]
    kicad_mod.append(PolygoneLine(polygone=out,
        layer="F.SilkS", width=configuration['silk_line_width']))
    kicad_mod.append(PolygoneLine(polygone=out,x_mirror=B/2,
        layer="F.SilkS", width=configuration['silk_line_width']))

    optional_pad_params = {}
    if configuration['kicad4_compatible']:
        optional_pad_params['tht_pad1_shape'] = Pad.SHAPE_RECT
    else:
        optional_pad_params['tht_pad1_shape'] = Pad.SHAPE_ROUNDRECT

    #generate the pads
    kicad_mod.append(PadArray(
        pincount=pins, x_spacing=pitch, type=Pad.TYPE_THT,
        shape=pad_shape, size=pad_size, drill=drill, layers=Pad.LAYERS_THT,
        **optional_pad_params))

    #add PCB locator if needed
    if boss:
        boss_x = B+2
        boss_y = -1.9
        boss_drill = 1.3
        kicad_mod.append(Pad(at=[boss_x, boss_y], size=boss_drill, drill=boss_drill,
            type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE, layers=Pad.LAYERS_NPTH))


    #draw the inner wall
    # Inner details are incorrect. I could not be bothered to fix them.
    # wall = [
    # {'x': B/2, 'y': yt + 2*w},
    # {'x': B/2 - pitch / 2, 'y': yt + 2*w},
    # {'x': B/2 - pitch / 2, 'y': yt + w},
    # {'x': B/2 - T/2 + w, 'y': yt + w},
    # {'x': B/2 - T/2 + w, 'y': y1 + 2*w},
    # {'x': -0.25, 'y': y1 + 2*w},
    # {'x': -0.25, 'y': y1 + w},
    # {'x': -(C-B)/2, 'y': y1 + w},
    # {'x': -(C-B)/2, 'y': y2 - 3*w},
    # {'x': x1+w, 'y': y2 - 3*w},
    # {'x': x1+w, 'y': y2 - w},
    # {'x': B/2, 'y': y2 - w},
    # ]
    #
    # kicad_mod.append(PolygoneLine(polygone=wall,
    #     layer="F.SilkS", width=configuration['silk_line_width']))
    # kicad_mod.append(PolygoneLine(polygone=wall, x_mirror=B/2,
    #     layer="F.SilkS", width=configuration['silk_line_width']))

    #pin-1 marker
    y =  3.5
    m = 0.3

    p1m_sl = 2
    p1m_off = o + 0.3
    pin = [
        {'x': body_edge['left'] - p1m_off,'y': body_edge['bottom']-p1m_sl},
        {'x': body_edge['left'] - p1m_off,'y': body_edge['bottom']+p1m_off},
        {'x': body_edge['left'] + p1m_sl,'y': body_edge['bottom']+p1m_off},
    ]

    kicad_mod.append(PolygoneLine(polygone=pin,
        layer="F.SilkS", width=configuration['silk_line_width']))

    p1m_sl = 1

    pin = [
        {'x': -p1m_sl/2,'y': body_edge['bottom']},
        {'x': 0,'y': body_edge['bottom'] - p1m_sl/sqrt(2)},
        {'x': p1m_sl/2,'y': body_edge['bottom']},
    ]
    kicad_mod.append(PolygoneLine(polygone=pin,
        layer="F.Fab", width=configuration['fab_line_width']))

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

    for variant in variant_params:
        for pins_per_row in pins_per_row_range:
            generate_one_footprint(pins_per_row, variant, configuration)
