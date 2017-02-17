#!/usr/bin/env python

import sys
import os
import math

# ensure that the kicad-footprint-generator directory is available
#sys.path.append(os.environ.get('KIFOOTPRINTGENERATOR'))  # enable package import from parent directory
#sys.path.append("D:\hardware\KiCAD\kicad-footprint-generator")  # enable package import from parent directory
sys.path.append(os.path.join(sys.path[0],"..","..","kicad_mod")) # load kicad_mod path
sys.path.append(os.path.join(sys.path[0],"..","..")) # load kicad_mod path
sys.path.append(os.path.join(sys.path[0],"..","tools")) # load kicad_mod path

from KicadModTree import *  # NOQA
from footprint_scripts_pin_headers import *  # NOQA




if __name__ == '__main__':
    # common settings
    rm=2.54
    ddrill=1
    pad=[1.7,1.7]
    singlecol_packwidth=2.54
    singlecol_packoffset=0
    angled_pack_width=2.5
    angled_pack_offset=3.9-2.5
    angled_pin_length=6
    angled_pin_width=0.64
    rmx_pad_offset=1.5
    rmx_pin_length=2.65
    pin_width=0.64
    pad_smd=[3,1]

    for cols in [1,2]:
        for rows in range(1,41):
            makePinHeadStraight(rows, cols, rm, rm, cols * singlecol_packwidth + singlecol_packoffset,
                                singlecol_packwidth / 2 + singlecol_packoffset,
                                singlecol_packwidth / 2 + singlecol_packoffset, ddrill, pad, [], "Pin_Headers", "Pin_Header", "pin header",
                                [(cols - 1) * rm / 2 / 25.4, -(rows - 1) * rm / 2 / 25.4, 0], [1, 1, 1],
                                [0, 0, 90])
            makePinHeadAngled(rows, cols, rm, rm, angled_pack_width, angled_pack_offset, angled_pin_length, angled_pin_width, ddrill, pad,
                              [], "Pin_Headers", "Pin_Header", "pin header", [(cols - 1) * rm / 2 / 25.4, -(rows - 1) * rm / 2 / 25.4, 0], [1, 1, 1],
                                [0, 0, 90])
            makePinHeadStraightSMD(rows, cols, rm, rm, rmx_pad_offset, rmx_pin_length, pin_width, cols * singlecol_packwidth + singlecol_packoffset,
                                singlecol_packwidth / 2 + singlecol_packoffset,
                                singlecol_packwidth / 2 + singlecol_packoffset, pad_smd,
                                   True)
            if cols==1:
                makePinHeadStraightSMD(rows, cols, rm, rm, rmx_pad_offset, rmx_pin_length, pin_width,
                                   cols * singlecol_packwidth + singlecol_packoffset,
                                   singlecol_packwidth / 2 + singlecol_packoffset,
                                   singlecol_packwidth / 2 + singlecol_packoffset, pad_smd,
                                   False)

    rm=2.00
    ddrill=0.8
    pad=[1.35, 1.35]
    singlecol_packwidth=2.0
    singlecol_packoffset=0
    angled_pack_width=1.5
    angled_pack_offset=3-1.5
    angled_pin_length=4
    angled_pin_width=0.5
    rmx_pad_offset=2.125
    rmx_pin_length=2
    pin_width=0.5
    pad_smd=[2.75,1]
    for cols in [1, 2]:
        for rows in range(1, 41):
            makePinHeadStraight(rows, cols, rm, rm, cols * singlecol_packwidth + singlecol_packoffset,
                                singlecol_packwidth / 2 + singlecol_packoffset,
                                singlecol_packwidth / 2 + singlecol_packoffset, ddrill, pad, [], "Pin_Headers", "Pin_Header", "pin header",
                                offset3d=[0,0, 0], scale3d=[1, 1, 1],
                                rotate3d=[0, 0, 0])
            makePinHeadAngled(rows, cols, rm, rm, angled_pack_width, angled_pack_offset, angled_pin_length,
                              angled_pin_width, ddrill, pad,
                              [], "Pin_Headers", "Pin_Header", "pin header", [(cols - 1) * rm / 2 / 25.4, -(rows - 1) * rm / 2 / 25.4, 0],
                              [1, 1, 1],
                              [0, 0, 90])
            makePinHeadStraightSMD(rows, cols, rm, rm, rmx_pad_offset, rmx_pin_length, pin_width,
                                   cols * singlecol_packwidth + singlecol_packoffset,
                                   singlecol_packwidth / 2 + singlecol_packoffset,
                                   singlecol_packwidth / 2 + singlecol_packoffset, pad_smd,
                                   True)
            if cols == 1:
                makePinHeadStraightSMD(rows, cols, rm, rm, rmx_pad_offset, rmx_pin_length, pin_width,
                                       cols * singlecol_packwidth + singlecol_packoffset,
                                       singlecol_packwidth / 2 + singlecol_packoffset,
                                       singlecol_packwidth / 2 + singlecol_packoffset, pad_smd,
                                       False)

    rm = 1.27
    ddrill = 0.65
    pad = [1, 1]
    package_width=[2.54,3.41]
    singlecol_packwidth = 1.27
    angled_pack_width=1
    angled_pack_offset=3.81-1
    angled_pin_length=3.81
    angled_pin_width=0.4
    rmx_pad_offset=1.95
    rmx_pin_length=1.92
    pin_width=0.4
    pad_smd=[2.1,0.75]
    for cols in [1, 2]:
        for rows in range(1, 41):
            makePinHeadStraight(rows, cols, rm, rm, package_width[cols-1],
                                singlecol_packwidth / 2 ,
                                singlecol_packwidth / 2 , ddrill, pad, [], "Pin_Headers", "Pin_Header", "pin header",
                                offset3d=[0, 0, 0], scale3d=[1, 1, 1],
                                rotate3d=[0, 0, 0])
            makePinHeadAngled(rows, cols, rm, rm, angled_pack_width, angled_pack_offset, angled_pin_length,
                              angled_pin_width, ddrill, pad,
                              [], "Pin_Headers", "Pin_Header", "pin header", [(cols - 1) * rm / 2 / 25.4, -(rows - 1) * rm / 2 / 25.4, 0],
                              [1, 1, 1],
                              [0, 0, 90])
            makePinHeadAngled(rows, cols, rm, rm, angled_pack_width, angled_pack_offset, angled_pin_length,
                              angled_pin_width, ddrill, pad,
                              [], "Pin_Headers", "Pin_Header", "pin header", [(cols - 1) * rm / 2 / 25.4, -(rows - 1) * rm / 2 / 25.4, 0],
                              [1, 1, 1],
                              [0, 0, 90])
            makePinHeadStraightSMD(rows, cols, rm, rm, rmx_pad_offset, rmx_pin_length, pin_width,
                                   cols * singlecol_packwidth + singlecol_packoffset,
                                   singlecol_packwidth / 2 + singlecol_packoffset,
                                   singlecol_packwidth / 2 + singlecol_packoffset, pad_smd,
                                   True)
            if cols == 1:
                makePinHeadStraightSMD(rows, cols, rm, rm, rmx_pad_offset, rmx_pin_length, pin_width,
                                       cols * singlecol_packwidth + singlecol_packoffset,
                                       singlecol_packwidth / 2 + singlecol_packoffset,
                                       singlecol_packwidth / 2 + singlecol_packoffset, pad_smd,
                                       False)
