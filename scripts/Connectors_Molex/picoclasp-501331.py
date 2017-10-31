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

"""

http://www.molex.com/pdm_docs/sd/5013310207_sd.pdf

PN suffix falls into two categories:
Pincount = 2-5:
    Suffix is "0x07", where "x" is the pin count and the color is natural
Pincount 6-15:
    Suffix is "xxyy",
    where "xx" is the pin count and
    where "yy" is the color ("62" = green "42" = blue, "22" = red, "12" = black, "07" = natural)

This script only generates natural-colored footprints per the PR discussion on GitHub
However, any valid color suffix from the current datasheets will be accepted as an argument

"""

import sys
import os
import argparse

sys.path.append(os.path.join(sys.path[0], "../.."))  # enable package import from parent directory

from KicadModTree import *  # NOQA


def round_to(n, precision):
    correction = 0.5 if n >= 0 else -0.5
    return int( n/precision+correction ) * precision


if __name__ == '__main__':

    # handle arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('gen_pn', help='suffix of 501331 series number (e.g. 1507)', type=str, nargs='*')
    parser.add_argument('-v', '--verbose', help='show extra information while generating the footprint', action='store_true')
    args = parser.parse_args()
    gen_pn = args.gen_pn # input argument in a list
    
    # if user did not supply an argument we will get an empty list and generate all footprints (PN validation is later)
    if gen_pn:
        partnumbers = gen_pn
    else:
        # build list of natural color PN suffixes
        # this is a little tricky: use range() to build a list of ints, then convert each list element to a string, then finally add an "07" suffix to each element
        partnumbers = [s + "07" for s in ["{:02d}".format(x) for x in range(2, 16)]]
    
    for partnumber in partnumbers:
        
        # do not proceed if pin count or PN are not valid
        if not ((partnumber.isdigit()) and (len(partnumber) == 4) and (partnumber[2:4] in ["07","12","22","42","62"])):
            sys.exit("Partnumber is not valid!")
        
        # the first two digits of the PN suffix are the pin count
        pincount = int(partnumber[:2])
        
        footprint_name = 'Molex_PicoClasp_501331-{pn:s}_1x{pc:02g}_P1.0mm_Vertical'.format(pc=pincount, pn=partnumber)
        
        print('Building {:s} '.format(footprint_name))
        
        # calculate working values
        pitch = 1.0
        pad_left_x = -1.325
        pad_width = 1.55
        pad_height = 0.6
        
        nail_width = 1.8
        nail_height = 1.2
        nail_x = pad_left_x + 4.2 - 0.9 - pad_width / 2.0
        nail_y = ((pincount - 1) * pitch) / 2.0 + 0.7 + nail_height / 2.0

        body_offset = pad_left_x + 0.175
        body_width = body_offset + 3
        body_hump_width = body_offset + 4.47
        half_body_hump_height = 2.25
        half_body_height = ((pincount - 1) * pitch) / 2.0 + 1.5

        pin1_y = -((pincount - 1) * pitch) / 2.0
        silk_clearance = 0.36 # 0.3mm desired clearance must include silk line endcap radius
        nudge = 0.12

        courtyard_precision = 0.01
        courtyard_clearance = 0.5
        courtyard_left_x = round_to(pad_left_x - pad_width / 2.0 - courtyard_clearance, courtyard_precision)
        courtyard_right_x = round_to(nail_x + nail_width / 2.0 + courtyard_clearance, courtyard_precision)
        courtyard_hump_x = round_to(body_hump_width + courtyard_clearance, courtyard_precision)
        courtyard_y = round_to(nail_y + nail_height / 2.0 + courtyard_clearance, courtyard_precision)

        label_y_offset = courtyard_y + 0.7
        
        # initialise footprint
        kicad_mod = Footprint(footprint_name)
        kicad_mod.setDescription('Molex Pico-Clasp header, {pc:02g} contacts, 1.00mm pitch, http://www.molex.com/pdm_docs/sd/5013310207_sd.pdf'.format(pc=pincount))
        kicad_mod.setTags('connector molex pico clasp 501331-{:s}'.format(partnumber))
        kicad_mod.setAttribute('smd')

        # set general values
        kicad_mod.append(Text(type='reference', text='REF**', size=[1,1], at=[0, -label_y_offset], layer='F.SilkS'))
        kicad_mod.append(Text(type='user', text='%R', size=[1,1], at=[pad_left_x + 2, 0], rotation=90, layer='F.Fab'))
        kicad_mod.append(Text(type='value', text=footprint_name, at=[0, label_y_offset], layer='F.Fab'))

        # create pads
        kicad_mod.append(PadArray(pincount=pincount, y_spacing=pitch, center=[pad_left_x,0], type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, size=[pad_width,pad_height], layers=Pad.LAYERS_SMT))
        
        # create "fitting nail" (mounting) holes
        kicad_mod.append(Pad(at=[nail_x,-nail_y], type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, size=[nail_width,nail_height], layers=['F.Cu','F.Paste','F.Mask']))
        kicad_mod.append(Pad(at=[nail_x,nail_y], type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, size=[nail_width,nail_height], layers=['F.Cu','F.Paste','F.Mask']))

        # create fab outline and pin 1 marker
        if pincount <=5:
            kicad_mod.append(RectLine(start=[body_offset, -half_body_height], end=[body_width, half_body_height], layer='F.Fab'))
        else:
            kicad_mod.append(PolygoneLine(polygone=[[body_offset, -half_body_height],[body_width, -half_body_height],[body_width, -half_body_hump_height],\
                    [body_hump_width, -half_body_hump_height],[body_hump_width, half_body_hump_height],[body_width, half_body_hump_height],\
                    [body_width, half_body_height],[body_offset, half_body_height],[body_offset, -half_body_height]], layer='F.Fab'))
        kicad_mod.append(PolygoneLine(polygone=[[body_offset, pin1_y+0.5],[body_offset+1, pin1_y],[body_offset, pin1_y-0.5]], layer='F.Fab'))

        # create silkscreen outline and pin 1 marker
        kicad_mod.append(PolygoneLine(polygone=[[body_offset-0.8, pin1_y-pad_height/2.0-silk_clearance],[body_offset-nudge, pin1_y-pad_height/2.0-silk_clearance],\
                [body_offset-nudge, -half_body_height-nudge],[nail_x-nail_width/2.0-silk_clearance, -half_body_height-nudge]], layer='F.SilkS'))
        kicad_mod.append(PolygoneLine(polygone=[[body_offset-nudge, -pin1_y+pad_height/2.0+silk_clearance],[body_offset-nudge, half_body_height+nudge],\
                [nail_x-nail_width/2.0-silk_clearance, half_body_height+nudge]], layer='F.SilkS'))
        if pincount <= 5:
            kicad_mod.append(Line(start=[body_width+nudge, -nail_y+nail_height/2.0+silk_clearance], end=[body_width+nudge, nail_y-nail_height/2.0-silk_clearance], layer='F.SilkS'))
        else:
            kicad_mod.append(PolygoneLine(polygone=[[body_width+nudge, -nail_y+nail_height/2.0+silk_clearance],[body_width+nudge, -half_body_hump_height-nudge],\
                    [body_hump_width+nudge, -half_body_hump_height-nudge],[body_hump_width+nudge, half_body_hump_height+nudge],\
                    [body_width+nudge, half_body_hump_height+nudge],[body_width+nudge, nail_y-nail_height/2.0-silk_clearance]], layer='F.SilkS'))
        
        # create courtyard
        if pincount <= 5:
            kicad_mod.append(RectLine(start=[courtyard_left_x, -courtyard_y], end=[courtyard_right_x, courtyard_y], layer='F.CrtYd'))
        else:
            kicad_mod.append(RectLine(start=[courtyard_left_x, -courtyard_y], end=[courtyard_hump_x, courtyard_y], layer='F.CrtYd'))

        # add model
        kicad_mod.append(Model(filename="${{KISYS3DMOD}}/Connectors_Molex.3dshapes/{:s}.wrl".format(footprint_name), at=[0, 0, 0], scale=[1, 1, 1], rotate=[0, 0, 0]))

        # print render tree
        if args.verbose:
            print(kicad_mod.getRenderTree())

        # write file
        file_handler = KicadFileHandler(kicad_mod)
        file_handler.writeFile('{:s}.kicad_mod'.format(footprint_name))

