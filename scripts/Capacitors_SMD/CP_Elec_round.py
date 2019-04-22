#!/usr/bin/env python

import sys
import os
import argparse
import yaml
import math
from collections import namedtuple

sys.path.append(os.path.join(sys.path[0], "..", ".."))  # load parent path of KicadModTree

from KicadModTree import *  # NOQA
from KicadModTree.nodes.base.Pad import Pad  # NOQA


def create_footprint(name, configuration, **kwargs):
    kicad_mod = Footprint(name)

    # init kicad footprint
    datasheet = ""
    if 'datasheet' in kwargs:
        datasheet = kwargs['datasheet']
    kicad_mod.setDescription(kwargs['description'] + " " + datasheet)
    kicad_mod.setTags('Capacitor Electrolytic')
    kicad_mod.setAttribute('smd')

    # set general values
    text_offset_y = kwargs['width'] / 2. + configuration['courtyard_offset']['default'] + 0.8

    #silkscreen REF**
    silk_text_size = configuration['references'][0]['size']
    silk_text_thickness = silk_text_size[0]*configuration['references'][0]['fontwidth']
    kicad_mod.append(Text(type='reference', text='REF**', at=[0, -text_offset_y], layer='F.SilkS', size=[silk_text_size[0], silk_text_size[1]], thickness= silk_text_thickness))
    #fab value
    fab_text_size = configuration['values'][0]['size']
    fab_text_thickness = fab_text_size[0]*configuration['values'][0]['fontwidth']
    kicad_mod.append(Text(type='value', text=name, at=[0, text_offset_y], layer='F.Fab', size=[fab_text_size[0], fab_text_size[1]], thickness= fab_text_thickness))
    #fab REF**
    fab_text_size = kwargs['diameter']/5.
    fab_text_size = min(fab_text_size, configuration['references'][1]['size_max'][0])
    fab_text_size = max(fab_text_size, configuration['references'][1]['size_min'][0])
    fab_text_thickness = fab_text_size*configuration['references'][1]['thickness_factor']
    kicad_mod.append(Text(type='user', text='%R', at=[0, 0], layer='F.Fab', size=[fab_text_size, fab_text_size], thickness= fab_text_thickness))

    # create fabrication layer
    fab_x = kwargs['length'] / 2.
    fab_y = kwargs['width'] / 2.

    if kwargs['pin1_chamfer'] == 'auto':
        fab_edge = min(fab_x/2, fab_y/2, configuration['fab_pin1_marker_length'])
    else:
        fab_edge = kwargs['pin1_chamfer']
    fab_x_edge = fab_x - fab_edge
    fab_y_edge = fab_y - fab_edge
    kicad_mod.append(Line(start=[fab_x, -fab_y], end=[fab_x, fab_y], layer='F.Fab', width=configuration['fab_line_width']))
    kicad_mod.append(Line(start=[-fab_x_edge, -fab_y], end=[fab_x, -fab_y], layer='F.Fab', width=configuration['fab_line_width']))
    kicad_mod.append(Line(start=[-fab_x_edge, fab_y], end=[fab_x, fab_y], layer='F.Fab', width=configuration['fab_line_width']))
    if fab_edge > 0:
        kicad_mod.append(Line(start=[-fab_x, -fab_y_edge], end=[-fab_x, fab_y_edge], layer='F.Fab', width=configuration['fab_line_width']))
        kicad_mod.append(Line(start=[-fab_x, -fab_y_edge], end=[-fab_x_edge, -fab_y], layer='F.Fab', width=configuration['fab_line_width']))
    kicad_mod.append(Line(start=[-fab_x, fab_y_edge], end=[-fab_x_edge, fab_y], layer='F.Fab', width=configuration['fab_line_width']))
    kicad_mod.append(Circle(center=[0, 0], radius=kwargs['diameter']/2., layer='F.Fab', width=configuration['fab_line_width']))


    #fab polarity marker
    fab_pol_size = kwargs['diameter']/10.
    fab_pol_wing = fab_pol_size/2.
    fab_pol_distance = kwargs['diameter']/2. - fab_pol_wing - configuration['fab_line_width']
    fab_pol_pos_y = fab_text_size/2 + configuration['silk_pad_clearance'] + fab_pol_size
    fab_pol_pos_x = math.sqrt(fab_pol_distance*fab_pol_distance-fab_pol_pos_y*fab_pol_pos_y)
    fab_pol_pos_x = -fab_pol_pos_x
    fab_pol_pos_y = -fab_pol_pos_y
    kicad_mod.append(Line(start=[fab_pol_pos_x-fab_pol_wing, fab_pol_pos_y], end=[fab_pol_pos_x+fab_pol_wing, fab_pol_pos_y], 
        layer='F.Fab', width=configuration['fab_line_width']))
    kicad_mod.append(Line(start=[fab_pol_pos_x, fab_pol_pos_y-fab_pol_wing], end=[fab_pol_pos_x, fab_pol_pos_y+fab_pol_wing], 
        layer='F.Fab', width=configuration['fab_line_width']))


    # create silkscreen
    fab_to_silk_offset = configuration['silk_fab_offset']
    silk_x = kwargs['length'] / 2. + fab_to_silk_offset
    silk_y = kwargs['width'] / 2. + fab_to_silk_offset
    silk_y_start = kwargs['pad_width'] / 2. + configuration['silk_pad_clearance'] + configuration['silk_line_width']/2.
    silk_45deg_offset = fab_to_silk_offset*math.tan(math.radians(22.5))
    silk_x_edge = fab_x - fab_edge + silk_45deg_offset
    silk_y_edge = fab_y - fab_edge + silk_45deg_offset

    kicad_mod.append(Line(start=[silk_x, silk_y], end=[silk_x, silk_y_start], layer='F.SilkS', width=configuration['silk_line_width']))
    kicad_mod.append(Line(start=[silk_x, -silk_y], end=[silk_x, -silk_y_start], layer='F.SilkS', width=configuration['silk_line_width']))
    kicad_mod.append(Line(start=[-silk_x_edge, -silk_y], end=[silk_x, -silk_y], layer='F.SilkS', width=configuration['silk_line_width']))
    kicad_mod.append(Line(start=[-silk_x_edge, silk_y], end=[silk_x, silk_y], layer='F.SilkS', width=configuration['silk_line_width']))

    if silk_y_edge > silk_y_start:
        kicad_mod.append(Line(start=[-silk_x, silk_y_edge], end=[-silk_x, silk_y_start], layer='F.SilkS', width=configuration['silk_line_width']))
        kicad_mod.append(Line(start=[-silk_x, -silk_y_edge], end=[-silk_x, -silk_y_start], layer='F.SilkS', width=configuration['silk_line_width']))

        kicad_mod.append(Line(start=[-silk_x, -silk_y_edge], end=[-silk_x_edge, -silk_y], layer='F.SilkS', width=configuration['silk_line_width']))
        kicad_mod.append(Line(start=[-silk_x, silk_y_edge], end=[-silk_x_edge, silk_y], layer='F.SilkS', width=configuration['silk_line_width']))
    else:
        silk_x_cut = silk_x - (silk_y_start - silk_y_edge) # because of the 45 degree edge we can user a simple apporach
        silk_y_edge_cut = silk_y_start

        kicad_mod.append(Line(start=[-silk_x_cut, -silk_y_edge_cut], end=[-silk_x_edge, -silk_y], layer='F.SilkS', width=configuration['silk_line_width']))
        kicad_mod.append(Line(start=[-silk_x_cut, silk_y_edge_cut], end=[-silk_x_edge, silk_y], layer='F.SilkS', width=configuration['silk_line_width']))

    #silk polarity marker
    silk_pol_size = kwargs['diameter']/8.
    silk_pol_wing = silk_pol_size/2.
    silk_pol_pos_y = silk_y_start + silk_pol_size
    silk_pol_pos_x = silk_x + silk_pol_wing + configuration['silk_line_width']*2
    silk_pol_pos_x = -silk_pol_pos_x
    silk_pol_pos_y = -silk_pol_pos_y
    kicad_mod.append(Line(start=[silk_pol_pos_x-silk_pol_wing, silk_pol_pos_y], end=[silk_pol_pos_x+silk_pol_wing, silk_pol_pos_y], 
        layer='F.SilkS', width=configuration['silk_line_width']))
    kicad_mod.append(Line(start=[silk_pol_pos_x, silk_pol_pos_y-silk_pol_wing], end=[silk_pol_pos_x, silk_pol_pos_y+silk_pol_wing], 
        layer='F.SilkS', width=configuration['silk_line_width']))

    # create courtyard
    courtyard_offset = configuration['courtyard_offset']['default']
    courtyard_x = kwargs['length'] / 2. + courtyard_offset
    courtyard_y = kwargs['width'] / 2. + courtyard_offset
    courtyard_pad_x = kwargs['pad_spacing'] / 2. + kwargs['pad_length'] + courtyard_offset
    courtyard_pad_y = kwargs['pad_width'] / 2. + courtyard_offset
    courtyard_45deg_offset = courtyard_offset*math.tan(math.radians(22.5))
    courtyard_x_edge = fab_x - fab_edge + courtyard_45deg_offset
    courtyard_y_edge = fab_y - fab_edge + courtyard_45deg_offset
    courtyard_x_lower_edge = courtyard_x
    if courtyard_y_edge < courtyard_pad_y:
        courtyard_x_lower_edge = courtyard_x_lower_edge - courtyard_pad_y + courtyard_y_edge
        courtyard_y_edge = courtyard_pad_y
    #rounding
    courtyard_x = float(format(courtyard_x, ".2f"))
    courtyard_y = float(format(courtyard_y, ".2f"))
    courtyard_pad_x = float(format(courtyard_pad_x, ".2f"))
    courtyard_pad_y = float(format(courtyard_pad_y, ".2f"))
    courtyard_x_edge = float(format(courtyard_x_edge, ".2f"))
    courtyard_y_edge = float(format(courtyard_y_edge, ".2f"))
    courtyard_x_lower_edge = float(format(courtyard_x_lower_edge, ".2f"))

    # drawing courtyard
    kicad_mod.append(Line(start=[courtyard_x, -courtyard_y], end=[courtyard_x, -courtyard_pad_y], layer='F.CrtYd', width=configuration['courtyard_line_width']))
    kicad_mod.append(Line(start=[courtyard_x, -courtyard_pad_y], end=[courtyard_pad_x, -courtyard_pad_y], layer='F.CrtYd', width=configuration['courtyard_line_width']))
    kicad_mod.append(Line(start=[courtyard_pad_x, -courtyard_pad_y], end=[courtyard_pad_x, courtyard_pad_y], layer='F.CrtYd', width=configuration['courtyard_line_width']))
    kicad_mod.append(Line(start=[courtyard_pad_x, courtyard_pad_y], end=[courtyard_x, courtyard_pad_y], layer='F.CrtYd', width=configuration['courtyard_line_width']))
    kicad_mod.append(Line(start=[courtyard_x, courtyard_pad_y], end=[courtyard_x, courtyard_y], layer='F.CrtYd', width=configuration['courtyard_line_width']))

    kicad_mod.append(Line(start=[-courtyard_x_edge, courtyard_y], end=[courtyard_x, courtyard_y], layer='F.CrtYd', width=configuration['courtyard_line_width']))
    kicad_mod.append(Line(start=[-courtyard_x_edge, -courtyard_y], end=[courtyard_x, -courtyard_y], layer='F.CrtYd', width=configuration['courtyard_line_width']))
    if fab_edge > 0:
        kicad_mod.append(Line(start=[-courtyard_x_lower_edge, courtyard_y_edge], end=[-courtyard_x_edge, courtyard_y], layer='F.CrtYd', width=configuration['courtyard_line_width']))
        kicad_mod.append(Line(start=[-courtyard_x_lower_edge, -courtyard_y_edge], end=[-courtyard_x_edge, -courtyard_y], layer='F.CrtYd', width=configuration['courtyard_line_width']))
    if courtyard_y_edge > courtyard_pad_y:
        kicad_mod.append(Line(start=[-courtyard_x, -courtyard_y_edge], end=[-courtyard_x, -courtyard_pad_y], layer='F.CrtYd', width=configuration['courtyard_line_width']))
        kicad_mod.append(Line(start=[-courtyard_x, courtyard_pad_y], end=[-courtyard_x, courtyard_y_edge], layer='F.CrtYd', width=configuration['courtyard_line_width']))
    kicad_mod.append(Line(start=[-courtyard_x_lower_edge, -courtyard_pad_y], end=[-courtyard_pad_x, -courtyard_pad_y], layer='F.CrtYd', width=configuration['courtyard_line_width']))
    kicad_mod.append(Line(start=[-courtyard_pad_x, -courtyard_pad_y], end=[-courtyard_pad_x, courtyard_pad_y], layer='F.CrtYd', width=configuration['courtyard_line_width']))
    kicad_mod.append(Line(start=[-courtyard_pad_x, courtyard_pad_y], end=[-courtyard_x_lower_edge, courtyard_pad_y], layer='F.CrtYd', width=configuration['courtyard_line_width']))
    

    # all pads have this kwargs, so we only write them once
    pad_kwargs = {'type': Pad.TYPE_SMT,
                  'shape': Pad.SHAPE_RECT,
                  'layers': ['F.Cu', 'F.Mask', 'F.Paste']}

    # create pads
    x_pad_spacing = kwargs['pad_spacing'] / 2. + kwargs['pad_length'] / 2.
    kicad_mod.append(Pad(number= 1, at=[-x_pad_spacing, 0],
                         size=[kwargs['pad_length'], kwargs['pad_width']], **pad_kwargs))
    kicad_mod.append(Pad(number= 2, at=[x_pad_spacing, 0],
                         size=[kwargs['pad_length'], kwargs['pad_width']], **pad_kwargs))

    lib_name ='Capacitor_SMD'
    # add model
    modelname = name.replace("_HandSoldering", "")
    kicad_mod.append(Model(filename="{model_prefix:s}{lib_name:s}.3dshapes/{name:s}.wrl".format(model_prefix=configuration['3d_model_prefix'], lib_name=lib_name, name=modelname),
                            at=[0, 0, 0], scale=[1, 1, 1], rotate=[0, 0, 0]))

    # write file
    output_dir = '{lib_name:s}.pretty/'.format(lib_name=lib_name)
    if not os.path.isdir(output_dir): #returns false if path does not yet exist!! (Does not check path validity)
        os.makedirs(output_dir)

    filename = '{outdir:s}{fp_name:s}.kicad_mod'.format(outdir=output_dir, fp_name=name)
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile(filename)


def parse_and_execute_yml_file(filepath, configuration):
    with open(filepath, 'r') as stream:
        try:
            yaml_parsed = yaml.safe_load(stream)
            for footprint in yaml_parsed:
                print("generate {name}.kicad_mod".format(name=footprint))
                create_footprint(footprint, configuration , **yaml_parsed.get(footprint))
        except yaml.YAMLError as exc:
            print(exc)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse *.kicad_mod.yml file(s) and create matching footprints')
    parser.add_argument('files', metavar='file', type=str, nargs='+',
                        help='yml-files to parse')
    parser.add_argument('--global_config', type=str, nargs='?', help='the config file defining how the footprint will look like. (KLC)', default='../tools/global_config_files/config_KLCv3.0.yaml')
    #parser.add_argument('-v', '--verbose', help='show more information when creating footprint', action='store_true')
    # TODO: allow writing into sub file
    args = parser.parse_args()
    with open(args.global_config, 'r') as config_stream:
        try:
            configuration = yaml.safe_load(config_stream)
        except yaml.YAMLError as exc:
            print(exc)

    for filepath in args.files:
        parse_and_execute_yml_file(filepath, configuration)
