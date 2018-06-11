#!/usr/bin/env python

from __future__ import division

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
from footprint_scripts_terminal_blocks import *


if __name__ == '__main__':
    script_generated_note = ("script-generated using https://github.com"
            "/pointhi/kicad-footprint-generator/scripts/TerminalBlock_TE-Connectivity")
    long_classname = "TerminalBlock_TE-Connectivity"
    classname = "TerminalBlock_TE"

    pins = range(2,12+1)
    rm = 2.54
    package_height = 6.5
    leftbottom_offset = [1.5, 3.25]
    ddrill = 1.1
    pad = [2.2,2.2]
    screw_diameter = 2.2
    bevel_height = [0.4,5.5]
    slit_screw = True
    screw_pin_offset = [0,0]
    secondDrillDiameter = 0
    secondDrillOffset = [0,2.54]
    secondDrillPad = [0,0]
    secondHoleDiameter = 0
    secondHoleOffset = [0,0]
    thirdHoleDiameter = 0
    thirdHoleOffset = [0,-4]
    fourthHoleDiameter = 0
    fourthHoleOffset = [0,0]
    fabref_offset = [0,2.0]
    nibbleSize = []
    nibblePos = []
    for p in pins:
        name_prefix = "{}-".format(p // 10) if p // 10 > 0 else ""
        name = "{}282834-{}".format(name_prefix, p % 10)
        webpage = ("http://www.te.com/commerce/DocumentDelivery/DDEController"
                "?Action=showdoc&DocId=Customer+Drawing%7F282834%7FC1%7Fpdf"
                "%7FEnglish%7FENG_CD_282834_C1.pdf")
        classname_description = "Terminal Block TE {0}".format(name)
        footprint_name = "{}_{}_1x{:02}_P{:3.2f}mm_Horizontal".format(
                classname, name, p, rm)
        makeTerminalBlockStd(footprint_name=footprint_name,
                pins=p,
                rm=rm, 
                package_height=package_height,
                leftbottom_offset=leftbottom_offset, 
                ddrill=ddrill,
                pad=pad,
                screw_diameter=screw_diameter,
                bevel_height=bevel_height,
                slit_screw=slit_screw,
                screw_pin_offset=screw_pin_offset,
                secondHoleDiameter=secondHoleDiameter,
                secondHoleOffset=secondHoleOffset,
                thirdHoleDiameter=thirdHoleDiameter,
                thirdHoleOffset=thirdHoleOffset,
                fourthHoleDiameter=fourthHoleDiameter,
                fourthHoleOffset=fourthHoleOffset, 
                secondDrillDiameter=secondDrillDiameter,
                secondDrillOffset=secondDrillOffset,
                secondDrillPad=secondDrillPad,
                nibbleSize=nibbleSize,
                nibblePos=nibblePos,
                fabref_offset=fabref_offset,
                tags_additional=[],
                lib_name='${KISYS3DMOD}/'+long_classname,
                classname=classname,
                classname_description=classname_description,
                webpage=webpage,
                script_generated_note=script_generated_note)
