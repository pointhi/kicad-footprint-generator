#!/usr/bin/env python

import sys
import os

sys.path.append(os.path.join(sys.path[0], "..", ".."))  # load parent path of KicadModTree

from KicadModTree import *  # NOQA
from KicadModTree.nodes.base.Pad import Pad  # NOQA


def smd_chip(args):
    # init kicad footprint
    kicad_mod = Footprint(args['name'])
    kicad_mod.setDescription(args['description'])
    kicad_mod.setTags(args['tags'])
    kicad_mod.setAttribute('smd')

    # set general values
    text_x = 0.
    text_y = max([args['pad_y'] / 2., args['part_y'] / 2.]) + args['courtyard'] + 0.75

    kicad_mod.append(Text(type='reference', text='REF**', at=[text_x, -text_y], layer='F.SilkS'))
    kicad_mod.append(Text(type='user', text='%R', at=[text_x, -text_y], layer='F.Fab'))
    kicad_mod.append(Text(type='value', text=args['name'], at=[text_x, text_y], layer='F.Fab'))

    # create silkscreen
    silk_x = args['part_x'] / 2.
    silk_y = max([args['pad_y'] / 2., args['part_y'] / 2.]) + min(max(0.15, args['courtyard'] - 0.05), 0.2)

    kicad_mod.append(Line(start=[silk_x, silk_y], end=[-silk_x, silk_y], layer='F.SilkS'))
    kicad_mod.append(Line(start=[silk_x, -silk_y], end=[-silk_x, -silk_y], layer='F.SilkS'))

    # create fabrication layer
    kicad_mod.append(RectLine(start=[args['part_x'] / 2., args['part_y'] / 2.],
                              end=[-args['part_x'] / 2., -args['part_y'] / 2.],
                              layer='F.Fab'))

    # create courtyard
    courtyard_x = args['courtyard'] + max([args['pad_spacing'] / 2. + args['pad_x'], args['part_x'] / 2.])
    courtyard_y = args['courtyard'] + max([args['pad_y'] / 2., args['part_y'] / 2.])

    kicad_mod.append(RectLine(start=[courtyard_x, courtyard_y],
                              end=[-courtyard_x, -courtyard_y],
                              layer='F.CrtYd'))

    # create pads
    pad_settings = {'type': Pad.TYPE_SMT,
                    'shape': Pad.SHAPE_RECT,
                    'size': [args['pad_x'], args['pad_y']],
                    'layers': Pad.LAYERS_SMT}

    pad_x_center = (args['pad_spacing'] + args['pad_x'])  / 2.

    kicad_mod.append(Pad(number=1, at=[-pad_x_center, 0], **pad_settings))
    kicad_mod.append(Pad(number=2, at=[pad_x_center, 0], **pad_settings))

    # add model
    kicad_mod.append(Model(filename="{model_dir}.3dshapes/{name}.wrl".format(**args),
                           at=[0, 0, 0], scale=[1, 1, 1], rotate=[0, 0, 0]))

    # write file
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile('{}.kicad_mod'.format(args['name']))


if __name__ == '__main__':
    parser = ModArgparser(smd_chip)
    parser.add_parameter("name", type=str, required=True)  # the root node of .yml files is parsed as name
    parser.add_parameter("description", type=str, required=True)
    parser.add_parameter("tags", type=str, required=True)
    parser.add_parameter("model_dir", type=str, required=True)
    parser.add_parameter("courtyard", type=float, required=False, default=0.25)
    parser.add_parameter("part_x", type=float, required=True)
    parser.add_parameter("part_y", type=float, required=True)
    parser.add_parameter("pad_x", type=float, required=True)
    parser.add_parameter("pad_y", type=float, required=True)
    parser.add_parameter("pad_spacing", type=float, required=True)

    parser.run()  # now run our script which handles the whole part of parsing the files
