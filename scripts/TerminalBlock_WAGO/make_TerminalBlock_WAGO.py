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

    script_generated_note="script-generated using https://github.com/pointhi/kicad-footprint-generator/scripts/TerminalBlock_WAGO";
    classname="TerminalBlock_WAGO"
    
    

   
    
    pins=[1,2,3,4,5,6,7,8,9,10,12,16,24]
    rm=7.5
    package_height=15
    leftbottom_offset=[2.75, 6.7, 3.75]
    ddrill=1.2
    pad=[2,3]
    screw_diameter=2.2
    bevel_height=[2.9]
    vsegment_lines_offset=[-1.25]
    opening=[2.9,2.3]
    opening_xoffset=1.25
    opening_yoffset=1.45
    opening_elliptic=True
    secondDrillDiameter=ddrill
    secondDrillOffset=[2.5,-5]
    secondDrillPad=pad
    secondHoleDiameter=[4,4.4]
    secondHoleOffset=[1.25,0]
    thirdHoleDiameter=[4,1]
    thirdHoleOffset=[1.25,0]
    fourthHoleDiameter=3#4
    fourthHoleOffset=[1.25,-5.75]
    fifthHoleDiameter=0
    fifthHoleOffset=[2.5,-0.75]
    secondEllipseSize=[0,0]
    secondEllipseOffset=[1.25,2.5]
    fabref_offset=[0,-1]
    nibbleSize=[]
    nibblePos=[]
    for p in pins:
        name="804-{0}".format(300+p);
        webpage="";
        classname_description="Terminal Block WAGO {0}".format(name);
        footprint_name="TerminalBlock_WAGO_{0}_1x{2:02}_P{1:3.2f}mm_45Degree".format(name, rm, p)
        makeTerminalBlock45Degree(footprint_name=footprint_name, 
                                  pins=p, rm=rm, 
                                  package_height=package_height, leftbottom_offset=leftbottom_offset, 
                                  ddrill=ddrill, pad=pad, vsegment_lines_offset=vsegment_lines_offset,
                                  opening=opening, opening_xoffset=opening_xoffset, opening_yoffset=opening_yoffset, opening_elliptic=opening_elliptic,
                                  bevel_height=bevel_height, secondHoleDiameter=secondHoleDiameter, secondHoleOffset=secondHoleOffset, thirdHoleDiameter=thirdHoleDiameter, thirdHoleOffset=thirdHoleOffset, fourthHoleDiameter=fourthHoleDiameter, fourthHoleOffset=fourthHoleOffset, fifthHoleDiameter=fifthHoleDiameter,fifthHoleOffset=fifthHoleOffset,
                                  secondDrillDiameter=secondDrillDiameter,secondDrillOffset=secondDrillOffset,secondDrillPad=secondDrillPad,
                                  secondEllipseSize=secondEllipseSize,secondEllipseOffset=secondEllipseOffset,
                                  nibbleSize=nibbleSize, nibblePos=nibblePos, fabref_offset=fabref_offset,
                                  tags_additional=[], lib_name="${KISYS3DMOD}/"+classname, classname=classname, classname_description=classname_description, webpage=webpage, script_generated_note=script_generated_note)

     
     

    
    pins=[1,2,3,4,5,6,7,8,9,10,12,16,24]
    rm=5
    package_height=15
    leftbottom_offset=[2.75, 6.7, 3.75]
    ddrill=1.2
    pad=[2,3]
    screw_diameter=2.2
    bevel_height=[2.9]
    vsegment_lines_offset=[-1.25]
    opening=[2.9,2.3]
    opening_xoffset=1.25
    opening_yoffset=1.45
    opening_elliptic=True
    secondDrillDiameter=ddrill
    secondDrillOffset=[2.5,-5]
    secondDrillPad=pad
    secondHoleDiameter=[4,4.4]
    secondHoleOffset=[1.25,0]
    thirdHoleDiameter=[4,1]
    thirdHoleOffset=[1.25,0]
    fourthHoleDiameter=3#4
    fourthHoleOffset=[1.25,-5.75]
    fifthHoleDiameter=0
    fifthHoleOffset=[1.25,-0.75]
    secondEllipseSize=[0,0]
    secondEllipseOffset=[1.25,2.5]
    fabref_offset=[0,-1]
    nibbleSize=[]
    nibblePos=[]
    for p in pins:
        name="804-{0}".format(100+p);
        webpage="";
        classname_description="Terminal Block WAGO {0}".format(name);
        footprint_name="TerminalBlock_WAGO_{0}_1x{2:02}_P{1:3.2f}mm_45Degree".format(name, rm, p)
        makeTerminalBlock45Degree(footprint_name=footprint_name, 
                                  pins=p, rm=rm, 
                                  package_height=package_height, leftbottom_offset=leftbottom_offset, 
                                  ddrill=ddrill, pad=pad,  vsegment_lines_offset=vsegment_lines_offset,
                                  opening=opening, opening_xoffset=opening_xoffset, opening_yoffset=opening_yoffset, opening_elliptic=opening_elliptic,
                                  bevel_height=bevel_height, secondHoleDiameter=secondHoleDiameter, secondHoleOffset=secondHoleOffset, thirdHoleDiameter=thirdHoleDiameter, thirdHoleOffset=thirdHoleOffset, fourthHoleDiameter=fourthHoleDiameter, fourthHoleOffset=fourthHoleOffset, fifthHoleDiameter=fifthHoleDiameter,fifthHoleOffset=fifthHoleOffset,
                                  secondDrillDiameter=secondDrillDiameter,secondDrillOffset=secondDrillOffset,secondDrillPad=secondDrillPad,
                                  secondEllipseSize=secondEllipseSize,secondEllipseOffset=secondEllipseOffset,
                                  nibbleSize=nibbleSize, nibblePos=nibblePos, fabref_offset=fabref_offset,
                                  tags_additional=[], lib_name="${KISYS3DMOD}/"+classname, classname=classname, classname_description=classname_description, webpage=webpage, script_generated_note=script_generated_note)


    pins=[1,2,3,4,6,8,12,16,24,36,48]
    rm=5
    package_height=14
    leftbottom_offset=[3.5, 9, 3.8]
    ddrill=1.15
    pad=[1.5,3]
    screw_diameter=2.2
    bevel_height=[1,6.7,9.5]
    opening=[4,3.3]
    opening_xoffset=0.5
    opening_yoffset=1.3#package_height-leftbottom_offset[1]-opening[1]/2
    secondDrillDiameter=ddrill
    secondDrillOffset=[0,5]
    secondDrillPad=pad
    secondHoleDiameter=[5,14]
    secondHoleOffset=[0.5,2]
    thirdHoleDiameter=[4,1]
    thirdHoleOffset=[0.5,3.2]
    fourthHoleDiameter=[1,2.5]
    fourthHoleOffset=[0.5,-3.4]
    fabref_offset=[0,-1]
    nibbleSize=[]
    nibblePos=[]
    for p in pins:
        name="236-{0}".format(100+p);
        webpage="";
        classname_description="Terminal Block WAGO {0}".format(name);
        footprint_name="TerminalBlock_WAGO_{0}_1x{2:02}_P{1:3.2f}mm_45Degree".format(name, rm, p)
        makeTerminalBlock45Degree(footprint_name=footprint_name, 
                                  pins=p, rm=rm, 
                                  package_height=package_height, leftbottom_offset=leftbottom_offset, 
                                  ddrill=ddrill, pad=pad, 
                                  opening=opening, opening_xoffset=opening_xoffset, opening_yoffset=opening_yoffset, 
                                  bevel_height=bevel_height, secondHoleDiameter=secondHoleDiameter, secondHoleOffset=secondHoleOffset, thirdHoleDiameter=thirdHoleDiameter, thirdHoleOffset=thirdHoleOffset, fourthHoleDiameter=fourthHoleDiameter, fourthHoleOffset=fourthHoleOffset, 
                                  nibbleSize=nibbleSize, nibblePos=nibblePos, fabref_offset=fabref_offset,
                                  tags_additional=[], lib_name="${KISYS3DMOD}/"+classname, classname=classname, classname_description=classname_description, webpage=webpage, script_generated_note=script_generated_note)
        name="236-{0}".format(400+p);
        webpage="";
        classname_description="Terminal Block WAGO {0}".format(name);
        footprint_name="TerminalBlock_WAGO_{0}_1x{2:02}_P{1:3.2f}mm_45Degree".format(name, rm, p)
        makeTerminalBlock45Degree(footprint_name=footprint_name, 
                                  pins=p, rm=rm, 
                                  package_height=package_height, leftbottom_offset=leftbottom_offset, 
                                  ddrill=ddrill, pad=pad, 
                                  opening=opening, opening_xoffset=opening_xoffset, opening_yoffset=opening_yoffset, 
                                  bevel_height=bevel_height, secondHoleDiameter=secondHoleDiameter, secondHoleOffset=secondHoleOffset, thirdHoleDiameter=thirdHoleDiameter, thirdHoleOffset=thirdHoleOffset, fourthHoleDiameter=fourthHoleDiameter, fourthHoleOffset=fourthHoleOffset, 
                                  secondDrillDiameter=secondDrillDiameter,secondDrillOffset=secondDrillOffset,secondDrillPad=secondDrillPad,
                                  nibbleSize=nibbleSize, nibblePos=nibblePos, fabref_offset=fabref_offset,
                                  tags_additional=[], lib_name="${KISYS3DMOD}/"+classname, classname=classname, classname_description=classname_description, webpage=webpage, script_generated_note=script_generated_note)

    pins=[1,2,3,4,6,8,12,16,24]
    rm=7.5
    package_height=14
    leftbottom_offset=[3.5, 9, 6.3]
    ddrill=1.15
    pad=[1.5,3]
    screw_diameter=2.2
    bevel_height=[1,6.7,9.5]
    opening=[4,3.3]
    opening_xoffset=0.5
    opening_yoffset=1.3#package_height-leftbottom_offset[1]-opening[1]/2
    secondDrillDiameter=ddrill
    secondDrillOffset=[0,5]
    secondDrillPad=pad
    secondHoleDiameter=[rm,package_height]
    secondHoleOffset=[1.75,2]
    thirdHoleDiameter=[4,1]
    thirdHoleOffset=[0.5,3.2]
    fourthHoleDiameter=1,2.5
    fourthHoleOffset=[0.5,-3.4]
    fabref_offset=[0,-1]
    nibbleSize=[]
    nibblePos=[]
    for p in pins:
        name="236-{0}".format(200+p);
        webpage="";
        classname_description="Terminal Block WAGO {0}".format(name);
        footprint_name="TerminalBlock_WAGO_{0}_1x{2:02}_P{1:3.2f}mm_45Degree".format(name, rm, p)
        makeTerminalBlock45Degree(footprint_name=footprint_name, 
                                  pins=p, rm=rm, 
                                  package_height=package_height, leftbottom_offset=leftbottom_offset, 
                                  ddrill=ddrill, pad=pad, 
                                  opening=opening, opening_xoffset=opening_xoffset, opening_yoffset=opening_yoffset, 
                                  bevel_height=bevel_height, secondHoleDiameter=secondHoleDiameter, secondHoleOffset=secondHoleOffset, thirdHoleDiameter=thirdHoleDiameter, thirdHoleOffset=thirdHoleOffset, fourthHoleDiameter=fourthHoleDiameter, fourthHoleOffset=fourthHoleOffset, 
                                  nibbleSize=nibbleSize, nibblePos=nibblePos, fabref_offset=fabref_offset,
                                  tags_additional=[], lib_name="${KISYS3DMOD}/"+classname, classname=classname, classname_description=classname_description, webpage=webpage, script_generated_note=script_generated_note)
        name="236-{0}".format(500+p);
        webpage="";
        classname_description="Terminal Block WAGO {0}".format(name);
        footprint_name="TerminalBlock_WAGO_{0}_1x{2:02}_P{1:3.2f}mm_45Degree".format(name, rm, p)
        makeTerminalBlock45Degree(footprint_name=footprint_name, 
                                  pins=p, rm=rm, 
                                  package_height=package_height, leftbottom_offset=leftbottom_offset, 
                                  ddrill=ddrill, pad=pad, 
                                  opening=opening, opening_xoffset=opening_xoffset, opening_yoffset=opening_yoffset, 
                                  bevel_height=bevel_height, secondHoleDiameter=secondHoleDiameter, secondHoleOffset=secondHoleOffset, thirdHoleDiameter=thirdHoleDiameter, thirdHoleOffset=thirdHoleOffset, fourthHoleDiameter=fourthHoleDiameter, fourthHoleOffset=fourthHoleOffset, 
                                  secondDrillDiameter=secondDrillDiameter,secondDrillOffset=secondDrillOffset,secondDrillPad=secondDrillPad,
                                  nibbleSize=nibbleSize, nibblePos=nibblePos, fabref_offset=fabref_offset,
                                  tags_additional=[], lib_name="${KISYS3DMOD}/"+classname, classname=classname, classname_description=classname_description, webpage=webpage, script_generated_note=script_generated_note)

    pins=[1,2,3,4,6,8,12,16,24]
    rm=10
    package_height=14
    leftbottom_offset=[3.5, 9, 8.8]
    ddrill=1.15
    pad=[1.5,3]
    screw_diameter=2.2
    bevel_height=[1,6.7,9.5]
    opening=[4,3.3]
    opening_xoffset=0.5
    opening_yoffset=1.3#package_height-leftbottom_offset[1]-opening[1]/2
    secondDrillDiameter=ddrill
    secondDrillOffset=[0,5]
    secondDrillPad=pad
    secondHoleDiameter=[rm,package_height]
    secondHoleOffset=[3,2]
    thirdHoleDiameter=[4,1]
    thirdHoleOffset=[0.5,3.2]
    fourthHoleDiameter=1,2.5
    fourthHoleOffset=[0.5,-3.4]
    fabref_offset=[0,-1]
    nibbleSize=[]
    nibblePos=[]
    for p in pins:
        name="236-{0}".format(300+p);
        webpage="";
        classname_description="Terminal Block WAGO {0}".format(name);
        footprint_name="TerminalBlock_WAGO_{0}_1x{2:02}_P{1:3.2f}mm_45Degree".format(name, rm, p)
        makeTerminalBlock45Degree(footprint_name=footprint_name, 
                                  pins=p, rm=rm, 
                                  package_height=package_height, leftbottom_offset=leftbottom_offset, 
                                  ddrill=ddrill, pad=pad, 
                                  opening=opening, opening_xoffset=opening_xoffset, opening_yoffset=opening_yoffset, 
                                  bevel_height=bevel_height, secondHoleDiameter=secondHoleDiameter, secondHoleOffset=secondHoleOffset, thirdHoleDiameter=thirdHoleDiameter, thirdHoleOffset=thirdHoleOffset, fourthHoleDiameter=fourthHoleDiameter, fourthHoleOffset=fourthHoleOffset, 
                                  nibbleSize=nibbleSize, nibblePos=nibblePos, fabref_offset=fabref_offset,
                                  tags_additional=[], lib_name="${KISYS3DMOD}/"+classname, classname=classname, classname_description=classname_description, webpage=webpage, script_generated_note=script_generated_note)
        name="236-{0}".format(600+p);
        webpage="";
        classname_description="Terminal Block WAGO {0}".format(name);
        footprint_name="TerminalBlock_WAGO_{0}_1x{2:02}_P{1:3.2f}mm_45Degree".format(name, rm, p)
        makeTerminalBlock45Degree(footprint_name=footprint_name, 
                                  pins=p, rm=rm, 
                                  package_height=package_height, leftbottom_offset=leftbottom_offset, 
                                  ddrill=ddrill, pad=pad, 
                                  opening=opening, opening_xoffset=opening_xoffset, opening_yoffset=opening_yoffset, 
                                  bevel_height=bevel_height, secondHoleDiameter=secondHoleDiameter, secondHoleOffset=secondHoleOffset, thirdHoleDiameter=thirdHoleDiameter, thirdHoleOffset=thirdHoleOffset, fourthHoleDiameter=fourthHoleDiameter, fourthHoleOffset=fourthHoleOffset, 
                                  secondDrillDiameter=secondDrillDiameter,secondDrillOffset=secondDrillOffset,secondDrillPad=secondDrillPad,
                                  nibbleSize=nibbleSize, nibblePos=nibblePos, fabref_offset=fabref_offset,
                                  tags_additional=[], lib_name="${KISYS3DMOD}/"+classname, classname=classname, classname_description=classname_description, webpage=webpage, script_generated_note=script_generated_note)
