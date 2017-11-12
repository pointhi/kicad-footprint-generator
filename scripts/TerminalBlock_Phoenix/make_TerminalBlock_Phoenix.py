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

    script_generated_note="script-generated using https://github.com/pointhi/kicad-footprint-generator/scripts/TerminalBlock_Phoenix";
    classname="TerminalBlock_Phoenix"
    
    
 
    pins=range(2,8+1)
    rm=2.5
    package_height=5
    leftbottom_offset=[3-0.65, 0.9, 0.65]
    ddrill=1.2
    pad=[2,2]
    bevel_height=[]
    opening=[2,1]
    opening_xoffset=1
    opening_yoffset=3.0
    secondDrillDiameter=ddrill
    secondDrillOffset=[0,-3.1]
    secondDrillPad=pad
    secondHoleDiameter=2
    secondHoleOffset=[-1,-0.5]
    thirdHoleDiameter=0
    thirdHoleOffset=[-1,-1]
    fourthHoleDiameter=0
    fourthHoleOffset=[0,0]
    fabref_offset=[0,-3.56]
    nibbleSize=[]
    nibblePos=[]
    for p in pins:
        name="PTSM-0,5-{0}-{1:1.2}-V-THR".format(p,rm);
        webpage="http://www.produktinfo.conrad.com/datenblaetter/550000-574999/556444-da-01-de-LEITERPLATTENKL__PTSM_0_5__4_2_5_V_THR.pdf";
        classname_description="Terminal Block Phoenix {0}".format(name);
        footprint_name="TerminalBlock_Phoenix_{0}_1x{2:02}_P{1:3.2f}mm_Vertical".format(name, rm, p)
        makeTerminalBlockVertical(footprint_name=footprint_name, 
                                  pins=p, rm=rm, 
                                  package_height=package_height, leftbottom_offset=leftbottom_offset, opening_xoffset=opening_xoffset, opening_yoffset=opening_yoffset, opening=opening,
                                  ddrill=ddrill, pad=pad, bevel_height=bevel_height, secondHoleDiameter=secondHoleDiameter, secondHoleOffset=secondHoleOffset, thirdHoleDiameter=thirdHoleDiameter, thirdHoleOffset=thirdHoleOffset, fourthHoleDiameter=fourthHoleDiameter, fourthHoleOffset=fourthHoleOffset, 
                                  secondDrillDiameter=secondDrillDiameter,secondDrillOffset=secondDrillOffset,secondDrillPad=secondDrillPad,
                                  nibbleSize=nibbleSize, nibblePos=nibblePos, fabref_offset=fabref_offset,
                                  tags_additional=[], lib_name='${KISYS3DMOD}/'+classname, classname=classname, classname_description=classname_description, 
                                  webpage=webpage, script_generated_note=script_generated_note)
   
 
    pins=range(2,8+1)
    rm=2.5
    package_height=10
    leftbottom_offset=[2.35, 2.8]
    ddrill=1.2
    pad=[1.8,3]
    screw_diameter=0
    bevel_height=[]
    slit_screw=False
    screw_pin_offset=[0,0]
    secondDrillDiameter=ddrill
    secondDrillOffset=[0,-5]
    secondDrillPad=pad
    secondHoleDiameter=[1,1]
    secondHoleOffset=[0,6.5]
    thirdHoleDiameter=0
    thirdHoleOffset=[0,-4]
    fourthHoleDiameter=0
    fourthHoleOffset=[0,0]
    fabref_offset=[0,0]
    nibbleSize=[]
    nibblePos=[]
    for p in pins:
        name="PTSM-0,5-{0}-{1:1.2}-H-THR".format(p,rm);
        webpage="http://www.produktinfo.conrad.com/datenblaetter/550000-574999/556441-da-01-de-LEITERPLATTENKL__PTSM_0_5__8_2_5_H_THR.pdf";
        classname_description="Terminal Block Phoenix {0}".format(name);
        footprint_name="TerminalBlock_Phoenix_{0}_1x{2:02}_P{1:3.2f}mm_Horizontal".format(name, rm, p)
        makeTerminalBlockStd(footprint_name=footprint_name, 
                                  pins=p, rm=rm, 
                                  package_height=package_height, leftbottom_offset=leftbottom_offset, 
                                  ddrill=ddrill, pad=pad, screw_diameter=screw_diameter, bevel_height=bevel_height, slit_screw=slit_screw, screw_pin_offset=screw_pin_offset, secondHoleDiameter=secondHoleDiameter, secondHoleOffset=secondHoleOffset, thirdHoleDiameter=thirdHoleDiameter, thirdHoleOffset=thirdHoleOffset, fourthHoleDiameter=fourthHoleDiameter, fourthHoleOffset=fourthHoleOffset, 
                                  secondDrillDiameter=secondDrillDiameter,secondDrillOffset=secondDrillOffset,secondDrillPad=secondDrillPad,
                                  nibbleSize=nibbleSize, nibblePos=nibblePos, fabref_offset=fabref_offset,
                                  tags_additional=[], lib_name='${KISYS3DMOD}/'+classname, classname=classname, classname_description=classname_description, 
                                  webpage=webpage, script_generated_note=script_generated_note)
   
 
    pins=range(2,16+1)
    rm=5.08
    package_height=9.8
    leftbottom_offset=[rm/2, 4.6]
    ddrill=1.3
    pad=[2.6,2.6]
    screw_diameter=3
    bevel_height=[0.5,2,6.9]
    slit_screw=True
    screw_pin_offset=[0,0]
    secondHoleDiameter=0
    secondHoleOffset=[0,0]
    thirdHoleDiameter=0
    thirdHoleOffset=[0,-4]
    fourthHoleDiameter=0
    fourthHoleOffset=[0,0]
    fabref_offset=[0,3.5]
    nibbleSize=[]
    nibblePos=[]
    for p in pins:
        name="MKDS-1,5-{0}-{1:2.3}".format(p,rm);
        webpage="http://www.farnell.com/datasheets/100425.pdf";
        classname_description="Terminal Block Phoenix {0}".format(name);
        footprint_name="TerminalBlock_Phoenix_{0}_1x{2:02}_P{1:3.2f}mm_Horizontal".format(name, rm, p)
        makeTerminalBlockStd(footprint_name=footprint_name, 
                                  pins=p, rm=rm, 
                                  package_height=package_height, leftbottom_offset=leftbottom_offset, 
                                  ddrill=ddrill, pad=pad, screw_diameter=screw_diameter, bevel_height=bevel_height, slit_screw=slit_screw, screw_pin_offset=screw_pin_offset, secondHoleDiameter=secondHoleDiameter, secondHoleOffset=secondHoleOffset, thirdHoleDiameter=thirdHoleDiameter, thirdHoleOffset=thirdHoleOffset, fourthHoleDiameter=fourthHoleDiameter, fourthHoleOffset=fourthHoleOffset, 
                                  nibbleSize=nibbleSize, nibblePos=nibblePos, fabref_offset=fabref_offset,
                                  tags_additional=[], lib_name='${KISYS3DMOD}/'+classname, classname=classname, classname_description=classname_description, 
                                  webpage=webpage, script_generated_note=script_generated_note)

     
   
    pins=range(2,16+1)
    rm=5
    package_height=9.8
    leftbottom_offset=[rm/2, 4.6]
    ddrill=1.3
    pad=[2.6,2.6]
    screw_diameter=3
    bevel_height=[0.5,2,6.9]
    slit_screw=True
    screw_pin_offset=[0,0]
    secondHoleDiameter=0
    secondHoleOffset=[0,0]
    thirdHoleDiameter=0
    thirdHoleOffset=[0,-4]
    fourthHoleDiameter=0
    fourthHoleOffset=[0,0]
    fabref_offset=[0,3.5]
    nibbleSize=[]
    nibblePos=[]
    for p in pins:
        name="MKDS-1,5-{0}".format(p);
        webpage="http://www.farnell.com/datasheets/100425.pdf";
        classname_description="Terminal Block Phoenix {0}".format(name);
        footprint_name="TerminalBlock_Phoenix_{0}_1x{2:02}_P{1:3.2f}mm_Horizontal".format(name, rm, p)
        makeTerminalBlockStd(footprint_name=footprint_name, 
                                  pins=p, rm=rm, 
                                  package_height=package_height, leftbottom_offset=leftbottom_offset, 
                                  ddrill=ddrill, pad=pad, screw_diameter=screw_diameter, bevel_height=bevel_height, slit_screw=slit_screw, screw_pin_offset=screw_pin_offset, secondHoleDiameter=secondHoleDiameter, secondHoleOffset=secondHoleOffset, thirdHoleDiameter=thirdHoleDiameter, thirdHoleOffset=thirdHoleOffset, fourthHoleDiameter=fourthHoleDiameter, fourthHoleOffset=fourthHoleOffset, 
                                  nibbleSize=nibbleSize, nibblePos=nibblePos, fabref_offset=fabref_offset,
                                  tags_additional=[], lib_name='${KISYS3DMOD}/'+classname, classname=classname, classname_description=classname_description, 
                                  webpage=webpage, script_generated_note=script_generated_note)
  

    
    pins=range(2,16+1)
    rm=5.08
    package_height=11.2
    leftbottom_offset=[rm/2, 5.3]
    ddrill=1.3
    pad=[2.6,2.6]
    screw_diameter=4
    bevel_height=[0.5,3,9.2]
    slit_screw=True
    screw_pin_offset=[0,0]
    secondHoleDiameter=0
    secondHoleOffset=[0,0]
    thirdHoleDiameter=0
    thirdHoleOffset=[0,-4]
    fourthHoleDiameter=0
    fourthHoleOffset=[0,0]
    fabref_offset=[0,3.4]
    nibbleSize=[]
    nibblePos=[]
    for p in pins:
        name="MKDS-3-{0}-{1:2.3}".format(p,rm);
        webpage="http://www.farnell.com/datasheets/2138224.pdf";
        classname_description="Terminal Block Phoenix {0}".format(name);
        footprint_name="TerminalBlock_Phoenix_{0}_1x{2:02}_P{1:3.2f}mm_Horizontal".format(name, rm, p)
        makeTerminalBlockStd(footprint_name=footprint_name, 
                                  pins=p, rm=rm, 
                                  package_height=package_height, leftbottom_offset=leftbottom_offset, 
                                  ddrill=ddrill, pad=pad, screw_diameter=screw_diameter, bevel_height=bevel_height, slit_screw=slit_screw, screw_pin_offset=screw_pin_offset, secondHoleDiameter=secondHoleDiameter, secondHoleOffset=secondHoleOffset, thirdHoleDiameter=thirdHoleDiameter, thirdHoleOffset=thirdHoleOffset, fourthHoleDiameter=fourthHoleDiameter, fourthHoleOffset=fourthHoleOffset, 
                                  nibbleSize=nibbleSize, nibblePos=nibblePos, fabref_offset=fabref_offset,
                                  tags_additional=[], lib_name='${KISYS3DMOD}/'+classname, classname=classname, classname_description=classname_description, 
                                  webpage=webpage, script_generated_note=script_generated_note)

     
    
     

    
    pins=range(2,16+1)
    rm=3.5
    package_height=7.6
    leftbottom_offset=[rm/2, package_height-3.1]
    ddrill=1.2
    pad=[2.4,2.4]
    screw_diameter=3
    bevel_height=[0.4,1.5]
    slit_screw=True
    screw_pin_offset=[0,0]
    secondDrillDiameter=0
    secondDrillOffset=[0,2.54]
    secondDrillPad=[0,0]
    secondHoleDiameter=0
    secondHoleOffset=[0,0]
    thirdHoleDiameter=0
    thirdHoleOffset=[0,-4]
    fourthHoleDiameter=0
    fourthHoleOffset=[0,0]
    fabref_offset=[0,1.7]
    nibbleSize=[]
    nibblePos=[]
    for p in pins:
        name="PT-1,5-{0}-{1:1.2}-H".format(p,rm);
        webpage="";
        classname_description="Terminal Block Phoenix {0}".format(name);
        footprint_name="TerminalBlock_Phoenix_{0}_1x{2:02}_P{1:3.2f}mm_Horizontal".format(name, rm, p)
        makeTerminalBlockStd(footprint_name=footprint_name, 
                                  pins=p, rm=rm, 
                                  package_height=package_height, leftbottom_offset=leftbottom_offset, 
                                  ddrill=ddrill, pad=pad, screw_diameter=screw_diameter, bevel_height=bevel_height, slit_screw=slit_screw, screw_pin_offset=screw_pin_offset, secondHoleDiameter=secondHoleDiameter, secondHoleOffset=secondHoleOffset, thirdHoleDiameter=thirdHoleDiameter, thirdHoleOffset=thirdHoleOffset, fourthHoleDiameter=fourthHoleDiameter, fourthHoleOffset=fourthHoleOffset, 
                                  secondDrillDiameter=secondDrillDiameter,secondDrillOffset=secondDrillOffset,secondDrillPad=secondDrillPad,
                                  nibbleSize=nibbleSize, nibblePos=nibblePos, fabref_offset=fabref_offset,
                                  tags_additional=[], lib_name='${KISYS3DMOD}/'+classname, classname=classname, classname_description=classname_description, 
                                  webpage=webpage, script_generated_note=script_generated_note)
    
    
     

    
    pins=range(2,16+1)
    rm=5.0
    package_height=9
    leftbottom_offset=[rm/2, package_height-4]
    ddrill=1.3
    pad=[2.6,2.6]
    screw_diameter=4
    bevel_height=[0.4,1.5]
    slit_screw=True
    screw_pin_offset=[0,0]
    secondDrillDiameter=0
    secondDrillOffset=[0,2.54]
    secondDrillPad=[0,0]
    secondHoleDiameter=0
    secondHoleOffset=[0,0]
    thirdHoleDiameter=0
    thirdHoleOffset=[0,-4]
    fourthHoleDiameter=0
    fourthHoleOffset=[0,0]
    fabref_offset=[0,2.4]
    nibbleSize=[]
    nibblePos=[]
    for p in pins:
        name="PT-1,5-{0}-{1:1.2}-H".format(p,rm);
        webpage="http://www.mouser.com/ds/2/324/ItemDetail_1935161-922578.pdf";
        classname_description="Terminal Block Phoenix {0}".format(name);
        footprint_name="TerminalBlock_Phoenix_{0}_1x{2:02}_P{1:3.2f}mm_Horizontal".format(name, rm, p)
        makeTerminalBlockStd(footprint_name=footprint_name, 
                                  pins=p, rm=rm, 
                                  package_height=package_height, leftbottom_offset=leftbottom_offset, 
                                  ddrill=ddrill, pad=pad, screw_diameter=screw_diameter, bevel_height=bevel_height, slit_screw=slit_screw, screw_pin_offset=screw_pin_offset, secondHoleDiameter=secondHoleDiameter, secondHoleOffset=secondHoleOffset, thirdHoleDiameter=thirdHoleDiameter, thirdHoleOffset=thirdHoleOffset, fourthHoleDiameter=fourthHoleDiameter, fourthHoleOffset=fourthHoleOffset, 
                                  secondDrillDiameter=secondDrillDiameter,secondDrillOffset=secondDrillOffset,secondDrillPad=secondDrillPad,
                                  nibbleSize=nibbleSize, nibblePos=nibblePos, fabref_offset=fabref_offset,
                                  tags_additional=[], lib_name='${KISYS3DMOD}/'+classname, classname=classname, classname_description=classname_description, 
                                  webpage=webpage, script_generated_note=script_generated_note)

      

    
    pins=range(2,3+1)
    rm=2.54
    package_height=6.2
    leftbottom_offset=[1.5, 3.1]
    ddrill=1.1
    pad=[2.2,2.2]
    screw_diameter=2.2
    bevel_height=[0.5,5.8]
    slit_screw=True
    screw_pin_offset=[0,0]
    secondDrillDiameter=1.1
    secondDrillOffset=[0,2.54]
    secondDrillPad=[0,0]
    secondHoleDiameter=0
    secondHoleOffset=[0,0]
    thirdHoleDiameter=0
    thirdHoleOffset=[0,-4]
    fourthHoleDiameter=0
    fourthHoleOffset=[0,0]
    fabref_offset=[0,2.0]
    nibbleSize=[]
    nibblePos=[]
    for p in pins:
        name="MPT-0,5-{0}-{1:2.3}".format(p,rm);
        webpage="http://www.mouser.com/ds/2/324/ItemDetail_1725656-920552.pdf";
        classname_description="Terminal Block Phoenix {0}".format(name);
        footprint_name="TerminalBlock_Phoenix_{0}_1x{2:02}_P{1:3.2f}mm_Horizontal".format(name, rm, p)
        makeTerminalBlockStd(footprint_name=footprint_name, 
                                  pins=p, rm=rm, 
                                  package_height=package_height, leftbottom_offset=leftbottom_offset, 
                                  ddrill=ddrill, pad=pad, screw_diameter=screw_diameter, bevel_height=bevel_height, slit_screw=slit_screw, screw_pin_offset=screw_pin_offset, secondHoleDiameter=secondHoleDiameter, secondHoleOffset=secondHoleOffset, thirdHoleDiameter=thirdHoleDiameter, thirdHoleOffset=thirdHoleOffset, fourthHoleDiameter=fourthHoleDiameter, fourthHoleOffset=fourthHoleOffset, 
                                  secondDrillDiameter=secondDrillDiameter,secondDrillOffset=secondDrillOffset,secondDrillPad=secondDrillPad,
                                  nibbleSize=nibbleSize, nibblePos=nibblePos, fabref_offset=fabref_offset,
                                  tags_additional=[], lib_name='${KISYS3DMOD}/'+classname, classname=classname, classname_description=classname_description, 
                                  webpage=webpage, script_generated_note=script_generated_note)

    
   
    pins=range(4,12+1)
    rm=2.54
    package_height=6.2
    leftbottom_offset=[1.5, 3.1]
    ddrill=1.1
    pad=[2.2,2.2]
    screw_diameter=2.2
    bevel_height=[0.5,5.8]
    slit_screw=True
    screw_pin_offset=[0,0]
    secondDrillDiameter=0
    secondDrillOffset=[0,2.54]
    secondDrillPad=[0,0]
    secondHoleDiameter=0
    secondHoleOffset=[0,0]
    thirdHoleDiameter=0
    thirdHoleOffset=[0,-4]
    fourthHoleDiameter=0
    fourthHoleOffset=[0,0]
    fabref_offset=[0,2.0]
    nibbleSize=[]
    nibblePos=[]
    for p in pins:
        name="MPT-0,5-{0}-{1:2.3}".format(p,rm);
        webpage="http://www.mouser.com/ds/2/324/ItemDetail_1725672-916605.pdf";
        classname_description="Terminal Block Phoenix {0}".format(name);
        footprint_name="TerminalBlock_Phoenix_{0}_1x{2:02}_P{1:3.2f}mm_Horizontal".format(name, rm, p)
        makeTerminalBlockStd(footprint_name=footprint_name, 
                                  pins=p, rm=rm, 
                                  package_height=package_height, leftbottom_offset=leftbottom_offset, 
                                  ddrill=ddrill, pad=pad, screw_diameter=screw_diameter, bevel_height=bevel_height, slit_screw=slit_screw, screw_pin_offset=screw_pin_offset, secondHoleDiameter=secondHoleDiameter, secondHoleOffset=secondHoleOffset, thirdHoleDiameter=thirdHoleDiameter, thirdHoleOffset=thirdHoleOffset, fourthHoleDiameter=fourthHoleDiameter, fourthHoleOffset=fourthHoleOffset, 
                                  secondDrillDiameter=secondDrillDiameter,secondDrillOffset=secondDrillOffset,secondDrillPad=secondDrillPad,
                                  nibbleSize=nibbleSize, nibblePos=nibblePos, fabref_offset=fabref_offset,
                                  tags_additional=[], lib_name='${KISYS3DMOD}/'+classname, classname=classname, classname_description=classname_description, 
                                  webpage=webpage, script_generated_note=script_generated_note)

    
    
    
    
    