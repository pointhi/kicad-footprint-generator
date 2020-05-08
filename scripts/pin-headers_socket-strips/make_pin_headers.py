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
                                singlecol_packwidth / 2 + singlecol_packoffset, ddrill, pad, [], "/Pin_Headers", "Pin_Header", "pin header",
                                [0, 0, 0], [1, 1, 1], [0, 0, 0], "${KISYS3DMOD}")
            makePinHeadAngled(rows, cols, rm, rm, angled_pack_width, angled_pack_offset, angled_pin_length, angled_pin_width, ddrill, pad,
                              [], "/Pin_Headers", "Pin_Header", "pin header", [0, 0, 0], [1, 1, 1], [0, 0, 0], "${KISYS3DMOD}")
            if rows != 1 or cols == 2:
              if cols == 2:
                  makePinHeadStraightSMD(rows, cols, rm, rm, rmx_pad_offset[cols-1], rmx_pin_length[cols-1], pin_width, cols * singlecol_packwidth + singlecol_packoffset,
                                      singlecol_packwidth / 2 + singlecol_packoffset,
                                      singlecol_packwidth / 2 + singlecol_packoffset, dual_pad_smd,
                                         True, [], "/Pin_Headers", "Pin_Header", "pin header",
                                         [0, 0, 0], [1, 1, 1], [0, 0, 0], "${KISYS3DMOD}")
              if cols==1:
                  makePinHeadStraightSMD(rows, cols, rm, rm, rmx_pad_offset[cols-1], rmx_pin_length[cols-1], pin_width,
                                     cols * singlecol_packwidth + singlecol_packoffset,
                                     singlecol_packwidth / 2 + singlecol_packoffset,
                                     singlecol_packwidth / 2 + singlecol_packoffset, single_pad_smd,
                                     True, [], "/Pin_Headers", "Pin_Header", "pin header",
                                     [0, 0, 0], [1, 1, 1], [0, 0, 0], "${KISYS3DMOD}")
                  makePinHeadStraightSMD(rows, cols, rm, rm, rmx_pad_offset[cols-1], rmx_pin_length[cols-1], pin_width,
                                     cols * singlecol_packwidth + singlecol_packoffset,
                                     singlecol_packwidth / 2 + singlecol_packoffset,
                                     singlecol_packwidth / 2 + singlecol_packoffset, single_pad_smd,
                                     False, [], "/Pin_Headers", "Pin_Header", "pin header",
                                     [0, 0, 0], [1, 1, 1], [0, 0, 0], "${KISYS3DMOD}")

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
                                singlecol_packwidth / 2 + singlecol_packoffset, ddrill, pad, [], "Pin_Headers", "Pin_Header", "pin header",
                                [0, 0, 0], [1, 1, 1], [0, 0, 0], "${KISYS3DMOD}")
            makePinHeadAngled(rows, cols, rm, rm, angled_pack_width, angled_pack_offset, angled_pin_length,
                              angled_pin_width, ddrill, pad,
                              [], "Pin_Headers", "Pin_Header", "pin header", [0, 0, 0], [1, 1, 1], [0, 0, 0], "${KISYS3DMOD}")
            if rows != 1 or cols == 2:
              if cols == 2:
                  makePinHeadStraightSMD(rows, cols, rm, rm, rmx_pad_offset[cols-1], rmx_pin_length[cols-1], pin_width,
                                         cols * singlecol_packwidth + singlecol_packoffset,
                                         singlecol_packwidth / 2 + singlecol_packoffset,
                                         singlecol_packwidth / 2 + singlecol_packoffset, dual_pad_smd,
                                         True, [], "Pin_Headers", "Pin_Header", "pin header",
                                         [0, 0, 0], [1, 1, 1], [0, 0, 0], "${KISYS3DMOD}")
              if cols == 1:
                  makePinHeadStraightSMD(rows, cols, rm, rm, rmx_pad_offset[cols-1], rmx_pin_length[cols-1], pin_width,
                                         cols * singlecol_packwidth + singlecol_packoffset,
                                         singlecol_packwidth / 2 + singlecol_packoffset,
                                         singlecol_packwidth / 2 + singlecol_packoffset, single_pad_smd,
                                         True, [], "Pin_Headers", "Pin_Header", "pin header",
                                         [0, 0, 0], [1, 1, 1], [0, 0, 0], "${KISYS3DMOD}")
                  makePinHeadStraightSMD(rows, cols, rm, rm, rmx_pad_offset[cols-1], rmx_pin_length[cols-1], pin_width,
                                         cols * singlecol_packwidth + singlecol_packoffset,
                                         singlecol_packwidth / 2 + singlecol_packoffset,
                                         singlecol_packwidth / 2 + singlecol_packoffset, single_pad_smd,
                                         False, [], "Pin_Headers", "Pin_Header", "pin header",
                                         [0, 0, 0], [1, 1, 1], [0, 0, 0], "${KISYS3DMOD}")

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
                                singlecol_packwidth / 2 , ddrill, pad, [], "Pin_Headers", "Pin_Header", "pin header",
                                [0, 0, 0], [1, 1, 1], [0, 0, 0], "${KISYS3DMOD}")
            makePinHeadAngled(rows, cols, rm, rm, angled_pack_width, angled_pack_offset, angled_pin_length,
                              angled_pin_width, ddrill, pad,
                              [], "Pin_Headers", "Pin_Header", "pin header", [0, 0, 0], [1, 1, 1], [0, 0, 0], "${KISYS3DMOD}")
            if rows != 1 or cols == 2:
                if cols == 2:
                    makePinHeadStraightSMD(rows, cols, rm, rm, rmx_pad_offset[cols-1], rmx_pin_length[cols-1], pin_width,
                                           package_width[cols-1],
                                           singlecol_packwidth / 2 + singlecol_packoffset,
                                           singlecol_packwidth / 2 + singlecol_packoffset, dual_pad_smd,
                                           True, [], "Pin_Headers", "Pin_Header", "pin header",
                                           [0, 0, 0], [1, 1, 1], [0, 0, 0], "${KISYS3DMOD}")
                if cols == 1:
                    makePinHeadStraightSMD(rows, cols, rm, rm, rmx_pad_offset[cols-1], rmx_pin_length[cols-1], pin_width,
                                           package_width[cols-1],
                                           singlecol_packwidth / 2 + singlecol_packoffset,
                                           singlecol_packwidth / 2 + singlecol_packoffset, single_pad_smd,
                                           True, [], "Pin_Headers", "Pin_Header", "pin header",
                                           [0, 0, 0], [1, 1, 1], [0, 0, 0], "${KISYS3DMOD}")
                    makePinHeadStraightSMD(rows, cols, rm, rm, rmx_pad_offset[cols-1], rmx_pin_length[cols-1], pin_width,
                                           package_width[cols-1],
                                           singlecol_packwidth / 2 + singlecol_packoffset,
                                           singlecol_packwidth / 2 + singlecol_packoffset, single_pad_smd,
                                           False, [], "Pin_Headers", "Pin_Header", "pin header",
                                           [0, 0, 0], [1, 1, 1], [0, 0, 0], "${KISYS3DMOD}")
    #single row THT Straight headers https://gct.co/pdfjs/web/viewer.html?file=/Files/Drawings/BC020.pdf&t=1502019369628
    #dual row THT Straight headers https://gct.co/files/drawings/bc035.pdf
    #single row THT Angled headers https://gct.co/pdfjs/web/viewer.html?file=/Files/Drawings/BC030.pdf&t=1502031327147
    #dual row THT Angled headers https://gct.co/files/drawings/bc045.pdf
    #single row SMD Straight headers http://www.farnell.com/datasheets/1912818.pdf?_ga=2.101918145.1303212991.1501602361-984110936.1498471838
    #dual row SMD Straight headers https://gct.co/files/drawings/bc050.pdf
    rm = 1.0
    ddrill = 0.5
    pad = [0.85, 0.85]
    package_width=[1.27,2.3]
    singlecol_packwidth = 1.00
    angled_pack_width=[1.0, 1.2]
    angled_pack_offset= [0.25, 0.9]
    angled_pin_length=2.0
    angled_pin_width=0.3
    rmx_pad_offset=[0.875, 1.65]
    rmx_pin_length=[1.25, 2.4]
    pin_width=0.3
    single_pad_smd=[1.75,0.6]
    dual_pad_smd=[2.0,0.5]
    for cols in [1, 2]:
        for rows in range(1, 41):
            makePinHeadStraight(rows, cols, rm, rm, package_width[cols-1],
                                singlecol_packwidth / 2 ,
                                singlecol_packwidth / 2 , ddrill, pad, [], "Pin_Headers", "Pin_Header", "pin header",
                                [0, 0, 0], [1, 1, 1], [0, 0, 0], "${KISYS3DMOD}")
            makePinHeadAngled(rows, cols, rm, rm, angled_pack_width[cols-1], angled_pack_offset[cols-1], angled_pin_length,
                              angled_pin_width, ddrill, pad,
                              [], "Pin_Headers", "Pin_Header", "pin header", [0, 0, 0], [1, 1, 1], [0, 0, 0], "${KISYS3DMOD}")
            
            if rows != 1 or cols == 2:
                if cols == 2:
                    makePinHeadStraightSMD(rows, cols, rm, rm, rmx_pad_offset[cols-1], rmx_pin_length[cols-1], pin_width,
                                           package_width[cols-1],
                                           singlecol_packwidth / 2 + singlecol_packoffset,
                                           singlecol_packwidth / 2 + singlecol_packoffset, dual_pad_smd,
                                           True, [], "Pin_Headers", "Pin_Header", "pin header",
                                           [0, 0, 0], [1, 1, 1], [0, 0, 0], "${KISYS3DMOD}")
                
                if cols == 1:
                    makePinHeadStraightSMD(rows, cols, rm, rm, rmx_pad_offset[cols-1], rmx_pin_length[cols-1], pin_width,
                                           package_width[cols-1],
                                           singlecol_packwidth / 2 + singlecol_packoffset,
                                           singlecol_packwidth / 2 + singlecol_packoffset, single_pad_smd,
                                           True, [], "Pin_Headers", "Pin_Header", "pin header",
                                           [0, 0, 0], [1, 1, 1], [0, 0, 0], "${KISYS3DMOD}")
                    makePinHeadStraightSMD(rows, cols, rm, rm, rmx_pad_offset[cols-1], rmx_pin_length[cols-1], pin_width,
                                           package_width[cols-1],
                                           singlecol_packwidth / 2 + singlecol_packoffset,
                                           singlecol_packwidth / 2 + singlecol_packoffset, single_pad_smd,
                                           False, [], "Pin_Headers", "Pin_Header", "pin header",
                                           [0, 0, 0], [1, 1, 1], [0, 0, 0], "${KISYS3DMOD}")
