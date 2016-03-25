#!/usr/bin/env python

import sys
import os

sys.path.append(os.path.join(sys.path[0], "..", ".."))  # load parent path of  KicadModTree

from KicadModTree import *  # NOQA
from KicadModTree.nodes.base.Pad import Pad  # NOQA


def create_shielding(name, outer_size, size,
                     attachment_width, attachment_length, attachment_positions, outer_attachment_length):

    kicad_mod = Footprint(name)

    # init kicad footprint
    kicad_mod.setDescription('WE-SHC Shielding Cabinet SMD {size}x{size}mm'.format(size=size))
    kicad_mod.setTags('Shielding Cabinet')
    kicad_mod.setAttribute('smd')

    # set general values
    kicad_mod.append(Text(type='reference', text='REF**', at=[0, -outer_size / 2. - 1], layer='F.SilkS'))
    kicad_mod.append(Text(type='value', text=name, at=[0, outer_size / 2. + 1], layer='F.Fab'))

    # create courtyard
    kicad_mod.append(RectLine(start=[-outer_size / 2. - 0.25, -outer_size / 2. - 0.25],
                              end=[outer_size / 2. + 0.25, outer_size / 2. + 0.25],
                              layer='F.CrtYd'))

    # create Fabriaction Layer
    kicad_mod.append(RectLine(start=[-size / 2., -size / 2.],
                              end=[size / 2., size / 2.],
                              layer='F.Fab'))

    outer_pointing_pos = outer_size / 2. - attachment_width / 2.

    general_kwargs = {'number': 1,
                      'type': Pad.TYPE_SMT,
                      'shape': Pad.SHAPE_RECT,
                      'layers': ['F.Cu', 'F.Mask']}

    vertical_kwargs = {'number': 1,
                       'type': Pad.TYPE_SMT,
                       'shape': Pad.SHAPE_RECT,
                       'size': [attachment_width, attachment_length],
                       'layers': ['F.Cu', 'F.Mask']}

    horizontal_kwargs = {'number': 1,
                         'type': Pad.TYPE_SMT,
                         'shape': Pad.SHAPE_RECT,
                         'size': [attachment_length, attachment_width],
                         'layers': ['F.Cu', 'F.Mask']}

    # create inner pads
    for position in attachment_positions:
        kicad_mod.append(Pad(at=[outer_pointing_pos, position / 2.], **vertical_kwargs))
        kicad_mod.append(Pad(at=[outer_pointing_pos, -position / 2.], **vertical_kwargs))
        kicad_mod.append(Pad(at=[-outer_pointing_pos, position / 2.], **vertical_kwargs))
        kicad_mod.append(Pad(at=[-outer_pointing_pos, -position / 2.], **vertical_kwargs))

        kicad_mod.append(Pad(at=[position / 2., outer_pointing_pos], **horizontal_kwargs))
        kicad_mod.append(Pad(at=[position / 2., -outer_pointing_pos], **horizontal_kwargs))
        kicad_mod.append(Pad(at=[-position / 2., outer_pointing_pos], **horizontal_kwargs))
        kicad_mod.append(Pad(at=[-position / 2., -outer_pointing_pos], **horizontal_kwargs))

    # create edge pads
    kicad_mod.append(Pad(at=[outer_pointing_pos, outer_pointing_pos],
                         size=[attachment_width, attachment_width], **general_kwargs))
    kicad_mod.append(Pad(at=[outer_pointing_pos, -outer_pointing_pos],
                         size=[attachment_width, attachment_width], **general_kwargs))
    kicad_mod.append(Pad(at=[-outer_pointing_pos, outer_pointing_pos],
                         size=[attachment_width, attachment_width], **general_kwargs))
    kicad_mod.append(Pad(at=[-outer_pointing_pos, -outer_pointing_pos],
                         size=[attachment_width, attachment_width], **general_kwargs))

    inner_edge_pos = outer_size / 2 - attachment_width - (outer_attachment_length - attachment_width) / 2.
    inner_edge_length = outer_attachment_length-attachment_width

    kicad_mod.append(Pad(at=[inner_edge_pos, outer_pointing_pos],
                         size=[inner_edge_length, attachment_width], **general_kwargs))
    kicad_mod.append(Pad(at=[inner_edge_pos, -outer_pointing_pos],
                         size=[inner_edge_length, attachment_width], **general_kwargs))
    kicad_mod.append(Pad(at=[-inner_edge_pos, outer_pointing_pos],
                         size=[inner_edge_length, attachment_width], **general_kwargs))
    kicad_mod.append(Pad(at=[-inner_edge_pos, -outer_pointing_pos],
                         size=[inner_edge_length, attachment_width], **general_kwargs))

    kicad_mod.append(Pad(at=[outer_pointing_pos, inner_edge_pos],
                         size=[attachment_width, inner_edge_length], **general_kwargs))
    kicad_mod.append(Pad(at=[outer_pointing_pos, -inner_edge_pos],
                         size=[attachment_width, inner_edge_length], **general_kwargs))
    kicad_mod.append(Pad(at=[-outer_pointing_pos, inner_edge_pos],
                         size=[attachment_width, inner_edge_length], **general_kwargs))
    kicad_mod.append(Pad(at=[-outer_pointing_pos, -inner_edge_pos],
                         size=[attachment_width, inner_edge_length], **general_kwargs))

    # write file
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile('{name}.kicad_mod'.format(name=name))


if __name__ == '__main__':
    # http://katalog.we-online.com/pbs/datasheet/36103205.pdf
    create_shielding('Würth_36103205_20x20mm', 21.5, 20, 1, 2.6, [7.5], 3.3)

    # http://katalog.we-online.com/pbs/datasheet/36103255.pdf
    create_shielding('Würth_36103255_25x25mm', 26.5, 25, 1, 2.6, [5.1, 12.5], 3.3)

    # http://katalog.we-online.com/pbs/datasheet/36103305.pdf
    create_shielding('Würth_36103305_30x30mm', 31.5, 30, 1, 2.6, [7.5, 17.5], 3.3)

    # http://katalog.we-online.com/pbs/datasheet/36103505.pdf
    create_shielding('Würth_36103505_50x50mm', 51.5, 50, 1, 2.6, [7.5, 17.5, 27.5, 37.5], 3.3)

    # http://katalog.we-online.com/pbs/datasheet/36103605.pdf
    create_shielding('Würth_36103605_60x60mm', 61.5, 60, 1, 2.6, [7.5, 17.5, 27.5, 37.5, 47.5], 3.5)
