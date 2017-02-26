#!/usr/bin/env python

import sys
import os

sys.path.append(os.path.join(sys.path[0], "..", ".."))  # load parent path of KicadModTree

from KicadModTree import *  # NOQA
from KicadModTree.nodes.base.Pad import Pad  # NOQA


def buzzer_round_tht(args):
    # some variables
    buzzer_center = args['pad_spacing'] / 2.
    buzzer_radius = args['diameter'] / 2.

    # init kicad footprint
    kicad_mod = Footprint(args['name'])
    kicad_mod.setDescription(args['datasheet'])
    kicad_mod.setTags("buzzer round tht")

    # set general values
    kicad_mod.append(Text(type='reference', text='REF**', at=[buzzer_center, -buzzer_radius - 1], layer='F.SilkS'))
    kicad_mod.append(Text(type='user', text='%R', at=[buzzer_center, -buzzer_radius - 1], layer='F.Fab'))
    kicad_mod.append(Text(type='value', text=args['name'], at=[buzzer_center, buzzer_radius + 1], layer='F.Fab'))

    # create silkscreen
    kicad_mod.append(Circle(center=[buzzer_center, 0], radius=buzzer_radius + 0.1, layer='F.SilkS'))

    kicad_mod.append(Text(type='user', text='+', at=[0, -args['pad_size'] / 2 - 1], layer='F.SilkS'))
    kicad_mod.append(Text(type='user', text='+', at=[0, -args['pad_size']/2 - 1], layer='F.Fab'))

    # create fabrication layer
    kicad_mod.append(Circle(center=[buzzer_center, 0], radius=buzzer_radius, layer='F.Fab'))

    # create courtyard
    kicad_mod.append(Circle(center=[buzzer_center, 0], radius=buzzer_radius + args['courtyard'], layer='F.CrtYd'))

    # create pads
    kicad_mod.append(Pad(number=1, type=Pad.TYPE_THT, shape=Pad.SHAPE_RECT,
                         at=[0, 0], size=args['pad_size'], drill=args['hole_size'], layers=Pad.LAYERS_THT))
    kicad_mod.append(Pad(number=2, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
                         at=[args['pad_spacing'], 0], size=args['pad_size'], drill=args['hole_size'], layers=Pad.LAYERS_THT))

    # write file
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile('{}.kicad_mod'.format(args['name']))


if __name__ == '__main__':
    parser = ModArgparser(buzzer_round_tht)
    parser.add_parameter("name", type=str, required=True)  # the root node of .yml files is parsed as name
    parser.add_parameter("datasheet", type=str, required=False)
    parser.add_parameter("courtyard", type=float, required=False, default=0.25)
    parser.add_parameter("diameter", type=float, required=True)
    parser.add_parameter("hole_size", type=float, required=True)
    parser.add_parameter("pad_size", type=float, required=True)
    parser.add_parameter("pad_spacing", type=float, required=True)

    parser.run()  # now run our script which handles the whole part of parsing the files
