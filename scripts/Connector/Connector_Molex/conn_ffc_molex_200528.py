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

pinrange = range(4, 31) # 4-30 circuits

series = ""
series_long = ('Molex 1.00mm Pitch Easy-On BackFlip, ' +
               'Right-Angle, Bottom Contact FFC/FPC')
manufacturer = 'Molex'
orientation = 'H'
number_of_rows = 1

conn_category = "FFC-FPC"

lib_by_conn_category = True

part_code = "200528-0{:02d}0"

pitch = 1.0
pad_size = (0.4, 1.0)
mp_size = (2.0, 1.3)
foot_y = 3.95
toe_size = (0.55, 0.35)
lead_size = (0.15, pad_size[1] - 0.6)




def make_module(pin_count, configuration):
    mpn = part_code.format(pin_count)
    datasheet='https://www.molex.com/pdm_docs/sd/2005280{:02d}0_sd.pdf'.format(pin_count)

    orientation_str = configuration['orientation_options'][orientation]
    footprint_name = configuration['fp_name_format_string'].format(
        man = manufacturer,
        series = series,
        mpn = mpn,
        num_rows = number_of_rows,
        pins = pin_count,
	pins_per_row = pin_count,
        mounting_pad = "-1MP",
        pitch = pitch,
        orientation = orientation_str)

    footprint_name = footprint_name.replace("__",'_')

    kicad_mod = Footprint(footprint_name)
    kicad_mod.setAttribute('smd')
    kicad_mod.setDescription(
        ("Molex {:s}, {:s}, {:d} Circuits ({:s}), " +
         "generated with kicad-footprint-generator").format(
        series_long, mpn, pin_count, datasheet))
    kicad_mod.setTags(configuration['keyword_fp_string'].format(
        man=manufacturer,
        series=series,
        orientation=orientation_str,
        entry=configuration['entry_direction'][orientation]))




    A = pin_count + 5.2
    B = pin_span = pin_count - 1
    C = pin_count + 3.6
    pin_y = -(0.4 - (lead_size[1] / 2)) - 0.71
    lever_size = (C, 4)
    toe_ins_corner = ((A / 2) - toe_size[0], pin_y + (0.4 - (lead_size[1] / 2)))
    lever_out_corner = (C / 2,
        (toe_ins_corner[1] - toe_size[1]) + 5.25)
    pad_silk_off = (configuration['silk_pad_clearance'] +
                    (configuration['silk_line_width'] / 2))
    fab_silk_off = configuration['silk_fab_offset']

    ## Mounting Pads ##

    mp_pos = ((pin_span / 2) + 1.8 + (mp_size[0] / 2),
        pin_y + (pad_size[1] / 2) + 1.55 + (mp_size[1] / 2))

    def make_anchor_pad(x_direction):
        kicad_mod.append(
            Pad(number = configuration['mounting_pad_number'],
                type = Pad.TYPE_SMT,
                shape = Pad.SHAPE_RECT,
                at = [x_direction * mp_pos[0], mp_pos[1]],
                size = mp_size,
                layers = Pad.LAYERS_SMT))
    make_anchor_pad(-1)
    make_anchor_pad(1)

    ## Pads ##

    kicad_mod.append(
        PadArray(center = [0, pin_y],
            pincount = pin_count,
            x_spacing = pitch,
            type = Pad.TYPE_SMT,
            shape = Pad.SHAPE_RECT,
            size = pad_size,
            layers = Pad.LAYERS_SMT))

    ## Fab ##

    fab_body_outline = [
        {'x': toe_ins_corner[0], 'y': toe_ins_corner[1] - toe_size[1]},
        {'x': toe_ins_corner[0], 'y': toe_ins_corner[1]},
        {'x': -toe_ins_corner[0], 'y': toe_ins_corner[1]},
        {'x': -toe_ins_corner[0], 'y': toe_ins_corner[1] - toe_size[1]},
        {'x': -(A / 2), 'y': toe_ins_corner[1] - toe_size[1]},
        {'x': -(A / 2), 'y': (toe_ins_corner[1] - toe_size[1]) + foot_y},
        {'x': (A / 2), 'y': (toe_ins_corner[1] - toe_size[1]) + foot_y},
        {'x': (A / 2), 'y': toe_ins_corner[1] - toe_size[1]},
        {'x': toe_ins_corner[0], 'y': toe_ins_corner[1] - toe_size[1]}
    ]

    kicad_mod.append(PolygoneLine(
        polygone = fab_body_outline,
        layer = 'F.Fab',
        width = configuration['fab_line_width']))

    fab_pin1_mark = [
        {'x': -(pin_span / 2) - 0.5, 'y': toe_ins_corner[1]},
        {'x': -(pin_span / 2), 'y': toe_ins_corner[1] + 0.75},
        {'x': -(pin_span / 2) + 0.5, 'y': toe_ins_corner[1]}
    ]

    kicad_mod.append(PolygoneLine(
        polygone = fab_pin1_mark,
        layer = 'F.Fab',
        width = configuration['fab_line_width']))

    fab_lever_outline = [
        {'x': lever_out_corner[0], 'y': lever_out_corner[1] - lever_size[1]},
        {'x': -lever_out_corner[0], 'y': lever_out_corner[1] - lever_size[1]},
        {'x': -lever_out_corner[0], 'y': lever_out_corner[1]},
        {'x': lever_out_corner[0], 'y': lever_out_corner[1]},
        {'x': lever_out_corner[0], 'y': lever_out_corner[1] - lever_size[1]}
    ]

    kicad_mod.append(PolygoneLine(
        polygone = fab_lever_outline,
        layer = 'F.Fab',
        width = configuration['fab_line_width']))

    ## SilkS ##

    silk_outline1 = [
        {'x': (-(pin_span / 2) - (pad_size[0] / 2)) - pad_silk_off, 'y': pin_y - (pad_size[1] / 2)},
        {'x': (-(pin_span / 2) - (pad_size[0] / 2)) - pad_silk_off, 'y': toe_ins_corner[1] - fab_silk_off},
        {'x': -toe_ins_corner[0] + fab_silk_off, 'y': toe_ins_corner[1] - fab_silk_off},
        {'x': -toe_ins_corner[0] + fab_silk_off, 'y': (toe_ins_corner[1] - toe_size[1]) - fab_silk_off},
        {'x': -(A / 2) - fab_silk_off, 'y': (toe_ins_corner[1] - toe_size[1]) - fab_silk_off},
        {'x': -(A / 2) - fab_silk_off, 'y': (mp_pos[1] - (mp_size[1] / 2)) - pad_silk_off},
    ]


    silk_outline2 = [
        {'x': -(A / 2) - fab_silk_off, 'y': (mp_pos[1] + (mp_size[1] / 2)) + pad_silk_off},
        {'x': -(A / 2) - fab_silk_off, 'y': ((toe_ins_corner[1] - toe_size[1]) + foot_y) + fab_silk_off},
        {'x': -lever_out_corner[0] - fab_silk_off, 'y': ((toe_ins_corner[1] - toe_size[1]) + foot_y) + fab_silk_off},
        {'x': -lever_out_corner[0] - fab_silk_off, 'y': lever_out_corner[1] + fab_silk_off},
        {'x': lever_out_corner[0] + fab_silk_off, 'y': lever_out_corner[1] + fab_silk_off},
        {'x': lever_out_corner[0] + fab_silk_off, 'y': ((toe_ins_corner[1] - toe_size[1]) + foot_y) + fab_silk_off},
        {'x': (A / 2) + fab_silk_off, 'y': ((toe_ins_corner[1] - toe_size[1]) + foot_y) + fab_silk_off},
        {'x': (A / 2) + fab_silk_off, 'y': (mp_pos[1] + (mp_size[1] / 2)) + pad_silk_off},
    ]

    silk_outline3 = [
        {'x': (A / 2) + fab_silk_off, 'y': (mp_pos[1] - (mp_size[1] / 2)) - pad_silk_off},
        {'x': (A / 2) + fab_silk_off, 'y': (toe_ins_corner[1] - toe_size[1]) - fab_silk_off},
        {'x': toe_ins_corner[0] - fab_silk_off, 'y': (toe_ins_corner[1] - toe_size[1]) - fab_silk_off},
        {'x': toe_ins_corner[0] - fab_silk_off, 'y': toe_ins_corner[1] - fab_silk_off},
        {'x': ((pin_span / 2) + (pad_size[0] / 2)) + pad_silk_off, 'y': toe_ins_corner[1] - fab_silk_off}
    ]

    kicad_mod.append(PolygoneLine(
        polygone = silk_outline1,
        layer = 'F.SilkS',
        width = configuration['silk_line_width']))

    kicad_mod.append(PolygoneLine(
        polygone = silk_outline2,
        layer = 'F.SilkS',
        width = configuration['silk_line_width']))

    kicad_mod.append(PolygoneLine(
        polygone = silk_outline3,
        layer = 'F.SilkS',
        width = configuration['silk_line_width']))

    ## CrtYd ##

    bounding_box = {
        'top': pin_y - (pad_size[1] / 2),
        'left': (-mp_pos[0] - (mp_size[0] / 2)),
        'bottom': lever_out_corner[1],
        'right': (mp_pos[0] + (mp_size[0] / 2))}

    cx1 = roundToBase(bounding_box['left']-configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])
    cy1 = roundToBase(bounding_box['top']-configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])

    cx2 = roundToBase(bounding_box['right']+configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])
    cy2 = roundToBase(bounding_box['bottom']+configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])

    kicad_mod.append(RectLine(
        start=[cx1, cy1], end=[cx2, cy2],
        layer='F.CrtYd', width=configuration['courtyard_line_width']))

    ## Text ##

    addTextFields(kicad_mod=kicad_mod, configuration=configuration, body_edges=bounding_box, courtyard={'top':cy1, 'bottom':cy2}, fp_name=footprint_name, text_y_inside_position='center')




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
