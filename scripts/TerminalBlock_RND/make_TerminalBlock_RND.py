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

    script_generated_note="script-generated using https://github.com/pointhi/kicad-footprint-generator/scripts/TerminalBlock_RND";
    classname="TerminalBlock_RND"

    pins=range(2,12+1)
    rm=5
    package_height=10
    leftbottom_offset=[rm/2,package_height-2.3]
    ddrill=1.3
    pad=[2.5,2.5]
    bevel_height=[3.5]
    opening=[4.1,5.4]
    opening_yoffset=package_height-1-opening[1]
    secondHoleDiameter=0
    secondHoleOffset=[0,0]
    thirdHoleDiameter=0
    thirdHoleOffset=[0,0]
    fourthHoleDiameter=0
    fourthHoleOffset=[0,0]
    fabref_offset=[0,3]
    nibbleSize=[]
    nibblePos=[]
    for p in pins:
        makeTerminalBlockVertical(footprint_name="TerminalBlock_RND_205-{0:05}_1x{2:02}_P{1:3.2f}mm_Vertical".format(274+p, rm, p), 
                                  pins=p, rm=rm, 
                                  package_height=package_height, leftbottom_offset=leftbottom_offset, 
                                  ddrill=ddrill, pad=pad, 
                                  opening=opening, opening_yoffset=opening_yoffset, 
                                  bevel_height=bevel_height, secondHoleDiameter=secondHoleDiameter, secondHoleOffset=secondHoleOffset, thirdHoleDiameter=thirdHoleDiameter, thirdHoleOffset=thirdHoleOffset, fourthHoleDiameter=fourthHoleDiameter, fourthHoleOffset=fourthHoleOffset, 
                                  nibbleSize=nibbleSize,nibblePos=nibblePos, fabref_offset=fabref_offset,
                                  tags_additional=[], lib_name="${KISYS3DMOD}/TerminalBlock_RND", classname="TerminalBlock_RND", classname_description="terminal block RND 205-{0:05}".format(76+p), webpage="http://cdn-reichelt.de/documents/datenblatt/C151/RND_205-00276_DB_EN.pdf", script_generated_note=script_generated_note)

    
    pins=range(2,12+1)
    rm=5.08
    package_height=10.6
    leftbottom_offset=[2.54, 5.3]
    ddrill=1.3
    pad=[2.5,2.5]
    screw_diameter=3
    bevel_height=[0.6,2.8,package_height-2]
    slit_screw=True
    screw_pin_offset=[0,0]
    secondHoleDiameter=[2.5,.5]
    secondHoleOffset=[0,-(package_height-leftbottom_offset[1])+secondHoleDiameter[1]]
    thirdHoleDiameter=0
    thirdHoleOffset=[0,0]
    fourthHoleDiameter=0
    fourthHoleOffset=[0,0]
    nibbleSize=[]#[0.6,1.2]
    nibblePos=[]#[-nibbleSize[0],0.25]
    fabref_offset=0
    for p in pins:
        name="205-{0:05}".format(285+p)
        footprint_name="TerminalBlock_RND_{0}_1x{2:02}_P{1:3.2f}mm_Horizontal".format(name, rm, p)
        classname_description="terminal block RND {0}".format(name)
        webpage="http://cdn-reichelt.de/documents/datenblatt/C151/RND_205-00287_DB_EN.pdf"
        makeTerminalBlockStd(footprint_name=footprint_name, 
                                  pins=p, rm=rm, 
                                  package_height=package_height, leftbottom_offset=leftbottom_offset, 
                                  ddrill=ddrill, pad=pad, screw_diameter=screw_diameter, bevel_height=bevel_height, slit_screw=slit_screw, screw_pin_offset=screw_pin_offset, secondHoleDiameter=secondHoleDiameter, secondHoleOffset=secondHoleOffset, thirdHoleDiameter=thirdHoleDiameter, thirdHoleOffset=thirdHoleOffset, fourthHoleDiameter=fourthHoleDiameter, fourthHoleOffset=fourthHoleOffset, 
                                  nibbleSize=nibbleSize, nibblePos=nibblePos, fabref_offset=fabref_offset,
                                  tags_additional=[], lib_name='${KISYS3DMOD}/'+classname, classname=classname, classname_description=classname_description, 
                                  webpage=webpage, script_generated_note=script_generated_note)

                                  
    pins=range(2,12+1)
    rm=5
    package_height=8.1
    leftbottom_offset=[2.5, 4.05]
    ddrill=1.1
    pad=[2.1,2.1]
    screw_diameter=3
    bevel_height=[0.6,1.2,package_height-2]
    slit_screw=True
    screw_pin_offset=[0,0]
    secondHoleDiameter=[2.5,1]
    secondHoleOffset=[0,-(package_height-leftbottom_offset[1])+secondHoleDiameter[1]/2]
    thirdHoleDiameter=0
    thirdHoleOffset=[rm/2,0]
    fourthHoleDiameter=0
    fourthHoleOffset=[rm/2,-(package_height-leftbottom_offset[1])+secondHoleDiameter[1]/2]
    fabref_offset=0
    nibbleSize=[]
    nibblePos=[]
    for p in pins:
        name="205-{0:05}".format(43+p)
        footprint_name="TerminalBlock_RND_{0}_1x{2:02}_P{1:3.2f}mm_Horizontal".format(name, rm, p)
        classname_description="terminal block RND {0}".format(name)
        webpage="http://cdn-reichelt.de/documents/datenblatt/C151/RND_205-00045_DB_EN.pdf"
        makeTerminalBlockStd(footprint_name=footprint_name, 
                                  pins=p, rm=rm, 
                                  package_height=package_height, leftbottom_offset=leftbottom_offset, 
                                  ddrill=ddrill, pad=pad, screw_diameter=screw_diameter, bevel_height=bevel_height, slit_screw=slit_screw, screw_pin_offset=screw_pin_offset, secondHoleDiameter=secondHoleDiameter, secondHoleOffset=secondHoleOffset, thirdHoleDiameter=thirdHoleDiameter, thirdHoleOffset=thirdHoleOffset, fourthHoleDiameter=fourthHoleDiameter, fourthHoleOffset=fourthHoleOffset, 
                                  nibbleSize=nibbleSize, nibblePos=nibblePos, fabref_offset=fabref_offset,
                                  tags_additional=[], lib_name='${KISYS3DMOD}/'+classname, classname=classname, classname_description=classname_description, 
                                  webpage=webpage, script_generated_note=script_generated_note)

    pins=range(2,12+1)
    rm=5
    package_height=12.6
    leftbottom_offset=[rm/2, 6.5]
    ddrill=1.3
    pad=[2.5,2.5]
    screw_diameter=2.2
    bevel_height=[7.7,9.8]
    vsegment_lines_offset=[]
    opening=[3.0,5]
    opening_xoffset=0
    opening_yoffset=2
    opening_elliptic=False
    secondDrillDiameter=0
    secondDrillOffset=[2.5,-5]
    secondDrillPad=pad
    secondHoleDiameter=0
    secondHoleOffset=[0,0]
    thirdHoleDiameter=0
    thirdHoleOffset=[1.25,0]
    fourthHoleDiameter=0
    fourthHoleOffset=[1.25,-5.75]
    fifthHoleDiameter=0
    fifthHoleOffset=[1.25,-0.75]
    secondEllipseSize=[3.2,2.5]
    secondEllipseOffset=[0,-4.7]
    fabref_offset=[0,-1]
    nibbleSize=[]
    nibblePos=[]
    for p in pins:
        name="205-{0:05}".format(54+p)
        footprint_name="TerminalBlock_RND_{0}_1x{2:02}_P{1:3.2f}mm_45Degree".format(name, rm, p)
        classname_description="terminal block RND {0}".format(name)
        webpage="http://cdn-reichelt.de/documents/datenblatt/C151/RND_205-00056_DB_EN.pdf"
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
   
    pins=range(2,12+1)
    rm=10
    package_height=10.3
    leftbottom_offset=[rm/4, 5]
    ddrill=1.3
    pad=[2.5,2.5]
    screw_diameter=3
    bevel_height=[0.6,1.2,package_height-2]
    slit_screw=False
    screw_pin_offset=[0,0]
    secondHoleDiameter=[2.5,1]
    secondHoleOffset=[0,-(package_height-leftbottom_offset[1])+secondHoleDiameter[1]/2]
    thirdHoleDiameter=screw_diameter
    thirdHoleOffset=[rm/2,0]
    fourthHoleDiameter=[2.5,1]
    fourthHoleOffset=[rm/2,-(package_height-leftbottom_offset[1])+secondHoleDiameter[1]/2]
    fabref_offset=[0,3]
    nibbleSize=[]
    nibblePos=[]
    for p in pins:
        name="205-{0:05}".format(76+p)
        footprint_name="TerminalBlock_RND_{0}_1x{2:02}_P{1:3.2f}mm_Horizontal".format(name, rm, p)
        classname_description="terminal block RND {0}".format(name)
        webpage="http://cdn-reichelt.de/documents/datenblatt/C151/RND_205-00078_DB_EN.pdf"
        makeTerminalBlockStd(footprint_name=footprint_name, 
                                  pins=p, rm=rm, 
                                  package_height=package_height, leftbottom_offset=leftbottom_offset, 
                                  ddrill=ddrill, pad=pad, screw_diameter=screw_diameter, bevel_height=bevel_height, slit_screw=slit_screw, screw_pin_offset=screw_pin_offset, secondHoleDiameter=secondHoleDiameter, secondHoleOffset=secondHoleOffset, thirdHoleDiameter=thirdHoleDiameter, thirdHoleOffset=thirdHoleOffset, fourthHoleDiameter=fourthHoleDiameter, fourthHoleOffset=fourthHoleOffset, 
                                  nibbleSize=nibbleSize, nibblePos=nibblePos, fabref_offset=fabref_offset,
                                  tags_additional=[], lib_name='${KISYS3DMOD}/'+classname, classname=classname, classname_description=classname_description, 
                                  webpage=webpage, script_generated_note=script_generated_note)

    
    pins=range(2,12+1)
    rm=7.5
    package_height=10.3
    leftbottom_offset=[rm/2, 5]
    ddrill=1.3
    pad=[2.5,2.5]
    screw_diameter=3
    bevel_height=[0.6,1.2,package_height-2]
    slit_screw=False
    screw_pin_offset=[0,0]
    secondHoleDiameter=[2.5,1]
    secondHoleOffset=[0,-(package_height-leftbottom_offset[1])+secondHoleDiameter[1]/2]
    thirdHoleDiameter=0
    thirdHoleOffset=[rm/2,0]
    fourthHoleDiameter=0
    fourthHoleOffset=[rm/2,-(package_height-leftbottom_offset[1])+secondHoleDiameter[1]/2]
    fabref_offset=[0,3]
    nibbleSize=[]
    nibblePos=[]
    for p in pins:
        name="205-{0:05}".format(65+p)
        footprint_name="TerminalBlock_RND_{0}_1x{2:02}_P{1:3.2f}mm_Horizontal".format(name, rm, p)
        classname_description="terminal block RND {0}".format(name)
        webpage="http://cdn-reichelt.de/documents/datenblatt/C151/RND_205-00067_DB_EN.pdf"
        makeTerminalBlockStd(footprint_name=footprint_name, 
                                  pins=p, rm=rm, 
                                  package_height=package_height, leftbottom_offset=leftbottom_offset, 
                                  ddrill=ddrill, pad=pad, screw_diameter=screw_diameter, bevel_height=bevel_height, slit_screw=slit_screw, screw_pin_offset=screw_pin_offset, secondHoleDiameter=secondHoleDiameter, secondHoleOffset=secondHoleOffset, thirdHoleDiameter=thirdHoleDiameter, thirdHoleOffset=thirdHoleOffset, fourthHoleDiameter=fourthHoleDiameter, fourthHoleOffset=fourthHoleOffset, 
                                  nibbleSize=nibbleSize, nibblePos=nibblePos, fabref_offset=fabref_offset,
                                  tags_additional=[], lib_name='${KISYS3DMOD}/'+classname, classname=classname, classname_description=classname_description, 
                                  webpage=webpage, script_generated_note=script_generated_note)

                                  
    pins=range(2,12+1)
    rm=10
    package_height=8.1
    leftbottom_offset=[2.5, 4.05]
    ddrill=1.3
    pad=[2.5,2.5]
    screw_diameter=3
    bevel_height=[0.6,1.2,package_height-2]
    slit_screw=True
    screw_pin_offset=[0,0]
    secondHoleDiameter=[2.5,1]
    secondHoleOffset=[0,-(package_height-leftbottom_offset[1])+secondHoleDiameter[1]/2]
    thirdHoleDiameter=screw_diameter
    thirdHoleOffset=[rm/2,0]
    fourthHoleDiameter=[2.5,1]
    fourthHoleOffset=[rm/2,-(package_height-leftbottom_offset[1])+secondHoleDiameter[1]/2]
    fabref_offset=0
    nibbleSize=[]
    nibblePos=[]
    for p in pins:
        name="205-{0:05}".format(296+p)
        footprint_name="TerminalBlock_RND_{0}_1x{2:02}_P{1:3.2f}mm_Horizontal".format(name, rm, p)
        classname_description="terminal block RND {0}".format(name)
        webpage="http://cdn-reichelt.de/documents/datenblatt/C151/RND_205-00298_DB_EN.pdf"
        makeTerminalBlockStd(footprint_name=footprint_name, 
                                  pins=p, rm=rm, 
                                  package_height=package_height, leftbottom_offset=leftbottom_offset, 
                                  ddrill=ddrill, pad=pad, screw_diameter=screw_diameter, bevel_height=bevel_height, slit_screw=slit_screw, screw_pin_offset=screw_pin_offset, secondHoleDiameter=secondHoleDiameter, secondHoleOffset=secondHoleOffset, thirdHoleDiameter=thirdHoleDiameter, thirdHoleOffset=thirdHoleOffset, fourthHoleDiameter=fourthHoleDiameter, fourthHoleOffset=fourthHoleOffset, 
                                  nibbleSize=nibbleSize, nibblePos=nibblePos, fabref_offset=fabref_offset,
                                  tags_additional=[], lib_name='${KISYS3DMOD}/'+classname, classname=classname, classname_description=classname_description, 
                                  webpage=webpage, script_generated_note=script_generated_note)
 
    
    pins=range(2,12+1)
    rm=5.08
    package_height=8.45
    leftbottom_offset=[2.54, 4.05]
    ddrill=1.1
    pad=[2.1,2.1]
    screw_diameter=2.5
    bevel_height=[0.5,1.6,package_height-1.85]
    slit_screw=True
    screw_pin_offset=[0,0]
    secondHoleDiameter=[2.5,1]
    secondHoleOffset=[0,-(package_height-leftbottom_offset[1])+secondHoleDiameter[1]/2]
    thirdHoleDiameter=0
    thirdHoleOffset=[0,0]
    fourthHoleDiameter=0
    fourthHoleOffset=[0,0]
    nibbleSize=[]#[0.6,1.2]
    nibblePos=[]#[-nibbleSize[0],0.25]
    fabref_offset=0
    for p in pins:
        name="205-{0:05}".format(230+p)
        footprint_name="TerminalBlock_RND_{0}_1x{2:02}_P{1:3.2f}mm_Horizontal".format(name, rm, p)
        classname_description="terminal block RND {0}".format(name)
        webpage="http://cdn-reichelt.de/documents/datenblatt/C151/RND_205-00232_DB_EN.pdf"
        makeTerminalBlockStd(footprint_name=footprint_name,
                                  pins=p, rm=rm, 
                                  package_height=package_height, leftbottom_offset=leftbottom_offset, 
                                  ddrill=ddrill, pad=pad, screw_diameter=screw_diameter, bevel_height=bevel_height, slit_screw=slit_screw, screw_pin_offset=screw_pin_offset, secondHoleDiameter=secondHoleDiameter, secondHoleOffset=secondHoleOffset, thirdHoleDiameter=thirdHoleDiameter, thirdHoleOffset=thirdHoleOffset, fourthHoleDiameter=fourthHoleDiameter, fourthHoleOffset=fourthHoleOffset, 
                                  nibbleSize=nibbleSize, nibblePos=nibblePos, fabref_offset=fabref_offset,
                                  tags_additional=[], lib_name='${KISYS3DMOD}/'+classname, classname=classname, classname_description=classname_description, 
                                  webpage=webpage, script_generated_note=script_generated_note)
    
    pins=range(2,12+1)
    rm=5
    package_height=7.6
    leftbottom_offset=[2.5, 3.5]
    ddrill=1.3
    pad=[2.5,2.5]
    screw_diameter=3
    bevel_height=[0.6,1.2,package_height-1.7]
    slit_screw=True
    screw_pin_offset=[0,0]
    secondHoleDiameter=1.1
    secondHoleOffset=[0,-3]
    thirdHoleDiameter=0
    thirdHoleOffset=[0,0]
    fourthHoleDiameter=0
    fourthHoleOffset=[0,0]
    nibbleSize=[]#[0.6,1.2]
    nibblePos=[]#[-nibbleSize[0],0.25]
    fabref_offset=0
    for p in pins:
        name="205-{0:05}".format(10+p)
        footprint_name="TerminalBlock_RND_{0}_1x{2:02}_P{1:3.2f}mm_Horizontal".format(name, rm, p)
        classname_description="terminal block RND {0}".format(name)
        webpage="http://cdn-reichelt.de/documents/datenblatt/C151/RND_205-00012_DB_EN.pdf"
        makeTerminalBlockStd(footprint_name=footprint_name, 
                                  pins=p, rm=rm, 
                                  package_height=package_height, leftbottom_offset=leftbottom_offset, 
                                  ddrill=ddrill, pad=pad, screw_diameter=screw_diameter, bevel_height=bevel_height, slit_screw=slit_screw, screw_pin_offset=screw_pin_offset, secondHoleDiameter=secondHoleDiameter, secondHoleOffset=secondHoleOffset, thirdHoleDiameter=thirdHoleDiameter, thirdHoleOffset=thirdHoleOffset, fourthHoleDiameter=fourthHoleDiameter, fourthHoleOffset=fourthHoleOffset, 
                                  nibbleSize=nibbleSize, nibblePos=nibblePos, fabref_offset=fabref_offset,
                                  tags_additional=[], lib_name='${KISYS3DMOD}/'+classname, classname=classname, classname_description=classname_description, 
                                  webpage=webpage, script_generated_note=script_generated_note)

                                  
    pins=range(2,12+1)
    rm=10.16
    package_height=8.3
    leftbottom_offset=[2.54, 4.55]
    ddrill=1.3
    pad=[2.5,2.5]
    screw_diameter=3
    bevel_height=[0.6, 1.2, package_height-1.5]
    slit_screw=True
    screw_pin_offset=[0,0]
    secondHoleDiameter=[2.5,1]
    secondHoleOffset=[0,-(package_height-leftbottom_offset[1])+secondHoleDiameter[1]/2]
    thirdHoleDiameter=screw_diameter
    thirdHoleOffset=[rm/2,0]
    fourthHoleDiameter=secondHoleDiameter
    fourthHoleOffset=[rm/2,secondHoleOffset[1]]
    fabref_offset=0 #[0,2.5]
    nibbleSize=[]
    nibblePos=[]
    for p in pins:
        name="205-{0:05}".format(239+p)
        footprint_name="TerminalBlock_RND_{0}_1x{2:02}_P{1:3.2f}mm_Horizontal".format(name, rm, p)
        classname_description="terminal block RND {0}".format(name)
        webpage="http://cdn-reichelt.de/documents/datenblatt/C151/RND_205-00023_DB_EN.pdf"
        makeTerminalBlockStd(footprint_name=footprint_name, 
                                  pins=p, rm=rm, 
                                  package_height=package_height, leftbottom_offset=leftbottom_offset, 
                                  ddrill=ddrill, pad=pad, screw_diameter=screw_diameter, bevel_height=bevel_height, slit_screw=slit_screw, screw_pin_offset=screw_pin_offset, secondHoleDiameter=secondHoleDiameter, secondHoleOffset=secondHoleOffset, thirdHoleDiameter=thirdHoleDiameter, thirdHoleOffset=thirdHoleOffset, fourthHoleDiameter=fourthHoleDiameter, fourthHoleOffset=fourthHoleOffset, 
                                  nibbleSize=nibbleSize, nibblePos=nibblePos, fabref_offset=fabref_offset,
                                  tags_additional=[], lib_name='${KISYS3DMOD}/'+classname, classname=classname, classname_description=classname_description, 
                                  webpage=webpage, script_generated_note=script_generated_note)

    pins=range(2,12+1)
    rm=5
    package_height=9
    leftbottom_offset=[2.5, 4]
    ddrill=1.3
    pad=[2.5,2.5]
    screw_diameter=3
    bevel_height=[1.5]
    slit_screw=True
    screw_pin_offset=[0,0]
    secondHoleDiameter=1.8
    secondHoleOffset=[0,-3]
    thirdHoleDiameter=0
    thirdHoleOffset=[0,0]
    fourthHoleDiameter=0
    fourthHoleOffset=[0,0]
    fabref_offset=0 #[0,3.8]
    nibbleSize=[]
    nibblePos=[]
    for p in pins:
        name="205-{0:05}".format(p-1)
        footprint_name="TerminalBlock_RND_{0}_1x{2:02}_P{1:3.2f}mm_Horizontal".format(name, rm, p)
        classname_description="terminal block RND {0}".format(name)
        webpage="http://cdn-reichelt.de/documents/datenblatt/C151/RND_205-00001_DB_EN.pdf"
        makeTerminalBlockStd(footprint_name=footprint_name, 
                                  pins=p, rm=rm, 
                                  package_height=package_height, leftbottom_offset=leftbottom_offset, 
                                  ddrill=ddrill, pad=pad, screw_diameter=screw_diameter, bevel_height=bevel_height, slit_screw=slit_screw, screw_pin_offset=screw_pin_offset, secondHoleDiameter=secondHoleDiameter, secondHoleOffset=secondHoleOffset, thirdHoleDiameter=thirdHoleDiameter, thirdHoleOffset=thirdHoleOffset, fourthHoleDiameter=fourthHoleDiameter, fourthHoleOffset=fourthHoleOffset, 
                                  nibbleSize=nibbleSize, nibblePos=nibblePos, fabref_offset=fabref_offset,
                                  tags_additional=[], lib_name='${KISYS3DMOD}/'+classname, classname=classname, classname_description=classname_description, 
                                  webpage=webpage, script_generated_note=script_generated_note)

                                  
    pins=range(2,12+1)
    rm=10
    package_height=9
    leftbottom_offset=[2.5, 4]
    ddrill=1.3
    pad=[2.5,2.5]
    screw_diameter=3
    bevel_height=[1.5]
    slit_screw=True
    screw_pin_offset=[0,0]
    secondHoleDiameter=1.8
    secondHoleOffset=[0,-3]
    thirdHoleDiameter=screw_diameter
    thirdHoleOffset=[rm/2,0]
    fourthHoleDiameter=1.8
    fourthHoleOffset=[rm/2,-3]
    fabref_offset=[0,3.8]
    nibbleSize=[]
    nibblePos=[]
    for p in pins:
        name="205-{0:05}".format(21+p)
        footprint_name="TerminalBlock_RND_{0}_1x{2:02}_P{1:3.2f}mm_Horizontal".format(name, rm, p)
        classname_description="terminal block RND {0}".format(name)
        webpage="http://cdn-reichelt.de/documents/datenblatt/C151/RND_205-00023_DB_EN.pdf"
        makeTerminalBlockStd(footprint_name=footprint_name, 
                                  pins=p, rm=rm, 
                                  package_height=package_height, leftbottom_offset=leftbottom_offset, 
                                  ddrill=ddrill, pad=pad, screw_diameter=screw_diameter, bevel_height=bevel_height, slit_screw=slit_screw, screw_pin_offset=screw_pin_offset, secondHoleDiameter=secondHoleDiameter, secondHoleOffset=secondHoleOffset, thirdHoleDiameter=thirdHoleDiameter, thirdHoleOffset=thirdHoleOffset, fourthHoleDiameter=fourthHoleDiameter, fourthHoleOffset=fourthHoleOffset, 
                                  nibbleSize=nibbleSize, nibblePos=nibblePos, fabref_offset=fabref_offset,
                                  tags_additional=[], lib_name='${KISYS3DMOD}/'+classname, classname=classname, classname_description=classname_description, 
                                  webpage=webpage, script_generated_note=script_generated_note)
