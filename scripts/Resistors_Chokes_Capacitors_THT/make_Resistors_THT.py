#!/usr/bin/env python

import sys
import os
import math

# ensure that the kicad-footprint-generator directory is available
#sys.path.append(os.environ.get('KIFOOTPRINTGENERATOR'))  # enable package import from parent directory
#sys.path.append("D:\hardware\KiCAD\kicad-footprint-generator")  # enable package import from parent directory
sys.path.append(os.path.join(sys.path[0],"..","..","kicad_mod")) # load kicad_mod path
sys.path.append(os.path.join(sys.path[0],"..","..")) # load kicad_mod path

from KicadModTree import *  # NOQA
from resistor_tools import *
from footprint_scripts import *









if __name__ == '__main__':
    # standard resistors: http://cdn-reichelt.de/documents/datenblatt/B400/1_4W%23YAG.pdf
    type = "cyl"
    script3d="res_axial_cyl_hor.py"
    with open(script3d, "w") as myfile:
        myfile.write("#\n# SCRIPT to generate 3D models\n#\n\n")
    script3dv="res_axial_cyl_ver.py"
    with open(script3dv, "w") as myfile:
        myfile.write("#\n# SCRIPT to generate 3D models\n#\n\n")

    d2=0
    seriesname = "Axial_DIN0204"; w=3.6; d=1.6; ddrill=0.7; R_POW=1/6; add_description="http://cdn-reichelt.de/documents/datenblatt/B400/1_4W%23YAG.pdf"; name_additions=[]
    for rm in [5.08, 7.62]:
        makeResistorAxialHorizontal(seriesname=seriesname, rm=rm, rmdisp=rm, w=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type,d2=d2,  x_3d=[0,0,0], s_3d=[1/2.54,1/2.54,1/2.54], has3d=1, specialfpname="", add_description=add_description, name_additions=name_additions, specialtags=[],script3d=script3d)
    for rm in [1.9,2.54, 5.08]:
        makeResistorAxialVertical(seriesname=seriesname, rm=rm, rmdisp=rm, l=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type, d2=d2, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", largepadsx=0, largepadsy=0, add_description=add_description, name_additions=name_additions, specialtags=[],script3d=script3dv)

    seriesname = "Axial_DIN0207"; w = 6.3; d = 2.5; ddrill = 0.8; R_POW = 1 / 4; add_description="http://cdn-reichelt.de/documents/datenblatt/B400/1_4W%23YAG.pdf"; name_additions=[]
    for rm in [7.62, 10.16, 15.24]:
        makeResistorAxialHorizontal(seriesname=seriesname, rm=rm, rmdisp=rm, w=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type, d2=d2, x_3d=[0,0,0], s_3d=[1/2.54,1/2.54,1/2.54], has3d=1, specialfpname="", add_description=add_description, name_additions=name_additions, specialtags=[],script3d=script3d)
    for rm in [2.54, 5.08]:
        makeResistorAxialVertical(seriesname=seriesname, rm=rm, rmdisp=rm, l=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type, d2=d2, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", largepadsx=0, largepadsy=0, add_description=add_description, name_additions=name_additions, specialtags=[],script3d=script3dv)

    seriesname="Axial_DIN0309"; w = 9; d = 3.2; ddrill = 0.8; R_POW = 1 / 2; add_description="http://cdn-reichelt.de/documents/datenblatt/B400/1_4W%23YAG.pdf"; name_additions=[]
    for rm in [12.7, 15.24, 20.32, 25.4]:
        makeResistorAxialHorizontal(seriesname=seriesname, rm=rm, rmdisp=rm, w=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type, d2=d2, x_3d=[0,0,0], s_3d=[1/2.54,1/2.54,1/2.54], has3d=1, specialfpname="", add_description=add_description, name_additions=name_additions, specialtags=[],script3d=script3d)
    for rm in [2.54, 5.08]:
        makeResistorAxialVertical(seriesname=seriesname, rm=rm, rmdisp=rm, l=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type, d2=d2, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", largepadsx=0, largepadsy=0, add_description=add_description, name_additions=name_additions, specialtags=[],script3d=script3dv)

    seriesname = "Axial_DIN0411"; w = 9.9; d = 3.6; ddrill = 1.2; R_POW = 1; add_description=""; name_additions=[]
    for rm in [12.7,15.24, 20.32, 25.4]:
        makeResistorAxialHorizontal(seriesname=seriesname, rm=rm, rmdisp=rm, w=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type, d2=d2, x_3d=[0,0,0], s_3d=[1/2.54,1/2.54,1/2.54], has3d=1, specialfpname="", add_description=add_description, name_additions=name_additions, specialtags=[],script3d=script3d)
    for rm in [5.08,7.62]:
        makeResistorAxialVertical(seriesname=seriesname, rm=rm, rmdisp=rm, l=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type, d2=d2, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", largepadsx=0, largepadsy=0, add_description=add_description, name_additions=name_additions, specialtags=[],script3d=script3dv)

    seriesname = "Axial_DIN0414"; w = 11.9; d = 4.5; ddrill = 1.2; R_POW = 2; add_description="http://www.vishay.com/docs/20128/wkxwrx.pdf"; name_additions=[]
    for rm in [15.24, 20.32, 25.4]:
        makeResistorAxialHorizontal(seriesname=seriesname, rm=rm, rmdisp=rm, w=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type, d2=d2, x_3d=[0,0,0], s_3d=[1/2.54,1/2.54,1/2.54], has3d=1, specialfpname="", add_description=add_description, name_additions=name_additions, specialtags=[],script3d=script3d)
    for rm in [5.08,7.62]:
        makeResistorAxialVertical(seriesname=seriesname, rm=rm, rmdisp=rm, l=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type, d2=d2, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", largepadsx=0, largepadsy=0, add_description=add_description, name_additions=name_additions, specialtags=[],script3d=script3dv)

    seriesname = "Axial_DIN0516"; w = 15.5; d = 5; ddrill = 1.2; R_POW = 2; add_description="http://cdn-reichelt.de/documents/datenblatt/B400/1_4W%23YAG.pdf"; name_additions=[]
    for rm in [20.32, 25.4, 30.48]:
        makeResistorAxialHorizontal(seriesname=seriesname, rm=rm, rmdisp=rm, w=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type, d2=d2, x_3d=[0,0,0], s_3d=[1/2.54,1/2.54,1/2.54], has3d=1, specialfpname="", add_description=add_description, name_additions=name_additions, specialtags=[],script3d=script3d)
    for rm in [5.08, 7.62]:
        makeResistorAxialVertical(seriesname=seriesname, rm=rm, rmdisp=rm, l=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type, d2=d2, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", largepadsx=0, largepadsy=0, add_description=add_description, name_additions=name_additions, specialtags=[],script3d=script3dv)

    seriesname = "Axial_DIN0614"; w = 14.3; d = 5.7; ddrill = 1.4; R_POW = 1.5; add_description=""
    for rm in [15.24, 20.32, 25.4]:
        makeResistorAxialHorizontal(seriesname=seriesname, rm=rm, rmdisp=rm, w=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type, d2=d2, x_3d=[0,0,0], s_3d=[1/2.54,1/2.54,1/2.54], has3d=1, specialfpname="", add_description=add_description, name_additions=name_additions, specialtags=[],script3d=script3d)
    for rm in [5.08,7.62]:
        makeResistorAxialVertical(seriesname=seriesname, rm=rm, rmdisp=rm, l=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type, d2=d2, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", largepadsx=0, largepadsy=0, add_description=add_description, name_additions=name_additions, specialtags=[],script3d=script3dv)


    seriesname = "Axial_DIN0617"; w = 17; d = 6; ddrill = 1.2; R_POW = 2; add_description="http://www.vishay.com/docs/20128/wkxwrx.pdf"; name_additions=[]
    for rm in [20.32, 25.4, 30.48]:
        makeResistorAxialHorizontal(seriesname=seriesname, rm=rm, rmdisp=rm, w=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type, d2=d2, x_3d=[0,0,0], s_3d=[1/2.54,1/2.54,1/2.54], has3d=1, specialfpname="", add_description=add_description, name_additions=name_additions, specialtags=[],script3d=script3d)
    for rm in [5.08, 7.62]:
        makeResistorAxialVertical(seriesname=seriesname, rm=rm, rmdisp=rm, l=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type, d2=d2, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", largepadsx=0, largepadsy=0, add_description=add_description, name_additions=name_additions, specialtags=[],script3d=script3dv)


    seriesname = "Axial_DIN0918"; w = 18; d = 9; ddrill = 1.2; R_POW = 4; add_description=""
    for rm in [22.86, 25.4, 30.48]:
        makeResistorAxialHorizontal(seriesname=seriesname, rm=rm, rmdisp=rm, w=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type, d2=d2, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", add_description=add_description, name_additions=name_additions, specialtags=[],script3d=script3d)
    for rm in [7.62]:
        makeResistorAxialVertical(seriesname=seriesname, rm=rm, rmdisp=rm, l=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type, d2=d2, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", largepadsx=0, largepadsy=0, add_description=add_description, name_additions=name_additions, specialtags=[],script3d=script3dv)

    seriesname = "Axial_DIN0922"; w = 20; d = 9; ddrill = 1.2; R_POW = 5; add_description="http://www.vishay.com/docs/20128/wkxwrx.pdf"; name_additions=[]
    for rm in [25.4, 30.48]:
        makeResistorAxialHorizontal(seriesname=seriesname, rm=rm, rmdisp=rm, w=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type, d2=d2, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", add_description=add_description, name_additions=name_additions, specialtags=[],script3d=script3d)
    for rm in [7.62]:
        makeResistorAxialVertical(seriesname=seriesname, rm=rm, rmdisp=rm, l=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type, d2=d2, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", largepadsx=0, largepadsy=0, add_description=add_description, name_additions=name_additions, specialtags=[],script3d=script3dv)

		


    # POWER Resistors (rectangular)
    script3d = "res_axial_box_hor.py"
    with open(script3d, "w") as myfile:
        myfile.write("#\n# SCRIPT to generate 3D models\n#\n\n")
    script3dv = "res_axial_box_ver.py"
    with open(script3dv, "w") as myfile:
        myfile.write("#\n# SCRIPT to generate 3D models\n#\n\n")
    type = "box"
    seriesname = "Axial_Power"; w=20; d=6.4; d2=6.4; ddrill=1.2; R_POW=4; add_description="http://cdn-reichelt.de/documents/datenblatt/B400/5WAXIAL_9WAXIAL_11WAXIAL_17WAXIAL%23YAG.pdf"; name_additions=[]
    for rm in [22.4, 25.4, 30.48]:
        makeResistorAxialHorizontal(seriesname=seriesname, rm=rm, rmdisp=rm, w=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type,d2=d2,  x_3d=[0,0,0], s_3d=[1/2.54,1/2.54,1/2.54], has3d=1, specialfpname="", add_description=add_description, name_additions=name_additions, specialtags=[],script3d=script3d)
    for rm in [5.08,7.62]:
        makeResistorAxialVertical(seriesname=seriesname, rm=rm, rmdisp=rm, l=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type, d2=d2, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", largepadsx=0, largepadsy=0, add_description=add_description, name_additions=name_additions, specialtags=[],script3d=script3dv)

    seriesname = "Axial_Power"; w=25; d=6.4; d2=6.4; ddrill=1.2; R_POW=5; name_additions=[]
    for rm in [27.94,30.48]:
        makeResistorAxialHorizontal(seriesname=seriesname, rm=rm, rmdisp=rm, w=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type,d2=d2,  x_3d=[0,0,0], s_3d=[1/2.54,1/2.54,1/2.54], has3d=1, specialfpname="", add_description=add_description, name_additions=name_additions, specialtags=[],script3d=script3d)

    seriesname = "Axial_Power"; w=38; d=6.4; d2=6.4; ddrill=1.2; R_POW=7; name_additions=[]
    for rm in [40.64,45.72]:
        makeResistorAxialHorizontal(seriesname=seriesname, rm=rm, rmdisp=rm, w=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type,d2=d2,  x_3d=[0,0,0], s_3d=[1/2.54,1/2.54,1/2.54], has3d=1, specialfpname="", add_description=add_description, name_additions=name_additions, specialtags=[],script3d=script3d)

    seriesname = "Axial_Power"; w=25; d=9; d2=9; ddrill=1.2; R_POW=7; name_additions=[]
    for rm in [27.94,30.48]:
        makeResistorAxialHorizontal(seriesname=seriesname, rm=rm, rmdisp=rm, w=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type,d2=d2,  x_3d=[0,0,0], s_3d=[1/2.54,1/2.54,1/2.54], has3d=1, specialfpname="", add_description=add_description, name_additions=name_additions, specialtags=[],script3d=script3d)
    for rm in [7.62,10.16]:
        makeResistorAxialVertical(seriesname=seriesname, rm=rm, rmdisp=rm, l=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type, d2=d2, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", largepadsx=0, largepadsy=0, add_description=add_description, name_additions=name_additions, specialtags=[],script3d=script3dv)

    seriesname = "Axial_Power"; w=38; d=9; d2=9; ddrill=1.2; R_POW=9; name_additions=[]
    for rm in [40.64,45.72]:
        makeResistorAxialHorizontal(seriesname=seriesname, rm=rm, rmdisp=rm, w=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type,d2=d2,  x_3d=[0,0,0], s_3d=[1/2.54,1/2.54,1/2.54], has3d=1, specialfpname="", add_description=add_description, name_additions=name_additions, specialtags=[],script3d=script3d)

    seriesname = "Axial_Power"; w=50; d=9; d2=9; ddrill=1.2; R_POW=11; name_additions=[]
    for rm in [55.88,60.96]:
        makeResistorAxialHorizontal(seriesname=seriesname, rm=rm, rmdisp=rm, w=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type,d2=d2,  x_3d=[0,0,0], s_3d=[1/2.54,1/2.54,1/2.54], has3d=1, specialfpname="", add_description=add_description, name_additions=name_additions, specialtags=[],script3d=script3d)

    seriesname = "Axial_Power"; w=75; d=9; d2=9; ddrill=1.2; R_POW=17; name_additions=[]
    for rm in [81.28,86.36]:
        makeResistorAxialHorizontal(seriesname=seriesname, rm=rm, rmdisp=rm, w=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type,d2=d2,  x_3d=[0,0,0], s_3d=[1/2.54,1/2.54,1/2.54], has3d=1, specialfpname="", add_description=add_description, name_additions=name_additions, specialtags=[],script3d=script3d)

    seriesname = "Axial_Power"; w=48; d=12.5; d2=12.5; ddrill=1.2; R_POW=15; name_additions=[]
    for rm in [55.88,60.96]:
        makeResistorAxialHorizontal(seriesname=seriesname, rm=rm, rmdisp=rm, w=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type,d2=d2,  x_3d=[0,0,0], s_3d=[1/2.54,1/2.54,1/2.54], has3d=1, specialfpname="", add_description=add_description, name_additions=name_additions, specialtags=[],script3d=script3d)
    for rm in [7.62,10.16]:
        makeResistorAxialVertical(seriesname=seriesname, rm=rm, rmdisp=rm, l=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type, d2=d2, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", largepadsx=0, largepadsy=0, add_description=add_description, name_additions=name_additions, specialtags=[],script3d=script3dv)

    seriesname = "Axial_Power"; w=60; d=14; d2=14; ddrill=1.2; R_POW=25; name_additions=[]
    for rm in [66.04,71.12]:
        makeResistorAxialHorizontal(seriesname=seriesname, rm=rm, rmdisp=rm, w=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type,d2=d2,  x_3d=[0,0,0], s_3d=[1/2.54,1/2.54,1/2.54], has3d=1, specialfpname="", add_description=add_description, name_additions=name_additions, specialtags=[],script3d=script3d)
    for rm in [10.16]:
        makeResistorAxialVertical(seriesname=seriesname, rm=rm, rmdisp=rm, l=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type, d2=d2, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", largepadsx=0, largepadsy=0, add_description=add_description, name_additions=name_additions, specialtags=[],script3d=script3dv)

    # shunt resistor with additional pins
    type = "box"
    seriesname = "Axial_Shunt";  ddrill=1.5; add_description="http://www.vishay.com/docs/30217/cpsl.pdf"; name_additions=[]
    rm = 25.4; shuntPinsRM=14.3; w=22.2; d=8; d2=d; R_POW=3
    makeResistorAxialHorizontal(seriesname=seriesname, rm=rm, rmdisp=rm, w=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type,d2=d2, hasShuntPins=True, shuntPinsRM=shuntPinsRM,  x_3d=[0,0,0], s_3d=[1/2.54,1/2.54,1/2.54], has3d=1, specialfpname="", add_description=add_description, name_additions=name_additions, specialtags=[])
    rm = 25.4; shuntPinsRM=14.3; w=22.2; d=9.5; d2=d; R_POW=5
    makeResistorAxialHorizontal(seriesname=seriesname, rm=rm, rmdisp=rm, w=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type,d2=d2, hasShuntPins=True, shuntPinsRM=shuntPinsRM,  x_3d=[0,0,0], s_3d=[1/2.54,1/2.54,1/2.54], has3d=1, specialfpname="", add_description=add_description, name_additions=name_additions, specialtags=[])
    rm = 38.1; shuntPinsRM=25.4; w=35.3; d=9.5; d2=d; R_POW=7
    makeResistorAxialHorizontal(seriesname=seriesname, rm=rm, rmdisp=rm, w=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type,d2=d2, hasShuntPins=True, shuntPinsRM=shuntPinsRM,  x_3d=[0,0,0], s_3d=[1/2.54,1/2.54,1/2.54], has3d=1, specialfpname="", add_description=add_description, name_additions=name_additions, specialtags=[])
    rm = 50.8; shuntPinsRM=34.93; w=47.6; d=9.5; d2=d; R_POW=10
    makeResistorAxialHorizontal(seriesname=seriesname, rm=rm, rmdisp=rm, w=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type,d2=d2, hasShuntPins=True, shuntPinsRM=shuntPinsRM,  x_3d=[0,0,0], s_3d=[1/2.54,1/2.54,1/2.54], has3d=1, specialfpname="", add_description=add_description, name_additions=name_additions, specialtags=[])
    rm = 50.8; shuntPinsRM=34.93; w=47.6; d=12.7; d2=d; R_POW=15
    makeResistorAxialHorizontal(seriesname=seriesname, rm=rm, rmdisp=rm, w=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type,d2=d2, hasShuntPins=True, shuntPinsRM=shuntPinsRM,  x_3d=[0,0,0], s_3d=[1/2.54,1/2.54,1/2.54], has3d=1, specialfpname="", add_description=add_description, name_additions=name_additions, specialtags=[])

    # wire bridge/bare metal resistor elements
    type = "bridge"
    seriesname = "Bare_Metal_Element"; d=4.8; d2=2; ddrill=1.5; add_description="https://www.bourns.com/pdfs/PWR4412-2S.pdf"; name_additions=[]
    rm = 11.4; w=rm+1; R_POW=1
    makeResistorAxialHorizontal(seriesname=seriesname, rm=rm, rmdisp=rm, w=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type,d2=d2,  x_3d=[0,0,0], s_3d=[1/2.54,1/2.54,1/2.54], has3d=1, specialfpname="", add_description=add_description, name_additions=name_additions, specialtags=[])
    rm = 15.3; w=rm+1; R_POW=3
    makeResistorAxialHorizontal(seriesname=seriesname, rm=rm, rmdisp=rm, w=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type,d2=d2,  x_3d=[0,0,0], s_3d=[1/2.54,1/2.54,1/2.54], has3d=1, specialfpname="", add_description=add_description, name_additions=name_additions, specialtags=[])
    rm = 20.3; w=rm+1; R_POW=5
    makeResistorAxialHorizontal(seriesname=seriesname, rm=rm, rmdisp=rm, w=w, d=d, ddrill=ddrill, R_POW=R_POW, type=type,d2=d2,  x_3d=[0,0,0], s_3d=[1/2.54,1/2.54,1/2.54], has3d=1, specialfpname="", add_description=add_description, name_additions=name_additions, specialtags=[])
    
    # radial resistors, 45° wires
    rm2=0; w2=0
    type = "simple45"; seriesname = "Radial_Power"; add_description = "http://www.vitrohm.com/content/files/vitrohm_series_kv_-_201601.pdf"; name_additions=[]
    w = 7; h = 8; ddrill = 1.2; rm=2.4; rm2=2.3; R_POW=7
    makeResistorRadial(seriesname=seriesname, rm=rm, w=w, h=h, ddrill=ddrill, R_POW=R_POW, rm2=rm2, vlines=False, w2=w2, type=type, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", name_additions=name_additions, specialtags=[], add_description=add_description)
    w = 9; h = 10; ddrill = 1.2; rm=2.7; rm2=2.3; R_POW=17
    makeResistorRadial(seriesname=seriesname, rm=rm, w=w, h=h, ddrill=ddrill, R_POW=R_POW, rm2=rm2, vlines=False, w2=w2, type=type, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", name_additions=name_additions, specialtags=[], add_description=add_description)

    # radial resistors, simple box
    rm2=0; w2=0
    type = "simple"; seriesname = "Box"; add_description = "http://www.vishay.com/docs/60051/cns020.pdf"; name_additions=[]
    w = 8.38; h = 2.54; ddrill = 0.8; rm=5.08; rm2=0; R_POW=0.5
    makeResistorRadial(seriesname=seriesname, rm=rm, w=w, h=h, ddrill=ddrill, R_POW=R_POW, rm2=rm2, vlines=False, w2=w2, type=type, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", name_additions=name_additions, specialtags=[], add_description=add_description)

    add_description = "http://www.produktinfo.conrad.com/datenblaetter/425000-449999/443860-da-01-de-METALLBAND_WIDERSTAND_0_1_OHM_5W_5Pr.pdf"; name_additions=[]
    w = 13; h = 4; ddrill = 1; rm=9; rm2=0; R_POW=2
    makeResistorRadial(seriesname=seriesname, rm=rm, w=w, h=h, ddrill=ddrill, R_POW=R_POW, rm2=rm2, vlines=False, w2=w2, type=type, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", name_additions=name_additions, specialtags=[], add_description=add_description)
    w = 14; h = 5; ddrill = 1; rm=9; rm2=0; R_POW=5
    makeResistorRadial(seriesname=seriesname, rm=rm, w=w, h=h, ddrill=ddrill, R_POW=R_POW, rm2=rm2, vlines=False, w2=w2, type=type, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", name_additions=name_additions, specialtags=[], add_description=add_description)
    w = 26; h = 5; ddrill = 1.4; rm=20; rm2=0; R_POW=10
    makeResistorRadial(seriesname=seriesname, rm=rm, w=w, h=h, ddrill=ddrill, R_POW=R_POW, rm2=rm2, vlines=False, w2=w2, type=type, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", name_additions=name_additions, specialtags=[], add_description=add_description)

    # radial resistors, simple
    rm2=0; w2=0
    type = "simple"; seriesname = "Radial_Power"; add_description = "http://www.vishay.com/docs/30218/cpcx.pdf"; name_additions=[]
    w = 11; w2=w-2; h = 7; ddrill = 1.2; rm=5; rm2=0; R_POW=2
    makeResistorRadial(seriesname=seriesname, rm=rm, w=w, h=h, ddrill=ddrill, R_POW=R_POW, rm2=rm2, vlines=True, w2=w2, type=type, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", name_additions=name_additions, specialtags=[], add_description=add_description)
    w = 12; w2=w-2; h = 8; ddrill = 1.2; rm=5; rm2=0; R_POW=3
    makeResistorRadial(seriesname=seriesname, rm=rm, w=w, h=h, ddrill=ddrill, R_POW=R_POW, rm2=rm2, vlines=True, w2=w2, type=type, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", name_additions=name_additions, specialtags=[], add_description=add_description)
    w = 13; w2=w-2; h = 9; ddrill = 1.2; rm=5; rm2=0; R_POW=7
    makeResistorRadial(seriesname=seriesname, rm=rm, w=w, h=h, ddrill=ddrill, R_POW=R_POW, rm2=rm2, vlines=True, w2=w2, type=type, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", name_additions=name_additions, specialtags=[], add_description=add_description)
    w = 16.1; w2=w-3; h = 9; ddrill = 1.4; rm=7.37; rm2=0; R_POW=10
    makeResistorRadial(seriesname=seriesname, rm=rm, w=w, h=h, ddrill=ddrill, R_POW=R_POW, rm2=rm2, vlines=True, w2=w2, type=type, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", name_additions=name_additions, specialtags=[], add_description=add_description)
