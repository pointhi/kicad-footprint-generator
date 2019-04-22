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
from footprint_keepout_area import addRectangularKeepout

pins_per_row_range = range(2,23)

series = ""
series_long = 'LY 20 series connector'
manufacturer = 'JAE'
orientation = 'H'
number_of_rows = 2
datasheet='http://www.jae.com/z-en/pdf_download_exec.cfm?param=SJ038187.pdf'

part_code = "LY20-{:d}P-DLT1"

# def get_name(pin_count):
#     return 'Molex-502250-{0}91_2Rows-{0}Pins_P0.3mm_Horizontal'.format(pin_count)

pitch = 2
drill = 0.8
start_pos_x = 0 # Where should pin 1 be located.
pad_to_pad_clearance = 0.8
max_annular_ring = 0.5 #How much copper should be in y direction?
min_annular_ring = 0.15


pitch_row = 2

pad_size = [pitch_row - pad_to_pad_clearance, pitch - pad_to_pad_clearance]
if pad_size[0] - drill < 2*min_annular_ring:
    pad_size[0] = drill + 2*min_annular_ring
if pad_size[0] - drill > 2*max_annular_ring:
    pad_size[0] = drill + 2*max_annular_ring

if pad_size[1] - drill < 2*min_annular_ring:
    pad_size[1] = drill + 2*min_annular_ring
if pad_size[1] - drill > 2*max_annular_ring:
    pad_size[1] = drill + 2*max_annular_ring

ROW_NAMES = ('a','b')
def incrementPadNumber(old_number):
    return old_number[0] + str(int(old_number[1:])+1)

if pad_size[0] == pad_size[1]:
    pad_shape = Pad.SHAPE_CIRCLE
else:
    pad_shape = Pad.SHAPE_OVAL

def make_module(pins_per_row, configuration):
    pad_silk_off = configuration['silk_line_width']/2 + configuration['silk_pad_clearance']
    off = configuration['silk_fab_offset']

    mpn = part_code.format(pins_per_row*2)

    orientation_str = configuration['orientation_options'][orientation]
    footprint_name = configuration['fp_name_format_string'].format(man=manufacturer,
        series=series,
        mpn=mpn, num_rows=number_of_rows, pins_per_row=pins_per_row, mounting_pad = "",
        pitch=pitch, orientation=orientation_str)

    footprint_name = footprint_name.replace("__",'_')

    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription("Molex {:s}, {:s}, {:d} Circuits ({:s}), generated with kicad-footprint-generator".format(series_long, mpn, pins_per_row, datasheet))
    kicad_mod.setTags(configuration['keyword_fp_string'].format(series=series,
        orientation=orientation_str, man=manufacturer,
        entry=configuration['entry_direction'][orientation]))

    Wi = 4.8
    T = 2.8
    W = Wi + T


    body_edge = {}
    body_edge['right'] = pitch_row + 2.2 + T
    body_edge['left'] = body_edge['right'] - W

    A = (pins_per_row-1)*pitch
    B = (A - 8) if A >= 8 else 0
    C = (A - 4.6) if A >= 4.6 else 0
    D = A + 2.6
    E = A + 3.6

    body_edge['top'] = -(E - A)/2
    body_edge['bottom'] = body_edge['top'] + E

    bounding_box = body_edge.copy()

    ############################## Pins ###############################
    optional_pad_params = {}
    if configuration['kicad4_compatible']:
        optional_pad_params['tht_pad1_shape'] = Pad.SHAPE_RECT
    else:
        optional_pad_params['tht_pad1_shape'] = Pad.SHAPE_ROUNDRECT

    for row_idx in range(2):
        kicad_mod.append(PadArray(
            initial=ROW_NAMES[row_idx]+'1', start=[(row_idx)*pitch_row, 0],
            y_spacing=pitch, pincount=pins_per_row, increment=incrementPadNumber,
            size=pad_size, drill=drill,
            type=Pad.TYPE_THT, shape=pad_shape, layers=Pad.LAYERS_THT,
            tht_pad1_id=ROW_NAMES[0]+'1',
            **optional_pad_params))

    ############################ Outline ##############################
    kicad_mod.append(RectLine(
        start=[body_edge['left'], body_edge['top']],
        end=[body_edge['right'], body_edge['bottom']],
        layer="F.Fab", width=configuration['fab_line_width']
    ))

    r_no_silk = max(pad_size)/2 + pad_silk_off
    dx = abs(body_edge['left']) + off
    pin_center_silk_y = 0 if dx >= r_no_silk else sqrt(r_no_silk**2-dx**2)
    pin1_center_silk_y = pad_size[1]/2 + pad_silk_off

    YCb = A/2+C/2
    YCt = A/2-C/2
    YBb = A/2+B/2


    poly_silk_b = [
        {'x': body_edge['left']-off, 'y': body_edge['bottom']+off},
        {'x': body_edge['right']+off, 'y': body_edge['bottom']+off},
        {'x': body_edge['right']+off, 'y': YCb},
    ]
    if C > 0:
        poly_silk_b.extend([
            {'x': body_edge['right']-T, 'y': YCb},
            {'x': body_edge['right']-T, 'y': A/2},
        ])
    kicad_mod.append(PolygoneLine(polygone=poly_silk_b,
        layer="F.SilkS", width=configuration['silk_line_width']))
    kicad_mod.append(PolygoneLine(polygone=poly_silk_b, y_mirror=A/2,
        layer="F.SilkS", width=configuration['silk_line_width']))


    if pin_center_silk_y == 0:
        kicad_mod.append(Line(
            start=[body_edge['left']-off, body_edge['top']],
            end=[body_edge['left']-off, body_edge['bottom']],
            layer="F.SilkS", width=configuration['silk_line_width']
        ))
    else:
        kicad_mod.append(Line(
            start=[body_edge['left']-off, body_edge['top']-off],
            end=[body_edge['left']-off, -pin1_center_silk_y],
            layer="F.SilkS", width=configuration['silk_line_width']
        ))
        kicad_mod.append(Line(
            start=[body_edge['left']-off, pin1_center_silk_y],
            end=[body_edge['left']-off, pitch-pin_center_silk_y],
            layer="F.SilkS", width=configuration['silk_line_width']
        ))
        kicad_mod.append(Line(
            start=[body_edge['left']-off, A+pin_center_silk_y],
            end=[body_edge['left']-off, body_edge['bottom']+off],
            layer="F.SilkS", width=configuration['silk_line_width']
        ))
        for i in range(1, pins_per_row-1):
            yt = i*pitch + pin_center_silk_y
            yb = (i+1)*pitch - pin_center_silk_y
            kicad_mod.append(Line(
                start=[body_edge['left']-off, yt],
                end=[body_edge['left']-off, yb],
                layer="F.SilkS", width=configuration['silk_line_width']
            ))

    x1 = body_edge['right']-T

    pin_w = 0.5
    pin_L = 2.7
    pin_chamfer_x = pin_w/3


    if B>0:
        x2 = x1 + 2 # estimated from drawing
        poly = [
            {'x': x2, 'y':YCb},
            {'x': x2, 'y':YBb+pin_w/2}
        ]
        kicad_mod.append(PolygoneLine(polygone=poly,
            layer="F.SilkS", width=configuration['silk_line_width']))
        kicad_mod.append(PolygoneLine(polygone=poly, y_mirror=A/2,
            layer="F.SilkS", width=configuration['silk_line_width']))


    #pins
    if C>0:
        for i in range(pins_per_row):
            ypc = i*pitch

            x3 = x1 + pin_L
            x2 = x3 - pin_chamfer_x

            if ypc - pin_w/2 >= YCt and ypc + pin_w/2 <= YCb:
                pin_poly = [
                    {'x': x1, 'y': ypc-pin_w/2},
                    {'x': x2, 'y': ypc-pin_w/2},
                    {'x': x3, 'y': ypc},
                    {'x': x2, 'y': ypc+pin_w/2},
                    {'x': x1, 'y': ypc+pin_w/2}
                ]
                kicad_mod.append(PolygoneLine(polygone=pin_poly,
                    layer="F.SilkS", width=configuration['silk_line_width']))

    ########################### Pin 1 #################################

    p1s_sl = 2
    p1s_off = off + 0.3
    kicad_mod.append(PolygoneLine(
        polygone=[
            {'x': body_edge['left'] + p1s_sl, 'y': body_edge['top'] - p1s_off},
            {'x': body_edge['left'] - p1s_off, 'y': body_edge['top'] - p1s_off},
            {'x': body_edge['left'] - p1s_off, 'y': body_edge['top'] + p1s_sl}
        ], layer="F.SilkS", width=configuration['silk_line_width']))

    p1f_sl = 1
    kicad_mod.append(PolygoneLine(
        polygone=[
            {'x': body_edge['left'], 'y': p1f_sl/2},
            {'x': body_edge['left'] + p1f_sl/sqrt(2), 'y': 0},
            {'x': body_edge['left'], 'y': -p1f_sl/2}
        ], layer="F.Fab", width=configuration['fab_line_width']))

    ########################### CrtYd #################################
    cx1 = roundToBase(bounding_box['left']-configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])
    cy1 = roundToBase(bounding_box['top']-configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])

    cx2 = roundToBase(bounding_box['right']+configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])
    cy2 = roundToBase(bounding_box['bottom']+configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])

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

    for pins_per_row in pins_per_row_range:
        make_module(pins_per_row, configuration)
