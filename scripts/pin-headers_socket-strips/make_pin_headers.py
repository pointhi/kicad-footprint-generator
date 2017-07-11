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
    # from http://katalog.we-online.de/em/datasheet/6130xx11121.pdf
    # and  http://katalog.we-online.de/em/datasheet/6130xx21121.pdf
    # and  http://katalog.we-online.de/em/datasheet/6130xx11021.pdf
    # and  http://katalog.we-online.de/em/datasheet/6130xx21021.pdf
    # and  https://cdn.harwin.com/pdfs/M20-877.pdf
    # and  https://cdn.harwin.com/pdfs/M20-876.pdf

    rm=2.54
    ddrill=1
    pad=[1.7,1.7]
    singlecol_packwidth=2.54
    singlecol_packoffset=0
    angled_pack_width=2.54
    angled_pack_offset=1.5
    angled_pin_length=6
    angled_pin_width=0.64
    rmx_pad_offset=[1.655,2.525]
    rmx_pin_length=[2.54,3.6]
    pin_width=0.64
    single_pad_smd=[2.51,1.0]
    dual_pad_smd=[3.15,1.0]

    for cols in [1,2]:
        for rows in range(1,41):
            makePinHeadStraight(rows, cols, rm, rm, cols * singlecol_packwidth + singlecol_packoffset,
                                singlecol_packwidth / 2 + singlecol_packoffset,
                                singlecol_packwidth / 2 + singlecol_packoffset, ddrill, pad, [], "${KISYS3DMOD}/Pin_Headers", "Pin_Header", "pin header",
                                [0, 0, 0], [1, 1, 1], [0, 0, 0])
            makePinHeadAngled(rows, cols, rm, rm, angled_pack_width, angled_pack_offset, angled_pin_length, angled_pin_width, ddrill, pad,
                              [], "${KISYS3DMOD}/Pin_Headers", "Pin_Header", "pin header", [0, 0, 0], [1, 1, 1], [0, 0, 0])
            if rows != 1 or cols == 2:
              if cols == 2:
                  makePinHeadStraightSMD(rows, cols, rm, rm, rmx_pad_offset[cols-1], rmx_pin_length[cols-1], pin_width, cols * singlecol_packwidth + singlecol_packoffset,
                                      singlecol_packwidth / 2 + singlecol_packoffset,
                                      singlecol_packwidth / 2 + singlecol_packoffset, dual_pad_smd,
                                         True, [], "${KISYS3DMOD}/Pin_Headers", "Pin_Header", "pin header",
                                         [0, 0, 0], [1, 1, 1], [0, 0, 0])
              if cols==1:
                  makePinHeadStraightSMD(rows, cols, rm, rm, rmx_pad_offset[cols-1], rmx_pin_length[cols-1], pin_width,
                                     cols * singlecol_packwidth + singlecol_packoffset,
                                     singlecol_packwidth / 2 + singlecol_packoffset,
                                     singlecol_packwidth / 2 + singlecol_packoffset, single_pad_smd,
                                     True, [], "${KISYS3DMOD}/Pin_Headers", "Pin_Header", "pin header",
                                     [0, 0, 0], [1, 1, 1], [0, 0, 0])
                  makePinHeadStraightSMD(rows, cols, rm, rm, rmx_pad_offset[cols-1], rmx_pin_length[cols-1], pin_width,
                                     cols * singlecol_packwidth + singlecol_packoffset,
                                     singlecol_packwidth / 2 + singlecol_packoffset,
                                     singlecol_packwidth / 2 + singlecol_packoffset, single_pad_smd,
                                     False, [], "${KISYS3DMOD}/Pin_Headers", "Pin_Header", "pin header",
                                     [0, 0, 0], [1, 1, 1], [0, 0, 0])

    # From http://katalog.we-online.de/em/datasheet/6200xx11121.pdf
    # and  http://katalog.we-online.de/em/datasheet/6200xx21121.pdf
    # and  http://www.mouser.com/ds/2/4/page_280-282-24683.pdf
    # and  https://cdn.harwin.com/pdfs/M22-273.pdf
    # and  https://cdn.harwin.com/pdfs/M22-552.pdf

    rm=2.00
    ddrill=0.8
    pad=[1.35, 1.35]
    singlecol_packwidth=2.0
    singlecol_packoffset=0
    angled_pack_width=1.5
    angled_pack_offset=3-1.5
    angled_pin_length=4.2
    angled_pin_width=0.5
    rmx_pad_offset=[1.175,2.085]
    rmx_pin_length=[2.1,2.875]
    pin_width=0.5
    single_pad_smd=[2.35,0.85]
    dual_pad_smd=[2.58,1.0]
    for cols in [1, 2]:
        for rows in range(1, 41):
            makePinHeadStraight(rows, cols, rm, rm, cols * singlecol_packwidth + singlecol_packoffset,
                                singlecol_packwidth / 2 + singlecol_packoffset,
                                singlecol_packwidth / 2 + singlecol_packoffset, ddrill, pad, [], "${KISYS3DMOD}/Pin_Headers", "Pin_Header", "pin header",
                                [0, 0, 0], [1, 1, 1], [0, 0, 0])
            makePinHeadAngled(rows, cols, rm, rm, angled_pack_width, angled_pack_offset, angled_pin_length,
                              angled_pin_width, ddrill, pad,
                              [], "${KISYS3DMOD}/Pin_Headers", "Pin_Header", "pin header", [0, 0, 0], [1, 1, 1], [0, 0, 0])
            if rows != 1 or cols == 2:
              if cols == 2:
                  makePinHeadStraightSMD(rows, cols, rm, rm, rmx_pad_offset[cols-1], rmx_pin_length[cols-1], pin_width,
                                         cols * singlecol_packwidth + singlecol_packoffset,
                                         singlecol_packwidth / 2 + singlecol_packoffset,
                                         singlecol_packwidth / 2 + singlecol_packoffset, dual_pad_smd,
                                         True, [], "${KISYS3DMOD}/Pin_Headers", "Pin_Header", "pin header",
                                         [0, 0, 0], [1, 1, 1], [0, 0, 0])
              if cols == 1:
                  makePinHeadStraightSMD(rows, cols, rm, rm, rmx_pad_offset[cols-1], rmx_pin_length[cols-1], pin_width,
                                         cols * singlecol_packwidth + singlecol_packoffset,
                                         singlecol_packwidth / 2 + singlecol_packoffset,
                                         singlecol_packwidth / 2 + singlecol_packoffset, single_pad_smd,
                                         True, [], "${KISYS3DMOD}/Pin_Headers", "Pin_Header", "pin header",
                                         [0, 0, 0], [1, 1, 1], [0, 0, 0])
                  makePinHeadStraightSMD(rows, cols, rm, rm, rmx_pad_offset[cols-1], rmx_pin_length[cols-1], pin_width,
                                         cols * singlecol_packwidth + singlecol_packoffset,
                                         singlecol_packwidth / 2 + singlecol_packoffset,
                                         singlecol_packwidth / 2 + singlecol_packoffset, single_pad_smd,
                                         False, [], "${KISYS3DMOD}/Pin_Headers", "Pin_Header", "pin header",
                                         [0, 0, 0], [1, 1, 1], [0, 0, 0])

    # From https://cdn.harwin.com/pdfs/M50-393.pdf
    # https://cdn.harwin.com/pdfs/M50-363.pdf
    # https://cdn.harwin.com/pdfs/M50-353.pdf
    # https://cdn.harwin.com/pdfs/M50-360.pdf
    # and http://www.mouser.com/ds/2/181/M50-360R-1064294.pdfs
    rm = 1.27
    ddrill = 0.65
    pad = [1.0, 1.0]
    package_width=[2.1,3.41]
    singlecol_packwidth = 1.27
    angled_pack_width=1.0
    angled_pack_offset=0.5
    angled_pin_length=4.0
    angled_pin_width=0.4
    rmx_pad_offset=[1.5,1.95]
    rmx_pin_length=[2.5, 2.75]
    pin_width=0.4
    single_pad_smd=[3.0,0.65]
    dual_pad_smd=[2.4,0.74]
    for cols in [1, 2]:
        for rows in range(1, 41):
            makePinHeadStraight(rows, cols, rm, rm, package_width[cols-1],
                                singlecol_packwidth / 2 ,
                                singlecol_packwidth / 2 , ddrill, pad, [], "${KISYS3DMOD}/Pin_Headers", "Pin_Header", "pin header",
                                [0, 0, 0], [1, 1, 1], [0, 0, 0])
            makePinHeadAngled(rows, cols, rm, rm, angled_pack_width, angled_pack_offset, angled_pin_length,
                              angled_pin_width, ddrill, pad,
                              [], "${KISYS3DMOD}/Pin_Headers", "Pin_Header", "pin header", [0, 0, 0], [1, 1, 1], [0, 0, 0])
            makePinHeadAngled(rows, cols, rm, rm, angled_pack_width, angled_pack_offset, angled_pin_length,
                              angled_pin_width, ddrill, pad,
                              [], "${KISYS3DMOD}/Pin_Headers", "Pin_Header", "pin header", [0, 0, 0], [1, 1, 1], [0, 0, 0])
            if rows != 1 or cols == 2:
                if cols == 2:
                    makePinHeadStraightSMD(rows, cols, rm, rm, rmx_pad_offset[cols-1], rmx_pin_length[cols-1], pin_width,
                                           package_width[cols-1],
                                           singlecol_packwidth / 2 + singlecol_packoffset,
                                           singlecol_packwidth / 2 + singlecol_packoffset, dual_pad_smd,
                                           True, [], "${KISYS3DMOD}/Pin_Headers", "Pin_Header", "pin header",
                                           [0, 0, 0], [1, 1, 1], [0, 0, 0])
                if cols == 1:
                    makePinHeadStraightSMD(rows, cols, rm, rm, rmx_pad_offset[cols-1], rmx_pin_length[cols-1], pin_width,
                                           package_width[cols-1],
                                           singlecol_packwidth / 2 + singlecol_packoffset,
                                           singlecol_packwidth / 2 + singlecol_packoffset, single_pad_smd,
                                           True, [], "${KISYS3DMOD}/Pin_Headers", "Pin_Header", "pin header",
                                           [0, 0, 0], [1, 1, 1], [0, 0, 0])
                    makePinHeadStraightSMD(rows, cols, rm, rm, rmx_pad_offset[cols-1], rmx_pin_length[cols-1], pin_width,
                                           package_width[cols-1],
                                           singlecol_packwidth / 2 + singlecol_packoffset,
                                           singlecol_packwidth / 2 + singlecol_packoffset, single_pad_smd,
                                           False, [], "${KISYS3DMOD}/Pin_Headers", "Pin_Header", "pin header",
                                           [0, 0, 0], [1, 1, 1], [0, 0, 0])
