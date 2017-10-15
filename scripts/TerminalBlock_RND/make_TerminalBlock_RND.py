#!/usr/bin/env python

import sys
import os
import math

# ensure that the kicad-footprint-generator directory is available
#sys.path.append(os.environ.get('KIFOOTPRINTGENERATOR'))  # enable package import from parent directory
#sys.path.append("D:\hardware\KiCAD\kicad-footprint-generator")	 # enable package import from parent directory
sys.path.append(os.path.join(sys.path[0],"..","..","kicad_mod")) # load kicad_mod path
sys.path.append(os.path.join(sys.path[0],"..","..")) # load kicad_mod path
sys.path.append(os.path.join(sys.path[0],"..","tools")) # load kicad_mod path

from KicadModTree import *	# NOQA
from footprint_scripts_terminal_blocks import *





if __name__ == '__main__':

	pins=range(2,12+1)
	rm=10
	package_height=10.3
	leftbottom_offset=[rm/4, 5]
	ddrill=1.4
	pad=[2.6,2.6]
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
		makeTerminalBlockStd("TerminalBlock_RND_205-{0:05}_Pitch{1:3.2f}mm".format(76+p, rm), p, rm, package_height, leftbottom_offset, ddrill, pad, screw_diameter, bevel_height, slit_screw, screw_pin_offset, secondHoleDiameter, secondHoleOffset, thirdHoleDiameter, thirdHoleOffset, fourthHoleDiameter, fourthHoleOffset, nibbleSize,nibblePos, fabref_offset,
						tags_additional=[], lib_name="${{KISYS3DMOD}}/TerminalBlock_RND", classname="TerminalBlock_RND", classname_description="terminal block RND 205-{0:05}, see http://cdn-reichelt.de/documents/datenblatt/C151/RND_205-00078_DB_EN.pdf".format(76+p))
	
	pins=range(2,12+1)
	rm=7.5
	package_height=10.3
	leftbottom_offset=[rm/2, 5]
	ddrill=1.4
	pad=[2.6,2.6]
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
		makeTerminalBlockStd("TerminalBlock_RND_205-{0:05}_Pitch{1:3.2f}mm".format(65+p, rm), p, rm, package_height, leftbottom_offset, ddrill, pad, screw_diameter, bevel_height, slit_screw, screw_pin_offset, secondHoleDiameter, secondHoleOffset, thirdHoleDiameter, thirdHoleOffset, fourthHoleDiameter, fourthHoleOffset, nibbleSize,nibblePos, fabref_offset,
						tags_additional=[], lib_name="${{KISYS3DMOD}}/TerminalBlock_RND", classname="TerminalBlock_RND", classname_description="terminal block RND 205-{0:05}, see http://cdn-reichelt.de/documents/datenblatt/C151/RND_205-00067_DB_EN.pdf".format(65+p))

	pins=range(2,12+1)
	rm=5
	package_height=8.1
	leftbottom_offset=[2.5, 4.05]
	ddrill=1.4
	pad=[2.6,2.6]
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
		makeTerminalBlockStd("TerminalBlock_RND_205-{0:05}_Pitch{1:3.2f}mm".format(43+p, rm), p, rm, package_height, leftbottom_offset, ddrill, pad, screw_diameter, bevel_height, slit_screw, screw_pin_offset, secondHoleDiameter, secondHoleOffset, thirdHoleDiameter, thirdHoleOffset, fourthHoleDiameter, fourthHoleOffset, nibbleSize,nibblePos, fabref_offset,
						tags_additional=[], lib_name="${{KISYS3DMOD}}/TerminalBlock_RND", classname="TerminalBlock_RND", classname_description="terminal block RND 205-{0:05}, see http://cdn-reichelt.de/documents/datenblatt/C151/RND_205-00045_DB_EN.pdf".format(43+p))

	pins=range(2,12+1)
	rm=10
	package_height=8.1
	leftbottom_offset=[2.5, 4.05]
	ddrill=1.4
	pad=[2.6,2.6]
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
		makeTerminalBlockStd("TerminalBlock_RND_205-{0:05}_Pitch{1:3.2f}mm".format(296+p, rm), p, rm, package_height, leftbottom_offset, ddrill, pad, screw_diameter, bevel_height, slit_screw, screw_pin_offset, secondHoleDiameter, secondHoleOffset, thirdHoleDiameter, thirdHoleOffset, fourthHoleDiameter, fourthHoleOffset, nibbleSize,nibblePos, fabref_offset,
						tags_additional=[], lib_name="${{KISYS3DMOD}}/TerminalBlock_RND", classname="TerminalBlock_RND", classname_description="terminal block RND 205-{0:05}, see http://cdn-reichelt.de/documents/datenblatt/C151/RND_205-00298_DB_EN.pdf".format(296+p))

	
	pins=range(2,12+1)
	rm=5.08
	package_height=10.16
	leftbottom_offset=[2.54, 5.3]
	ddrill=1.6
	pad=[3,3]
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
		makeTerminalBlockStd("TerminalBlock_RND_205-{0:05}_Pitch{1:3.2f}mm".format(p+285, rm), p, rm, package_height, leftbottom_offset, ddrill, pad, screw_diameter, bevel_height, slit_screw, screw_pin_offset, secondHoleDiameter, secondHoleOffset, thirdHoleDiameter, thirdHoleOffset, fourthHoleDiameter, fourthHoleOffset,nibbleSize,nibblePos, fabref_offset,
						tags_additional=[], lib_name="${{KISYS3DMOD}}/TerminalBlock_RND", classname="TerminalBlock_RND", classname_description="terminal block RND 205-{0:05}, http://cdn-reichelt.de/documents/datenblatt/C151/RND_205-00287_DB_EN.pdf".format(p+285))

	
	pins=range(2,12+1)
	rm=5.08
	package_height=8.45
	leftbottom_offset=[2.54, 4.05]
	ddrill=1.3
	pad=[2.5,2.5]
	screw_diameter=3
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
		makeTerminalBlockStd("TerminalBlock_RND_205-{0:05}_Pitch{1:3.2f}mm".format(p+230, rm), p, rm, package_height, leftbottom_offset, ddrill, pad, screw_diameter, bevel_height, slit_screw, screw_pin_offset, secondHoleDiameter, secondHoleOffset, thirdHoleDiameter, thirdHoleOffset, fourthHoleDiameter, fourthHoleOffset,nibbleSize,nibblePos, fabref_offset,
						tags_additional=[], lib_name="${{KISYS3DMOD}}/TerminalBlock_RND", classname="TerminalBlock_RND", classname_description="terminal block RND 205-{0:05}, http://cdn-reichelt.de/documents/datenblatt/C151/RND_205-00232_DB_EN.pdf".format(p+230))
	
	pins=range(2,12+1)
	rm=5
	package_height=7.6
	leftbottom_offset=[2.5, 3.5]
	ddrill=1.2
	pad=[2.3,2.3]
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
		makeTerminalBlockStd("TerminalBlock_RND_205-{0:05}_Pitch{1:3.2f}mm".format(p+10, rm), p, rm, package_height, leftbottom_offset, ddrill, pad, screw_diameter, bevel_height, slit_screw, screw_pin_offset, secondHoleDiameter, secondHoleOffset, thirdHoleDiameter, thirdHoleOffset, fourthHoleDiameter, fourthHoleOffset,nibbleSize,nibblePos, fabref_offset,
						tags_additional=[], lib_name="${{KISYS3DMOD}}/TerminalBlock_RND", classname="TerminalBlock_RND", classname_description="terminal block RND 205-{0:05}, see http://cdn-reichelt.de/documents/datenblatt/C151/RND_205-00012_DB_EN.pdf".format(p+10))

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
		makeTerminalBlockStd("TerminalBlock_RND_205-{0:05}_Pitch{1:3.2f}mm".format(239+p, rm), p, rm, package_height, leftbottom_offset, ddrill, pad, screw_diameter, bevel_height, slit_screw, screw_pin_offset, secondHoleDiameter, secondHoleOffset, thirdHoleDiameter, thirdHoleOffset, fourthHoleDiameter, fourthHoleOffset, nibbleSize,nibblePos, fabref_offset,
						tags_additional=[], lib_name="${{KISYS3DMOD}}/TerminalBlock_RND", classname="TerminalBlock_RND", classname_description="terminal block RND 205-{0:05}, see http://cdn-reichelt.de/documents/datenblatt/C151/RND_205-00023_DB_EN.pdf".format(239+p))

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
		makeTerminalBlockStd("TerminalBlock_RND_205-{0:05}_Pitch{1:3.2f}mm".format(p-1, rm), p, rm, package_height, leftbottom_offset, ddrill, pad, screw_diameter, bevel_height, slit_screw, screw_pin_offset, secondHoleDiameter, secondHoleOffset, thirdHoleDiameter, thirdHoleOffset, fourthHoleDiameter, fourthHoleOffset, nibbleSize,nibblePos, fabref_offset,
						tags_additional=[], lib_name="${{KISYS3DMOD}}/TerminalBlock_RND", classname="TerminalBlock_RND", classname_description="terminal block RND 205-{0:05}, see http://cdn-reichelt.de/documents/datenblatt/C151/RND_205-00001_DB_EN.pdf".format(p-1))

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
		makeTerminalBlockStd("TerminalBlock_RND_205-{0:05}_Pitch{1:3.2f}mm".format(21+p, rm), p, rm, package_height, leftbottom_offset, ddrill, pad, screw_diameter, bevel_height, slit_screw, screw_pin_offset, secondHoleDiameter, secondHoleOffset, thirdHoleDiameter, thirdHoleOffset, fourthHoleDiameter, fourthHoleOffset, nibbleSize,nibblePos, fabref_offset,
						tags_additional=[], lib_name="${{KISYS3DMOD}}/TerminalBlock_RND", classname="TerminalBlock_RND", classname_description="terminal block RND 205-{0:05}, see http://cdn-reichelt.de/documents/datenblatt/C151/RND_205-00023_DB_EN.pdf".format(21+p))
