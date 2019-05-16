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

pinrange = [25, 29, 41, 51, 71, 81]

series = ""
series_long = 'JAE 0.2mm pitch, 1mm overall height FFC/FPC connector'
manufacturer = 'JAE'
orientation = 'H'
number_of_rows = 2
datasheet='http://www.jae.com/z-en/pdf_download_exec.cfm?param=SJ108178.pdf'

conn_category = "FFC-FPC"

lib_by_conn_category = True

part_code = "FF08{:02d}SA1"

# def get_name(pin_count):
#     return 'Molex-502250-{0}91_2Rows-{0}Pins_P0.3mm_Horizontal'.format(pin_count)

cable_pitch = 0.2
odd_pad_size = (0.55, 0.18) # bottom
even_pad_size = (0.7, 0.18) # top

def make_module(pin_count, configuration):
    pad_silk_off = configuration['silk_line_width']/2 + configuration['silk_pad_clearance']
    off = configuration['silk_fab_offset']

    mpn = part_code.format(pin_count)

    orientation_str = configuration['orientation_options'][orientation]
    footprint_name = configuration['fp_name_unequal_row_format_string'].format(man=manufacturer,
        series=series,
        mpn=mpn, num_rows=number_of_rows, pins=pin_count, mounting_pad = "",
        pitch=cable_pitch*2, orientation=orientation_str)

    footprint_name = footprint_name.replace("__",'_')

    kicad_mod = Footprint(footprint_name)
    kicad_mod.setAttribute('smd')
    kicad_mod.setDescription("Molex {:s}, {:s}, {:d} Circuits ({:s}), generated with kicad-footprint-generator".format(series_long, mpn, pin_count, datasheet))
    kicad_mod.setTags(configuration['keyword_fp_string'].format(series=series,
        orientation=orientation_str, man=manufacturer,
        entry=configuration['entry_direction'][orientation]))


    pad_to_pad_inside = 2
    pad_to_pad_outside = pad_to_pad_inside + odd_pad_size[0] + even_pad_size[0]
    row_spacing = pad_to_pad_outside - odd_pad_size[0]/2 - even_pad_size[0]/2

    odd_pad_x = -pad_to_pad_outside/2 + odd_pad_size[0]/2
    even_pad_x = odd_pad_x + row_spacing


    B = cable_pitch * (pin_count - 1)

    A = B + (7.05-4.8)
    bar_width_max = 2*3.8
    bar_chamfer_y = 1
    bar_from_side_min = 0.1

    bar_width = A - 2*bar_from_side_min
    if bar_width > bar_width_max:
        bar_width = bar_width_max

    body_edge = {
        'top': -A/2,
        'bottom': A/2,
        'left': odd_pad_x - odd_pad_size[0]/2 + 0.35
    }
    body_edge['right'] = body_edge['left'] + 2.85

    bar_down_edge = body_edge['left'] + 3.23


    bounding_box = {
        'top': body_edge['top'],
        'bottom': body_edge['bottom'],
        'left': odd_pad_x - odd_pad_size[0]/2,
        'right': bar_down_edge
    }

    kicad_mod.append(RectLine(
        start=[body_edge['left'], body_edge['top']],
        end=[body_edge['right'], body_edge['bottom']],
        layer="F.Fab", width=configuration['fab_line_width']
    ))
    kicad_mod.append(PolygoneLine(
        polygone=[
            {'x': body_edge['right'], 'y': -bar_width/2},
            {'x': bar_down_edge, 'y': -bar_width/2 + bar_chamfer_y},
            {'x': bar_down_edge, 'y': bar_width/2 - bar_chamfer_y},
            {'x': body_edge['right'], 'y': bar_width/2}
        ],
        layer="F.Fab", width=configuration['fab_line_width']
    ))

    odd_pins_outside = B/2 + odd_pad_size[1]/2 + pad_silk_off
    silk_outline = [
        {'x': body_edge['left']-off, 'y':odd_pins_outside},
        {'x': body_edge['left']-off, 'y':body_edge['bottom']+off},
        {'x': body_edge['right'] + off, 'y':body_edge['bottom']+off},
        {'x': body_edge['right'] + off, 'y': bar_width/2 + off},
        {'x': bar_down_edge + off, 'y': bar_width/2 - bar_chamfer_y + off},
        {'x': bar_down_edge + off, 'y': 0}
    ]
    kicad_mod.append(PolygoneLine(
        polygone=silk_outline,
        layer="F.SilkS", width=configuration['silk_line_width']
    ))
    kicad_mod.append(PolygoneLine(
        polygone=silk_outline, y_mirror=0,
        layer="F.SilkS", width=configuration['silk_line_width']
    ))

    even_pins = pin_count//2
    odd_pins = pin_count - even_pins
    kicad_mod.append(PadArray(
            center=[odd_pad_x,0], pincount=odd_pins,
            initial=1, increment=2, y_spacing=2*cable_pitch,
            type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
            size=odd_pad_size, layers=Pad.LAYERS_SMT))
    kicad_mod.append(PadArray(
            center=[even_pad_x, 0], pincount=even_pins,
            initial=2, increment=2, y_spacing=2*cable_pitch,
            type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
            size=even_pad_size, layers=Pad.LAYERS_SMT))

    pin1_y = -B/2
    ps1_m = 0.3
    p1s_x = bounding_box['left'] - pad_silk_off
    pin = [
        {'x': p1s_x -  ps1_m/sqrt(2), 'y': pin1_y-ps1_m/2},
        {'x': p1s_x, 'y': pin1_y},
        {'x': p1s_x -  ps1_m/sqrt(2), 'y': pin1_y+ps1_m/2},
        {'x': p1s_x -  ps1_m/sqrt(2), 'y': pin1_y-ps1_m/2}
    ]
    kicad_mod.append(PolygoneLine(polygone=pin,
        layer="F.SilkS", width=configuration['silk_line_width']))

    sl=0.6
    pin = [
        {'x': body_edge['left'], 'y': pin1_y-sl/2},
        {'x': body_edge['left'] + sl/sqrt(2), 'y': pin1_y},
        {'x': body_edge['left'], 'y': pin1_y+sl/2}
    ]
    kicad_mod.append(PolygoneLine(polygone=pin,
        width=configuration['fab_line_width'], layer='F.Fab'))

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
        courtyard={'top':cy1, 'bottom':cy2}, fp_name=footprint_name, text_y_inside_position='right')

    ##################### Output and 3d model ############################
    model3d_path_prefix = configuration.get('3d_model_prefix','${KISYS3DMOD}/')

    if lib_by_conn_category:
        lib_name = configuration['lib_name_specific_function_format_string'].format(category=conn_category)
    else:
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

    for pincount in pinrange:
        make_module(pincount, configuration)
