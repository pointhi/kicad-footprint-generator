#!/usr/bin/env python

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

sys.path.append(os.path.join(sys.path[0], "..", "..", ".."))  # load parent path of KicadModTree
from math import sqrt
import argparse
import yaml
from helpers import *
from KicadModTree import *

sys.path.append(os.path.join(sys.path[0], "..", "..", "tools"))  # load parent path of tools
from footprint_text_fields import addTextFields

manufacturer = ''
category = 'SOIC'
package = 'SOP'
pitch = 1.27
size_y = 12.5
size_x = 7
pincount_range = [18]
pad_size = [1.725, 0.6]
datasheet = 'https://toshiba.semicon-storage.com/info/docget.jsp?did=30523'
mpn = ''
is_smd = True

def generate_one_footprint(pincount, configuration):
    footprint_name = configuration['fp_name_format_string'].format(
        man=manufacturer,
        mpn=mpn,
        pkg=package,
        pincount=pincount,
        size_y=size_y,
        size_x=size_x,
        pitch=pitch
        )
    footprint_name = footprint_name.replace('__','_').lstrip('_')

    print(footprint_name)

    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription("{manufacturer} {mpn} {package}, {pincount} Pin ({datasheet}), generated with kicad-footprint-generator {scriptname}".format(
        manufacturer = manufacturer,
        package = package,
        mpn = mpn, 
        pincount = pincount,
        datasheet = datasheet,
        scriptname = os.path.basename(__file__)).replace("  ", " "))

    kicad_mod.setTags(configuration['keyword_fp_string'].format(
        category=category,
        package=package,
        man=manufacturer,
        ))

    kicad_mod.setAttribute('smd')

    # ########################## Dimensions ##############################
    

    pad1_x = -size_x/2-pad_size[0]/2
    pad1_y = -((pincount/2)-1)/2*pitch
    padN_x = +size_x/2+pad_size[0]/2
    padN_y = pad1_y


    body_edge = {
        'left': -size_x/2,
        'right': size_x/2,
        'top': -size_y/2,
        'bottom': size_y/2
        }

    bounding_box = {
        'left': pad1_x - pad_size[0]/2,
        'right': padN_x + pad_size[0]/2,
        'top': body_edge['top'],
        'bottom': body_edge['bottom'],
    }

    # # ############################# Pads ##################################
       
    # Pads
    kicad_mod.append(PadArray(start=[pad1_x, pad1_y], initial=1,
        pincount=int(pincount/2), increment=1,  y_spacing=pitch, size=pad_size,
        type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, layers=Pad.LAYERS_SMT, drill=None))
    kicad_mod.append(PadArray(start=[padN_x, padN_y], initial=pincount,
        pincount=int(pincount/2), increment=-1, y_spacing=pitch, size=pad_size,
        type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, layers=Pad.LAYERS_SMT, drill=None))

    # # ######################## Fabrication Layer ###########################

    fab_bevel_size = min(configuration['fab_bevel_size_absolute'], configuration['fab_bevel_size_relative']*max(size_x, size_y))

    poly_fab = [
        {'x': body_edge['left']+fab_bevel_size, 'y': body_edge['top']},
        {'x': body_edge['right'], 'y': body_edge['top']},
        {'x': body_edge['right'], 'y': body_edge['bottom']},
        {'x': body_edge['left'], 'y': body_edge['bottom']},
        {'x': body_edge['left'], 'y': body_edge['top']+fab_bevel_size},
        {'x': body_edge['left']+fab_bevel_size, 'y': body_edge['top']},
    ]

    kicad_mod.append(PolygoneLine(
        polygone=poly_fab,
        width=configuration['fab_line_width'],
        layer="F.Fab"))

    # ############################ SilkS ##################################

    silk_pad_offset = configuration['silk_pad_clearance'] + configuration['silk_line_width']/2
    silk_offset = configuration['silk_fab_offset']

    silk_xp1_top = pad1_y - pad_size[1]/2 - silk_pad_offset

    poly_silk_top = [
        {'x': pad1_x - pad_size[0]/2 , 'y': silk_xp1_top},
        {'x': body_edge['left'] - silk_offset, 'y': silk_xp1_top},
        {'x': body_edge['left'] - silk_offset, 'y': body_edge['top'] - silk_offset},
        {'x': body_edge['right'] + silk_offset, 'y': body_edge['top'] - silk_offset},
        {'x': body_edge['right'] + silk_offset, 'y': silk_xp1_top},
    ]

    kicad_mod.append(PolygoneLine(polygone=poly_silk_top,
    width=configuration['silk_line_width'], layer="F.SilkS"))        

    silk_xpM_bottom = pad1_y + pitch*((pincount/2)-1)+ pad_size[1]/2 + silk_pad_offset

    poly_silk_bottom = [
        {'x': body_edge['left'] - silk_offset, 'y': silk_xpM_bottom},
        {'x': body_edge['left'] - silk_offset, 'y': body_edge['bottom'] + silk_offset},
        {'x': body_edge['right'] + silk_offset, 'y': body_edge['bottom'] + silk_offset},
        {'x': body_edge['right'] + silk_offset, 'y': silk_xpM_bottom},
    ]

    kicad_mod.append(PolygoneLine(polygone=poly_silk_bottom,
    width=configuration['silk_line_width'], layer="F.SilkS"))        

    # # ############################ CrtYd ##################################

    courtyard_offset = configuration['courtyard_offset']['default']
    courtyard_grid = configuration['courtyard_grid']

    courtyard_top = roundToBase(bounding_box['top'] - courtyard_offset, courtyard_grid)
    courtyard_bottom = roundToBase(bounding_box['bottom'] + courtyard_offset, courtyard_grid)
    courtyard_left = roundToBase(bounding_box['left'] - courtyard_offset, courtyard_grid)
    courtyard_right = roundToBase(bounding_box['right'] + courtyard_offset, courtyard_grid)

    poly_cy = [
        {'x': courtyard_left, 'y': courtyard_top},
        {'x': courtyard_right, 'y': courtyard_top},
        {'x': courtyard_right, 'y': courtyard_bottom},
        {'x': courtyard_left, 'y': courtyard_bottom},
        {'x': courtyard_left, 'y': courtyard_top},
    ]
    kicad_mod.append(PolygoneLine(polygone=poly_cy,
        layer='F.CrtYd', width=configuration['courtyard_line_width']))

    # ######################### Text Fields ###############################

    addTextFields(kicad_mod=kicad_mod, configuration=configuration, body_edges=body_edge,
        courtyard={'top': courtyard_top, 'bottom': courtyard_bottom}, fp_name=footprint_name, text_y_inside_position='bottom')

    ##################### Output and 3d model ############################

    model3d_path_prefix = configuration.get('3d_model_prefix','${KISYS3DMOD}/')

    lib_name = configuration['lib_name_format_string'].format(category=category)
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
    parser.add_argument('--series_config', type=str, nargs='?', help='the config file defining series parameters.', default='../package_config_KLCv3.yaml')
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

    for pincount in pincount_range:
        generate_one_footprint(pincount, configuration)
