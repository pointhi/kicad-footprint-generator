#!/usr/bin/env python3

# KicadModTree is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# KicadModTree is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with kicad-footprint-generator. If not, see < http://www.gnu.org/licenses/ >.
#
# (C) 2016 by Thomas Pointhuber, <thomas.pointhuber@gmx.at>

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

series = "SlimStack"
series_long = 'SlimStack Fine-Pitch SMT Board-to-Board Connectors'
manufacturer = 'Molex'
orientation = 'V'
number_of_rows = 2
datasheet = 'http://www.molex.com/pdm_docs/sd/5019204001_sd.pdf'

#pins_per_row per row
pins_range = [30,40,50]

#Molex part number
#n = number of circuits per row
part_code = "501920-{n:02}01"

pitch = 0.5

def generate_one_footprint(pincount, configuration):
    mpn = part_code.format(n=pincount)

    # handle arguments
    orientation_str = configuration['orientation_options'][orientation]
    footprint_name = configuration['fp_name_format_string'].format(man=manufacturer,
        series=series,
        mpn=mpn, num_rows=number_of_rows, pins_per_row=pincount//2, mounting_pad = "",
        pitch=pitch, orientation=orientation_str)

    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription("Molex {:s}, {:s}, {:d} Pins ({:s}), generated with kicad-footprint-generator".format(series_long, mpn, pincount, datasheet))
    kicad_mod.setTags(configuration['keyword_fp_string'].format(series=series,
        orientation=orientation_str, man=manufacturer,
        entry=configuration['entry_direction'][orientation]))

    kicad_mod.setAttribute('smd')

    # calculate working values
    pad_x_spacing = 0.5
    pad_y_spacing = 2.4 + 1.1
    pad_width = 0.3
    pad_height = 1.1
    pad_x_span = (pad_x_spacing * ((pincount / 2) - 1))

    h_body_width = 3.1 / 2.0
    h_body_length = (pad_x_span / 2.0) + 1.4 + 0.37

    fab_width = configuration['fab_line_width']

    outline_x = h_body_length - (pad_x_span / 2.0) - pad_width/2 - (configuration['silk_pad_clearance'] + configuration['silk_line_width']/2)
    marker_y = 0.8
    silk_width = configuration['silk_line_width']
    nudge = configuration['silk_fab_offset']

    courtyard_width = configuration['courtyard_line_width']
    courtyard_precision = configuration['courtyard_grid']
    courtyard_clearance = configuration['courtyard_offset']['connector']
    courtyard_x = roundToBase(h_body_length + courtyard_clearance, courtyard_precision)
    courtyard_y = roundToBase((pad_y_spacing + pad_height) / 2.0 + courtyard_clearance, courtyard_precision)

    # create pads
    kicad_mod.append(PadArray(pincount=pincount//2, x_spacing=pad_x_spacing, y_spacing=0,\
        center=[0,-pad_y_spacing/2.0], initial=1, increment=2, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, size=[pad_width, pad_height],\
        layers=Pad.LAYERS_SMT))
    kicad_mod.append(PadArray(pincount=pincount//2, x_spacing=pad_x_spacing, y_spacing=0,\
        center=[0,pad_y_spacing/2.0], initial=2, increment=2, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, size=[pad_width, pad_height],\
        layers=Pad.LAYERS_SMT))

    # create fab outline and pin 1 marker
    kicad_mod.append(RectLine(start=[-h_body_length, -h_body_width], end=[h_body_length, h_body_width], layer='F.Fab', width=fab_width))
    body_edge={
        'left':-h_body_length,
        'top':-h_body_width
    }
    body_edge['right'] = -body_edge['left']
    body_edge['bottom'] = -body_edge['top']
    kicad_mod.append(Line(start=[-h_body_length+outline_x, -h_body_width-nudge], end=[-h_body_length+outline_x, -h_body_width-marker_y], layer='F.Fab', width=fab_width))

    # create silkscreen outline and pin 1 marker
    left_outline = [[-h_body_length+outline_x, h_body_width+nudge], [-h_body_length-nudge, h_body_width+nudge], [-h_body_length-nudge, -h_body_width-nudge],\
                    [-h_body_length+outline_x, -h_body_width-nudge], [-h_body_length+outline_x, -h_body_width-marker_y]]
    right_outline = [[h_body_length-outline_x, h_body_width+nudge], [h_body_length+nudge, h_body_width+nudge], [h_body_length+nudge, -h_body_width-nudge],\
                     [h_body_length-outline_x, -h_body_width-nudge]]
    kicad_mod.append(PolygoneLine(polygone=left_outline, layer='F.SilkS', width=silk_width))
    kicad_mod.append(PolygoneLine(polygone=right_outline, layer='F.SilkS', width=silk_width))

    # create courtyard
    kicad_mod.append(RectLine(start=[-courtyard_x, -courtyard_y], end=[courtyard_x, courtyard_y], layer='F.CrtYd', width=courtyard_width))

    ######################### Text Fields ###############################

    addTextFields(kicad_mod=kicad_mod, configuration=configuration, body_edges=body_edge,
        courtyard={'top':-courtyard_y, 'bottom':+courtyard_y},
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

    for pins in pins_range:
        generate_one_footprint(pins, configuration)
