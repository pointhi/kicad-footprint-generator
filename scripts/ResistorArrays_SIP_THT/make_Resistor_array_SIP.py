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
from drawing_tools import *
from footprint_scripts_sip import *


if __name__ == '__main__':
    for R in range(3, 14):
        pins=R+1
        makeSIP(pins, "Resistor_Array_SIP%d" % (pins), "{0}-pin Resistor SIP pack".format(pins, R))
    #for R in range(3,6):
    #    pins=2*R
    #    makeSIP(pins, "Resistor_ArrayParallel_SIP%d" % (R), "{0}-pin Resistor SIP pack, {1} parallel resistors".format(pins, R))
    #for R in range(3,6):
    #    pins=R+2
    #    makeSIP(pins, "Resistor_ArrayDivider_SIP%d" % (R), "{0}-pin Resistor SIP pack, {1} voltage dividers = {2} resistors".format(pins, R, 2*R))
