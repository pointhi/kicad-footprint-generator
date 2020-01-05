#!/usr/bin/env python3

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

series = 'DF13'
series_long = 'DF13 through hole'
manufacturer = 'Hirose'
orientation = 'H'
number_of_rows = 1
datasheet = 'https://www.hirose.com/product/en/products/DF13/DF13-4P-1.25DS%2820%29/'

#pins_per_row per row
pins_per_row_range = [2,3,4,5,6,7,8,9,10,11,12,14,15]

#Molex part number
#n = number of circuits per row
part_code = "DF13-{n:02}P-1.25DS"

pitch = 1.25
drill = 0.6

pad_to_pad_clearance = 0.8
max_annular_ring = 0.4
min_annular_ring = 0.15



pad_size = [pitch - pad_to_pad_clearance, drill + 2*max_annular_ring]
if pad_size[0] - drill < 2*min_annular_ring:
    pad_size[0] = drill + 2*min_annular_ring
if pad_size[0] - drill > 2*max_annular_ring:
    pad_size[0] = drill + 2*max_annular_ring

pad_shape=Pad.SHAPE_OVAL
if pad_size[1] == pad_size[0]:
    pad_shape=Pad.SHAPE_CIRCLE



def generate_one_footprint(pins, configuration):
    mpn = part_code.format(n=pins)
    pad_silk_off = configuration['silk_line_width']/2 + configuration['silk_pad_clearance']
    # handle arguments
    orientation_str = configuration['orientation_options'][orientation]
    footprint_name = configuration['fp_name_no_series_format_string'].format(man=manufacturer,
        series=series,
        mpn=mpn, num_rows=number_of_rows, pins_per_row=pins, mounting_pad = "",
        pitch=pitch, orientation=orientation_str)

    footprint_name = footprint_name.replace("__",'_')

    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription("{:s} {:s}, {:s}, {:d} Pins per row ({:s}), generated with kicad-footprint-generator".format(manufacturer, series_long, mpn, pins_per_row, datasheet))
    kicad_mod.setTags(configuration['keyword_fp_string'].format(series=series,
        orientation=orientation_str, man=manufacturer,
        entry=configuration['entry_direction'][orientation]))


    # create pads
    #createNumberedPadsTHT(kicad_mod, pincount, pitch, drill, {'x':x_dia, 'y':y_dia})
    optional_pad_params = {}
    if configuration['kicad4_compatible']:
        optional_pad_params['tht_pad1_shape'] = Pad.SHAPE_RECT
    else:
        optional_pad_params['tht_pad1_shape'] = Pad.SHAPE_ROUNDRECT

    kicad_mod.append(PadArray(start=[0,0], pincount=pins, x_spacing=pitch,
        type=Pad.TYPE_THT, shape=pad_shape, size=pad_size,
        drill=drill, layers=Pad.LAYERS_THT,
        **optional_pad_params))

    A = (pins - 1) * pitch
    B = A + 2.9

    x1 = -(B-A) / 2
    y1 = -4.5
    x2 = x1 + B
    y2 = y1 + 5.4

    body_edge={
        'left':x1,
        'right':x2,
        'bottom':y2,
        'top': y1
        }
    bounding_box = body_edge.copy()

    #draw the connector outline on the F.Fab layer
    kicad_mod.append(RectLine(
        start={'x': x1,'y': y1}, end={'x': x2,'y': y2},
        layer='F.Fab', width=configuration['fab_line_width']))

    #line offset
    off = configuration['silk_fab_offset']

    x1 -= off
    y1 -= off

    x2 += off
    y2 += off

    #y offset from pins 'q'
    q = -0.3

    #x offset from border w
    w = 0.55

    #outline size o
    o = 0.15

    #draw the main outline around the footprint
    kicad_mod.append(PolygoneLine(
        polygone=[
            {'x':-0.2*pitch,'y':pad_size[1]/2+pad_silk_off},
            {'x':-0.2*pitch,'y':y2},
            {'x':x1,'y':y2},
            {'x':x1,'y':y1},
            {'x':x2,'y':y1},
            {'x':x2,'y':y2},
            {'x':(pins -1 + 0.2) * pitch,'y':y2},
            {'x':(pins -1 + 0.2) * pitch,'y':pad_size[1]/2+pad_silk_off}],
        layer='F.SilkS', width=configuration['silk_line_width']))

    #line across the middle
    py = -2.5
    kicad_mod.append(Line(start={'x':x1+w,'y':py},end={'x':x2-w,'y':py},
        layer='F.SilkS', width=configuration['silk_line_width']))
    kicad_mod.append(Line(start={'x':x1+w,'y':py+1.5},end={'x':x2-w,'y':py+1.5},
        layer='F.SilkS', width=configuration['silk_line_width']))

    kicad_mod.append(Line(start={'x':x1+w,'y':y1},end={'x':x1+w,'y':y2},
        layer='F.SilkS', width=configuration['silk_line_width']))
    kicad_mod.append(Line(start={'x':x2-w,'y':y1},end={'x':x2-w,'y':y2},
        layer='F.SilkS', width=configuration['silk_line_width']))
    #add picture of pins

     #add pictures of pins
    #pin-width w
    #pin-length l
    w = 0.15
    l = 1.5

    for p in range(pins):

        px = p * pitch

        kicad_mod.append(PolygoneLine(
            polygone=[
                {'x': px-w,'y': py},
                {'x': px-w,'y': py-l+0.25*w},
                {'x': px,'y': py-l},
                {'x': px+w,'y': py-l+0.25*w},
                {'x': px+w,'y': py}],
            layer='F.SilkS', width=configuration['silk_line_width']))

        #add outline around pins

        if p > 0:
            kicad_mod.append(PolygoneLine(
                polygone=[
                    {'x':px-0.8*pitch,'y':pad_size[1]/2+pad_silk_off},
                   {'x':px-0.8*pitch,'y':y2},
                   {'x':px-0.2*pitch,'y':y2},
                   {'x':px-0.2*pitch,'y':pad_size[1]/2+pad_silk_off}],
                layer='F.SilkS', width=configuration['silk_line_width']))

    #add pin-1 marker

    xm = 0
    ym = 1.5

    m = 0.3

    kicad_mod.append(PolygoneLine(
            polygone=[
                {'x':xm,'y':ym},
                {'x':xm - m,'y':ym + 2 * m},
                {'x':xm + m,'y':ym + 2 * m},
                {'x':xm,'y':ym}],
            layer='F.SilkS', width=configuration['silk_line_width']))

    sl=1
    pin = [
        {'y': body_edge['bottom'], 'x': -sl/2},
        {'y': body_edge['bottom'] - sl/sqrt(2), 'x': 0},
        {'y': body_edge['bottom'], 'x': sl/2}
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
