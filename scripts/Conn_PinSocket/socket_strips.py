#!/usr/bin/env python

#
# Parts script module for socket strip footprints for KicCad
#
# This script is built on top of the kicad-footprint-generator framework
# by Thomas Pointhuber, https://github.com/pointhi/kicad-footprint-generator
#
# This module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with kicad-footprint-generator. If not, see < http://www.gnu.org/licenses/ >.

#
# based on scripts/tools/footprint_scripts_pin_headers.py
# refactored by and (C) 2017 Terje Io, <http://github.com/terjeio>
#

# 2017-11-25

import sys
import os

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../..")

from KicadModTree import Footprint, Translation, Pad, Model, KicadFileHandler
from canvas import Layer, PadLayer, Keepout, OutDir
from cq_base_parameters import PinStyle, CaseType

txt_descr = ["", ", single row", ", double cols", ", double cols", ", triple cols", ", quadruple cols"]
txt_tag = ["", " single row", " double row", ", triple cols", " quadruple row"]

root_dir = OutDir("./")

#Keepout.DEBUG = 1

def getPadOffsets(overall_width, pad):
    return round((overall_width - pad[0]) / 2.0, 3)

def getPinLength(overall_width, packwidth):
    return round((overall_width - packwidth) / 2.0, 3)

class pinSocketVerticalTHT (object):
    def __init__(self, params):
        self.make_me = params.type == CaseType.THT and params.pin_style == PinStyle.STRAIGHT and params.pad_width > 0
        self.params = params

    def makeModelName(self, genericName):
        return "PinSocket_{0}x{1:02}_P{2:03.2f}mm_Vertical".format(self.params.num_pin_rows, self.params.num_pins, self.params.pin_pitch)

    def make(self, tags_additional=[], isSocket=True):

        param = self.params

        lib_name ="Conn_PinSocket_{0:03.2f}mm".format(param.pin_pitch)
        footprint_name = self.makeModelName("")
        description = "Through hole straight socket strip, {0}x{1:02}, {2:03.2f}mm pitch".format(param.num_pin_rows, param.num_pins, param.pin_pitch)
        tags = "Through hole socket strip THT {0}x{1:02} {2:03.2f}mm".format(param.num_pin_rows, param.num_pins, param.pin_pitch)

        tags += txt_tag[param.num_pin_rows]
        description += txt_descr[param.num_pin_rows]

        pad = [param.pad_length, param.pad_width]
        rowdist = param.pin_pitch

        if len(tags_additional) > 0:
            for t in tags_additional:
                footprint_name = footprint_name + "_" + t
                description = description + ", " + t
                tags = tags + " " + t

        if len(param.datasheet) > 0:
            description += " (" + param.datasheet + ")"

        description += ", script generated"

        print "###################"
        print footprint_name, "in", lib_name

        # init kicad footprint
        kicad_mod = Footprint(footprint_name)
        kicad_mod.setDescription(description)
        kicad_mod.setTags(tags)

        if Keepout.DEBUG:
            kicad_modg = Translation(0.0, 0.0)
        else:
            kicad_modg = Translation(-rowdist if isSocket and param.num_pin_rows > 1 else -param.pins_offset, 0.0)
        kicad_mod.append(kicad_modg)

        # create layer canvases
        silk    = Layer(kicad_modg, 'F.SilkS')
        fab     = Layer(kicad_modg, 'F.Fab')
        crt     = Layer(kicad_modg, 'F.CrtYd', offset=0.5) # offset 0.5 for connectors
        pads    = PadLayer(kicad_modg, pad, Pad.TYPE_THT, Pad.SHAPE_OVAL, shape_first=Pad.SHAPE_RECT, drill=param.pin_drill, x_offset=param.pins_offset)
        keepout = Keepout(silk)

        if Keepout.DEBUG:
            kicad_mod.setSolderMaskMargin(silk.getSoldermaskMargin())

        rmh = param.pin_pitch / 2.0
        r_dist = rowdist * (param.num_pin_rows - 1)

        h_fab = param.num_pins * param.pin_pitch + param.body_overlength
        w_fab = param.body_width
        t_fab = -rmh - param.body_overlength / 2.0

        h_slk = h_fab + silk.offset * 2.0
        w_slk = max(w_fab + silk.offset * 2.0, r_dist - pad[0] - silk.offset * 4.0)
        t_slk = t_fab - silk.offset

        w_crt = max(param.body_width, r_dist + pad[0]) + crt.offset * 2.0
        h_crt = max(h_fab, (param.num_pins - 1) * param.pin_pitch + pad[1]) + crt.offset * 2.0
        t_crt = t_fab - crt.offset

        c_ofs = 0.0 if param.num_pin_rows == 1 else rmh

        if param.num_pin_rows == 1:
            r_dist = rowdist

        # create pads

        y = 0.0
        for r in range(1, param.num_pins + 1):
            x = rowdist if isSocket and param.num_pin_rows > 1 else 0.0
            for c in range(1, param.num_pin_rows + 1):
                pads.add(x, y)
                x = x + (-rowdist if isSocket and param.num_pin_rows > 1 else rowdist)
            y += param.pin_pitch

        # add pads to silk keepout
        keepout.addPads()
        keepout.debug_draw()

        # add text to silk layer
        silk.goto(c_ofs, t_crt - silk.txt_offset)\
            .text('reference', 'REF**')\
            .setOrigin(-w_slk / 2.0 + c_ofs, t_slk)

        # add fab layer
        bevel = Layer.getBevel(h_fab, w_fab)
        fab.goto(c_ofs, h_crt + t_crt + fab.txt_offset)\
           .text('value', footprint_name)\
           .goto(c_ofs, h_fab / 2.0 + t_fab)\
           .setTextDefaults(max_size=1.0)\
           .setTextSize(0.6 * (h_fab if param.num_pins == 1 and param.num_pin_rows <= 2 else w_fab))\
           .text('user', '%R', rotation=0 if param.num_pins == 1 and param.num_pin_rows <= 2 else 90)\
           .setOrigin(-w_fab / 2.0 + c_ofs, t_fab)\
           .rect(w_fab, h_fab, bevel=(0.0 if isSocket else bevel, bevel if isSocket else 0.0, 0.0, 0.0), origin="topLeft")

        # continue with silkscreen

        pin1 = keepout.getPadBB(1)

    #    if isSocket and param.pins_offset > 0.0: # for 1.00 mm sockets
    #        w_slk = w_slk / 2.0 + (pin1.width / 2.0 + pin1.x)

        f = -1 if isSocket else 1

        if param.num_pin_rows == 1:
            silk.jump(w_slk if isSocket else 0.0, -t_slk + rmh)
            if param.num_pins == 1:
                silk.down(silk.offset, draw=False)\
                    .right(f * w_slk)\
                    .up(silk.line_width)\
                    .jump(-f * w_slk, silk.line_width)\
                    .up(silk.line_width)
            else:
                silk.rect(f * w_slk, h_slk - rmh + t_slk, origin="topLeft")
        else:
            if isSocket:
                silk.right(w_slk, draw=False)
            silk.right(f * w_slk / 2.0, draw=False)\
                .right(f * w_slk / 2.0)\
                .down(h_slk)\
                .left(f * w_slk)\
                .up(h_slk + t_slk - rowdist / 2.0)\
                .right(f * w_slk / 2.0)\
                .up(-t_slk + rowdist / 2.0)

        # add pin1 marker
        silk.goto(max(pin1.x - f * pin1.width / 2.0, w_slk / 2.0 + c_ofs), pin1.y)\
            .up(max(-t_slk, pin1.height / 2.0))\
            .right(f * (silk.x - pin1.x))

        # add courtyard
        crt.setOrigin(-w_crt / 2.0 + c_ofs, t_crt)\
           .rect(w_crt, h_crt, origin="topLeft")

        # add model
        kicad_modg.append(Model(filename="${KISYS3DMOD}/" + lib_name + ".3dshapes/" + footprint_name + ".wrl"))

        # write file
        file_handler = KicadFileHandler(kicad_mod)
        file_handler.writeFile(root_dir.saveTo(lib_name) + footprint_name + '.kicad_mod')



#
#                                                          <-->pack_offset
#                 <--------------pack_width--------------->
#                                                             <-rowdist>
#                 +---------------------------------------+            ---+
#                 |                                       |  OOO      OOO |          ^
#                 |                                       |  OOO ==== OOO |  ^       pin_width
#                 |                                       |  OOO      OOO    |       v
#                 +---------------------------------------+                  pin_pitch
#                 |                                       |  OOO      OOO    |
#                 |                                       |  OOO ==== OOO    v
#                 |                                       |  OOO      OOO
#                 +---------------------------------------+
#
class pinSocketHorizontalTHT (object):
    def __init__(self, params):
        self.make_me =  params.type == CaseType.THT and params.pin_style == PinStyle.ANGLED and params.pad_width > 0
        self.params = params

    def makeModelName(self, genericName):
        return "PinSocket_{0}x{1:02}_P{2:03.2f}mm_Horizontal".format(self.params.num_pin_rows, self.params.num_pins, self.params.pin_pitch)

    def make(self, tags_additional=[], isSocket=True):

        param = self.params

        lib_name ="Conn_PinSocket_{0:03.2f}mm".format(param.pin_pitch)
        footprint_name = self.makeModelName("")
        description = "Through hole angled socket strip, {0}x{1:02}, {2:03.2f}mm pitch, {3}mm socket length"\
                       .format(param.num_pin_rows, param.num_pins, param.pin_pitch, param.body_width)
        tags = "Through hole angled socket strip THT {0}x{1:02} {2:03.2f}mm".format(param.num_pin_rows, param.num_pins, param.pin_pitch)

        tags += txt_tag[param.num_pin_rows]
        description += txt_descr[param.num_pin_rows]

        pad = [param.pad_length, param.pad_width]
        rowdist = param.pin_pitch

        if len(tags_additional) > 0:
            for t in tags_additional:
                footprint_name = footprint_name + "_" + t
                description = description + ", " + t
                tags = tags + " " + t

        if len(param.datasheet) > 0:
            description += " (" + param.datasheet + ")"

        description += ", script generated"

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
        silk    = Layer(kicad_modg, 'F.SilkS')
        fab     = Layer(kicad_modg, 'F.Fab')
        crt     = Layer(kicad_modg, 'F.CrtYd', offset=0.5) # offset 0.5 for connectors
        pads    = PadLayer(kicad_modg, pad, Pad.TYPE_THT, Pad.SHAPE_OVAL, shape_first=Pad.SHAPE_RECT, drill=param.pin_drill)
        keepout = Keepout(silk)

        if Keepout.DEBUG:
            kicad_mod.setSolderMaskMargin(silk.getSoldermaskMargin())

        rmh = param.pin_pitch / 2.0
        r_dist = rowdist * (param.num_pin_rows - 1)

        h_fab = (param.num_pins - 1) * param.pin_pitch + param.pin_pitch
        w_fab = -param.body_width
        l_fab = -(r_dist + param.body_offset)
        t_fab = -rmh

        h_slk = h_fab + silk.offset * 2.0
        w_slk = w_fab - silk.offset * 2.0
        l_slk = l_fab + silk.offset
        t_slk = t_fab - silk.offset

        w_crt = -(rmh + r_dist + param.body_offset + param.body_width + crt.offset * 2.0)
        h_crt = h_fab + crt.offset * 2.0
        l_crt = rmh + crt.offset
        t_crt = -rmh - crt.offset

        # create pads
        y = 0.0
        for r in range(1, param.num_pins + 1):
            x = 0.0
            for c in range(1, param.num_pin_rows + 1):
                pads.add(x, y)
                x -= rowdist
            y += param.pin_pitch

        # add pads to silk keepout
        keepout.addPads()
        keepout.debug_draw()

        # add text to silk
        silk.goto(l_crt + w_crt / 2.0, t_crt - silk.txt_offset)\
            .text('reference', 'REF**')

        # create FAB-layer
        bevel = min(Layer.getBevel(h_fab, abs(w_fab)), -t_fab - param.pin_width / 2.0)

        fab.goto(l_fab + w_fab / 2.0, (h_fab - param.pin_pitch) / 2.0)\
           .text('user', '%R', rotation=(90 if h_fab >= -w_fab else 0))\
           .rect(-w_fab, h_fab, bevel=(0.0, bevel, 0.0, 0.0))\
           .goto(l_crt + w_crt / 2.0, h_crt + t_crt + fab.txt_offset)\
           .text('value', footprint_name)

        # add pin markers
        fab.goto(l_fab / 2.0, 0.0)
        for r in range(1, param.num_pins + 1):
            fab.rect(l_fab, param.pin_width, draw=(True, False, True, True))\
               .down(param.pin_pitch, False)

        # continue silk layer, set origin and fill pin1 rectangle
        silk.setOrigin(l_fab + w_slk + silk.offset, t_slk)\
            .jump(0.0, -t_slk - rmh)\
            .fillrect(-w_slk, param.pin_pitch + silk.offset + (silk.offset if param.num_pins == 1 else 0.0))\

        pw = param.pin_width + silk.offset * 2.0

        # add pin markers
        silk.goto(l_slk / 2.0, 0.0)
        for r in range(1, param.num_pins + 1):
            silk.rect(l_slk, pw, draw=(True, False, True, False))\
               .down(param.pin_pitch, False)

        #add separation lines
        silk.goHome()\
            .jump(0.0, silk.line_width / 2.0)
        for r in range(1, param.num_pins + 1):
            silk.right(-w_slk, r != 1)\
                .jump(w_slk, param.pin_pitch)

        # add outline
        silk.goHome()\
            .rect(-w_slk, h_slk, origin='topLeft')

        pin1 = keepout.getPadBB(1)

        # add pin1 marker
        silk.goto(pin1.x + pin1.width / 2.0, pin1.y)\
            .up(max(-t_slk, pin1.height / 2.0))\
            .left(silk.x - pin1.x)

        # create courtyard
        crt.setOrigin(l_crt + w_crt / 2.0, t_crt + h_crt / 2.0)\
           .rect(w_crt, h_crt)

        # add model
        kicad_modg.append(Model(filename="${KISYS3DMOD}/" + lib_name + ".3dshapes/" + footprint_name + ".wrl"))

        # write file
        file_handler = KicadFileHandler(kicad_mod)
        file_handler.writeFile(root_dir.saveTo(lib_name) + footprint_name + '.kicad_mod')



class pinSocketVerticalSMD (object):
    def __init__(self, params):
        self.make_me = params.type == 'SMD' and params.pad_width > 0
        self.params = params

    def makeModelName(self, genericName):
        genericName = "PinSocket_{0}x{1:02}_P{2:03.2f}mm_Vertical_SMD".format(self.params.num_pin_rows, self.params.num_pins, self.params.pin_pitch)
        return genericName + (("_Pin1Right" if self.params.pin1start_right else "_Pin1Left") if self.params.num_pin_rows == 1 else "" )

    def make(self, tags_additional=[], isSocket=True):

        param = self.params

        lib_name ="Conn_PinSocket_{0:03.2f}mm".format(param.pin_pitch)
        footprint_name = self.makeModelName("")
        description = "surface-mounted straight socket strip, {0}x{1:02}, {2:03.2f}mm pitch".format(param.num_pin_rows, param.num_pins, param.pin_pitch)
        tags = "Surface mounted socket strip SMD {0}x{1:02} {2:03.2f}mm".format(param.num_pin_rows, param.num_pins, param.pin_pitch)

        tags += txt_tag[param.num_pin_rows]
        description += txt_descr[param.num_pin_rows]

        pad = [param.pad_length, param.pad_width]
        rowdist = param.pin_pitch

        rmx_pad_offset = getPadOffsets(param.pads_lp_width, pad)
        rmx_pin_length = getPinLength(param.pin_length, param.body_width)

        if (param.num_pin_rows == 1):
            if param.pin1start_right:
                description += ", style 2 (pin 1 right)"
                tags += " style2 pin1 right"
            else:
                description += ", style 1 (pin 1 left)"
                tags += " style1 pin1 left"

        if len(tags_additional) > 0:
            for t in tags_additional:
                footprint_name = footprint_name + "_" + t
                description = description + ", " + t
                tags = tags + " " + t

        if len(param.datasheet) > 0:
            description += " (" + param.datasheet + ")"

        description += ", script generated"

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

        rmh = param.pin_pitch / 2.0

        # create layer canvases
        silk    = Layer(kicad_modg, 'F.SilkS')
        fab     = Layer(kicad_modg, 'F.Fab')
        crt     = Layer(kicad_modg, 'F.CrtYd', offset=0.5) # offset 0.5 for connectors
        pads    = PadLayer(kicad_modg, pad, Pad.TYPE_SMT, Pad.SHAPE_RECT, y_offset=(param.num_pins - 1) * -rmh)
        keepout = Keepout(silk)

        if Keepout.DEBUG:
            kicad_mod.setSolderMaskMargin(silk.getSoldermaskMargin())

        r_dist = rowdist * (param.num_pin_rows - 1)

        h_fab = param.num_pins * param.pin_pitch + param.body_overlength
        w_fab = param.body_width
        t_fab = -param.body_overlength / 2.0

        h_slk = h_fab + silk.offset * 2.0
        w_slk = max(w_fab + silk.offset * 2.0, r_dist - pad[0] - silk.offset * 4.0)
    #    l_slk = (r_dist - w_slk) / 2.0
    #    t_slk = -param.body_overlength - silk.offset

        h_crt = max(h_fab, (param.num_pins - 1) * param.pin_pitch + pad[1]) + crt.offset * 2.0
        w_crt = max(param.body_width, rmx_pad_offset * 2.0 + pad[0]) + crt.offset * 2.0

        cleft = range(1, param.num_pins, 2) if param.pin1start_right else range(0, param.num_pins, 2)
        cright = range(0, param.num_pins, 2) if param.pin1start_right else range(1, param.num_pins, 2)
        even_pins = param.num_pins % 2.0 == 0.0

        # create pads
        if param.num_pin_rows == 1:
            for y in cleft:
                pads.add(-rmx_pad_offset, y * param.pin_pitch, number=y + 1)
            for y in cright:
                pads.add(rmx_pad_offset, y * param.pin_pitch, number=y + 1)
        elif param.num_pin_rows == 2:
            f = 1.0 if isSocket else -1.0
            for y in range(0,param.num_pins):
                pads.add(f * rmx_pad_offset, y * param.pin_pitch)\
                    .add(f * -rmx_pad_offset, y * param.pin_pitch)

        # add pads to silk keepout
        keepout.addPads()
        keepout.debug_draw()

        # add text and outline to silk layer
        silk.goto(0.0, -(h_crt / 2.0) - silk.txt_offset)\
            .text('reference', 'REF**')\
            .setOrigin(-w_slk / 2.0, -h_slk / 2.0)\
            .rect(w_slk, h_slk, origin = "topLeft")

        # pin1 marker
        pad1 = keepout.getPadBB(1)
        f = 1 if isSocket ^ (not param.pin1start_right) else -1

        silk.gotoY(pad1.y)\
            .jump(w_slk if f == 1 else 0.0, -pad1.height / 2.0)\
            .right(f * (pad[0] - silk.line_width) / 2.0 - (silk.x - pad1.x))

        # add text and outline to fab layer
        bevel = min(Layer.getBevel(h_fab, w_fab), -t_fab + rmh + param.pin_width / 2.0)

        fab.down((h_crt) / 2.0 + fab.txt_offset, draw=False)\
           .text('value', footprint_name)\
           .goHome()\
           .setTextDefaults(max_size=1.0)\
           .setTextSize(0.6 * (h_fab if param.num_pins == 1 and param.num_pin_rows <= 2 else w_fab))\
           .text('user', '%R', rotation=(90 if h_fab >= w_fab else 0))\
           .rect(w_fab, h_fab, bevel=(0.0 if param.pin1start_right else bevel, bevel if param.pin1start_right else 0.0, 0.0, 0.0))\
           .setOrigin(-w_fab / 2.0, -h_fab / 2.0)

        # add pin markers to fab layer
        trl = w_fab + rmx_pin_length
        if param.num_pin_rows == 2:
            fab.jump(-rmx_pin_length / 2.0, -t_fab + rmh)
            for r in range(1, param.num_pins + 1):
                fab.rect(rmx_pin_length, param.pin_width, draw=(True, False, True, True))\
                   .right(trl, draw=False)\
                   .rect(rmx_pin_length, param.pin_width, draw=(True, True, True, False))\
                   .left(trl, draw=False)\
                   .down(param.pin_pitch, draw=False)
        elif param.pin1start_right:
            trl = -trl
            fab.jump(w_fab + rmx_pin_length / 2.0, -t_fab + rmh)
            for c in cright:
                fab.rect(rmx_pin_length, param.pin_width, draw=(True, True, True, False))\
                   .jump(trl, param.pin_pitch)
                if even_pins or c != cright[-1]:
                    fab.rect(rmx_pin_length, param.pin_width, draw=(True, False, True, True))\
                       .jump(-trl, param.pin_pitch)
        else:
            fab.jump(-rmx_pin_length / 2.0, -t_fab + rmh)
            for c in cleft:
                fab.rect(rmx_pin_length, param.pin_width, draw=(True, False, True, True))\
                   .jump(trl, param.pin_pitch)
                if even_pins or c != cleft[-1]:
                    fab.rect(rmx_pin_length, param.pin_width, draw=(True, True, True, False))\
                       .jump(-trl, param.pin_pitch)

        # add courtyard
        crt.rect(w_crt, h_crt)

        # add model
        kicad_modg.append(Model(filename="${KISYS3DMOD}/" + lib_name + ".3dshapes/" + footprint_name + ".wrl"))

        # write file
        file_handler = KicadFileHandler(kicad_mod)
        file_handler.writeFile(root_dir.saveTo(lib_name) + footprint_name + '.kicad_mod')

### EOF ###
