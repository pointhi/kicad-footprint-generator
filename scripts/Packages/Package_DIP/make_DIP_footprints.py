#!/usr/bin/env python

import sys
import os
import math

# ensure that the kicad-footprint-generator directory is available
#sys.path.append(os.environ.get('KIFOOTPRINTGENERATOR'))  # enable package import from parent directory
#sys.path.append("D:\hardware\KiCAD\kicad-footprint-generator")  # enable package import from parent directory
sys.path.append(os.path.join(sys.path[0],"..","..","..","kicad_mod")) # load kicad_mod path
sys.path.append(os.path.join(sys.path[0],"..","..","..")) # load kicad_mod path
sys.path.append(os.path.join(sys.path[0],"..","..","tools")) # load kicad_mod path

from KicadModTree import *  # NOQA
from footprint_scripts_DIP import *





if __name__ == '__main__':
    # common settings
    overlen_top=1.27
    overlen_bottom=1.27
    rm=2.54
    ddrill=0.8
    pad=[1.6,1.6]
    pad_large=[2.4,1.6]
    pad_smdsocket=[3.1,1.6]
    pad_smdsocket_small=[1.6,1.6]

    # narrow 7.62 DIPs
    pins=[4,6,8,10,12,14,16,18,20,22,24,28]
    pinrow_distance=7.62
    package_width=6.35
    socket_width=pinrow_distance+2.54
    for p in pins:
        makeDIP(p,rm,pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad,False,0,0,0)
        makeDIP(p, rm, pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad_large, False, 0,0,0, ["LongPads"])
        socket_height = (p / 2 - 1) * rm + 2.54
        makeDIP(p, rm, pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad, False, socket_width,socket_height,0, ["Socket"])
        makeDIP(p, rm, pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad_large, False, socket_width,socket_height,0,  ["Socket","LongPads"])
        makeDIP(p, rm, pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad_smdsocket, True, socket_width,socket_height,1.27, ["SMDSocket","LongPads"])
        makeDIP(p, rm, pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad_smdsocket_small, True,socket_width, socket_height, 0, ["SMDSocket", "SmallPads"])

    # narrow 7.62 DIPs
    pins=[4,6,8,10,12,14,16,]
    pinrow_distance=10.16
    package_width=6.35
    socket_width=pinrow_distance+2.54
    for p in pins:
        makeDIP(p,rm,pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad,False,0,0,0)
        makeDIP(p, rm, pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad_large, False, 0,0,0, ["LongPads"])

    # mid 10.16 DIPs
    pins=[22,24]
    pinrow_distance=10.16
    package_width=9.14
    socket_width=pinrow_distance+2.54
    for p in pins:
        makeDIP(p,rm,pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad,False,0,0,0)
        makeDIP(p, rm, pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad_large, False, 0,0,0, ["LongPads"])
        socket_height = (p / 2 - 1) * rm + 2.54
        makeDIP(p, rm, pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad, False, socket_width,socket_height,0, ["Socket"])
        makeDIP(p, rm, pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad_large, False, socket_width,socket_height,0,  ["Socket","LongPads"])
        makeDIP(p, rm, pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad_smdsocket, True,
            socket_width, socket_height, 1.27, ["SMDSocket", "LongPads"])
        makeDIP(p, rm, pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad_smdsocket_small, True,
            socket_width, socket_height, 0, ["SMDSocket", "SmallPads"])

    # mid 15.24 DIPs
    pins=[24,28,32,40,42,48,64]
    pinrow_distance=15.24
    package_width=14.73
    socket_width=pinrow_distance+2.54
    for p in pins:
        makeDIP(p,rm,pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad,False,0,0,0)
        makeDIP(p, rm, pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad_large, False, 0,0,0, ["LongPads"])
        socket_height = (p / 2 - 1) * rm + 2.54
        makeDIP(p, rm, pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad, False, socket_width,socket_height,0, ["Socket"])
        makeDIP(p, rm, pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad_large, False, socket_width,socket_height,0,  ["Socket","LongPads"])
        makeDIP(p, rm, pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad_smdsocket, True,
            socket_width, socket_height, 1.27, ["SMDSocket", "LongPads"])
        makeDIP(p, rm, pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad_smdsocket_small, True,
            socket_width, socket_height, 0, ["SMDSocket", "SmallPads"])

    # large 22.86 DIPs
    pins=[64]
    pinrow_distance=22.86
    package_width=22.35
    socket_width=pinrow_distance+2.54
    for p in pins:
        makeDIP(p,rm,pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad,False,0,0,0)
        makeDIP(p, rm, pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad_large, False, 0,0,0, ["LongPads"])
        socket_height = (p / 2 - 1) * rm + 2.54
        makeDIP(p, rm, pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad, False, socket_width,socket_height,0, ["Socket"])
        makeDIP(p, rm, pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad_large, False, socket_width,socket_height,0,  ["Socket","LongPads"])
        makeDIP(p, rm, pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad_smdsocket, True,
            socket_width, socket_height, 1.27, ["SMDSocket", "LongPads"])
        makeDIP(p, rm, pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad_smdsocket_small, True,
            socket_width, socket_height, 0, ["SMDSocket", "SmallPads"])

    # large 25.4 DIPs
    pins=[40,64]
    pinrow_distance=25.4
    package_width=24.89
    socket_width=pinrow_distance+2.54
    for p in pins:
        makeDIP(p,rm,pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad,False,0,0,0)
        makeDIP(p, rm, pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad_large, False, 0,0,0, ["LongPads"])
        socket_height = (p / 2 - 1) * rm + 2.54
        makeDIP(p, rm, pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad, False, socket_width,socket_height,0, ["Socket"])
        makeDIP(p, rm, pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad_large, False, socket_width,socket_height,0,  ["Socket","LongPads"])
        makeDIP(p, rm, pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad_smdsocket, True,
            socket_width, socket_height, 1.27, ["SMDSocket", "LongPads"])
        makeDIP(p, rm, pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad_smdsocket_small, True,
            socket_width, socket_height, 0, ["SMDSocket", "SmallPads"])

    # special SMD footprints
    smd_pins=[4,6,8,10,12,14,16,18,20,22,24,32]
    pad_smd = [2, 1.78]
    smd_pinrow_distances=[7.62, 9.53, 11.48]
    package_width=6.35
    for p in smd_pins:
        for prd in smd_pinrow_distances:
            makeDIP(p, rm, prd, package_width, overlen_top, overlen_bottom, ddrill, pad_smd, True,  0,0,0, [], "Housings_DIP", [0, 0, 0], [1, 1, 1], [0, 0, 0], 'SMDIP', 'surface-mounted (SMD) DIP', 'SMD DIP DIL PDIP SMDIP')
    smd_pins=[4,6,8,10,12,14,16,18,20,22]
    pad_smd = [1.5, 1.78]
    smd_pinrow_distances=[9.53]
    package_width=6.35
    for p in smd_pins:
        for prd in smd_pinrow_distances:
            makeDIP(p, rm, prd, package_width, overlen_top, overlen_bottom, ddrill, pad_smd, True,  0,0,0, ['Clearance8mm'], "Housings_DIP", [0, 0, 0], [1, 1, 1], [0, 0, 0], 'SMDIP', 'surface-mounted (SMD) DIP', 'SMD DIP DIL PDIP SMDIP')

    smd_pins=[24,28,32,40,42,48,64]
    pad_smd = [2, 1.78]
    smd_pinrow_distances=[15.24]
    package_width=14.73
    for p in smd_pins:
        for prd in smd_pinrow_distances:
            makeDIP(p, rm, prd, package_width, overlen_top, overlen_bottom, ddrill, pad_smd, True,  0,0,0, [], "Housings_DIP", [0, 0, 0], [1, 1, 1], [0, 0, 0], 'SMDIP', 'surface-mounted (SMD) DIP', 'SMD DIP DIL PDIP SMDIP')
    smd_pins=[40]
    pad_smd = [2, 1.78]
    smd_pinrow_distances=[25.24]
    package_width=24.89
    for p in smd_pins:
        for prd in smd_pinrow_distances:
            makeDIP(p, rm, prd, package_width, overlen_top, overlen_bottom, ddrill, pad_smd, True,  0,0,0, [], "Housings_DIP", [0, 0, 0], [1, 1, 1], [0, 0, 0], 'SMDIP', 'surface-mounted (SMD) DIP', 'SMD DIP DIL PDIP SMDIP')


    # DIP-switches:
    pins=[2,4,6,8,10,12,14,16,18,20,22,24]
    pinrow_distance = 7.62
    package_width = 9.78
    switch_width=4.06
    switch_height=1.27
    overlen_top = 2.36
    overlen_bottom = 2.36
    package_width_narrow = 6.68
    switch_width_narrow = 3.62
    switch_height_narrow = 1.27
    overlen_top_narrow = 2.05
    overlen_bottom_narrow = 2.05
    pad_smd=[2.44,1.12]
    pinrow_distance_smd=8.61
    switch_width_piano=1.8
    switch_height_piano=1.5
    package_width_piano=10.8
    overlen_top_piano = 2.05
    overlen_bottom_piano = 2.05

    for p in pins:
        makeDIPSwitch(p, rm, pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad, switch_width, switch_height, 'Slide', False, [])
        makeDIPSwitch(p, rm, pinrow_distance, package_width_narrow, overlen_top_narrow, overlen_bottom_narrow, ddrill, pad, switch_width_narrow, switch_height_narrow, 'Slide', False, ["LowProfile"])
        makeDIPSwitch(p, rm, pinrow_distance_smd, package_width_narrow, overlen_top_narrow, overlen_bottom_narrow, ddrill, pad_smd, switch_width_narrow, switch_height_narrow, 'Slide', True,["SMD","LowProfile"], 'Buttons_Switches_SMD')
        makeDIPSwitch(p, rm, pinrow_distance, package_width_piano, overlen_top_piano, overlen_bottom_piano, ddrill, pad, switch_width_piano, switch_height_piano, 'Piano', False, [])

    # Copal CVS DIP-switches (http://www.nidec-copal-electronics.com/e/catalog/switch/cvs.pdf):
    pins = [2, 4, 6, 8, 16]
    rm = 1
    pinrow_distance = 5.9
    package_width = 4.7
    switch_width = 2
    switch_height = 0.5
    overlen_top = 1
    overlen_bottom = 1
    ddrill = 0
    pad_smd = [1.2, 0.5]

    for p in pins:
        makeDIPSwitch(p, rm, pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad_smd, switch_width,
                      switch_height, 'Slide', True, ["Copal_CVS"], "Buttons_Switches_SMD", [0, 0, 0], [1, 1, 1],
                      [0, 0, 0], "", True, [0.7, 0.7], 0.2, 0)



    # Omron A6H DIP-switches (https://www.omron.com/ecb/products/pdf/en-a6h.pdf):
    pins = [4,8,12,16,20]
    rm = 1.27
    pinrow_distance = 6.15
    package_width = 4.5
    switch_width = 3.2
    switch_height = 0.5
    overlen_top = 1.27
    overlen_bottom = 1.27
    ddrill = 0
    pad_smd = [1.25, 0.76]
    
    for p in pins:
        makeDIPSwitch(p, rm, pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad_smd, switch_width,
                      switch_height, 'Slide', True, ["Omron_A6H"], "Buttons_Switches_SMD", [0, 0, 0], [1, 1, 1],
                      [0, 0, 0], "", True)

    # Copal CHS DIP-switches (http://www.nidec-copal-electronics.com/e/catalog/switch/chs.pdf):
    pins = [2, 4, 8, 12, 16, 20]
    rm = 1.27
    pinrow_distance = 5.08
    pinrow_distanceB = 7.62
    package_width = 5.4
    switch_width = 3
    switch_height = 0.5
    overlen_top = 1.27
    overlen_bottom = 1.27
    ddrill = 0
    pad_smd = [1.6, 0.76]
    
    for p in pins:
        makeDIPSwitch(p, rm, pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad_smd, switch_width,
                      switch_height, 'Slide', True, ["Copal_CHS-A"], "Buttons_Switches_SMD", [0, 0, 0], [1, 1, 1],
                      [0, 0, 0], "", True)
        makeDIPSwitch(p, rm, pinrow_distanceB, package_width, overlen_top, overlen_bottom, ddrill, pad_smd, switch_width,
                      switch_height, 'Slide', True, ["Copal_CHS-B"], "Buttons_Switches_SMD", [0, 0, 0], [1, 1, 1],
                      [0, 0, 0], "", True)

    #
    # Special DIP
    #
    # http://www.experimentalistsanonymous.com/diy/Datasheets/MN3005.pdf
    #
    # common settings
    overlen_top=1.27
    overlen_bottom=1.27
    rm=2.54
    ddrill=0.8
    pad=[1.6,1.6]
    pad_large=[2.4,1.6]
    pad_smdsocket=[3.1,1.6]
    pad_smdsocket_small=[1.6,1.6]

    # narrow 7.62 DIPs
    pins=[8]
    pinrow_distance=7.62
    package_width=6.35
    socket_width=pinrow_distance+2.54
    makeDIP(16, rm, pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad,       False, 0, 0, 0, prefix_name = '8', skip_pin = [3, 4, 5, 6, 11, 12, 13, 14], skip_count = True, right_cnt_start = 5)
    socket_height = (p / 2 - 1) * rm + 2.54
    makeDIP(16, rm, pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad,       False, socket_width, socket_height,0, ["Socket"],            prefix_name = '8', skip_pin = [3, 4, 5, 6, 11, 12, 13, 14], skip_count = True, right_cnt_start = 5)
    makeDIP(16, rm, pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad_large, False, socket_width, socket_height,0, ["Socket","LongPads"], prefix_name = '8', skip_pin = [3, 4, 5, 6, 11, 12, 13, 14], skip_count = True, right_cnt_start = 5)
