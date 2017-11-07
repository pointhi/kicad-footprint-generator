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

This family of parts is spread over 3 datasheets, depending on the 3rd number in the PN suffix:

502340-xx10 (14-80 pin):
http://www.molex.com/pdm_docs/sd/5024301410_sd.pdf

502340-0820 (8 pin)
http://www.molex.com/pdm_docs/sd/5024300820_sd.pdf

502340-xx30 (14-90 pin):
http://www.molex.com/pdm_docs/sd/5024307030_sd.pdf

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
    parser.add_argument('gen_pn', help='suffix of 502430 series number (e.g. 0820)', type=str, nargs='*')
    parser.add_argument('-v', '--verbose', help='show extra information while generating the footprint', action='store_true')
    args = parser.parse_args()
    gen_pn = args.gen_pn # input argument in a list

    # list of valid partnumber suffixes from all datasheets
    valid_pns = ["1410","2010","2210","2410","2610","3010","3210","3410","4010","4410","5010","6010","6410","8010","0820","1430","2030","2230","2430","2630","3230","4030","5030","6030","7030","8030","9030"]
    
    # if user did not supply an argument we will get an empty list and generate all footprints (PN validation is later)
    if gen_pn:
        partnumbers = gen_pn
    else:
        partnumbers = valid_pns
    
    for partnumber in partnumbers:
        
        # do not proceed if pin count or PN are not valid
        #if not ((partnumber.isdigit()) and (len(partnumber) == 4) and (int(partnumber[:2]) % 2.0 == 0) and (partnumber[2:4] in ["10","20","30"])):
        if partnumber not in valid_pns:
            sys.exit("Partnumber is not valid!")
        
        # the first two digits of the PN suffix are the pin count
        pincount = int(partnumber[:2])
        
        footprint_name = 'Molex_SlimStack-502430-{pn:s}_2x{pc:02g}_P0.4mm_Vertical'.format(pc=pincount/2, pn=partnumber)
        
        print('Building {:s} '.format(footprint_name))
        
        # calculate working values
        pad_x_spacing = 0.4
        pad_y_spacing = 1.05 + 0.66
        pad_width = 0.22
        pad_height = 0.66
        pad_x_span = pad_x_spacing * ((pincount / 2) - 1)
        
        nail_x = pad_x_span / 2.0 + 0.95

        half_body_width = 1.54 / 2.0
        half_body_length = (pad_x_span / 2.0) + 1.33

        fab_width = 0.1

        outline_x = half_body_length - (pad_x_span / 2.0) - 0.45
        marker_y = 0.35
        silk_width = 0.12
        nudge = 0.12

        courtyard_width = 0.05
        courtyard_precision = 0.01
        courtyard_clearance = 0.5
        courtyard_x = round_to(half_body_length + courtyard_clearance, courtyard_precision)
        courtyard_y = round_to((pad_y_spacing + pad_height) / 2.0 + courtyard_clearance, courtyard_precision)

        label_x_offset = 0
        label_y_offset = courtyard_y + 0.7

        # select correct datasheet URL depending on part number
        if str(partnumber)[2:3] == "1":
            datasheet = "http://www.molex.com/pdm_docs/sd/5024301410_sd.pdf"
        elif str(partnumber)[2:3] == "2":
            datasheet = "http://www.molex.com/pdm_docs/sd/5024300820_sd.pdf"
        elif str(partnumber)[2:3] == "3":
            datasheet = "http://www.molex.com/pdm_docs/sd/5024307030_sd.pdf"
        
        # initialise footprint
        kicad_mod = Footprint(footprint_name)
        kicad_mod.setDescription('Molex SlimStack plug, 02x{pc:02g} contacts, 0.4mm pitch, 0.8mm height, SMT, {ds}'.format(pc=pincount/2, ds=datasheet))
        kicad_mod.setTags('connector molex slimstack 502430-{:s}'.format(partnumber))
        kicad_mod.setAttribute('smd')

        # set general values
        kicad_mod.append(Text(type='reference', text='REF**', size=[1,1], at=[label_x_offset, -label_y_offset], layer='F.SilkS'))
        kicad_mod.append(Text(type='user', text='%R', size=[1,1], at=[0, 0], layer='F.Fab'))
        kicad_mod.append(Text(type='value', text=footprint_name, at=[label_x_offset, label_y_offset], layer='F.Fab'))

        # create pads
        kicad_mod.append(PadArray(pincount=pincount//2, x_spacing=pad_x_spacing, y_spacing=0,center=[0,-pad_y_spacing/2.0],\
            initial=1, increment=2, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, size=[pad_width, pad_height],layers=Pad.LAYERS_SMT))
        kicad_mod.append(PadArray(pincount=pincount//2, x_spacing=pad_x_spacing, y_spacing=0,center=[0,pad_y_spacing/2.0],\
            initial=2, increment=2, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, size=[pad_width, pad_height],layers=Pad.LAYERS_SMT))
        
        # create "fitting nail" (npth mounting) holes
        #kicad_mod.append(Pad(at=[-nail_x, 0], type=Pad.TYPE_NPTH, shape=Pad.SHAPE_RECT, size=[0.35, 0.44], drill=[0.35, 0.44], layers=['*.Cu', '*.Mask']))
        #kicad_mod.append(Pad(at=[nail_x, 0], type=Pad.TYPE_NPTH, shape=Pad.SHAPE_RECT, size=[0.35, 0.44], drill=[0.35, 0.44], layers=['*.Cu', '*.Mask']))
        kicad_mod.append(RectLine(start=[-nail_x - 0.35 / 2.0, -0.22], end=[-nail_x + 0.35 / 2.0, 0.22], layer='Edge.Cuts', width=fab_width))
        kicad_mod.append(RectLine(start=[nail_x - 0.35 / 2.0, -0.22], end=[nail_x + 0.35 / 2.0, 0.22], layer='Edge.Cuts', width=fab_width))

        # create fab outline and pin 1 marker
        kicad_mod.append(RectLine(start=[-half_body_length, -half_body_width], end=[half_body_length, half_body_width], layer='F.Fab', width=fab_width))
        kicad_mod.append(Line(start=[-half_body_length+outline_x, -half_body_width], end=[-half_body_length+outline_x, -half_body_width-marker_y], layer='F.Fab', width=fab_width))

        # create silkscreen outline and pin 1 marker
        left_outline = [[-half_body_length+outline_x, half_body_width+nudge], [-half_body_length-nudge, half_body_width+nudge], [-half_body_length-nudge, -half_body_width-nudge],\
                        [-half_body_length+outline_x, -half_body_width-nudge], [-half_body_length+outline_x, -half_body_width-marker_y]]
        right_outline = [[half_body_length-outline_x, half_body_width+nudge], [half_body_length+nudge, half_body_width+nudge], [half_body_length+nudge, -half_body_width-nudge],\
                         [half_body_length-outline_x, -half_body_width-nudge]]
        kicad_mod.append(PolygoneLine(polygone=left_outline, layer='F.SilkS', width=silk_width))
        kicad_mod.append(PolygoneLine(polygone=right_outline, layer='F.SilkS', width=silk_width))

        # create courtyard
        kicad_mod.append(RectLine(start=[-courtyard_x, -courtyard_y], end=[courtyard_x, courtyard_y], layer='F.CrtYd', width=courtyard_width))

        # add model
        kicad_mod.append(Model(filename="${{KISYS3DMOD}}/Connectors_Molex.3dshapes/{:s}.wrl".format(footprint_name), at=[0, 0, 0], scale=[1, 1, 1], rotate=[0, 0, 0]))

        # print render tree
        if args.verbose:
            print(kicad_mod.getRenderTree())

        # write file
        file_handler = KicadFileHandler(kicad_mod)
        file_handler.writeFile('{:s}.kicad_mod'.format(footprint_name))

