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
orientation = 'V'

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
        'datasheet': "http://www.molex.com/pdm_docs/sd/1053101208_sd.pdf",
        'mpn': "105310-xx{n:02}"
    },
    'single':{
        'number_of_rows': 1,
        'datasheet': 'http://www.molex.com/pdm_docs/sd/1053091203_sd.pdf',
        'mpn': "105309-xx{n:02}"
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
    W = params['number_of_rows'] * pitch_row + 0.98

    #locating pin position
    if pins in [3,5,7]:
        C = B/2 - 1.25
    else:
        C = B/2

    #corner positions for plastic housing outline
    y1 = -(A-B)/2
    y2 = y1 + A

    x2 = (params['number_of_rows'] - 1)* pitch_row+1.74
    x1 = x2 - W

    TL = 5.2
    TW = 2.86

    off = configuration['silk_fab_offset']
    pad_silk_off = configuration['silk_pad_clearance'] + configuration['silk_line_width']/2

    body_edge={
        'left':x1,
        'right':x2,
        'bottom':y2,
        'top': y1
        }
    bounding_box = body_edge.copy()

    bounding_box['left'] = body_edge['left']-TW

    pad_silk_off = configuration['silk_pad_clearance'] + configuration['silk_line_width']/2

    #generate the pads
    if pins <= 3:
        if configuration['kicad4_compatible']:
            kicad_mod.append(Pad(number=1, at=[0, 0],
                size=pad_size, drill=drill,
                type=Pad.TYPE_THT, shape=Pad.SHAPE_OVAL, layers=Pad.LAYERS_THT))

            kicad_mod.append(Pad(number=1, at=[0, -pad_size[1]/4],
                size=[pad_size[0],pad_size[1]/2],
                type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, layers=['F.Cu', 'F.Mask']))
            kicad_mod.append(Pad(number=1, at=[0, -pad_size[1]/4],
                size=[pad_size[0],pad_size[1]/2],
                type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, layers=['B.Cu', 'B.Mask']))

        else:
            kicad_mod.append(ChamferedPad(number=1, at=[0, 0],
                size=pad_size, drill=drill,
                type=Pad.TYPE_THT, shape=Pad.SHAPE_OVAL, layers=Pad.LAYERS_THT,
                chamfer_size=0.4, radius_ratio=0.25, maximum_radius=0.25,
                corner_selection=CornerSelection({CornerSelection.BOTTOM_LEFT:True})))

    optional_pad_params = {}
    if configuration['kicad4_compatible']:
        optional_pad_params['tht_pad1_shape'] = Pad.SHAPE_RECT
    else:
        optional_pad_params['tht_pad1_shape'] = Pad.SHAPE_ROUNDRECT

    for r in range(params['number_of_rows']):
        pincount = pins
        initial = r*pins+1
        start=[r*pitch_row, 0]
        if r == 0 and pins <= 3:
            pincount = pins -1
            initial = 2
            start=[0, pitch]

        kicad_mod.append(PadArray(
            pincount=pincount, initial=initial, start=start,
            y_spacing=pitch, type=Pad.TYPE_THT, shape=pad_shape,
            size=pad_size, drill=drill, layers=Pad.LAYERS_THT,
            **optional_pad_params))

    #add the locating pin
    kicad_mod.append(Pad(at=[-1.34, C], size=1.3, drill=1.3,
        type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE, layers=Pad.LAYERS_NPTH))

    #add outline to F.Fab
    #kicad_mod.append(RectLine(start=[x1,y1],end=[x2,y2],layer='F.Fab'))

    #and to the silkscreen
    #and draw the tab

    def outline(off = 0, grid = 0):
        out = [
        {'y': roundToBase(B/2, grid),
        'x': roundToBase(x2+off, grid)},
        {'y': roundToBase(y1-off, grid),
        'x': roundToBase(x2+off, grid)},
        {'y': roundToBase(y1-off, grid),
        'x': roundToBase(x1-off, grid)},
        {'y': roundToBase(B/2-TL/2-off, grid),
        'x': roundToBase(x1-off, grid)},
        {'y': roundToBase(B/2-TL/2-off, grid),
        'x': roundToBase(x1-TW-off, grid)},
        {'y': roundToBase(B/2, grid),
        'x': roundToBase(x1-TW-off, grid)}
        ]

        return out

    kicad_mod.append(PolygoneLine(polygone=outline(), layer='F.Fab', width=configuration['fab_line_width']))
    kicad_mod.append(PolygoneLine(polygone=outline(), layer='F.Fab', width=configuration['fab_line_width'], y_mirror=B/2))

    kicad_mod.append(PolygoneLine(polygone=outline(off = off), layer='F.SilkS', width=configuration['silk_line_width']))
    kicad_mod.append(PolygoneLine(polygone=outline(off = off), layer='F.SilkS', width=configuration['silk_line_width'], y_mirror=B/2))

    CrtYd_off = configuration['courtyard_offset']['connector']
    kicad_mod.append(PolygoneLine(
        polygone=outline(off = CrtYd_off, grid=configuration['courtyard_grid']),
        layer='F.CrtYd', width=configuration['courtyard_line_width']))
    kicad_mod.append(PolygoneLine(
        polygone=outline(off = CrtYd_off, grid=configuration['courtyard_grid']),
        layer='F.CrtYd', width=configuration['courtyard_line_width'], y_mirror=B/2))

    # draw the tab
    kicad_mod.append(RectLine(start=[x1+2*off, B/2-TL/2],end=[x1-TW, B/2+TL/2],
        offset=-0.5, width=configuration['fab_line_width'], layer='F.Fab'))

    #draw the pins!
    # o = 0.475 * pitch
    # for i in range(pins):
    #     for j in range(params['number_of_rows']):
    #         y = i * pitch
    #         x = j * pitch
    #
    #         kicad_mod.append(RectLine(start=[x-o,y-o],end=[x+o,y+o], layer='F.Fab', width=configuration['fab_line_width']))

    #pin-1 marker
    p1m_off = configuration['silk_fab_offset'] + 0.3
    p1m_b = B/2-TL/2 - off
    if p1m_b > 0:
        p1m_b = 0

    pin = [
    {'x': 0,'y': body_edge['top'] - p1m_off},
    {'x': body_edge['left'] - p1m_off,'y': body_edge['top'] - p1m_off},
    {'x': body_edge['left'] - p1m_off,'y': p1m_b}
    ]

    kicad_mod.append(PolygoneLine(polygone=pin, layer='F.SilkS', width=configuration['silk_line_width']))

    sl=1
    pin = [
        {'y': body_edge['top'], 'x': -sl/2},
        {'y': body_edge['top'] + sl/sqrt(2), 'x': 0},
        {'y': body_edge['top'], 'x': sl/2}
    ]
    kicad_mod.append(PolygoneLine(polygone=pin,
        width=configuration['fab_line_width'], layer='F.Fab'))

    ######################### Text Fields ###############################
    addTextFields(kicad_mod=kicad_mod, configuration=configuration, body_edges=body_edge,
        courtyard={'top':bounding_box['top'] - CrtYd_off, 'bottom':bounding_box['bottom'] + CrtYd_off}, fp_name=footprint_name, text_y_inside_position='right')

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
