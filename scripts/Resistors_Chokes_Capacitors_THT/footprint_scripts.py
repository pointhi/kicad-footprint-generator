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

def roundG(x, g):
    if (x>0):
        return math.ceil(x/g)*g
    else:
        return math.floor(x/g)*g


def roundCrt(x):
    return roundG(x, 0.05)


crt_offset = 0.25
slk_offset = 0.06
lw_fab = 0.1
lw_crt = 0.05
lw_slk = 0.12
txt_offset = 1


# simple axial round (type="cyl") / box (type="box") / bare metal wire (type="bridge") resistor, horizontally mounted
# optionally with additional shunt leads: hasShuntPins=True, shuntPinsRM=DISTANCE
def makeResistorAxialHorizontal(seriesname, rm, rmdisp, w, d, ddrill, R_POW, type="cyl", d2=0, hasShuntPins=False, shuntPinsRM=0, x_3d=[0,0,0], s_3d=[1/2.54,1/2.54,1/2.54], has3d=1, specialfpname="", specialtags=[], add_description="", classname="Resistor", lib_name="Resistors_ThroughHole", name_additions=[]):
    padx=2*ddrill
    pady=padx


    left=(rm-w)/2
    top=-d/2
    h_slk=d+2*slk_offset
    w_slk=w+2*slk_offset
    l_slk=left-slk_offset
    r_slk=l_slk+w_slk
    t_slk=-h_slk/2
    w_crt=rm+padx+2*crt_offset
    h_crt=max(h_slk, pady)+2*crt_offset
    l_crt=min(l_slk, -padx/2)-crt_offset
    t_crt=min(t_slk, -pady/2)-crt_offset


    snfp=""
    sn=""
    snt=""
    if len(seriesname)>0:
        snfp="_"+seriesname
        sn=", "+seriesname+" series"
        snt = " " + seriesname + " series"

    pow_rat = ""
    if R_POW > 0:
        pow_rat="{0}W".format(R_POW)
        if (1/R_POW==int(1/R_POW)):
            pow_rat=pow_rat+" = 1/{0}W".format(int(1/R_POW))

    fnpins="_P{0:0.2f}mm".format(rmdisp)
    if hasShuntPins:
        fnpins = "_PS{0:0.2f}mm_P{1:0.2f}mm".format(shuntPinsRM,rmdisp)
    dimdesc="length*diameter={0}*{1}mm^2".format(w, d)
    dimdesct = "length {0}mm diameter {1}mm".format(w, d)
    footprint_name=classname+"{3}_Horizontal_L{1:0.1f}mm_D{2:0.1f}mm{0}".format(fnpins,w,d,snfp)
    description=classname+"{3}, Axial, Horizontal, pin distance={0}mm, {1}, {2}".format(rm, pow_rat, dimdesc,sn)
    tags=classname+"{3} Axial Horizontal pin distance {0}mm {1} {2}".format(rm, pow_rat, dimdesct, snt)
    if type=="box":
        footprint_name = classname+"{4}_Horizontal_W{1:0.1f}mm_L{3:0.1f}mm{0}".format(fnpins, d,d2,w, snfp)
        dimdesc = "length*width*height={0}*{1}*{1}mm^3".format(w,d, d2)
        dimdesct = "length {0}mm width {1}mm height {1}mm".format(w, d, d2)
    elif type=="bridge":
        footprint_name = classname+"{3}_L{2:0.1f}mm_W{1:0.1f}mm{0}".format(fnpins, d,w, snfp)
        dimdesc = "length*width={0}*{1}mm^2".format(w,d)
        dimdesct = "length {0}mm width {1}mm ".format(w, d)
        description=classname+"{3}, Bare Metal Strip/Wire, Horizontal, pin distance={0}mm, {1}, {2}".format(rm, pow_rat, dimdesc,sn)
        tags=classname+"{3} Bare Metal Strip Wire Horizontal pin distance {0}mm {1} {2}".format(rm, pow_rat, dimdesct, snt)

    if hasShuntPins:
        description = description + ", shunt pin distance = {0:0.2f}mm".format(shuntPinsRM)
        tags = tags + ", shunt pin distance {0:0.2f}mm".format(shuntPinsRM)

    for t in specialtags:
        description=description+", "+t
        tags = tags + " " + t
    if (specialfpname!=""):
        footprint_name=specialfpname;

    if len(add_description) > 0:
        description = description + ", " + add_description

    for n in name_additions:
        if len(n)>0:
            footprint_name=footprint_name+"_"+n

    print(footprint_name)

    # init kicad footprint
    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription(description)
    kicad_mod.setTags(tags)

    # set general values
    kicad_mod.append(Text(type='reference', text='REF**', at=[rm/2, t_slk-txt_offset], layer='F.SilkS'))
    kicad_mod.append(Text(type='value', text=footprint_name, at=[rm/2, h_slk/2+txt_offset], layer='F.Fab'))

    # create FAB-layer
    kicad_mod.append(RectLine(start=[left, top], end=[left+w, top+d], layer='F.Fab', width=lw_fab))
    if type != "bridge":
        kicad_mod.append(Line(start=[0, 0], end=[left, 0], layer='F.Fab', width=lw_fab))
        kicad_mod.append(Line(start=[rm, 0], end=[left+w, 0], layer='F.Fab', width=lw_fab))

    # create SILKSCREEN-layer

    if l_slk<padx/2+lw_slk+slk_offset:
        if t_slk<-(pady/2+lw_slk+slk_offset):
            kicad_mod.append(PolygoneLine(polygone=[[l_slk, -pady/2-lw_slk-slk_offset], [l_slk, t_slk], [l_slk + w_slk, t_slk], [l_slk + w_slk, -pady/2-lw_slk-slk_offset]], layer='F.SilkS'))
            kicad_mod.append(PolygoneLine(polygone=[[l_slk, pady/2+lw_slk+slk_offset], [l_slk, t_slk + h_slk], [l_slk + w_slk, t_slk + h_slk], [l_slk + w_slk, pady/2+lw_slk+slk_offset]], layer='F.SilkS'))
        else:
            kicad_mod.append(Line(start=[l_slk, t_slk], end=[l_slk + w_slk, t_slk], layer='F.SilkS'))
            kicad_mod.append(Line(start=[l_slk, t_slk + h_slk], end=[l_slk + w_slk, t_slk + h_slk], layer='F.SilkS'))
    else:
        kicad_mod.append(RectLine(start=[l_slk, t_slk], end=[l_slk + w_slk, t_slk + h_slk], layer='F.SilkS'))
    if padx/2+lw_slk+slk_offset<l_slk:
        kicad_mod.append(Line(start=[padx/2+lw_slk+slk_offset, 0], end=[l_slk, 0], layer='F.SilkS'))
        kicad_mod.append(Line(start=[rm-padx/2-lw_slk-slk_offset, 0], end=[l_slk+w_slk, 0], layer='F.SilkS'))
    if type == "bridge":
        y=-d2/2; y0=y; y1=y
        while y<d2/2:
            y1=y
            kicad_mod.append(Line(start=[padx/2+2*lw_slk+slk_offset, y], end=[rm-2*lw_slk-padx/2-slk_offset,y], layer='F.SilkS'))
            y=y+lw_slk
        kicad_mod.append(Line(start=[padx / 2 + 2 * lw_slk + slk_offset, y0], end=[padx / 2 + 2 * lw_slk + slk_offset, y1], layer='F.SilkS'))
        kicad_mod.append(Line(start=[rm - 2 * lw_slk - padx / 2 - slk_offset, y0], end=[rm - 2 * lw_slk - padx / 2 - slk_offset, y1],layer='F.SilkS'))

    # create courtyard
    kicad_mod.append(RectLine(start=[roundCrt(l_crt), roundCrt(t_crt)], end=[roundCrt(l_crt+w_crt), roundCrt(t_crt+h_crt)], layer='F.CrtYd', width=lw_crt))

    # create pads
    if hasShuntPins:
        kicad_mod.append(Pad(number=1, type=Pad.TYPE_THT, shape=Pad.SHAPE_OVAL, at=[0, 0], size=[padx, pady], drill=ddrill,layers=['*.Cu', '*.Mask']))
        kicad_mod.append(Pad(number=2, type=Pad.TYPE_THT, shape=Pad.SHAPE_OVAL, at=[(rm-shuntPinsRM)/2, 0], size=[padx, pady], drill=ddrill,layers=['*.Cu', '*.Mask']))
        kicad_mod.append(Pad(number=3, type=Pad.TYPE_THT, shape=Pad.SHAPE_OVAL, at=[(rm-shuntPinsRM)/2+shuntPinsRM, 0], size=[padx, pady], drill=ddrill,layers=['*.Cu', '*.Mask']))
        kicad_mod.append(Pad(number=4, type=Pad.TYPE_THT, shape=Pad.SHAPE_OVAL, at=[rm, 0], size=[padx, pady], drill=ddrill,layers=['*.Cu', '*.Mask']))
    else:
        kicad_mod.append(Pad(number=1, type=Pad.TYPE_THT, shape=Pad.SHAPE_OVAL, at=[0, 0], size=[padx, pady], drill=ddrill, layers=['*.Cu', '*.Mask']))
        kicad_mod.append(Pad(number=2, type=Pad.TYPE_THT, shape=Pad.SHAPE_OVAL, at=[rm, 0], size=[padx, pady], drill=ddrill, layers=['*.Cu', '*.Mask']))

    # add model
    if (has3d!=0):
        kicad_mod.append(Model(filename=lib_name + ".3dshapes/"+footprint_name+".wrl", at=x_3d, scale=s_3d, rotate=[0, 0, 0]))

    # print render tree
    # print(kicad_mod.getRenderTree())
    # print(kicad_mod.getCompleteRenderTree())

    # write file
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile(footprint_name+'.kicad_mod')


# simple axial round (type="cyl")/ box (type="box") resistor, vertically mounted
def makeResistorAxialVertical(seriesname,rm, rmdisp, l, d, ddrill, R_POW, type="cyl", d2=0, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", largepadsx=0, largepadsy=0, specialtags=[], add_description="", classname="Resistor", lib_name="Resistors_ThroughHole", name_additions=[]):
    padx = 2 * ddrill
    pady = padx
    if (largepadsx):
        padx = max(padx, largepadsx)
    if (largepadsy):
        pady = max(pady, largepadsy)


    left = -d / 2
    top = -d / 2
    d_slk = max(max(padx, pady) + 0.15, d + 2 * slk_offset)
    d2_slk = max(max(padx, pady) + 0.15, d2 + 2 * slk_offset)
    w_slk = rm + d / 2 + padx / 2 + 2 * slk_offset
    l_slk = left - slk_offset
    r_slk = l_slk + w_slk
    t_slk = -d_slk / 2

    w_crt = w_slk + 2 * crt_offset
    h_crt = d_slk + 2 * crt_offset
    l_crt = l_slk - crt_offset
    t_crt = t_slk - crt_offset

    snfp = ""
    sn = ""
    snt = ""
    if len(seriesname) > 0:
        snfp = "_" + seriesname
        sn = ", " + seriesname + " series"
        snt = " " + seriesname + " series"

    pow_rat =""
    if R_POW > 0:
        pow_rat = "{0}W".format(R_POW)
        if (1 / R_POW == int(1 / R_POW)):
            pow_rat = pow_rat + " = 1/{0}W".format(int(1 / R_POW))
    dimdesc = "length*diameter={0}*{1}mm^2".format(w, d)
    dimdesct = "length {0}mm diameter {1}mm".format(w, d)
    footprint_name = classname+"{3}_Vertical_L{1:0.1f}mm_D{2:0.1f}mm_P{0:0.2f}mm".format(rmdisp, w, d, snfp)
    if type == "box":
        footprint_name = classname+"{4}_Vertical_L{3:0.1f}mm_W{1:0.1f}mm_P{0:0.2f}mm".format(rmdisp, d, d2,
                                                                                                         w, snfp)
        dimdesc = "length*width*height={0}*{1}*{1}mm^3".format(w, d, d2)
        dimdesct = "length {0}mm width {1}mm height {1}mm".format(w, d, d2)
    description = classname+"{3}, Axial, Vertical, pin distance={0}mm, {1}, {2}".format(rm, pow_rat, dimdesc, sn)
    tags = classname+"{3} Axial Vertical pin distance {0}mm {1} {2}".format(rm, pow_rat, dimdesct, snt)

    for t in specialtags:
        description = description + ", " + t
        tags = tags + " " + t
    if (specialfpname != ""):
        footprint_name = specialfpname;

    if len(add_description) > 0:
        description = description + ", " + add_description

    for n in name_additions:
        if len(n)>0:
            footprint_name=footprint_name+"_"+n

    print(footprint_name)

    # init kicad footprint
    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription(description)
    kicad_mod.setTags(tags)

    # set general values
    kicad_mod.append(Text(type='reference', text='REF**', at=[rm / 2, t_slk - txt_offset], layer='F.SilkS'))
    kicad_mod.append(Text(type='value', text=footprint_name, at=[rm / 2, d_slk / 2 + txt_offset], layer='F.Fab'))

    # create FAB-layer
    if type=="cyl":
        kicad_mod.append(Circle(center=[0, 0], radius=d / 2, layer='F.Fab', width=lw_fab))
    else:
        kicad_mod.append(RectLine(start=[-d/2, -d2/2], end=[d/2,d2/2], layer='F.Fab', width=lw_fab))
    kicad_mod.append(Line(start=[0, 0], end=[rm,0], layer='F.Fab', width=lw_fab))

    # create SILKSCREEN-layer
    xs1 = d_slk / 2
    xs2 = rm - padx / 2 - 0.3

    if (xs1 < xs2):
        if type == "cyl":
            kicad_mod.append(Circle(center=[0, 0], radius=d_slk / 2, layer='F.SilkS', width=lw_slk))
        else:
            kicad_mod.append(RectLine(start=[-d_slk/2, -d2_slk/2], end=[d_slk/2,d2_slk/2], layer='F.SilkS', width=lw_slk))
        kicad_mod.append(Line(start=[xs1, 0], end=[xs2, 0], layer='F.SilkS', width=lw_slk))
    else:
        xx=math.sqrt(d_slk*d_slk/4-pady*pady/4)
        alpha=360-2*math.acos(xx/(d_slk/2))/3.1415*180
        if type == "cyl":
            kicad_mod.append(Arc(center=[0, 0], start=[xx, -pady/2], angle=-alpha, layer='F.SilkS', width=lw_slk))
        else:
            kicad_mod.append(PolygoneLine(polygone=[[d_slk/2, -pady/2-slk_offset],
                                                    [d_slk / 2, -d2_slk / 2],
                                                    [-d_slk / 2, -d2_slk / 2],
                                                    [d_slk / 2, -d2_slk / 2],
                                                    [d_slk / 2, +pady / 2 + slk_offset]], layer='F.SilkS', width=lw_slk))

    # create courtyard
    kicad_mod.append(
        RectLine(start=[roundCrt(l_crt), roundCrt(t_crt)], end=[roundCrt(l_crt + w_crt), roundCrt(t_crt + h_crt)],
                 layer='F.CrtYd', width=lw_crt))

    # create pads
    kicad_mod.append(Pad(number=1, type=Pad.TYPE_THT, shape=Pad.SHAPE_OVAL, at=[0, 0], size=[padx, pady], drill=ddrill,
                         layers=['*.Cu', '*.Mask']))
    kicad_mod.append(Pad(number=2, type=Pad.TYPE_THT, shape=Pad.SHAPE_OVAL, at=[rm, 0], size=[padx, pady], drill=ddrill,
                         layers=['*.Cu', '*.Mask']))

    # add model
    if (has3d != 0):
        kicad_mod.append(
            Model(filename=lib_name + ".3dshapes/" + footprint_name + ".wrl", at=x_3d, scale=s_3d, rotate=[0, 0, 0]))

    # print render tree
    # print(kicad_mod.getRenderTree())
    # print(kicad_mod.getCompleteRenderTree())

    # write file
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile(footprint_name + '.kicad_mod')


# simple radial rectangular resistor, vertically mounted
#   style options:
#     1. type="simple"
#           +----------------+ ^
#           |                | |
#           |  OO        OO  | h
#           |                | |
#           +----------------+ v
#               <---rm--->
#           <-------w-------->
#     2. type="simple", vlines=True
#           +-+------------+-+ ^
#           | |            | | |
#           | | OO     OO  | | h
#           | |            | | |
#           +-+------------+-+ v
#               <--rm-->
#           <-------w-------->
#             <----w2------>
#     3. type="simple45"
#           +----------------+ ^
#           |            OO  | |  ^rm2
#           |       OO       | h  v
#           |                | |
#           +----------------+ v
#                   <-rm->
#           <-------w-------->
#     4. type="simple45", vlines=True
#           +-+------------+-+ ^
#           | |         OO | | |  ^rm2
#           | |     OO     | | h  v
#           | |            | | |
#           +-+------------+-+ v
#                   <-rm->
#           <-------w-------->
#             <----w2------>
#     5. type="round": ellipse, diameter w/h
def makeResistorRadial(seriesname, rm, w, h, ddrill, R_POW, rm2=0, vlines=False,w2=0, type="simple", x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", specialtags=[], add_description="", classname="Resistor", lib_name="Resistors_ThroughHole", name_additions=[]):
    padx = 2 * ddrill
    pady = padx

    padpos=[]
    offset=[0,0]
    if type=="simple" or type=="round":
        padpos.append([1,- rm / 2, 0, ddrill,padx,pady])
        padpos.append([2,rm / 2, 0, ddrill,padx,pady])
        offset=[rm/2,0]
    elif type == "simple45":
        padpos.append([1,0, 0, ddrill,padx,pady])
        padpos.append([2,rm,-rm2, ddrill,padx,pady])
        offset = [0, 0]

    l_fab = -w / 2
    t_fab = -h / 2
    lvl1_fab = -w2 / 2
    lvl2_fab = w2 / 2
    w_fab = w
    h_fab = h
    d_fab = max(w, h)
    h_slk = h_fab + 2 * slk_offset
    w_slk = w_fab + 2 * slk_offset
    l_slk = l_fab - slk_offset
    t_slk = t_fab - slk_offset
    lvl1_slk=lvl1_fab
    lvl2_slk = lvl2_fab
    d_slk=d_fab+lw_slk+slk_offset
    w_crt = max(w_slk, rm+padx) + 2 * crt_offset
    h_crt = max(h_slk, rm2+pady) + 2 * crt_offset
    l_crt = -w_crt/2
    t_crt = -h_crt/2

    snfp = ""
    sn = ""
    snt = ""
    if len(seriesname) > 0:
        snfp = "_" + seriesname
        sn = ", " + seriesname + " series"
        snt = " " + seriesname + " series"

    pow_rat = ""
    if R_POW > 0:
        pow_rat = "{0}W".format(R_POW)
        if (1 / R_POW == int(1 / R_POW)):
            pow_rat = pow_rat + " = 1/{0}W".format(int(1 / R_POW))

    fnpins = "_P{0:0.2f}mm".format(rm)
    pind="{0:0.2f}mm".format(rm)
    if type == "simple45":
        fnpins = "_Px{0:0.2f}mm_Py{1:0.2f}mm".format(rm,rm2)
        pind = "{0:0.2f}*{1:0.2f}mm^2".format(rm,rm2)

    dimdesc = "length*width={0}*{1}mm^2".format(w, h)
    dimdesct = "length {0}mm width {1}mm".format(w, h)
    if type=="round":
        if w==h:
            dimdesc = "diameter={0}mm^2".format(w)
            dimdesct = "diameter {0}mm".format(w)
        else:
            dimdesc = "diameterX*diameterY={0}*{1}mm^2".format(w, h)
            dimdesct = "diameterX {0}mm diameterY {1}mm".format(w, h)
        footprint_name = classname + "{2}_D{1:0.1f}mm{0}".format(fnpins, w, snfp)
    else:
        footprint_name = classname+"{3}_L{1:0.1f}mm_W{2:0.1f}mm{0}".format(fnpins, w, h, snfp)
    description = classname+"{3}, Radial, pin distance={0}, {1}, {2}".format(pind, pow_rat, dimdesc, sn)
    tags = classname+"{3} Radial pin distance {0} {1} {2}".format(pind, pow_rat, dimdesct, snt)


    for t in specialtags:
        description = description + ", " + t
        tags = tags + " " + t
    if (specialfpname != ""):
        footprint_name = specialfpname;

    if len(add_description) > 0:
        description = description + ", " + add_description

    for n in name_additions:
        if len(n)>0:
            footprint_name=footprint_name+"_"+n

    print(footprint_name)

    # init kicad footprint
    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription(description)
    kicad_mod.setTags(tags)

    kicad_modg = Translation(offset[0], offset[1])
    kicad_mod.append(kicad_modg)


    # set general values
    kicad_modg.append(Text(type='reference', text='REF**', at=[0, t_slk - txt_offset], layer='F.SilkS'))
    kicad_modg.append(Text(type='value', text=footprint_name, at=[0, t_slk+h_slk + txt_offset], layer='F.Fab'))

    # create FAB-layer
    if type=="round":
        kicad_modg.append(Circle(center=[l_fab+w_fab/2, t_fab+h_fab/2], radius=d_fab/2, layer='F.Fab', width=lw_fab))
    else:
        kicad_modg.append(RectLine(start=[l_fab, t_fab], end=[l_fab + w_fab, t_fab + h_fab], layer='F.Fab', width=lw_fab))
        if vlines:
            kicad_modg.append(Line(start=[lvl1_fab, t_fab], end=[lvl1_fab,t_fab+h_fab], layer='F.Fab', width=lw_fab))
            kicad_modg.append(Line(start=[lvl2_fab, t_fab], end=[lvl2_fab, t_fab + h_fab], layer='F.Fab', width=lw_fab))


    # build keepeout for SilkScreen
    keepouts=[]
    for p in padpos:
        keepouts=keepouts+addKeepoutRound(p[1],p[2],p[4]+2*lw_slk+2*slk_offset,p[5]+2*lw_slk+2*slk_offset)


    # create SILKSCREEN-layer
    if type=="round":
        if d_slk<rm+padx+2*(lw_slk+slk_offset):
            dxs=d_slk/2
            dys=pady/2+lw_slk+slk_offset
            alpha = 2 * (90 - math.fabs(180 / 3.1415 * math.atan(math.fabs(dys) / math.fabs(dxs))))
            kicad_modg.append(Arc(center=[0,0], start=[-dxs,-dys], angle=alpha, layer='F.SilkS', width=lw_slk))
            kicad_modg.append(Arc(center=[0, 0], start=[-dxs, dys], angle=-alpha, layer='F.SilkS', width=lw_slk))
        else:
            kicad_modg.append(Circle(center=[l_slk + w_slk / 2, t_slk + h_slk / 2], radius=d_slk/2, layer='F.SilkS', width=lw_slk))
    else:
        addRectWithKeepout(kicad_modg, l_slk, t_slk, w_slk, h_slk, 'F.SilkS', lw_slk, keepouts, 0.001)
        if vlines:
            addVLineWithKeepout(kicad_modg, lvl1_slk, t_slk, t_slk+h_slk, 'F.SilkS', lw_slk, keepouts, 0.001)
            addVLineWithKeepout(kicad_modg, lvl2_slk, t_slk, t_slk + h_slk, 'F.SilkS', lw_slk, keepouts, 0.001)


    # create courtyard
    kicad_mod.append(RectLine(start=[roundCrt(l_crt+offset[0]), roundCrt(t_crt+offset[1])], end=[roundCrt(l_crt + w_crt+offset[0]), roundCrt(t_crt + h_crt+offset[1])],layer='F.CrtYd', width=lw_crt))

    # create pads
    pn=1
    for p in padpos:
        kicad_modg.append(Pad(number=p[0], type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE, at=[p[1], p[2]], size=[p[4],p[5]], drill=p[3], layers=['*.Cu', '*.Mask']))


    # add model
    if (has3d != 0):
        kicad_modg.append(Model(filename=lib_name + ".3dshapes/" + footprint_name + ".wrl", at=x_3d, scale=s_3d, rotate=[0, 0, 0]))

    # print render tree
    # print(kicad_mod.getRenderTree())
    # print(kicad_mod.getCompleteRenderTree())

    # write file
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile(footprint_name + '.kicad_mod')

