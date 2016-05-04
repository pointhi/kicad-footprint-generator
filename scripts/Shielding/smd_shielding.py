#!/usr/bin/env python

import sys
import os
import argparse
import yaml

sys.path.append(os.path.join(sys.path[0], "..", ".."))  # load parent path of KicadModTree

from KicadModTree import *  # NOQA
from KicadModTree.nodes.base.Pad import Pad  # NOQA


# https://stackoverflow.com/questions/4265546/python-round-to-nearest-05
def round_to(n, precision):
    correction = 0.5 if n >= 0 else -0.5
    return int(n/precision+correction) * precision


def calculate_pad_spacer(pad_spacer, mirror_spacer):
    pad_spacer_pos = []

    if mirror_spacer:
        for spacer in reversed(pad_spacer):
            pad_spacer_pos.append(spacer * -1)

    pad_spacer_pos += pad_spacer

    return pad_spacer_pos


def create_smd_shielding(name, **kwargs):
    kicad_mod = Footprint(name)

    # init kicad footprint
    kicad_mod.setDescription(kwargs['description'])
    kicad_mod.setTags('Shielding Cabinet')
    kicad_mod.setAttribute('smd')

    # do some pre calculations
    # TODO: when mirror=False, array has to have even number of array elements
    x_pad_positions = calculate_pad_spacer(kwargs['x_pad_spacer'], kwargs.get('x_pad_mirror', True))
    y_pad_positions = calculate_pad_spacer(kwargs['y_pad_spacer'], kwargs.get('y_pad_mirror', True))

    x_pad_min = min(x_pad_positions)
    x_pad_max = max(x_pad_positions)
    y_pad_min = min(y_pad_positions)
    y_pad_max = max(y_pad_positions)

    x_pad_min_center = x_pad_min + kwargs['pads_width']/2.
    x_pad_max_center = x_pad_max - kwargs['pads_width']/2.
    y_pad_min_center = y_pad_min + kwargs['pads_width']/2.
    y_pad_max_center = y_pad_max - kwargs['pads_width']/2.

    # set general values
    kicad_mod.append(Text(type='reference', text='REF**', at=[0, y_pad_min - kwargs['courtjard'] - 0.75], layer='F.SilkS'))
    kicad_mod.append(Text(type='value', text=name, at=[0, y_pad_max + kwargs['courtjard'] + 0.75], layer='F.Fab'))

    # create courtyard
    x_courtjard_min = round_to(x_pad_min - kwargs['courtjard'], 0.05)
    x_courtjard_max = round_to(x_pad_max + kwargs['courtjard'], 0.05)
    y_courtjard_min = round_to(y_pad_min - kwargs['courtjard'], 0.05)
    y_courtjard_max = round_to(y_pad_max + kwargs['courtjard'], 0.05)

    kicad_mod.append(RectLine(start=[x_courtjard_min, y_courtjard_min],
                              end=[x_courtjard_max, y_courtjard_max],
                              layer='F.CrtYd'))

    # create Fabriaction Layer
    kicad_mod.append(RectLine(start=[-kwargs['x_part_size'] / 2., -kwargs['y_part_size'] / 2.],
                              end=[kwargs['x_part_size'] / 2., kwargs['y_part_size'] / 2.],
                              layer='F.Fab'))

    # all pads have this kwargs, so we only write them one
    general_kwargs = {'number': 1,
                      'type': Pad.TYPE_SMT,
                      'shape': Pad.SHAPE_RECT,
                      'layers': ['F.Cu', 'F.Mask']}

    # create edge pads
    kicad_mod.append(Pad(at=[x_pad_min_center, y_pad_min_center],
                         size=[kwargs['pads_width'], kwargs['pads_width']], **general_kwargs))
    kicad_mod.append(Pad(at=[x_pad_max_center, y_pad_min_center],
                         size=[kwargs['pads_width'], kwargs['pads_width']], **general_kwargs))
    kicad_mod.append(Pad(at=[x_pad_max_center, y_pad_max_center],
                         size=[kwargs['pads_width'], kwargs['pads_width']], **general_kwargs))
    kicad_mod.append(Pad(at=[x_pad_min_center, y_pad_max_center],
                         size=[kwargs['pads_width'], kwargs['pads_width']], **general_kwargs))

    # iterate pairwise over pads
    for pad_start, pad_end in zip(x_pad_positions[0::2], x_pad_positions[1::2]):
        if pad_start == x_pad_min:
            pad_start += kwargs['pads_width']
        if pad_end == x_pad_max:
            pad_end -= kwargs['pads_width']

        kicad_mod.append(Pad(at=[(pad_start+pad_end)/2., y_pad_min_center],
                         size=[abs(pad_start-pad_end), kwargs['pads_width']], **general_kwargs))
        kicad_mod.append(Pad(at=[(pad_start+pad_end)/2., y_pad_max_center],
                         size=[abs(pad_start-pad_end), kwargs['pads_width']], **general_kwargs))

    for pad_start, pad_end in zip(y_pad_positions[0::2], y_pad_positions[1::2]):
        if pad_start == y_pad_min:
            pad_start += kwargs['pads_width']
        if pad_end == y_pad_max:
            pad_end -= kwargs['pads_width']

        kicad_mod.append(Pad(at=[x_pad_min_center, (pad_start+pad_end)/2.],
                         size=[kwargs['pads_width'], abs(pad_start-pad_end)], **general_kwargs))
        kicad_mod.append(Pad(at=[x_pad_max_center, (pad_start+pad_end)/2.],
                         size=[kwargs['pads_width'], abs(pad_start-pad_end)], **general_kwargs))

    # write file
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile('{name}.kicad_mod'.format(name=name))


def parse_and_execute_yml_file(filepath):
    with open(filepath, 'r') as stream:
        try:
            yaml_parsed = yaml.load(stream)
            for footprint in yaml_parsed:
                print("generate {name}.kicad_mod".format(name=footprint))
                create_smd_shielding(footprint, **yaml_parsed.get(footprint))
        except yaml.YAMLError as exc:
            print(exc)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse *.kicad_mod.yml file(s) and create matching footprints')
    parser.add_argument('files', metavar='file', type=str, nargs='+',
                        help='yml-files to parse')
    #parser.add_argument('-v', '--verbose', help='show more information when creating footprint', action='store_true')
    # TODO: allow writing into sub file
    args = parser.parse_args()
    for filepath in args.files:
        parse_and_execute_yml_file(filepath)
