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
from drawing_tools import *  # NOQA


def makePinHeadStraight(rows, cols, rm, coldist, package_width, overlen_top, overlen_bottom, ddrill, pad,
                        tags_additional=[], lib_name="Pin_Headers", classname="Pin_Header", classname_description="pin header", offset3d=[0, 0, 0], scale3d=[1, 1, 1],
                        rotate3d=[0, 0, 0], isSocket=False):
    h_fab = (rows - 1) * rm + overlen_top + overlen_bottom
    w_fab = package_width
    l_fab = (coldist * (cols - 1) - w_fab) / 2
    t_fab = -overlen_top
    
    h_slk = h_fab + 2 * slk_offset
    w_slk = max(w_fab + 2 * slk_offset, coldist * (cols - 1) - pad[0] - 4 * slk_offset)
    l_slk = (coldist * (cols - 1) - w_slk) / 2
    t_slk = -overlen_top - slk_offset
    
    w_crt = max(package_width, coldist * (cols - 1) + pad[0]) + 2 * crt_offset
    h_crt = max(h_fab, (rows - 1) * rm + pad[1]) + 2 * crt_offset
    l_crt = coldist * (cols - 1) / 2 - w_crt / 2
    t_crt = (rows - 1) * rm / 2 - h_crt / 2
    
    # if rm == 2.54:
    #    footprint_name = "Pin_Header_Straight_{0}x{1:02}".format(cols, rows)
    # else:
    footprint_name = "{3}_Straight_{0}x{1:02}_Pitch{2:03.2f}mm".format(cols, rows, rm,classname)
    
    description = "Through hole straight {3}, {0}x{1:02}, {2:03.2f}mm pitch".format(cols, rows, rm,classname_description)
    tags = "Through hole {3} THT {0}x{1:02} {2:03.2f}mm".format(cols, rows, rm,classname_description)
    if (cols == 1):
        description = description + ", single row"
        tags = tags + " single row"
    elif (cols == 2):
        description = description + ", double rows"
        tags = tags + " double row"
    elif (cols == 3):
        description = description + ", triple rows"
        tags = tags + " triple row"
    
    if (len(tags_additional) > 0):
        for t in tags_additional:
            footprint_name = footprint_name + "_" + t
            description = description + ", " + t
            tags = tags + " " + t
    
    print(footprint_name)
    
    # init kicad footprint
    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription(description)
    kicad_mod.setTags(tags)
    
    # anchor for SMD-symbols is in the center, for THT-sybols at pin1
    offset=[0,0]
    if isSocket and cols>1:
        offset = [-coldist, 0]
    kicad_modg = Translation(offset[0], offset[1])
    kicad_mod.append(kicad_modg)
    
    # set general values
    kicad_modg.append(
        Text(type='reference', text='REF**', at=[coldist * (cols - 1) / 2, t_slk - txt_offset], layer='F.SilkS'))
    kicad_modg.append(Text(type='value', text=footprint_name, at=[coldist * (cols - 1) / 2, t_slk + h_slk + txt_offset],
                           layer='F.Fab'))
    
    # create FAB-layer
    kicad_modg.append(RectLine(start=[l_fab, t_fab], end=[l_fab + w_fab, t_fab + h_fab], layer='F.Fab', width=lw_fab))
    
    # create SILKSCREEN-layer + pin1 marker
    if (cols == 1):
        kicad_modg.append(
            RectLine(start=[l_slk, 0.5 * rm], end=[l_slk + w_slk, t_slk + h_slk], layer='F.SilkS', width=lw_slk))
    else:
        if isSocket and cols>1:
            kicad_modg.append(PolygoneLine(
                polygone=[[l_slk+w_slk, 0.5 * rm], [l_slk+w_slk, t_slk + h_slk], [l_slk , t_slk + h_slk], [l_slk , t_slk],
                          [l_slk+w_slk/2, t_slk], [l_slk+w_slk/2, 0.5 * rm], [l_slk+w_slk, 0.5 * rm]], layer='F.SilkS', width=lw_slk))
        else:
            kicad_modg.append(PolygoneLine(
                polygone=[[l_slk, 0.5 * rm], [l_slk, t_slk + h_slk], [l_slk + w_slk, t_slk + h_slk], [l_slk + w_slk, t_slk],
                          [0.5 * rm, t_slk], [0.5 * rm, 0.5 * rm], [l_slk, 0.5 * rm]], layer='F.SilkS', width=lw_slk))
    if isSocket and cols>1:
        kicad_modg.append(PolygoneLine(polygone=[[l_slk+w_slk, 0], [l_slk+w_slk, t_slk], [l_slk+w_slk-rm/2, t_slk]], layer='F.SilkS', width=lw_slk))
    else:
        kicad_modg.append(PolygoneLine(polygone=[[l_slk, 0], [l_slk, t_slk], [0, t_slk]], layer='F.SilkS', width=lw_slk))

    # create courtyard
    kicad_mod.append(RectLine(start=[roundCrt(l_crt + offset[0]), roundCrt(t_crt + offset[1])],
                              end=[roundCrt(l_crt + offset[0] + w_crt), roundCrt(t_crt + offset[1] + h_crt)],
                              layer='F.CrtYd', width=lw_crt))
    
    # create pads
    p1 = int(1)
    x1 = 0
    y1 = 0
    
    pad_type = Pad.TYPE_THT
    pad_shape1 = Pad.SHAPE_RECT
    pad_shapeother = Pad.SHAPE_OVAL
    pad_layers = '*'
    
    p = 1
    
    for r in range(1, rows + 1):
        
        if isSocket and cols>1:
            x1=coldist
        else:
            x1 = 0
        for c in range(1, cols + 1):
            if p == 1:
                kicad_modg.append(Pad(number=p, type=pad_type, shape=pad_shape1, at=[x1, y1], size=pad, drill=ddrill,
                                      layers=[pad_layers + '.Cu', pad_layers + '.Mask']))
            else:
                kicad_modg.append(
                    Pad(number=p, type=pad_type, shape=pad_shapeother, at=[x1, y1], size=pad, drill=ddrill,
                        layers=[pad_layers + '.Cu', pad_layers + '.Mask']))
            
            p = p + 1
            if isSocket and cols>1:
                x1 = x1 - coldist
            else:
                x1 = x1 + coldist
        
        y1 = y1 + rm
    
    # add model
    kicad_modg.append(
        Model(filename=lib_name + ".3dshapes/" + footprint_name + ".wrl", at=offset3d, scale=scale3d, rotate=rotate3d))
    
    # print render tree
    # print(kicad_mod.getRenderTree())
    # print(kicad_mod.getCompleteRenderTree())
    
    # write file
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile(footprint_name + '.kicad_mod')


#
#             <-->pack_offset
#                 <------->pack_width
#                          <------------------------------>pin_length
#    <-coldist>
# +---            +-------+
# | OOO      OOO  |       +-------------------------------+            ^
# | OOO ==== OOO  |       |                               +    ^       pin_width
#   OOO      OOO  |       +-------------------------------+    |       v
#                 +-------+                                    rm
#   OOO      OOO  |       +-------------------------------+    |
#   OOO ==== OOO  |       |                               +    v
#   OOO      OOO  |       +-------------------------------+
#                 +-------+                                    rm
#
def makePinHeadAngled(rows, cols, rm, coldist, pack_width, pack_offset, pin_length, pin_width, ddrill, pad,
                      tags_additional=[], lib_name="Pin_Headers", classname="Pin_Header",
                      classname_description="pin header", offset3d=[0, 0, 0], scale3d=[1, 1, 1],
                      rotate3d=[0, 0, 0]):
    h_fabb = (rows - 1) * rm + rm / 2 + rm / 2
    w_fabb = pack_width
    l_fabb = coldist * (cols - 1) + pack_offset
    t_fabb = -rm / 2
    l_fabp = l_fabb + w_fabb
    t_fabp = -pin_width / 2
    
    h_slkb = h_fabb + 2 * slk_offset
    w_slkb = w_fabb + 2 * slk_offset
    l_slkb = l_fabb - slk_offset
    t_slkb = t_fabb - slk_offset
    l_slkp = l_slkb + w_slkb
    t_slkp = t_fabp - slk_offset
    l_slk = -rm / 2
    t_slk = -rm / 2
    
    w_crt = rm / 2 + (cols - 1) * coldist + pack_offset + pack_width + pin_length + 2 * crt_offset
    h_crt = h_fabb + 2 * crt_offset
    l_crt = -rm / 2 - crt_offset
    t_crt = -rm / 2 - crt_offset
    
    # if rm == 2.54:
    #    footprint_name = "Pin_Header_Angled_{0}x{1:02}".format(cols, rows)
    # else:
    footprint_name = "{3}_Angled_{0}x{1:02}_Pitch{2:03.2f}mm".format(cols, rows, rm, classname)
    
    description = "Through hole angled {4}, {0}x{1:02}, {2:03.2f}mm pitch, {3}mm pin length".format(cols, rows,
                                                                                                    rm,
                                                                                                    pin_length,
                                                                                                    classname_description)
    tags = "Through hole angled {3} THT {0}x{1:02} {2:03.2f}mm".format(cols, rows, rm, classname_description)
    if (cols == 1):
        description = description + ", single row"
        tags = tags + " single row"
    elif (cols == 2):
        description = description + ", double rows"
        tags = tags + " double row"
    elif (cols == 3):
        description = description + ", triple rows"
        tags = tags + " triple row"
    
    if (len(tags_additional) > 0):
        for t in tags_additional:
            footprint_name = footprint_name + "_" + t
            description = description + ", " + t
            tags = tags + " " + t
    
    print(footprint_name)
    
    # init kicad footprint
    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription(description)
    kicad_mod.setTags(tags)
    
    # anchor for SMD-symbols is in the center, for THT-sybols at pin1
    offset = [0, 0]
    kicad_modg = Translation(offset[0], offset[1])
    kicad_mod.append(kicad_modg)
    
    # set general values
    kicad_modg.append(
        Text(type='reference', text='REF**', at=[l_crt + w_crt / 2, t_crt + crt_offset - txt_offset], layer='F.SilkS'))
    kicad_modg.append(
        Text(type='value', text=footprint_name, at=[l_crt + w_crt / 2, t_crt + h_crt - crt_offset + txt_offset],
             layer='F.Fab'))
    
    # create FAB-layer
    y1 = t_fabb
    yp = t_fabp
    for r in range(1, rows + 1):
        kicad_modg.append(RectLine(start=[l_fabb, y1], end=[l_fabb + w_fabb, y1 + rm], layer='F.Fab', width=lw_fab))
        kicad_modg.append(
            RectLine(start=[0, yp], end=[l_fabp + pin_length, yp + pin_width], layer='F.Fab', width=lw_fab))
        y1 = y1 + rm
        yp = yp + rm
    
    # create SILKSCREEN-layer + pin1 marker
    y1 = t_slkb
    yp = t_slkp
    for r in range(1, rows + 1):
        if (rows == 1 and r == 1):
            kicad_modg.append(
                RectLine(start=[l_slkb, y1], end=[l_slkb + w_slkb, y1 + rm + 2 * slk_offset], layer='F.SilkS',
                         width=lw_slk))
        if (r == 1 or r == rows):
            kicad_modg.append(RectLine(start=[l_slkb, y1], end=[l_slkb + w_slkb, y1 + rm + slk_offset], layer='F.SilkS',
                                       width=lw_slk))
            y1 = y1 + slk_offset
        else:
            kicad_modg.append(
                RectLine(start=[l_slkb, y1], end=[l_slkb + w_slkb, y1 + rm], layer='F.SilkS', width=lw_slk))
        kicad_modg.append(
            RectLine(start=[l_slkp, yp], end=[l_slkp + pin_length, yp + pin_width + 2 * slk_offset], layer='F.SilkS',
                     width=lw_slk))
        kicad_modg.append(
            Line(start=[(cols - 1) * coldist + pad[0] / 2 + slk_offset, yp], end=[l_slkb, yp], layer='F.SilkS',
                 width=lw_slk))
        kicad_modg.append(Line(start=[(cols - 1) * coldist + pad[0] / 2 + slk_offset, yp + pin_width + 2 * slk_offset],
                               end=[l_slkb, yp + pin_width + 2 * slk_offset], layer='F.SilkS', width=lw_slk))
        if cols > 1:
            for c in range(2, cols + 1):
                kicad_modg.append(Line(start=[(c - 2) * coldist + pad[0] / 2 + slk_offset, yp],
                                       end=[(c - 1) * coldist - pad[0] / 2 - slk_offset, yp], layer='F.SilkS',
                                       width=lw_slk))
                kicad_modg.append(
                    Line(start=[(c - 2) * coldist + pad[0] / 2 + slk_offset, yp + pin_width + 2 * slk_offset],
                         end=[(c - 1) * coldist - pad[0] / 2 - slk_offset, yp + pin_width + 2 * slk_offset],
                         layer='F.SilkS', width=lw_slk))
        if r == 1:
            y = yp + lw_slk
            while y < yp + pin_width + 2 * slk_offset:
                kicad_modg.append(Line(start=[l_slkp, y], end=[l_slkp + pin_length, y], layer='F.SilkS', width=lw_slk))
                y = y + lw_slk
        y1 = y1 + rm
        yp = yp + rm
    
    kicad_modg.append(PolygoneLine(polygone=[[l_slk, 0], [l_slk, t_slk], [0, t_slk]], layer='F.SilkS', width=lw_slk))
    
    # create courtyard
    kicad_mod.append(RectLine(start=[roundCrt(l_crt + offset[0]), roundCrt(t_crt + offset[1])],
                              end=[roundCrt(l_crt + offset[0] + w_crt), roundCrt(t_crt + offset[1] + h_crt)],
                              layer='F.CrtYd', width=lw_crt))
    
    # create pads
    p1 = int(1)
    x1 = 0
    y1 = 0
    
    pad_type = Pad.TYPE_THT
    pad_shape1 = Pad.SHAPE_RECT
    pad_shapeother = Pad.SHAPE_OVAL
    pad_layers = '*'
    
    p = 1
    
    for r in range(1, rows + 1):
        x1 = 0
        for c in range(1, cols + 1):
            if p == 1:
                kicad_modg.append(Pad(number=p, type=pad_type, shape=pad_shape1, at=[x1, y1], size=pad, drill=ddrill,
                                      layers=[pad_layers + '.Cu', pad_layers + '.Mask']))
            else:
                kicad_modg.append(
                    Pad(number=p, type=pad_type, shape=pad_shapeother, at=[x1, y1], size=pad, drill=ddrill,
                        layers=[pad_layers + '.Cu', pad_layers + '.Mask']))
            
            p = p + 1
            x1 = x1 + coldist
        
        y1 = y1 + rm
    
    # add model
    kicad_modg.append(
        Model(filename=lib_name + ".3dshapes/" + footprint_name + ".wrl", at=offset3d, scale=scale3d, rotate=rotate3d))
    
    # print render tree
    # print(kicad_mod.getRenderTree())
    # print(kicad_mod.getCompleteRenderTree())
    
    # write file
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile(footprint_name + '.kicad_mod')


#
#                                                          <-->pack_offset
#                 <--------------pack_width--------------->
#                                                             <-coldist>
#                 +---------------------------------------+            ---+
#                 |                                       |  OOO      OOO |          ^
#                 |                                       |  OOO ==== OOO |  ^       pin_width
#                 |                                       |  OOO      OOO    |       v
#                 +---------------------------------------+                  rm
#                 |                                       |  OOO      OOO    |
#                 |                                       |  OOO ==== OOO    v
#                 |                                       |  OOO      OOO
#                 +---------------------------------------+
#
def makeSocketStripAngled(rows, cols, rm, coldist, pack_width, pack_offset, pin_width, ddrill, pad,
                      tags_additional=[], lib_name="Socket_Strips", classname="Socket_Strip",
                      classname_description="socket strip", offset3d=[0, 0, 0], scale3d=[1, 1, 1],
                      rotate3d=[0, 0, 0]):
    h_fabb = (rows - 1) * rm + rm / 2 + rm / 2
    w_fabb = -pack_width
    l_fabb = -1*(coldist * (cols - 1) + pack_offset)
    t_fabb = -rm / 2
    l_fabp = l_fabb + w_fabb
    t_fabp = -pin_width / 2
    
    h_slkb = h_fabb + 2 * slk_offset
    w_slkb = w_fabb - 2 * slk_offset
    l_slkb = l_fabb + slk_offset
    t_slkb = t_fabb - slk_offset
    l_slkp = l_slkb + w_slkb
    t_slkp = t_fabp - slk_offset
    l_slk = -rm / 2
    t_slk = -rm / 2
    
    w_crt = -1*(rm / 2 + (cols - 1) * coldist + pack_offset + pack_width  + 2 * crt_offset)
    h_crt = h_fabb + 2 * crt_offset
    l_crt = rm / 2 + crt_offset
    t_crt = -rm / 2 - crt_offset
    
    # if rm == 2.54:
    #    footprint_name = "Pin_Header_Angled_{0}x{1:02}".format(cols, rows)
    # else:
    footprint_name = "{3}_Angled_{0}x{1:02}_Pitch{2:03.2f}mm".format(cols, rows, rm, classname)
    
    description = "Through hole angled {4}, {0}x{1:02}, {2:03.2f}mm pitch, {3}mm socket length".format(cols, rows,
                                                                                                    rm,
                                                                                                    pack_width,
                                                                                                    classname_description)
    tags = "Through hole angled {3} THT {0}x{1:02} {2:03.2f}mm".format(cols, rows, rm, classname_description)
    if (cols == 1):
        description = description + ", single row"
        tags = tags + " single row"
    elif (cols == 2):
        description = description + ", double rows"
        tags = tags + " double row"
    elif (cols == 3):
        description = description + ", triple rows"
        tags = tags + " triple row"
    
    if (len(tags_additional) > 0):
        for t in tags_additional:
            footprint_name = footprint_name + "_" + t
            description = description + ", " + t
            tags = tags + " " + t
    
    print(footprint_name)
    
    # init kicad footprint
    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription(description)
    kicad_mod.setTags(tags)
    
    # anchor for SMD-symbols is in the center, for THT-sybols at pin1
    offset = [0, 0]
    kicad_modg =Translation(offset[0], offset[1])
    kicad_mod.append(kicad_modg)
    
    # set general values
    kicad_modg.append(
        Text(type='reference', text='REF**', at=[l_crt + w_crt / 2, t_crt + crt_offset - txt_offset], layer='F.SilkS'))
    kicad_modg.append(
        Text(type='value', text=footprint_name, at=[l_crt + w_crt / 2, t_crt + h_crt - crt_offset + txt_offset],
             layer='F.Fab'))
    
    # create FAB-layer
    y1 = t_fabb
    yp = t_fabp
    for r in range(1, rows + 1):
        kicad_modg.append(RectLine(start=[l_fabb, y1], end=[l_fabb + w_fabb, y1 + rm], layer='F.Fab', width=lw_fab))
        kicad_modg.append(
            RectLine(start=[0, yp], end=[l_fabb , yp + pin_width], layer='F.Fab', width=lw_fab))
        y1 = y1 + rm
        yp = yp + rm
    
    # create SILKSCREEN-layer + pin1 marker
    y1 = t_slkb
    yp = t_slkp
    for r in range(1, rows + 1):
        if (rows == 1 and r == 1):
            kicad_modg.append(
                RectLine(start=[l_slkb, y1], end=[l_slkb + w_slkb, y1 + rm + 2 * slk_offset], layer='F.SilkS',
                         width=lw_slk))
        if (r == 1 or r == rows):
            kicad_modg.append(RectLine(start=[l_slkb, y1], end=[l_slkb + w_slkb, y1 + rm + slk_offset], layer='F.SilkS',
                                       width=lw_slk))
            y1 = y1 + slk_offset
        else:
            kicad_modg.append(RectLine(start=[l_slkb, y1], end=[l_slkb + w_slkb, y1 + rm], layer='F.SilkS', width=lw_slk))
        
        kicad_modg.append(Line(start=[-1*((cols - 1) * coldist + pad[0] / 2 + slk_offset+lw_slk), yp], end=[l_slkb, yp], layer='F.SilkS',width=lw_slk))
        kicad_modg.append(Line(start=[-1*((cols - 1) * coldist + pad[0] / 2 + slk_offset+lw_slk), yp + pin_width + 2 * slk_offset],end=[l_slkb, yp + pin_width + 2 * slk_offset], layer='F.SilkS', width=lw_slk))
        if cols > 1:
            for c in range(2, cols + 1):
                kicad_modg.append(Line(start=[-1*((c - 2) * coldist + pad[0] / 2 + slk_offset+lw_slk), yp],
                                       end=[-1*((c - 1) * coldist - pad[0] / 2 - slk_offset-lw_slk), yp], layer='F.SilkS',
                                       width=lw_slk))
                kicad_modg.append(
                    Line(start=[-1*((c - 2) * coldist + pad[0] / 2 + slk_offset+lw_slk), yp + pin_width + 2 * slk_offset],
                         end=[-1*((c - 1) * coldist - pad[0] / 2 - slk_offset-lw_slk), yp + pin_width + 2 * slk_offset],
                         layer='F.SilkS', width=lw_slk))
        if r == 1:
            y = y1 + lw_slk
            while y < y1 + rm + 2 * slk_offset:
                kicad_modg.append(Line(start=[l_slkb, y], end=[l_slkb + w_slkb, y], layer='F.SilkS', width=lw_slk))
                y = y + lw_slk
        y1 = y1 + rm
        yp = yp + rm
    
    kicad_modg.append(PolygoneLine(polygone=[[0, -rm/2], [rm/2, -rm/2], [rm/2, 0]], layer='F.SilkS', width=lw_slk))
    
    # create courtyard
    kicad_mod.append(RectLine(start=[roundCrt(l_crt + offset[0]), roundCrt(t_crt + offset[1])],
                              end=[roundCrt(l_crt + offset[0] + w_crt), roundCrt(t_crt + offset[1] + h_crt)],
                              layer='F.CrtYd', width=lw_crt))
    
    # create pads
    p1 = int(1)
    x1 = 0
    y1 = 0
    
    pad_type = Pad.TYPE_THT
    pad_shape1 = Pad.SHAPE_RECT
    pad_shapeother = Pad.SHAPE_OVAL
    pad_layers = '*'

    p = 1
    for r in range(1, rows + 1):
        x1 = 0
        for c in range(1, cols + 1):
            if p == 1:
                kicad_modg.append(Pad(number=p, type=pad_type, shape=pad_shape1, at=[x1, y1], size=pad, drill=ddrill,
                                      layers=[pad_layers + '.Cu', pad_layers + '.Mask']))
            else:
                kicad_modg.append(
                    Pad(number=p, type=pad_type, shape=pad_shapeother, at=[x1, y1], size=pad, drill=ddrill,
                        layers=[pad_layers + '.Cu', pad_layers + '.Mask']))
        
            p = p + 1
            x1 = x1 - coldist
    
        y1 = y1 + rm
    
    # add model
    kicad_modg.append(
        Model(filename=lib_name + ".3dshapes/" + footprint_name + ".wrl", at=offset3d, scale=scale3d, rotate=rotate3d))
    
    # print render tree
    # print(kicad_mod.getRenderTree())
    # print(kicad_mod.getCompleteRenderTree())
    
    # write file
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile(footprint_name + '.kicad_mod')
    
    
    
    
    
    
    
    
    
    
    
    
    


def makePinHeadStraightSMD(rows, cols, rm, coldist, rmx_pad_offset,rmx_pin_length, pin_width, package_width, overlen_top, overlen_bottom, pad,
                        start_left=True, tags_additional=[], lib_name="Pin_Headers", classname="Pin_Header", classname_description="pin header", offset3d=[0, 0, 0], scale3d=[1, 1, 1],
                        rotate3d=[0, 0, 0], isSocket=False):
    ddrill=0.5
    h_fab = (rows - 1) * rm + overlen_top + overlen_bottom
    w_fab = package_width
    l_fab = (coldist * (cols - 1) - w_fab) / 2
    t_fab = -overlen_top
    
    h_slk = h_fab + 2 * slk_offset
    w_slk = max(w_fab + 2 * slk_offset, coldist * (cols - 1) - pad[0] - 4 * slk_offset)
    l_slk = (coldist * (cols - 1) - w_slk) / 2
    t_slk = -overlen_top - slk_offset
    
    w_crt = max(package_width, coldist * (cols - 1)+2*rmx_pad_offset + pad[0]) + 2 * crt_offset
    h_crt = max(h_fab, (rows - 1) * rm + pad[1]) + 2 * crt_offset
    l_crt = coldist * (cols - 1) / 2 - w_crt / 2
    t_crt = (rows - 1) * rm / 2 - h_crt / 2
    
    # if rm == 2.54:
    #    footprint_name = "Pin_Header_Straight_{0}x{1:02}".format(cols, rows)
    # else:
    footprint_name = "{3}_Straight_{0}x{1:02}_Pitch{2:03.2f}mm_SMD".format(cols, rows, rm,classname)
    
    description = "surface-mounted straight {3}, {0}x{1:02}, {2:03.2f}mm pitch".format(cols, rows, rm,classname_description)
    tags = "Surface mounted {3} SMD {0}x{1:02} {2:03.2f}mm".format(cols, rows, rm,classname_description)
    if (cols == 1):
        description = description + ", single row"
        tags = tags + " single row"
        if start_left:
            description = description + ", style 1 (pin 1 left)"
            tags = tags + " style1 pin1 left"
            footprint_name = footprint_name + "_Pin1Left"
        else:
            description = description + ", style 2 (pin 1 right)"
            tags = tags + " style2 pin1 right"
            footprint_name = footprint_name + "_Pin1Right"
    elif (cols == 2):
        description = description + ", double rows"
        tags = tags + " double row"



    if (len(tags_additional) > 0):
        for t in tags_additional:
            footprint_name = footprint_name + "_" + t
            description = description + ", " + t
            tags = tags + " " + t
    
    print(footprint_name)
    
    # init kicad footprint
    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription(description)
    kicad_mod.setTags(tags)
    kicad_mod.setAttribute('smd')
    
    # anchor for SMD-symbols is in the center, for THT-sybols at pin1
    offset = [-(cols-1)*coldist/2, -(rows-1)*rm/2.0]
    
    kicad_modg = Translation(offset[0], offset[1])
    kicad_mod.append(kicad_modg)
    
    # set general values
    kicad_modg.append(
        Text(type='reference', text='REF**', at=[coldist * (cols - 1) / 2, t_slk - txt_offset], layer='F.SilkS'))
    kicad_modg.append(Text(type='value', text=footprint_name, at=[coldist * (cols - 1) / 2, t_slk + h_slk + txt_offset],
                           layer='F.Fab'))

    cleft = range(0, rows, 2)
    cright = range(1, rows, 2)
    if not start_left:
        cleft = range(1, rows, 2)
        cright = range(0, rows, 2)

    # create FAB-layer
    kicad_modg.append(RectLine(start=[l_fab, t_fab], end=[l_fab + w_fab, t_fab + h_fab], layer='F.Fab', width=lw_fab))
    if cols==1:
        for c in cleft:
            kicad_modg.append(RectLine(start=[l_fab, c*rm-pin_width/2], end=[ -rmx_pin_length, c*rm+pin_width/2], layer='F.Fab', width=lw_fab))
        for c in cright:
            kicad_modg.append(RectLine(start=[l_fab+w_fab, c*rm-pin_width/2], end=[rmx_pin_length, c*rm+pin_width/2], layer='F.Fab', width=lw_fab))
    elif cols == 2:
        for c in range(0,rows):
            kicad_modg.append(RectLine(start=[l_fab, c * rm - pin_width / 2], end=[ - rmx_pin_length, c * rm + pin_width/2],layer='F.Fab', width=lw_fab))
            kicad_modg.append(RectLine(start=[l_fab + w_fab, c * rm - pin_width / 2], end=[rm + rmx_pin_length, c * rm + pin_width/2], layer='F.Fab', width=lw_fab))

    # create SILKSCREEN-layer + pin1 marker
    kicad_modg.append(PolygoneLine(polygone=[[l_slk, -(pad[1] / 2 + 2*lw_slk + slk_offset)], [l_slk, t_slk], [l_slk + w_slk, t_slk], [l_slk + w_slk, -(pad[1] / 2 + 2*lw_slk + slk_offset)]], layer='F.SilkS', width=lw_slk))
    kicad_modg.append(PolygoneLine(polygone=[[l_slk, (rows-1)*rm + (pad[1] / 2 + 2*lw_slk + slk_offset)], [l_slk, t_slk + h_slk], [l_slk + w_slk, t_slk + h_slk], [l_slk + w_slk, (rows-1)*rm + (pad[1] / 2 + 2*lw_slk + slk_offset)]], layer='F.SilkS', width=lw_slk))
    if (cols == 1):
        silkh=2*rm-pad[1]-4*lw_slk+2*slk_offset
        for c in cleft:
            kicad_modg.append(Line(start=[l_slk+w_slk, max(t_slk, c * rm - silkh/2)], end=[l_slk+w_slk, min(t_slk+h_slk,c * rm + silkh / 2)], layer='F.SilkS', width=lw_slk))
            if (c+1)==1:
                kicad_modg.append(Line(start=[l_slk , c*rm-pad[1]/2- 2*lw_slk - slk_offset], end=[-rmx_pad_offset-pad[0]/2 , c*rm-pad[1]/2- 2*lw_slk - slk_offset], layer='F.SilkS', width=lw_slk))
        for c in cright:
            kicad_modg.append(Line(start=[l_slk , max(t_slk, c * rm - silkh / 2)],end=[l_slk, min(t_slk+h_slk,c * rm + silkh / 2)], layer='F.SilkS',width=lw_slk))
            if (c + 1) == 1:
                kicad_modg.append(Line(start=[l_slk+w_slk, c * rm - pad[1] / 2 - 2 * lw_slk - slk_offset],
                                       end=[rmx_pad_offset + pad[0] / 2, c * rm - pad[1] / 2 - 2 * lw_slk - slk_offset],
                                       layer='F.SilkS', width=lw_slk))
    if (cols==2):
        if isSocket:
            #print(pad[0]/2+rmx_pad_offset,pad[0]/2,rmx_pad_offset)
            kicad_modg.append(Line(start=[pad[0]/2+rmx_pad_offset+coldist, -(pad[1] / 2 + 2*lw_slk + slk_offset)], end=[l_slk+w_slk, -(pad[1] / 2 + 2*lw_slk + slk_offset)], layer='F.SilkS', width=lw_slk))
        else:
            kicad_modg.append(Line(start=[-pad[0] / 2 - rmx_pad_offset, -(pad[1] / 2 + 2 * lw_slk + slk_offset)],
                                   end=[l_slk, -(pad[1] / 2 + 2 * lw_slk + slk_offset)], layer='F.SilkS', width=lw_slk))
    
    # create courtyard
    kicad_mod.append(RectLine(start=[roundCrt(l_crt + offset[0]), roundCrt(t_crt + offset[1])],
                              end=[roundCrt(l_crt + offset[0] + w_crt), roundCrt(t_crt + offset[1] + h_crt)],
                              layer='F.CrtYd', width=lw_crt))
    
    # create pads
    p1 = int(1)
    x1 = 0
    y1 = 0
    
    pad_type = Pad.TYPE_SMT
    pad_shape1 = Pad.SHAPE_RECT
    pad_layers = 'F'
    
    if cols==1:
        for c in cleft:
            kicad_modg.append(Pad(number=c+1, type=pad_type, shape=pad_shape1, at=[-rmx_pad_offset, c*rm], size=pad, drill=ddrill,layers=[pad_layers + '.Cu', pad_layers + '.Mask']))
        for c in cright:
            kicad_modg.append(Pad(number=c+1, type=pad_type, shape=pad_shape1, at=[rmx_pad_offset, c * rm], size=pad, drill=ddrill,layers=[pad_layers + '.Cu', pad_layers + '.Mask']))
    elif cols==2:
        p = 1
        for c in range(0,rows):
            if isSocket:
                kicad_modg.append(Pad(number=p, type=pad_type, shape=pad_shape1, at=[coldist+rmx_pad_offset, c * rm], size=pad, drill=ddrill,layers=[pad_layers + '.Cu', pad_layers + '.Mask']))
                p=p+1
                kicad_modg.append(Pad(number=p, type=pad_type, shape=pad_shape1, at=[-rmx_pad_offset, c * rm], size=pad, drill=ddrill, layers=[pad_layers + '.Cu', pad_layers + '.Mask']))
                p=p+1
            else:
                kicad_modg.append(Pad(number=p, type=pad_type, shape=pad_shape1, at=[-rmx_pad_offset, c * rm], size=pad, drill=ddrill, layers=[pad_layers + '.Cu', pad_layers + '.Mask']))
                p=p+1
                kicad_modg.append(Pad(number=p, type=pad_type, shape=pad_shape1, at=[coldist+rmx_pad_offset, c * rm], size=pad, drill=ddrill,layers=[pad_layers + '.Cu', pad_layers + '.Mask']))
                p=p+1

    
    # add model
    kicad_modg.append(Model(filename=lib_name + ".3dshapes/" + footprint_name + ".wrl", at=offset3d, scale=scale3d, rotate=rotate3d))
    
    # print render tree
    # print(kicad_mod.getRenderTree())
    # print(kicad_mod.getCompleteRenderTree())
    
    # write file
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile(footprint_name + '.kicad_mod')
