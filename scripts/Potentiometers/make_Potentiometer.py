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
    script3d_pv="pots_ver.py"
    with open(script3d_pv, "w") as myfile:
        myfile.write("#\n# SCRIPT to generate 3D models\n#\n\n")
    script3d_trv="trim_round_ver.py"
    with open(script3d_trv, "w") as myfile:
        myfile.write("#\n# SCRIPT to generate 3D models\n#\n\n")
    script3d_ph_bel="pots_hor_below.py"
    with open(script3d_ph_bel, "w") as myfile:
        myfile.write("#\n# SCRIPT to generate 3D models\n#\n\n")
    script3d_ph="pots_hor.py"
    with open(script3d_ph, "w") as myfile:
        myfile.write("#\n# SCRIPT to generate 3D models\n#\n\n")

    classname = "Potentiometer"
    lib_name = "Potentiometers"
    R_POW = 0
    specialtags=[]
    name_additions=[]

    footprint_name="Potentiometer_Omeg_PC16PU"
    class_name="Omeg PC16PU"
    pins = 3; rmx=5.0; rmy=5.; ddrill=1.3
    wbody=9.3; hbody=16.9; height3d = 21; screwzpos = 12.5
    wscrew=6; dscrew=7
    wshaft=50-wscrew; dshaft=4; pinxoffset=6.3; pinyoffset=(hbody-2*rmy)/2
    add_description="http://www.omeg.co.uk/pc6bubrc.htm"
    makePotentiometerVertical(footprint_name=footprint_name, class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_pv,height3d=height3d, screwzpos=screwzpos)
    voffsetx=1.75; dbody=16.9; vwbody=5; vpinyoffset=(hbody-2*rmy)/2; c_offsety=dbody/2; c_offsetx=10.8
    makePotentiometerHorizontal(mount_below=True, footprint_name=footprint_name, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=dscrew+0.5,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_ph_bel,height3d=height3d)
    makePotentiometerHorizontal(mount_below=False, footprint_name=footprint_name, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=dscrew+0.5,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_ph,height3d=height3d)

    
    footprint_name="Potentiometer_VishaySpectrol_248GJ_249GJ"
    class_name="Vishay/Spectrol 248GJ/249GJ Single"
    pins = 3; rmx=7.62; rmy=2.54; ddrill=1
    wbody=7.6; hbody=12.5; height3d = 13.1; screwzpos = 12.7/2+0.6
    wscrew=9.5; dscrew=3/8*25.4
    wshaft=22.22-wscrew; dshaft=7.6; pinxoffset=5.08; pinyoffset=(hbody-2*rmy)/2
    add_description="http://www.vishay.com/docs/57054/248249.pdf"
    makePotentiometerVertical(footprint_name=footprint_name, class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_pv,height3d=height3d, screwzpos=screwzpos)
    voffsetx=0.75; dbody=0; vwbody=12.7; vpinyoffset=(hbody-2*rmy)/2; c_offsety=hbody/2; c_offsetx=vwbody/2
    makePotentiometerHorizontal(mount_below=True, footprint_name=footprint_name, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=dscrew+0.5,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_ph_bel,height3d=height3d)
    makePotentiometerHorizontal(mount_below=False, footprint_name=footprint_name, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=dscrew+0.5,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_ph,height3d=height3d)
    footprint_name="Potentiometer_VishaySpectrol_248GH_249GH"
    class_name="Vishay/Spectrol 248GH/249GH Single"
    wscrew=9.5; dscrew=0.25*25.4
    wshaft=19.05-wscrew; dshaft=3.18; pinxoffset=5.08; pinyoffset=(hbody-2*rmy)/2
    add_description="http://www.vishay.com/docs/57054/248249.pdf"
    makePotentiometerVertical(footprint_name=footprint_name, class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_pv,height3d=height3d, screwzpos=screwzpos)

    footprint_name="Potentiometer_VishaySpectrol_148_149_Single"
    class_name="Vishay/Spectrol 148/149 Single"
    pins = 3; rmx=7.62; rmy=2.54; ddrill=1
    wbody=8.83; hbody=12.5; height3d = 13.1; screwzpos = 12.5/2+0.6
    wscrew=6.35; dscrew=0.25*25.4
    wshaft=12.8-wscrew; dshaft=3.17; pinxoffset=5.08; pinyoffset=(hbody-2*rmy)/2
    add_description="http://www.vishay.com/docs/57040/148149.pdf"
    makePotentiometerVertical(footprint_name=footprint_name, class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_pv,height3d=height3d, screwzpos=screwzpos)
    voffsetx=0.75; dbody=0; vwbody=12.5; vpinyoffset=(hbody-2*rmy)/2; c_offsety=hbody/2; c_offsetx=vwbody/2
    makePotentiometerHorizontal(mount_below=True, footprint_name=footprint_name, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=dscrew+0.5,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_ph_bel,height3d=height3d)
    makePotentiometerHorizontal(mount_below=False, footprint_name=footprint_name, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=dscrew+0.5,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_ph,height3d=height3d)
    footprint_name="Potentiometer_VishaySpectrol_148A_149A_Single"
    class_name="Vishay/Spectrol 148A/149A Single with mounting plates"
    wbody = 6.35 + 3.85 + 1.52 + 0.5;
    makePotentiometerVertical(mh_ddrill=1.3, mh_count=4, mh_rmx=3.85+6.35, mh_rmy=10.16, mh_xoffset=3.85, mh_yoffset=(10.16-2*rmy)/2, footprint_name=footprint_name, class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_pv,height3d=height3d, screwzpos=screwzpos)
    footprint_name="Potentiometer_VishaySpectrol_148_149_Double"
    class_name="Vishay/Spectrol 148/149 Double"
    pins = 6;  wbody=16.45; wscrew=7;
    makePotentiometerVertical(footprint_name=footprint_name, class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_pv,height3d=height3d, screwzpos=screwzpos)
    footprint_name="Potentiometer_VishaySpectrol_148A_149A_Double"
    class_name="Vishay/Spectrol 148A/149A Double with mounting plates"
    wbody = 6.35+7.62+3.85+1.52+0.5;
    makePotentiometerVertical(mh_ddrill=1.3, mh_count=4, mh_rmx=3.85+7.62+6.35, mh_rmy=10.16, mh_xoffset=3.85, mh_yoffset=(10.16-2*rmy)/2, footprint_name=footprint_name, class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_pv,height3d=height3d, screwzpos=screwzpos)

    footprint_name="Potentiometer_Piher_PC-16_Single"
    class_name="Piher PC-16 Single"
    pins = 3; rmx=7.5; rmy=5.0; ddrill=1.3
    wbody=8; hbody=16; height3d = 20.5; screwzpos = 12.5
    wscrew=9; dscrew=10
    wshaft=25-wscrew; dshaft=6; pinxoffset=6.5; pinyoffset=(hbody-2*rmy)/2
    add_description="http://www.piher-nacesa.com/pdf/20-PC16v03.pdf"
    makePotentiometerVertical(footprint_name=footprint_name, class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_pv,height3d=height3d, screwzpos=screwzpos)
    voffsetx = 0.5; dbody = 0; vwbody = 18; vpinyoffset = (hbody - 2 * rmy) / 2; c_offsetx = 10; c_offsety = hbody / 2
    makePotentiometerHorizontal(mount_below=True, footprint_name=footprint_name, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=dscrew+0.5,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_ph_bel,height3d=height3d)
    makePotentiometerHorizontal(mount_below=False, footprint_name=footprint_name, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=dscrew+0.5,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_ph,height3d=height3d)
    footprint_name="Potentiometer_Piher_PC-16SV_Single"
    class_name="Piher PC-16SV Single"
    voffsetx=0.5; dbody=0; vwbody=18; vpinyoffset=(hbody-2*rmy)/2; c_offsetx=10; c_offsety=hbody/2
    makePotentiometerHorizontal(mh_ddrill=1.3, mh_count=2, mh_rmx=0, mh_rmy=10.0, mh_xoffset=15, mh_yoffset=(10-2*rmy)/2, mount_below=False, footprint_name=footprint_name, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=dscrew+0.5,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_ph_bel,height3d=height3d)
    footprint_name="Potentiometer_Piher_PC-16_Double"
    class_name="Piher PC-16 Double"
    pins = 6;  wbody=16;
    makePotentiometerVertical(footprint_name=footprint_name, class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_pv,height3d=height3d, screwzpos=screwzpos)
    footprint_name="Potentiometer_Piher_PC-16_Triple"
    class_name="Piher PC-16 Triple"
    pins = 9;  wbody=24;
    makePotentiometerVertical(footprint_name=footprint_name, class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_pv,height3d=height3d, screwzpos=screwzpos)

    footprint_name="Potentiometer_Piher_T16H_Single"
    class_name="Piher T16H Single"
    pins = 3; rmx=7.5; rmy=5.0; ddrill=1.3
    wbody=7.5; hbody=16; height3d = 21; screwzpos = 12.5
    wscrew=5; dscrew=7
    wshaft=15-wscrew; dshaft=4; pinxoffset=1.5; pinyoffset=(hbody-2*rmy)/2
    add_description="http://www.piher-nacesa.com/pdf/22-T16v03.pdf"
    makePotentiometerVertical(footprint_name=footprint_name, class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_pv,height3d=height3d, screwzpos=screwzpos)
    footprint_name="Potentiometer_Piher_T16L_Single"
    class_name="Piher T16L Single"
    voffsetx=-0.5; dbody=16; vwbody=3; vpinyoffset=(hbody-2*rmy)/2; c_offsetx=10.5; c_offsety=hbody/2
    makePotentiometerHorizontal(mount_below=True, footprint_name=footprint_name, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=dscrew+0.5,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_ph_bel,height3d=height3d)
    footprint_name="Potentiometer_Piher_T16H_Double"
    class_name="Piher T16H Double"
    pins = 6;  wbody=15;
    makePotentiometerVertical(footprint_name=footprint_name, class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_pv,height3d=height3d, screwzpos=screwzpos)
 
    footprint_name="Potentiometer_Alps_RK163_Single"
    class_name="Alps RK163 Single"
    pins = 3; rmx=5.0; rmy=5.0; ddrill=1.3
    wbody=10.5; hbody=17.9; height3d = 21; screwzpos = 12.5
    wscrew=5; dscrew=7
    wshaft=15-wscrew; dshaft=6; pinxoffset=3.8; pinyoffset=(hbody-2*rmy)/2
    add_description="http://www.alps.com/prod/info/E/PDF/Potentiometer/MetalShaft/RK163/RK163.PDF"
    makePotentiometerVertical(footprint_name=footprint_name, class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_pv,height3d=height3d, screwzpos=screwzpos)
    footprint_name="Potentiometer_Alps_RK163_Double"
    class_name="Alps RK163 Double"
    pins = 6;  wbody=12.1; wscrew=7;
    makePotentiometerVertical(footprint_name=footprint_name, class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_pv,height3d=height3d, screwzpos=screwzpos)
    
    footprint_name="Potentiometer_Alps_RK097_Single"
    class_name="Alps RK097 Single"
    pins = 3; rmx=2.5; rmy=2.5; ddrill=1
    wbody=7.05; hbody=9.5; height3d = 6.5+0.25+4.85; screwzpos = 6.5+0.25
    wscrew=5; dscrew=7
    wshaft=15-wscrew; dshaft=6; pinxoffset=5; pinyoffset=(hbody-2*rmy)/2
    add_description="http://www.alps.com/prod/info/E/HTML/Potentiometer/RotaryPotentiometers/RK097/RK097111080J.html"
    makePotentiometerVertical(footprint_name=footprint_name, class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_pv,height3d=height3d, screwzpos=screwzpos)
    footprint_name="Potentiometer_Alps_RK097_Double"
    class_name="Alps RK097 Double"
    pins = 6;  wbody=9.55;
    add_description = "http://www.alps.com/prod/info/E/HTML/Potentiometer/RotaryPotentiometers/RK097/RK09712100AV.html"
    makePotentiometerVertical(footprint_name=footprint_name, class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_pv,height3d=height3d, screwzpos=screwzpos)

    footprint_name="Potentiometer_Bourns_PTV09A-2"
    class_name="Bourns PTV09A-2 Single with mounting sleve Single"
    pins = 3; rmx=2.5; rmy=2.5; ddrill=1
    wbody=5; hbody=9.7; height3d = 10+5.5; screwzpos = 10
    wscrew=0.8; dscrew=6.8
    wshaft=15-wbody-wscrew; dshaft=6; pinxoffset=3.5; pinyoffset=(hbody-2*rmy)/2
    add_description="http://www.bourns.com/docs/Product-Datasheets/ptv09.pdf"
    makePotentiometerVertical(mh_ddrill=2.3, mh_count=2, mh_rmx=0, mh_rmy=10, mh_xoffset=-3.3, mh_yoffset=(10-2*rmy)/2, footprint_name=footprint_name, class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_pv,height3d=height3d, screwzpos=screwzpos)
    footprint_name="Potentiometer_Bourns_PTV09A-1"
    class_name="Bourns PTV09A-1 with mounting sleve Single"
    voffsetx=1; dbody=0; vwbody=12; vpinyoffset=(hbody-2*rmy)/2; c_offsetx=6.5; c_offsety=hbody/2
    makePotentiometerHorizontal(mh_ddrill=2, mh_count=2, mh_rmx=0, mh_rmy=8.8, mh_xoffset=7, mh_yoffset=(8.8-2*rmy)/2, mount_below=False, footprint_name=footprint_name, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=dscrew+0.5,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_ph_bel,height3d=height3d)
    
    footprint_name="Potentiometer_Bourns_PRS11S"
    class_name="Bourns PRS11S Single"
    pins = 5; rmx=-16.5; rmy=2.5; ddrill=1
    wbody=13; hbody=11.7; height3d = 7.2
    wscrew=4.3; dscrew=6.8
    wshaft=20-wbody-wscrew; dshaft=6; pinxoffset=3.5; pinyoffset=(hbody-2*rmy)/2
    add_description="http://www.bourns.com/docs/Product-Datasheets/prs11s.pdf?sfvrsn=2"
    voffsetx=3.5/2; dbody=0; vwbody=13; vpinyoffset=(hbody-2*rmy)/2; c_offsetx=6.5; c_offsety=hbody/2
    makePotentiometerHorizontal(SMD_pads=True, SMD_padsize=[4,2], mh_ddrill=1.5, mh_count=2, mh_rmx=0, mh_rmy=11.3, mh_xoffset=8.5, mh_yoffset=(11.3-2*rmy)/2, mh_nopads=True, mount_below=False, footprint_name=footprint_name, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=dscrew+0.5,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_ph_bel,height3d=height3d)
    

    footprint_name="Potentiometer_Alps_RK09K"
    class_name="Alps RK09K Single with mounting sleve Single"
    pins = 3; rmx=2.5; rmy=2.5; ddrill=1
    wbody=6.8; hbody=9.8; height3d = 6.5+5.5; screwzpos = 6.5
    wscrew=0.8; dscrew=6.5
    wshaft=15-6.8-wscrew; dshaft=6; pinxoffset=3.4; pinyoffset=(hbody-2*rmy)/2
    add_description="http://www.alps.com/prod/info/E/HTML/Potentiometer/RotaryPotentiometers/RK09K/RK09K1110A2S.html"
    makePotentiometerVertical(mh_ddrill=2.3, mh_count=2, mh_rmx=0, mh_rmy=10, mh_xoffset=-3.3, mh_yoffset=(10-2*rmy)/2, footprint_name=footprint_name, class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_pv,height3d=height3d, screwzpos=screwzpos)
    footprint_name="Potentiometer_Alps_RK09K"
    class_name="Alps RK09K with mounting sleve Single"
    voffsetx=1; dbody=0; vwbody=12; vpinyoffset=(hbody-2*rmy)/2; c_offsetx=6.5; c_offsety=hbody/2
    add_description="http://www.alps.com/prod/info/E/HTML/Potentiometer/RotaryPotentiometers/RK09K/RK09D1130C1B.html"
    makePotentiometerHorizontal(mh_ddrill=2, mh_count=2, mh_rmx=0, mh_rmy=8.8, mh_xoffset=7, mh_yoffset=(8.8-2*rmy)/2, mount_below=False, footprint_name=footprint_name, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=dscrew+0.5,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_ph_bel,height3d=height3d)
    
    
    footprint_name="Potentiometer_Alps_RK09L_Single"
    class_name="Alps RK09L Single"
    pins = 3; rmx=2.5; rmy=2.5; ddrill=1
    wbody=7.45; hbody=12.1; height3d = 6.5+0.25+4.85; screwzpos = 6.5+0.25
    wscrew=5; dscrew=9
    wshaft=15-wscrew; dshaft=6; pinxoffset=5; pinyoffset=(hbody-2*rmy)/2
    add_description="http://www.alps.com/prod/info/E/HTML/Potentiometer/RotaryPotentiometers/RK09L/RK09L1120A2S.html"
    makePotentiometerVertical(mh_ddrill=2.1, mh_count=2, mh_rmx=0, mh_rmy=9.5, mh_xoffset=-4.1, mh_yoffset=(9.5-2*rmy)/2, footprint_name=footprint_name, class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_pv,height3d=height3d, screwzpos=screwzpos)
    footprint_name="Potentiometer_Alps_RK09L_Sleve_Single"
    class_name="Alps RK09L Single"
    add_description="http://www.alps.com/prod/info/E/HTML/Potentiometer/RotaryPotentiometers/RK09L/RK09L1140A5E.html"
    voffsetx=1; dbody=0; vwbody=11.35; vpinyoffset=(hbody-2*rmy)/2; c_offsetx=6.5; c_offsety=hbody/2
    makePotentiometerHorizontal(mh_ddrill=2, mh_count=2, mh_rmx=0, mh_rmy=9.5, mh_xoffset=7.5, mh_yoffset=(9.5-2*rmy)/2, mount_below=False, footprint_name=footprint_name, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=dscrew+0.5,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_ph_bel,height3d=height3d)
    footprint_name="Potentiometer_Alps_RK09L_Double"
    class_name="Alps RK09L Double"
    pins = 6;  wbody=9.14;
    add_description = "http://www.alps.com/prod/info/E/HTML/Potentiometer/RotaryPotentiometers/RK09L/RK09L122002M.html"
    makePotentiometerVertical(mh_ddrill=2.1, mh_count=2, mh_rmx=0, mh_rmy=9.5, mh_xoffset=-5.8, mh_yoffset=(9.5-2*rmy)/2, footprint_name=footprint_name, class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_pv,height3d=height3d, screwzpos=screwzpos)
    footprint_name="Potentiometer_Alps_RK09L_Double"
    class_name="Alps RK09L Double"
    add_description="http://www.alps.com/prod/info/E/HTML/Potentiometer/RotaryPotentiometers/RK09L/RK09L124000Z.html"
    voffsetx=1; dbody=0; vwbody=11.35; vpinyoffset=(hbody-2*rmy)/2; c_offsetx=6.5; c_offsety=hbody/2
    makePotentiometerHorizontal(mh_ddrill=2, mh_count=2, mh_rmx=0, mh_rmy=9.5, mh_xoffset=7.5, mh_yoffset=(9.5-2*rmy)/2, mount_below=False, footprint_name=footprint_name, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=dscrew+0.5,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_ph_bel,height3d=height3d)

    footprint_name="Potentiometer_Alps_RK09Y"
    class_name="Alps RK09Y Single"
    pins = 3; rmx=5.0; rmy=2.5; ddrill=1.0
    wbody=5.4; hbody=9.5; height3d = 6.25+0.25+4.85; screwzpos = 6.25+0.25
    wscrew=5; dscrew=7
    wshaft=12-wscrew; dshaft=5; pinxoffset=3.45; pinyoffset=(hbody-2*rmy)/2
    add_description="http://www.alps.com/prod/info/E/HTML/Potentiometer/RotaryPotentiometers/RK09Y11/RK09Y11L0001.html"
    makePotentiometerVertical(footprint_name=footprint_name, class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_pv,height3d=height3d, screwzpos=screwzpos)

    class_name="Bourns 3339S Single"
    pins = 3; rmx=-2.54; rmy=2.54; ddrill=0.8
    wbody=5.97; hbody=8.13; dbody=0; height3d = 9.53; screwzpos = 5.54;
    wscrew=8-5.97; dscrew=7.62
    wshaft=0; dshaft=4; pinxoffset=+4.57-wscrew; pinyoffset=(hbody-2*rmy)/2
    footprint_name = "Potentiometer_Trimmer_Bourns_3339S".format(rmx, 2 * rmy)
    makePotentiometerVertical(style="trimmer", footprint_name=footprint_name, class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_trv,height3d=height3d, screwzpos=screwzpos)
    rmx=2.54; pinxoffset=+4.57-wscrew+2.54
    footprint_name = "Potentiometer_Trimmer_Bourns_3339W".format(rmx, 2 * rmy)
    makePotentiometerVertical(style="trimmer", footprint_name=footprint_name, class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_trv,height3d=height3d, screwzpos=screwzpos)
    
    class_name="Bourns 3339P Single"
    pins = 3; rmx=-2.54; rmy=2.54; ddrill=0.7
    wbody=0; hbody=7.62; dbody=7.62; height3d = 6.35
    wscrew=-wbody; dscrew=5
    wshaft=0; dshaft=0; pinxoffset=0; pinyoffset=(hbody-2*rmy)/2
    voffsetx=-rmx; vwbody=0; pinyoffset=(hbody-2*rmy)/2; c_offsetx=rmx; c_offsety=hbody/2; c_ddrill=2
    class_name="Bourns 3339P Single"
    footprint_name = "Potentiometer_Trimmer_Bourns_3339P".format(rmx, 2 * rmy)
    makePotentiometerHorizontal(deco='slit', style="trimmer", mount_below=False, footprint_name=footprint_name, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=c_ddrill,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_ph_bel,height3d=height3d)
    rmx = 2.54 / math.sqrt(2);
    rmy = 2.54 / math.sqrt(2);
    voffsetx = rmx*2;
    vwbody = 0;
    pinyoffset = (hbody - 2 * rmy) / 2; c_offsetx=-rmx;  c_offsety=hbody/2; c_ddrill=2
    class_name="Bourns 3339H Single"
    footprint_name = "Potentiometer_Trimmer_Bourns_3339H".format(rmx, 2 * rmy)
    makePotentiometerHorizontal(deco='slit', style="trimmer", mount_below=False, footprint_name=footprint_name, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=c_ddrill,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_ph_bel,height3d=height3d)

    class_name="Vishay T7YA Single"
    pins = 3; rmx=2.54; rmy=2.54; ddrill=0.8
    wbody=0; hbody=7; dbody=7; height3d = 5.85
    wscrew=-wbody; dscrew=4.1
    wshaft=0; dshaft=0; pinxoffset=0; pinyoffset=(hbody-2*rmy)/2
    voffsetx=-rmx; vwbody=0; vpinyoffset=(hbody-2*rmy)/2; c_offsetx=2.5; c_offsety=hbody/2; c_ddrill=2
    add_description="http://www.vishay.com/docs/51015/t7.pdf"
    class_name="Vishay T7YA Single"
    footprint_name = "Potentiometer_Trimmer_Vishay_T7YA".format(rmx, 2 * rmy)
    makePotentiometerHorizontal(deco='slit', style="trimmer", mount_below=False, footprint_name=footprint_name, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=c_ddrill,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_ph_bel,height3d=height3d)
    
    class_name="Suntan TSR-3386H Single"
    pins = 3; rmx=2.54; rmy=2.54; ddrill=0.8
    wbody=-4.83; hbody=9.83; dbody=0; height3d = 9.53; screwzpos = 5.33;
    wscrew=0; dscrew=3.15
    wshaft=0; dshaft=0; pinxoffset=-(4.83-2.54)/2; pinyoffset=(hbody-2*rmy)/2
    add_description="http://www.Suntan.com/docs/51016/TSR-3386.pdf"
    footprint_name = "Potentiometer_Trimmer_Suntan_TSR-3386H".format(rmx, 2 * rmy)
    makePotentiometerVertical(style="trimmer", footprint_name=footprint_name, class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_trv,height3d=height3d, screwzpos=screwzpos)
    rmx=0; pinxoffset=-4.83/2
    footprint_name = "Potentiometer_Trimmer_Suntan_TSR-3386C".format(rmx, 2 * rmy)
    makePotentiometerVertical(style="trimmer", footprint_name=footprint_name, class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_trv,height3d=height3d, screwzpos=screwzpos)
    class_name="Suntan TSR-3386P Single"
    rmx=2.54; dbody=0; voffsetx=-4.78; vwbody=9.53; vpinyoffset=(hbody-2*rmy)/2; c_offsetx=9.53-5.64; c_offsety=hbody/2; c_ddrill=2
    footprint_name = "Potentiometer_Trimmer_Suntan_TSR-3386P".format(rmx, 2 * rmy)
    makePotentiometerHorizontal(deco="slit", style="trimmer", mount_below=False, footprint_name=footprint_name, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=c_ddrill,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_ph_bel,height3d=height3d)

    class_name="Vishay T73XX Single"
    pins = 3; rmx=2.54; rmy=2.54; ddrill=0.8
    wbody=-4.7; hbody=6.6; dbody=0; height3d = 7; screwzpos = 3.8;
    wscrew=0; dscrew=3
    wshaft=0; dshaft=0; pinxoffset=-1.02; pinyoffset=(hbody-2*rmy)/2
    add_description="http://www.vishay.com/docs/51016/t73.pdf"
    footprint_name = "Potentiometer_Trimmer_Vishay_T73XX".format(rmx, 2 * rmy)
    makePotentiometerVertical(style="trimmer", footprint_name=footprint_name, class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_trv,height3d=height3d, screwzpos=screwzpos)
    rmx=0; pinxoffset=-2.35
    footprint_name = "Potentiometer_Trimmer_Vishay_T73XW".format(rmx, 2 * rmy)
    makePotentiometerVertical(style="trimmer", footprint_name=footprint_name, class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_trv,height3d=height3d, screwzpos=screwzpos)
    class_name="Vishay T73YP Single"
    rmx=2.54; dbody=0; voffsetx=-3.56; vwbody=7; vpinyoffset=(hbody-2*rmy)/2; c_offsetx=3.8; c_offsety=hbody/2; c_ddrill=2
    footprint_name = "Potentiometer_Trimmer_Vishay_T73YP".format(rmx, 2 * rmy)
    makePotentiometerHorizontal(deco="cross", style="trimmer", mount_below=False, footprint_name=footprint_name, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=c_ddrill,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_ph_bel,height3d=height3d)


    class_name="Piher PT-6h Single"
    pins = 3; rmx=2.5; rmy=2.5; ddrill=0.9
    wbody=-3.5; hbody=6.3; dbody=6.3; height3d = 4.5+dbody/2; screwzpos = 4.5;
    wscrew=-wbody; dscrew=2
    wshaft=0; dshaft=1.8; pinxoffset=0; pinyoffset=(hbody-2*rmy)/2
    add_description="http://www.piher-nacesa.com/pdf/11-PT6v03.pdf"
    footprint_name = "Potentiometer_Trimmer_Piher_PT-6h".format(rmx, 2 * rmy)
    makePotentiometerVertical(style="trimmer", footprint_name=footprint_name, class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_trv,height3d=height3d, screwzpos=screwzpos)
    class_name="Piher PT-6v Single"
    rmx=5; dbody=6.3; voffsetx=0; vwbody=0; vpinyoffset=(hbody-2*rmy)/2; c_offsetx=2.5; c_offsety=hbody/2; c_ddrill=2
    footprint_name = "Potentiometer_Trimmer_Piher_PT-6v".format(rmx, 2 * rmy)
    makePotentiometerHorizontal(style="trimmer", mount_below=False, footprint_name=footprint_name, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=c_ddrill,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_ph_bel,height3d=height3d)
    makePotentiometerHorizontal(style="trimmer", mount_below=True, footprint_name=footprint_name, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=c_ddrill,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_ph_bel,height3d=height3d)

    class_name="Piher PT-10h2.5 Single"
    pins = 3; rmx=2.5; rmy=2.5; ddrill=1.3
    wbody=-4.8; hbody=10.3; height3d = 12.1; screwzpos = 7; dbody=10.3
    wscrew=-wbody; dscrew=3.5
    wshaft=0; dshaft=3; pinxoffset=0; pinyoffset=(hbody-2*rmy)/2
    add_description="http://www.piher-nacesa.com/pdf/12-PT10v03.pdf"
    footprint_name="Potentiometer_Trimmer_Piher_PT-10h2.5"
    name_additions=["Px{0:1.1f}mm_Py{1:1.1f}mm".format(rmx, 2*rmy)]
    makePotentiometerVertical(style="trimmer", footprint_name=footprint_name, class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_trv,height3d=height3d, screwzpos=screwzpos)
    class_name="Piher PT-10h5 Single"
    rmx=5; height3d = 12.1; screwzpos = 7;  pinyoffset=(hbody-2*rmy)/2
    footprint_name="Potentiometer_Trimmer_Piher_PT-10h5"
    name_additions = ["Px{0:1.1f}mm_Py{1:1.1f}mm".format(rmx, 2 * rmy)]
    makePotentiometerVertical(style="trimmer", footprint_name=footprint_name, class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_trv,height3d=height3d, screwzpos=screwzpos)
    class_name="Piher PT-101h3.8 Single"
    rmx=3.8; height3d = 17.1; screwzpos = 9.6;  pinyoffset=(hbody-2*rmy)/2
    footprint_name="Potentiometer_Trimmer_Piher_PT-10h3.8"
    name_additions = ["Px{0:1.1f}mm_Py{1:1.1f}mm".format(rmx, 2 * rmy)]
    makePotentiometerVertical(style="trimmer", footprint_name=footprint_name, class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_trv,height3d=height3d, screwzpos=screwzpos)
    class_name="Piher PT-10v10 Single"
    hbody=10; rmx=10; dbody=10.3; voffsetx=0; vwbody=0; vpinyoffset=(hbody-2*rmy)/2; c_offsetx=5; c_offsety=hbody/2; c_ddrill=4
    footprint_name = "Potentiometer_Trimmer_Piher_PT-10v10".format(rmx, 2 * rmy)
    name_additions = ["Px{0:1.1f}mm_Py{1:1.1f}mm".format(rmx, 2 * rmy)]
    makePotentiometerHorizontal(style="trimmer", mount_below=False, footprint_name=footprint_name, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=c_ddrill,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_ph_bel,height3d=height3d)
    makePotentiometerHorizontal(style="trimmer", mount_below=True, footprint_name=footprint_name, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=c_ddrill,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_ph_bel,height3d=height3d)
    class_name="Piher PT-10v5 Single"
    voffsetx = -5.3/2; hbody=10; rmx=5; dbody=10.3; vwbody=0; vpinyoffset=(hbody-2*rmy)/2; c_offsetx=10.3/2; c_offsety=dbody/2; c_ddrill=3
    footprint_name = "Potentiometer_Trimmer_Piher_PT-10v5".format(rmx, 2 * rmy)
    name_additions = ["Px{0:1.1f}mm_Py{1:1.1f}mm".format(rmx, 2 * rmy)]
    makePotentiometerHorizontal(style="trimmer", mount_below=False, footprint_name=footprint_name, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=c_ddrill,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_ph_bel,height3d=height3d)
    name_additions = []

    
    class_name="Piher PT-15h5 Single"
    pins = 3; rmx=5.0; rmy=5; ddrill=1.3
    wbody=-5; hbody=15; height3d = 17.5; screwzpos = 10; dbody=15
    wscrew=-wbody; dscrew=6
    wshaft=0; dshaft=4.4; pinxoffset=0; pinyoffset=(hbody-2*rmy)/2
    add_description="http://www.piher-nacesa.com/pdf/14-PT15v03.pdf"
    footprint_name="Potentiometer_Trimmer_Piher_PT-15h5"
    name_additions = ["Px{0:1.1f}mm_Py{1:1.1f}mm".format(rmx, 2 * rmy)]
    makePotentiometerVertical(style="trimmer", footprint_name=footprint_name, class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_trv,height3d=height3d, screwzpos=screwzpos)
    class_name="Piher PT-15h2.5 Single"
    rmy=5; rmx=2.5; height3d = 17.5; screwzpos = 10;  pinyoffset=(hbody-2*rmy)/2
    footprint_name="Potentiometer_Trimmer_Piher_PT-15h2.5"
    name_additions = ["Px{0:1.1f}mm_Py{1:1.1f}mm".format(rmx, 2 * rmy)]
    makePotentiometerVertical(style="trimmer", footprint_name=footprint_name, class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_trv,height3d=height3d, screwzpos=screwzpos)
    class_name="Piher PT-15B Single"
    rmy=4.4; rmx=4; height3d = 17.1; screwzpos = 9.6;  pinyoffset=(hbody-2*rmy)/2
    footprint_name="Potentiometer_Trimmer_Piher_PT-15B"
    name_additions = ["Px{0:1.1f}mm_Py{1:1.1f}mm".format(rmx, 2 * rmy)]
    makePotentiometerVertical(style="trimmer", footprint_name=footprint_name, class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_trv,height3d=height3d, screwzpos=screwzpos)
    class_name="Piher PT-15hc5 Single"
    rmy=5; rmx=5; height3d = 20; screwzpos = 12.5;  pinyoffset=(hbody-2*rmy)/2
    footprint_name="Potentiometer_Trimmer_Piher_PT-15hc5"
    name_additions = ["Px{0:1.1f}mm_Py{1:1.1f}mm".format(rmx, 2 * rmy)]
    makePotentiometerVertical(style="trimmer", footprint_name=footprint_name, class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_trv,height3d=height3d, screwzpos=screwzpos)
    class_name="Piher PT-15v12.5 Single"
    hbody=10; rmx=12.5; dbody=15; voffsetx=0; vwbody=0; vpinyoffset=(dbody-2*rmy)/2; c_offsetx=7.5; c_offsety=dbody/2; c_ddrill=7
    footprint_name = "Potentiometer_Trimmer_Piher_PT-15v12.5".format(rmx, 2 * rmy)
    name_additions = ["Px{0:1.1f}mm_Py{1:1.1f}mm".format(rmx, 2 * rmy)]
    makePotentiometerHorizontal(style="trimmer", mount_below=False, footprint_name=footprint_name, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=c_ddrill,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_ph_bel,height3d=height3d)
    makePotentiometerHorizontal(style="trimmer", mount_below=True, footprint_name=footprint_name, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=c_ddrill,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_ph_bel,height3d=height3d)
    class_name="Piher PT-15v15 Single"
    voffsetx =0; hbody=15; rmx=15; dbody=15; vwbody=0; vpinyoffset=(dbody-2*rmy)/2; c_offsetx=7.5; c_offsety=dbody/2; c_ddrill=7
    footprint_name = "Potentiometer_Trimmer_Piher_PT-15v15".format(rmx, 2 * rmy)
    name_additions = ["Px{0:1.1f}mm_Py{1:1.1f}mm".format(rmx, 2 * rmy)]
    makePotentiometerHorizontal(style="trimmer", mount_below=False, footprint_name=footprint_name, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=c_ddrill,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_ph_bel,height3d=height3d)
    makePotentiometerHorizontal(style="trimmer", mount_below=True, footprint_name=footprint_name, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=c_ddrill,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_ph_bel,height3d=height3d)
    name_additions = []


    class_name="ACP CA6h Single"
    pins = 3; rmx=2.5; rmy=2.5; ddrill=0.9
    wbody=-3.5; hbody=6.3; dbody=0; height3d = 4.5+dbody/2; screwzpos = 4.5;
    wscrew=-wbody; dscrew=2
    wshaft=0; dshaft=1.8; pinxoffset=0; pinyoffset=(hbody-2*rmy)/2
    add_description="http://www.acptechnologies.com/wp-content/uploads/2016/12/ACP-CAT%C3%81LOGO-ENTERO-2016.pdf"
    footprint_name = "Potentiometer_Trimmer_ACP_CA6h".format(rmx, 2 * rmy)
    makePotentiometerVertical(style="trimmer", footprint_name=footprint_name, class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_trv,height3d=height3d, screwzpos=screwzpos)
    class_name="ACP CA6v Single"
    rmx=5; dbody=0; voffsetx=-1.3/2; vwbody=6.3; vpinyoffset=(hbody-2*rmy)/2; c_offsetx=6.3/2; c_offsety=hbody/2; c_ddrill=2.5; height3d=4.6
    footprint_name = "Potentiometer_Trimmer_ACP_CA6v".format(rmx, 2 * rmy)
    makePotentiometerHorizontal(style="trimmer", mount_below=False, footprint_name=footprint_name, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=c_ddrill,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=vpinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_ph_bel,height3d=height3d)
    makePotentiometerHorizontal(style="trimmer", mount_below=True, footprint_name=footprint_name, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=c_ddrill,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=vpinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_ph_bel,height3d=height3d)
    class_name="ACP CA6VSMD Single"
    rmx=8.65; rmy=4.3/2; dbody=0; vwbody=6.3; voffsetx=(rmx-vwbody)/2; vpinyoffset=(hbody-2*rmy)/2; c_offsetx=6.3/2; c_offsety=hbody/2; c_ddrill=2.5
    footprint_name = "Potentiometer_Trimmer_ACP_CA6VSMD".format(rmx, 2 * rmy)
    makePotentiometerHorizontal(SMD_pads=True, SMD_padsize=[2.5,2], style="trimmer", mount_below=False, footprint_name=footprint_name, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=c_ddrill,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=vpinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_ph_bel,height3d=height3d)
    makePotentiometerHorizontal(SMD_pads=True, SMD_padsize=[2.5,2], style="trimmer", mount_below=True, footprint_name=footprint_name, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=c_ddrill,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=vpinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_ph_bel,height3d=height3d)
    name_additions = []

    class_name="ACP CA9h2.5 Single"
    pins = 3; rmx=2.5; rmy=2.5; ddrill=1.3
    wbody=-4.8; hbody=9.8; dbody=0; height3d = 12; screwzpos = 7;
    wscrew=-wbody; dscrew=3
    wshaft=0; dshaft=2.1; pinxoffset=0; pinyoffset=(hbody-2*rmy)/2
    add_description="http://www.acptechnologies.com/wp-content/uploads/2016/12/ACP-CAT%C3%81LOGO-ENTERO-2016.pdf"
    footprint_name = "Potentiometer_Trimmer_ACP_CA9h2.5".format(rmx, 2 * rmy)
    name_additions = ["Px{0:1.1f}mm_Py{1:1.1f}mm".format(rmx, 2 * rmy)]
    makePotentiometerVertical(style="trimmer", footprint_name=footprint_name, class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_trv,height3d=height3d, screwzpos=screwzpos)
    rmx=3.8
    class_name="ACP CA9h3.8 Single"
    footprint_name = "Potentiometer_Trimmer_ACP_CA9h3.8".format(rmx, 2 * rmy)
    name_additions = ["Px{0:1.1f}mm_Py{1:1.1f}mm".format(rmx, 2 * rmy)]
    makePotentiometerVertical(style="trimmer", footprint_name=footprint_name, class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_trv,height3d=height3d, screwzpos=screwzpos)
    rmx=5
    class_name="ACP CA9h5 Single"
    footprint_name = "Potentiometer_Trimmer_ACP_CA9h5".format(rmx, 2 * rmy)
    name_additions = ["Px{0:1.1f}mm_Py{1:1.1f}mm".format(rmx, 2 * rmy)]
    makePotentiometerVertical(style="trimmer", footprint_name=footprint_name, class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_trv,height3d=height3d, screwzpos=screwzpos)
    class_name="ACP CA9V Single"
    rmx=10; dbody=0; voffsetx=0; vwbody=10; vpinyoffset=(hbody-2*rmy)/2; c_offsetx=vwbody/2; c_offsety=hbody/2; c_ddrill=4; height3d=7.2
    footprint_name = "Potentiometer_Trimmer_ACP_CA9v".format(rmx, 2 * rmy)
    name_additions = ["Px{0:1.1f}mm_Py{1:1.1f}mm".format(rmx, 2 * rmy)]
    makePotentiometerHorizontal(style="trimmer", mount_below=False, footprint_name=footprint_name, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=c_ddrill,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=vpinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_ph_bel,height3d=height3d)
    makePotentiometerHorizontal(style="trimmer", mount_below=True, footprint_name=footprint_name, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=c_ddrill,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=vpinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_ph_bel,height3d=height3d)
    class_name="ACP CA9VSMD Single"
    rmx=9.25; rmy=2.5; dbody=0; voffsetx=-0.25; vwbody=10; vpinyoffset=(hbody-2*rmy)/2; c_offsetx=4.75; c_offsety=hbody/2; c_ddrill=4; height3d=5.5
    footprint_name = "Potentiometer_Trimmer_ACP_CA9VSMD".format(rmx, 2 * rmy)
    name_additions = ["Px{0:1.1f}mm_Py{1:1.1f}mm".format(rmx, 2 * rmy)]
    makePotentiometerHorizontal(SMD_pads=True, SMD_padsize=[2.5,2.5], style="trimmer", mount_below=False, footprint_name=footprint_name, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=c_ddrill,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=vpinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_ph_bel,height3d=height3d)
    makePotentiometerHorizontal(SMD_pads=True, SMD_padsize=[2.5,2.5], style="trimmer", mount_below=True, footprint_name=footprint_name, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=c_ddrill,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=vpinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_ph_bel,height3d=height3d)
    name_additions = []


    class_name="ACP CA14h2.5 Single"
    pins = 3; rmx=2.5; rmy=5; ddrill=1.3
    wbody=-5.0; hbody=14; dbody=0; height3d = 17; screwzpos = 10;
    wscrew=-wbody; dscrew=6
    wshaft=0; dshaft=5; pinxoffset=0; pinyoffset=(hbody-2*rmy)/2
    add_description="http://www.acptechnologies.com/wp-content/uploads/2016/12/ACP-CAT%C3%81LOGO-ENTERO-2016.pdf"
    footprint_name = "Potentiometer_Trimmer_ACP_CA14h2.5".format(rmx, 2 * rmy)
    name_additions = ["Px{0:1.1f}mm_Py{1:1.1f}mm".format(rmx, 2 * rmy)]
    makePotentiometerVertical(style="trimmer", footprint_name=footprint_name, class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_trv,height3d=height3d, screwzpos=screwzpos)
    rmx=4
    class_name="ACP CA14h4 Single"
    footprint_name = "Potentiometer_Trimmer_ACP_CA14h4".format(rmx, 2 * rmy)
    name_additions = ["Px{0:1.1f}mm_Py{1:1.1f}mm".format(rmx, 2 * rmy)]
    makePotentiometerVertical(style="trimmer", footprint_name=footprint_name, class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_trv,height3d=height3d, screwzpos=screwzpos)
    rmx=5
    class_name="ACP CA14h5 Single"
    footprint_name = "Potentiometer_Trimmer_ACP_CA14h5".format(rmx, 2 * rmy)
    name_additions = ["Px{0:1.1f}mm_Py{1:1.1f}mm".format(rmx, 2 * rmy)]
    makePotentiometerVertical(style="trimmer", footprint_name=footprint_name, class_name=class_name, wbody=wbody, hbody=hbody, wscrew=wscrew, dscrew=dscrew, wshaft=wshaft, dshaft=dshaft, pinxoffset=pinxoffset,pinyoffset=pinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, R_POW=R_POW, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_trv,height3d=height3d, screwzpos=screwzpos)
    class_name="ACP CA14V15 Single"
    rmx=15; dbody=0; voffsetx=0.5; vwbody=14; vpinyoffset=(hbody-2*rmy)/2; c_offsetx=vwbody/2; c_offsety=hbody/2; c_ddrill=7; height3d=7.2
    footprint_name = "Potentiometer_Trimmer_ACP_CA14v".format(rmx, 2 * rmy)
    name_additions = ["Px{0:1.1f}mm_Py{1:1.1f}mm".format(rmx, 2 * rmy)]
    makePotentiometerHorizontal(style="trimmer", mount_below=False, footprint_name=footprint_name, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=c_ddrill,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=vpinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_ph_bel,height3d=height3d)
    makePotentiometerHorizontal(style="trimmer", mount_below=True, footprint_name=footprint_name, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=c_ddrill,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=vpinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_ph_bel,height3d=height3d)
    class_name="ACP CA14VSMD Single"
    rmx=13; rmy=5; dbody=0; voffsetx=-0.7; vwbody=14; vpinyoffset=(hbody-2*rmy)/2; c_offsetx=7; c_offsety=hbody/2; c_ddrill=7; height3d=5.8
    footprint_name = "Potentiometer_Trimmer_ACP_CA14VSMD".format(rmx, 2 * rmy)
    name_additions = ["Px{0:1.1f}mm_Py{1:1.1f}mm".format(rmx, 2 * rmy)]
    makePotentiometerHorizontal(SMD_pads=True, SMD_padsize=[2.5,2.5], style="trimmer", mount_below=False, footprint_name=footprint_name, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=c_ddrill,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=vpinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_ph_bel,height3d=height3d)
    makePotentiometerHorizontal(SMD_pads=True, SMD_padsize=[2.5,2.5], style="trimmer", mount_below=True, footprint_name=footprint_name, class_name=class_name, wbody=vwbody, hbody=hbody, d_body=dbody, dshaft=dshaft, dscrew=dscrew, c_ddrill=c_ddrill,c_offsetx=c_offsetx, c_offsety=c_offsety, pinxoffset=voffsetx,pinyoffset=vpinyoffset, pins=pins, rmx=rmx, rmy=rmy, ddrill=ddrill, specialtags=specialtags, add_description=add_description,classname=classname, lib_name=lib_name, name_additions=name_additions, script3d=script3d_ph_bel,height3d=height3d)
    name_additions = []

    footprint_name="Potentiometer_Trimmer_Bourns_3005"
    class_name="Bourns 3005"
    wbody=19.3; hbody=4.06; pinxoffset=16; pinyoffset=(hbody-2.54)/2+2.54; height3d = 7.87
    rmx2=-7.62; rmy2=-2.54; rmx3=-12.7; rmy3=0; ddrill=1;
    dscrew=3; wscrew = 1.52; screwxoffset = 0; screwyoffset = hbody/2;
    style = "screwleft"; SMD_pads = False; SMD_padsize = []; specialtags = []; name_additions = []
    add_description = "https://www.bourns.com/pdfs/3005.pdf";
    makeSpindleTrimmer(footprint_name=footprint_name, class_name=class_name, ddrill=ddrill, wbody=wbody, hbody=hbody, pinxoffset=pinxoffset, pinyoffset=pinyoffset, rmx2=rmx2, rmy2=rmy2, rmx3=rmx3, rmy3=rmy3, dscrew=dscrew, wscrew=wscrew, screwxoffset=screwxoffset, screwyoffset=screwyoffset, style=style, SMD_pads=SMD_pads, SMD_padsize=SMD_padsize, specialtags=specialtags, add_description=add_description, classname="Potentiometer", lib_name="Potentiometers", name_additions=name_additions, script3d=script3d_tsl, height3d=height3d)
    
    footprint_name="Potentiometer_Trimmer_Vishay_43"
    class_name="Vishay 43"
    wbody=19.0; hbody=4.8; pinxoffset=16; pinyoffset=(hbody-2.54)/2+2.54; height3d = 6.35
    rmx2=-7.62; rmy2=-2.54; rmx3=-12.7; rmy3=0; ddrill=1;
    dscrew=2.36; wscrew = 1.52; screwxoffset = 0; screwyoffset = hbody/2;
    style = "screwleft"; SMD_pads = False; SMD_padsize = []; specialtags = []; name_additions = []
    add_description = "http://www.vishay.com/docs/57026/43.pdf";
    makeSpindleTrimmer(footprint_name=footprint_name, class_name=class_name, ddrill=ddrill, wbody=wbody, hbody=hbody, pinxoffset=pinxoffset, pinyoffset=pinyoffset, rmx2=rmx2, rmy2=rmy2, rmx3=rmx3, rmy3=rmy3, dscrew=dscrew, wscrew=wscrew, screwxoffset=screwxoffset, screwyoffset=screwyoffset, style=style, SMD_pads=SMD_pads, SMD_padsize=SMD_padsize, specialtags=specialtags, add_description=add_description, classname="Potentiometer", lib_name="Potentiometers", name_additions=name_additions, script3d=script3d_tsl, height3d=height3d)

    footprint_name="Potentiometer_Trimmer_Bourns_3006P"
    class_name="Bourns 3006P"
    wbody=19.05; hbody=4.83; pinxoffset=16; pinyoffset=(hbody-2.54)/2+2.54; height3d = 6.35
    rmx2=-7.62; rmy2=-2.54; rmx3=-12.7; rmy3=0; ddrill=1;
    dscrew=2.36; wscrew = 1.52; screwxoffset = 0; screwyoffset = hbody/2;
    style = "screwleft"; SMD_pads = False; SMD_padsize = []; specialtags = []; name_additions = []
    add_description = "http://www.bourns.com/docs/Product-Datasheets/3006.pdf?sfvrsn=0";
    makeSpindleTrimmer(footprint_name=footprint_name, class_name=class_name, ddrill=ddrill, wbody=wbody, hbody=hbody, pinxoffset=pinxoffset, pinyoffset=pinyoffset, rmx2=rmx2, rmy2=rmy2, rmx3=rmx3, rmy3=rmy3, dscrew=dscrew, wscrew=wscrew, screwxoffset=screwxoffset, screwyoffset=screwyoffset, style=style, SMD_pads=SMD_pads, SMD_padsize=SMD_padsize, specialtags=specialtags, add_description=add_description, classname="Potentiometer", lib_name="Potentiometers", name_additions=name_additions, script3d=script3d_tsl, height3d=height3d)
    footprint_name="Potentiometer_Trimmer_Bourns_3006W"
    class_name="Bourns 3006W"
    wbody=19.05; hbody=4.83; pinxoffset=16; pinyoffset=4.83+0.15; height3d = 6.35
    rmx2=-7.62; rmy2=-5.06; rmx3=-12.7; rmy3=0; ddrill=1;
    dscrew=2.36; wscrew = 1.52; screwxoffset = 0; screwyoffset = hbody/2;
    style = "screwleft"; SMD_pads = False; SMD_padsize = []; specialtags = []; name_additions = []
    makeSpindleTrimmer(footprint_name=footprint_name, class_name=class_name, ddrill=ddrill, wbody=wbody, hbody=hbody, pinxoffset=pinxoffset, pinyoffset=pinyoffset, rmx2=rmx2, rmy2=rmy2, rmx3=rmx3, rmy3=rmy3, dscrew=dscrew, wscrew=wscrew, screwxoffset=screwxoffset, screwyoffset=screwyoffset, style=style, SMD_pads=SMD_pads, SMD_padsize=SMD_padsize, specialtags=specialtags, add_description=add_description, classname="Potentiometer", lib_name="Potentiometers", name_additions=name_additions, script3d=script3d_tsl, height3d=height3d)
    footprint_name="Potentiometer_Trimmer_Bourns_3006Y"
    class_name="Bourns 3006Y"
    wbody=19.05; hbody=4.83; pinxoffset=18.42; pinyoffset=(hbody-2.54)/2+2.54; height3d = 6.35
    print(hbody,pinyoffset)
    rmx2=-(17.78-7.62); rmy2=-2.54; rmx3=-17.78; rmy3=0; ddrill=1;
    dscrew=2.36; wscrew = 1.52; screwxoffset = 0; screwyoffset = hbody/2;
    style = "screwleft"; SMD_pads = False; SMD_padsize = []; specialtags = []; name_additions = []
    makeSpindleTrimmer(footprint_name=footprint_name, class_name=class_name, ddrill=ddrill, wbody=wbody, hbody=hbody, pinxoffset=pinxoffset, pinyoffset=pinyoffset, rmx2=rmx2, rmy2=rmy2, rmx3=rmx3, rmy3=rmy3, dscrew=dscrew, wscrew=wscrew, screwxoffset=screwxoffset, screwyoffset=screwyoffset, style=style, SMD_pads=SMD_pads, SMD_padsize=SMD_padsize, specialtags=specialtags, add_description=add_description, classname="Potentiometer", lib_name="Potentiometers", name_additions=name_additions, script3d=script3d_tsl, height3d=height3d)

    footprint_name="Potentiometer_Trimmer_Bourns_3009P"
    class_name="Bourns 3009P"
    wbody=19.05; hbody=4.83; pinxoffset=16; pinyoffset=(hbody-2.54)/2+2.54; height3d = 8.98
    rmx2=-7.62; rmy2=-2.54; rmx3=-12.7; rmy3=0; ddrill=1;
    dscrew=2.36; wscrew = 1.52; screwxoffset = 0; screwyoffset = hbody/2;
    style = "screwleft"; SMD_pads = False; SMD_padsize = []; specialtags = []; name_additions = []
    add_description = "http://www.bourns.com/docs/Product-Datasheets/3009.pdf?sfvrsn=0";
    footprint_name="Potentiometer_Trimmer_Bourns_3009W"
    class_name="Bourns 3009Y"
    wbody=19.05; hbody=4.83; pinxoffset=18.42; pinyoffset=(hbody-2.54)/2+2.54; height3d = 8.98
    print(hbody,pinyoffset)
    rmx2=-(17.78-7.62); rmy2=-2.54; rmx3=-17.78; rmy3=0; ddrill=1;
    dscrew=2.36; wscrew = 1.52; screwxoffset = 0; screwyoffset = hbody/2;
    style = "screwleft"; SMD_pads = False; SMD_padsize = []; specialtags = []; name_additions = []
    add_description = "http://www.bourns.com/docs/Product-Datasheets/3009.pdf?sfvrsn=0";
    makeSpindleTrimmer(footprint_name=footprint_name, class_name=class_name, ddrill=ddrill, wbody=wbody, hbody=hbody, pinxoffset=pinxoffset, pinyoffset=pinyoffset, rmx2=rmx2, rmy2=rmy2, rmx3=rmx3, rmy3=rmy3, dscrew=dscrew, wscrew=wscrew, screwxoffset=screwxoffset, screwyoffset=screwyoffset, style=style, SMD_pads=SMD_pads, SMD_padsize=SMD_padsize, specialtags=specialtags, add_description=add_description, classname="Potentiometer", lib_name="Potentiometers", name_additions=name_additions, script3d=script3d_tsl, height3d=height3d)

    footprint_name="Potentiometer_Trimmer_Bourns_3296W"
    class_name="Bourns 3296W"
    wbody=9.53; hbody=4.83; pinxoffset=(wbody-5.08)/2+5.08; pinyoffset=2.41; height3d = 10.03
    rmx2=-2.54; rmy2=0; rmx3=-5.08; rmy3=0; ddrill=0.8;
    dscrew=2.19; wscrew = dscrew; screwxoffset = wbody-1.27; screwyoffset = hbody-1.27;
    style = "screwtop"; SMD_pads = False; SMD_padsize = []; specialtags = []; name_additions = []
    add_description = "https://www.bourns.com/pdfs/3296.pdf";
    makeSpindleTrimmer(footprint_name=footprint_name, class_name=class_name, ddrill=ddrill, wbody=wbody, hbody=hbody, pinxoffset=pinxoffset, pinyoffset=pinyoffset, rmx2=rmx2, rmy2=rmy2, rmx3=rmx3, rmy3=rmy3, dscrew=dscrew, wscrew=wscrew, screwxoffset=screwxoffset, screwyoffset=screwyoffset, style=style, SMD_pads=SMD_pads, SMD_padsize=SMD_padsize, specialtags=specialtags, add_description=add_description, classname="Potentiometer", lib_name="Potentiometers", name_additions=name_additions, script3d=script3d_tsl, height3d=height3d)
    footprint_name="Potentiometer_Trimmer_Bourns_3296X"
    class_name="Bourns 3296X"
    wbody=9.53; hbody=4.83; pinxoffset=(wbody-5.08)/2+5.08; pinyoffset=2.41; height3d = 10.03
    rmx2=-2.54; rmy2=0; rmx3=-5.08; rmy3=0; ddrill=0.8; dscrew = 2.19; wscrew = 1.52; screwxoffset = 0; screwyoffset = hbody- 1.27;
    style = "screwleft"; SMD_pads = False; SMD_padsize = []; specialtags = []; name_additions = []
    add_description = "https://www.bourns.com/pdfs/3296.pdf";
    makeSpindleTrimmer(footprint_name=footprint_name, class_name=class_name, ddrill=ddrill, wbody=wbody, hbody=hbody, pinxoffset=pinxoffset, pinyoffset=pinyoffset, rmx2=rmx2, rmy2=rmy2, rmx3=rmx3, rmy3=rmy3, dscrew=dscrew, wscrew=wscrew, screwxoffset=screwxoffset, screwyoffset=screwyoffset, style=style, SMD_pads=SMD_pads, SMD_padsize=SMD_padsize, specialtags=specialtags, add_description=add_description, classname="Potentiometer", lib_name="Potentiometers", name_additions=name_additions, script3d=script3d_tsl, height3d=height3d)
    footprint_name="Potentiometer_Trimmer_Bourns_3296Y"
    class_name="Bourns 3296Y"
    wbody=9.53; hbody=4.83; pinxoffset=(wbody-5.08)/2+5.08; pinyoffset=1.14; height3d = 10.03
    rmx2=-2.54; rmy2=2.54; rmx3=-5.08; rmy3=0; ddrill=0.8;
    dscrew=2.19; wscrew = dscrew; screwxoffset = wbody-1.27; screwyoffset = hbody-1.27;
    style = "screwtop"; SMD_pads = False; SMD_padsize = []; specialtags = []; name_additions = []
    add_description = "https://www.bourns.com/pdfs/3296.pdf";
    makeSpindleTrimmer(footprint_name=footprint_name, class_name=class_name, ddrill=ddrill, wbody=wbody, hbody=hbody, pinxoffset=pinxoffset, pinyoffset=pinyoffset, rmx2=rmx2, rmy2=rmy2, rmx3=rmx3, rmy3=rmy3, dscrew=dscrew, wscrew=wscrew, screwxoffset=screwxoffset, screwyoffset=screwyoffset, style=style, SMD_pads=SMD_pads, SMD_padsize=SMD_padsize, specialtags=specialtags, add_description=add_description, classname="Potentiometer", lib_name="Potentiometers", name_additions=name_additions, script3d=script3d_tsl, height3d=height3d)
    footprint_name="Potentiometer_Trimmer_Bourns_3296Z"
    class_name="Bourns 3296Z"
    wbody=9.53; hbody=4.83; pinxoffset=(wbody-5.08)/2+5.08; pinyoffset=hbody-1.14-2.54; height3d = 10.03
    rmx2=-2.54; rmy2=2.54; rmx3=-5.08; rmy3=0; ddrill=0.8;
    dscrew=2.19; wscrew = 1.52; screwxoffset = 0; screwyoffset = hbody-1.27;
    style = "screwleft"; SMD_pads = False; SMD_padsize = []; specialtags = []; name_additions = []
    add_description = "https://www.bourns.com/pdfs/3296.pdf";
    makeSpindleTrimmer(footprint_name=footprint_name, class_name=class_name, ddrill=ddrill, wbody=wbody, hbody=hbody, pinxoffset=pinxoffset, pinyoffset=pinyoffset, rmx2=rmx2, rmy2=rmy2, rmx3=rmx3, rmy3=rmy3, dscrew=dscrew, wscrew=wscrew, screwxoffset=screwxoffset, screwyoffset=screwyoffset, style=style, SMD_pads=SMD_pads, SMD_padsize=SMD_padsize, specialtags=specialtags, add_description=add_description, classname="Potentiometer", lib_name="Potentiometers", name_additions=name_additions, script3d=script3d_tsl, height3d=height3d)
    footprint_name="Potentiometer_Trimmer_Bourns_3296P"
    class_name="Bourns 3296P"
    wbody=10.03; hbody=9.53; pinxoffset=wbody/2; pinyoffset=(hbody-5.08)/2; height3d = 4.83
    rmx2=-2.54; rmy2=2.54; rmx3=0; rmy3=5.08; ddrill=0.8;
    dscrew=2.19; wscrew = 1.52; screwxoffset = 0; screwyoffset = 1.27;
    style = "screwleft"; SMD_pads = False; SMD_padsize = []; specialtags = []; name_additions = []
    add_description = "https://www.bourns.com/pdfs/3296.pdf";
    makeSpindleTrimmer(footprint_name=footprint_name, class_name=class_name, ddrill=ddrill, wbody=wbody, hbody=hbody, pinxoffset=pinxoffset, pinyoffset=pinyoffset, rmx2=rmx2, rmy2=rmy2, rmx3=rmx3, rmy3=rmy3, dscrew=dscrew, wscrew=wscrew, screwxoffset=screwxoffset, screwyoffset=screwyoffset, style=style, SMD_pads=SMD_pads, SMD_padsize=SMD_padsize, specialtags=specialtags, add_description=add_description, classname="Potentiometer", lib_name="Potentiometers", name_additions=name_additions, script3d=script3d_tsl, height3d=height3d)


    footprint_name="Potentiometer_Trimmer_Bourns_3299W"
    class_name="Bourns 3299W"
    wbody=9.53; hbody=6.10; pinxoffset=(wbody-5.08)/2+5.08; pinyoffset=1.91; height3d = 10.03
    rmx2=-2.54; rmy2=0; rmx3=-5.08; rmy3=0; ddrill=0.8;
    dscrew=2.19; wscrew = dscrew; screwxoffset = wbody-1.27; screwyoffset = hbody-1.27;
    style = "screwtop"; SMD_pads = False; SMD_padsize = []; specialtags = []; name_additions = []
    add_description = "https://www.bourns.com/pdfs/3299.pdf";
    makeSpindleTrimmer(footprint_name=footprint_name, class_name=class_name, ddrill=ddrill, wbody=wbody, hbody=hbody, pinxoffset=pinxoffset, pinyoffset=pinyoffset, rmx2=rmx2, rmy2=rmy2, rmx3=rmx3, rmy3=rmy3, dscrew=dscrew, wscrew=wscrew, screwxoffset=screwxoffset, screwyoffset=screwyoffset, style=style, SMD_pads=SMD_pads, SMD_padsize=SMD_padsize, specialtags=specialtags, add_description=add_description, classname="Potentiometer", lib_name="Potentiometers", name_additions=name_additions, script3d=script3d_tsl, height3d=height3d)
    footprint_name="Potentiometer_Trimmer_Bourns_3299X"
    class_name="Bourns 3299X"
    wbody=9.53; hbody=6.10; pinxoffset=(wbody-5.08)/2+5.08; pinyoffset=1.91; height3d = 10.03
    rmx2=-2.54; rmy2=0; rmx3=-5.08; rmy3=0; ddrill=0.8; dscrew = 2.19; wscrew = 1.52; screwxoffset = 0; screwyoffset = hbody- 1.27;
    style = "screwleft"; SMD_pads = False; SMD_padsize = []; specialtags = []; name_additions = []
    add_description = "https://www.bourns.com/pdfs/3299.pdf";
    makeSpindleTrimmer(footprint_name=footprint_name, class_name=class_name, ddrill=ddrill, wbody=wbody, hbody=hbody, pinxoffset=pinxoffset, pinyoffset=pinyoffset, rmx2=rmx2, rmy2=rmy2, rmx3=rmx3, rmy3=rmy3, dscrew=dscrew, wscrew=wscrew, screwxoffset=screwxoffset, screwyoffset=screwyoffset, style=style, SMD_pads=SMD_pads, SMD_padsize=SMD_padsize, specialtags=specialtags, add_description=add_description, classname="Potentiometer", lib_name="Potentiometers", name_additions=name_additions, script3d=script3d_tsl, height3d=height3d)
    footprint_name="Potentiometer_Trimmer_Bourns_3299Y"
    class_name="Bourns 3299Y"
    wbody=9.53; hbody=6.10; pinxoffset=(wbody-5.08)/2+5.08; pinyoffset=1.91; height3d = 10.03
    rmx2=-2.54; rmy2=2.54; rmx3=-5.08; rmy3=0; ddrill=0.8;
    dscrew=2.19; wscrew = dscrew; screwxoffset = wbody-1.27; screwyoffset = hbody-1.27;
    style = "screwtop"; SMD_pads = False; SMD_padsize = []; specialtags = []; name_additions = []
    add_description = "https://www.bourns.com/pdfs/3299.pdf";
    makeSpindleTrimmer(footprint_name=footprint_name, class_name=class_name, ddrill=ddrill, wbody=wbody, hbody=hbody, pinxoffset=pinxoffset, pinyoffset=pinyoffset, rmx2=rmx2, rmy2=rmy2, rmx3=rmx3, rmy3=rmy3, dscrew=dscrew, wscrew=wscrew, screwxoffset=screwxoffset, screwyoffset=screwyoffset, style=style, SMD_pads=SMD_pads, SMD_padsize=SMD_padsize, specialtags=specialtags, add_description=add_description, classname="Potentiometer", lib_name="Potentiometers", name_additions=name_additions, script3d=script3d_tsl, height3d=height3d)
    footprint_name="Potentiometer_Trimmer_Bourns_3299Z"
    class_name="Bourns 3299Z"
    wbody=9.53; hbody=6.10; pinxoffset=(wbody-5.08)/2+5.08; pinyoffset=1.91; height3d = 10.03
    rmx2=-2.54; rmy2=2.54; rmx3=-5.08; rmy3=0; ddrill=0.8;
    dscrew=2.19; wscrew = 1.52; screwxoffset = 0; screwyoffset = hbody-1.27;
    style = "screwleft"; SMD_pads = False; SMD_padsize = []; specialtags = []; name_additions = []
    add_description = "https://www.bourns.com/pdfs/3299.pdf";
    makeSpindleTrimmer(footprint_name=footprint_name, class_name=class_name, ddrill=ddrill, wbody=wbody, hbody=hbody, pinxoffset=pinxoffset, pinyoffset=pinyoffset, rmx2=rmx2, rmy2=rmy2, rmx3=rmx3, rmy3=rmy3, dscrew=dscrew, wscrew=wscrew, screwxoffset=screwxoffset, screwyoffset=screwyoffset, style=style, SMD_pads=SMD_pads, SMD_padsize=SMD_padsize, specialtags=specialtags, add_description=add_description, classname="Potentiometer", lib_name="Potentiometers", name_additions=name_additions, script3d=script3d_tsl, height3d=height3d)
    footprint_name="Potentiometer_Trimmer_Bourns_3299P"
    class_name="Bourns 3299P"
    wbody=10.03; hbody=9.53; pinxoffset=wbody/2; pinyoffset=(hbody-5.08)/2; height3d = 6.10
    rmx2=-2.54; rmy2=2.54; rmx3=0; rmy3=5.08; ddrill=0.8;
    dscrew=2.19; wscrew = 1.52; screwxoffset = 0; screwyoffset = 1.27;
    style = "screwleft"; SMD_pads = False; SMD_padsize = []; specialtags = []; name_additions = []
    add_description = "https://www.bourns.com/pdfs/3299.pdf";
    makeSpindleTrimmer(footprint_name=footprint_name, class_name=class_name, ddrill=ddrill, wbody=wbody, hbody=hbody, pinxoffset=pinxoffset, pinyoffset=pinyoffset, rmx2=rmx2, rmy2=rmy2, rmx3=rmx3, rmy3=rmy3, dscrew=dscrew, wscrew=wscrew, screwxoffset=screwxoffset, screwyoffset=screwyoffset, style=style, SMD_pads=SMD_pads, SMD_padsize=SMD_padsize, specialtags=specialtags, add_description=add_description, classname="Potentiometer", lib_name="Potentiometers", name_additions=name_additions, script3d=script3d_tsl, height3d=height3d)


    footprint_name="Potentiometer_Trimmer_Bourns_3266Y"
    class_name="Bourns 3266Y"
    wbody=6.71; hbody=4.5; pinxoffset=(wbody-5.08)/2+5.08; pinyoffset=2.16; height3d = 6.71
    rmx2=-2.54; rmy2=0; rmx3=-5.08; rmy3=0; ddrill=0.8;
    dscrew=1.78; wscrew = dscrew; screwxoffset = wbody-1.22; screwyoffset = hbody-1.27;
    style = "screwtop"; SMD_pads = False; SMD_padsize = []; specialtags = []; name_additions = []
    add_description = "https://www.bourns.com/pdfs/3266.pdf";
    makeSpindleTrimmer(footprint_name=footprint_name, class_name=class_name, ddrill=ddrill, wbody=wbody, hbody=hbody, pinxoffset=pinxoffset, pinyoffset=pinyoffset, rmx2=rmx2, rmy2=rmy2, rmx3=rmx3, rmy3=rmy3, dscrew=dscrew, wscrew=wscrew, screwxoffset=screwxoffset, screwyoffset=screwyoffset, style=style, SMD_pads=SMD_pads, SMD_padsize=SMD_padsize, specialtags=specialtags, add_description=add_description, classname="Potentiometer", lib_name="Potentiometers", name_additions=name_additions, script3d=script3d_tsl, height3d=height3d)
    footprint_name="Potentiometer_Trimmer_Bourns_3266Z"
    class_name="Bourns 3266Z"
    wbody=6.71; hbody=4.5; pinxoffset=(wbody-5.08)/2+5.08; pinyoffset=2.16; height3d = 6.71
    rmx2=-2.54; rmy2=0; rmx3=-5.08; rmy3=0; ddrill=0.8; dscrew = 1.78; wscrew = 1.52; screwxoffset = 0; screwyoffset = hbody- 1.27;
    style = "screwleft"; SMD_pads = False; SMD_padsize = []; specialtags = []; name_additions = []
    add_description = "https://www.bourns.com/pdfs/3266.pdf";
    makeSpindleTrimmer(footprint_name=footprint_name, class_name=class_name, ddrill=ddrill, wbody=wbody, hbody=hbody, pinxoffset=pinxoffset, pinyoffset=pinyoffset, rmx2=rmx2, rmy2=rmy2, rmx3=rmx3, rmy3=rmy3, dscrew=dscrew, wscrew=wscrew, screwxoffset=screwxoffset, screwyoffset=screwyoffset, style=style, SMD_pads=SMD_pads, SMD_padsize=SMD_padsize, specialtags=specialtags, add_description=add_description, classname="Potentiometer", lib_name="Potentiometers", name_additions=name_additions, script3d=script3d_tsl, height3d=height3d)
    footprint_name="Potentiometer_Trimmer_Bourns_3266W"
    class_name="Bourns 3266W"
    wbody=6.71; hbody=4.5; pinxoffset=(wbody-5.08)/2+5.08; pinyoffset=1.02; height3d = 6.71
    rmx2=-2.54; rmy2=2.54; rmx3=-5.08; rmy3=0; ddrill=0.8;
    dscrew=1.78; wscrew = dscrew; screwxoffset = wbody-1.27; screwyoffset = hbody-1.27;
    style = "screwtop"; SMD_pads = False; SMD_padsize = []; specialtags = []; name_additions = []
    add_description = "https://www.bourns.com/pdfs/3266.pdf";
    makeSpindleTrimmer(footprint_name=footprint_name, class_name=class_name, ddrill=ddrill, wbody=wbody, hbody=hbody, pinxoffset=pinxoffset, pinyoffset=pinyoffset, rmx2=rmx2, rmy2=rmy2, rmx3=rmx3, rmy3=rmy3, dscrew=dscrew, wscrew=wscrew, screwxoffset=screwxoffset, screwyoffset=screwyoffset, style=style, SMD_pads=SMD_pads, SMD_padsize=SMD_padsize, specialtags=specialtags, add_description=add_description, classname="Potentiometer", lib_name="Potentiometers", name_additions=name_additions, script3d=script3d_tsl, height3d=height3d)
    footprint_name="Potentiometer_Trimmer_Bourns_3266X"
    class_name="Bourns 3266X"
    wbody=6.71; hbody=4.5; pinxoffset=(wbody-5.08)/2+5.08; pinyoffset=1.02; height3d = 6.71
    rmx2=-2.54; rmy2=2.54; rmx3=-5.08; rmy3=0; ddrill=0.8;
    dscrew=1.78; wscrew = 1.52; screwxoffset = 0; screwyoffset = hbody-1.27;
    style = "screwleft"; SMD_pads = False; SMD_padsize = []; specialtags = []; name_additions = []
    add_description = "https://www.bourns.com/pdfs/3266.pdf";
    makeSpindleTrimmer(footprint_name=footprint_name, class_name=class_name, ddrill=ddrill, wbody=wbody, hbody=hbody, pinxoffset=pinxoffset, pinyoffset=pinyoffset, rmx2=rmx2, rmy2=rmy2, rmx3=rmx3, rmy3=rmy3, dscrew=dscrew, wscrew=wscrew, screwxoffset=screwxoffset, screwyoffset=screwyoffset, style=style, SMD_pads=SMD_pads, SMD_padsize=SMD_padsize, specialtags=specialtags, add_description=add_description, classname="Potentiometer", lib_name="Potentiometers", name_additions=name_additions, script3d=script3d_tsl, height3d=height3d)
    footprint_name="Potentiometer_Trimmer_Bourns_3266P"
    class_name="Bourns 3266P"
    wbody=6.71; hbody=6.71; pinxoffset=wbody/2; pinyoffset=(hbody-5.08)/2; height3d = 4.5
    rmx2=-2.54; rmy2=2.54; rmx3=0; rmy3=5.08; ddrill=0.8;
    dscrew=1.78; wscrew = 1.52; screwxoffset = 0; screwyoffset = 1.27;
    style = "screwleft"; SMD_pads = False; SMD_padsize = []; specialtags = []; name_additions = []
    add_description = "https://www.bourns.com/pdfs/3266.pdf";
    makeSpindleTrimmer(footprint_name=footprint_name, class_name=class_name, ddrill=ddrill, wbody=wbody, hbody=hbody, pinxoffset=pinxoffset, pinyoffset=pinyoffset, rmx2=rmx2, rmy2=rmy2, rmx3=rmx3, rmy3=rmy3, dscrew=dscrew, wscrew=wscrew, screwxoffset=screwxoffset, screwyoffset=screwyoffset, style=style, SMD_pads=SMD_pads, SMD_padsize=SMD_padsize, specialtags=specialtags, add_description=add_description, classname="Potentiometer", lib_name="Potentiometers", name_additions=name_additions, script3d=script3d_tsl, height3d=height3d)



    footprint_name="Potentiometer_Trimmer_Bourns_3269W"
    class_name="Bourns 3269W"
    wbody=6.35; hbody=4.32; pinxoffset=(wbody-5.08)/2+5.08; pinyoffset=-0.25; height3d = 7.44
    rmx2=-2.54; rmy2=4.83; rmx3=-5.08; rmy3=0; ddrill=0.8;
    dscrew=1.78; wscrew = dscrew; screwxoffset = wbody-1.002; screwyoffset = hbody-1.52;
    style = "screwtop"; SMD_pads = True; SMD_padsize = [1.19,2.79]; specialtags = []; name_additions = []
    add_description = "https://www.bourns.com/pdfs/3269.pdf";
    makeSpindleTrimmer(footprint_name=footprint_name, class_name=class_name, ddrill=ddrill, wbody=wbody, hbody=hbody, pinxoffset=pinxoffset, pinyoffset=pinyoffset, rmx2=rmx2, rmy2=rmy2, rmx3=rmx3, rmy3=rmy3, dscrew=dscrew, wscrew=wscrew, screwxoffset=screwxoffset, screwyoffset=screwyoffset, style=style, SMD_pads=SMD_pads, SMD_padsize=SMD_padsize, specialtags=specialtags, add_description=add_description, classname="Potentiometer", lib_name="Potentiometers", name_additions=name_additions, script3d=script3d_tsl, height3d=height3d)
    footprint_name="Potentiometer_Trimmer_Bourns_3269X"
    class_name="Bourns 3269X"
    wbody=6.35; hbody=4.32; pinxoffset=(wbody-5.08)/2+5.08; pinyoffset=-0.25; height3d = 7.44
    rmx2=-2.54; rmy2=4.83; rmx3=-5.08; rmy3=0; ddrill=0.8;
    dscrew=1.78; wscrew = 1.52; screwxoffset = 0; screwyoffset = hbody-1.52;
    style = "screwleft"; SMD_pads = True; SMD_padsize = [1.19,2.79]; specialtags = []; name_additions = []
    add_description = "https://www.bourns.com/pdfs/3269.pdf";
    makeSpindleTrimmer(footprint_name=footprint_name, class_name=class_name, ddrill=ddrill, wbody=wbody, hbody=hbody, pinxoffset=pinxoffset, pinyoffset=pinyoffset, rmx2=rmx2, rmy2=rmy2, rmx3=rmx3, rmy3=rmy3, dscrew=dscrew, wscrew=wscrew, screwxoffset=screwxoffset, screwyoffset=screwyoffset, style=style, SMD_pads=SMD_pads, SMD_padsize=SMD_padsize, specialtags=specialtags, add_description=add_description, classname="Potentiometer", lib_name="Potentiometers", name_additions=name_additions, script3d=script3d_tsl, height3d=height3d)
    footprint_name="Potentiometer_Trimmer_Bourns_3269P"
    class_name="Bourns 3269P"
    wbody=6.35; hbody=6.35; pinxoffset=-(wbody-6.4)/2+6.4; pinyoffset=(hbody-5.08)/2; height3d = 5.21
    rmx2=-6.4; rmy2=2.54; rmx3=0; rmy3=5.08; ddrill=0.8;
    dscrew=1.78; wscrew = 1.52; screwxoffset = 0; screwyoffset = 1.27;
    style = "screwleft"; SMD_pads = True; SMD_padsize = [3.3,1.19]; specialtags = []; name_additions = []
    add_description = "https://www.bourns.com/pdfs/3269.pdf";
    makeSpindleTrimmer(footprint_name=footprint_name, class_name=class_name, ddrill=ddrill, wbody=wbody, hbody=hbody, pinxoffset=pinxoffset, pinyoffset=pinyoffset, rmx2=rmx2, rmy2=rmy2, rmx3=rmx3, rmy3=rmy3, dscrew=dscrew, wscrew=wscrew, screwxoffset=screwxoffset, screwyoffset=screwyoffset, style=style, SMD_pads=SMD_pads, SMD_padsize=SMD_padsize, specialtags=specialtags, add_description=add_description, classname="Potentiometer", lib_name="Potentiometers", name_additions=name_additions, script3d=script3d_tsl, height3d=height3d)


    footprint_name="Potentiometer_Trimmer_Bourns_3214W"
    class_name="Bourns 3214W"
    wbody=4.8; hbody=3.5; pinxoffset=(wbody-2.5)/2+2.5; pinyoffset=0.3; height3d = 5.1
    rmx2=-1.25; rmy2=2.9; rmx3=-2.5; rmy3=0; ddrill=0.8;
    dscrew=1.5; wscrew = dscrew; screwxoffset = 1.2; screwyoffset = hbody-1.1;
    style = "screwtop"; SMD_pads = True; SMD_padsize = [1.3,1.6,2,1.6,1.3,1.6]; specialtags = []; name_additions = []
    add_description = "https://www.bourns.com/pdfs/3214.pdf";
    makeSpindleTrimmer(footprint_name=footprint_name, class_name=class_name, ddrill=ddrill, wbody=wbody, hbody=hbody, pinxoffset=pinxoffset, pinyoffset=pinyoffset, rmx2=rmx2, rmy2=rmy2, rmx3=rmx3, rmy3=rmy3, dscrew=dscrew, wscrew=wscrew, screwxoffset=screwxoffset, screwyoffset=screwyoffset, style=style, SMD_pads=SMD_pads, SMD_padsize=SMD_padsize, specialtags=specialtags, add_description=add_description, classname="Potentiometer", lib_name="Potentiometers", name_additions=name_additions, script3d=script3d_tsl, height3d=height3d)
    footprint_name="Potentiometer_Trimmer_Bourns_3214X"
    class_name="Bourns 3214X"
    wbody=4.8; hbody=3.5; pinxoffset=(wbody-2.5)/2+2.5; pinyoffset=-(5.1-3.5)/2; height3d = 5.3
    rmx2=-1.15; rmy2=5.1; rmx3=-2.3; rmy3=0; ddrill=0.8;
    dscrew=1.5; wscrew = dscrew; screwxoffset = 1.2; screwyoffset = hbody-1.1;
    style = "screwtop"; SMD_pads = True; SMD_padsize = [1.3,1.9,2,1.9,1.3,1.9]; specialtags = []; name_additions = []
    add_description = "https://www.bourns.com/pdfs/3214.pdf";
    makeSpindleTrimmer(footprint_name=footprint_name, class_name=class_name, ddrill=ddrill, wbody=wbody, hbody=hbody, pinxoffset=pinxoffset, pinyoffset=pinyoffset, rmx2=rmx2, rmy2=rmy2, rmx3=rmx3, rmy3=rmy3, dscrew=dscrew, wscrew=wscrew, screwxoffset=screwxoffset, screwyoffset=screwyoffset, style=style, SMD_pads=SMD_pads, SMD_padsize=SMD_padsize, specialtags=specialtags, add_description=add_description, classname="Potentiometer", lib_name="Potentiometers", name_additions=name_additions, script3d=script3d_tsl, height3d=height3d)
    footprint_name="Potentiometer_Trimmer_Bourns_3214G"
    class_name="Bourns 3214G"
    wbody=4.6; hbody=4.8; pinxoffset=(wbody-5.2)/2+5.2; pinyoffset=(hbody-2.3)/2; height3d = 3.71
    rmx2=-5.2; rmy2=1.15; rmx3=0; rmy3=2.3; ddrill=0.8;
    dscrew=1.78; wscrew = 0; screwxoffset = 0; screwyoffset = 1.27;
    style = "screwleft"; SMD_pads = True; SMD_padsize = [1.3,1.3,1.3,2,1.3,1.3]; specialtags = []; name_additions = []
    add_description = "https://www.bourns.com/pdfs/3214.pdf";
    makeSpindleTrimmer(footprint_name=footprint_name, class_name=class_name, ddrill=ddrill, wbody=wbody, hbody=hbody, pinxoffset=pinxoffset, pinyoffset=pinyoffset, rmx2=rmx2, rmy2=rmy2, rmx3=rmx3, rmy3=rmy3, dscrew=dscrew, wscrew=wscrew, screwxoffset=screwxoffset, screwyoffset=screwyoffset, style=style, SMD_pads=SMD_pads, SMD_padsize=SMD_padsize, specialtags=specialtags, add_description=add_description, classname="Potentiometer", lib_name="Potentiometers", name_additions=name_additions, script3d=script3d_tsl, height3d=height3d)
    footprint_name="Potentiometer_Trimmer_Bourns_3214J"
    class_name="Bourns 3214J"
    wbody=4.6; hbody=4.8; pinxoffset=(wbody-4)/2+4; pinyoffset=(hbody-2.3)/2; height3d = 3.71
    rmx2=-4; rmy2=1.15; rmx3=0; rmy3=2.3; ddrill=0.8;
    dscrew=1.78; wscrew = 0; screwxoffset = 0; screwyoffset = 1.27;
    style = "screwleft"; SMD_pads = True; SMD_padsize = [2,1.3,2,2,2,1.3]; specialtags = []; name_additions = []
    add_description = "https://www.bourns.com/pdfs/3214.pdf";
    makeSpindleTrimmer(footprint_name=footprint_name, class_name=class_name, ddrill=ddrill, wbody=wbody, hbody=hbody, pinxoffset=pinxoffset, pinyoffset=pinyoffset, rmx2=rmx2, rmy2=rmy2, rmx3=rmx3, rmy3=rmy3, dscrew=dscrew, wscrew=wscrew, screwxoffset=screwxoffset, screwyoffset=screwyoffset, style=style, SMD_pads=SMD_pads, SMD_padsize=SMD_padsize, specialtags=specialtags, add_description=add_description, classname="Potentiometer", lib_name="Potentiometers", name_additions=name_additions, script3d=script3d_tsl, height3d=height3d)

    footprint_name="Potentiometer_Trimmer_Vishay_TS53YJ"
    class_name="Vishay TS53YJ"
    wbody=5; hbody=5; pinxoffset=0.5+4; pinyoffset=(5-2.3)/2; height3d = 2.7
    rmx2=-4; rmy2=1.15; rmx3=0; rmy3=2.3; ddrill=0.8;
    dscrew=2.3; wscrew = dscrew; screwxoffset = wbody/2; screwyoffset = hbody/2;
    style = "screwtop"; screwstyle="cross"; SMD_pads = True; SMD_padsize = [2,1.3,2,2,2,1.3]; specialtags = []; name_additions = []
    add_description = "https://www.bourns.com/pdfs/3224.pdf";
    makeSpindleTrimmer(footprint_name=footprint_name, class_name=class_name, screwstyle=screwstyle, ddrill=ddrill, wbody=wbody, hbody=hbody, pinxoffset=pinxoffset, pinyoffset=pinyoffset, rmx2=rmx2, rmy2=rmy2, rmx3=rmx3, rmy3=rmy3, dscrew=dscrew, wscrew=wscrew, screwxoffset=screwxoffset, screwyoffset=screwyoffset, style=style, SMD_pads=SMD_pads, SMD_padsize=SMD_padsize, specialtags=specialtags, add_description=add_description, classname="Potentiometer", lib_name="Potentiometers", name_additions=name_additions, script3d=script3d_tsl, height3d=height3d)
    footprint_name="Potentiometer_Trimmer_Vishay_TS53YL"
    class_name="Vishay TS53YL"
    wbody=5; hbody=5; pinxoffset=-0.25+5.5; pinyoffset=(5-2.3)/2; height3d = 2.7
    rmx2=-5.5; rmy2=1.15; rmx3=0; rmy3=2.3; ddrill=0.8;
    dscrew=2.3; wscrew = dscrew; screwxoffset = wbody/2; screwyoffset = hbody/2;
    style = "screwtop"; screwstyle="cross"; SMD_pads = True; SMD_padsize = [1.3,1.3,2,1.3,1.3,1.3]; specialtags = []; name_additions = []
    add_description = "https://www.bourns.com/pdfs/3224.pdf";
    makeSpindleTrimmer(footprint_name=footprint_name, class_name=class_name, screwstyle=screwstyle, ddrill=ddrill, wbody=wbody, hbody=hbody, pinxoffset=pinxoffset, pinyoffset=pinyoffset, rmx2=rmx2, rmy2=rmy2, rmx3=rmx3, rmy3=rmy3, dscrew=dscrew, wscrew=wscrew, screwxoffset=screwxoffset, screwyoffset=screwyoffset, style=style, SMD_pads=SMD_pads, SMD_padsize=SMD_padsize, specialtags=specialtags, add_description=add_description, classname="Potentiometer", lib_name="Potentiometers", name_additions=name_additions, script3d=script3d_tsl, height3d=height3d)

    footprint_name="Potentiometer_Trimmer_Bourns_3224W"
    class_name="Bourns 3224W"
    wbody=4.8; hbody=3.5; pinxoffset=(wbody-2.5)/2+2.5; pinyoffset=0.3; height3d = 5.1
    rmx2=-1.25; rmy2=2.9; rmx3=-2.5; rmy3=0; ddrill=0.8;
    dscrew=1.5; wscrew = dscrew; screwxoffset = 1.2; screwyoffset = hbody-1.1;
    style = "screwtop"; SMD_pads = True; SMD_padsize = [1.3,1.6,2,1.6,1.3,1.6]; specialtags = []; name_additions = []
    add_description = "https://www.bourns.com/pdfs/3224.pdf";
    makeSpindleTrimmer(footprint_name=footprint_name, class_name=class_name, ddrill=ddrill, wbody=wbody, hbody=hbody, pinxoffset=pinxoffset, pinyoffset=pinyoffset, rmx2=rmx2, rmy2=rmy2, rmx3=rmx3, rmy3=rmy3, dscrew=dscrew, wscrew=wscrew, screwxoffset=screwxoffset, screwyoffset=screwyoffset, style=style, SMD_pads=SMD_pads, SMD_padsize=SMD_padsize, specialtags=specialtags, add_description=add_description, classname="Potentiometer", lib_name="Potentiometers", name_additions=name_additions, script3d=script3d_tsl, height3d=height3d)
    footprint_name="Potentiometer_Trimmer_Bourns_3224X"
    class_name="Bourns 3224X"
    wbody=4.8; hbody=3.5; pinxoffset=(wbody-2.5)/2+2.5; pinyoffset=-(5.1-3.5)/2; height3d = 5.3
    rmx2=-1.15; rmy2=5.1; rmx3=-2.3; rmy3=0; ddrill=0.8;
    dscrew=1.5; wscrew = dscrew; screwxoffset = 1.2; screwyoffset = hbody-1.1;
    style = "screwtop"; SMD_pads = True; SMD_padsize = [1.3,1.9,2,1.9,1.3,1.9]; specialtags = []; name_additions = []
    add_description = "https://www.bourns.com/pdfs/3224.pdf";
    makeSpindleTrimmer(footprint_name=footprint_name, class_name=class_name, ddrill=ddrill, wbody=wbody, hbody=hbody, pinxoffset=pinxoffset, pinyoffset=pinyoffset, rmx2=rmx2, rmy2=rmy2, rmx3=rmx3, rmy3=rmy3, dscrew=dscrew, wscrew=wscrew, screwxoffset=screwxoffset, screwyoffset=screwyoffset, style=style, SMD_pads=SMD_pads, SMD_padsize=SMD_padsize, specialtags=specialtags, add_description=add_description, classname="Potentiometer", lib_name="Potentiometers", name_additions=name_additions, script3d=script3d_tsl, height3d=height3d)
    footprint_name="Potentiometer_Trimmer_Bourns_3224G"
    class_name="Bourns 3224G"
    wbody=4.6; hbody=4.8; pinxoffset=(wbody-5.2)/2+5.2; pinyoffset=(hbody-2.3)/2; height3d = 3.71
    rmx2=-5.2; rmy2=1.15; rmx3=0; rmy3=2.3; ddrill=0.8;
    dscrew=1.78; wscrew = 0; screwxoffset = 0; screwyoffset = 1.27;
    style = "screwleft"; SMD_pads = True; SMD_padsize = [1.3,1.3,1.3,2,1.3,1.3]; specialtags = []; name_additions = []
    add_description = "https://www.bourns.com/pdfs/3224.pdf";
    makeSpindleTrimmer(footprint_name=footprint_name, class_name=class_name, ddrill=ddrill, wbody=wbody, hbody=hbody, pinxoffset=pinxoffset, pinyoffset=pinyoffset, rmx2=rmx2, rmy2=rmy2, rmx3=rmx3, rmy3=rmy3, dscrew=dscrew, wscrew=wscrew, screwxoffset=screwxoffset, screwyoffset=screwyoffset, style=style, SMD_pads=SMD_pads, SMD_padsize=SMD_padsize, specialtags=specialtags, add_description=add_description, classname="Potentiometer", lib_name="Potentiometers", name_additions=name_additions, script3d=script3d_tsl, height3d=height3d)
    footprint_name="Potentiometer_Trimmer_Bourns_3224J"
    class_name="Bourns 3224J"
    wbody=4.6; hbody=4.8; pinxoffset=(wbody-4)/2+4; pinyoffset=(hbody-2.3)/2; height3d = 3.71
    rmx2=-4; rmy2=1.15; rmx3=0; rmy3=2.3; ddrill=0.8;
    dscrew=1.78; wscrew = 0; screwxoffset = 0; screwyoffset = 1.27;
    style = "screwleft"; SMD_pads = True; SMD_padsize = [2,1.3,2,2,2,1.3]; specialtags = []; name_additions = []
    add_description = "https://www.bourns.com/pdfs/3224.pdf";
    makeSpindleTrimmer(footprint_name=footprint_name, class_name=class_name, ddrill=ddrill, wbody=wbody, hbody=hbody, pinxoffset=pinxoffset, pinyoffset=pinyoffset, rmx2=rmx2, rmy2=rmy2, rmx3=rmx3, rmy3=rmy3, dscrew=dscrew, wscrew=wscrew, screwxoffset=screwxoffset, screwyoffset=screwyoffset, style=style, SMD_pads=SMD_pads, SMD_padsize=SMD_padsize, specialtags=specialtags, add_description=add_description, classname="Potentiometer", lib_name="Potentiometers", name_additions=name_additions, script3d=script3d_tsl, height3d=height3d)
    
    
    
    