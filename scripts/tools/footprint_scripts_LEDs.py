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


# LED footprints
#   style options:
#     1. type="box"
#           +----------------+ ^
#           |                | |
#           |  OO        OO  | h
#           |                | |
#           +----------------+ v
#               <---rm--->
#           <-------w-------->
#     2. type="round"
#              /----------\   ^
#             |            \  |
#             |  OO    OO   | h
#             |            /  |
#              \__________/   v
#                 <-rm->
#           <-------w-------->
#     3. type="roundedbox"
#           +--------------\   ^
#           |               \  |
#           |  OO        OO  | h
#           |               /  |
#           +--------------/   v
#               <---rm--->
#           <-------w-------->
#     4. type="oval"
#           +----------------+ ^
#           |                | |
#           |  OO        OO  | h
#           |                | |
#           +----------------+ v
#               <---rm--->
#           <-------w-------->
#     2. type="round_simple"
#              /----------\   ^
#             /            \  |
#            |   OO    OO   | h
#             \            /  |
#              \__________/   v
#                 <-rm->
#           <-------w-------->
# in the center a second circle is drawn if rin>0
def makeLEDRadial(rm, w, h, ddrill, win=0, rin=0, pins=2, type="round", x_3d=[0, 0, 0],
                  s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], has3d=1, specialfpname="", specialtags=[], add_description="",
                  classname="LED", lib_name="LEDs", name_additions=[], script3d="", height3d=8, height3d_bottom=1):
    padx = 2 * ddrill
    pady = padx
    if padx + min_pad_distance > rm:
        padx = (rm - min_pad_distance)
    txtoffset = txt_offset
    
    pad1style = Pad.SHAPE_RECT
    
    padpos = []
    offset = [0, 0]
    overpad_width = (pins - 1) * rm
    xpad = -overpad_width / 2
    offset = [-xpad, 0]
    for p in range(1, pins + 1):
        padpos.append([p, xpad, 0, ddrill, padx, pady])
        xpad = xpad + rm
    
    l_fab = -w / 2
    t_fab = -h / 2
    w_fab = w
    h_fab = h
    d_fab = max(w, h)
    d2_fab = rin
    h_slk = h_fab + 2 * slk_offset
    w_slk = w_fab + 2 * slk_offset
    l_slk = l_fab - slk_offset
    t_slk = t_fab - slk_offset
    d_slk = d_fab + lw_slk + slk_offset
    w_crt = max(w_slk, overpad_width + padx) + 2 * crt_offset
    h_crt = max(h_slk, pady) + 2 * crt_offset
    l_crt = -w_crt / 2
    t_crt = -h_crt / 2
    
    snfp = ""
    sn = ""
    snt = ""
    
    fnsize = ""
    sizetag = ""
    if type == "round" or type == "round_simple":
        fnsize = "_D{0:0.1f}mm".format(rin)
        sizetag = "diameter {0:0.1f}mm".format(rin)
    else:
        if type == "oval":
            sizetag = " Oval"
        if type == "box":
            sizetag = " Rectangular"
        wsize = w
        if type == "box" and win > 0:
            wsize = win
        fnsize = fnsize + "_W{0:0.1f}mm_H{1:0.1f}mm".format(wsize, h)
        sizetag = sizetag + " size {0:0.1f}x{1:0.1f}mm^2".format(wsize, h)
        if rin > 0:
            fnsize = "_D{0:0.1f}mm".format(rin) + fnsize
            sizetag = sizetag + " diameter {0:0.1f}mm".format(rin)
    
    fnpincnt = ""
    pincnttag = "{0:d} pins".format(pins)
    if pins > 2:
        fnpincnt = "-{0:d}".format(pins)
        if type == "box":
            fnpincnt = fnpincnt + "pins"
    
    footprint_name = classname + fnsize + fnpincnt
    
    description = classname
    tags = classname
    
    addedtags = specialtags
    if len(sizetag) > 0:
        addedtags.append(sizetag)
    if len(pincnttag) > 0:
        addedtags.append(pincnttag)
    
    for t in addedtags:
        description = description + ", " + t
        tags = tags + " " + t
    if (specialfpname != ""):
        footprint_name = specialfpname;
    
    if len(add_description) > 0:
        description = description + ", " + add_description
    
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
            myfile.write("# d_wire\nApp.ActiveDocument.Spreadsheet.set('B4', '0.02')\n")
            myfile.write("App.ActiveDocument.recompute()\n")
            myfile.write("# rin\nApp.ActiveDocument.Spreadsheet.set('B1', '{0}')\n".format(rin))
            myfile.write("# w\nApp.ActiveDocument.Spreadsheet.set('B2', '{0}')\n".format(w))
            myfile.write("# h\nApp.ActiveDocument.Spreadsheet.set('C2', '{0}')\n".format(h))
            myfile.write("# RM\nApp.ActiveDocument.Spreadsheet.set('B3', '{0}')\n".format(rm))
            myfile.write("# d_wire\nApp.ActiveDocument.Spreadsheet.set('B4', '{0}')\n".format(ddrill - 0.3))
            myfile.write("# H\nApp.ActiveDocument.Spreadsheet.set('B5', '{0}')\n".format(height3d))
            myfile.write("# H_bottom\nApp.ActiveDocument.Spreadsheet.set('B6', '{0}')\n".format(height3d_bottom))
            myfile.write("App.ActiveDocument.recompute()\n")
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
    kicad_modg.append(Text(type='reference', text='REF**', at=[0, t_slk - txtoffset], layer='F.SilkS'))
    kicad_modg.append(Text(type='value', text=footprint_name, at=[0, t_slk + h_slk + txtoffset], layer='F.Fab'))
    
    # create FAB-layer
    if type == "round":
        kicad_modg.append(Circle(center=[0, 0], radius=d2_fab / 2, layer='F.Fab', width=lw_fab))
        xmark = d2_fab / 2
        ymark = math.sqrt(d_fab * d_fab / 4 - xmark * xmark)
        alpha = 360 - 2 * math.atan(ymark / xmark) / 3.1415 * 180
        kicad_modg.append(Arc(center=[0, 0], start=[-xmark, -ymark], angle=alpha, layer='F.Fab', width=lw_fab))
        kicad_modg.append(Line(start=[-xmark, -ymark], end=[-xmark, ymark], angle=alpha, layer='F.Fab', width=lw_fab))
    if type == "round_simple":
        kicad_modg.append(Circle(center=[0, 0], radius=d2_fab / 2, layer='F.Fab', width=lw_fab))
        kicad_modg.append(Circle(center=[0, 0], radius=d_fab / 2, layer='F.Fab', width=lw_fab))
    elif type == "box":
        kicad_modg.append(
            RectLine(start=[l_fab, t_fab], end=[l_fab + w_fab, t_fab + h_fab], layer='F.Fab', width=lw_fab))
        if d2_fab > 0:
            kicad_modg.append(Circle(center=[0, 0], radius=d2_fab / 2, layer='F.Fab', width=lw_fab))
        if win > 0:
            kicad_modg.append(
                RectLine(start=[-win / 2, t_fab], end=[win / 2, t_fab + h_fab], layer='F.Fab', width=lw_fab))
    elif type == "oval":
        r = w / 2
        ystart = 0
        xstart = math.sqrt(r * r - ystart * ystart)
        ycenter = h / 2 - r
        alpha = 180 - 2 * math.atan(math.fabs(ycenter) / xstart) / 3.1415 * 180
        kicad_modg.append(Arc(center=[0, -ycenter], start=[-xstart, ystart], angle=alpha, layer='F.Fab', width=lw_fab))
        kicad_modg.append(Arc(center=[0, ycenter], start=[-xstart, -ystart], angle=-alpha, layer='F.Fab', width=lw_fab))
    
    # build keepeout for SilkScreen
    keepouts = []
    for p in padpos:
        if p[0] == 1:
            keepouts = keepouts + addKeepoutRect(p[1], p[2], p[4] + 2 * lw_slk + 2 * slk_offset,
                                                 p[5] + 2 * lw_slk + 2 * slk_offset)
        else:
            keepouts = keepouts + addKeepoutRound(p[1], p[2], p[4] + 2 * lw_slk + 2 * slk_offset,
                                                  p[5] + 2 * lw_slk + 2 * slk_offset)
    
    # create SILKSCREEN-layer
    if type == "box":
        addRectWithKeepout(kicad_modg, l_slk, t_slk, w_slk, h_slk, 'F.SilkS', lw_slk, keepouts)
        if pins == 3:
            addVLineWithKeepout(kicad_modg, -offset[0] + rm / 2, t_slk, t_slk + h_slk, 'F.SilkS', lw_slk, keepouts)
        else:
            addVLineWithKeepout(kicad_modg, l_slk + lw_slk, t_slk, t_slk + h_slk, 'F.SilkS', lw_slk, keepouts)
            addVLineWithKeepout(kicad_modg, l_slk + 2 * lw_slk, t_slk, t_slk + h_slk, 'F.SilkS', lw_slk, keepouts)
    elif type == "round":
        xmark = d2_fab / 2 + slk_offset
        ymark = math.sqrt(d_slk * d_slk / 4 - xmark * xmark)
        ypad = pady / 2 + slk_offset + lw_slk
        xpad = math.sqrt(d_slk * d_slk / 4 - ypad * ypad)
        alphamark = math.atan(ymark / xmark) / 3.1415 * 180
        alphapad = math.atan(ypad / xpad) / 3.1415 * 180
        alpha = 180 - alphamark
        if containedInAnyKeepout(xmark, 0.1, keepouts) or containedInAnyKeepout(d_fab / 2, 0.1, keepouts):
            alpha = alpha - alphapad
        kicad_modg.append(Arc(center=[0, 0], start=[-xmark, -ymark], angle=alpha, layer='F.SilkS', width=lw_slk))
        kicad_modg.append(Arc(center=[0, 0], start=[-xmark, ymark], angle=-alpha, layer='F.SilkS', width=lw_slk))
        addVLineWithKeepout(kicad_modg, -xmark, -ymark, ymark, 'F.SilkS', lw_slk, keepouts)
        
        ypad = pady / 2 + slk_offset + lw_slk
        xpad = math.sqrt(d2_fab * d2_fab / 4 - ypad * ypad)
        alphapad = math.atan(ypad / xpad) / 3.1415 * 180
        
        alpha = 180
        if containedInAnyKeepout(d2_fab / 2, 0.1, keepouts) or containedInAnyKeepout(-d2_fab / 2, 0.1, keepouts):
            alpha = alpha - 2 * alphapad
        if alpha == 180:
            kicad_modg.append(Circle(center=[0, 0], radius=d2_fab / 2, layer='F.SilkS', width=lw_slk))
        else:
            kicad_modg.append(Arc(center=[0, 0], start=[-xpad, -ypad], angle=alpha, layer='F.SilkS', width=lw_slk))
            kicad_modg.append(Arc(center=[0, 0], start=[-xpad, ypad], angle=-alpha, layer='F.SilkS', width=lw_slk))
    elif type == "round_simple":
        rs = [d2_fab, d_slk]
        xpads = []
        ypads = []
        fullCircle = False
        for r in rs:
            ypad = pady / 2 + slk_offset + lw_slk
            xpad = math.sqrt(r * r / 4 - ypad * ypad)
            xpads.append(xpad)
            ypads.append(ypad)
            alphapad = math.atan(ypad / xpad) / 3.1415 * 180
            
            alpha = 180
            if containedInAnyKeepout(r / 2, 0.1, keepouts) or containedInAnyKeepout(-r / 2, 0.1, keepouts):
                alpha = alpha - 2 * alphapad
            if alpha == 180:
                kicad_modg.append(Circle(center=[0, 0], radius=r / 2, layer='F.SilkS', width=lw_slk))
                fullCircle = True
            else:
                kicad_modg.append(Arc(center=[0, 0], start=[-xpad, -ypad], angle=alpha, layer='F.SilkS', width=lw_slk))
                kicad_modg.append(Arc(center=[0, 0], start=[-xpad, ypad], angle=-alpha, layer='F.SilkS', width=lw_slk))
        if fullCircle:
            x = -d_slk / 2 + lw_slk * 2
            y = math.sqrt(d_slk * d_slk / 4 - x * x)
            kicad_modg.append(Line(start=[x, -y], end=[x, y], layer='F.SilkS', width=lw_slk))
        else:
            kicad_modg.append(
                Line(start=[-xpads[0], ypads[0]], end=[-xpads[1], ypads[0]], layer='F.SilkS', width=lw_slk))
            kicad_modg.append(
                Line(start=[-xpads[0], -ypads[0]], end=[-xpads[1], -ypads[0]], layer='F.SilkS', width=lw_slk))
    elif type == "oval":
        r = w_slk / 2
        ystart = 0
        xstart = math.sqrt(r * r - ystart * ystart)
        ycenter = h_slk / 2 - r
        alpha = 180 - 2 * math.atan(math.fabs(ycenter) / xstart) / 3.1415 * 180
        kicad_modg.append(
            Arc(center=[0, -ycenter], start=[-xstart, ystart], angle=alpha, layer='F.SilkS', width=lw_slk))
        kicad_modg.append(
            Arc(center=[0, ycenter], start=[-xstart, -ystart], angle=-alpha, layer='F.SilkS', width=lw_slk))
        xmark = -xstart + 2 * lw_slk
        ymark = ycenter + math.sqrt(r * r - xmark * xmark)
        print(ymark, ycenter, ymark + ycenter)
        addVLineWithKeepout(kicad_modg, xmark, -ymark, ymark, 'F.SilkS', lw_slk, keepouts)
    
    # create courtyard
    kicad_mod.append(RectLine(start=[roundCrt(l_crt + offset[0]), roundCrt(t_crt + offset[1])],
                              end=[roundCrt(l_crt + w_crt + offset[0]), roundCrt(t_crt + h_crt + offset[1])],
                              layer='F.CrtYd', width=lw_crt))

    # debug_draw_keepouts(kicad_modg, keepouts)
    
    # create pads
    pn = 1
    for p in padpos:
        ps = Pad.SHAPE_CIRCLE
        if (p[4] != p[5]):
            ps = Pad.SHAPE_OVAL
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

