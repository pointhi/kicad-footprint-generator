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
from footprint_scripts_dsub import *  # NOQA




if __name__ == '__main__':

	highDensity=False
	rmx=2.77
	rmy=2.84
	pindrill=1.1
	pad=1.8
	mountingdrill=3.1
	mountingpad=[4,4]
	mountingdistance=24.99
	outline_size=0
	outline_cornerradius=0
	connwidth=0
	connwidthsmall=0
	connheight=0
	conn_cornerradius=0
	tags_additional=[]
	lib_name="${{KISYS3DMOD}}/Connectors_DSub"
	classname="DSub"
	classname_description="D-Sub connector"
	webpage=""
	for pins in [9,15,19,23,25,37]:
		isMale=True
		makeDSubStraight(pins, isMale, highDensity, rmx, rmy, pindrill, pad, mountingdrill, mountingpad, mountingdistance, outline_size, outline_cornerradius, connwidth, connwidthsmall, connheight, conn_cornerradius, tags_additional, lib_name, classname, classname_description, webpage)
		isMale=False
		makeDSubStraight(pins, isMale, highDensity, rmx, rmy, pindrill, pad, mountingdrill, mountingpad, mountingdistance, outline_size, outline_cornerradius, connwidth, connwidthsmall, connheight, conn_cornerradius, tags_additional, lib_name, classname, classname_description, webpage)
