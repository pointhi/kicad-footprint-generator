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
from drawing_tools import *
from footprint_global_properties import *


# screate potentiometer footprints, vertically mounted
#
# style=normal:
#        ^   ^      +-----------+
# pinyoffset |      |           |
#        v   |   ^  |   O1   O4 +-------+                                              ^
#            | rmy  |           |       +-------------------------------+ ^            |
#            |   v  |   O2   O5 |       |                               | dshaft       |
#            |      |           |       +-------------------------------+ v            dscrew
#            hbody  |   O3   O6 +-------+                                              v
#            |      |           |
#            v      +-----------+       <----------wshaft--------------->
#                        <rmx>  <------->wscrew
#                   <---wbody--->
#                             <->pinxoffset
#
#
# style=trimmer (only valid for 3-pin!!!):
#  as above, but pins:
#
#    O1           ^
#                 rmy
#            O2   v
#
#    O3
#     <-rmx-->
def makePotentiometerVertical(footprint_name, class_name, wbody, hbody, wscrew, dscrew, wshaft, dshaft, style="normal", pinxoffset=0,
                              pinyoffset=0, pins=3, rmx=5.08, rmy=5.08, ddrill=1.5, R_POW=0, x_3d=[0, 0, 0],
                              s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialtags=[], add_description="",
                              classname="Potentiometer", lib_name="Potentiometers", name_additions=[], script3d="",
                              height3d=10, screwzpos=5, mh_ddrill=1.5, mh_count=0, mh_rmx=0, mh_rmy=15, mh_xoffset=0,
                              mh_yoffset=0):
    padx = 1.8 * ddrill
    pady = padx
    txtoffset = txt_offset
    
    pad1style = Pad.SHAPE_CIRCLE
    
    cols = pins / 3
    overpadwidth = rmx * (cols - 1) + padx
    overpadheight = rmy * 2 + pady
    # crt_offset=0.75
    
    
    padpos = []
    offset = [0, 0]
    if pins >= 3:
        if style=="trimmer":
            padpos.append([3, 0, 2 * rmy, ddrill, padx, pady])
            padpos.append([2, rmx, rmy, ddrill, padx, pady])
            padpos.append([1, 0, 0, ddrill, padx, pady])
            offset = [0, 0]
        else:
            padpos.append([3, 0, 0, ddrill, padx, pady])
            padpos.append([2, 0, rmy, ddrill, padx, pady])
            padpos.append([1, 0, 2 * rmy, ddrill, padx, pady])
            offset = [0, -2 * rmy]
    if pins >= 6:
        padpos.append([6, -rmx, 0, ddrill, padx, pady])
        padpos.append([5, -rmx, rmy, ddrill, padx, pady])
        padpos.append([4, -rmx, 2 * rmy, ddrill, padx, pady])
    if pins >= 9:
        padpos.append([9, -2*rmx, 0, ddrill, padx, pady])
        padpos.append([8, -2*rmx, rmy, ddrill, padx, pady])
        padpos.append([7, -2*rmx, 2 * rmy, ddrill, padx, pady])

    if mh_count == 1:
        padpos.append([0, mh_xoffset, -mh_yoffset, mh_ddrill, 2 * mh_ddrill, 2 * mh_ddrill])
    if mh_count == 2:
        padpos.append([0, mh_xoffset, -mh_yoffset, mh_ddrill, 2 * mh_ddrill, 2 * mh_ddrill])
        padpos.append([0, mh_xoffset - mh_rmx, -mh_yoffset + mh_rmy, mh_ddrill, 2 * mh_ddrill, 2 * mh_ddrill])
    if mh_count == 4:
        padpos.append([0, mh_xoffset, -mh_yoffset, mh_ddrill, 2 * mh_ddrill, 2 * mh_ddrill])
        padpos.append([0, mh_xoffset - mh_rmx, -mh_yoffset + mh_rmy, mh_ddrill, 2 * mh_ddrill, 2 * mh_ddrill])
        padpos.append([0, mh_xoffset - mh_rmx, -mh_yoffset, mh_ddrill, 2 * mh_ddrill, 2 * mh_ddrill])
        padpos.append([0, mh_xoffset, -mh_yoffset + mh_rmy, mh_ddrill, 2 * mh_ddrill, 2 * mh_ddrill])
    
    lbody_fab = -(wbody - pinxoffset)
    tbody_fab = -pinyoffset
    wbody_fab = wbody
    hbody_fab = hbody
    
    wscrew_fab = wscrew
    hscrew_fab = dscrew
    lscrew_fab = lbody_fab + wbody_fab
    tscrew_fab = tbody_fab + (hbody_fab - hscrew_fab) / 2.0
    
    wshaft_fab = wshaft
    hshaft_fab = dshaft
    lshaft_fab = lscrew_fab + wscrew_fab
    tshaft_fab = tbody_fab + (hbody_fab - hshaft_fab) / 2.0
    
    lbody_slk = lbody_fab - math.copysign( slk_offset,wbody_fab)
    tbody_slk = tbody_fab - slk_offset
    wbody_slk = wbody_fab + math.copysign(2 * slk_offset,wbody_fab)
    hbody_slk = hbody_fab + 2 * slk_offset
    
    lscrew_slk = lbody_slk + wbody_slk
    tscrew_slk = tscrew_fab - slk_offset
    wscrew_slk = wscrew_fab
    hscrew_slk = hscrew_fab + 2* slk_offset

    lshaft_slk = lscrew_slk + wscrew_slk
    tshaft_slk = tshaft_fab - slk_offset
    wshaft_slk = wshaft_fab
    hshaft_slk = hshaft_fab + 2*slk_offset

    if wbody_fab < 0:
        wscrew_slk = wscrew_slk + 2 * slk_offset
        wshaft_slk = wshaft_slk + 2 * slk_offset

    minx = miny = 1e99
    maxx = maxy = -1e99
    for p in padpos:
        maxx = max(maxx, p[1] + p[4] / 2)
        minx = min(minx, p[1] - p[4] / 2)
        maxy = max(maxy, p[2] + p[5] / 2)
        miny = min(miny, p[2] - p[5] / 2)
    
    minx = min(minx, lbody_fab, lbody_fab + wbody_fab + wscrew_fab + wshaft_fab)
    miny = min(miny, tbody_fab, tscrew_fab, tshaft_fab)
    maxx = max(maxx, lbody_fab + wbody_fab + wscrew_fab + wshaft_fab, lbody_fab)
    maxy = max(maxy, tbody_fab + hbody_fab, tscrew_fab + hscrew_fab, tshaft_fab + hshaft_fab)
    
    h_crt = (maxy - miny) + 2 * crt_offset
    w_crt = (maxx - minx) + 2 * crt_offset
    l_crt = minx - crt_offset
    t_crt = miny - crt_offset
    
    pow_rat = ""
    if R_POW > 0:
        pow_rat = "{0}W".format(R_POW)
        if (1 / R_POW == int(1 / R_POW)):
            pow_rat = pow_rat + " = 1/{0}W".format(int(1 / R_POW))
    
    tgs = specialtags
    if len(class_name) > 0:
        tgs.append(class_name)
    if len(pow_rat) > 0:
        tgs.append(pow_rat)
    
    description = "Potentiometer, vertically mounted"
    tags = "Potentiometer vertical"
    for t in tgs:
        if len(description) > 0: description = description + ", "
        description = description + t
        if len(tags) > 0: tags = tags + " "
        tags = tags + " " + t
    
    if len(add_description) > 0:
        if len(description) > 0: description = description + ", "
        description = description + add_description
    
    footprint_name = footprint_name + "_Vertical"

    for n in name_additions:
        if len(n) > 0:
            footprint_name = footprint_name + "_" + n
    print(footprint_name)
    
    if script3d != "":
        with open(script3d, "a") as myfile:
            myfile.write("\n\n # {0}\n".format(footprint_name))
            myfile.write("import FreeCAD\n")
            myfile.write("import os\n")
            myfile.write("import os.path\n\n")
            myfile.write("App.ActiveDocument.clearAll()\n")

            line=0
            line += 1; script3d_writevariable(myfile, line, 'lbody_fab', min(lbody_fab+wbody_fab,lbody_fab)+offset[0])
            line += 1; script3d_writevariable(myfile, line, 'tbody_fab', min(tbody_fab+hbody_fab,tbody_fab)+offset[1])
            line += 1; script3d_writevariable(myfile, line, 'wbody_fab', math.fabs(wbody_fab))
            line += 1; script3d_writevariable(myfile, line, 'hbody_fab', math.fabs(hbody_fab))
            line += 1; script3d_writevariable(myfile, line, 'lscrew_fab', min(lscrew_fab+wscrew_fab,lscrew_fab)+offset[0])
            line += 1; script3d_writevariable(myfile, line, 'tscrew_fab', min(tscrew_fab+hscrew_fab,tscrew_fab)+offset[1])
            line += 1; script3d_writevariable(myfile, line, 'wscrew_fab', math.fabs(wscrew_fab))
            line += 1; script3d_writevariable(myfile, line, 'hscrew_fab', math.fabs(hscrew_fab))
            line += 1; script3d_writevariable(myfile, line, 'lshaft_fab', min(lshaft_fab+wshaft_fab,lshaft_fab)+offset[0])
            line += 1; script3d_writevariable(myfile, line, 'tshaft_fab', min(tshaft_fab+hshaft_fab,tshaft_fab)+offset[1])
            line += 1; script3d_writevariable(myfile, line, 'wshaft_fab', math.fabs(wshaft_fab))
            line += 1; script3d_writevariable(myfile, line, 'hshaft_fab', math.fabs(hshaft_fab))
            line += 1; script3d_writevariable(myfile, line, 'rmx', rmx)
            line += 1; script3d_writevariable(myfile, line, 'rmy', rmy)
            for p in padpos:
                if p[0]==1:
                    line += 1;
                    script3d_writevariable(myfile, line, 'padx', p[1])
                    line += 1;
                    script3d_writevariable(myfile, line, 'pady', p[2])
            line += 1; script3d_writevariable(myfile, line, 'd_wire', ddrill-0.3)
            line += 1; script3d_writevariable(myfile, line, 'height', height3d)
            line += 1; script3d_writevariable(myfile, line, 'screwzpos', screwzpos)
            written=False
            for p in padpos:
                if p[0] == 0 and not written:
                    line += 1;
                    script3d_writevariable(myfile, line, 'mhpadx', p[1])
                    line += 1;
                    script3d_writevariable(myfile, line, 'mhpady', p[2])
                    written=True
            line += 1; script3d_writevariable(myfile, line, 'mh_rmx', mh_rmx)
            line += 1; script3d_writevariable(myfile, line, 'mh_rmy', mh_rmy)
            line += 1; script3d_writevariable(myfile, line, 'offsetx', offset[0])
            line += 1; script3d_writevariable(myfile, line, 'offsety', offset[1])


            myfile.write("App.ActiveDocument.recompute()\n\n")
            myfile.write("doc = FreeCAD.activeDocument()\n")
            myfile.write("__objs__=[]\n")
            myfile.write("for obj in doc.Objects:	\n")
            myfile.write("    if obj.ViewObject.Visibility:\n")
            myfile.write("        __objs__.append(obj)\n")
            myfile.write("\nFreeCADGui.export(__objs__,os.path.split(doc.FileName)[0]+os.sep+\"{0}.wrl\")\n".format(
                footprint_name))
            myfile.write("doc.saveCopy(os.path.split(doc.FileName)[0]+os.sep+\"{0}.FCStd\")\n".format(footprint_name))
            myfile.write("print(\"created {0}\")\n".format(footprint_name))
    
    # init kicad footprint
    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription(description)
    kicad_mod.setTags(tags)
    
    kicad_modg = Translation(offset[0], offset[1])
    kicad_mod.append(kicad_modg)
    
    # set general values
    kicad_modg.append(Text(type='reference', text='REF**', at=[0, t_crt - txtoffset], layer='F.SilkS'))
    kicad_modg.append(Text(type='value', text=footprint_name, at=[0, t_crt + h_crt + txtoffset], layer='F.Fab'))
    
    # create FAB-layer
    kicad_modg.append(
        RectLine(start=[lbody_fab, tbody_fab], end=[lbody_fab + wbody_fab, tbody_fab + hbody_fab], layer='F.Fab',
                 width=lw_fab))
    if wscrew_fab * hscrew_fab != 0:
        kicad_modg.append(
            RectLine(start=[lscrew_fab, tscrew_fab], end=[lscrew_fab + wscrew_fab, tscrew_fab + hscrew_fab],
                     layer='F.Fab', width=lw_fab))
    if wshaft_fab * hshaft_fab != 0:
        kicad_modg.append(
            RectLine(start=[lshaft_fab, tshaft_fab], end=[lshaft_fab + wshaft_fab, tshaft_fab + hshaft_fab],
                     layer='F.Fab', width=lw_fab))
    
    # build keepeout for SilkScreen
    keepouts = []
    for p in padpos:
        keepouts = keepouts + addKeepoutRound(p[1], p[2], p[4] + 2 * lw_slk + 2 * slk_offset,
                                              p[5] + 2 * lw_slk + 2 * slk_offset)
    
    # create SILKSCREEN-layer
    addRectWithKeepout(kicad_modg, lbody_slk, tbody_slk, wbody_slk, hbody_slk, 'F.SilkS', lw_slk, keepouts, 0.001)
    if wscrew>0 and wscrew_slk * hscrew_slk != 0:
        addRectWithKeepout(kicad_modg, lscrew_slk, tscrew_slk, wscrew_slk, hscrew_slk, 'F.SilkS', lw_slk, keepouts,
                           0.001)
    if wshaft>0 and wshaft_slk * hshaft_slk != 0:
        addRectWithKeepout(kicad_modg, lshaft_slk, tshaft_slk, wshaft_slk, hshaft_slk, 'F.SilkS', lw_slk, keepouts,
                           0.001)
    
    # create courtyard
    kicad_mod.append(RectLine(start=[roundCrt(l_crt + offset[0]), roundCrt(t_crt + offset[1])],
                              end=[roundCrt(l_crt + w_crt + offset[0]), roundCrt(t_crt + h_crt + offset[1])],
                              layer='F.CrtYd', width=lw_crt))
    
    # create pads
    pn = 1
    for p in padpos:
        ps = Pad.SHAPE_CIRCLE
        if p[0] == 1:
            ps = pad1style
        kicad_modg.append(Pad(number=p[0], type=Pad.TYPE_THT, shape=ps, at=[p[1], p[2]], size=[p[4], p[5]], drill=p[3],
                              layers=['*.Cu', '*.Mask']))
    
    # add model
    if (has3d != 0):
        kicad_modg.append(
            Model(filename=lib_name + ".3dshapes/" + footprint_name + ".wrl", at=x_3d, scale=s_3d, rotate=[0, 0, 0]))
    
    # print render tree
    # print(kicad_mod.getRenderTree())
    # print(kicad_mod.getCompleteRenderTree())
    
    # write file
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile(footprint_name + '.kicad_mod')


# screate potentiometer footprints, vertically mounted
#
# style=normal
#                    <-->pinxoffset
#        ^   ^          +---------------+ ^
# pinyoffset |          |               | |
#        v   |   ^  O1  |               | cofsety
#            | rmy      |     CCCCC     | |
#            |   v  O2  |     CCCCC     | v
#            |          |     CCCCC     |
#            hbody  O3  |               |
#            |          |               |
#            v          +---------------+
#                       <------->coffsetx
#                       <-----wbody----->
#
#
# style=trimmer (only valid for 3-pin!!!):
#  as above, but pins:
#
#    O1           ^
#                 rmy
#            O2   v
#
#    O3
#     <-rmx-->
#
def makePotentiometerHorizontal(footprint_name, class_name, wbody, hbody, deco="none", style="normal", d_body=0,
                                dshaft=6, dscrew=7, c_ddrill=0, c_offsetx=0, c_offsety=0, pinxoffset=0,
                                pinyoffset=0, pins=3, rmx=5.08, rmy=5.08, ddrill=1.5, mount_below=True, SMD_pads=False,
                                SMD_padsize=[], SMD_type="3-5", R_POW=0, x_3d=[0, 0, 0],
                                s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialtags=[], add_description="",
                                classname="Potentiometer", lib_name="Potentiometers", name_additions=[], script3d="",
                                height3d=10, mh_ddrill=1.5, mh_count=0, mh_rmx=0, mh_rmy=15, mh_xoffset=0, mh_yoffset=0,
                                mh_smd=False, mh_padsize=[], mh_nopads=False):
    padx = 1.8 * ddrill
    pady = padx
    if SMD_pads and len(SMD_padsize) >= 2:
        padx = SMD_padsize[0]
        pady = SMD_padsize[1]
    
    txtoffset = txt_offset
    
    pad1style = Pad.SHAPE_CIRCLE
    
    cols = pins / 3
    overpadwidth = rmx * (cols - 1) + padx
    overpadheight = rmy * 2 + pady
    # crt_offset=0.75
    
    
    padpos = []
    offset = [0, 0]
    padtype = Pad.TYPE_THT
    padstyle = Pad.SHAPE_CIRCLE
    if SMD_pads:
        padtype = Pad.TYPE_SMT
        padstyle = Pad.SHAPE_RECT
    mhtype = Pad.TYPE_NPTH
    mhstyle = Pad.SHAPE_CIRCLE
    if mh_smd:
        mhtype = Pad.TYPE_SMT
        mhstyle = Pad.SHAPE_RECT
    if pins >= 3:
        if style == "trimmer":
            padpos.append([3, 0, 0, ddrill, padx, pady, padtype, padstyle])
            padpos.append([2, rmx, rmy, ddrill, padx, pady, padtype, padstyle])
            padpos.append([1, 0, 2 * rmy, ddrill, padx, pady, padtype, padstyle])
            offset = [0, -2 * rmy]
            if SMD_pads:
                offset = [-rmx/2, -rmy]
        else:
            padpos.append([3, 0, 0, ddrill, padx, pady, padtype, padstyle])
            padpos.append([2, 0, rmy, ddrill, padx, pady, padtype, padstyle])
            padpos.append([1, 0, 2 * rmy, ddrill, padx, pady, padtype, padstyle])
            offset = [0, -2 * rmy]
            if SMD_pads:
                offset = [0, -rmy]
    if pins == 4:
        padpos.append([4, 0, -rmy, ddrill, padx, pady, padtype, padstyle])
    if pins == 5 and SMD_pads and SMD_type == "3-5":
        padpos.append([5, -rmx, 0, ddrill, padx, pady, padtype, padstyle])
        padpos.append([4, -rmx, 2 * rmy, ddrill, padx, pady, padtype, padstyle])
        if SMD_pads:
            offset[0] = -rmx / 2
    if pins >= 6:
        padpos.append([6, -rmx, 0, ddrill, padx, pady, padtype, padstyle])
        padpos.append([5, -rmx, rmy, ddrill, padx, pady, padtype, padstyle])
        padpos.append([4, -rmx, 2 * rmy, ddrill, padx, pady, padtype, padstyle])
        if SMD_pads:
            offset[0] = -rmx / 2
    if pins >= 9:
        padpos.append([9, -2 * rmx, 0, ddrill, padx, pady, padtype, padstyle])
        padpos.append([8, -2 * rmx, rmy, ddrill, padx, pady, padtype, padstyle])
        padpos.append([7, -2 * rmx, 2 * rmy, ddrill, padx, pady, padtype, padstyle])
        if SMD_pads:
            offset[0] = -rmx
    
    mhpadsizex = 2 * mh_ddrill
    mhpadsizey = mhpadsizex
    if mh_nopads:
        mhpadsizex = mh_ddrill
        mhpadsizey = mhpadsizex
    if mh_smd and len(mh_padsize) >= 2:
        mhpadsizex = mh_padsize[0]
        mhpadsizey = mh_padsize[1]
    
    if mh_count == 1:
        padpos.append([0, mh_xoffset, -mh_yoffset, mh_ddrill, mhpadsizex, mhpadsizey, mhtype, mhstyle])
    if mh_count == 2:
        padpos.append([0, mh_xoffset, -mh_yoffset, mh_ddrill, mhpadsizex, mhpadsizey, mhtype, mhstyle])
        padpos.append(
            [0, mh_xoffset - mh_rmx, -mh_yoffset + mh_rmy, mh_ddrill, mhpadsizex, mhpadsizey, mhtype, mhstyle])
    if mh_count == 4:
        padpos.append([0, mh_xoffset, -mh_yoffset, mh_ddrill, mhpadsizex, mhpadsizey, mhtype, mhstyle])
        padpos.append(
            [0, mh_xoffset - mh_rmx, -mh_yoffset + mh_rmy, mh_ddrill, mhpadsizex, mhpadsizey, mhtype, mhstyle])
        padpos.append([0, mh_xoffset - mh_rmx, -mh_yoffset, mh_ddrill, mhpadsizex, mhpadsizey, mhtype, mhstyle])
        padpos.append([0, mh_xoffset, -mh_yoffset + mh_rmy, mh_ddrill, mhpadsizex, mhpadsizey, mhtype, mhstyle])
    
    lbody_fab = pinxoffset
    tbody_fab = -pinyoffset
    wbody_fab = wbody
    hbody_fab = hbody
    cdbody_fab = d_body
    clbody_fab = lbody_fab + c_offsetx
    ctbody_fab = tbody_fab + c_offsety
    
    if mount_below and c_ddrill > 0:
        padpos.append([0, clbody_fab, ctbody_fab, c_ddrill, c_ddrill, c_ddrill, mhtype, mhstyle])
    
    lbody_slk = lbody_fab - slk_offset
    tbody_slk = tbody_fab - slk_offset
    wbody_slk = wbody_fab + 2 * slk_offset
    hbody_slk = hbody_fab + 2 * slk_offset
    cdbody_slk = cdbody_fab + 2 * slk_offset
    clbody_slk = clbody_fab
    ctbody_slk = ctbody_fab
    
    minx = miny = 1e99
    maxx = maxy = -1e99
    for p in padpos:
        maxx = max(maxx, p[1] + p[4] / 2)
        minx = min(minx, p[1] - p[4] / 2)
        maxy = max(maxy, p[2] + p[5] / 2)
        miny = min(miny, p[2] - p[5] / 2)
    
    minx = min(minx, lbody_fab, clbody_fab - cdbody_fab / 2)
    miny = min(miny, tbody_fab, ctbody_fab - cdbody_fab / 2)
    maxx = max(maxx, lbody_fab + wbody_fab, clbody_fab + cdbody_fab / 2)
    maxy = max(maxy, tbody_fab + hbody_fab, ctbody_fab + cdbody_fab / 2)
    
    h_crt = (maxy - miny) + 2 * crt_offset
    w_crt = (maxx - minx) + 2 * crt_offset
    l_crt = minx - crt_offset
    t_crt = miny - crt_offset
    
    pow_rat = ""
    if R_POW > 0:
        pow_rat = "{0}W".format(R_POW)
        if (1 / R_POW == int(1 / R_POW)):
            pow_rat = pow_rat + " = 1/{0}W".format(int(1 / R_POW))
    
    tgs = specialtags
    if len(class_name) > 0:
        tgs.append(class_name)
    if len(pow_rat) > 0:
        tgs.append(pow_rat)
    
    description = "Potentiometer, horizontally mounted"
    tags = "Potentiometer horizontal"
    if mount_below:
        description = description + ", mounted from below"
        tags = tags + " mounted from below lower-side"
    for t in tgs:
        if len(description) > 0: description = description + ", "
        description = description + t
        if len(tags) > 0: tags = tags + " "
        tags = tags + " " + t
    
    if len(add_description) > 0:
        if len(description) > 0: description = description + ", "
        description = description + add_description
    
    footprint_name = footprint_name + "_Horizontal"
    for n in name_additions:
        if len(n) > 0:
            footprint_name = footprint_name + "_" + n
    
    if mount_below:
        footprint_name = footprint_name + "_MountLS"
    print(footprint_name)
    
    if script3d != "":
        with open(script3d, "a") as myfile:
            myfile.write("\n\n # {0}\n".format(footprint_name))
            myfile.write("import FreeCAD\n")
            myfile.write("import os\n")
            myfile.write("import os.path\n\n")

            myfile.write("App.ActiveDocument.clearAll()\n")
            
            line = 0
            line += 1; script3d_writevariable(myfile, line, 'lbody_fab', min(lbody_fab+wbody_fab,lbody_fab)+offset[0])
            line += 1; script3d_writevariable(myfile, line, 'tbody_fab', min(tbody_fab+hbody_fab,tbody_fab)+offset[1])
            line += 1; script3d_writevariable(myfile, line, 'wbody_fab', math.fabs(wbody_fab))
            line += 1; script3d_writevariable(myfile, line, 'hbody_fab', math.fabs(hbody_fab))
            line += 1; script3d_writevariable(myfile, line, 'clbody_fab', clbody_fab+offset[0])
            line += 1; script3d_writevariable(myfile, line, 'ctbody_fab', ctbody_fab+offset[1])
            line += 1; script3d_writevariable(myfile, line, 'cdbody_fab', cdbody_fab)
            line += 1; script3d_writevariable(myfile, line, 'dscrew', dscrew)
            line += 1; script3d_writevariable(myfile, line, 'dshaft', dshaft)
            line += 1; script3d_writevariable(myfile, line, 'rmx', rmx)
            line += 1; script3d_writevariable(myfile, line, 'rmy', rmy)
            for p in padpos:
                if p[0] == 1:
                    line += 1;
                    script3d_writevariable(myfile, line, 'padx', p[1])
                    line += 1;
                    script3d_writevariable(myfile, line, 'pady', p[2])
            line += 1; script3d_writevariable(myfile, line, 'd_wire', ddrill-0.3)
            line += 1; script3d_writevariable(myfile, line, 'height', height3d)
            written=False
            for p in padpos:
                if p[0] == 0 and not written:
                    line += 1;
                    script3d_writevariable(myfile, line, 'mhpadx', p[1])
                    line += 1;
                    script3d_writevariable(myfile, line, 'mhpady', p[2])
                    written=True
            line += 1; script3d_writevariable(myfile, line, 'mh_rmx', mh_rmx)
            line += 1; script3d_writevariable(myfile, line, 'mh_rmy', mh_rmy)
            line += 1; script3d_writevariable(myfile, line, 'offsetx', offset[0])
            line += 1; script3d_writevariable(myfile, line, 'offsety', offset[1])

            myfile.write("App.ActiveDocument.recompute()\n\n")
            myfile.write("doc = FreeCAD.activeDocument()\n")
            myfile.write("__objs__=[]\n")
            myfile.write("for obj in doc.Objects:	\n")
            myfile.write("    if obj.ViewObject.Visibility:\n")
            myfile.write("        __objs__.append(obj)\n")
            myfile.write("\nFreeCADGui.export(__objs__,os.path.split(doc.FileName)[0]+os.sep+\"{0}.wrl\")\n".format(
                footprint_name))
            myfile.write("doc.saveCopy(os.path.split(doc.FileName)[0]+os.sep+\"{0}.FCStd\")\n".format(footprint_name))
            myfile.write("print(\"created {0}\")\n".format(footprint_name))
    
    # init kicad footprint
    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription(description)
    kicad_mod.setTags(tags)
    if SMD_pads:
        kicad_mod.setAttribute('smd')
    
    kicad_modg = Translation(offset[0], offset[1])
    kicad_mod.append(kicad_modg)
    
    # set general values
    kicad_modg.append(Text(type='reference', text='REF**', at=[l_crt + w_crt / 2, t_crt - txtoffset], layer='F.SilkS'))
    kicad_modg.append(
        Text(type='value', text=footprint_name, at=[l_crt + w_crt / 2, t_crt + h_crt + txtoffset], layer='F.Fab'))
    
    # create FAB-layer
    layer = 'F'
    if mount_below:
        layer = 'B'
    drawbody = wbody > 0
    if cdbody_fab > 0:
        if style == "trimmer":
            dy = hbody_fab / 2
            if drawbody and dy <= cdbody_fab / 2:
                dx = math.sqrt(cdbody_fab * cdbody_fab / 4 - dy * dy)
                alpha = 360 - 2 * math.atan(dy / dy) / 3.1415 * 180
                kicad_modg.append(PolygoneLine(polygone=[
                    [clbody_fab - dx, ctbody_fab - dy],
                    [lbody_fab, ctbody_fab - dy],
                    [lbody_fab, ctbody_fab + dy],
                    [clbody_fab - dx, ctbody_fab + dy]
                ], layer=layer + '.Fab', width=lw_fab))
                kicad_modg.append(
                    Arc(center=[clbody_fab, ctbody_fab], start=[clbody_fab - dx, ctbody_fab - dy], angle=alpha,
                        layer=layer + '.Fab', width=lw_fab))
            else:
                kicad_modg.append(
                    Circle(center=[clbody_fab, ctbody_fab], radius=cdbody_fab / 2, layer=layer + '.Fab', width=lw_fab))
                if drawbody:
                    kicad_modg.append(
                        RectLine(start=[lbody_fab, tbody_fab], end=[lbody_fab + wbody_fab, tbody_fab + hbody_fab],
                                 layer=layer + '.Fab', width=lw_fab))
        else:
            kicad_modg.append(
                Circle(center=[clbody_fab, ctbody_fab], radius=cdbody_fab / 2, layer=layer + '.Fab', width=lw_fab))
            dy = hbody_fab / 2
            if drawbody and dy <= cdbody_fab / 2:
                dx = math.sqrt(cdbody_fab * cdbody_fab / 4 - dy * dy)
                kicad_modg.append(PolygoneLine(polygone=[
                    [clbody_fab - dx, ctbody_fab - dy],
                    [lbody_fab, ctbody_fab - dy],
                    [lbody_fab, ctbody_fab + dy],
                    [clbody_fab - dx, ctbody_fab + dy]
                ], layer=layer + '.Fab', width=lw_fab))
            elif drawbody:
                kicad_modg.append(
                    RectLine(start=[lbody_fab, tbody_fab], end=[lbody_fab + wbody_fab, tbody_fab + hbody_fab],
                             layer=layer + '.Fab', width=lw_fab))
    elif drawbody:
        kicad_modg.append(RectLine(start=[lbody_fab, tbody_fab], end=[lbody_fab + wbody_fab, tbody_fab + hbody_fab],
                                   layer=layer + '.Fab', width=lw_fab))
    
    if dscrew > 0:
        kicad_modg.append(
            Circle(center=[clbody_fab, ctbody_fab], radius=dscrew / 2, layer=layer + '.Fab', width=lw_fab))
        if deco == "slit":
            addSlitScrew(kicad_modg, clbody_fab, ctbody_fab, dscrew / 2, layer + '.Fab', lw_fab)
        elif deco == "cross":
            addCrossScrew(kicad_modg, clbody_fab, ctbody_fab, dscrew / 2, layer + '.Fab', lw_fab)
    if dshaft > 0: kicad_modg.append(
        Circle(center=[clbody_fab, ctbody_fab], radius=dshaft / 2, layer=layer + '.Fab', width=lw_fab))
    
    # build keepeout for SilkScreen
    keepouts = []
    for p in padpos:
        if p[7] == Pad.SHAPE_CIRCLE:
            keepouts = keepouts + addKeepoutRound(p[1], p[2], p[4] + 2 * lw_slk + 2 * slk_offset,
                                                  p[5] + 2 * lw_slk + 2 * slk_offset)
        else:
            keepouts = keepouts + addKeepoutRect(p[1], p[2], p[4] + 2 * lw_slk + 2 * slk_offset,
                                                 p[5] + 2 * lw_slk + 2 * slk_offset)
    # debug_draw_keepouts(kicad_modg,keepouts)
    
    # create SILKSCREEN-layer
    drawbody = wbody > 0
    if cdbody_fab > 0:
        addCircleWithKeepout(kicad_modg, clbody_slk, ctbody_slk, cdbody_slk / 2, layer + '.SilkS', lw_slk, keepouts)
        if mount_below:
            addDCircleWithKeepout(kicad_modg, clbody_slk, ctbody_slk, cdbody_slk / 2, 'F.SilkS', lw_slk, keepouts)
        dy = hbody_slk / 2
        if drawbody and dy <= cdbody_slk / 2:
            dx = math.sqrt(cdbody_slk * cdbody_slk / 4 - dy * dy)
            if mount_below:
                addHDLineWithKeepout(kicad_modg, clbody_slk - dx, lbody_slk, ctbody_slk - dy, 'F.SilkS', lw_slk,
                                     keepouts)
                addVDLineWithKeepout(kicad_modg, lbody_slk, ctbody_slk - dy, ctbody_slk + dy, 'F.SilkS', lw_slk,
                                     keepouts)
                addHDLineWithKeepout(kicad_modg, clbody_slk - dx, lbody_slk, ctbody_slk + dy, 'F.SilkS', lw_slk,
                                     keepouts)
            addHLineWithKeepout(kicad_modg, clbody_slk - dx, lbody_slk, ctbody_slk - dy, layer + '.SilkS', lw_slk,
                                keepouts)
            addVLineWithKeepout(kicad_modg, lbody_slk, ctbody_slk - dy, ctbody_slk + dy, layer + '.SilkS', lw_slk,
                                keepouts)
            addHLineWithKeepout(kicad_modg, clbody_slk - dx, lbody_slk, ctbody_slk + dy, layer + '.SilkS', lw_slk,
                                keepouts)
            drawbody = False
    
    if drawbody:
        addRectWithKeepout(kicad_modg, lbody_slk, tbody_slk, wbody_slk, hbody_slk, layer + '.SilkS', lw_slk, keepouts,
                           0.001)
        if mount_below:
            addDRectWithKeepout(kicad_modg, lbody_slk, tbody_slk, wbody_slk, hbody_slk, 'F.SilkS', lw_slk, keepouts,
                                0.001)
    
    if dshaft > 0 and (not mount_below):
        addCircleWithKeepout(kicad_modg, clbody_fab, ctbody_fab, dshaft / 2, layer + '.SilkS', lw_slk, keepouts)
    
    # create courtyard
    kicad_mod.append(RectLine(start=[roundCrt(l_crt + offset[0]), roundCrt(t_crt + offset[1])],
                              end=[roundCrt(l_crt + w_crt + offset[0]), roundCrt(t_crt + h_crt + offset[1])],
                              layer='F.CrtYd', width=lw_crt))
    if mount_below:
        kicad_mod.append(RectLine(start=[roundCrt(l_crt + offset[0]), roundCrt(t_crt + offset[1])],
                                  end=[roundCrt(l_crt + w_crt + offset[0]), roundCrt(t_crt + h_crt + offset[1])],
                                  layer='B.CrtYd', width=lw_crt))
    
    # create pads
    pn = 1
    for p in padpos:
        if p[6] == Pad.TYPE_SMT:
            kicad_modg.append(Pad(number=p[0], type=p[6], shape=p[7], at=[p[1], p[2]], size=[p[4], p[5]], drill=p[3],
                                  layers=[layer + '.Cu', layer + '.Mask']))
        else:
            kicad_modg.append(Pad(number=p[0], type=p[6], shape=p[7], at=[p[1], p[2]], size=[p[4], p[5]], drill=p[3],
                                  layers=['*.Cu', '*.Mask']))
    
    # add model
    if (has3d != 0):
        kicad_modg.append(
            Model(filename=lib_name + ".3dshapes/" + footprint_name + ".wrl", at=x_3d, scale=s_3d, rotate=[0, 0, 0]))
    
    # print render tree
    # print(kicad_mod.getRenderTree())
    # print(kicad_mod.getCompleteRenderTree())
    
    # write file
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile(footprint_name + '.kicad_mod')


# create spindle trimmer potentiometer footprints
#                                                      <-----------rmx2------------->
#                  screwxoffset<>      <------------------rmx3---------------------->
#   screwyoffset ^              +---------------------------------------------------------------+         ^       ^
#                |     ^   +----|                                                               |         |       |
#                v  dsrew  +--  |                     O2O                                       | ^       |       pinyoffset
#                      v   +----|                                                               | rmy2    |       |
#                    wscrew<--->|     O3O                                           O1O         | v       hbody   v
#                               |                                                               |         |
#                               +---------------------------------------------------------------+         v
#                               <----------------------------wbody------------------------------>
#                               <------pinxoffset------------------------------------>
#
# style=screwtop/screwleft
def makeSpindleTrimmer(footprint_name, class_name, wbody, hbody,pinxoffset,pinyoffset,
                                rmx2,rmy2,rmx3,rmy3,
                                dscrew,ddrill=1,wscrew=0,screwxoffset=0,screwyoffset=0,
                                style = "screwleft", screwstyle="slit", SMD_pads=False,
                                SMD_padsize=[], R_POW=0, x_3d=[0, 0, 0],
                                s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialtags=[], add_description="",
                                classname="Potentiometer", lib_name="Potentiometers", name_additions=[], script3d="",
                                height3d=10):
    padx = 1.8 * ddrill
    pady = padx
    if SMD_pads and len(SMD_padsize) >= 2:
        padx = SMD_padsize[0]
        pady = SMD_padsize[1]
    
    txtoffset = txt_offset
    
    
    
    padpos = []
    padtype = Pad.TYPE_THT
    padstyle = Pad.SHAPE_CIRCLE
    if SMD_pads:
        padtype = Pad.TYPE_SMT
        padstyle = Pad.SHAPE_RECT
    padpos.append([1, pinxoffset, pinyoffset, ddrill, padx, pady, padtype, padstyle])
    if SMD_pads and len(SMD_padsize) >= 4:
        padpos.append([2, pinxoffset+rmx2, pinyoffset+rmy2, ddrill, SMD_padsize[2], SMD_padsize[3], padtype, padstyle])
    else:
        padpos.append([2, pinxoffset + rmx2, pinyoffset + rmy2, ddrill, padx, pady, padtype, padstyle])
    if SMD_pads and len(SMD_padsize) >= 6:
        padpos.append([3, pinxoffset + rmx3, pinyoffset + rmy3, ddrill, SMD_padsize[4], SMD_padsize[5], padtype, padstyle])
    else:
        padpos.append([3, pinxoffset+rmx3, pinyoffset+rmy3, ddrill, padx, pady, padtype, padstyle])
    offset = [-pinxoffset, -pinyoffset]
    if SMD_pads:
        offset = [-(pinxoffset+pinxoffset+rmx2+pinxoffset+rmx3)/3, -(pinyoffset+pinyoffset+rmy2+pinyoffset+rmy3)/3]
    
    lbody_fab = 0
    tbody_fab = 0
    wbody_fab = wbody
    hbody_fab = hbody

    lbody_slk = lbody_fab - slk_offset
    tbody_slk = tbody_fab - slk_offset
    wbody_slk = wbody_fab + 2 * slk_offset
    hbody_slk = hbody_fab + 2 * slk_offset

    if style=="screwleft":
        lscrew_fab=lbody_fab+screwxoffset-wscrew
        tscrew_fab = tbody_fab + screwyoffset-dscrew/2
        wscrew_fab = wscrew
        hscrew_fab = dscrew
        lscrew_slk=lscrew_fab-slk_offset
        tscrew_slk = tscrew_fab-slk_offset
        wscrew_slk = wscrew_fab
        hscrew_slk = hscrew_fab+slk_offset*2
    elif style=="screwtop":
        lscrew_fab=lbody_fab+screwxoffset
        tscrew_fab = tbody_fab + screwyoffset
        wscrew_fab = dscrew
        hscrew_fab = dscrew
        lscrew_slk = lscrew_fab
        tscrew_slk = tscrew_fab
        wscrew_slk = wscrew_fab + 2*slk_offset
        hscrew_slk = hscrew_fab + 2*slk_offset

    
    minx = miny = 1e99
    maxx = maxy = -1e99
    for p in padpos:
        maxx = max(maxx, p[1] + p[4] / 2)
        minx = min(minx, p[1] - p[4] / 2)
        maxy = max(maxy, p[2] + p[5] / 2)
        miny = min(miny, p[2] - p[5] / 2)
    
    minx = min(minx, lbody_fab)
    miny = min(miny, tbody_fab)
    maxx = max(maxx, lbody_fab + wbody_fab)
    maxy = max(maxy, tbody_fab + hbody_fab)
    if style == "screwleft":
        minx = min(minx, lscrew_fab)
        miny = min(miny, tscrew_fab)
        maxx = max(maxx, lscrew_fab + wscrew_fab)
        maxy = max(maxy, tscrew_fab + hscrew_fab)

    h_crt = (maxy - miny) + 2 * crt_offset
    w_crt = (maxx - minx) + 2 * crt_offset
    l_crt = minx - crt_offset
    t_crt = miny - crt_offset
    
    pow_rat = ""
    if R_POW > 0:
        pow_rat = "{0}W".format(R_POW)
        if (1 / R_POW == int(1 / R_POW)):
            pow_rat = pow_rat + " = 1/{0}W".format(int(1 / R_POW))
    
    tgs = specialtags
    if len(class_name) > 0:
        tgs.append(class_name)
    if len(pow_rat) > 0:
        tgs.append(pow_rat)
    
    description = "Spindle Trimmer Potentiometer"
    tags = "Spindle Trimmer Potentiometer "
    for t in tgs:
        if len(description) > 0: description = description + ", "
        description = description + t
        if len(tags) > 0: tags = tags + " "
        tags = tags + " " + t
    
    if len(add_description) > 0:
        if len(description) > 0: description = description + ", "
        description = description + add_description
    
    for n in name_additions:
        if len(n) > 0:
            footprint_name = footprint_name + "_" + n
    
    print(footprint_name)
    
    if script3d != "":
        with open(script3d, "a") as myfile:

            
            myfile.write("\n\n # {0}\n".format(footprint_name))
            myfile.write("import FreeCAD\n")
            myfile.write("import os\n")
            myfile.write("import os.path\n\n")
            myfile.write("App.ActiveDocument.clearAll()\n")
            line = 0
            line += 1; script3d_writevariable(myfile, line, 'lbody_fab', min(lbody_fab+wbody_fab,lbody_fab)+offset[0])
            line += 1; script3d_writevariable(myfile, line, 'tbody_fab', min(tbody_fab+hbody_fab,tbody_fab)+offset[1])
            line += 1; script3d_writevariable(myfile, line, 'wbody_fab', math.fabs(wbody_fab))
            line += 1; script3d_writevariable(myfile, line, 'hbody_fab', math.fabs(hbody_fab))
            line += 1; script3d_writevariable(myfile, line, 'lscrew_fab', min(lscrew_fab+wscrew_fab,lscrew_fab)+offset[0])
            line += 1; script3d_writevariable(myfile, line, 'tscrew_fab', min(tscrew_fab+hscrew_fab,tscrew_fab)+offset[1])
            line += 1; script3d_writevariable(myfile, line, 'wscrew_fab', math.fabs(wscrew_fab))
            line += 1; script3d_writevariable(myfile, line, 'hscrew_fab', math.fabs(hscrew_fab))
            line += 1; script3d_writevariable(myfile, line, 'dscrew', dscrew)
            line += 1; script3d_writevariable(myfile, line, 'wscrew', wscrew)
            line += 1; script3d_writevariable(myfile, line, 'rmxtwo', rmx2)
            line += 1; script3d_writevariable(myfile, line, 'rmytwo', rmy2)
            line += 1; script3d_writevariable(myfile, line, 'rmxthree', rmx3)
            line += 1; script3d_writevariable(myfile, line, 'rmythree', rmy3)
            for p in padpos:
                if p[0] == 1:
                    line += 1;
                    script3d_writevariable(myfile, line, 'padx', p[1])
                    line += 1;
                    script3d_writevariable(myfile, line, 'pady', p[2])
            line += 1; script3d_writevariable(myfile, line, 'd_wire', ddrill-0.3)
            line += 1; script3d_writevariable(myfile, line, 'height', height3d)
            line += 1; script3d_writevariable(myfile, line, 'offsetx', offset[0])
            line += 1; script3d_writevariable(myfile, line, 'offsety', offset[1])

            myfile.write("App.ActiveDocument.recompute()\n\n")
            myfile.write("doc = FreeCAD.activeDocument()\n")
            myfile.write("__objs__=[]\n")
            myfile.write("for obj in doc.Objects:	\n")
            myfile.write("    if obj.ViewObject.Visibility:\n")
            myfile.write("        __objs__.append(obj)\n")
            myfile.write("\nFreeCADGui.export(__objs__,os.path.split(doc.FileName)[0]+os.sep+\"{0}.wrl\")\n".format(
                footprint_name))
            myfile.write("doc.saveCopy(os.path.split(doc.FileName)[0]+os.sep+\"{0}.FCStd\")\n".format(footprint_name))
            myfile.write("print(\"created {0}\")\n".format(footprint_name))
    
    # init kicad footprint
    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription(description)
    kicad_mod.setTags(tags)
    if SMD_pads:
        kicad_mod.setAttribute('smd')
    
    kicad_modg = Translation(offset[0], offset[1])
    kicad_mod.append(kicad_modg)
    
    # set general values
    kicad_modg.append(Text(type='reference', text='REF**', at=[l_crt + w_crt / 2, t_crt - txtoffset], layer='F.SilkS'))
    kicad_modg.append(
        Text(type='value', text=footprint_name, at=[l_crt + w_crt / 2, t_crt + h_crt + txtoffset], layer='F.Fab'))
    
    # create FAB-layer
    layer = 'F'
    kicad_modg.append(RectLine(start=[lbody_fab, tbody_fab], end=[lbody_fab + wbody_fab, tbody_fab + hbody_fab], layer=layer + '.Fab', width=lw_fab))
    if style == "screwleft":
        kicad_modg.append(RectLine(start=[lscrew_fab, tscrew_fab], end=[lscrew_fab + wscrew_fab, tscrew_fab + hscrew_fab], layer=layer + '.Fab',width=lw_fab))
        kicad_modg.append(Line(start=[lscrew_fab, tscrew_fab+hscrew_fab/2], end=[lscrew_fab + wscrew_fab/2, tscrew_fab + hscrew_fab/2], layer=layer + '.Fab', width=lw_fab))
    elif style == "screwtop":
        if screwstyle=="slit":
            addSlitScrew(kicad_modg, lscrew_fab, tscrew_fab, wscrew_fab / 2, layer + '.Fab', lw_fab)
        else:
            addCrossScrew(kicad_modg, lscrew_fab, tscrew_fab, wscrew_fab / 2, layer + '.Fab', lw_fab)
        
    
    # build keepeout for SilkScreen
    keepouts = []
    for p in padpos:
        if p[7] == Pad.SHAPE_CIRCLE:
            keepouts = keepouts + addKeepoutRound(p[1], p[2], p[4] + 2 * lw_slk + 2 * slk_offset,
                                                  p[5] + 2 * lw_slk + 2 * slk_offset)
        else:
            keepouts = keepouts + addKeepoutRect(p[1], p[2], p[4] + 2 * lw_slk + 2 * slk_offset,
                                                 p[5] + 2 * lw_slk + 2 * slk_offset)
    # debug_draw_keepouts(kicad_modg,keepouts)
    
    # create SILKSCREEN-layer
    layer = 'F'
    addRectWithKeepout(kicad_modg, lbody_slk, tbody_slk, wbody_slk, hbody_slk, layer + '.SilkS', lw_slk, keepouts)
    if style == "screwleft":
        addRectWithKeepout(kicad_modg, lscrew_slk, tscrew_slk, wscrew_slk, hscrew_slk, layer + '.SilkS', lw_slk, keepouts)
        addHLineWithKeepout(kicad_modg, lscrew_slk, lscrew_slk+wscrew_slk/2, tscrew_slk+hscrew_slk/2, layer + '.SilkS', lw_slk, keepouts)
    elif style == "screwtop":
        if screwstyle == "slit":
            addSlitScrewWithKeepouts(kicad_modg, lscrew_slk, tscrew_slk, wscrew_slk / 2, layer + '.SilkS', lw_slk, keepouts)
        else:
            addCrossScrewWithKeepouts(kicad_modg, lscrew_slk, tscrew_slk, wscrew_slk / 2, layer + '.SilkS', lw_slk,
                                     keepouts)

    
    # create courtyard
    kicad_mod.append(RectLine(start=[roundCrt(l_crt + offset[0]), roundCrt(t_crt + offset[1])],
                              end=[roundCrt(l_crt + w_crt + offset[0]), roundCrt(t_crt + h_crt + offset[1])],
                              layer='F.CrtYd', width=lw_crt))
    
    # create pads
    pn = 1
    for p in padpos:
        if p[6] == Pad.TYPE_SMT:
            kicad_modg.append(Pad(number=p[0], type=p[6], shape=p[7], at=[p[1], p[2]], size=[p[4], p[5]], drill=p[3],
                                  layers=[layer + '.Cu', layer + '.Mask']))
        else:
            kicad_modg.append(Pad(number=p[0], type=p[6], shape=p[7], at=[p[1], p[2]], size=[p[4], p[5]], drill=p[3],
                                  layers=['*.Cu', '*.Mask']))
    
    # add model
    if (has3d != 0):
        kicad_modg.append(
            Model(filename=lib_name + ".3dshapes/" + footprint_name + ".wrl", at=x_3d, scale=s_3d, rotate=[0, 0, 0]))
    
    # print render tree
    # print(kicad_mod.getRenderTree())
    # print(kicad_mod.getCompleteRenderTree())
    
    # write file
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile(footprint_name + '.kicad_mod')

