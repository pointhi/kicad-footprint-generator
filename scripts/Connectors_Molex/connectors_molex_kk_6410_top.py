#!/usr/bin/env python

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
sys.path.append(os.path.join(sys.path[0], "..", ".."))  # load parent path of KicadModTree
import argparse
import yaml
from helpers import *
from KicadModTree import *

sys.path.append(os.path.join(sys.path[0], "..", "tools"))  # load parent path of tools
from footprint_text_fields import addTextFields

series = "KK-254"
manufacturer = 'Molex'
orientation = 'V'
number_of_rows = 1
datasheet = 'http://www.jst-mfg.com/product/pdf/eng/eEH.pdf'

pitch = 2.54
drill = 1.2 # square pins:0.64mm -> touching circle: ~0.9mm -> minimum drill accourding to KLC: 1.1mm
start_pos_x = 0 # Where should pin 1 be located.
pad_to_pad_clearance = 0.8
pad_copper_y_solder_length = 0.5 #How much copper should be in y direction?
min_annular_ring = 0.15

def generate_one_footprint(pincount, configuration):

    mpn = '0022272{n:02d}1'.format(n=pincount)

    # handle arguments
    orientation_str = configuration['orientation_options'][orientation]
    footprint_name = configuration['fp_name_format_string'].format(man=manufacturer,
        series=series,
        mpn=mpn, num_rows=number_of_rows, pins_per_row=pincount,
        pitch=pitch, orientation=orientation_str)

    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription("Molex {:s} series connector, {:s}, {:d}Pins ({:s}), generated with kicad-footprint-generator".format(series, mpn, pincount, datasheet))
    kicad_mod.setTags(configuration['keyword_fp_string'].format(series=series,
        orientation=orientation_str, man=manufacturer,
        entry=configuration['entry_direction'][orientation]))

    # calculate working values
    end_pos_x = (pincount-1) * pitch
    centre_x = (end_pos_x - start_pos_x) / 2.0
    nudge = configuration['silk_fab_offset']
    silk_w = configuration['silk_line_width']
    fab_w = configuration['fab_line_width']


    body_edge={
        'left':start_pos_x - pitch/2,
        'right':end_pos_x + pitch/2,
        'bottom':1.88+1
        }
    body_edge['top'] = body_edge['bottom']-5.08


    pad_size = [pitch - pad_to_pad_clearance, drill + 2*pad_copper_y_solder_length]
    if pad_size[0] - drill < 2*min_annular_ring:
        pad_size[0] = drill + 2*min_annular_ring

    # create pads
    # kicad_mod.append(Pad(number=1, type=Pad.TYPE_THT, shape=Pad.SHAPE_RECT,
    #                     at=[0, 0], size=pad_size,
    #                     drill=drill, layers=Pad.LAYERS_THT))

    kicad_mod.append(PadArray(initial=1, start=[start_pos_x, 0],
        x_spacing=pitch, pincount=pincount,
        size=pad_size, drill=drill,
        type=Pad.TYPE_THT, shape=Pad.SHAPE_OVAL, layers=Pad.LAYERS_THT))

    # create fab outline
    kicad_mod.append(RectLine(start=[start_pos_x-pitch/2.0, -5.8/2.0],\
        end=[end_pos_x+pitch/2.0, 5.8/2.0], layer='F.Fab', width=fab_w))

    # create silkscreen
    kicad_mod.append(RectLine(start=[start_pos_x-pitch/2.0-nudge, -3.02],\
        end=[end_pos_x+pitch/2.0+nudge, 2.98], layer='F.SilkS', width=silk_w))

    # pin 1 markers
    kicad_mod.append(Line(start=[start_pos_x-pitch/2.0-0.4, -2.0],\
        end=[start_pos_x-pitch/2.0-0.4, 2.0], layer='F.SilkS', width=silk_w))
    kicad_mod.append(Line(start=[start_pos_x-pitch/2.0-0.4, -2.0],\
        end=[start_pos_x-pitch/2.0-0.4, 2.0], layer='F.Fab', width=fab_w))

    if pincount <= 6:
        # one ramp
        kicad_mod.append(PolygoneLine(polygone=[[start_pos_x, 2.98], [start_pos_x, 1.98],\
            [end_pos_x, 1.98], [end_pos_x, 2.98]], layer='F.SilkS', width=silk_w))
        kicad_mod.append(PolygoneLine(polygone=[[start_pos_x, 1.98], [start_pos_x+0.25, 1.55],\
            [end_pos_x-0.25, 1.55], [end_pos_x, 1.98] ],layer='F.SilkS', width=silk_w))
        kicad_mod.append(PolygoneLine(polygone=[[start_pos_x+0.25, 2.98],\
            [start_pos_x+0.25, 1.98]], layer='F.SilkS', width=silk_w))
        kicad_mod.append(PolygoneLine(polygone=[[end_pos_x-0.25, 2.98],\
            [end_pos_x-0.25, 1.98]], layer='F.SilkS', width=silk_w))

    else:
        # two ramps
        kicad_mod.append(PolygoneLine(polygone=[[start_pos_x, 2.98], [start_pos_x, 1.98],\
            [start_pos_x+2*pitch, 1.98], [start_pos_x+2*pitch, 2.98]], layer='F.SilkS', width=silk_w))
        kicad_mod.append(PolygoneLine(polygone=[[start_pos_x, 1.98], [start_pos_x+0.25, 1.55],\
            [start_pos_x+2*pitch, 1.55], [start_pos_x+2*pitch, 1.98] ],layer='F.SilkS', width=silk_w))
        kicad_mod.append(PolygoneLine(polygone=[[start_pos_x+0.25, 2.98],\
            [start_pos_x+0.25, 1.98]], layer='F.SilkS', width=silk_w))

        kicad_mod.append(PolygoneLine(polygone=[[end_pos_x, 2.98], [end_pos_x, 1.98],\
            [end_pos_x-2*pitch, 1.98], [end_pos_x-2*pitch, 2.98]], layer='F.SilkS', width=silk_w))
        kicad_mod.append(PolygoneLine(polygone=[[end_pos_x, 1.98], [end_pos_x-0.25, 1.55],\
            [end_pos_x-2*pitch, 1.55], [end_pos_x-2*pitch, 1.98] ],layer='F.SilkS', width=silk_w))
        kicad_mod.append(PolygoneLine(polygone=[[end_pos_x-0.25, 2.98],\
            [end_pos_x-0.25, 1.98]], layer='F.SilkS', width=silk_w))

    for i in range(0, pincount):
        middle_x = start_pos_x + i * pitch
        start_x = middle_x - 1.6/2
        end_x = middle_x + 1.6/2
        kicad_mod.append(PolygoneLine(polygone=[[start_x, -3.02], [start_x, -2.4],\
            [end_x, -2.4], [end_x, -3.02]], layer='F.SilkS', width=silk_w))

    ########################### CrtYd #################################
    cx1 = roundToBase(body_edge['left']-configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])
    cy1 = roundToBase(body_edge['top']-configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])

    cx2 = roundToBase(body_edge['right']+configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])
    cy2 = roundToBase(body_edge['bottom']+configuration['courtyard_offset']['connector'], configuration['courtyard_grid'])

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
    parser.add_argument('--global_config', type=str, nargs='?', help='the config file defining how the footprint will look like. (KLC)', default='../tools/global_config_files/config_KLCv3.0.yaml')
    parser.add_argument('--series_config', type=str, nargs='?', help='the config file defining series parameters.', default='../Connector_SMD_single_row_plus_mounting_pad/conn_config_KLCv3.yaml')
    args = parser.parse_args()

    with open(args.global_config, 'r') as config_stream:
        try:
            configuration = yaml.load(config_stream)
        except yaml.YAMLError as exc:
            print(exc)

    with open(args.series_config, 'r') as config_stream:
        try:
            configuration.update(yaml.load(config_stream))
        except yaml.YAMLError as exc:
            print(exc)

    for pincount in range(2, 17):
        generate_one_footprint(pincount, configuration)
