#!/usr/bin/env python

import sys
import os

sys.path.append(os.path.join(sys.path[0], "..", ".."))  # load parent path of  KicadModTree

from KicadModTree import *  # NOQA
from KicadModTree.nodes.base.Pad import Pad  # NOQA


def create_shielding(name, outer_size, size,
                     attachment_drill, attachment_diameter, attachment_positions):

    attachment_positions = sorted(attachment_positions)

    kicad_mod = Footprint(name)

    # init kicad footprint
    kicad_mod.setDescription('WE-SHC Shielding Cabinet THT {size}x{size}mm'.format(size=size))
    kicad_mod.setTags('Shielding Cabinet')

    courtjard_size = outer_size / 2. + attachment_diameter / 2. + 0.25

    # set general values
    kicad_mod.append(Text(type='reference', text='REF**', at=[0, -courtjard_size - 1], layer='F.SilkS'))
    kicad_mod.append(Text(type='value', text=name, at=[0, courtjard_size + 1], layer='F.Fab'))

    # create courtyard
    kicad_mod.append(RectLine(start=[-courtjard_size, -courtjard_size],
                              end=[courtjard_size, courtjard_size],
                              layer='F.CrtYd'))

    # create Fabriaction Layer
    kicad_mod.append(RectLine(start=[-size / 2., -size / 2.],
                              end=[size / 2., size / 2.],
                              layer='F.Fab'))

    general_kwargs = {'number': 1,
                      'type': Pad.TYPE_THT,
                      'shape': Pad.SHAPE_CIRCLE,
                      'size': [attachment_diameter, attachment_diameter],
                      'drill': attachment_drill,
                      'layers': ['*.Cu', '*.Mask']}

    # create pads
    for position in attachment_positions:
        kicad_mod.append(Pad(at=[outer_size / 2., position / 2.], **general_kwargs))
        kicad_mod.append(Pad(at=[-outer_size / 2., position / 2.], **general_kwargs))
        kicad_mod.append(Pad(at=[position / 2., outer_size / 2.], **general_kwargs))
        kicad_mod.append(Pad(at=[position / 2., -outer_size / 2.], **general_kwargs))

        if position != 0. or 2*outer_size == 2*position:
            kicad_mod.append(Pad(at=[outer_size / 2., -position / 2.], **general_kwargs))
            kicad_mod.append(Pad(at=[-outer_size / 2., -position / 2.], **general_kwargs))
            kicad_mod.append(Pad(at=[-position / 2., outer_size / 2.], **general_kwargs))
            kicad_mod.append(Pad(at=[-position / 2., -outer_size / 2.], **general_kwargs))

    # create silk screen
    silk_padding = 0.2
    silk_outline = size / 2. + silk_padding

    pad_padding = 0.4

    if attachment_positions[0] != 0.:
        line_end = attachment_positions[0] / 2. - attachment_diameter / 2. - pad_padding
        kicad_mod.append(Line(start=[silk_outline, line_end], end=[silk_outline, -line_end], layer='F.SilkS'))
        kicad_mod.append(Line(start=[-silk_outline, -line_end], end=[-silk_outline, line_end], layer='F.SilkS'))
        kicad_mod.append(Line(start=[line_end, silk_outline], end=[-line_end, silk_outline], layer='F.SilkS'))
        kicad_mod.append(Line(start=[line_end, -silk_outline], end=[-line_end, -silk_outline], layer='F.SilkS'))

    for begin, end in zip(attachment_positions, attachment_positions[1:]):
        line_begin = begin / 2. + attachment_diameter / 2. + pad_padding
        line_end = end / 2. - attachment_diameter / 2. - pad_padding
        kicad_mod.append(Line(start=[silk_outline, line_begin], end=[silk_outline, line_end], layer='F.SilkS'))
        kicad_mod.append(Line(start=[silk_outline, -line_begin], end=[silk_outline, -line_end], layer='F.SilkS'))
        kicad_mod.append(Line(start=[-silk_outline, line_begin], end=[-silk_outline, line_end], layer='F.SilkS'))
        kicad_mod.append(Line(start=[-silk_outline, -line_begin], end=[-silk_outline, -line_end], layer='F.SilkS'))
        kicad_mod.append(Line(start=[line_begin, silk_outline], end=[line_end, silk_outline], layer='F.SilkS'))
        kicad_mod.append(Line(start=[line_begin, -silk_outline], end=[line_end, -silk_outline], layer='F.SilkS'))
        kicad_mod.append(Line(start=[-line_begin, silk_outline], end=[-line_end, silk_outline], layer='F.SilkS'))
        kicad_mod.append(Line(start=[-line_begin, -silk_outline], end=[-line_end, -silk_outline], layer='F.SilkS'))

    if attachment_positions[-1] != outer_size:
        line_begin = attachment_positions[-1] / 2. + attachment_diameter / 2. + pad_padding
        line_end = outer_size / 2. + silk_padding
        kicad_mod.append(Line(start=[silk_outline, line_begin], end=[silk_outline, line_end], layer='F.SilkS'))
        kicad_mod.append(Line(start=[silk_outline, -line_begin], end=[silk_outline, -line_end], layer='F.SilkS'))
        kicad_mod.append(Line(start=[-silk_outline, line_begin], end=[-silk_outline, line_end], layer='F.SilkS'))
        kicad_mod.append(Line(start=[-silk_outline, -line_begin], end=[-silk_outline, -line_end], layer='F.SilkS'))
        kicad_mod.append(Line(start=[line_begin, silk_outline], end=[line_end, silk_outline], layer='F.SilkS'))
        kicad_mod.append(Line(start=[line_begin, -silk_outline], end=[line_end, -silk_outline], layer='F.SilkS'))
        kicad_mod.append(Line(start=[-line_begin, silk_outline], end=[-line_end, silk_outline], layer='F.SilkS'))
        kicad_mod.append(Line(start=[-line_begin, -silk_outline], end=[-line_end, -silk_outline], layer='F.SilkS'))

    # fix KLC issue 6.3
    # kicad_mod.insert(Translation(outer_size / 2., attachment_positions[-1] / 2.))

    # write file
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile('{name}.kicad_mod'.format(name=name))


if __name__ == '__main__':
    # http://katalog.we-online.de/pbs/datasheet/36503205.pdf
    create_shielding('Würth_36503205_20x20mm', 20.5, 20.5, 1.1, 1.7, [5.08, 15.24])

    # http://katalog.we-online.de/pbs/datasheet/36503255.pdf
    create_shielding('Würth_36503255_25x25mm', 25.5, 25.5, 1.1, 1.7, [0, 10.16, 20.32])

    # http://katalog.we-online.de/pbs/datasheet/36503305.pdf
    create_shielding('Würth_36503305_30x30mm', 30.5, 30.5, 1.1, 1.7, [5.08, 15.24, 25.40])

    # http://katalog.we-online.de/pbs/datasheet/36503505.pdf
    create_shielding('Würth_36503505_50x50mm', 50.5, 50.5, 1.1, 1.7, [5.08, 15.24, 25.40, 35.56, 45.72])

    # http://katalog.we-online.de/pbs/datasheet/36503605.pdf
    create_shielding('Würth_36503605_60x60mm', 60.5, 60.5, 1.1, 1.7, [5.08, 15.24, 25.40, 35.56, 45.72, 55.88])
