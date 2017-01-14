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
from footprint_scripts_LEDs import *


if __name__ == '__main__':
    # standard resistors: http://cdn-reichelt.de/documents/datenblatt/B400/1_4W%23YAG.pdf
    type = "round"
    script3d_rv="leds_round_ver.py"
    with open(script3d_rv, "w") as myfile:
        myfile.write("#\n# SCRIPT to generate 3D models\n#\n\n")

    d2=0
    R_POW = 0
    clname="LED"
    lbname="LEDs"
    ddrill = 0.9

    type="round"; pins=2;
    rm=2.54; rin=3; w=3.8; h=w; height3d=4.3; height3d_bottom=1; name_additions=[]; specialtags=[]; add_description=""
    makeLEDRadial(pins=pins, rm=rm, w=w, h=h, ddrill=ddrill, rin=rin, type=type, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", specialtags=specialtags, add_description=add_description, classname=clname, lib_name=lbname,name_additions=name_additions, script3d=script3d_rv, height3d=height3d, height3d_bottom=height3d_bottom)
    pins = 3; add_description="http://www.kingbright.com/attachments/file/psearch/000/00/00/L-3VSURKCGKC(Ver.8A).pdf"
    makeLEDRadial(pins=pins, rm=rm, w=w, h=h, ddrill=ddrill, rin=rin, type=type, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", specialtags=specialtags, add_description=add_description, classname=clname, lib_name=lbname,name_additions=name_additions, script3d=script3d_rv, height3d=height3d, height3d_bottom=height3d_bottom)
    pins=2; rm=2.54; rin=5; w=5.8; h=w; height3d=7.6; height3d_bottom=1; name_additions=[]; specialtags=[]; add_description="http://cdn-reichelt.de/documents/datenblatt/A500/LL-504BC2E-009.pdf"
    makeLEDRadial(pins=pins, rm=rm, w=w, h=h, ddrill=ddrill, rin=rin, type=type, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", specialtags=specialtags, add_description=add_description, classname=clname, lib_name=lbname,name_additions=name_additions, script3d=script3d_rv, height3d=height3d, height3d_bottom=height3d_bottom)
    pins = 3; add_description="http://www.kingbright.com/attachments/file/psearch/000/00/00/L-59EGC(Ver.17A).pdf"
    makeLEDRadial(pins=pins, rm=rm, w=w, h=h, ddrill=ddrill, rin=rin, type=type, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", specialtags=specialtags, add_description=add_description, classname=clname, lib_name=lbname,name_additions=name_additions, script3d=script3d_rv, height3d=height3d, height3d_bottom=height3d_bottom)
    pins = 4; rm=1.27; add_description="http://www.kingbright.com/attachments/file/psearch/000/00/00/L-154A4SUREQBFZGEW(Ver.9A).pdf"
    makeLEDRadial(pins=pins, rm=rm, w=w, h=h, ddrill=ddrill, rin=rin, type=type, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", specialtags=specialtags, add_description=add_description, classname=clname, lib_name=lbname,name_additions=name_additions, script3d=script3d_rv, height3d=height3d, height3d_bottom=height3d_bottom)
    pins=2; rm=2.54; rin=4; w=4.8; h=w; height3d=6; height3d_bottom=1; name_additions=[]; specialtags=[]; add_description="http://www.kingbright.com/attachments/file/psearch/000/00/00/L-43GD(Ver.12B).pdf"
    makeLEDRadial(pins=pins, rm=rm, w=w, h=h, ddrill=ddrill, rin=rin, type=type, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", specialtags=specialtags, add_description=add_description, classname=clname, lib_name=lbname,name_additions=name_additions, script3d=script3d_rv, height3d=height3d, height3d_bottom=height3d_bottom)
    pins=2; rm=2.54; rin=8; w=9; h=w; height3d=9; height3d_bottom=2; name_additions=[]; specialtags=[]; add_description="http://cdn-reichelt.de/documents/datenblatt/A500/LED8MMGE_LED8MMGN_LED8MMRT%23KIN.pdf"
    makeLEDRadial(pins=pins, rm=rm, w=w, h=h, ddrill=ddrill, rin=rin, type=type, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", specialtags=specialtags, add_description=add_description, classname=clname, lib_name=lbname,name_additions=name_additions, script3d=script3d_rv, height3d=height3d, height3d_bottom=height3d_bottom)
    pins = 3; add_description=""
    makeLEDRadial(pins=pins, rm=rm, w=w, h=h, ddrill=ddrill, rin=rin, type=type, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", specialtags=specialtags, add_description=add_description, classname=clname, lib_name=lbname,name_additions=name_additions, script3d=script3d_rv, height3d=height3d, height3d_bottom=height3d_bottom)
    pins=2; rm=2.54; rin=10; w=11; h=w; height3d=11.5; height3d_bottom=2; name_additions=[]; specialtags=[]; add_description="http://cdn-reichelt.de/documents/datenblatt/A500/LED10-4500RT%23KIN.pdf"
    makeLEDRadial(pins=pins, rm=rm, w=w, h=h, ddrill=ddrill, rin=rin, type=type, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", specialtags=specialtags, add_description=add_description, classname=clname, lib_name=lbname,name_additions=name_additions, script3d=script3d_rv, height3d=height3d, height3d_bottom=height3d_bottom)
    pins = 3; add_description="http://www.kingbright.com/attachments/file/psearch/000/00/00/L-819EGW(Ver.14A).pdf"
    makeLEDRadial(pins=pins, rm=rm, w=w, h=h, ddrill=ddrill, rin=rin, type=type, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", specialtags=specialtags, add_description=add_description, classname=clname, lib_name=lbname,name_additions=name_additions, script3d=script3d_rv, height3d=height3d, height3d_bottom=height3d_bottom)
    pins=2; rm=2.54; rin=20; w=23; h=w; height3d=10; height3d_bottom=3.5; name_additions=[]; specialtags=[]; add_description="http://cdn-reichelt.de/documents/datenblatt/A500/DLC2-6GD%28V6%29.pdf"
    makeLEDRadial(pins=pins, rm=rm, w=w, h=h, ddrill=ddrill, rin=rin, type=type, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", specialtags=specialtags, add_description=add_description, classname=clname, lib_name=lbname,name_additions=name_additions, script3d=script3d_rv, height3d=height3d, height3d_bottom=height3d_bottom)
    type="oval"; pins=2; rm=2.54; rin=0; w=5.2; h=3.8; height3d=7; height3d_bottom=0; name_additions=[]; specialtags=["Oval"]; add_description="http://www.kingbright.com/attachments/file/psearch/000/00/00/L-5603QBC-D(Ver.12B).pdf"
    makeLEDRadial(pins=pins, rm=rm, w=w, h=h, ddrill=ddrill, rin=rin, type=type, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", specialtags=specialtags, add_description=add_description, classname=clname+"_Oval", lib_name=lbname,name_additions=name_additions, script3d=script3d_rv, height3d=height3d, height3d_bottom=height3d_bottom)
    type="box"; pins=2; rm=2.54; rin=2; w=4.8; h=2.5; height3d=4.5; height3d_bottom=3.5; name_additions=[]; specialtags=["Round", "FlatTop"]; add_description="http://www.kingbright.com/attachments/file/psearch/000/00/00/L-13GD(Ver.11B).pdf"
    makeLEDRadial(pins=pins, rm=rm, w=w, h=h, ddrill=ddrill, rin=rin, type=type, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", specialtags=specialtags, add_description=add_description, classname=clname+"_Round_FlatTop", lib_name=lbname,name_additions=name_additions, script3d=script3d_rv, height3d=height3d, height3d_bottom=height3d_bottom)
    type="round"; pins=2; rm=2.54; rin=3; w=3.8; h=w; height3d=4.8; height3d_bottom=6-4.8; name_additions=[]; specialtags=["Round","FlatTop"]; add_description="http://www.kingbright.com/attachments/file/psearch/000/00/00/L-47XEC(Ver.9A).pdf"
    makeLEDRadial(pins=pins, rm=rm, w=w, h=h, ddrill=ddrill, rin=rin, type=type, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", specialtags=specialtags, add_description=add_description, classname=clname+"_Round_FlatTop", lib_name=lbname,name_additions=name_additions, script3d=script3d_rv, height3d=height3d, height3d_bottom=height3d_bottom)
    type="round"; pins=2; rm=2.54; rin=5; w=5.9; h=w; height3d=8.6; height3d_bottom=1; name_additions=[]; specialtags=["Round","FlatTop"]; add_description="http://www.kingbright.com/attachments/file/psearch/000/00/00/L-483GDT(Ver.15B).pdf"
    makeLEDRadial(pins=pins, rm=rm, w=w, h=h, ddrill=ddrill, rin=rin, type=type, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", specialtags=specialtags, add_description=add_description, classname=clname+"_Round_FlatTop", lib_name=lbname,name_additions=name_additions, script3d=script3d_rv, height3d=height3d, height3d_bottom=height3d_bottom)
    type="box"; pins=2; rm=2.54; rin=2; w=4; h=2.8; height3d=1.95; height3d_bottom=5-1.95; name_additions=[]; specialtags=["Round","FlatTop"]; add_description="http://www.kingbright.com/attachments/file/psearch/000/00/00/L-1034IDT(Ver.9A).pdf"
    makeLEDRadial(pins=pins, rm=rm, w=w, h=h, ddrill=ddrill, rin=rin, type=type, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", specialtags=specialtags, add_description=add_description, classname=clname+"_Round_FlatTop", lib_name=lbname,name_additions=name_additions, script3d=script3d_rv, height3d=height3d, height3d_bottom=height3d_bottom)
    type="box"; pins=2; rm=2.54; rin=0; w=3.9; h=1.75; height3d=7; height3d_bottom=0; name_additions=[]; specialtags=["Rectangular"]; add_description="http://www.kingbright.com/attachments/file/psearch/000/00/00/L-2774GD(Ver.7B).pdf"
    makeLEDRadial(pins=pins, rm=rm, w=w, h=h, ddrill=ddrill, rin=rin, type=type, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", specialtags=specialtags, add_description=add_description, classname=clname+"_Rectangular", lib_name=lbname,name_additions=name_additions, script3d=script3d_rv, height3d=height3d, height3d_bottom=height3d_bottom)
    type="box"; pins=2; rm=2.54; rin=0; w=3.9; h=1.9; height3d=7; height3d_bottom=0; name_additions=[]; specialtags=["Rectangular"]; add_description="http://www.kingbright.com/attachments/file/psearch/000/00/00/L-144GDT(Ver.14B).pdf"
    makeLEDRadial(pins=pins, rm=rm, w=w, h=h, ddrill=ddrill, rin=rin, type=type, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", specialtags=specialtags, add_description=add_description, classname=clname+"_Rectangular", lib_name=lbname,name_additions=name_additions, script3d=script3d_rv, height3d=height3d, height3d_bottom=height3d_bottom)
    type="box"; pins=2; rm=2.54; rin=0; w=3; h=2;  height3d=7; height3d_bottom=0; name_additions=[]; specialtags=["Rectangular"]; add_description="http://www.kingbright.com/attachments/file/psearch/000/00/00/L-169XCGDK(Ver.9B).pdf"
    makeLEDRadial(pins=pins, rm=rm, w=w, h=h, ddrill=ddrill, rin=rin, type=type, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", specialtags=specialtags, add_description=add_description, classname=clname+"_Rectangular", lib_name=lbname,name_additions=name_additions, script3d=script3d_rv, height3d=height3d, height3d_bottom=height3d_bottom)
    type="box"; pins=2; rm=2.54; rin=0; w=5; h=2;  height3d=9.7; height3d_bottom=0; name_additions=[]; specialtags=["Rectangular"]; add_description="http://www.kingbright.com/attachments/file/psearch/000/00/00/L-169XCGDK(Ver.9B).pdf"
    makeLEDRadial(pins=pins, rm=rm, w=w, h=h, ddrill=ddrill, rin=rin, type=type, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", specialtags=specialtags, add_description=add_description, classname=clname+"_Rectangular", lib_name=lbname,name_additions=name_additions, script3d=script3d_rv, height3d=height3d, height3d_bottom=height3d_bottom)
    type="box"; pins=3; rm=2.54; rin=0; w=5; h=2;  height3d=9.7; height3d_bottom=0; name_additions=[]; specialtags=["Rectangular"]; add_description="http://www.kingbright.com/attachments/file/psearch/000/00/00/L-169XCGDK(Ver.9B).pdf"
    makeLEDRadial(pins=pins, rm=rm, w=w, h=h, ddrill=ddrill, rin=rin, type=type, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", specialtags=specialtags, add_description=add_description, classname=clname+"_Rectangular", lib_name=lbname,name_additions=name_additions, script3d=script3d_rv, height3d=height3d, height3d_bottom=height3d_bottom)
    type="box"; pins=2; rm=2.54; rin=0; w=5; h=5;  height3d=9.7; height3d_bottom=0; name_additions=[]; specialtags=["Rectangular"]; add_description="http://www.kingbright.com/attachments/file/psearch/000/00/00/L-169XCGDK(Ver.9B).pdf"
    makeLEDRadial(pins=pins, rm=rm, w=w, h=h, ddrill=ddrill, rin=rin, type=type, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", specialtags=specialtags, add_description=add_description, classname=clname+"_Rectangular", lib_name=lbname,name_additions=name_additions, script3d=script3d_rv, height3d=height3d, height3d_bottom=height3d_bottom)
    