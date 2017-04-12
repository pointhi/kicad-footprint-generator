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
import argparse

sys.path.append(os.path.join(sys.path[0], "../.."))  # enable package import from parent directory

from KicadModTree import *  # NOQA


if __name__ == '__main__':

    # handle arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('pincount', help='number of pins of the connector', type=int, nargs=1)
    parser.add_argument('-v', '--verbose', help='show extra information while generating the footprint', action='store_true')
    args = parser.parse_args()
    pincount = int(args.pincount[0])
    footprint_name = 'Molex_KK-6410-{pc:02g}_{pc:02g}x2.54mm_Straight'.format(pc=pincount)

    print('Building {:s} '.format(footprint_name))

    # calculate working values
    pad_spacing = 2.54
    start_pos_x = 0
    end_pos_x = (pincount-1) * pad_spacing
    centre_x = (end_pos_x - start_pos_x) / 2.0
    nudge = 0.1
    silk_w = 0.12

    # initialise footprint
    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription('Connector Headers with Friction Lock, 22-27-2{pincount:02g}1, http://www.molex.com/pdm_docs/sd/022272021_sd.pdf'.format(pincount=pincount))
    kicad_mod.setTags('connector molex kk_6410 22-27-2{pincount:02g}1'.format(pincount=pincount))

    # set general values
    kicad_mod.append(Text(type='reference', text='REF**', size=[1,1], at=[1, -4.5], layer='F.SilkS'))
    kicad_mod.append(Text(type='user', text='%R', size=[1,1], at=[centre_x, 0], layer='F.Fab'))
    kicad_mod.append(Text(type='value', text=footprint_name, at=[centre_x, 4.5], layer='F.Fab'))

    # create pads
    kicad_mod.append(Pad(at=[0,0], number=1, type=Pad.TYPE_THT, shape=Pad.SHAPE_RECT, size=[2,2.6],\
        drill=1.2, layers=Pad.LAYERS_THT))
    kicad_mod.append(PadArray(pincount=pincount-1, spacing=[pad_spacing,0], start=[pad_spacing,0],\
        initial=2, increment=1, type=Pad.TYPE_THT, shape=Pad.SHAPE_OVAL, size=[2,2.6],\
        drill=1.2, layers=Pad.LAYERS_THT))

    # create fab outline
    kicad_mod.append(RectLine(start=[start_pos_x-pad_spacing/2.0-2*nudge, -3.02-nudge],\
        end=[end_pos_x+pad_spacing/2.0+2*nudge, 2.98+nudge], layer='F.Fab', width=silk_w))

    # create silkscreen
    kicad_mod.append(RectLine(start=[start_pos_x-pad_spacing/2.0-nudge, -3.02],\
        end=[end_pos_x+pad_spacing/2.0+nudge, 2.98], layer='F.SilkS', width=silk_w))

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
            [start_pos_x+2*pad_spacing, 1.98], [start_pos_x+2*pad_spacing, 2.98]], layer='F.SilkS', width=silk_w))
        kicad_mod.append(PolygoneLine(polygone=[[start_pos_x, 1.98], [start_pos_x+0.25, 1.55],\
            [start_pos_x+2*pad_spacing, 1.55], [start_pos_x+2*pad_spacing, 1.98] ],layer='F.SilkS', width=silk_w))
        kicad_mod.append(PolygoneLine(polygone=[[start_pos_x+0.25, 2.98],\
            [start_pos_x+0.25, 1.98]], layer='F.SilkS', width=silk_w))

        kicad_mod.append(PolygoneLine(polygone=[[end_pos_x, 2.98], [end_pos_x, 1.98],\
            [end_pos_x-2*pad_spacing, 1.98], [end_pos_x-2*pad_spacing, 2.98]], layer='F.SilkS', width=silk_w))
        kicad_mod.append(PolygoneLine(polygone=[[end_pos_x, 1.98], [end_pos_x-0.25, 1.55],\
            [end_pos_x-2*pad_spacing, 1.55], [end_pos_x-2*pad_spacing, 1.98] ],layer='F.SilkS', width=silk_w))
        kicad_mod.append(PolygoneLine(polygone=[[end_pos_x-0.25, 2.98],\
            [end_pos_x-0.25, 1.98]], layer='F.SilkS', width=silk_w))

    for i in range(0, pincount):
        middle_x = start_pos_x + i * pad_spacing
        start_x = middle_x - 1.6/2
        end_x = middle_x + 1.6/2
        kicad_mod.append(PolygoneLine(polygone=[[start_x, -3.02], [start_x, -2.4],\
            [end_x, -2.4], [end_x, -3.02]], layer='F.SilkS', width=silk_w))

    # create Courtyard
    def round_to(n, precision):
        correction = 0.5 if n >= 0 else -0.5
        return int( n/precision+correction ) * precision

    kicad_mod.append(RectLine(start=[round_to(start_pos_x-2.54/2-0.5-0.03-0.1, 0.05),2.98+0.5+0.02], end=[round_to(end_pos_x+2.54/2+0.5+0.03+0.1, 0.05),-3.02-0.5-0.03], layer='F.CrtYd', width=0.05))

    # add model
    kicad_mod.append(Model(filename="${{KISYS3DMOD}}/Connectors_Molex.3dshapes/{:s}.wrl".format(footprint_name), at=[0, 0, 0], scale=[1, 1, 1], rotate=[0, 0, 0]))

    # print render tree
    if args.verbose:
        print(kicad_mod.getRenderTree())

    # write file
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile('{:s}.kicad_mod'.format(footprint_name))

