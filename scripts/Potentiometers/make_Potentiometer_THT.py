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
from footprint_scripts_potentiometers import *


if __name__ == '__main__':
    script3d_tsl="trimmer_screwleft.py"
    with open(script3d_tsl, "w") as myfile:
        myfile.write("#\n# SCRIPT to generate 3D models\n#\n\n")
    script3d_tst="trimmer_screwtop.py"
    with open(script3d_tst, "w") as myfile:
        myfile.write("#\n# SCRIPT to generate 3D models\n#\n\n")
    script3d_tsl_smd="trimmer_screwleft_smd.py"
    with open(script3d_tsl_smd, "w") as myfile:
        myfile.write("#\n# SCRIPT to generate 3D models\n#\n\n")
    script3d_tst_smd="trimmer_screwtop_smd.py"
    with open(script3d_tst_smd, "w") as myfile:
        myfile.write("#\n# SCRIPT to generate 3D models\n#\n\n")
    script3d_pv="pots_ver.py"
    with open(script3d_pv, "w") as myfile:
        myfile.write("#\n# SCRIPT to generate 3D models\n#\n\n")
    script3d_trv="trim_round_ver.py"
    with open(script3d_trv, "w") as myfile:
        myfile.write("#\n# SCRIPT to generate 3D models\n#\n\n")
    script3d_trh="trim_round_hor.py"
    with open(script3d_trh, "w") as myfile:
        myfile.write("#\n# SCRIPT to generate 3D models\n#\n\n")
    script3d_trh_bel="trim_round_hor_below.py"
    with open(script3d_trh_bel, "w") as myfile:
        myfile.write("#\n# SCRIPT to generate 3D models\n#\n\n")
    script3d_trh_smd="trim_round_smd_hor.py"
    with open(script3d_trh_smd, "w") as myfile:
        myfile.write("#\n# SCRIPT to generate 3D models\n#\n\n")
    script3d_trh_smd_bel="trim_round_smd_hor_below.py"
    with open(script3d_trh_smd_bel, "w") as myfile:
        myfile.write("#\n# SCRIPT to generate 3D models\n#\n\n")
    script3d_ph_bel="pots_hor_below.py"
    with open(script3d_ph_bel, "w") as myfile:
        myfile.write("#\n# SCRIPT to generate 3D models\n#\n\n")
    script3d_ph="pots_hor.py"
    with open(script3d_ph, "w") as myfile:
        myfile.write("#\n# SCRIPT to generate 3D models\n#\n\n")

    R_POW = 0

    class_name="Omeg PC16BU"; add_description="http://www.omeg.co.uk/pc6bubrc.htm"
    pins = 3; rmx=5.0; rmy=5.; ddrill=1.3; wbody=9.3; hbody=16.9; height3d = 21; screwzpos = 12.5; wscrew=6; dscrew=7
    wshaft=50-wscrew; dshaft=4; pinxoffset=6.3; pinyoffset=(hbody-2*rmy)/2.0
    makePotentiometerHorizontal(class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_pv,height3d=height3d, screwzpos=screwzpos)
    voffsetx=1.75; dbody=16.9; vwbody=5; vpinyoffset=(hbody-2*rmy)/2.0; c_offsety=dbody/2.0; c_offsetx=10.8
    #makePotentiometerVertical(shaft_hole=True, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=dscrew+0.5,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_ph_bel,height3d=height3d)
    makePotentiometerVertical(shaft_hole=False, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=dscrew+0.5,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_ph,height3d=height3d)
    
    class_name="Vishay 248GJ-249GJ Single"; add_description="http://www.vishay.com/docs/57054/248249.pdf"
    pins = 3; rmx=7.62; rmy=2.54; ddrill=1; wbody=7.6; hbody=12.5; height3d = 13.1; screwzpos = 12.7/2.0+0.6; wscrew=9.5; dscrew=(3/8.0)*25.4
    wshaft=22.22-wscrew; dshaft=(1/4.0)*25.4; pinxoffset=5.08; pinyoffset=(hbody-2*rmy)/2.0
    makePotentiometerHorizontal(class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_pv,height3d=height3d, screwzpos=screwzpos)
    voffsetx=0.75; dbody=0; vwbody=12.7; vpinyoffset=(hbody-2*rmy)/2.0; c_offsety=hbody/2.0; c_offsetx=vwbody/2.0
    #makePotentiometerVertical(shaft_hole=True, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=dscrew+0.5,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_ph_bel,height3d=height3d)
    makePotentiometerVertical(shaft_hole=False, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=dscrew+0.5,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_ph,height3d=height3d)
    class_name="Vishay 248BH-249BH Single"; add_description="http://www.vishay.com/docs/57054/248249.pdf"
    wscrew=9.5; dscrew=0.25*25.4; wshaft=19.05-wscrew; dshaft=3.18; pinxoffset=5.08; pinyoffset=(hbody-2*rmy)/2.0
    makePotentiometerHorizontal(class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_pv,height3d=height3d, screwzpos=screwzpos)

    class_name="Vishay 148-149 Single"; add_description="http://www.vishay.com/docs/57040/148149.pdf"
    pins = 3; rmx=7.62; rmy=2.54; ddrill=1; wbody=8.83; hbody=12.5; height3d = 13.1; screwzpos = 12.5/2.0+0.6; wscrew=6.35; dscrew=0.25*25.4
    wshaft=12.8-wscrew; dshaft=3.17; pinxoffset=5.08; pinyoffset=(hbody-2*rmy)/2.0
    makePotentiometerHorizontal(class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_pv,height3d=height3d, screwzpos=screwzpos)
    voffsetx=0.75; dbody=0; vwbody=12.5; vpinyoffset=(hbody-2*rmy)/2.0; c_offsety=hbody/2.0; c_offsetx=vwbody/2.0
    #makePotentiometerVertical(shaft_hole=True, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=dscrew+0.5,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_ph_bel,height3d=height3d)
    makePotentiometerVertical(shaft_hole=False, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=dscrew+0.5,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_ph,height3d=height3d)
    class_name="Vishay 148E-149E Single"
    wbody = 6.35 + 3.85 + 1.52 + 0.5
    makePotentiometerHorizontal(mh_ddrill=1.3, mh_count=4, mh_rmx=3.85+6.35, mh_rmy=10.16, mh_xoffset=3.85, mh_yoffset=(10.16-2*rmy)/2.0, class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_pv,height3d=height3d, screwzpos=screwzpos)
    class_name="Vishay 148-149 Dual"
    pins = 6; wbody=16.45; wscrew=7
    makePotentiometerHorizontal(class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_pv,height3d=height3d, screwzpos=screwzpos)
    class_name="Vishay 148E-149E Dual"
    wbody = 6.35+7.62+3.85+1.52+0.5
    makePotentiometerHorizontal(mh_ddrill=1.3, mh_count=4, mh_rmx=3.85+7.62+6.35, mh_rmy=10.16, mh_xoffset=3.85, mh_yoffset=(10.16-2*rmy)/2.0, class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_pv,height3d=height3d, screwzpos=screwzpos)

    class_name="Piher PC-16 Single"; add_description="http://www.piher-nacesa.com/pdf/20-PC16v03.pdf"
    pins = 3; rmx=7.5; rmy=5.0; ddrill=1.3; wbody=8; hbody=16; height3d = 20.5; screwzpos = 12.5; wscrew=9; dscrew=10
    wshaft=25-wscrew; dshaft=6; pinxoffset=6.5; pinyoffset=(hbody-2*rmy)/2.0
    makePotentiometerHorizontal(class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_pv,height3d=height3d, screwzpos=screwzpos)
    voffsetx = 0.5; dbody = 0; vwbody = 18; vpinyoffset = (hbody-2*rmy)/2.0; c_offsetx = 10; c_offsety = hbody/2.0
    #makePotentiometerVertical(shaft_hole=True, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=dscrew+0.5,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_ph_bel,height3d=height3d)
    makePotentiometerVertical(shaft_hole=False, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=dscrew+0.5,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_ph,height3d=height3d)
    #class_name="Piher PC-16SV Single"
    #voffsetx=0.5; dbody=0; vwbody=18; vpinyoffset=(hbody-2*rmy)/2.0; c_offsetx=10; c_offsety=hbody/2.0
    #makePotentiometerVertical(mh_ddrill=1.3, mh_count=2, mh_rmx=0, mh_rmy=10.0, mh_xoffset=15, mh_yoffset=(10-2*rmy)/2.0, shaft_hole=False, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=dscrew+0.5,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_ph_bel,height3d=height3d)
    class_name="Piher PC-16 Dual"
    pins = 6; wbody=16
    makePotentiometerHorizontal(class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_pv,height3d=height3d, screwzpos=screwzpos)
    class_name="Piher PC-16 Triple"
    pins = 9; wbody=24
    makePotentiometerHorizontal(class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_pv,height3d=height3d, screwzpos=screwzpos)

    class_name="Piher T-16H Single"; add_description="http://www.piher-nacesa.com/pdf/22-T16v03.pdf"
    pins = 3; rmx=7.5; rmy=5.0; ddrill=1.3; wbody=7.5; hbody=16; height3d = 21; screwzpos = 12.5; wscrew=5; dscrew=7
    wshaft=15-wscrew; dshaft=4; pinxoffset=1.5; pinyoffset=(hbody-2*rmy)/2.0
    makePotentiometerHorizontal(class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_pv,height3d=height3d, screwzpos=screwzpos)
    class_name="Piher T-16L Single"
    voffsetx=-0.5; dbody=16; vwbody=3; vpinyoffset=(hbody-2*rmy)/2.0; c_offsetx=10.5; c_offsety=hbody/2.0
    makePotentiometerVertical(shaft_hole=True, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=dscrew+0.5,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_ph_bel,height3d=height3d)
    class_name="Piher T-16H Double"
    pins = 6; wbody=15
    makePotentiometerHorizontal(class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_pv,height3d=height3d, screwzpos=screwzpos)
 
    class_name="Alps RK163 Single"; add_description="http://www.alps.com/prod/info/E/HTML/Potentiometer/RotaryPotentiometers/RK16/RK16_list.html"
    pins = 3; rmx=5.0; rmy=5.0; ddrill=1.3; wbody=10.5; hbody=17.9; height3d = 21; screwzpos = 12.5; wscrew=5; dscrew=7
    wshaft=15-wscrew; dshaft=6; pinxoffset=3.8; pinyoffset=(hbody-2*rmy)/2.0
    makePotentiometerHorizontal(class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_pv,height3d=height3d, screwzpos=screwzpos)
    class_name="Alps RK163 Dual"
    pins = 6; wbody=12.1; wscrew=7
    makePotentiometerHorizontal(class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_pv,height3d=height3d, screwzpos=screwzpos)
    
    class_name="Alps RK097 Single"; add_description="http://www.alps.com/prod/info/E/HTML/Potentiometer/RotaryPotentiometers/RK097/RK097_list.html"
    pins = 3; rmx=2.5; rmy=2.5; ddrill=1; wbody=7.05; hbody=9.5; height3d = 6.5+0.25+4.85; screwzpos = 6.5+0.25; wscrew=5; dscrew=7
    wshaft=15-wscrew; dshaft=6; pinxoffset=5; pinyoffset=(hbody-2*rmy)/2.0
    makePotentiometerHorizontal(class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_pv,height3d=height3d, screwzpos=screwzpos)
    class_name="Alps RK097 Dual"
    pins = 6; wbody=9.55
    makePotentiometerHorizontal(class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_pv,height3d=height3d, screwzpos=screwzpos)

    class_name="Bourns PTV09A-2 Single"; add_description="http://www.bourns.com/docs/Product-Datasheets/ptv09.pdf"
    pins = 3; rmx=2.5; rmy=2.5; ddrill=1; wbody=5; hbody=9.7; height3d = 10+5.5; screwzpos = 10; wscrew=0.8; dscrew=6.8
    wshaft=15-wbody-wscrew; dshaft=6; pinxoffset=3.5; pinyoffset=(hbody-2*rmy)/2.0
    makePotentiometerHorizontal(mh_ddrill=2.3, mh_count=2, mh_rmx=0, mh_rmy=10, mh_xoffset=-3.3, mh_yoffset=(10-2*rmy)/2.0, class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_pv,height3d=height3d, screwzpos=screwzpos)
    class_name="Bourns PTV09A-1 Single"
    voffsetx=1; dbody=0; vwbody=12; vpinyoffset=(hbody-2*rmy)/2.0; c_offsetx=6.5; c_offsety=hbody/2.0
    makePotentiometerVertical(mh_ddrill=2, mh_count=2, mh_rmx=0, mh_rmy=8.8, mh_xoffset=7, mh_yoffset=(8.8-2*rmy)/2.0, shaft_hole=False, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=dscrew+0.5,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_ph_bel,height3d=height3d)    

    class_name="Alps RK09K Single"; add_description="http://www.alps.com/prod/info/E/HTML/Potentiometer/RotaryPotentiometers/RK09K/RK09K_list.html"
    pins = 3; rmx=2.5; rmy=2.5; ddrill=1; wbody=6.8; hbody=9.8; height3d = 6.5+5.5; screwzpos = 6.5; wscrew=0.8; dscrew=6.5
    wshaft=15-6.8-wscrew; dshaft=6; pinxoffset=3.4; pinyoffset=(hbody-2*rmy)/2.0
    makePotentiometerHorizontal(mh_ddrill=2.3, mh_count=2, mh_rmx=0, mh_rmy=10, mh_xoffset=-3.3, mh_yoffset=(10-2*rmy)/2.0, class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_pv,height3d=height3d, screwzpos=screwzpos)
    class_name="Alps RK09K Single"
    voffsetx=1; dbody=0; vwbody=12; vpinyoffset=(hbody-2*rmy)/2.0; c_offsetx=6.5; c_offsety=hbody/2.0
    makePotentiometerVertical(mh_ddrill=2, mh_count=2, mh_rmx=0, mh_rmy=8.8, mh_xoffset=7, mh_yoffset=(8.8-2*rmy)/2.0, shaft_hole=False, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=dscrew+0.5,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_ph_bel,height3d=height3d)
    
    class_name="Alps RK09L Single"; add_description="http://www.alps.com/prod/info/E/HTML/Potentiometer/RotaryPotentiometers/RK09L/RK09L_list.html"
    pins = 3; rmx=2.5; rmy=2.5; ddrill=1; wbody=7.45; hbody=12.1; height3d = 6.5+0.25+4.85; screwzpos = 6.5+0.25; wscrew=5; dscrew=9
    wshaft=15-wscrew; dshaft=6; pinxoffset=5; pinyoffset=(hbody-2*rmy)/2.0
    makePotentiometerHorizontal(mh_ddrill=2.1, mh_count=2, mh_rmx=0, mh_rmy=9.5, mh_xoffset=-4.1, mh_yoffset=(9.5-2*rmy)/2.0, class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_pv,height3d=height3d, screwzpos=screwzpos)
    class_name="Alps RK09L Single"
    voffsetx=1; dbody=0; vwbody=11.35; vpinyoffset=(hbody-2*rmy)/2.0; c_offsetx=6.5; c_offsety=hbody/2.0
    makePotentiometerVertical(mh_ddrill=2, mh_count=2, mh_rmx=0, mh_rmy=9.5, mh_xoffset=7.5, mh_yoffset=(9.5-2*rmy)/2.0, shaft_hole=False, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=dscrew+0.5,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_ph_bel,height3d=height3d)
    class_name="Alps RK09L Double"
    pins = 6; wbody=9.14
    makePotentiometerHorizontal(mh_ddrill=2.1, mh_count=2, mh_rmx=0, mh_rmy=9.5, mh_xoffset=-5.8, mh_yoffset=(9.5-2*rmy)/2.0, class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_pv,height3d=height3d, screwzpos=screwzpos)
    class_name="Alps RK09L Double"
    voffsetx=1; dbody=0; vwbody=11.35; vpinyoffset=(hbody-2*rmy)/2.0; c_offsetx=6.5; c_offsety=hbody/2.0
    makePotentiometerVertical(mh_ddrill=2, mh_count=2, mh_rmx=0, mh_rmy=9.5, mh_xoffset=7.5, mh_yoffset=(9.5-2*rmy)/2.0, shaft_hole=False, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=dscrew+0.5,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_ph_bel,height3d=height3d)

    class_name="Alps RK09Y11 Single"; add_description="http://www.alps.com/prod/info/E/HTML/Potentiometer/RotaryPotentiometers/RK09Y11/RK09Y11_list.html"
    pins = 3; rmx=5.0; rmy=2.5; ddrill=1.0; wbody=5.4; hbody=9.5; height3d = 6.25+0.25+4.85; screwzpos = 6.25+0.25; wscrew=5; dscrew=7
    wshaft=12-wscrew; dshaft=5; pinxoffset=3.45; pinyoffset=(hbody-2*rmy)/2.0
    makePotentiometerHorizontal(class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_pv,height3d=height3d, screwzpos=screwzpos)

    class_name="Bourns 3339S"; add_description='http://www.bourns.com/docs/Product-Datasheets/3339.pdf'
    pins = 3; rmx=-2.54; rmy=2.54; ddrill=0.8; wbody=5.97; hbody=8.13; dbody=0; height3d = 9.53; screwzpos = 5.54; wscrew=8-5.97; dscrew=7.62
    wshaft=0; dshaft=4; pinxoffset=+4.57-wscrew; pinyoffset=(hbody-2*rmy)/2.0
    makePotentiometerHorizontal(style="trimmer", class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_trv,height3d=height3d, screwzpos=screwzpos)
    rmx=2.54; pinxoffset=+4.57-wscrew+2.54
    class_name="Bourns 3339W"
    makePotentiometerHorizontal(style="trimmer", class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_trv,height3d=height3d, screwzpos=screwzpos)
    class_name="Bourns 3339P"
    pins = 3; rmx=-2.54; rmy=2.54; ddrill=0.7; wbody=0; hbody=7.62; dbody=7.62; height3d = 6.35; wscrew=-wbody; dscrew=5
    wshaft=0; dshaft=0; pinxoffset=0; pinyoffset=(hbody-2*rmy)/2.0
    voffsetx=-rmx; vwbody=0; pinyoffset=(hbody-2*rmy)/2.0; c_offsetx=rmx; c_offsety=hbody/2.0; c_ddrill=2
    makePotentiometerVertical(screwstyle='slit', style="trimmer", shaft_hole=False, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=c_ddrill,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_ph_bel,height3d=height3d)
    class_name="Bourns 3339H"
    rmx = 2.54 / math.sqrt(2); rmy = 2.54 / math.sqrt(2); voffsetx = rmx*2; vwbody = 0
    pinyoffset = (hbody - 2 * rmy)/2.0; c_offsetx=-rmx;  c_offsety=hbody/2.0; c_ddrill=2
    makePotentiometerVertical(screwstyle='slit', style="trimmer", shaft_hole=False, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=c_ddrill,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_ph_bel,height3d=height3d)

    class_name="Vishay T7-YA Single"; add_description="http://www.vishay.com/docs/51015/t7.pdf"
    pins = 3; rmx=2.54; rmy=2.54; ddrill=0.8; wbody=0; hbody=7; dbody=7; height3d = 5.85; wscrew=-wbody; dscrew=4.1
    wshaft=0; dshaft=0; pinxoffset=0; pinyoffset=(hbody-2*rmy)/2.0
    voffsetx=-rmx; vwbody=0; vpinyoffset=(hbody-2*rmy)/2.0; c_offsetx=2.5; c_offsety=hbody/2.0; c_ddrill=2
    makePotentiometerVertical(screwstyle='slit', style="trimmer", shaft_hole=False, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=c_ddrill,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_ph_bel,height3d=height3d)
    
    class_name="Bourns 3386X"; add_description="https://www.bourns.com/pdfs/3386.pdf"
    pins = 3; rmx=2.54; rmy=2.54; ddrill=0.8; wbody=-4.83; hbody=9.53; dbody=0; height3d = 9.53; screwzpos = 5.33; wscrew=0; dscrew=3.15
    wshaft=0; dshaft=0; pinxoffset=-(4.83-2.54)/2.0; pinyoffset=(hbody-2*rmy)/2.0
    makePotentiometerHorizontal(style="trimmer", class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_trv,height3d=height3d, screwzpos=screwzpos)
    class_name = "Bourns 3386C"
    rmx=0; pinxoffset=-4.83/2.0
    makePotentiometerHorizontal(style="trimmer", class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_trv,height3d=height3d, screwzpos=screwzpos)
    class_name="Bourns 3386P"
    rmx=2.54; dbody=0; voffsetx=-4.78; vwbody=9.53; vpinyoffset=(hbody-2*rmy)/2.0; c_offsetx=9.53-5.64; c_offsety=hbody/2.0; c_ddrill=2; height3d = 4.83
    makePotentiometerVertical(screwstyle="slit", style="trimmer", shaft_hole=False, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=c_ddrill,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_ph_bel,height3d=height3d)
    class_name="Bourns 3386F"
    rmx=5.08; voffsetx=-9.53+5.08+2.34
    makePotentiometerVertical(screwstyle="slit", style="trimmer", shaft_hole=False, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=c_ddrill,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_ph_bel,height3d=height3d)

    class_name="Vishay T73XX"; add_description="http://www.vishay.com/docs/51016/t73.pdf"
    pins = 3; rmx=2.54; rmy=2.54; ddrill=0.8; wbody=-4.7; hbody=6.6; dbody=0; height3d = 7; screwzpos = 3.8; wscrew=0; dscrew=3
    wshaft=0; dshaft=0; pinxoffset=-1.02; pinyoffset=(hbody-2*rmy)/2.0
    makePotentiometerHorizontal(style="trimmer", class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_trv,height3d=height3d, screwzpos=screwzpos)
    class_name="Vishay T73XW"
    rmx=0; pinxoffset=-2.35
    makePotentiometerHorizontal(style="trimmer", class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_trv,height3d=height3d, screwzpos=screwzpos)
    class_name="Vishay T73YP"
    rmx=2.54; dbody=0; voffsetx=-3.56; vwbody=7; vpinyoffset=(hbody-2*rmy)/2.0; c_offsetx=3.8; c_offsety=hbody/2.0; c_ddrill=2
    makePotentiometerVertical(screwstyle="cross", style="trimmer", shaft_hole=False, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=c_ddrill,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_ph_bel,height3d=height3d)

    class_name="Piher PT-6-H"; add_description="http://www.piher-nacesa.com/pdf/11-PT6v03.pdf"
    pins = 3; rmx=2.5; rmy=2.5; ddrill=0.9; wbody=-3.5; hbody=6.3; dbody=6.3; height3d = 4.5+dbody/2.0; screwzpos = 4.5; wscrew=-wbody; dscrew=2
    wshaft=0; dshaft=1.8; pinxoffset=0; pinyoffset=(hbody-2*rmy)/2.0
    makePotentiometerHorizontal(style="trimmer", class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_trv,height3d=height3d, screwzpos=screwzpos)
    class_name="Piher PT-6-V"
    rmx=5; dbody=6.3; voffsetx=0; vwbody=0; vpinyoffset=(hbody-2*rmy)/2.0; c_offsetx=2.5; c_offsety=hbody/2.0; c_ddrill=2; height3d=4
    makePotentiometerVertical(style="trimmer", shaft_hole=False, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=c_ddrill,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_trh,height3d=height3d)
    makePotentiometerVertical(style="trimmer", shaft_hole=True, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=c_ddrill,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_trh_bel,height3d=height3d)

    class_name="Piher PT-10-H01"; add_description="http://www.piher-nacesa.com/pdf/12-PT10v03.pdf"
    pins = 3; rmx=2.5; rmy=2.5; ddrill=1.3; wbody=-4.8; hbody=10.3; height3d = 12.1; screwzpos = 7; dbody=10.3; wscrew=-wbody; dscrew=3.5
    wshaft=0; dshaft=3; pinxoffset=0; pinyoffset=(hbody-2*rmy)/2.0
    #name_additions=["Px{0:1.1f}mm_Py{1:1.1f}mm".format(rmx, 2*rmy)]
    makePotentiometerHorizontal(style="trimmer", class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_trv,height3d=height3d, screwzpos=screwzpos)
    class_name="Piher PT-10-H05"
    rmx=5; height3d = 12.1; screwzpos = 7;  pinyoffset=(hbody-2*rmy)/2.0
    #name_additions = ["Px{0:1.1f}mm_Py{1:1.1f}mm".format(rmx, 2 * rmy)]
    makePotentiometerHorizontal(style="trimmer", class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_trv,height3d=height3d, screwzpos=screwzpos)
    class_name="Piher PT-101-H3.8"
    rmx=3.8; height3d = 17.1; screwzpos = 9.6;  pinyoffset=(hbody-2*rmy)/2.0
    #name_additions = ["Px{0:1.1f}mm_Py{1:1.1f}mm".format(rmx, 2 * rmy)]
    #makePotentiometerHorizontal(style="trimmer", class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_trv,height3d=height3d, screwzpos=screwzpos)
    class_name="Piher PT-10-V10"
    hbody=10; rmx=10; dbody=10.3; voffsetx=0; vwbody=0; vpinyoffset=(hbody-2*rmy)/2.0; c_offsetx=5; c_offsety=hbody/2.0; c_ddrill=4; height3d=5.3
    #name_additions = ["Px{0:1.1f}mm_Py{1:1.1f}mm".format(rmx, 2 * rmy)]
    makePotentiometerVertical(style="trimmer", shaft_hole=False, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=c_ddrill,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_trh,height3d=height3d)
    makePotentiometerVertical(style="trimmer", shaft_hole=True, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=c_ddrill,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_trh_bel,height3d=height3d)
    class_name="Piher PT-10-V05"
    voffsetx = -5.3/2.0; hbody=10; rmx=5; dbody=10.3; vwbody=0; vpinyoffset=(hbody-2*rmy)/2.0; c_offsetx=10.3/2.0; c_offsety=dbody/2.0; c_ddrill=3
    #name_additions = ["Px{0:1.1f}mm_Py{1:1.1f}mm".format(rmx, 2 * rmy)]
    makePotentiometerVertical(style="trimmer", shaft_hole=False, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=c_ddrill,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_trh_bel,height3d=height3d)
    #name_additions = []
    
    class_name="Piher PT-15-H05"; add_description="http://www.piher-nacesa.com/pdf/14-PT15v03.pdf"
    pins = 3; rmx=5.0; rmy=5; ddrill=1.3; wbody=-5; hbody=15; height3d = 17.5; screwzpos = 10; dbody=15; wscrew=-wbody; dscrew=6
    wshaft=0; dshaft=4.4; pinxoffset=0; pinyoffset=(hbody-2*rmy)/2.0
    #name_additions = ["Px{0:1.1f}mm_Py{1:1.1f}mm".format(rmx, 2 * rmy)]
    makePotentiometerHorizontal(style="trimmer", class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_trv,height3d=height3d, screwzpos=screwzpos)
    class_name="Piher PT-15-H01"
    rmy=5; rmx=2.5; height3d = 17.5; screwzpos = 10;  pinyoffset=(hbody-2*rmy)/2.0
    #name_additions = ["Px{0:1.1f}mm_Py{1:1.1f}mm".format(rmx, 2 * rmy)]
    makePotentiometerHorizontal(style="trimmer", class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_trv,height3d=height3d, screwzpos=screwzpos)
    class_name="Piher PT-15-H06"
    rmy=4.4; rmx=4; height3d = 17.1; screwzpos = 9.6;  pinyoffset=(hbody-2*rmy)/2.0
    #name_additions = ["Px{0:1.1f}mm_Py{1:1.1f}mm".format(rmx, 2 * rmy)]
    makePotentiometerHorizontal(style="trimmer", class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_trv,height3d=height3d, screwzpos=screwzpos)
    class_name="Piher PT-15-H25"
    rmy=5; rmx=5; height3d = 20; screwzpos = 12.5;  pinyoffset=(hbody-2*rmy)/2.0
    #name_additions = ["Px{0:1.1f}mm_Py{1:1.1f}mm".format(rmx, 2 * rmy)]
    makePotentiometerHorizontal(style="trimmer", class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_trv,height3d=height3d, screwzpos=screwzpos)
    class_name="Piher PT-15-V02"
    hbody=10; rmx=12.5; dbody=15; voffsetx=0; vwbody=0; vpinyoffset=(dbody-2*rmy)/2.0; c_offsetx=7.5; c_offsety=dbody/2.0; c_ddrill=7; height3d=5.5
    #name_additions = ["Px{0:1.1f}mm_Py{1:1.1f}mm".format(rmx, 2 * rmy)]
    makePotentiometerVertical(style="trimmer", shaft_hole=False, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=c_ddrill,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_trh,height3d=height3d)
    makePotentiometerVertical(style="trimmer", shaft_hole=True, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=c_ddrill,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_trh_bel,height3d=height3d)
    class_name="Piher PT-15-V15"
    voffsetx =0; hbody=15; rmx=15; dbody=15; vwbody=0; vpinyoffset=(dbody-2*rmy)/2.0; c_offsetx=7.5; c_offsety=dbody/2.0; c_ddrill=7
    #name_additions = ["Px{0:1.1f}mm_Py{1:1.1f}mm".format(rmx, 2 * rmy)]
    makePotentiometerVertical(style="trimmer", shaft_hole=False, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=c_ddrill,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_trh,height3d=height3d)
    makePotentiometerVertical(style="trimmer", shaft_hole=True, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=c_ddrill,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_trh_bel,height3d=height3d)
    #name_additions=[]
    
    class_name="ACP CA6-H2,5"; add_description="http://www.acptechnologies.com/wp-content/uploads/2017/06/01-ACP-CA6.pdf"
    pins = 3; rmx=2.5; rmy=2.5; ddrill=0.9; wbody=-3.5; hbody=6.3; dbody=0; height3d = 4.5+hbody/2.0; screwzpos = 4.5; wscrew=-wbody; dscrew=2
    wshaft=0; dshaft=1.8; pinxoffset=0; pinyoffset=(hbody-2*rmy)/2.0
    makePotentiometerHorizontal(style="trimmer", class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_trv,height3d=height3d, screwzpos=screwzpos)

    class_name="ACP CA9-H2,5"; add_description="http://www.acptechnologies.com/wp-content/uploads/2017/05/02-ACP-CA9-CE9.pdf"
    pins = 3; rmx=2.5; rmy=2.5; ddrill=1.3; wbody=-4.8; hbody=9.8; dbody=0; height3d = 12; screwzpos = 7; wscrew=-wbody; dscrew=3
    wshaft=0; dshaft=2.1; pinxoffset=0; pinyoffset=(hbody-2*rmy)/2.0
    #name_additions = ["Px{0:1.1f}mm_Py{1:1.1f}mm".format(rmx, 2 * rmy)]
    makePotentiometerHorizontal(style="trimmer", class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_trv,height3d=height3d, screwzpos=screwzpos)
    class_name="ACP CA9-H3,8"
    rmx=3.8; height3d = 12
    #name_additions = ["Px{0:1.1f}mm_Py{1:1.1f}mm".format(rmx, 2 * rmy)]
    makePotentiometerHorizontal(style="trimmer", class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_trv,height3d=height3d, screwzpos=screwzpos)
    class_name="ACP CA9-H5"
    rmx=5; height3d = 12
    #name_additions = ["Px{0:1.1f}mm_Py{1:1.1f}mm".format(rmx, 2 * rmy)]
    makePotentiometerHorizontal(style="trimmer", class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_trv,height3d=height3d, screwzpos=screwzpos)
    class_name="ACP CA9-V10"
    rmx=10; dbody=0; voffsetx=0; vwbody=10; vpinyoffset=(hbody-2*rmy)/2.0; c_offsetx=vwbody/2.0; c_offsety=hbody/2.0; c_ddrill=4; height3d=7.2
    #name_additions = ["Px{0:1.1f}mm_Py{1:1.1f}mm".format(rmx, 2 * rmy)]
    makePotentiometerVertical(style="trimmer", shaft_hole=False, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=c_ddrill,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=vpinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_trh,height3d=height3d)
    makePotentiometerVertical(style="trimmer", shaft_hole=True, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=c_ddrill,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=vpinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_trh_bel,height3d=height3d)
    #name_additions=[]
    
    class_name="ACP CA14-H2,5"; add_description="http://www.acptechnologies.com/wp-content/uploads/2017/10/03-ACP-CA14-CE14.pdf"
    pins = 3; rmx=2.5; rmy=5; ddrill=1.3; wbody=-5.0; hbody=14; dbody=0; height3d = 17; screwzpos = 10; wscrew=-wbody; dscrew=6
    wshaft=0; dshaft=5; pinxoffset=0; pinyoffset=(hbody-2*rmy)/2.0
    #name_additions = ["Px{0:1.1f}mm_Py{1:1.1f}mm".format(rmx, 2 * rmy)]
    makePotentiometerHorizontal(style="trimmer", class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_trv,height3d=height3d, screwzpos=screwzpos)
    class_name="ACP CA14-H4"
    rmx=4
    #name_additions = ["Px{0:1.1f}mm_Py{1:1.1f}mm".format(rmx, 2 * rmy)]
    makePotentiometerHorizontal(style="trimmer", class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_trv,height3d=height3d, screwzpos=screwzpos)
    class_name="ACP CA14-H5"
    rmx=5
    #name_additions = ["Px{0:1.1f}mm_Py{1:1.1f}mm".format(rmx, 2 * rmy)]
    makePotentiometerHorizontal(style="trimmer", class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_trv,height3d=height3d, screwzpos=screwzpos)
    class_name="ACP CA14V-15"
    rmx=15; dbody=0; voffsetx=0.5; vwbody=14; vpinyoffset=(hbody-2*rmy)/2.0; c_offsetx=vwbody/2.0; c_offsety=hbody/2.0; c_ddrill=7; height3d=7.2
    #name_additions = ["Px{0:1.1f}mm_Py{1:1.1f}mm".format(rmx, 2 * rmy)]
    makePotentiometerVertical(style="trimmer", shaft_hole=False, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=c_ddrill,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=vpinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_trh,height3d=height3d)
    makePotentiometerVertical(style="trimmer", shaft_hole=True, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=c_ddrill,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=vpinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_trh_bel,height3d=height3d)
    #name_additions=[]
    
    class_name="Bourns 3005"; add_description = "http://www.bourns.com/docs/Product-Datasheets/3005.pdf";
    wbody=19.3; hbody=4.06; pinxoffset=16; pinyoffset=(hbody-2.54)/2.0+2.54; height3d = 7.87; rmx2=-7.62; rmy2=-2.54; rmx3=-12.7; rmy3=0; ddrill=1; dscrew=3; wscrew = 1.52; screwxoffset = 0; screwyoffset = hbody/2.0
    style = "screwleft"; SMD_pads = False; SMD_padsize = []
    makeSpindleTrimmer(shaft_hole=False, class_name=class_name, ddrill=ddrill, wbody=wbody, hbody=hbody, pinxoffset=pinxoffset, pinyoffset=pinyoffset, rmx2=rmx2, rmy2=rmy2, rmx3=rmx3, rmy3=rmy3, dscrew=dscrew, wscrew=wscrew, screwxoffset=screwxoffset, screwyoffset=screwyoffset, style=style, SMD_pads=SMD_pads, SMD_padsize=SMD_padsize, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_tsl, height3d=height3d)
    
    class_name="Vishay 43"; add_description = "http://www.vishay.com/docs/57026/43.pdf";
    wbody=19.0; hbody=4.8; pinxoffset=16; pinyoffset=(hbody-2.54)/2.0+2.54; height3d = 6.35; rmx2=-7.62; rmy2=-2.54; rmx3=-12.7; rmy3=0; ddrill=1; dscrew=2.36; wscrew = 1.52; screwxoffset = 0; screwyoffset = hbody/2.0
    style = "screwleft"; SMD_pads = False; SMD_padsize = []
    makeSpindleTrimmer(shaft_hole=False, class_name=class_name, ddrill=ddrill, wbody=wbody, hbody=hbody, pinxoffset=pinxoffset, pinyoffset=pinyoffset, rmx2=rmx2, rmy2=rmy2, rmx3=rmx3, rmy3=rmy3, dscrew=dscrew, wscrew=wscrew, screwxoffset=screwxoffset, screwyoffset=screwyoffset, style=style, SMD_pads=SMD_pads, SMD_padsize=SMD_padsize, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_tsl, height3d=height3d)

    class_name="Bourns 3006P"; add_description = "https://www.bourns.com/docs/Product-Datasheets/3006.pdf";
    wbody=19.05; hbody=4.83; pinxoffset=16; pinyoffset=(hbody-2.54)/2.0+2.54; height3d = 6.35; rmx2=-7.62; rmy2=-2.54; rmx3=-12.7; rmy3=0; ddrill=1; dscrew=2.36; wscrew = 1.52; screwxoffset = 0; screwyoffset = hbody/2.0
    style = "screwleft"; SMD_pads = False; SMD_padsize = []
    makeSpindleTrimmer(shaft_hole=False, class_name=class_name, ddrill=ddrill, wbody=wbody, hbody=hbody, pinxoffset=pinxoffset, pinyoffset=pinyoffset, rmx2=rmx2, rmy2=rmy2, rmx3=rmx3, rmy3=rmy3, dscrew=dscrew, wscrew=wscrew, screwxoffset=screwxoffset, screwyoffset=screwyoffset, style=style, SMD_pads=SMD_pads, SMD_padsize=SMD_padsize, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_tsl, height3d=height3d)
    class_name="Bourns 3006W"
    wbody=19.05; hbody=4.83; pinxoffset=16; pinyoffset=4.83+0.15; height3d = 6.35; rmx2=-7.62; rmy2=-5.06; rmx3=-12.7; rmy3=0; ddrill=1; dscrew=2.36; wscrew = 1.52; screwxoffset = 0; screwyoffset = hbody/2.0
    style = "screwleft"; SMD_pads = False; SMD_padsize = []
    makeSpindleTrimmer(shaft_hole=False, class_name=class_name, ddrill=ddrill, wbody=wbody, hbody=hbody, pinxoffset=pinxoffset, pinyoffset=pinyoffset, rmx2=rmx2, rmy2=rmy2, rmx3=rmx3, rmy3=rmy3, dscrew=dscrew, wscrew=wscrew, screwxoffset=screwxoffset, screwyoffset=screwyoffset, style=style, SMD_pads=SMD_pads, SMD_padsize=SMD_padsize, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_tsl, height3d=height3d)
    class_name="Bourns 3006Y"
    wbody=19.05; hbody=4.83; pinxoffset=18.42; pinyoffset=(hbody-2.54)/2.0+2.54; height3d = 6.35; rmx2=-(17.78-7.62); rmy2=-2.54; rmx3=-17.78; rmy3=0; ddrill=1; dscrew=2.36; wscrew = 1.52; screwxoffset = 0; screwyoffset = hbody/2.0
    style = "screwleft"; SMD_pads = False; SMD_padsize = []
    makeSpindleTrimmer(shaft_hole=False, class_name=class_name, ddrill=ddrill, wbody=wbody, hbody=hbody, pinxoffset=pinxoffset, pinyoffset=pinyoffset, rmx2=rmx2, rmy2=rmy2, rmx3=rmx3, rmy3=rmy3, dscrew=dscrew, wscrew=wscrew, screwxoffset=screwxoffset, screwyoffset=screwyoffset, style=style, SMD_pads=SMD_pads, SMD_padsize=SMD_padsize, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_tsl, height3d=height3d)

    class_name="Bourns 3009P"; add_description = "http://www.bourns.com/docs/Product-Datasheets/3009.pdf"
    wbody=19.05; hbody=4.83; pinxoffset=16; pinyoffset=(hbody-2.54)/2.0+2.54; height3d = 8.98; rmx2=-7.62; rmy2=-2.54; rmx3=-12.7; rmy3=0; ddrill=1; dscrew=2.36; wscrew = 1.52; screwxoffset = 0; screwyoffset = hbody/2.0
    style = "screwleft"; SMD_pads = False; SMD_padsize = []
    makeSpindleTrimmer(shaft_hole=False, class_name=class_name, ddrill=ddrill, wbody=wbody, hbody=hbody, pinxoffset=pinxoffset, pinyoffset=pinyoffset, rmx2=rmx2, rmy2=rmy2, rmx3=rmx3, rmy3=rmy3, dscrew=dscrew, wscrew=wscrew, screwxoffset=screwxoffset, screwyoffset=screwyoffset, style=style, SMD_pads=SMD_pads, SMD_padsize=SMD_padsize, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_tsl, height3d=height3d)
    class_name="Bourns 3009Y"
    wbody=19.05; hbody=4.83; pinxoffset=18.42; pinyoffset=(hbody-2.54)/2.0+2.54; height3d = 8.98; rmx2=-(17.78-7.62); rmy2=-2.54; rmx3=-17.78; rmy3=0; ddrill=1; dscrew=2.36; wscrew = 1.52; screwxoffset = 0; screwyoffset = hbody/2.0
    style = "screwleft"; SMD_pads = False; SMD_padsize = []
    makeSpindleTrimmer(shaft_hole=False, class_name=class_name, ddrill=ddrill, wbody=wbody, hbody=hbody, pinxoffset=pinxoffset, pinyoffset=pinyoffset, rmx2=rmx2, rmy2=rmy2, rmx3=rmx3, rmy3=rmy3, dscrew=dscrew, wscrew=wscrew, screwxoffset=screwxoffset, screwyoffset=screwyoffset, style=style, SMD_pads=SMD_pads, SMD_padsize=SMD_padsize, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_tsl, height3d=height3d)

    class_name="Bourns 3296W"; add_description = "https://www.bourns.com/pdfs/3296.pdf";
    wbody=9.53; hbody=4.83; pinxoffset=(wbody-5.08)/2.0+5.08; pinyoffset=2.41; height3d = 10.03; rmx2=-2.54; rmy2=0; rmx3=-5.08; rmy3=0; ddrill=0.8; dscrew=2.19; wscrew = dscrew; screwxoffset = wbody-1.27; screwyoffset = hbody-1.27
    style = "screwtop"; SMD_pads = False; SMD_padsize = []
    makeSpindleTrimmer(shaft_hole=False, class_name=class_name, ddrill=ddrill, wbody=wbody, hbody=hbody, pinxoffset=pinxoffset, pinyoffset=pinyoffset, rmx2=rmx2, rmy2=rmy2, rmx3=rmx3, rmy3=rmy3, dscrew=dscrew, wscrew=wscrew, screwxoffset=screwxoffset, screwyoffset=screwyoffset, style=style, SMD_pads=SMD_pads, SMD_padsize=SMD_padsize, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_tst, height3d=height3d)
    class_name="Bourns 3296X"
    wbody=9.53; hbody=4.83; pinxoffset=(wbody-5.08)/2.0+5.08; pinyoffset=2.41; height3d = 10.03; rmx2=-2.54; rmy2=0; rmx3=-5.08; rmy3=0; ddrill=0.8; dscrew = 2.19; wscrew = 1.52; screwxoffset = 0; screwyoffset = hbody-1.27
    style = "screwleft"; SMD_pads = False; SMD_padsize = []
    makeSpindleTrimmer(shaft_hole=False, class_name=class_name, ddrill=ddrill, wbody=wbody, hbody=hbody, pinxoffset=pinxoffset, pinyoffset=pinyoffset, rmx2=rmx2, rmy2=rmy2, rmx3=rmx3, rmy3=rmy3, dscrew=dscrew, wscrew=wscrew, screwxoffset=screwxoffset, screwyoffset=screwyoffset, style=style, SMD_pads=SMD_pads, SMD_padsize=SMD_padsize, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_tsl, height3d=height3d)
    class_name="Bourns 3296Y"
    wbody=9.53; hbody=4.83; pinxoffset=(wbody-5.08)/2.0+5.08; pinyoffset=1.14; height3d = 10.03; rmx2=-2.54; rmy2=2.54; rmx3=-5.08; rmy3=0; ddrill=0.8; dscrew=2.19; wscrew = dscrew; screwxoffset = wbody-1.27; screwyoffset = hbody-1.27
    style = "screwtop"; SMD_pads = False; SMD_padsize = []
    makeSpindleTrimmer(shaft_hole=False, class_name=class_name, ddrill=ddrill, wbody=wbody, hbody=hbody, pinxoffset=pinxoffset, pinyoffset=pinyoffset, rmx2=rmx2, rmy2=rmy2, rmx3=rmx3, rmy3=rmy3, dscrew=dscrew, wscrew=wscrew, screwxoffset=screwxoffset, screwyoffset=screwyoffset, style=style, SMD_pads=SMD_pads, SMD_padsize=SMD_padsize, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_tst, height3d=height3d)
    class_name="Bourns 3296Z"
    wbody=9.53; hbody=4.83; pinxoffset=(wbody-5.08)/2.0+5.08; pinyoffset=hbody-1.14-2.54; height3d = 10.03; rmx2=-2.54; rmy2=2.54; rmx3=-5.08; rmy3=0; ddrill=0.8; dscrew=2.19; wscrew = 1.52; screwxoffset = 0; screwyoffset = hbody-1.27
    style = "screwleft"; SMD_pads = False; SMD_padsize = []
    makeSpindleTrimmer(class_name=class_name, ddrill=ddrill, wbody=wbody, hbody=hbody, pinxoffset=pinxoffset, pinyoffset=pinyoffset, rmx2=rmx2, rmy2=rmy2, rmx3=rmx3, rmy3=rmy3, dscrew=dscrew, wscrew=wscrew, screwxoffset=screwxoffset, screwyoffset=screwyoffset, style=style, SMD_pads=SMD_pads, SMD_padsize=SMD_padsize, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_tsl, height3d=height3d)
    class_name="Bourns 3296P"
    wbody=10.03; hbody=9.53; pinxoffset=wbody/2.0; pinyoffset=(hbody-5.08)/2.0; height3d = 4.83; rmx2=-2.54; rmy2=2.54; rmx3=0; rmy3=5.08; ddrill=0.8; dscrew=2.19; wscrew = 1.52; screwxoffset = 0; screwyoffset = 1.27
    style = "screwleft"; SMD_pads = False; SMD_padsize = []
    makeSpindleTrimmer(shaft_hole=False, class_name=class_name, ddrill=ddrill, wbody=wbody, hbody=hbody, pinxoffset=pinxoffset, pinyoffset=pinyoffset, rmx2=rmx2, rmy2=rmy2, rmx3=rmx3, rmy3=rmy3, dscrew=dscrew, wscrew=wscrew, screwxoffset=screwxoffset, screwyoffset=screwyoffset, style=style, SMD_pads=SMD_pads, SMD_padsize=SMD_padsize, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_tsl, height3d=height3d)

    class_name="Bourns 3299W"; add_description = "https://www.bourns.com/pdfs/3299.pdf";
    wbody=9.53; hbody=6.10; pinxoffset=(wbody-5.08)/2.0+5.08; pinyoffset=1.91; height3d = 10.03; rmx2=-2.54; rmy2=0; rmx3=-5.08; rmy3=0; ddrill=0.8; dscrew=2.19; wscrew = dscrew; screwxoffset = wbody-1.27; screwyoffset = hbody-1.27
    style = "screwtop"; SMD_pads = False; SMD_padsize = []
    makeSpindleTrimmer(shaft_hole=False, class_name=class_name, ddrill=ddrill, wbody=wbody, hbody=hbody, pinxoffset=pinxoffset, pinyoffset=pinyoffset, rmx2=rmx2, rmy2=rmy2, rmx3=rmx3, rmy3=rmy3, dscrew=dscrew, wscrew=wscrew, screwxoffset=screwxoffset, screwyoffset=screwyoffset, style=style, SMD_pads=SMD_pads, SMD_padsize=SMD_padsize, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_tst, height3d=height3d)
    class_name="Bourns 3299X"
    wbody=9.53; hbody=6.10; pinxoffset=(wbody-5.08)/2.0+5.08; pinyoffset=1.91; height3d = 10.03; rmx2=-2.54; rmy2=0; rmx3=-5.08; rmy3=0; ddrill=0.8; dscrew = 2.19; wscrew = 1.52; screwxoffset = 0; screwyoffset = hbody-1.27
    style = "screwleft"; SMD_pads = False; SMD_padsize = []
    makeSpindleTrimmer(shaft_hole=False, class_name=class_name, ddrill=ddrill, wbody=wbody, hbody=hbody, pinxoffset=pinxoffset, pinyoffset=pinyoffset, rmx2=rmx2, rmy2=rmy2, rmx3=rmx3, rmy3=rmy3, dscrew=dscrew, wscrew=wscrew, screwxoffset=screwxoffset, screwyoffset=screwyoffset, style=style, SMD_pads=SMD_pads, SMD_padsize=SMD_padsize, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_tsl, height3d=height3d)
    class_name="Bourns 3299Y"
    wbody=9.53; hbody=6.10; pinxoffset=(wbody-5.08)/2.0+5.08; pinyoffset=1.91; height3d = 10.03; rmx2=-2.54; rmy2=2.54; rmx3=-5.08; rmy3=0; ddrill=0.8; dscrew=2.19; wscrew = dscrew; screwxoffset = wbody-1.27; screwyoffset = hbody-1.27
    style = "screwtop"; SMD_pads = False; SMD_padsize = []
    makeSpindleTrimmer(shaft_hole=False, class_name=class_name, ddrill=ddrill, wbody=wbody, hbody=hbody, pinxoffset=pinxoffset, pinyoffset=pinyoffset, rmx2=rmx2, rmy2=rmy2, rmx3=rmx3, rmy3=rmy3, dscrew=dscrew, wscrew=wscrew, screwxoffset=screwxoffset, screwyoffset=screwyoffset, style=style, SMD_pads=SMD_pads, SMD_padsize=SMD_padsize, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_tst, height3d=height3d)
    class_name="Bourns 3299Z"
    wbody=9.53; hbody=6.10; pinxoffset=(wbody-5.08)/2.0+5.08; pinyoffset=1.91; height3d = 10.03; rmx2=-2.54; rmy2=2.54; rmx3=-5.08; rmy3=0; ddrill=0.8; dscrew=2.19; wscrew = 1.52; screwxoffset = 0; screwyoffset = hbody-1.27
    style = "screwleft"; SMD_pads = False; SMD_padsize = []
    makeSpindleTrimmer(shaft_hole=False, class_name=class_name, ddrill=ddrill, wbody=wbody, hbody=hbody, pinxoffset=pinxoffset, pinyoffset=pinyoffset, rmx2=rmx2, rmy2=rmy2, rmx3=rmx3, rmy3=rmy3, dscrew=dscrew, wscrew=wscrew, screwxoffset=screwxoffset, screwyoffset=screwyoffset, style=style, SMD_pads=SMD_pads, SMD_padsize=SMD_padsize, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_tsl, height3d=height3d)
    class_name="Bourns 3299P"
    wbody=10.03; hbody=9.53; pinxoffset=wbody/2.0; pinyoffset=(hbody-5.08)/2.0; height3d = 6.10; rmx2=-2.54; rmy2=2.54; rmx3=0; rmy3=5.08; ddrill=0.8; dscrew=2.19; wscrew = 1.52; screwxoffset = 0; screwyoffset = 1.27
    style = "screwleft"; SMD_pads = False; SMD_padsize = []
    makeSpindleTrimmer(shaft_hole=False, class_name=class_name, ddrill=ddrill, wbody=wbody, hbody=hbody, pinxoffset=pinxoffset, pinyoffset=pinyoffset, rmx2=rmx2, rmy2=rmy2, rmx3=rmx3, rmy3=rmy3, dscrew=dscrew, wscrew=wscrew, screwxoffset=screwxoffset, screwyoffset=screwyoffset, style=style, SMD_pads=SMD_pads, SMD_padsize=SMD_padsize, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_tsl, height3d=height3d)

    class_name="Bourns 3266Y"; add_description = "https://www.bourns.com/docs/Product-Datasheets/3266.pdf";
    wbody=6.71; hbody=4.5; pinxoffset=(wbody-5.08)/2.0+5.08; pinyoffset=2.16; height3d = 6.71; rmx2=-2.54; rmy2=0; rmx3=-5.08; rmy3=0; ddrill=0.8; dscrew=1.78; wscrew = dscrew; screwxoffset = wbody-1.22; screwyoffset = hbody-1.27
    style = "screwtop"; SMD_pads = False; SMD_padsize = []
    makeSpindleTrimmer(shaft_hole=False, class_name=class_name, ddrill=ddrill, wbody=wbody, hbody=hbody, pinxoffset=pinxoffset, pinyoffset=pinyoffset, rmx2=rmx2, rmy2=rmy2, rmx3=rmx3, rmy3=rmy3, dscrew=dscrew, wscrew=wscrew, screwxoffset=screwxoffset, screwyoffset=screwyoffset, style=style, SMD_pads=SMD_pads, SMD_padsize=SMD_padsize, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_tst, height3d=height3d)
    class_name="Bourns 3266Z"
    wbody=6.71; hbody=4.5; pinxoffset=(wbody-5.08)/2.0+5.08; pinyoffset=2.16; height3d = 6.71; rmx2=-2.54; rmy2=0; rmx3=-5.08; rmy3=0; ddrill=0.8; dscrew = 1.78; wscrew = 1.52; screwxoffset = 0; screwyoffset = hbody-1.27
    style = "screwleft"; SMD_pads = False; SMD_padsize = []
    makeSpindleTrimmer(shaft_hole=False, class_name=class_name, ddrill=ddrill, wbody=wbody, hbody=hbody, pinxoffset=pinxoffset, pinyoffset=pinyoffset, rmx2=rmx2, rmy2=rmy2, rmx3=rmx3, rmy3=rmy3, dscrew=dscrew, wscrew=wscrew, screwxoffset=screwxoffset, screwyoffset=screwyoffset, style=style, SMD_pads=SMD_pads, SMD_padsize=SMD_padsize, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_tsl, height3d=height3d)
    class_name="Bourns 3266W"
    wbody=6.71; hbody=4.5; pinxoffset=(wbody-5.08)/2.0+5.08; pinyoffset=1.02; height3d = 6.71; rmx2=-2.54; rmy2=2.54; rmx3=-5.08; rmy3=0; ddrill=0.8; dscrew=1.78; wscrew = dscrew; screwxoffset = wbody-1.27; screwyoffset = hbody-1.27
    style = "screwtop"; SMD_pads = False; SMD_padsize = []
    makeSpindleTrimmer(shaft_hole=False, class_name=class_name, ddrill=ddrill, wbody=wbody, hbody=hbody, pinxoffset=pinxoffset, pinyoffset=pinyoffset, rmx2=rmx2, rmy2=rmy2, rmx3=rmx3, rmy3=rmy3, dscrew=dscrew, wscrew=wscrew, screwxoffset=screwxoffset, screwyoffset=screwyoffset, style=style, SMD_pads=SMD_pads, SMD_padsize=SMD_padsize, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_tst, height3d=height3d)
    class_name="Bourns 3266X"
    wbody=6.71; hbody=4.5; pinxoffset=(wbody-5.08)/2.0+5.08; pinyoffset=1.02; height3d = 6.71; rmx2=-2.54; rmy2=2.54; rmx3=-5.08; rmy3=0; ddrill=0.8; dscrew=1.78; wscrew = 1.52; screwxoffset = 0; screwyoffset = hbody-1.27
    style = "screwleft"; SMD_pads = False; SMD_padsize = []
    makeSpindleTrimmer(shaft_hole=False, class_name=class_name, ddrill=ddrill, wbody=wbody, hbody=hbody, pinxoffset=pinxoffset, pinyoffset=pinyoffset, rmx2=rmx2, rmy2=rmy2, rmx3=rmx3, rmy3=rmy3, dscrew=dscrew, wscrew=wscrew, screwxoffset=screwxoffset, screwyoffset=screwyoffset, style=style, SMD_pads=SMD_pads, SMD_padsize=SMD_padsize, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_tsl, height3d=height3d)
    class_name="Bourns 3266P"
    wbody=6.71; hbody=6.71; pinxoffset=wbody/2.0; pinyoffset=(hbody-5.08)/2.0; height3d = 4.5; rmx2=-2.54; rmy2=2.54; rmx3=0; rmy3=5.08; ddrill=0.8; dscrew=1.78; wscrew = 1.52; screwxoffset = 0; screwyoffset = 1.27
    style = "screwleft"; SMD_pads = False; SMD_padsize = []
    makeSpindleTrimmer(shaft_hole=False, class_name=class_name, ddrill=ddrill, wbody=wbody, hbody=hbody, pinxoffset=pinxoffset, pinyoffset=pinyoffset, rmx2=rmx2, rmy2=rmy2, rmx3=rmx3, rmy3=rmy3, dscrew=dscrew, wscrew=wscrew, screwxoffset=screwxoffset, screwyoffset=screwyoffset, style=style, SMD_pads=SMD_pads, SMD_padsize=SMD_padsize, specialtags=[], add_description=add_description, name_additions=[], script3d=script3d_tsl, height3d=height3d)    
