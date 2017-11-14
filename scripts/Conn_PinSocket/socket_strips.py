#!/usr/bin/env python

# KicadModTree is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# KicadModTree is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with kicad-footprint-generator. If not, see < http://www.gnu.org/licenses/ >.
#

#
# based on scripts/tools/footprint_scripts_pin_headers.py
# refactored by Terje Io, <http://github.com/terjeio>
#

import sys
import os

sys.path.append(os.path.join(sys.path[0],"..","..")) # load kicad_mod path

from KicadModTree import Footprint, Translation, Pad, Model, KicadFileHandler
from canvas import Layer, PadLayer

save_dir = "./"
txt_descr = ["", ", single row", ", double rows", ", double rows", ", triple rows", ", quadruple rows"]
txt_tag = ["", " single row", " double row", ", triple rows", " quadruple row"]

def save_to(lib_name):
    out_dir = "" if save_dir == "" or save_dir == None else save_dir + lib_name + ".pretty/"

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    return out_dir

def make_me(series, rows, cols, rm):
#    return series == 0 and rm == 1.27 and rows == 9
#    return series == 2 and rm == 1.27 and (rows == 5 or rows == 8) # and cols == 1
#    return series < 10 and (rows <= 3 or rows == 5 or rows == 8) #and cols == 1
    return True

def makePinHeadStraight(rows, cols, rm, coldist, package_width, overlen_top, overlen_bottom, ddrill, pad,
                        tags_additional=[], lib_name=None, classname=None, classname_description=None, isSocket=False):

    if not make_me(0, rows, cols, rm):
        return

    if lib_name == None or classname == None or classname_description == None:
        return # raise error?

    footprint_name = "{3}_{0}x{1:02}_P{2:03.2f}mm_Vertical".format(cols, rows, rm, classname)
    description = "Through hole straight {3}, {0}x{1:02}, {2:03.2f}mm pitch".format(cols, rows, rm,classname_description)
    tags = "Through hole {3} THT {0}x{1:02} {2:03.2f}mm".format(cols, rows, rm, classname_description)

    tags += txt_tag[cols]
    description += txt_descr[cols]

    if len(tags_additional) > 0:
        for t in tags_additional:
            footprint_name = footprint_name + "_" + t
            description = description + ", " + t
            tags = tags + " " + t

    print "###################"
    print footprint_name, "in", lib_name

    # init kicad footprint
    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription(description)
    kicad_mod.setTags(tags)

    # anchor for THT-symbols at pin1
    kicad_modg = Translation(-coldist if isSocket and cols > 1 else 0.0, 0.0)
    kicad_mod.append(kicad_modg)

    # create layer canvases
    silk = Layer(kicad_modg, 'F.SilkS')
    fab  = Layer(kicad_modg, 'F.Fab')
    crt  = Layer(kicad_modg, 'F.CrtYd', offset=0.5) # offset 0.5 for connectors
    pads = PadLayer(kicad_modg, pad, Pad.TYPE_THT, Pad.SHAPE_OVAL, shape_first=Pad.SHAPE_RECT, drill=ddrill)

    rmh = rm / 2.0
    c_dist = coldist * (cols - 1)

    h_fab = (rows - 1) * rm + overlen_top + overlen_bottom
    w_fab = package_width
#    l_fab = (c_dist - w_fab) / 2.0
    t_fab = -overlen_top

    h_slk = h_fab + silk.offset * 2.0
    w_slk = max(w_fab + silk.offset * 2.0, c_dist - pad[0] - silk.offset * 4.0)
#    l_slk = (c_dist - w_slk) / 2.0
    t_slk = -overlen_top - silk.offset

    w_crt = max(package_width, c_dist + pad[0]) + crt.offset * 2.0
    h_crt = max(h_fab, (rows - 1) * rm + pad[1]) + crt.offset * 2.0
    t_crt = t_fab - crt.offset

    c_ofs = 0.0 if cols == 1 else rmh

    if cols == 1:
        c_dist = coldist

    # add text to silk layer
    silk.goto(c_ofs, t_crt - silk.txt_offset)\
        .text('reference', 'REF**')\
        .setOrigin(-w_slk / 2.0 + c_ofs, t_slk)

    bevel = Layer.getBevel(h_fab, w_fab)
    fab.goto(c_ofs, h_crt + t_crt + fab.txt_offset)\
       .text('value', footprint_name)\
       .goto(c_ofs, h_fab / 2.0 + t_fab)\
       .setTextDefaults(max_size=1.0)\
       .setTextSize(0.6 * (h_fab if rows == 1 and cols <= 2 else w_fab))\
       .text('user', '%R', rotation=0 if rows == 1 and cols <= 2 else 90)\
       .setOrigin(-w_fab / 2.0 + c_ofs, t_fab)\
       .rect(w_fab, h_fab, bevel=(0.0 if isSocket else bevel, bevel if isSocket else 0.0, 0.0, 0.0, 0.0), origin="topLeft")

    # create SILKSCREEN-layer + pin1 marker

    f = -1 if isSocket else 1
    sofs = coldist + silk.offset

    if cols == 1:
        silk.jump(w_slk if isSocket else 0.0, -t_slk + rmh)
        if rows == 1:
            silk.right(f * w_slk)
        else:
            silk.rect(f * w_slk, h_slk - rmh + t_slk, origin="topLeft")
    else:
        if isSocket:
            silk.right(w_slk, draw=False)
        silk.right(f * w_slk / 2.0, draw=False)\
            .right(f * w_slk / 2.0)\
            .down(h_slk)\
            .left(f * w_slk)\
            .up(h_slk + t_slk - sofs / 2.0)\
            .right(f * w_slk / 2.0)\
            .up(-t_slk + sofs / 2.0)

    # add pin1 marker
    silk.goHome()\
        .jump(w_slk if isSocket else 0.0, sofs / 2.0)\
        .up(sofs / 2.0)\
        .right(f * sofs / 2.0)

    # add courtyard
    crt.setOrigin(-w_crt / 2.0 + c_ofs, t_crt)\
       .rect(w_crt, h_crt, origin="topLeft")

    # create pads

    y = 0.0
    for r in range(1, rows + 1):
        x = coldist if isSocket and cols > 1 else 0.0
        for c in range(1, cols + 1):
            pads.add(x, y)
            x = x + (-coldist if isSocket and cols > 1 else coldist)
        y += rm

    # add model
    kicad_modg.append(Model(filename="${KISYS3DMOD}/" + lib_name + ".3dshapes/" + footprint_name + ".wrl"))

    # print render tree
    # print(kicad_mod.getRenderTree())
    # print(kicad_mod.getCompleteRenderTree())

    # write file
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile(save_to(lib_name) + footprint_name + '.kicad_mod')



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
                           tags_additional=[], lib_name=None, classname=None, classname_description=None):

    if not make_me(1, rows, cols, rm):
        return

    if lib_name == None or classname == None or classname_description == None:
        return # raise error?

    footprint_name = "{3}_{0}x{1:02}_P{2:03.2f}mm_Horizontal".format(cols, rows, rm, classname)
    description = "Through hole angled {4}, {0}x{1:02}, {2:03.2f}mm pitch, {3}mm socket length"\
                   .format(cols, rows, rm, pack_width, classname_description)
    tags = "Through hole angled {3} THT {0}x{1:02} {2:03.2f}mm".format(cols, rows, rm, classname_description)

    tags += txt_tag[cols]
    description += txt_descr[cols]

    if len(tags_additional) > 0:
        for t in tags_additional:
            footprint_name = footprint_name + "_" + t
            description = description + ", " + t
            tags = tags + " " + t

    print "###################"
    print footprint_name, "in", lib_name

    # init kicad footprint
    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription(description)
    kicad_mod.setTags(tags)

    # anchor for SMD-symbols is in the center, for THT-sybols at pin1
    kicad_modg = Translation(0, 0)
    kicad_mod.append(kicad_modg)

    # create layer canvases
    silk = Layer(kicad_modg, 'F.SilkS')
    fab  = Layer(kicad_modg, 'F.Fab')
    crt  = Layer(kicad_modg, 'F.CrtYd', offset=0.5) # offset 0.5 for connectors
    pads = PadLayer(kicad_modg, pad, Pad.TYPE_THT, Pad.SHAPE_OVAL, shape_first=Pad.SHAPE_RECT, drill=ddrill)

    rmh = rm / 2.0
    c_dist = coldist * (cols - 1)

    h_fab = (rows - 1) * rm + rm
    w_fab = -pack_width
    l_fab = -(c_dist + pack_offset)
    t_fab = -rmh

    h_slk = h_fab + silk.offset * 2.0
    w_slk = w_fab - silk.offset * 2.0
    l_slk = l_fab + silk.offset
    t_slk = t_fab - silk.offset

    w_crt = -(rmh + c_dist + pack_offset + pack_width + crt.offset * 2.0)
    h_crt = h_fab + crt.offset * 2.0
    l_crt = rmh + crt.offset
    t_crt = -rmh - crt.offset

    # create silk layer and add text
    silk.goto(l_crt + w_crt / 2.0, t_crt - silk.txt_offset)\
        .text('reference', 'REF**')

    # create FAB-layer
    bevel = min(1.0, rm * 0.25 if rows == 1 else -t_fab - pin_width / 2.0)
    fab.goto(l_fab + w_fab / 2.0, (h_fab - rm) / 2.0)\
       .text('user', '%R', rotation=(90 if h_fab >= -w_fab else 0))\
       .rect(-w_fab, h_fab, bevel=(0.0, bevel, 0.0, 0.0))\
       .goto(l_crt + w_crt / 2.0, h_crt + t_crt + fab.txt_offset)\
       .text('value', footprint_name)

    # add pin markers
    fab.goto(l_fab / 2.0, 0.0)
    for r in range(1, rows + 1):
        fab.rect(l_fab, pin_width, draw=(True, False, True, True))\
           .down(rm, False)

    # continue silk layer, set origin and fill pin1 rectangle
    silk.setOrigin(l_fab + w_slk + silk.offset, t_slk)\
        .jump(0.0, -t_slk - rmh)\
        .fillrect(-w_slk, rm)\

    #add pin markers and separation lines
    pw = pin_width + silk.offset * 2.0
    x1 = rm - pad[0] / 2.0 - silk.offset - silk.line_width - l_slk - rm * cols #silly code? offset & line width
    xn = rm - pad[0] - (silk.offset + silk.line_width) * 2.0                   #silly code? offset & line width

    for r in range(1, rows + 1):
        silk.right(-w_slk, r != 1)\
            .down((rm - pw) / 2.0, False)\
            .right(x1)\
            .down(pw, False)\
            .left(x1)
        for s in range(1, cols):
            xo = rm * s + x1
            silk.jump(xo, -pw)\
                .left(xn)\
                .down(pw, False)\
                .right(xn)\
                .left(xo, False)
        silk.jump(w_slk, (rm - pw) / 2.0)

    # add outline
    silk.goHome()\
        .rect(-w_slk, h_slk, origin='topLeft')

    # pin1 marker
    silk.goto(0.0, -rmh)\
        .right(rmh)\
        .down(rmh)

    # create courtyard
    crt.setOrigin(l_crt + w_crt / 2.0, t_crt + h_crt / 2.0)\
       .rect(w_crt, h_crt)

    # create pads

    y = 0.0
    for r in range(1, rows + 1):
        x = 0.0
        for c in range(1, cols + 1):
            pads.add(x, y)
            x -= coldist
        y += rm

    # add model
    kicad_modg.append(Model(filename="${KISYS3DMOD}/" + lib_name + ".3dshapes/" + footprint_name + ".wrl"))

    # print render tree
    # print(kicad_mod.getRenderTree())
    # print(kicad_mod.getCompleteRenderTree())

    # write file
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile(save_to(lib_name) + footprint_name + '.kicad_mod')



def makePinHeadStraightSMD(rows, cols, rm, coldist, rmx_pad_offset, rmx_pin_length, pin_width, package_width, overlen_top, overlen_bottom, pad,
                            start_left=True, tags_additional=[], lib_name=None, classname=None, classname_description=None, isSocket=False):

    if not make_me(2, rows, cols, rm):
        return

    if lib_name == None or classname == None or classname_description == None:
        return # raise error?

    footprint_name = "{3}_{0}x{1:02}_P{2:03.2f}mm_Vertical_SMD".format(cols, rows, rm, classname)
    description = "surface-mounted straight {3}, {0}x{1:02}, {2:03.2f}mm pitch".format(cols, rows, rm, classname_description)
    tags = "Surface mounted {3} SMD {0}x{1:02} {2:03.2f}mm".format(cols, rows, rm, classname_description)

    tags += txt_tag[cols]
    description += txt_descr[cols]

    if (cols == 1):
        if start_left:
            description += ", style 1 (pin 1 left)"
            tags += " style1 pin1 left"
            footprint_name += "_Pin1Left"
        else:
            description += ", style 2 (pin 1 right)"
            tags += " style2 pin1 right"
            footprint_name += "_Pin1Right"

    if len(tags_additional) > 0:
        for t in tags_additional:
            footprint_name = footprint_name + "_" + t
            description = description + ", " + t
            tags = tags + " " + t

    print "###################"
    print footprint_name, "in", lib_name

    # init kicad footprint
    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription(description)
    kicad_mod.setTags(tags)
    kicad_mod.setAttribute('smd')

    # anchor for SMD-symbols is in the center
    kicad_modg = Translation(0.0, 0.0)
    kicad_mod.append(kicad_modg)

    rmh = rm / 2.0

    # create layer canvases
    silk = Layer(kicad_modg, 'F.SilkS')
    fab  = Layer(kicad_modg, 'F.Fab')
    crt  = Layer(kicad_modg, 'F.CrtYd', offset=0.5) # offset 0.5 for connectors
    pads = PadLayer(kicad_modg, pad, Pad.TYPE_SMT, Pad.SHAPE_RECT, y_offset=(rows - 1) * -rmh)

    c_dist = coldist * (cols - 1)

    h_fab = (rows - 1) * rm + overlen_top + overlen_bottom
    w_fab = package_width
    t_fab = -overlen_top

    h_slk = h_fab + silk.offset * 2.0
    w_slk = max(w_fab + silk.offset * 2.0, c_dist - pad[0] - silk.offset * 4.0)
    l_slk = (c_dist - w_slk) / 2.0
    t_slk = -overlen_top - silk.offset

    h_crt = max(h_fab, (rows - 1) * rm + pad[1]) + crt.offset * 2.0
    w_crt = max(package_width, rmx_pad_offset * 2.0 + pad[0]) + crt.offset * 2.0

    cleft = range(0, rows, 2) if start_left else range(1, rows, 2)
    cright = range(1, rows, 2) if start_left else range(0, rows, 2)
    even_pins = rows % 2.0 == 0.0

    # add text to silk layer
    silk.goto(0.0, -(h_crt / 2.0) - silk.txt_offset)\
        .text('reference', 'REF**')\
        .setOrigin(-w_slk / 2.0, -h_slk / 2.0)

    # add text and outline to fab layer
    bevel = min(1.0, rm * 0.25 if rows == 1 else (-t_fab - pin_width / 2.0))
     
    fab.down((h_crt) / 2.0 + fab.txt_offset, draw=False)\
       .text('value', footprint_name)\
       .goHome()\
       .setTextDefaults(max_size=1.0)\
       .setTextSize(0.6 * (h_fab if rows == 1 and cols <= 2 else w_fab))\
       .text('user', '%R', rotation=(90 if h_fab >= w_fab else 0))\
       .rect(w_fab, h_fab, bevel=(bevel if start_left else 0.0, 0.0 if start_left else bevel, 0.0, 0.0, 0.0))\
       .setOrigin(-w_fab / 2.0, -h_fab / 2.0)

    # add pin markers to fab layer
    trl = w_fab + rmx_pin_length
    if cols == 2:
        fab.jump(-rmx_pin_length / 2.0, -t_fab)
        for r in range(1, rows + 1):
            fab.rect(rmx_pin_length, pin_width, draw=(True, False, True, True))\
               .right(trl, draw=False)\
               .rect(rmx_pin_length, pin_width, draw=(True, True, True, False))\
               .left(trl, draw=False)\
               .down(rm, draw=False)
    elif start_left:
        fab.jump(-rmx_pin_length / 2.0, -t_fab)
        for c in cleft:
            fab.rect(rmx_pin_length, pin_width, draw=(True, False, True, True))\
               .jump(trl, rm)
            if even_pins or c != cleft[-1]:
                fab.rect(rmx_pin_length, pin_width, draw=(True, True, True, False))\
                   .jump(-trl, rm)
    else:
        trl = -trl
        fab.jump(w_fab + rmx_pin_length / 2.0, -t_fab)
        for c in cright:
            fab.rect(rmx_pin_length, pin_width, draw=(True, True, True, False))\
               .jump(trl, rm)
            if even_pins or c != cright[-1]:
                fab.rect(rmx_pin_length, pin_width, draw=(True, False, True, True))\
                   .jump(-trl, rm)

    # continue with silkscreen
    slk_offset_pad = silk.getPadOffsetV(pad)
    p1len = silk.getPadOffsetH(pad, rmx_pad_offset) + (l_slk if cols == 1 else - rmh + l_slk )
    tvl = -(t_slk + slk_offset_pad)
    slk_offset_pad *= 2.0

    # top, pin1 marker and bottom silk
    silk.jump(-p1len, tvl)\
        .right(p1len, draw=not start_left ^ isSocket)\
        .up(tvl, draw=cols > 1 or start_left)\
        .right(w_slk)\
        .down(tvl, draw=cols > 1 or not start_left)\
        .right(p1len, draw=start_left ^ isSocket)\
        .jump(-p1len, h_slk - tvl * 2.0)\
        .down(tvl, draw=cols > 1 or not start_left ^ even_pins)\
        .left(w_slk)\
        .up(tvl, draw=cols > 1 or start_left ^ even_pins)

    silk.goHome()
    pl = rm - slk_offset_pad
    if cols == 2:
        if slk_offset_pad < rm - silk.line_width * 2.0:
            silk.down(-t_slk + (rm - pl) / 2.0, draw=False)
            for c in range(0, rows - 1):
                silk.down(pl)\
                    .right(w_slk, draw=False)\
                    .up(pl)\
                    .jump(-w_slk, rm)
    else:
        pl += rm
        sofs = (-t_slk * 2.0 - pl) / 2.0
        silk.jump(0.0, tvl + slk_offset_pad if start_left else 0.0)
        if rows < 3:
            silk.down(pl + sofs)\
                .goHome()\
                .jump(w_slk, 0.0 if start_left else tvl + slk_offset_pad)\
                .down(pl + sofs)
        else:
            sl = []
            if not start_left:
                sl.append(cright[0])
            if not start_left ^ even_pins:
                sl.append(cright[-1])
            for c in cright:
                silk.down(pl + sofs if c in sl else pl)\
                    .down(slk_offset_pad, draw=False)

            silk.goHome()\
                .jump(w_slk, 0.0 if start_left else tvl + slk_offset_pad)
            sl = []
            if start_left:
                sl.append(cleft[0])
            if start_left ^ even_pins:
                sl.append(cleft[-1])
            for c in cleft:
                silk.down(pl + sofs if c in sl else pl)\
                    .jump(0.0, slk_offset_pad)

    # add courtyard
    crt.rect(w_crt, h_crt)

    # create pads
    if cols == 1:
        for y in cleft:
            pads.add(-rmx_pad_offset, y * rm, number=y + 1)
        for y in cright:
            pads.add(rmx_pad_offset, y * rm, number=y + 1)
    elif cols == 2:
        f = 1.0 if isSocket else -1.0
        for y in range(0,rows):
            pads.add(f * rmx_pad_offset, y * rm)\
                .add(f * -rmx_pad_offset, y * rm)

    # add model
    kicad_modg.append(Model(filename="${KISYS3DMOD}/" + lib_name + ".3dshapes/" + footprint_name + ".wrl"))

    # print render tree
    # print(kicad_mod.getRenderTree())
    # print(kicad_mod.getCompleteRenderTree())

    # write file
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile(save_to(lib_name) + footprint_name + '.kicad_mod')
