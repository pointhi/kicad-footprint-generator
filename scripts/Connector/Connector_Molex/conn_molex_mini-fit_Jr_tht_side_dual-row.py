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

series = "Mini-Fit_Jr"
series_long = 'Mini-Fit Jr. Power Connectors'
manufacturer = 'Molex'
orientation = 'H'
number_of_rows = 2


#pins_per_row_per_row per row
pins_per_row_range = range(1,13)

#Molex part number
#n = number of circuits per row
variant_params = {
    'peg':{
        'mount_pins': 'plastic_peg',
        'descriptive_name': 'Snap-in Plastic Peg PCB Lock',
        'datasheet': 'http://www.molex.com/pdm_docs/sd/039300020_sd.pdf',
        'part_code': {'mpn':"39-30-0{n:02d}0",'eng_num':"5569-{n:02}A2"},
        },
    'flange':{
        'mount_pins': 'screw_flange',
        'descriptive_name': 'PCB Mounting Flange',
        'datasheet': 'http://www.molex.com/pdm_docs/sd/039291047_sd.pdf',
        'part_code': {'mpn':"39-29-4{n:02d}9",'eng_num':"5569-{n:02}A1"},
        }
}

pitch = 4.2
drill = 1.8
start_pos_x = 0 # Where should pin 1 be located.
pad_to_pad_clearance = 1.5
max_annular_ring = 0.95
min_annular_ring = 0.15


row = 5.5

pad_size = [pitch - pad_to_pad_clearance, row - pad_to_pad_clearance]
if pad_size[0] - drill < 2*min_annular_ring:
    pad_size[0] = drill + 2*min_annular_ring
if pad_size[0] - drill > 2*max_annular_ring:
    pad_size[0] = drill + 2*max_annular_ring

if pad_size[1] - drill < 2*min_annular_ring:
    pad_size[1] = drill + 2*min_annular_ring
if pad_size[1] - drill > 2*max_annular_ring:
    pad_size[1] = drill + 2*max_annular_ring

pad_shape = Pad.SHAPE_OVAL
if pad_size[0] == pad_size[1]:
    pad_shape = Pad.SHAPE_CIRCLE


def generate_one_footprint(pins_per_row, variant, configuration):
    silk_pad_off = configuration['silk_pad_clearance']+configuration['silk_line_width']/2

    mpn = variant_params[variant]['part_code']['mpn'].format(n=pins_per_row*2)
    old_mpn = variant_params[variant]['part_code']['eng_num'].format(n=pins_per_row*2)

    # handle arguments
    orientation_str = configuration['orientation_options'][orientation]
    footprint_name = configuration['fp_name_format_string'].format(man=manufacturer,
        series=series,
        mpn=old_mpn, num_rows=number_of_rows, pins_per_row=pins_per_row, mounting_pad = "",
        pitch=pitch, orientation=orientation_str)

    kicad_mod = Footprint(footprint_name)
    descr_format_str = "Molex {:s}, old mpn/engineering number: {:s}, example for new mpn: {:s}, {:d} Pins per row, Mounting: {:s} ({:s}), generated with kicad-footprint-generator"
    kicad_mod.setDescription(descr_format_str.format(
        series_long, old_mpn, mpn, pins_per_row,
        variant_params[variant]['descriptive_name'], variant_params[variant]['datasheet']))
    tags = configuration['keyword_fp_string'].format(series=series,
        orientation=orientation_str, man=manufacturer,
        entry=configuration['entry_direction'][orientation])
    tags += variant_params[variant]['mount_pins']
    kicad_mod.setTags(tags)

    peg = variant_params[variant]['mount_pins'] == 'plastic_peg'

    #calculate fp dimensions

    #connector length
    A = pins_per_row * pitch + 1.2

    #pin centers
    B = (pins_per_row - 1) * pitch

    #plasic pin-lock
    C = A + 4

    #connector width
    W = 9.6

    #corner positions
    x1 = -(A-B)/2
    x2 = x1 + A

    y1 = -7.3 - 6.6
    y2 = y1 + 12.8
    body_edge={
        'left':x1,
        'right':x2,
        'bottom':y2,
        'top': y1
        }
    bounding_box = body_edge.copy()
    bounding_box['bottom'] = row + pad_size[1]/2

    #generate the pads
    optional_pad_params = {}
    if configuration['kicad4_compatible']:
        optional_pad_params['tht_pad1_shape'] = Pad.SHAPE_RECT
    else:
        optional_pad_params['tht_pad1_shape'] = Pad.SHAPE_ROUNDRECT

    for row_idx in range(2):
        kicad_mod.append(PadArray(
            pincount=pins_per_row, initial=row_idx*pins_per_row+1,
            start=[0, row_idx*row], x_spacing=pitch,
            type=Pad.TYPE_THT, shape=pad_shape,
            size=pad_size, drill=drill, layers=Pad.LAYERS_THT,
            **optional_pad_params))


    off = configuration['silk_fab_offset']
    #draw the 'peg' version
    #http://www.molex.com/pdm_docs/sd/026013127_sd.pdf
    #draw the outline of the shape
    kicad_mod.append(RectLine(start=[x1,y1],end=[x2,y2],
        layer='F.Fab', width=configuration['fab_line_width']))

    if peg:
        loc = 3.00
        if pins_per_row > 2: # two mounting holes
            kicad_mod.append(Pad(at=[0,-7.3],type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE, size=loc,drill=loc, layers=Pad.LAYERS_NPTH))
            #kicad_mod.append(Circle(center=[0,-7.3],radius=loc/2+0.1))
            kicad_mod.append(Pad(at=[B,-7.3],type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE, size=loc,drill=loc, layers=Pad.LAYERS_NPTH))
            #kicad_mod.append(Circle(center=[B,-7.3],radius=loc/2+0.1))
        else: #single hole
            kicad_mod.append(Pad(at=[B/2,-7.3],type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE, size=loc,drill=loc, layers=Pad.LAYERS_NPTH))
            #kicad_mod.append(Circle(center=[B/2,-7.3],radius=loc/2+0.1))


        #draw the outline of the connector on the silkscreen
        poly = [
        {'x': -2,'y': y2+off},
        {'x': x1-off,'y': y2+off},
        {'x': x1-off,'y': y1-off},
        {'x': B/2,'y': y1-off},
        ]

        kicad_mod.append(PolygoneLine(polygone=poly,
            layer='F.SilkS', width=configuration['silk_line_width']))
        kicad_mod.append(PolygoneLine(polygone=poly, x_mirror=B/2,
            layer='F.SilkS', width=configuration['silk_line_width']))

    #draw the 'screw' version
    #http://www.molex.com/pdm_docs/sd/039291027_sd.pdf
    else:
        loc = 3.2
        kicad_mod.append(Pad(at=[-4.5,  -4.2],type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE, size=loc, drill=loc, layers=Pad.LAYERS_NPTH))
        kicad_mod.append(Pad(at=[B+4.5, -4.2],type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE, size=loc, drill=loc, layers=Pad.LAYERS_NPTH))
        bounding_box['left'] = -15.4/2
        bounding_box['right'] = B + 15.4/2

        #draw the connector outline on silkscreen layer
        poly = [
        {'x': x1,'y': y2-6.2},
        {'x': -15.4/2,'y': y2-6.2},
        {'x': -15.4/2,'y': y2},
        {'x': x1,'y': y2}
        ]

        kicad_mod.append(PolygoneLine(polygone=poly,
            layer='F.Fab', width=configuration['fab_line_width']))
        kicad_mod.append(PolygoneLine(polygone=poly, x_mirror=B/2,
            layer='F.Fab', width=configuration['fab_line_width']))

        poly = [
        {'x': B/2,'y': y1-off},
        {'x': x1-off,'y': y1-off},
        {'x': x1-off,'y': y2-6.2-off},
        {'x': -15.4/2 - off,'y': y2-6.2-off},
        {'x': -15.4/2 - off,'y': y2+off},
        {'x': -2,'y': y2+off},
        ]

        kicad_mod.append(PolygoneLine(polygone=poly))
        kicad_mod.append(PolygoneLine(polygone=poly, x_mirror=B/2,
            layer='F.SilkS', width=configuration['silk_line_width']))





    #draw the pins_per_row on the Silkscreen layer
    o = pad_size[1]/2+silk_pad_off
    w = 0.3
    for i in range(pins_per_row):
        x = i * pitch
        ya = o
        yb = row - o
        kicad_mod.append(Line(start=[x-w,ya],end=[x-w,yb],
            layer='F.SilkS', width=configuration['silk_line_width']))
        kicad_mod.append(Line(start=[x+w,ya],end=[x+w,yb],
            layer='F.SilkS', width=configuration['silk_line_width']))

    #draw lines between each pin
    off = 0.1
    for i in range(pins_per_row-1):
        xa = i * pitch + pad_size[0] / 2 + silk_pad_off
        xb = (i+1) * pitch - pad_size[0] / 2 - silk_pad_off

        kicad_mod.append(Line(start=[xa,y2+off],end=[xb,y2+off],
            layer='F.SilkS', width=configuration['silk_line_width']))

    #pin-1 marker
    x =  -2
    m = 0.3

    arrow = [
    {'x': x,'y': 0},
    {'x': x-2*m,'y': +m},
    {'x': x-2*m,'y': -m},
    {'x': x,'y': 0},
    ]

    kicad_mod.append(PolygoneLine(polygone=arrow,
        layer='F.SilkS', width=configuration['silk_line_width']))


    sl = 2
    pin = [
        {'x': -sl/2, 'y': body_edge['bottom']},
        {'x': 0, 'y': body_edge['bottom']-sl/sqrt(2)},
        {'x': sl/2, 'y': body_edge['bottom']},
    ]
    kicad_mod.append(PolygoneLine(polygone=pin,
        width=configuration['fab_line_width'], layer='F.Fab'))

    ########################### CrtYd #################################
    CrtYd_offset = configuration['courtyard_offset']['connector']
    CrtYd_grid = configuration['courtyard_grid']

    cx1 = roundToBase(bounding_box['left'] - CrtYd_offset, CrtYd_grid)
    cy1 = roundToBase(bounding_box['top'] - CrtYd_offset, CrtYd_grid)

    cx2 = roundToBase(bounding_box['right'] + CrtYd_offset, CrtYd_grid)
    cy2 = roundToBase(bounding_box['bottom'] + CrtYd_offset, CrtYd_grid)

    if peg:
        kicad_mod.append(RectLine(
            start=[cx1, cy1], end=[cx2, cy2],
            layer='F.CrtYd', width=configuration['courtyard_line_width']))
    else:
        cxb_left = roundToBase(body_edge['left'] - CrtYd_offset, CrtYd_grid)
        cxp_left = roundToBase(-pad_size[0]/2 - CrtYd_offset, CrtYd_grid)

        cyb_bottom = roundToBase(body_edge['bottom'] + CrtYd_offset, CrtYd_grid)
        cyb_mount_top = roundToBase(body_edge['bottom'] -6.2 - CrtYd_offset, CrtYd_grid)

        poly_crtyd = [
                {'x': B/2, 'y': cy1},
                {'x': cxb_left, 'y': cy1},
                {'x': cxb_left, 'y': cyb_mount_top},
                {'x': cx1, 'y': cyb_mount_top},
                {'x': cx1, 'y': cyb_bottom},
                {'x': cxp_left, 'y': cyb_bottom},
                {'x': cxp_left, 'y': cy2},
                {'x': B/2, 'y': cy2},
            ]
        kicad_mod.append(PolygoneLine(
            polygone=poly_crtyd,
            layer='F.CrtYd', width=configuration['courtyard_line_width']))
        kicad_mod.append(PolygoneLine(
            polygone=poly_crtyd, x_mirror=B/2 if B/2 != 0 else 0.000000001,
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
