# -*- coding: utf8 -*-
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

#
# based on scripts\pin_headers_socket_strips
# refactored by Terje Io, <http://github.com/terjeio>
# updated for KLC3 and new naming convention
#

# Some datasheet sources:
#
# http://www.amphenol-icc.com/board-to-board.html?gender_filter=559
# http://www.taydaelectronics.com/connectors-sockets/pin-headers.html
# https://gct.co/board-to-board-connector/list?pitch=2.54mm%2C1.00mm&gender=Socket
# https://www.harwin.com/products/M50-3100545/
# https://lbconnector.en.alibaba.com/productgrouplist-804748813-8/Pin_Female_Box_Header.html?spm=a2700.8304367.costd19dbc.23.2ccc31d5Xg47e5&isGallery=Y
#

#
# NOTE: most footprints are based on legacy dimensions which does not have any documented datasheet sources
#

#import sys
#import os

#sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "\\..\\tools")

from socket_strips import *  # NOQA

if __name__ == '__main__':

    def getPadOffsets(overall_width, pads):
        result = []
        for i in range(0, len(pads)):
            result.append(round((overall_width[i] - pads[i][0]) / 2.0, 3))
        return result

    def getPinLength(overall_width, packwidth):
        result = []
        for i in range(0, len(overall_width)):
            result.append(round((overall_width[i] - packwidth[i]) / 2.0, 3))
        return result

    # bw  - body width
    # bo  - body offset
    # blo - body overlength
    # pl  - pin length, THT for 3D model
    # pad - pad size
    # drl - drill size
    # ow  - SMD, overall width (including pins)
    # lpo - SMD land pattern overall width
    # psz - SMD pin size (width, [, thickness for 3D model]) 
    # bh  - body height (3D parameter, PCB to top)
    
    # t  - typical
    # >  - min (greater or equal)
    # <  - max (smaller or equal)
    # NA - not available
    
    ######################
    # 2.54mm pin sockets #
    ######################

    # THT 1 row vertical:
    # KiCad legacy : bw: 2.54;             pad: 1.7; drl: 1.0
    # Amphenol FCi : bw: 2.54; blo: -0.08;           drl: >0.75; psz: 0.6, 0.2;  pl: 2.5; bh: 7.0

    # THT 2 cols vertical:
    # KiCad legacy : bw: 5.08;             pad: 1.7; drl: 1.0
    # Amphenol FCi : bw: 5.08; blo: -0.08;           drl: >0.8;  psz: 0.6, 0.2; pl: 2.5; bh: 7.0

    # THT 1 row horizontal:
    # KiCad legacy : bw: 8.51; bo: 1.52; pad: 1.7; drl: 1.0

    # THT 2 cols horizontal:
    # KiCad legacy : bw: 8.51; bo: 1.52; pad: 1.7; drl: 1.0

    # SMD 1 row:
    # Amphenol FCi 1: bw: 5.08;           blo: -0.08; pad: 2 - 1.0, <1.5; lpo: 6.1±0.2; psz: 0.6; bh: 7.0
    # V FHC50    1RL: bw: 2.50; ow: 4.80; blo: 0.60;  pad: 2.10, 1.02;    lpo: 5.5;     psz: 0.5, 0.2; bh: 5.0
    # V HOYATO    1*: bw: 2.50; ow: 4.05,             pad: 1.91, 1.00;    lpo; 5.2;     psz: 0.5, 0.2; bh: 7.5

    # SMD 2 cols vertical:
    # KiCad legacy   : bw: 5.08; ow: 8.04;             pad: 3.0, 1.0;                  psz: 1.38, 0.64
    # Amphenol FCi   : bw: 5.08; ow: 6.10; blo: -0.08; pad: t1.27, >4.2; lpo: 3.2±0.2; psz: 0.6;           bh: 7.0; Top entry
    # Amphenol FCi   : bw: 5.08; ow: 6.10; blo: -0.08; pad: t1.27, >1.4; lpo: 3.2±0.2; drl: 1.4; psz: 0.6; bh: 7.0; Dual entry
    # HOYATO PSDSM254: bw: 5.1;  ow: 7.2;              pad: 1.9, 1.2; psz: NA, 0.25 - with guide pins

    # common settings
    rm      = 2.54
    ddrill  = 1.0

    tht_pad              = [1.7, 1.7]
    tht_packwidth_vert   = [2.54, 5.08]
    tht_packoffset_vert  = [0, 0]
    tht_packwidth_horiz  = [8.51, 8.51]
    tht_packoffset_horiz = [1.52, 1.52]
    tht_pin_width_horiz  = 0.64

    smd_pin_width        = 0.64
    smd_packwidth_vert   = [2.54, 5.08]
    smd_overall_width    = [4.54, 7.84] # including pins
    smd_packoffset_vert  = [0, 0]
    smd_pads             = [[2.1, 1.0], [3.0, 1.0]]
    smd_overall_lp_width = [5.2, 8.04]
    smd_pin_length       = getPinLength(smd_overall_width, smd_packwidth_vert)
    smd_pad_offset       = getPadOffsets(smd_overall_lp_width, smd_pads)

    for rows in [1, 2]:

        tht_overlen_top    = rm / 2.0
        tht_overlen_bottom = tht_overlen_top
        smd_overlen_top    = tht_overlen_top
        smd_overlen_bottom = tht_overlen_top

        for cols in range(1, 41):
            makePinHeadStraight(cols, rows, rm, rm, tht_packwidth_vert[rows-1] + tht_packoffset_vert[rows-1],
                                tht_overlen_top, tht_overlen_bottom, ddrill, tht_pad, [],
                                "Conn_PinSocket_2.54mm", "PinSocket", "socket strip", isSocket=True)
            makeSocketStripAngled(cols, rows, rm, rm, tht_packwidth_horiz[rows-1], tht_packoffset_horiz[rows-1], tht_pin_width_horiz, ddrill, tht_pad, [],
                                 "Conn_PinSocket_2.54mm",  "PinSocket", "socket strip")
            if rows == 2:
                makePinHeadStraightSMD(cols, rows, rm, rm, smd_pad_offset[rows-1], smd_pin_length[rows-1], smd_pin_width,
                                       smd_packwidth_vert[rows-1] + smd_packoffset_vert[rows-1],
                                       smd_overlen_top, tht_overlen_bottom, smd_pads[rows-1], False, [],
                                       "Conn_PinSocket_2.54mm", "PinSocket", "socket strip", isSocket=True)
            elif cols > 1:
                makePinHeadStraightSMD(cols, rows, rm, rm, smd_pad_offset[rows-1], smd_pin_length[rows-1], smd_pin_width,
                                       smd_packwidth_vert[rows-1] + smd_packoffset_vert[rows-1],
                                       smd_overlen_top, smd_overlen_bottom, smd_pads[rows-1], True, [],
                                       "Conn_PinSocket_2.54mm", "PinSocket", "socket strip", isSocket=True)
                makePinHeadStraightSMD(cols, rows, rm, rm, smd_pad_offset[rows-1], smd_pin_length[rows-1], smd_pin_width,
                                       smd_packwidth_vert[rows-1] + smd_packoffset_vert[rows-1],
                                       smd_overlen_top, smd_overlen_bottom, smd_pads[rows-1], False, [],
                                       "Conn_PinSocket_2.54mm", "PinSocket", "socket strip", isSocket=True)

    ######################
    # 2.00mm pin sockets #
    ######################

    # THT 1 row vertical:
    # KiCad legacy : bw: 2.00;            pad: 1.35; drl: 0.8

    # THT 2 cols vertical:
    # KiCad legacy : bw: 4.00;            pad: 1.35; drl: 0.8
    # Amphenol FCi : bw: 4.20; blo: 0.8;                       psz: 0.5, 0.2;  pl: 2.5; bh: 7.0

    # THT 1 row horizontal:
    # KiCad legacy : bw: 6.35; bo: 1.27; pad: 1.7; drl: 1.0

    # THT 2 cols horizontal:
    # KiCad legacy : bw: 6.35; bo: 1.27; pad: 1.7; drl: 1.0

    # SMD 1 row LR:
    # 4601WVS-XX-6TV01 : bw: 2.5; ow: 4.2±0.15; blo: 0.6; pad: 2.0, 0.89; lpo: 5.2; psz: 0.5, 0.2; bh: 4.3
    #                  : bw: 2.4; ow: 4.2;      blo: 0.6; pad: 2.3, 0.90; lpo: 5.2; psz: 0.5, 0.2; bh: 4.3

    # SMD 2 cols vertical:
    # KiCad legacy   : bw: 4.0; ow: 6.00;             pad:  2.75,  1.0; lpo:  9.0; psz: 0.50
    # Amphenol FCi   : bw: 4.0; ow: 6.00; blo: -0.08; pad: >1.50, t1.0; lpo: >6.5; psz: 0.44, NA;    bh: 4.5
    # HOYATO PSDSM20 : bw: 4.0; ow: 6.15; blo: -0.08; pad:  2.00,  1.0; lpo:  7.0; psz: 0.50, NA;    bh: 4.5
    #                : bw: 4.0; ow: 6.00; blo:  0.60; pad:  2.30,  0.9; lpo:  7.0; psz: 0.50, 0.20;  bh: 4.3

    rm = 2.00
    ddrill = 0.8

    tht_pad              = [1.35, 1.35]
    tht_packwidth_vert   = [2.0, 4.0]
    tht_packoffset_vert  = [0, 0]
    tht_packwidth_horiz  = [6.35, 6.35]
    tht_packoffset_horiz = [1.27, 1.27]
    tht_pin_width_horiz  = 0.5

    smd_pin_width        = 0.5
    smd_packwidth_vert   = [2.0, 4.0]
    smd_overall_width    = [4.4, 6.0]
    smd_packoffset_vert  = [0, 0]
    smd_pads             = [[2.0, 0.9], [2.75, 1.0]]
    smd_overall_lp_width = [5.2, 9.0] # land pattern width (8.04)
    smd_pin_length       = getPinLength(smd_overall_width, smd_packwidth_vert)
    smd_pad_offset       = getPadOffsets(smd_overall_lp_width, smd_pads)

    for rows in [1, 2]:

        tht_overlen_top    = rm / 2.0
        tht_overlen_bottom = tht_overlen_top
        smd_overlen_top    = tht_overlen_top
        smd_overlen_bottom = tht_overlen_top

        for cols in range(1, 41):
            makePinHeadStraight(cols, rows, rm, rm, tht_packwidth_vert[rows-1] + tht_packoffset_vert[rows-1],
                                tht_overlen_top, tht_overlen_top, ddrill, tht_pad, [],
                                "Conn_PinSocket_2.00mm", "PinSocket", "socket strip", isSocket=True)
            makeSocketStripAngled(cols, rows, rm, rm, tht_packwidth_horiz[rows-1], tht_packoffset_horiz[rows-1],
                              tht_pin_width_horiz, ddrill, tht_pad, [],
                              "Conn_PinSocket_2.00mm", "PinSocket", "socket strip")
            if rows == 2:
                makePinHeadStraightSMD(cols, rows, rm, rm, smd_pad_offset[rows-1], smd_pin_length[rows-1], smd_pin_width,
                                       smd_packwidth_vert[rows-1] + smd_packoffset_vert[rows-1],
                                       smd_overlen_top, tht_overlen_top, smd_pads[rows-1], False, [],
                                       "Conn_PinSocket_2.00mm", "PinSocket", "socket strip", isSocket=True)
            elif cols > 1:
                makePinHeadStraightSMD(cols, rows, rm, rm, smd_pad_offset[rows-1], smd_pin_length[rows-1], smd_pin_width,
                                       smd_packwidth_vert[rows-1] + smd_packoffset_vert[rows-1],
                                       rm / 2.0 + tht_packoffset_vert[rows-1], rm / 2.0 + tht_packoffset_vert[rows-1], smd_pads[rows-1], True, [],
                                       "Conn_PinSocket_2.00mm", "PinSocket", "socket strip", isSocket=True)
                makePinHeadStraightSMD(cols, rows, rm, rm, smd_pad_offset[rows-1], smd_pin_length[rows-1], smd_pin_width,
                                       smd_packwidth_vert[rows-1] + tht_packoffset_vert[rows-1], smd_overlen_top, smd_overlen_bottom, smd_pads[rows-1], False, [],
                                      "Conn_PinSocket_2.00mm", "PinSocket", "socket strip", isSocket=True)

    ######################
    # 1.27mm pin sockets #
    ######################

    # THT 1 row vertical:
    # KiCad legacy : bw: 2.00;            pad: 1.00; drl: 0.7
    # InterContact : bw: 2.20; blo: NA;              drl: 0.6; pl: 2.45; bh: 4.1

    # THT 2 cols vertical:
    # KiCad legacy : bw: 3.05;            pad: 1.00; drl: 0.7
    # Amphenol FCi : bw: 3.00; blo: 0.46;            drl: 0.65; psz: 0.2, 0.4; pl: 2.4±0.3; bh: 4.4
    # InterContact : bw: 3.05;                       drl: 0.60;                pl: 2.45;    bh: 4.1,

    # THT 1 row horizontal:
    # InterContact : bw: 4.1, po: 1.2; drl: 0.60; pl: 3.00; bh: 2.2

    # THT 2 cols horizontal:
    # InterContact : bw: 4.1, po: 1.2;  drl: 0.60;                  pl: 3.00; bh: 3.05
    # GCT BD091    : bw: 4.4, po: 0.07; drl: 0.65; psz: 0.42, 0.15; pl: 2.00; bh: 3.10

    # SMD 1 row LR:
    # GCT BD074         : bw: 1.8; ow: 3.6; blo: 0.35; pad: 2.30, 0.70; lpo: 4.6; psz: 0.42, 0.15; bh: 2.2
    # GCT BD075         : bw: 1.8; ow: 3.6; blo: 0.35; pad: 1.80, 0.65; lpo: 3.5; psz: 0.42, 0.15; bh: 4.6

    # SMD 2 cols vertical:
    # KiCad legacy : bw: 2.54; ow: 5.11;                pad: 2.10, 0.75;      lpo: 5.7; psz: 0.40
    # Amphenol FCi : bw: 3.00; ow: 4.50±0.5; blo: 1.73; pad: 2.05, 0.76±0.05; lpo: 5.6; psz: 0.40, NA;   bh: 4.4
    # GCT BD064    : bw: 3.10; ow: 4.80±0.3; blo: 1.73; pad: 2.15, 0.65;      lpo: 5.8; psz: 0.42, 0.15; bh: 4.6
    
    # SMD 1 cols vertical:
    # GCT BD075    : bw: 1.80; ow: 3.50;     blo: 0.81; pad: 1.80, 0.65;      lpo: 4.5; psz: 0.42, 0.15; bh: 4.6

    rm = 1.27
    ddrill = 0.7

    tht_pad             = [1.0, 1.0]
    tht_packwidth_vert  = [2.54, 3.05]
    tht_packoffset_vert = [0.0, 0.0]

    smd_pin_width        = 0.4
    smd_packwidth_vert   = [1.80, 2.54]
    smd_overall_width    = [3.5, 5.11]
    smd_packoffset_vert  = [0.0, 0.0]
    smd_pads             = [[1.8, 0.65], [2.1, 0.75]]
    smd_overall_lp_width = [4.5, 5.7] # land pattern width
    smd_pin_length       = getPinLength(smd_overall_width, smd_packwidth_vert)
    smd_pad_offset       = getPadOffsets(smd_overall_lp_width, smd_pads)

    for rows in [1, 2]:

        tht_overlen_top    = rm / 2.0 # tht_packwidth_vert[rows-1] / 2.0 # + tht_packoffset_vert[rows-1]
        tht_overlen_bottom = tht_overlen_top
        smd_overlen_top    = tht_overlen_top
        smd_overlen_bottom = tht_overlen_top

        for cols in range(1, 41):
            makePinHeadStraight(cols, rows, rm, rm, tht_packwidth_vert[rows-1],
                                tht_overlen_top, tht_overlen_bottom, ddrill, tht_pad, [],
                                "Conn_PinSocket_1.27mm", "PinSocket", "socket strip", isSocket=True)
            if rows == 2:
                makePinHeadStraightSMD(cols, rows, rm, rm, smd_pad_offset[rows-1], smd_pin_length[rows-1], smd_pin_width,
                                       smd_packwidth_vert[rows-1],
                                       smd_overlen_top, smd_overlen_bottom, smd_pads[rows-1], False, [],
                                       "Conn_PinSocket_1.27mm", "PinSocket", "socket strip", isSocket=True)
            elif cols > 1:
                makePinHeadStraightSMD(cols, rows, rm, rm, smd_pad_offset[rows-1], smd_pin_length[rows-1], smd_pin_width,
                                       smd_packwidth_vert[rows-1] + smd_packoffset_vert[rows-1],
                                       rm / 2.0 + tht_packoffset_vert[rows-1], rm / 2.0 + tht_packoffset_vert[rows-1], smd_pads[rows-1], True, [],
                                       "Conn_PinSocket_1.27mm", "PinSocket", "socket strip", isSocket=True)
                makePinHeadStraightSMD(cols, rows, rm, rm, smd_pad_offset[rows-1], smd_pin_length[rows-1], smd_pin_width,
                                       smd_packwidth_vert[rows-1] + tht_packoffset_vert[rows-1], smd_overlen_top, smd_overlen_bottom, smd_pads[rows-1], False, [],
                                       "Conn_PinSocket_1.27mm", "PinSocket", "socket strip", isSocket=True)

    ######################
    # 1.00mm pin sockets #
    ######################

    # THT 1 row vertical:
    # GHC BC065    : bw: 1.50; blo: 0.75;              drl: 0.5; pl: 1.8; bh: 2.1

    # THT 2 cols vertical:

    # SMD 1 row LR:
    # GCT BC070    : bw: 1.5; ow: 2.9; blo: 0.75; pad: 1.95, 0.50; lpo: 3.9; psz: 0.30, 0.10; bh: 2.25

    # SMD 2 cols vertical:
    # GCT BC085    : bw: 2.5; ow: 3.90±0.25; blo: 0.25; pad: 1.85, 0.50;      lpo: 4.9; psz: 0.30, 0.10; bh: 2.25

    rm = 1.00
    ddrill = 0.5

    tht_pad             = [0.85, 0.85]
    tht_packwidth_vert  = [1.50, 3.05]
    tht_packoffset_vert = [0.75, 0.0]
    tht_overlen         = 0.75
    tht_pad_offset      = 0.29
    
    smd_pin_width        = 0.3
    smd_packwidth_vert   = [1.50, 2.5]
    smd_overall_width    = [2.9, 3.9]
    smd_packoffset_vert  = [0.0, 0.0]
    smd_overlen          = 0.75
    smd_pads             = [[1.95, 0.50], [1.85, 0.50]]
    smd_overall_lp_width = [3.9, 4.9] # land pattern width
    smd_pin_length       = getPinLength(smd_overall_width, smd_packwidth_vert)
    smd_pad_offset       = getPadOffsets(smd_overall_lp_width, smd_pads)

    for rows in [1, 2]:

        tht_overlen_top    = tht_overlen
        tht_overlen_bottom = tht_overlen
        smd_overlen_top    = smd_overlen
        smd_overlen_bottom = smd_overlen

        for cols in range(1, 41):
            if rows == 2:
                makePinHeadStraightSMD(cols, rows, rm, rm, smd_pad_offset[rows-1], smd_pin_length[rows-1], smd_pin_width,
                                       smd_packwidth_vert[rows-1],
                                       smd_overlen_top, smd_overlen_bottom, smd_pads[rows-1], False, [],
                                       "Conn_PinSocket_1.00mm", "PinSocket", "socket strip", isSocket=True)
            elif cols > 1:
                makePinHeadStraight(cols, rows, rm, rm, tht_packwidth_vert[rows-1],
                                    tht_overlen_top, tht_overlen_bottom, ddrill, tht_pad, [],
                                    "Conn_PinSocket_1.00mm", "PinSocket", "socket strip", isSocket=True, pad_offset=tht_pad_offset)
                makePinHeadStraightSMD(cols, rows, rm, rm, smd_pad_offset[rows-1], smd_pin_length[rows-1], smd_pin_width,
                                       smd_packwidth_vert[rows-1] + smd_packoffset_vert[rows-1],
                                       smd_overlen_top, smd_overlen_bottom, smd_pads[rows-1], True, [],
                                       "Conn_PinSocket_1.00mm", "PinSocket", "socket strip", isSocket=True)
                makePinHeadStraightSMD(cols, rows, rm, rm, smd_pad_offset[rows-1], smd_pin_length[rows-1], smd_pin_width,
                                       smd_packwidth_vert[rows-1] + smd_packoffset_vert[rows-1],
                                       smd_overlen_top, smd_overlen_bottom, smd_pads[rows-1], False, [],
                                       "Conn_PinSocket_1.00mm", "PinSocket", "socket strip", isSocket=True)

### EOF ###
