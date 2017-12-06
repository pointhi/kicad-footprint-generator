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
from footprint_scripts_terminal_blocks import *





if __name__ == '__main__':

    script_generated_note="script-generated using https://github.com/pointhi/kicad-footprint-generator/scripts/TerminalBlock_4Ucon";
    classname="TerminalBlock_4Ucon"
    
    

 
    pins=[2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    rm=3.5
    package_height=8.3
    leftbottom_offset=[2.25,package_height-3.7]
    ddrill=1.3
    pad=[2.6,2.6]
    bevel_height=[3.5]
    opening=[2.8,3.75]
    opening_yoffset=package_height-0.7-opening[1]
    secondHoleDiameter=2
    secondHoleOffset=[0,-(3.7-2.1)]
    thirdHoleDiameter=0
    thirdHoleOffset=[0,0]
    fourthHoleDiameter=0
    fourthHoleOffset=[0,0]
    fabref_offset=[0,3]
    nibbleSize=[]
    nibblePos=[]
    for pi in range(0,len(pins)):
        p=pins[pi];
        itemno=10691+p;
        name="{0}".format(itemno);
        webpage="http://www.4uconnector.com/online/object/4udrawing/{0}.pdf".format(itemno);
        classname_description="Terminal Block 4Ucon ItemNo. {0}".format(itemno);
        footprint_name="TerminalBlock_4Ucon_1x{2:02}_P{1:3.2f}mm_Vertical".format(name, rm, p)
        makeTerminalBlockVertical(footprint_name=footprint_name, 
                                  pins=p, rm=rm, 
                                  package_height=package_height, leftbottom_offset=leftbottom_offset, 
                                  ddrill=ddrill, pad=pad, 
                                  opening=opening, opening_yoffset=opening_yoffset, 
                                  bevel_height=bevel_height, secondHoleDiameter=secondHoleDiameter, secondHoleOffset=secondHoleOffset, thirdHoleDiameter=thirdHoleDiameter, thirdHoleOffset=thirdHoleOffset, fourthHoleDiameter=fourthHoleDiameter, fourthHoleOffset=fourthHoleOffset, 
                                  nibbleSize=nibbleSize, nibblePos=nibblePos, fabref_offset=fabref_offset,
                                  tags_additional=[], lib_name="${KISYS3DMOD}/"+classname, classname=classname, classname_description=classname_description, webpage=webpage, script_generated_note=script_generated_note)


    
    pins=[2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    itemnos=[19963,20193,20001,20223,19964,10684,19965,10686,10687,10688,10689,10690,10691,10692]
    rm=3.5
    package_height=7
    leftbottom_offset=[2.1, package_height-3.4]
    ddrill=1.2
    pad=[2.4,2.4]
    screw_diameter=2.75
    bevel_height=[1.5]
    slit_screw=False
    screw_pin_offset=[0,0]
    secondHoleDiameter=0
    secondHoleOffset=[0,0]
    thirdHoleDiameter=0
    thirdHoleOffset=[0,-4]
    fourthHoleDiameter=0
    fourthHoleOffset=[0,0]
    fabref_offset=[0,2.8]
    nibbleSize=[]
    nibblePos=[]
    for pi in range(0,len(pins)):
        p=pins[pi];
        itemno=itemnos[pi];
        name="{0}".format(itemno);
        webpage="http://www.4uconnector.com/online/object/4udrawing/{0}.pdf".format(itemno);
        classname_description="Terminal Block 4Ucon ItemNo. {0}".format(itemno);
        footprint_name="TerminalBlock_4Ucon_1x{2:02}_P{1:3.2f}mm_Horizontal".format(name, rm, p)
        makeTerminalBlockStd(footprint_name=footprint_name, 
                                  pins=p, rm=rm, 
                                  package_height=package_height, leftbottom_offset=leftbottom_offset, 
                                  ddrill=ddrill, pad=pad, screw_diameter=screw_diameter, bevel_height=bevel_height, slit_screw=slit_screw, screw_pin_offset=screw_pin_offset, secondHoleDiameter=secondHoleDiameter, secondHoleOffset=secondHoleOffset, thirdHoleDiameter=thirdHoleDiameter, thirdHoleOffset=thirdHoleOffset, fourthHoleDiameter=fourthHoleDiameter, fourthHoleOffset=fourthHoleOffset, 
                                  nibbleSize=nibbleSize, nibblePos=nibblePos, fabref_offset=fabref_offset,
                                  tags_additional=[], lib_name='${KISYS3DMOD}/'+classname, classname=classname, classname_description=classname_description, 
                                  webpage=webpage, script_generated_note=script_generated_note)

     
    
    
    
    
    