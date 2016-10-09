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

def roundG(x, g):
    if (x>0):
        return math.ceil(x/g)*g
    else:
        return math.floor(x/g)*g


def roundCrt(x):
    return roundG(x, 0.05)


# simple round horizontal standard resistor
def makeRES_SIMPLERECT_HOR(rm, rmdisp, w, d, ddrill, R_POW, x_3d=[0,0,0], s_3d=[1/2.54,1/2.54,1/2.54], has3d=1, specialfpname="", specialtags=[]):
    padx=2*ddrill
    pady=padx
    crt_offset=0.25
    slk_offset=0.15
    lw_fab=0.1
    lw_crt=0.05
    lw_slk=0.15
    txt_offset=1


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


    lib_name = "Resistors_ThroughHole"
    description="Resistor, Axial, Horizontal, RM {0}mm, {1}W, L*D {2}*{3}mm²".format(rm, R_POW, w, d)
    tags="Resistor Axial Horizontal RM {0}mm {1}W L*D {2}*{3}mm²".format(rm, R_POW, w, d)
    for t in specialtags:
        description=description+", "+t
        tags = tags + " " + t
    footprint_name="Resistor_Horizontal_RM{0}mm".format(rmdisp)
    if (specialfpname!=""):
        footprint_name=specialfpname;
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
    kicad_mod.append(Line(start=[0, 0], end=[left, 0], layer='F.Fab', width=lw_fab))
    kicad_mod.append(Line(start=[rm, 0], end=[left+w, 0], layer='F.Fab', width=lw_fab))

    # create SILKSCREEN-layer
    kicad_mod.append(RectLine(start=[l_slk, t_slk], end=[l_slk+w_slk, t_slk+h_slk], layer='F.SilkS'))
    kicad_mod.append(Line(start=[padx/2+0.3, 0], end=[l_slk, 0], layer='F.SilkS'))
    kicad_mod.append(Line(start=[rm-padx/2-0.3, 0], end=[l_slk+w_slk, 0], layer='F.SilkS'))

    # create courtyard
    kicad_mod.append(RectLine(start=[roundCrt(l_crt), roundCrt(t_crt)], end=[roundCrt(l_crt+w_crt), roundCrt(t_crt+h_crt)], layer='F.CrtYd', width=lw_crt))

    # create pads
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


# simple round vertically mounted standard resistor
def makeRES_SIMPLECIRC_VER(rm, rmdisp, l, d, ddrill, R_POW, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", largepadsx=0, largepadsy=0, specialtags=[]):
    padx = 2 * ddrill
    pady = padx
    if (largepadsx):
        padx = max(padx, largepadsx)
    if (largepadsy):
        pady = max(pady, largepadsy)
    crt_offset = 0.25
    slk_offset = 0.15
    lw_fab = 0.1
    lw_crt = 0.05
    lw_slk = 0.15
    txt_offset = 1

    left = -d / 2
    top = -d / 2
    d_slk = max(max(padx, pady) + 0.15, d + 2 * slk_offset)
    w_slk = rm + d / 2 + padx / 2 + 2 * slk_offset
    l_slk = left - slk_offset
    r_slk = l_slk + w_slk
    t_slk = -d_slk / 2

    w_crt = w_slk + 2 * crt_offset
    h_crt = d_slk + 2 * crt_offset
    l_crt = l_slk - crt_offset
    t_crt = t_slk - crt_offset

    lib_name = "Resistors_ThroughHole"
    description = "Resistor, Axial, Vertical, RM {0}mm, {1}W, L*D {2}*{3}mm²".format(rm, R_POW, l, d)
    tags = "Resistor Axial Vertical RM {0}mm {1}W L*D {2}*{3}mm²".format(rm, R_POW, l, d)
    for t in specialtags:
        description = description + ", " + t
        tags = tags + " " + t
    footprint_name = "Resistor_Vertical_RM{0}mm".format(rmdisp)
    if (specialfpname != ""):
        footprint_name = specialfpname;
    print(footprint_name)

    # init kicad footprint
    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription(description)
    kicad_mod.setTags(tags)

    # set general values
    kicad_mod.append(Text(type='reference', text='REF**', at=[rm / 2, t_slk - txt_offset], layer='F.SilkS'))
    kicad_mod.append(Text(type='value', text=footprint_name, at=[rm / 2, d_slk / 2 + txt_offset], layer='F.Fab'))

    # create FAB-layer
    kicad_mod.append(Circle(center=[0, 0], radius=d / 2, layer='F.Fab', width=lw_fab))

    # create SILKSCREEN-layer
    kicad_mod.append(Circle(center=[0, 0], radius=d_slk / 2, layer='F.SilkS'))
    xs1 = d_slk / 2
    xs2 = rm - padx / 2 - 0.3
    if (xs1 < xs2):
        kicad_mod.append(Line(start=[xs1, 0], end=[xs2, 0], layer='F.SilkS'))

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


# power resistor, axial wires, mounted horizontally
def makeRES_RECT_HOR(rm, rmdisp, rl, rw, rh, ddrill, material, R_POW, x_3d=[0,0,0], s_3d=[1/2.54,1/2.54,1/2.54], has3d=1, specialfpname="", specialtags=[]):
    padx=2*ddrill
    pady=padx
    crt_offset=0.25
    slk_offset=0.15
    lw_fab=0.1
    lw_crt=0.05
    lw_slk=0.15
    txt_offset=1

    w=rl
    h=max(rw,rh)
    left=(rm-rl)/2
    top=-h/2
    h_slk=h+2*slk_offset
    w_slk=rl+2*slk_offset
    l_slk=left-slk_offset
    r_slk=l_slk+w_slk
    t_slk=-h_slk/2
    w_crt=rm+padx+2*crt_offset
    h_crt=max(h_slk, pady)+2*crt_offset
    l_crt=min(l_slk, -padx/2)-crt_offset
    t_crt=min(t_slk, -pady/2)-crt_offset

    description = "Axial, Horizontal, RM {0}mm, {2}W, L {3}mm, W{4}mm, H{5}mm".format(rm, material, R_POW, rl, rw, rh)
    tags = "Axial Horizontal RM {0}mm {2}W L {3}mm W{4}mm H{5}mm".format(rm, material, R_POW, rl, rw, rh)
    for t in specialtags:
        description=description+", "+t
        tags = tags + " " + t


    mat_fn = ""
    if (material!=""):
        description=material+", "+description
        tags=material+" "+tags
        mat_fn = "_" + material
    description = "Resistor, " + description
    tags = "Resistor R " + tags

    lib_name = "Resistors_ThroughHole"
    if (specialfpname!=""):
        footprint_name=specialfpname;
    else:
        footprint_name="Resistor{4}_Horizontal_L{1}mm-W{2}mm-H{3}mm-p{0}mm".format(rmdisp,rl,rw,rh,mat_fn)
    print(footprint_name)

    # init kicad footprint
    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription(description)
    kicad_mod.setTags(tags)

    # set general values
    kicad_mod.append(Text(type='reference', text='REF**', at=[rm/2, t_slk-txt_offset], layer='F.SilkS'))
    kicad_mod.append(Text(type='value', text=footprint_name, at=[rm/2, h_slk/2+txt_offset], layer='F.Fab'))

    # create FAB-layer
    kicad_mod.append(RectLine(start=[left, top], end=[left+w, top+h], layer='F.Fab', width=lw_fab))
    kicad_mod.append(Line(start=[0, 0], end=[left, 0], layer='F.Fab', width=lw_fab))
    kicad_mod.append(Line(start=[rm, 0], end=[left+w, 0], layer='F.Fab', width=lw_fab))

    # create SILKSCREEN-layer
    kicad_mod.append(RectLine(start=[l_slk, t_slk], end=[l_slk+w_slk, t_slk+h_slk], layer='F.SilkS'))
    kicad_mod.append(Line(start=[padx, 0], end=[l_slk, 0], layer='F.SilkS'))
    kicad_mod.append(Line(start=[rm-padx, 0], end=[l_slk+w_slk, 0], layer='F.SilkS'))

    # create courtyard
    kicad_mod.append(RectLine(start=[roundCrt(l_crt), roundCrt(t_crt)], end=[roundCrt(l_crt+w_crt), roundCrt(t_crt+h_crt)], layer='F.CrtYd', width=lw_crt))

    # create pads
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


# power resisitor, axial wires, mounted vertically
#  ______
# |     |
# |  *--|--*
# |_____|
def makeRES_SIMPLERECT_VER(rm, rmdisp, l, w, h, ddrill, material, R_POW, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54],  has3d=1, specialfpname="", largepadsx=0, largepadsy=0, specialtags=[]):
    padx = 2 * ddrill
    pady = padx
    if (largepadsx):
        padx = max(padx, largepadsx)
    if (largepadsy):
        pady = max(pady, largepadsy)
    crt_offset = 0.25
    slk_offset = 0.15
    lw_fab = 0.1
    lw_crt = 0.05
    lw_slk = 0.15
    txt_offset = 1

    left = -w / 2
    top = -h / 2
    rw_slk = max(padx + 0.15, w + 2 * slk_offset)
    rh_slk = max(pady + 0.15, h + 2 * slk_offset)
    w_slk = rm + w / 2 + padx / 2 + 2 * slk_offset
    l_slk = -rw_slk/2
    t_slk = -rh_slk / 2

    w_crt = rw_slk/2+padx/2+rm + 2 * crt_offset
    h_crt = rh_slk + 2 * crt_offset
    l_crt = l_slk - crt_offset
    t_crt = t_slk - crt_offset

    lib_name = "Resistors_ThroughHole"
    description = "Axial, Vertical, RM {0}mm, {1}W, L{2}, W{3}mm, H{4}mm".format(rm, R_POW, l, w, h)
    tags = "Axial Vertical RM {0}mm {1}W L{2} W{3}mm H{4}mm".format(rm, R_POW, l, w, h)
    for t in specialtags:
        description=description+", "+t
        tags = tags + " " + t
    mat_fn=""
    if (material!=""):
        description=material+", "+description
        tags=material+" "+tags
        mat_fn="_"+material
    description = "Resistor, " + description
    tags = "Resistor R " + tags
    footprint_name="Resistor{4}_Axial_Vertical_L{1}mm-W{2}mm-H{3}mm-p{0}mm".format(rmdisp,l,w,h,mat_fn)
    if (specialfpname != ""):
        footprint_name = specialfpname;
    print(footprint_name)

    # init kicad footprint
    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription(description)
    kicad_mod.setTags(tags)

    # set general values
    kicad_mod.append(Text(type='reference', text='REF**', at=[rm / 2, t_slk - txt_offset], layer='F.SilkS'))
    kicad_mod.append(Text(type='value', text=footprint_name, at=[rm / 2, rh_slk / 2 + txt_offset], layer='F.Fab'))

    # create FAB-layer
    kicad_mod.append(RectLine(start=[-w/2, -h/2], end=[w/2, h/2], layer='F.Fab', width=lw_fab))
    kicad_mod.append(Line(start=[0,0], end=[rm,0], layer='F.Fab', width=lw_fab))

    # create SILKSCREEN-layer
    kicad_mod.append(RectLine(start=[l_slk,t_slk], end=[l_slk+rw_slk,t_slk+rh_slk], layer='F.SilkS'))
    xs1 = rw_slk / 2
    xs2 = rm - padx / 2 - 0.3
    if (xs1 < xs2):
        kicad_mod.append(Line(start=[xs1, 0], end=[xs2, 0], layer='F.SilkS'))

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




#                               _____________
#                               | |       | |
# power resistor, radial wires, | | *   * | |
#                               |_|_______|_|
def makeRES_VERT(rm, rmdisp, rl, rw, rh, ddrill, material, R_POW, x_3d=[0,0,0], s_3d=[1/2.54,1/2.54,1/2.54], has3d=1, specialfpname="", specialtags=[], largepadsx=0, largepadsy=0):
    padx=2*ddrill
    pady=padx
    if (largepadsx>0):
        padx=max(padx, largepadsx)
    if (largepadsy>0):
        pady=max(pady, largepadsy)
    crt_offset=0.25
    slk_offset=0.15
    lw_fab=0.1
    lw_crt=0.05
    lw_slk=0.15
    txt_offset=1

    w=rw
    h=rh
    left=-(rw-rm)/2
    top=-h/2
    h_slk=h+2*slk_offset
    w_slk=w+2*slk_offset
    l_slk=left-slk_offset
    r_slk=l_slk+w_slk
    t_slk=-h_slk/2
    xl1_slk=left+(rw-rh)/2
    xl2_slk=xl1_slk+rh
    w_crt=w_slk+2*crt_offset
    h_crt=h_slk+2*crt_offset
    l_crt=l_slk-crt_offset
    t_crt=t_slk-crt_offset


    lib_name = "Resistors_ThroughHole"
    description = "Radial, Vertical, symmetric pins, RM {0}mm, {1}W, L{2}, W{3}mm, H{4}mm".format(rm, R_POW, rl, rw, rh)
    tags = "Radial Vertical Symmetric Pins RM {0}mm {1}W L{2} W{3}mm H{4}mm".format(rm, R_POW, rl, rw, rh)
    if (largepadsx>0 | largepadsx>0):
        description = description + ", Large Pads"
        tags = tags + " Large Pads"
    for t in specialtags:
        description = description + ", " + t
        tags = tags + " " + t
    mat_fn = ""
    if (material != ""):
        description = material + ", " + description
        tags = material + " " + tags
        mat_fn = "_" + material
    description = "Resistor, " + description
    tags = "Resistor R " + tags


    if (specialfpname!=""):
        footprint_name=specialfpname;
    else:
        footprint_name = "Resistor{4}_Radial_PinsSymetric_L{1}mm-W{2}mm-H{3}mm-p{0}mm".format(rmdisp, rl, rw, rh,mat_fn)
    print(footprint_name)

    # init kicad footprint
    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription(description)
    kicad_mod.setTags(tags)

    # set general values
    kicad_mod.append(Text(type='reference', text='REF**', at=[rm/2, t_slk-txt_offset], layer='F.SilkS'))
    kicad_mod.append(Text(type='value', text=footprint_name, at=[rm/2, h_slk/2+txt_offset], layer='F.Fab'))

    # create FAB-layer
    kicad_mod.append(RectLine(start=[left, top], end=[left+w, top+h], layer='F.Fab', width=lw_fab))

    # create SILKSCREEN-layer
    kicad_mod.append(RectLine(start=[l_slk, t_slk], end=[l_slk+w_slk, t_slk+h_slk], layer='F.SilkS'))
    if (rw!=rh):
        kicad_mod.append(Line(start=[xl1_slk, t_slk], end=[xl1_slk, t_slk+h_slk], layer='F.SilkS'))
        kicad_mod.append(Line(start=[xl2_slk, t_slk], end=[xl2_slk, t_slk+h_slk], layer='F.SilkS'))

    # create courtyard
    kicad_mod.append(RectLine(start=[roundCrt(l_crt), roundCrt(t_crt)], end=[roundCrt(l_crt+w_crt), roundCrt(t_crt+h_crt)], layer='F.CrtYd', width=lw_crt))

    # create pads
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



#                                   _____________
#                                   | |     * | |rm2
# power resistor, center+45° wires, | |  * rm1| |
#                                   |_|_______|_|
def makeRES_VERT_45DegWIRES(rm1, rm2, rl, rw, rh, ddrill, material, R_POW, x_3d=[0,0,0], s_3d=[1/2.54,1/2.54,1/2.54], has3d=1, specialfpname="", specialtags=[], largepadsx=0, largepadsy=0):
    rmdisp=roundG(math.sqrt(rm1*rm1+rm2*rm2), 0.01)
    padx=2*ddrill
    pady=padx
    if (largepadsx>0):
        padx=max(padx, largepadsx)
    if (largepadsy>0):
        pady=max(pady, largepadsy)
    crt_offset=0.25
    slk_offset=0.15
    lw_fab=0.1
    lw_crt=0.05
    lw_slk=0.15
    txt_offset=1

    w=rh
    h=rw
    left=-w/2
    top=-h/2
    h_slk=h+2*slk_offset
    w_slk=w+2*slk_offset
    l_slk=left-slk_offset
    r_slk=l_slk+w_slk
    t_slk=-h_slk/2
    yl1_slk=top+(rw-rh)/2
    yl2_slk=yl1_slk+rh
    w_crt=w_slk+2*crt_offset
    h_crt=h_slk+2*crt_offset
    l_crt=l_slk-crt_offset
    t_crt=t_slk-crt_offset


    lib_name = "Resistors_ThroughHole"
    description = "Radial, Vertical, 45° pins, RM {0}mm, {1}W, L{2}, W{3}mm, H{4}mm".format(rmdisp, R_POW, rl, rw, rh)
    tags = "Radial Vertical 45° Pins RM {0}mm {1}W L{2} W{3}mm H{4}mm".format(rmdisp, R_POW, rl, rw, rh)
    if (largepadsx>0 | largepadsx>0):
        description = description + ", Large Pads"
        tags = tags + " Large Pads"
    for t in specialtags:
        description = description + ", " + t
        tags = tags + " " + t
    mat_fn = ""
    if (material != ""):
        description = material + ", " + description
        tags = material + " " + tags
        mat_fn = "_" + material
    description = "Resistor, " + description
    tags = "Resistor R " + tags


    if (specialfpname!=""):
        footprint_name=specialfpname;
    else:
        footprint_name = "Resistor{4}_Radial_PinsSymetric_L{1}mm-W{2}mm-H{3}mm-p{0}mm".format(rmdisp, rl, rw, rh,mat_fn)
    print(footprint_name)

    # init kicad footprint
    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription(description)
    kicad_mod.setTags(tags)

    # set general values
    kicad_mod.append(Text(type='reference', text='REF**', at=[l_slk-txt_offset, 0], rotation=90, layer='F.SilkS'))
    kicad_mod.append(Text(type='value', text=footprint_name, at=[w_slk/2+txt_offset,0], rotation=90, layer='F.Fab'))

    # create FAB-layer
    kicad_mod.append(RectLine(start=[left, top], end=[left+w, top+h], layer='F.Fab', width=lw_fab))

    # create SILKSCREEN-layer
    kicad_mod.append(RectLine(start=[l_slk, t_slk], end=[l_slk+w_slk, t_slk+h_slk], layer='F.SilkS'))
    if (rw!=rh):
        kicad_mod.append(Line(start=[l_slk, yl1_slk], end=[l_slk+w_slk, yl1_slk], layer='F.SilkS'))
        kicad_mod.append(Line(start=[l_slk, yl2_slk], end=[l_slk+w_slk, yl2_slk], layer='F.SilkS'))

    # create courtyard
    kicad_mod.append(RectLine(start=[roundCrt(l_crt), roundCrt(t_crt)], end=[roundCrt(l_crt+w_crt), roundCrt(t_crt+h_crt)], layer='F.CrtYd', width=lw_crt))

    # create pads
    kicad_mod.append(Pad(number=1, type=Pad.TYPE_THT, shape=Pad.SHAPE_OVAL, at=[0, 0], size=[padx, pady], drill=ddrill, layers=['*.Cu', '*.Mask']))
    kicad_mod.append(Pad(number=2, type=Pad.TYPE_THT, shape=Pad.SHAPE_OVAL, at=[rm2, rm1], size=[padx, pady], drill=ddrill, layers=['*.Cu', '*.Mask']))

    # add model
    if (has3d!=0):
        kicad_mod.append(Model(filename=lib_name + ".3dshapes/"+footprint_name+".wrl", at=x_3d, scale=s_3d, rotate=[0, 0, 0]))

    # print render tree
    # print(kicad_mod.getRenderTree())
    # print(kicad_mod.getCompleteRenderTree())

    # write file
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile(footprint_name+'.kicad_mod')





if __name__ == '__main__':
    #                        rm, rmdisp,    rl,    rw,    rh,  ddrill,    material,   R_POW,        x_3d=[0,0,0],  s_3d=[1/2.54,1/2.54,1/2.54], has3d=1,                               specialfpname="",                                     specialtags=[]
    makeRES_RECT_HOR(      25.4,     25,    19,     8,     8,       1,   "Ceramic",     "5",         [0.5, 0, 0],                   [4, 4, 4 ],       1)
    makeRES_RECT_HOR(     30.48,     30,    23,     9,     9,     1.2,   "Ceramic",     "7",         [0.6, 0, 0],                   [4, 4, 4 ],       1)
    makeRES_RECT_HOR(     45.72,     45,    36,    11,    10,     1.2,   "Ceramic",     "9",         [0.9, 0, 0],                   [4, 4, 4 ],       1)
    makeRES_RECT_HOR(     60.96,     60,    50,    14,    13,     1.2,   "Ceramic",    "11",         [1.2, 0, 0],                   [4, 4, 4 ],       1)
    makeRES_RECT_HOR(     80.01,     80,    65,    16,    15,     1.2,   "Ceramic",    "17",        [1.58, 0, 0],                [3.95, 4, 4 ],       1)
    makeRES_RECT_HOR(   35.0012,     35,    20,   6.6,   6.6,     1.2,   "Ceramic",     "2",           [0, 0, 0],       [1/2.54,1/2.54,1/2.54],       0,      "Resistor_Cement_Horizontal_Meggitt-SBC-2",                         ["Meggit", "SBC", "SBC-2"])

    #                        rm, rmdisp,    rl,    rw,    rh,  ddrill,    material,   R_POW,        x_3d=[0,0,0],  s_3d=[1/2.54,1/2.54,1/2.54], has3d=1,                                         specialfpname="",                                      specialtags=[], largepadsx=0, largepadsy=0
    makeRES_VERT(             5,      5,  25.5,    14,    10,     1.2,    "Cement",  "5W 7",          [0, 0, 0],       [1/2.54,1/2.54,1/2.54],       0,                  "Resistor_Cement_Vertical_KOA-BGR-5N-7N",       ["Meggitt","KOA","BSR","BGR","BWR","5N","7N"])
    makeRES_VERT(             5,      5,  25.5,    14,    10,     1.2,    "Cement",  "5W 7",          [0, 0, 0],       [1/2.54,1/2.54,1/2.54],       0,        "Resistor_Cement_Vertical_LargePads_KOA-BGR-5N-7N",       ["Meggitt","KOA","BSR","BGR","BWR","5N","7N"],            3)
    makeRES_VERT(             5,      5,  25.5,    13,     9,     1.2,    "Cement",     "3",          [0, 0, 0],       [1/2.54,1/2.54,1/2.54],       0,                              "Resistor_Cement_KOA-BGR-3N",            ["Meggitt","KOA","BSR","BGR","BWR","3N"])
    makeRES_VERT(             5,      5,  25.5,    13,     9,     1.2,    "Cement",     "3",          [0, 0, 0],       [1/2.54,1/2.54,1/2.54],       0,                    "Resistor_Cement_LargePads_KOA-BGR-3N",            ["Meggitt","KOA","BSR","BGR","BWR","3N"],            3)

    #                                 rm1,      rm2,     rl,    rw,    rh,  ddrill,    material,   R_POW,        x_3d=[0,0,0],  s_3d=[1/2.54,1/2.54,1/2.54], has3d=1,                                         specialfpname="",                                      specialtags=[], largepadsx=0, largepadsy=0
    #makeRES_VERT_45DegWIRES(          2.4,      2.3,   25.5,    13,     9,     1.2,    "Cement",     "3",          [0, 0, 0],       [1/2.54,1/2.54,1/2.54],       0,                                                        "",            ["Meggitt","KOA","BSR","BGR","BWR","3N"])

    #                          rm, rmdisp,   w,   h, ddrill,   R_POW,        x_3d=[0,0,0],  s_3d=[1/2.54,1/2.54,1/2.54], has3d=1, specialfpname=""
    makeRES_SIMPLERECT_HOR(   7.62,     7, 3.4, 1.7,        1,   "1/8",         [0.5, 0, 0],                   [4, 4, 4 ],       0)
    makeRES_SIMPLERECT_HOR(  10.16,    10, 6.5, 2.3,        1,   "1/4",         [0.2, 0, 0],             [0.4, 0.4, 0.4 ],       1)
    makeRES_SIMPLERECT_HOR(     15,    15,  10, 2.3,        1,   "1/4",       [0.295, 0, 0],           [0.395, 0.4, 0.4 ],       1)
    makeRES_SIMPLERECT_HOR(     20,    20,  15,   5,        1,    "2",        [0.395, 0, 0],           [0.395, 0.4, 0.4 ],       1)
    makeRES_SIMPLERECT_HOR(     25,    25,  17,   6,        1,    "3",            [0, 0, 0],       [1/2.54,1/2.54,1/2.54],       0)
    makeRES_SIMPLERECT_HOR(     30,    30,  24,   8,      1.2,    "5",            [0, 0, 0],       [1/2.54,1/2.54,1/2.54],       0)

    #                          rm, rmdisp,    l,      d, ddrill,   R_POW,    x_3d=[0,0,0],   s_3d=[1/2.54,1/2.54,1/2.54], has3d=1, specialfpname="", largepadsx=0, largepadsy=0
    makeRES_SIMPLECIRC_VER(   5.08,     5,   15,      5,      1,     "2",       [0, 0, 0],        [1/2.54,1/2.54,1/2.54],       0)
    makeRES_SIMPLECIRC_VER(    7.5,   7.5,   24,     10,      1,     "5",       [0, 0, 0],        [1/2.54,1/2.54,1/2.54],       0)

    #rm, rmdisp, l, w, h, ddrill, material, R_POW, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54],  has3d=1, specialfpname="", largepadsx=0, largepadsy=0, specialtags=[]
    #                          rm, rmdisp,    l,      w,      h, ddrill,      material,    R_POW,    x_3d=[0,0,0],   s_3d=[1/2.54,1/2.54,1/2.54], has3d=1, specialfpname="", largepadsx=0, largepadsy=0
    #makeRES_SIMPLERECT_VER(   7.5,    7.5,   24,     10,     10,      1,     "Ceramic",      "5",       [0, 0, 0],        [1/2.54,1/2.54,1/2.54],       0)
    #makeRES_SIMPLERECT_VER( 10.16,     10,   24,     10,     10,      1,     "Ceramic",      "5",       [0, 0, 0],        [1/2.54,1/2.54,1/2.54],       0)
