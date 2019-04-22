#!/usr/bin/env python

import sys
import os
import argparse
import yaml
import math

sys.path.append(os.path.join(sys.path[0], "..", ".."))  # load parent path of KicadModTree

from KicadModTree import *  # NOQA
from KicadModTree.nodes.base.Pad import Pad  # NOQA


# https://stackoverflow.com/questions/4265546/python-round-to-nearest-05
def round_to(n, precision):
    correction = 0.5 if n >= 0 else -0.5
    return int(n/precision+correction) * precision


def create_footprint(name, **kwargs):
    kicad_mod = Footprint(name)

    # init kicad footprint
    kicad_mod.setDescription(kwargs['description'])
    kicad_mod.setTags('Mounting Hole')

    # load some general values
    hole_x = float(kwargs['hole_x'])
    hole_y = float(kwargs['hole_y'])
    anular_ring = float(kwargs['anular_ring'])
    courtjard = float(kwargs['courtjard'])
    create_via = kwargs['via']

    pad_x = hole_x + 2*anular_ring
    pad_y = hole_y + 2*anular_ring
    courtjard_x = pad_x + 2*courtjard
    courtjard_y = pad_y + 2*courtjard

    # set general values
    kicad_mod.append(Text(type='reference', text='REF**', at=[0, -courtjard_y/2 - 0.75], layer='F.SilkS'))
    kicad_mod.append(Text(type='value', text=name, at=[0, courtjard_y/2 + 0.75], layer='F.Fab'))

    # create courtyard
    if hole_x == hole_y:
        kicad_mod.append(Circle(center=[0, 0], radius=courtjard_x/2., layer='F.CrtYd'))
    elif hole_x > hole_y:
        courtjard_length_x = courtjard_x - courtjard_y
        kicad_mod.append(RectLine(start=[courtjard_length_x / 2, courtjard_y / 2], end=[-courtjard_length_x / 2, courtjard_y / 2],
                                  layer='F.CrtYd'))
        kicad_mod.append(RectLine(start=[courtjard_length_x / 2, -courtjard_y / 2], end=[-courtjard_length_x / 2, -courtjard_y / 2],
                     layer='F.CrtYd'))
        kicad_mod.append(Arc(center=[courtjard_length_x/2 , 0], start=[courtjard_length_x / 2, -courtjard_y / 2], angle=180, layer='F.CrtYd'))
        kicad_mod.append(Arc(center=[-courtjard_length_x / 2, 0], start=[-courtjard_length_x / 2, courtjard_y / 2], angle=180, layer='F.CrtYd'))
    else: # hole_x < hole_y
        courtjard_length_y = courtjard_y - courtjard_x
        kicad_mod.append(
            RectLine(start=[courtjard_x / 2, courtjard_length_y / 2], end=[courtjard_x / 2, -courtjard_length_y / 2],
                     layer='F.CrtYd'))
        kicad_mod.append(
            RectLine(start=[-courtjard_x / 2, courtjard_length_y / 2], end=[-courtjard_x / 2, -courtjard_length_y / 2],
                     layer='F.CrtYd'))
        kicad_mod.append(
            Arc(center=[0, courtjard_length_y / 2], start=[courtjard_x / 2, courtjard_length_y / 2], angle=180,
                layer='F.CrtYd'))
        kicad_mod.append(
            Arc(center=[0, -courtjard_length_y / 2], start=[-courtjard_x / 2, -courtjard_length_y / 2], angle=180,
                layer='F.CrtYd'))

    # create pads
    pad_kwargs = {
        'number': 1,
        'type': Pad.TYPE_THT,
        'at': [0, 0],
        'size': [pad_x, pad_y],
        'layers': ['*.Cu', '*.Mask']
    }
    if hole_x == hole_y:
        kicad_mod.append(Pad(**pad_kwargs, shape=Pad.SHAPE_CIRCLE, drill=hole_x))
    else:
        kicad_mod.append(Pad(**pad_kwargs, shape=Pad.SHAPE_OVAL, drill=[hole_x, hole_y]))

    # create via's
    if create_via:
        via_count = int(kwargs['via_count'])
        via_diameter = float(kwargs['via_diameter'])
        x_size = hole_x + anular_ring
        y_size = hole_y + anular_ring

        circle_radius = min(x_size, y_size) / 2
        circle_scope = min(x_size, y_size) * math.pi

        if hole_x > hole_y:
            line_scope_x = 2 * (x_size - y_size)
            line_scope_y = 0
        else:
            line_scope_x = 0
            line_scope_y = 2 * (y_size - x_size)
        line_scope = line_scope_x + line_scope_y
        vias_scope = circle_scope + line_scope

        for step in range(via_count):
            scope_step = (vias_scope / via_count * step - line_scope_y / 4 + vias_scope) % vias_scope # align on right center

            if scope_step <= circle_scope / 4:
                local_scope_pos = scope_step
                circle_pos = local_scope_pos / circle_scope * 2 * math.pi
                step_x = math.cos(circle_pos) * circle_radius + line_scope_x / 4
                step_y = math.sin(circle_pos) * circle_radius + line_scope_y / 4
            elif scope_step <= circle_scope / 4 + line_scope_x / 2:
                local_scope_pos = scope_step - circle_scope / 4
                step_x = line_scope_x / 4 - local_scope_pos
                step_y = y_size / 2
            elif scope_step <= circle_scope / 2 + line_scope_x / 2:
                local_scope_pos = scope_step - line_scope_x / 2  # angle of circle already included
                circle_pos = local_scope_pos / circle_scope * 2 * math.pi
                step_x = math.cos(circle_pos) * circle_radius - line_scope_x / 4
                step_y = math.sin(circle_pos) * circle_radius + line_scope_y / 4
            elif scope_step <= circle_scope / 2 + line_scope_x / 2 + line_scope_y / 2:
                local_scope_pos = scope_step - circle_scope / 2 - line_scope_x / 2
                step_x = -x_size / 2
                step_y = line_scope_y / 4 - local_scope_pos
            elif scope_step <= 3 * circle_scope / 4 + line_scope_x / 2 + line_scope_y / 2:
                local_scope_pos = scope_step - line_scope_x / 2 -  line_scope_y / 2 # angle of circle already included
                circle_pos = local_scope_pos / circle_scope * 2 * math.pi
                step_x = math.cos(circle_pos) * circle_radius - line_scope_x / 4
                step_y = math.sin(circle_pos) * circle_radius - line_scope_y / 4
            elif scope_step <= 3 * circle_scope / 4 + line_scope_x + line_scope_y / 2:
                local_scope_pos = scope_step - 3 * circle_scope / 4 - line_scope_x / 2 - line_scope_y / 2
                step_x = -line_scope_x / 4 + local_scope_pos
                step_y = -y_size / 2
            elif scope_step <= circle_scope + line_scope_x + line_scope_y / 2:
                local_scope_pos = scope_step - line_scope_x - line_scope_y / 2  # angle of circle already included
                circle_pos = local_scope_pos / circle_scope * 2 * math.pi
                step_x = math.cos(circle_pos) * circle_radius + line_scope_x / 4
                step_y = math.sin(circle_pos) * circle_radius - line_scope_y / 4
            elif scope_step < circle_scope + line_scope_x + line_scope_y:
                local_scope_pos = scope_step - circle_scope - line_scope_x - line_scope_y / 2
                step_x = x_size / 2
                step_y = -line_scope_y / 4 + local_scope_pos
            else: # error
                raise "invalid scope_step"

            kicad_mod.append(Pad(number=1, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
                                 at=[step_x, step_y], size=[via_diameter+0.1, via_diameter+0.1], drill=via_diameter, layers=['*.Cu', '*.Mask']))

    # write file
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile('{name}.kicad_mod'.format(name=name))


def parse_and_execute_yml_file(filepath):
    with open(filepath, 'r') as stream:
        try:
            yaml_parsed = yaml.safe_load(stream)
            for footprint in yaml_parsed:
                print("generate {name}.kicad_mod".format(name=footprint))
                create_footprint(footprint, **yaml_parsed.get(footprint))
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
