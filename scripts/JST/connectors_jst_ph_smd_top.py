#!/usr/bin/env python

import sys
import os

# export PYTHONPATH="${PYTHONPATH}<path to kicad-footprint-generator directory>"
sys.path.append(os.path.join(sys.path[0], "..", ".."))  # load parent path of KicadModTree
import argparse
import yaml
from helpers import *
from KicadModTree import *

# http://www.jst-mfg.com/product/pdf/eng/ePH.pdf

series = "PH"
orientation = 'Vertical'
number_of_rows = 1
datasheet = 'http://www.jst-mfg.com/product/pdf/eng/ePH.pdf'

pitch = 2.00

pad_size = [1, 7.5-2]
mount_pad_size = [1.6, 3] #Datasheet: width = 1.5+/-0.1
pad_y_outside_distance = 7.5-1 #See freecad sketch and Datasheet.
pad_y_center_distance = pad_y_outside_distance-pad_size[1]/2.0-mount_pad_size[1]/2.0
pad_pos_y = pad_y_center_distance/2.0
mount_pad_y_pos = -pad_pos_y
mount_pad_center_x_to_pin = 1.6+mount_pad_size[0]/2.0


# Connector Parameters
silk_to_part_offset = 0.1

y_min = mount_pad_y_pos - mount_pad_size[1]/2.0 - 1
y_max = y_min + 5


silk_y_min = y_min - silk_to_part_offset
silk_y_max = y_max + silk_to_part_offset
body_back_protrusion_width = 0.8

y_min_big_cutout = y_max-1.2
dx_big_cutout_to_side = 3.45

def generate_one_footprint(pincount, configuration):
    x_mid = 0
    x_max = (pincount-1)*pitch/2.0 + 2.975
    silk_x_max = x_max + silk_to_part_offset
    x_min = -x_max
    silk_x_min = x_min - silk_to_part_offset
    first_pad_x=-(pincount-1)/2.0*pitch
    x_left_mount_pad = first_pad_x-mount_pad_center_x_to_pin

    # Surface mount shrouded header, Top entry type
    part = "B{n:d}B-PH-SM4-TB".format(n=pincount) #JST part number format string
    footprint_name = configuration['fp_name_format_string'].format(series=series, mpn=part, num_rows=number_of_rows,
        pins_per_row=pincount, pitch=pitch, orientation=orientation)

    kicad_mod = Footprint(footprint_name)
    description = "JST PH series connector, " + part + ", top entry type, surface mount, Datasheet: http://www.jst-mfg.com/product/pdf/eng/ePH.pdf"
    kicad_mod.setDescription(description)
    kicad_mod.setTags('connector jst ph')
    kicad_mod.setAttribute("smd")

    # create Silkscreen
    poly_silk_top = [
        {'x':silk_x_min, 'y':mount_pad_y_pos-mount_pad_size[1]/2.0-configuration['silk_pad_clearence']},
        {'x':silk_x_min, 'y':silk_y_min},
        {'x':silk_x_max, 'y':silk_y_min},
        {'x':silk_x_max, 'y':mount_pad_y_pos-mount_pad_size[1]/2.0-configuration['silk_pad_clearence']}
    ]
    kicad_mod.append(PolygoneLine(polygone=poly_silk_top, layer='F.SilkS', width=configuration['silk_line_width']))

    poly_silk_bottom_left = [
        {'x':silk_x_min, 'y':mount_pad_y_pos+mount_pad_size[1]/2.0+configuration['silk_pad_clearence']},
        {'x':silk_x_min, 'y':silk_y_max},
        {'x':first_pad_x-pad_size[0]/2.0-configuration['silk_pad_clearence'], 'y':silk_y_max}
    ]
    kicad_mod.append(PolygoneLine(polygone=poly_silk_bottom_left, layer='F.SilkS', width=configuration['silk_line_width']))

    poly_silk_bottom_right = [
        {'x':silk_x_max, 'y':mount_pad_y_pos+mount_pad_size[1]/2.0+configuration['silk_pad_clearence']},
        {'x':silk_x_max, 'y':silk_y_max},
        {'x':-first_pad_x+pad_size[0]/2.0+configuration['silk_pad_clearence'], 'y':silk_y_max}
    ]
    kicad_mod.append(PolygoneLine(polygone=poly_silk_bottom_right, layer='F.SilkS', width=configuration['silk_line_width']))

    if configuration['allow_silk_below_part'] == 'smd' or configuration['allow_silk_below_part'] == 'both':
        poly_silk_inner_left = [
            {'x':silk_x_min+3.5, 'y':silk_y_min},
            {'x':silk_x_min+3.5, 'y':silk_y_min+0.7},
            {'x':silk_x_min+1.8, 'y':silk_y_min+0.7},
            {'x':silk_x_min+1.8, 'y':silk_y_max-0.8},
            {'x':first_pad_x-pad_size[0]/2.0-configuration['silk_pad_clearence'], 'y':silk_y_max-0.8}
        ]
        kicad_mod.append(PolygoneLine(polygone=poly_silk_inner_left, layer='F.SilkS', width=configuration['silk_line_width']))

        poly_silk_inner_right = [
            {'x':silk_x_max-3.5, 'y':silk_y_min},
            {'x':silk_x_max-3.5, 'y':silk_y_min+0.7},
            {'x':silk_x_max-1.8, 'y':silk_y_min+0.7},
            {'x':silk_x_max-1.8, 'y':silk_y_max-0.8},
            {'x':-first_pad_x+pad_size[0]/2.0+configuration['silk_pad_clearence'], 'y':silk_y_max-0.8}
        ]
        kicad_mod.append(PolygoneLine(polygone=poly_silk_inner_right, layer='F.SilkS', width=configuration['silk_line_width']))

    #Fab outline
    kicad_mod.append(RectLine(start=[x_min, y_min], end=[x_max, y_max],
        layer='F.Fab', width=configuration['fab_line_width']))
    #Pin 1 Marker
    kicad_mod.append(Line(start=[first_pad_x-pad_size[0]/2.0-configuration['silk_pad_clearence'], silk_y_max],
        end=[first_pad_x-pad_size[0]/2.0-configuration['silk_pad_clearence'], pad_pos_y+pad_size[1]/2.0],
        layer='F.SilkS', width=configuration['silk_line_width']))
    poly_pin1_marker = [
        {'x':first_pad_x-1, 'y':y_max},
        {'x':first_pad_x, 'y':y_max-1},
        {'x':first_pad_x+1, 'y':y_max}
    ]
    kicad_mod.append(PolygoneLine(polygone=poly_pin1_marker, layer='F.Fab', width=configuration['fab_line_width']))
    #kicad_mod.addCircle({'x':start_pos_x-2.95+0.8+0.75, 'y':3.1+0.75}, {'x':0.25, 'y':0}, 'F.SilkS', 0.15)

    # create Courtyard
    part_x_min = x_left_mount_pad - mount_pad_size[0]/2.0
    part_x_max = -x_left_mount_pad + mount_pad_size[0]/2.0
    part_y_min = y_min
    part_y_max = pad_pos_y+pad_size[1]/2.0

    cx1 = roundToBase(part_x_min-configuration['courtyard_distance'], configuration['courtyard_grid'])
    cy1 = roundToBase(part_y_min-configuration['courtyard_distance'], configuration['courtyard_grid'])

    cx2 = roundToBase(part_x_max+configuration['courtyard_distance'], configuration['courtyard_grid'])
    cy2 = roundToBase(part_y_max+configuration['courtyard_distance'], configuration['courtyard_grid'])

    kicad_mod.append(RectLine(
        start=[cx1, cy1], end=[cx2, cy2],
        layer='F.CrtYd', width=configuration['courtyard_line_width']))

    # create pads
    #create Pads
    for p in range(pincount):
        Y = pad_pos_y
        X = first_pad_x + p * pitch

        num = p+1
        kicad_mod.append(Pad(number=num, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
                            at=[X, Y], size=pad_size, layers=Pad.LAYERS_SMT))

    kicad_mod.append(Pad(number ='""', type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
                        at=[x_left_mount_pad, mount_pad_y_pos],
                        size=mount_pad_size, layers=Pad.LAYERS_SMT))
    kicad_mod.append(Pad(number ='""', type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
                        at=[-x_left_mount_pad, mount_pad_y_pos],
                        size=mount_pad_size, layers=Pad.LAYERS_SMT))

    center = [0,-1.5]
    reference_fields = configuration['references']
    kicad_mod.append(Text(type='reference', text='REF**',
        **getTextFieldDetails(reference_fields[0], cy1, cy2, center)))

    for additional_ref in reference_fields[1:]:
        kicad_mod.append(Text(type='user', text='%R',
        **getTextFieldDetails(additional_ref, cy1, cy2, center)))

    value_fields = configuration['values']
    kicad_mod.append(Text(type='value', text=footprint_name,
        **getTextFieldDetails(value_fields[0], cy1, cy2, center)))

    for additional_value in value_fields[1:]:
        kicad_mod.append(Text(type='user', text='%V',
            **getTextFieldDetails(additional_value, cy1, cy2, center)))

    model3d_path_prefix = configuration.get('3d_model_prefix','${KISYS3DMOD}')

    lib_name = configuration['lib_name_format_string'].format(series=series)
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
    parser.add_argument('-c', '--config', type=str, nargs='?', help='the config file defining how the footprint will look like.', default='config_KLCv3.0.yaml')
    args = parser.parse_args()

    with open(args.config, 'r') as config_stream:
        try:
            configuration = yaml.load(config_stream)
        except yaml.YAMLError as exc:
            print(exc)

    for pincount in range(2,17):
        generate_one_footprint(pincount, configuration)
