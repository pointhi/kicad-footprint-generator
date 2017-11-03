#!/usr/bin/env python

import sys
import os
import argparse
import yaml
import math

sys.path.append(os.path.join(sys.path[0], "..", ".."))  # load parent path of KicadModTree

from KicadModTree import *  # NOQA
from KicadModTree.nodes.base.Pad import Pad  # NOQA

# def create_footprint(name, **kwargs):
#     kicad_mod = Footprint(name)
#
#     # init kicad footprint
#     kicad_mod.setDescription(kwargs['description'])
#     kicad_mod.setTags('Capacitor Electrolytic')
#     kicad_mod.setAttribute('smd')
#
#     # set general values
#     text_offset_y = kwargs['width'] / 2. + kwargs['courtjard'] + 0.8
#
#     kicad_mod.append(Text(type='reference', text='REF**', at=[0, -text_offset_y], layer='F.SilkS'))
#     kicad_mod.append(Text(type='value', text=name, at=[0, text_offset_y], layer='F.Fab'))
#
#     # create fabrication layer
#     fab_x = kwargs['length'] / 2.
#     fab_y = kwargs['width'] / 2.
#     fab_edge = 1
#     fab_x_edge = fab_x - fab_edge
#     fab_y_edge = fab_y - fab_edge
#     kicad_mod.append(Line(start=[fab_x, -fab_y], end=[fab_x, fab_y], layer='F.Fab'))
#     kicad_mod.append(Line(start=[-fab_x_edge, -fab_y], end=[fab_x, -fab_y], layer='F.Fab'))
#     kicad_mod.append(Line(start=[-fab_x_edge, fab_y], end=[fab_x, fab_y], layer='F.Fab'))
#     kicad_mod.append(Line(start=[-fab_x, -fab_y_edge], end=[-fab_x, fab_y_edge], layer='F.Fab'))
#
#     kicad_mod.append(Line(start=[-fab_x, -fab_y_edge], end=[-fab_x_edge, -fab_y], layer='F.Fab'))
#     kicad_mod.append(Line(start=[-fab_x, fab_y_edge], end=[-fab_x_edge, fab_y], layer='F.Fab'))
#
#     fab_text_x = kwargs['pad_spacing'] / 2. + kwargs['pad_length'] / 4.
#     kicad_mod.append(Text(type='user', text='+', at=[-fab_text_x, 0], layer='F.Fab'))
#
#     # create silkscreen
#     silk_x = kwargs['length'] / 2. + 0.11
#     silk_y = kwargs['width'] / 2. + 0.11
#     silk_y_start = kwargs['pad_width'] / 2. + 0.3
#     silk_x_edge = fab_x - fab_edge + 0.05
#     silk_y_edge = fab_y - fab_edge + 0.05
#
#     kicad_mod.append(Line(start=[silk_x, silk_y], end=[silk_x, silk_y_start], layer='F.SilkS'))
#     kicad_mod.append(Line(start=[silk_x, -silk_y], end=[silk_x, -silk_y_start], layer='F.SilkS'))
#     kicad_mod.append(Line(start=[-silk_x_edge, -silk_y], end=[silk_x, -silk_y], layer='F.SilkS'))
#     kicad_mod.append(Line(start=[-silk_x_edge, silk_y], end=[silk_x, silk_y], layer='F.SilkS'))
#
#     if silk_y_edge > silk_y_start:
#         kicad_mod.append(Line(start=[-silk_x, silk_y_edge], end=[-silk_x, silk_y_start], layer='F.SilkS'))
#         kicad_mod.append(Line(start=[-silk_x, -silk_y_edge], end=[-silk_x, -silk_y_start], layer='F.SilkS'))
#
#         kicad_mod.append(Line(start=[-silk_x, -silk_y_edge], end=[-silk_x_edge, -silk_y], layer='F.SilkS'))
#         kicad_mod.append(Line(start=[-silk_x, silk_y_edge], end=[-silk_x_edge, silk_y], layer='F.SilkS'))
#     else:
#         silk_x_cut = silk_x - (silk_y_start - silk_y_edge) # because of the 45 degree edge we can user a simple apporach
#         silk_y_edge_cut = silk_y_start
#
#         kicad_mod.append(Line(start=[-silk_x_cut, -silk_y_edge_cut], end=[-silk_x_edge, -silk_y], layer='F.SilkS'))
#         kicad_mod.append(Line(start=[-silk_x_cut, silk_y_edge_cut], end=[-silk_x_edge, silk_y], layer='F.SilkS'))
#
#     silk_cane_x_start = math.cos(math.asin(silk_y_start / (kwargs['diameter'] / 2.))) * (kwargs['diameter'] / 2.)
#     silk_cane_angle = 180 - math.acos(2 * (silk_cane_x_start / kwargs['diameter'])) * 360. / math.pi # TODO 180
#
#     kicad_mod.append(Arc(center=[0, 0], start=[-silk_cane_x_start, -silk_y_start], angle=silk_cane_angle,layer='F.SilkS'))
#     kicad_mod.append(Arc(center=[0, 0], start=[silk_cane_x_start, silk_y_start], angle=silk_cane_angle, layer='F.SilkS'))
#
#     # create courtyard
#     courtjard_x = kwargs['pad_spacing'] / 2. + kwargs['pad_length'] + kwargs['courtjard']
#     courtjard_y = kwargs['width'] / 2. + kwargs['courtjard']
#
#     kicad_mod.append(RectLine(start=[courtjard_x, courtjard_y], end=[-courtjard_x, -courtjard_y], layer='F.CrtYd'))
#
#     # '+' sign on silkscreen
#     silk_text_x = courtjard_x- 0.6
#     silk_text_y = courtjard_y - 0.6
#     kicad_mod.append(Text(type='user', text='+', at=[-silk_text_x, silk_text_y], layer='F.SilkS'))
#
#     # all pads have this kwargs, so we only write them once
#     pad_kwargs = {'type': Pad.TYPE_SMT,
#                   'shape': Pad.SHAPE_RECT,
#                   'layers': ['F.Cu', 'F.Mask', 'F.Paste']}
#
#     # create pads
#     x_pad_spacing = kwargs['pad_spacing'] / 2. + kwargs['pad_length'] / 2.
#     kicad_mod.append(Pad(number= 1, at=[-x_pad_spacing, 0],
#                          size=[kwargs['pad_length'], kwargs['pad_width']], **pad_kwargs))
#     kicad_mod.append(Pad(number= 2, at=[x_pad_spacing, 0],
#                          size=[kwargs['pad_length'], kwargs['pad_width']], **pad_kwargs))
#
#     # add model
#     kicad_mod.append(Model(filename="example.3dshapes/{name}.wrl".format(name=name),
#                             at=[0, 0, 0], scale=[1, 1, 1], rotate=[0, 0, 0]))
#
#     # write file
#     file_handler = KicadFileHandler(kicad_mod)
#     file_handler.writeFile('{name}.kicad_mod'.format(name=name))

F = 0.1
P = 0.05

def roundToBase(value, base):
	return round(value/base) * base

def calc_pad_details(device_params, ipc_data, ipc_round_base):
    # Zmax = Lmin + 2JT + √(CL^2 + F^2 + P^2)
    # Gmin = Smax − 2JH − √(CS^2 + F^2 + P^2)
    # Xmax = Wmin + 2JS + √(CW^2 + F^2 + P^2)

    length_tolerance = device_params['body_length_max']-device_params['body_length_min']
    width_tolerance = device_params['body_width_max']-device_params['body_width_min']
    spacing_tolerance = device_params['terminator_spacing_max']-device_params['terminator_spacing_min']

    Zmax = device_params['body_length_min'] + 2*ipc_data['toe'] + math.sqrt(length_tolerance**2 + F**2 + P**2)
    Gmin = device_params['terminator_spacing_max'] - 2*ipc_data['heel'] - math.sqrt(spacing_tolerance**2 + F**2 + P**2)
    Xmax = device_params['body_width_min'] + 2*ipc_data['side'] + math.sqrt(width_tolerance**2 + F**2 + P**2)

    Zmax = roundToBase(Zmax, ipc_round_base['toe'])
    Gmin = roundToBase(Gmin, ipc_round_base['heel'])
    Xmax = roundToBase(Xmax, ipc_round_base['side'])

    return {'at':[(Zmax+Gmin)/4,0], 'size':[(Zmax-Gmin)/2,Xmax], 'Z':Zmax,'G':Gmin,'W':Xmax}

def parse_and_execute_yml_file(filepath, ipc_defintions, package_size_defintions):
    with open(filepath, 'r') as stream:
        try:
            footprint_group_definitions = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    for group_name in footprint_group_definitions:
        #print(device_group)
        footprint_group_data = footprint_group_definitions[group_name]
        for size_name in package_size_defintions:
            device_size_data = package_size_defintions[size_name]
            print(group_name + ' ' + size_name)
            ipc_reference = device_size_data['ipc_reference']
            ipc_density = footprint_group_data['ipc_density']
            ipc_data_set = ipc_defintions[ipc_reference][ipc_density]
            ipc_round_base = ipc_defintions[ipc_reference]['round_base']
            print(calc_pad_details(device_size_data, ipc_data_set, ipc_round_base))
            #print(calc_pad_details())
            #print("generate {name}.kicad_mod".format(name=footprint))
        #create_footprint(footprint, **yaml_parsed.get(footprint))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse *.kicad_mod.yml file(s) and create matching footprints')
    parser.add_argument('files', metavar='file', type=str, nargs='+',
                        help='yml-files to parse')
    ipc_doc = 'ipc.yaml'
    with open(ipc_doc, 'r') as ipc_stream:
        try:
            ipc_defintions = yaml.load(ipc_stream)
        except yaml.YAMLError as exc:
            print(exc)

    device_size_doc = 'device_sizes.yaml'
    with open(device_size_doc, 'r') as size_stream:
        try:
            package_size_defintions = yaml.load(size_stream)
        except yaml.YAMLError as exc:
            print(exc)

    # print(ipc_defintions['ipc_spec_smaller_0603']['nominal'])
    #parser.add_argument('-v', '--verbose', help='show more information when creating footprint', action='store_true')
    # TODO: allow writing into sub file
    args = parser.parse_args()
    for filepath in args.files:
        parse_and_execute_yml_file(filepath, ipc_defintions, package_size_defintions)
