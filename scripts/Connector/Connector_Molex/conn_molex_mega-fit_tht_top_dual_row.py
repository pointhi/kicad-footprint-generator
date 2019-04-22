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

series = "Mega-Fit"
series_long = 'Mega-Fit Power Connectors'
manufacturer = 'Molex'
orientation = 'V'
number_of_rows = 2


#pins_per_row_per_row per row
pins_per_row_range = [1, 2, 3, 4, 5, 6]

#Molex part number
#n = number of circuits per row
variant_params = {
    'boss':{
        'mount_pins': False,
        'datasheet': 'http://www.molex.com/pdm_docs/sd/768290102_sd.pdf',
        'part_code': "76829-01{n:02d}",
        'alternative_codes': [
            "172065-02{n:02d}",
            "172065-03{n:02d}"
            ]
        },
    'mount_pins':{
        'mount_pins': True,
        'datasheet': 'http://www.molex.com/pdm_docs/sd/768290004_sd.pdf',
        'part_code': "76829-00{n:02d}",
        'alternative_codes': [
            "172065-00{n:02d}",
            "172065-10{n:02d}"
            ]
        }
}

pitch = 5.7
drill = 1.8
start_pos_x = 0 # Where should pin 1 be located.
pad_to_pad_clearance = 1.75
max_annular_ring = 0.95 #How much copper should be in y direction?
min_annular_ring = 0.15


row = 5.7

size = row - pad_to_pad_clearance
if size - drill < 2*min_annular_ring:
    size = drill + 2*min_annular_ring
if size - drill > 2*max_annular_ring:
    size = drill + 2*max_annular_ring



def generate_one_footprint(pins_per_row, variant, configuration):
    mpn = variant_params[variant]['part_code'].format(n=pins_per_row*2)
    alt_mpn = [code.format(n=pins_per_row*2) for code in variant_params[variant]['alternative_codes']]

    # handle arguments
    orientation_str = configuration['orientation_options'][orientation]
    footprint_name = configuration['fp_name_format_string'].format(man=manufacturer,
        series=series,
        mpn=mpn, num_rows=number_of_rows, pins_per_row=pins_per_row, mounting_pad = "",
        pitch=pitch, orientation=orientation_str)

    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription("Molex {:s}, {:s} (compatible alternatives: {:s}), {:d} Pins per row ({:s}), generated with kicad-footprint-generator".format(series_long, mpn, ', '.join(alt_mpn), pins_per_row, variant_params[variant]['datasheet']))
    kicad_mod.setTags(configuration['keyword_fp_string'].format(series=series,
        orientation=orientation_str, man=manufacturer,
        entry=configuration['entry_direction'][orientation]))

    #calculate fp dimensions

    #connector length
    if pins_per_row == 1:
        A = 8.35
    else:
        A = pins_per_row * pitch + 0.65

    B = A + 7.04

    #pin centers
    P = (pins_per_row - 1) * pitch

    #plasic pin-lock centre-distance
    C = A + 3.99
    #print('A: {}, B: {}, C: {}'.format(A,B,C))
    #connector width
    W = 12.48

    #corner positions
    x1 = -(A-P)/2
    x2 = x1 + A

    y2 = 3.47 + row
    y1 = y2 -W

    #tab length
    tab_l = 3.4
    #tab width
    tab_w = 1.55

    body_edge={
        'left':x1,
        'right':x2,
        'bottom':y2,
        'top': y1
        }
    bounding_box = body_edge.copy()
    bounding_box['bottom'] = y2 + tab_w

    optional_pad_params = {}
    if configuration['kicad4_compatible']:
        optional_pad_params['tht_pad1_shape'] = Pad.SHAPE_RECT
    else:
        optional_pad_params['tht_pad1_shape'] = Pad.SHAPE_ROUNDRECT

    #generate the pads
    for row_idx in range(2):
        kicad_mod.append(PadArray(
            pincount=pins_per_row, initial=row_idx*pins_per_row+1,
            start=[0, row_idx*row], x_spacing=pitch, type=Pad.TYPE_THT,
            shape=Pad.SHAPE_CIRCLE, size=size, drill=drill, layers=Pad.LAYERS_THT,
            **optional_pad_params))

    off = configuration['silk_fab_offset']
    silk_pad_off = configuration['silk_pad_clearance'] + configuration['silk_line_width']/2

    if variant_params[variant]['mount_pins']:
        #add PCB locators
        loc = 3.00
        offset = -0.325

        lx1 = P/2 - C/2
        lx2 = P/2 + C/2

        mounting_pin_y = row - offset

        kicad_mod.append(Pad(at=[lx1, mounting_pin_y],type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE, size=loc,drill=loc, layers=Pad.LAYERS_NPTH))
        kicad_mod.append(Pad(at=[lx2, mounting_pin_y],type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE, size=loc,drill=loc, layers=Pad.LAYERS_NPTH))

        #draw outline around the PCB locators
        #arc distance from pin
        mount_pin_radius = (B/2 - C/2)
        bounding_box['left'] = P/2 - B/2
        bounding_box['right'] = P/2 + B/2

        ######################## Fab ############################

        kicad_mod.append(Arc(center=[lx1,mounting_pin_y],
            start=[lx1,mounting_pin_y+mount_pin_radius], angle=180,
            layer='F.Fab', width=configuration['fab_line_width']))

        kicad_mod.append(Line(start=[lx1,mounting_pin_y-mount_pin_radius],
            end=[x1,mounting_pin_y-mount_pin_radius],
            layer='F.Fab', width=configuration['fab_line_width']))
        kicad_mod.append(Line(start=[lx1,mounting_pin_y+mount_pin_radius],
            end=[x1,mounting_pin_y+mount_pin_radius],
            layer='F.Fab', width=configuration['fab_line_width']))


        kicad_mod.append(Arc(center=[lx2,mounting_pin_y],
            start=[lx2,mounting_pin_y-mount_pin_radius], angle=180,
            layer='F.Fab', width=configuration['fab_line_width']))

        kicad_mod.append(Line(start=[lx2,mounting_pin_y-mount_pin_radius],
            end=[x2,mounting_pin_y-mount_pin_radius],
            layer='F.Fab', width=configuration['fab_line_width']))
        kicad_mod.append(Line(start=[lx2,mounting_pin_y+mount_pin_radius],
            end=[x2,mounting_pin_y+mount_pin_radius],
            layer='F.Fab', width=configuration['fab_line_width']))

        ######################## Silk ############################
        mount_pin_radius = loc/2 + silk_pad_off
        kicad_mod.append(Arc(center=[lx1,mounting_pin_y],
            start=[lx1,mounting_pin_y+mount_pin_radius], angle=180,
            layer='F.SilkS', width=configuration['silk_line_width']))

        kicad_mod.append(Line(start=[lx1,mounting_pin_y-mount_pin_radius],
            end=[x1-off,mounting_pin_y-mount_pin_radius],
            layer='F.SilkS', width=configuration['silk_line_width']))
        kicad_mod.append(Line(start=[lx1,mounting_pin_y+mount_pin_radius],
            end=[x1-off,mounting_pin_y+mount_pin_radius],
            layer='F.SilkS', width=configuration['silk_line_width']))


        kicad_mod.append(Arc(center=[lx2,mounting_pin_y],
            start=[lx2,mounting_pin_y-mount_pin_radius], angle=180,
            layer='F.SilkS', width=configuration['silk_line_width']))

        kicad_mod.append(Line(start=[lx2,mounting_pin_y-mount_pin_radius],
            end=[x2+off,mounting_pin_y-mount_pin_radius],
            layer='F.SilkS', width=configuration['silk_line_width']))
        kicad_mod.append(Line(start=[lx2,mounting_pin_y+mount_pin_radius],
            end=[x2+off,mounting_pin_y+mount_pin_radius],
            layer='F.SilkS', width=configuration['silk_line_width']))
    else:
        #add PCB locators
        boss_drill = 1.8

        boss_x = (pins_per_row-1) * pitch + (3.48 if pins_per_row == 1 else 2.48)
        boss_y = row + 2.77

        kicad_mod.append(Pad(at=[boss_x, boss_y],type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
            size=boss_drill, drill=boss_drill, layers=Pad.LAYERS_NPTH))

    #draw the outline of the shape
    p1m_sl = 1
    kicad_mod.append(PolygoneLine(polygone=[
            {'x': body_edge['left'] + p1m_sl, 'y': body_edge['top']},
            {'x': body_edge['left'], 'y': body_edge['top'] +p1m_sl},
            {'x': body_edge['left'], 'y': body_edge['bottom']},
            {'x': body_edge['right'], 'y': body_edge['bottom']},
            {'x': body_edge['right'], 'y': body_edge['top']},
            {'x': body_edge['left'] + p1m_sl, 'y': body_edge['top']}
        ],
        layer='F.Fab', width=configuration['fab_line_width']))

    #draw the outline of the tab
    kicad_mod.append(PolygoneLine(polygone=[
        {'x': P/2 - tab_l/2,'y': y2},
        {'x': P/2 - tab_l/2,'y': y2 + tab_w},
        {'x': P/2 + tab_l/2,'y': y2 + tab_w},
        {'x': P/2 + tab_l/2,'y': y2},
    ], layer='F.Fab', width=configuration['fab_line_width']))


    #draw the outline of the connector on the silkscreen

    outline = [
    {'x': P/2,'y': y1-off},
    {'x': x1-off,'y': y1-off},
    {'x': x1-off,'y': y2+off},
    {'x': P/2 - tab_l/2 - off,'y': y2+off},
    {'x': P/2 - tab_l/2 - off,'y': y2 + off + tab_w},
    {'x': P/2, 'y': y2 + off + tab_w},
    ]

    kicad_mod.append(PolygoneLine(polygone=outline,
        layer='F.SilkS', width=configuration['silk_line_width']))
    if variant_params[variant]['mount_pins']:
        kicad_mod.append(PolygoneLine(polygone=outline, x_mirror=P/2,
            layer='F.SilkS', width=configuration['silk_line_width']))
    else:
        outline1 = outline[:2]
        outline1.append({'x': outline[2]['x'], 'y': boss_y - boss_drill/2 - silk_pad_off})
        kicad_mod.append(PolygoneLine(polygone=outline1, x_mirror=P/2,
            layer='F.SilkS', width=configuration['silk_line_width']))

        outline2 = outline[2:]
        outline2[0]['x'] = P - boss_x + boss_drill/2 + silk_pad_off # outline contains the mirrored version
        kicad_mod.append(PolygoneLine(polygone=outline2, x_mirror=P/2,
            layer='F.SilkS', width=configuration['silk_line_width']))


    #draw square around each pin
    if draw_inner_details:
        for i in range(pins_per_row):
            for j in range(2):
                x = i * pitch
                y = j * row
                s = 0.4 * pitch
                kicad_mod.append(RectLine(start=[x-s,y-s],end=[x+s,y+s], layer='F.Fab', width=configuration['fab_line_width']))

    #pin-1 marker
    p1m_off = 0.3 + off
    p1m_sl = 2
    pin = [
        {'x': body_edge['left'] - p1m_off,'y': body_edge['top'] + p1m_sl},
        {'x': body_edge['left'] - p1m_off,'y': body_edge['top'] - p1m_off},
        {'x': body_edge['left'] + p1m_sl,'y': body_edge['top'] - p1m_off},
    ]

    kicad_mod.append(PolygoneLine(polygone=pin, layer='F.SilkS', width=configuration['silk_line_width']))

    ########################### CrtYd #################################
    cx1 = roundToBase(bounding_box['left']-configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])
    cy1 = roundToBase(bounding_box['top']-configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])

    cx2 = roundToBase(bounding_box['right']+configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])
    cy2 = roundToBase(bounding_box['bottom'] + configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])

    if variant_params[variant]['mount_pins']:
        cx3 = roundToBase(body_edge['left']-configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])
        cx4 = roundToBase(body_edge['right']+configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])
        mount_pin_radius = (B/2 - C/2)
        cy3=roundToBase(mounting_pin_y - mount_pin_radius - configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])

        poly_crtyd = [
            {'x': cx3, 'y': cy1},
            {'x': cx3, 'y': cy3},
            {'x': cx1, 'y': cy3},
            {'x': cx1, 'y': cy2},
            {'x': cx2, 'y': cy2},
            {'x': cx2, 'y': cy3},
            {'x': cx4, 'y': cy3},
            {'x': cx4, 'y': cy1},
            {'x': cx3, 'y': cy1}
        ]
        kicad_mod.append(PolygoneLine(polygone=poly_crtyd,
            layer='F.CrtYd', width=configuration['courtyard_line_width']))
    else:
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
