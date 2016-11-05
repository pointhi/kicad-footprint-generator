#!/usr/bin/env python

import sys
import os
import math
import time

# ensure that the kicad-footprint-generator directory is available
#sys.path.append(os.environ.get('KIFOOTPRINTGENERATOR'))  # enable package import from parent directory
#sys.path.append("D:\hardware\KiCAD\kicad-footprint-generator")  # enable package import from parent directory
sys.path.append(os.path.join(sys.path[0],"..","..","kicad_mod")) # load kicad_mod path
sys.path.append(os.path.join(sys.path[0],"..","..")) # load kicad_mod path

from KicadModTree import *  # NOQA
from tools import *
from TO_THT_packages import *


# vertical symbols for rectangular transistors
def makeVERT(lib_name, pck, has3d=False, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], lptext="_LargePads"):
    l_fabp = -pck.pin_offset_x
    t_fabp = -pck.pin_offset_z
    w_fabp = pck.plastic[0]
    h_fabp = pck.plastic[2]
    
    w_fabm = pck.metal[0]
    h_fabm = pck.metal[2]
    
    l_slkp = l_fabp - slk_offset
    t_slkp = t_fabp - slk_offset
    w_slkp = w_fabp + 2 * slk_offset
    h_slkp = h_fabp + 2 * slk_offset
    w_slkm = w_fabm + 2 * slk_offset
    h_slkm = h_fabm + 2 * slk_offset
    
    l_crt = min(-pck.pad[0] / 2, l_slkp) - crt_offset
    t_crt = min(-pck.pad[1] / 2, t_slkp) - crt_offset
    w_crt = max(max(w_slkp, w_slkm), (pck.pins - 1) * pck.rm + pck.pad[0]) + 2 * crt_offset
    h_crt = max(max(h_slkp, h_slkm), -t_crt + pck.pad[1] / 2) + 2 * crt_offset
    
    l_mounth = l_fabp + pck.mounting_hole_pos[0]
    
    txt_x = l_slkp + max(w_slkp, w_slkm) / 2
    
    tag_items = ["Vertical", "RM {0}mm".format(pck.rm)]
    
    footprint_name = pck.name
    footprint_name = footprint_name + "_Vertical"
    for t in pck.fpnametags:
        footprint_name = footprint_name + "_" + t
    if pck.largepads:
        tag_items.append("large Pads")
        footprint_name = footprint_name + lptext
    
    print(footprint_name)
    
    description = pck.name
    tags = pck.name
    for t in tag_items:
        description = description + ", " + t
        tags = tags + " " + t
    for t in pck.tags:
        description = description + ", " + t
        tags = tags + " " + t
    
    # init kicad footprint
    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription(description)
    kicad_mod.setTags(tags)
    
    # set general values
    kicad_mod.append(Text(type='reference', text='REF**', at=[txt_x, t_slkp - txt_offset], layer='F.SilkS'))
    kicad_mod.append(
        Text(type='value', text=footprint_name, at=[txt_x, t_slkp + max(h_slkm, h_slkp) + txt_offset], layer='F.Fab'))
    
    # create FAB-layer
    kicad_mod.append(
        RectLine(start=[l_fabp, t_fabp], end=[l_fabp + w_fabp, t_fabp + h_fabp], layer='F.Fab', width=lw_fab))
    if (pck.metal[2] > 0):
        kicad_mod.append(
            Line(start=[l_fabp, t_fabp + h_fabm], end=[l_fabp + w_fabp, t_fabp + h_fabm], layer='F.Fab', width=lw_fab))
        if pck.mounting_hole_diameter > 0:
            kicad_mod.append(Line(start=[l_mounth - pck.mounting_hole_diameter / 2, t_fabp],
                                  end=[l_mounth - pck.mounting_hole_diameter / 2, t_fabp + h_fabm], layer='F.Fab',
                                  width=lw_fab))
            kicad_mod.append(Line(start=[l_mounth + pck.mounting_hole_diameter / 2, t_fabp],
                                  end=[l_mounth + pck.mounting_hole_diameter / 2, t_fabp + h_fabm], layer='F.Fab',
                                  width=lw_fab))
    else:
        if pck.mounting_hole_diameter > 0:
            kicad_mod.append(Line(start=[l_mounth - pck.mounting_hole_diameter / 2, t_fabp],
                                  end=[l_mounth - pck.mounting_hole_diameter / 2, t_fabp + h_fabp], layer='F.Fab',
                                  width=lw_fab))
            kicad_mod.append(Line(start=[l_mounth + pck.mounting_hole_diameter / 2, t_fabp],
                                  end=[l_mounth + pck.mounting_hole_diameter / 2, t_fabp + h_fabp], layer='F.Fab',
                                  width=lw_fab))
    
    # create SILKSCREEN-layer
    keepouts = []
    x = 0
    for p in range(1, pck.pins + 1):
        if p==1:
            keepouts=keepouts+addKeepoutRect(x,0,pck.pad[0]+2*slk_dist,pck.pad[1]+2*slk_dist)
        else:
            keepouts=keepouts+addKeepoutRound(x,0,pck.pad[0]+2*slk_dist,pck.pad[1]+2*slk_dist)
        x = x + pck.rm
    
    
    addHLineWithKeepout(kicad_mod, l_slkp, l_slkp + w_slkp, t_slkp, 'F.SilkS', lw_slk, keepouts)
    addHLineWithKeepout(kicad_mod, l_slkp, l_slkp + w_slkp, t_slkp + h_slkp, 'F.SilkS', lw_slk, keepouts)
    addVLineWithKeepout(kicad_mod, l_slkp, t_slkp, t_slkp + h_slkp, 'F.SilkS', lw_slk, keepouts)
    addVLineWithKeepout(kicad_mod, l_slkp + w_slkp, t_slkp, t_slkp + h_slkp, 'F.SilkS', lw_slk, keepouts)
    if (pck.metal[2] > 0):
        addHLineWithKeepout(kicad_mod, l_slkp, l_slkp + w_slkp, t_slkp + h_slkm, 'F.SilkS', lw_slk, keepouts)
        if pck.mounting_hole_diameter > 0:
            addVLineWithKeepout(kicad_mod, l_mounth - pck.mounting_hole_diameter / 2, t_slkp, t_slkp + h_slkm,
                                'F.SilkS', lw_slk, keepouts)
            addVLineWithKeepout(kicad_mod, l_mounth + pck.mounting_hole_diameter / 2, t_slkp, t_slkp + h_slkm,
                                'F.SilkS', lw_slk, keepouts)
    else:
        if pck.mounting_hole_diameter > 0:
            addVLineWithKeepout(kicad_mod, l_mounth - pck.mounting_hole_diameter / 2, t_slkp, t_slkp + h_slkp,
                                'F.SilkS', lw_slk, keepouts)
            addVLineWithKeepout(kicad_mod, l_mounth + pck.mounting_hole_diameter / 2, t_slkp, t_slkp + h_slkp,
                                'F.SilkS', lw_slk, keepouts)
    
    # create courtyard
    kicad_mod.append(
        RectLine(start=[roundCrt(l_crt), roundCrt(t_crt)], end=[roundCrt(l_crt + w_crt), roundCrt(t_crt + h_crt)],
                 layer='F.CrtYd', width=lw_crt))
    
    # create pads
    x = 0
    for p in range(1, pck.pins + 1):
        if (p == 1):
            kicad_mod.append(
                Pad(number=p, type=Pad.TYPE_THT, shape=Pad.SHAPE_RECT, at=[x, 0], size=pck.pad, drill=pck.drill,
                    layers=['*.Cu', '*.Mask']))
        else:
            kicad_mod.append(
                Pad(number=p, type=Pad.TYPE_THT, shape=Pad.SHAPE_OVAL, at=[x, 0], size=pck.pad, drill=pck.drill,
                    layers=['*.Cu', '*.Mask']))
        x = x + pck.rm
    
    # add model
    if (has3d):
        kicad_mod.append(
            Model(filename=lib_name + ".3dshapes/" + footprint_name + ".wrl", at=x_3d, scale=s_3d, rotate=[0, 0, 0]))
    
    # print render tree
    # print(kicad_mod.getRenderTree())
    # print(kicad_mod.getCompleteRenderTree())
    
    # write file
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile(footprint_name + '.kicad_mod')



# horizontal symbols for rectangular transistors
def makeHOR(lib_name, pck, has3d=False, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], lptext="_LargePads"):
    l_fabp = -pck.pin_offset_x
    t_fabp = -pck.pin_minlength
    w_fabp = pck.plastic[0]
    h_fabp = pck.plastic[1]
    
    w_fabm = pck.metal[0]
    h_fabm = pck.metal[1]
    
    l_slkp = l_fabp - slk_offset
    t_slkp = t_fabp + slk_offset
    w_slkp = w_fabp + 2 * slk_offset
    h_slkp = h_fabp + 2 * slk_offset
    w_slkm = w_fabm + 2 * slk_offset
    h_slkm = h_fabm + 2 * slk_offset
    
    l_crt = min(-pck.pad[0] / 2, l_slkp) - crt_offset
    t_crt = t_slkp - max(h_slkp, h_slkm) - crt_offset
    h_crt = (-t_crt + pck.pad[1] / 2) + 2 * crt_offset
    addpad = 0
    if len(pck.additional_pin_pad_size) > 0:
        h_crt = h_crt + (pck.additional_pin_pad[1] + pck.additional_pin_pad_size[1] / 2 - h_fabm)
        t_crt = t_crt - (pck.additional_pin_pad[1] + pck.additional_pin_pad_size[1] / 2 - h_fabm)
        addpad = pck.additional_pin_pad_size[0]
        addpadx = l_fabp + pck.additional_pin_pad[0]
        addpady = t_fabp - pck.additional_pin_pad[1]
    w_crt = max(max(max(w_slkp, w_slkm), (pck.pins - 1) * pck.rm + pck.pad[0]), addpad) + 2 * crt_offset
    
    l_mounth = l_fabp + pck.mounting_hole_pos[0]
    t_mounth = t_fabp - pck.mounting_hole_pos[1]
    
    txt_x = l_slkp + max(w_slkp, w_slkm) / 2
    txt_t = (t_slkp - max(h_slkm, h_slkp)) - txt_offset
    txt_b = pck.pad[1] / 2 + txt_offset
    if len(pck.additional_pin_pad_size) > 0:
        txt_t = txt_t - (pck.additional_pin_pad[1] + pck.additional_pin_pad_size[1] / 2 - h_fabm)
    tag_items = ["Horizontal", "RM {0}mm".format(pck.rm)]
    
    footprint_name = pck.name
    if len(pck.additional_pin_pad_size) > 0:
        footprint_name = footprint_name + "-1EP"
    footprint_name = footprint_name + "_Horizontal"
    for t in pck.fpnametags:
        footprint_name = footprint_name + "_" + t
    if pck.largepads:
        tag_items.append("large Pads")
        footprint_name = footprint_name + lptext
    print(footprint_name)
    
    description = pck.name
    tags = pck.name
    for t in tag_items:
        description = description + ", " + t
        tags = tags + " " + t
    for t in pck.tags:
        description = description + ", " + t
        tags = tags + " " + t
    
    # init kicad footprint
    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription(description)
    kicad_mod.setTags(tags)
    
    # set general values
    kicad_mod.append(Text(type='reference', text='REF**', at=[txt_x, txt_t], layer='F.SilkS'))
    kicad_mod.append(Text(type='value', text=footprint_name, at=[txt_x, txt_b], layer='F.Fab'))
    
    # create FAB-layer
    if (h_fabm > 0):
        kicad_mod.append(RectLine(start=[l_fabp + pck.metal_offset_x, t_fabp - h_fabp],
                                  end=[l_fabp + pck.metal_offset_x + w_fabm, t_fabp - h_fabm], layer='F.Fab',
                                  width=lw_fab))
    if len(pck.plastic_angled)>0:
        kicad_mod.append(
            PolygoneLine(polygone=[[l_fabp, t_fabp], [l_fabp + w_fabp, t_fabp], [l_fabp + w_fabp, t_fabp - (h_fabp-pck.plastic_angled[1])],
                                   [l_fabp + w_fabp - pck.plastic_angled[0], t_fabp - (h_fabp)],
                                   [l_fabp + pck.plastic_angled[0], t_fabp - (h_fabp)],
                                   [l_fabp , t_fabp - (h_fabp-pck.plastic_angled[1])],
                                   [l_fabp, t_fabp]], layer='F.Fab', width=lw_fab))
    else:
        kicad_mod.append(
            RectLine(start=[l_fabp, t_fabp], end=[l_fabp + w_fabp, t_fabp - h_fabp], layer='F.Fab', width=lw_fab))
    if pck.mounting_hole_diameter > 0:
        kicad_mod.append(
            Circle(center=[l_mounth, t_mounth], radius=pck.mounting_hole_diameter / 2, layer='F.Fab', width=lw_fab))
    x = 0
    for p in range(1, pck.pins + 1):
        kicad_mod.append(Line(start=[x, t_fabp], end=[x, 0], layer='F.Fab', width=lw_fab))
        x = x + pck.rm
    
    # create SILKSCREEN-layer
    keepouts = []
    x = 0
    for p in range(1, pck.pins + 1):
        if p == 1:
            keepouts = keepouts + addKeepoutRect(x, 0, pck.pad[0] + 2 * slk_dist, pck.pad[1] + 2 * slk_dist)
        else:
            keepouts = keepouts + addKeepoutRound(x, 0, pck.pad[0] + 2 * slk_dist, pck.pad[1] + 2 * slk_dist)
        x = x + pck.rm
    
    if len(pck.additional_pin_pad_size) > 0:
        keepouts.append([addpadx - pck.additional_pin_pad_size[0] / 2 - slk_dist,
                         addpadx + pck.additional_pin_pad_size[0] / 2 + slk_dist,
                         addpady - pck.additional_pin_pad_size[1] / 2 - slk_dist,
                         addpady + pck.additional_pin_pad_size[1] / 2 + slk_dist])
    
    addHLineWithKeepout(kicad_mod, l_slkp, l_slkp + w_slkp, t_slkp, 'F.SilkS', lw_slk, keepouts)
    if h_fabm > 0:
        addHLineWithKeepout(kicad_mod, l_slkp, l_slkp + w_slkp, t_slkp - h_slkm, 'F.SilkS', lw_slk, keepouts)
        addVLineWithKeepout(kicad_mod, l_slkp, t_slkp, t_slkp - h_slkm, 'F.SilkS', lw_slk, keepouts)
        addVLineWithKeepout(kicad_mod, l_slkp + w_slkp, t_slkp, t_slkp - h_slkm, 'F.SilkS', lw_slk, keepouts)
    else:
        addHLineWithKeepout(kicad_mod, l_slkp, l_slkp + w_slkp, t_slkp - h_slkp, 'F.SilkS', lw_slk, keepouts)
        addVLineWithKeepout(kicad_mod, l_slkp, t_slkp, t_slkp - h_slkp, 'F.SilkS', lw_slk, keepouts)
        addVLineWithKeepout(kicad_mod, l_slkp + w_slkp, t_slkp, t_slkp - h_slkp, 'F.SilkS', lw_slk, keepouts)


    x = 0
    for p in range(1, pck.pins + 1):
        addVLineWithKeepout(kicad_mod, x, t_slkp, -(pck.pad[1]/2+slk_dist), 'F.SilkS', lw_slk, keepouts)
        x = x + pck.rm

    # create courtyard
    kicad_mod.append(
        RectLine(start=[roundCrt(l_crt), roundCrt(t_crt)], end=[roundCrt(l_crt + w_crt), roundCrt(t_crt + h_crt)],
                 layer='F.CrtYd', width=lw_crt))
    
    # create mounting hole
    if pck.mounting_hole_drill > 0:
        kicad_mod.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_OVAL, at=[l_mounth, t_mounth],
                             size=[pck.mounting_hole_drill, pck.mounting_hole_drill], drill=pck.mounting_hole_drill,
                             layers=['*.Cu', '*.Mask']))
    
    if len(pck.additional_pin_pad_size) > 0:
        kicad_mod.append(Pad(number=pck.pins + 1, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, at=[addpadx, addpady],
                             size=pck.additional_pin_pad_size, drill=0, layers=['F.Cu', 'F.Mask']))
    
    # create pads
    x = 0
    for p in range(1, pck.pins + 1):
        if (p == 1):
            kicad_mod.append(
                Pad(number=p, type=Pad.TYPE_THT, shape=Pad.SHAPE_RECT, at=[x, 0], size=pck.pad, drill=pck.drill,
                    layers=['*.Cu', '*.Mask']))
        else:
            kicad_mod.append(
                Pad(number=p, type=Pad.TYPE_THT, shape=Pad.SHAPE_OVAL, at=[x, 0], size=pck.pad, drill=pck.drill,
                    layers=['*.Cu', '*.Mask']))
        x = x + pck.rm
    
    # add model
    if (has3d):
        kicad_mod.append(
            Model(filename=lib_name + ".3dshapes/" + footprint_name + ".wrl", at=x_3d, scale=s_3d, rotate=[0, 0, 0]))
    
    # print render tree
    # print(kicad_mod.getRenderTree())
    # print(kicad_mod.getCompleteRenderTree())
    
    # write file
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile(footprint_name + '.kicad_mod')


# vertical, mounted-from-Lowerside symbols for rectangular transistors
def makeVERTLS(lib_name, pck, has3d=False, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], lptext="_LargePads"):
    l_fabp = -pck.pin_offset_x
    t_fabp = -pck.pin_offset_z
    w_fabp = pck.plastic[0]
    h_fabp = pck.plastic[2]
    
    w_fabm = pck.metal[0]
    h_fabm = pck.metal[2]
    
    l_slkp = l_fabp - slk_offset
    t_slkp = t_fabp - slk_offset
    w_slkp = w_fabp + 2 * slk_offset
    h_slkp = h_fabp + 2 * slk_offset
    w_slkm = w_fabm + 2 * slk_offset
    h_slkm = h_fabm + 2 * slk_offset
    
    l_crt = min(-pck.pad[0] / 2, l_slkp) - crt_offset
    t_crt = min(-pck.pad[1] / 2, t_slkp) - crt_offset
    w_crt = max(max(w_slkp, w_slkm), (pck.pins - 1) * pck.rm + pck.pad[0]) + 2 * crt_offset
    h_crt = max(max(h_slkp, h_slkm), -t_crt + pck.pad[1] / 2) + 2 * crt_offset
    
    l_mounth = l_fabp + pck.mounting_hole_pos[0]
    
    txt_x = l_slkp + max(w_slkp, w_slkm) / 2
    
    tag_items = ["Vertical", "RM {0}mm".format(pck.rm), "mount on lower-side of PCB"]
    
    footprint_name = pck.name
    footprint_name = footprint_name + "_Vertical"
    for t in pck.fpnametags:
        footprint_name = footprint_name + "_" + t
    footprint_name = footprint_name + "_MountFromLS"
    if pck.largepads:
        tag_items.append("large Pads")
        footprint_name = footprint_name + lptext
    
    print(footprint_name)
    
    description = pck.name
    tags = pck.name
    for t in tag_items:
        description = description + ", " + t
        tags = tags + " " + t
    for t in pck.tags:
        description = description + ", " + t
        tags = tags + " " + t
    
    # init kicad footprint
    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription(description)
    kicad_mod.setTags(tags)
    
    kicad_modt = Translation(-(pck.pins - 1) * pck.rm, 0)
    kicad_mod.append(kicad_modt)
    
    # set general values
    kicad_modt.append(Text(type='reference', text='REF**', at=[txt_x, t_slkp - txt_offset], layer='F.SilkS'))
    kicad_modt.append(
        Text(type='value', text=footprint_name, at=[txt_x, t_slkp + max(h_slkm, h_slkp) + txt_offset], layer='B.Fab'))
    
    # create FAB-layer
    kicad_modt.append(
        RectLine(start=[l_fabp, t_fabp], end=[l_fabp + w_fabp, t_fabp + h_fabp], layer='B.Fab', width=lw_fab))
    if (pck.metal[2] > 0):
        kicad_modt.append(
            Line(start=[l_fabp, t_fabp + h_fabm], end=[l_fabp + w_fabp, t_fabp + h_fabm], layer='B.Fab', width=lw_fab))
        if pck.mounting_hole_diameter > 0:
            kicad_modt.append(Line(start=[l_mounth - pck.mounting_hole_diameter / 2, t_fabp],
                                   end=[l_mounth - pck.mounting_hole_diameter / 2, t_fabp + h_fabm], layer='B.Fab',
                                   width=lw_fab))
            kicad_modt.append(Line(start=[l_mounth + pck.mounting_hole_diameter / 2, t_fabp],
                                   end=[l_mounth + pck.mounting_hole_diameter / 2, t_fabp + h_fabm], layer='B.Fab',
                                   width=lw_fab))
    else:
        if pck.mounting_hole_diameter > 0:
            kicad_modt.append(Line(start=[l_mounth - pck.mounting_hole_diameter / 2, t_fabp],
                                   end=[l_mounth - pck.mounting_hole_diameter / 2, t_fabp + h_fabp], layer='B.Fab',
                                   width=lw_fab))
            kicad_modt.append(Line(start=[l_mounth + pck.mounting_hole_diameter / 2, t_fabp],
                                   end=[l_mounth + pck.mounting_hole_diameter / 2, t_fabp + h_fabp], layer='B.Fab',
                                   width=lw_fab))
    
    # create SILKSCREEN-layer
    keepouts = []
    x = (pck.pins - 1) * pck.rm
    for p in range(1, pck.pins + 1):
        if p == 1:
            keepouts = keepouts + addKeepoutRect(x, 0, pck.pad[0] + 2 * slk_dist, pck.pad[1] + 2 * slk_dist)
        else:
            keepouts = keepouts + addKeepoutRound(x, 0, pck.pad[0] + 2 * slk_dist, pck.pad[1] + 2 * slk_dist)
        x = x - pck.rm
    
    addHDLineWithKeepout(kicad_modt, l_slkp, 3 * lw_slk, l_slkp + w_slkp, t_slkp, 'F.SilkS', lw_slk, keepouts)
    addHDLineWithKeepout(kicad_modt, l_slkp, 3 * lw_slk, l_slkp + w_slkp, t_slkp + h_slkp, 'F.SilkS', lw_slk, keepouts)
    addVDLineWithKeepout(kicad_modt, l_slkp, t_slkp, 3 * lw_slk, t_slkp + h_slkp, 'F.SilkS', lw_slk, keepouts)
    addVDLineWithKeepout(kicad_modt, l_slkp + w_slkp, t_slkp, 3 * lw_slk, t_slkp + h_slkp, 'F.SilkS', lw_slk, keepouts)
    if (pck.metal[2] > 0):
        addHDLineWithKeepout(kicad_modt, l_slkp, 3 * lw_slk, l_slkp + w_slkp, t_slkp + h_slkm, 'F.SilkS', lw_slk,
                             keepouts)
        if pck.mounting_hole_diameter > 0:
            addVDLineWithKeepout(kicad_modt, l_mounth - pck.mounting_hole_diameter / 2, t_slkp, 3 * lw_slk,
                                 t_slkp + h_slkm,
                                 'F.SilkS', lw_slk, keepouts)
            addVDLineWithKeepout(kicad_modt, l_mounth + pck.mounting_hole_diameter / 2, t_slkp, 3 * lw_slk,
                                 t_slkp + h_slkm,
                                 'F.SilkS', lw_slk, keepouts)
    else:
        if pck.mounting_hole_diameter > 0:
            addVDLineWithKeepout(kicad_modt, l_mounth - pck.mounting_hole_diameter / 2, t_slkp, 3 * lw_slk,
                                 t_slkp + h_slkp,
                                 'F.SilkS', lw_slk, keepouts)
            addVDLineWithKeepout(kicad_modt, l_mounth + pck.mounting_hole_diameter / 2, t_slkp, 3 * lw_slk,
                                 t_slkp + h_slkp,
                                 'F.SilkS', lw_slk, keepouts)
    
    # create courtyard
    kicad_modt.append(
        RectLine(start=[roundCrt(l_crt), roundCrt(t_crt)], end=[roundCrt(l_crt + w_crt), roundCrt(t_crt + h_crt)],
                 layer='B.CrtYd', width=lw_crt))
    
    # create pads
    x = (pck.pins - 1) * pck.rm
    for p in range(1, pck.pins + 1):
        if (p == 1):
            kicad_modt.append(
                Pad(number=p, type=Pad.TYPE_THT, shape=Pad.SHAPE_RECT, at=[x, 0], size=pck.pad, drill=pck.drill,
                    layers=['*.Cu', '*.Mask']))
        else:
            kicad_modt.append(
                Pad(number=p, type=Pad.TYPE_THT, shape=Pad.SHAPE_OVAL, at=[x, 0], size=pck.pad, drill=pck.drill,
                    layers=['*.Cu', '*.Mask']))
        x = x - pck.rm
    
    # add model
    if (has3d):
        kicad_modt.append(
            Model(filename=lib_name + ".3dshapes/" + footprint_name + ".wrl", at=x_3d, scale=s_3d, rotate=[0, 0, 0]))
    
    # print render tree
    # print(kicad_mod.getRenderTree())
    # print(kicad_mod.getCompleteRenderTree())
    
    # write file
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile(footprint_name + '.kicad_mod')


# horizontal, mounted-from-Lowerside symbols for rectangular transistors
def makeHORLS(lib_name, pck, has3d=False, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], lptext="_LargePads"):
    l_fabp = -pck.pin_offset_x
    t_fabp = -pck.pin_minlength
    w_fabp = pck.plastic[0]
    h_fabp = pck.plastic[1]
    
    w_fabm = pck.metal[0]
    h_fabm = pck.metal[1]
    
    l_slkp = l_fabp - slk_offset
    t_slkp = t_fabp + slk_offset
    w_slkp = w_fabp + 2 * slk_offset
    h_slkp = h_fabp + 2 * slk_offset
    w_slkm = w_fabm + 2 * slk_offset
    h_slkm = h_fabm + 2 * slk_offset
    
    l_crt = min(-pck.pad[0] / 2, l_slkp) - crt_offset
    t_crt = t_slkp - max(h_slkp, h_slkm) - crt_offset
    h_crt = (-t_crt + pck.pad[1] / 2) + 2 * crt_offset
    addpad = 0
    if len(pck.additional_pin_pad_size) > 0:
        h_crt = h_crt + (pck.additional_pin_pad[1] + pck.additional_pin_pad_size[1] / 2 - h_fabm)
        t_crt = t_crt - (pck.additional_pin_pad[1] + pck.additional_pin_pad_size[1] / 2 - h_fabm)
        addpad = pck.additional_pin_pad_size[0]
        addpadx = l_fabp + pck.additional_pin_pad[0]
        addpady = t_fabp - pck.additional_pin_pad[1]
    w_crt = max(max(max(w_slkp, w_slkm), (pck.pins - 1) * pck.rm + pck.pad[0]), addpad) + 2 * crt_offset
    
    l_mounth = l_fabp + pck.mounting_hole_pos[0]
    t_mounth = t_fabp - pck.mounting_hole_pos[1]
    
    txt_x = l_slkp + max(w_slkp, w_slkm) / 2
    txt_t = (t_slkp - max(h_slkm, h_slkp)) - txt_offset
    txt_b = pck.pad[1] / 2 + txt_offset
    if len(pck.additional_pin_pad_size) > 0:
        txt_t = txt_t - (pck.additional_pin_pad[1] + pck.additional_pin_pad_size[1] / 2 - h_fabm)
    tag_items = ["Horizontal", "RM {0}mm".format(pck.rm), "mount on lower-side of PCB", "mount with cooling pad pointing away from PCB", "Reversed"]
    
    footprint_name = pck.name
    if len(pck.additional_pin_pad_size) > 0:
        footprint_name = footprint_name + "-1EP"
    footprint_name = footprint_name + "_Horizontal"
    for t in pck.fpnametags:
        footprint_name = footprint_name + "_" + t
    footprint_name = footprint_name + "_Reversed_MountFromLS"
    if pck.largepads:
        tag_items.append("large Pads")
        footprint_name = footprint_name + lptext
    print(footprint_name)
    
    description = pck.name
    tags = pck.name
    for t in tag_items:
        description = description + ", " + t
        tags = tags + " " + t
    for t in pck.tags:
        description = description + ", " + t
        tags = tags + " " + t
    
    # init kicad footprint
    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription(description)
    kicad_mod.setTags(tags)

    kicad_modt=Translation(-(pck.pins - 1) * pck.rm,0)
    kicad_mod.append(kicad_modt)

    # set general values
    kicad_modt.append(Text(type='reference', text='REF**', at=[txt_x, txt_t], layer='F.SilkS'))
    kicad_modt.append(Text(type='value', text=footprint_name, at=[txt_x, txt_b], layer='B.Fab'))
    
    # create FAB-layer
    if (h_fabm > 0):
        kicad_modt.append(RectLine(start=[l_fabp + pck.metal_offset_x, t_fabp - h_fabp],
                                  end=[l_fabp + pck.metal_offset_x + w_fabm, t_fabp - h_fabm], layer='B.Fab',
                                  width=lw_fab))
    kicad_modt.append(
        RectLine(start=[l_fabp, t_fabp], end=[l_fabp + w_fabp, t_fabp - h_fabp], layer='B.Fab', width=lw_fab))
    kicad_modt.append(
        RectLine(start=[l_fabp, t_fabp], end=[l_fabp + w_fabp, t_fabp - h_fabp], layer='B.Fab', width=lw_fab))
    if pck.mounting_hole_diameter > 0:
        kicad_modt.append(
            Circle(center=[l_mounth, t_mounth], radius=pck.mounting_hole_diameter / 2, layer='B.Fab', width=lw_fab))
    x = 0
    for p in range(1, pck.pins + 1):
        kicad_modt.append(Line(start=[x, t_fabp], end=[x, 0], layer='B.Fab', width=lw_fab))
        x = x + pck.rm
    
    # create SILKSCREEN-layer
    keepouts = []
    x = 0
    for p in range(1, pck.pins + 1):
        if p == 1:
            keepouts = keepouts + addKeepoutRect(x, 0, pck.pad[0] + 2 * slk_dist, pck.pad[1] + 2 * slk_dist)
        else:
            keepouts = keepouts + addKeepoutRound(x, 0, pck.pad[0] + 2 * slk_dist, pck.pad[1] + 2 * slk_dist)
        x = x + pck.rm
    
    if len(pck.additional_pin_pad_size) > 0:
        keepouts.append([addpadx - pck.additional_pin_pad_size[0] / 2 - slk_dist,
                         addpadx + pck.additional_pin_pad_size[0] / 2 + slk_dist,
                         addpady - pck.additional_pin_pad_size[1] / 2 - slk_dist,
                         addpady + pck.additional_pin_pad_size[1] / 2 + slk_dist])
    
    addHDLineWithKeepout(kicad_modt, l_slkp, 3 * lw_slk, l_slkp + w_slkp, t_slkp, 'F.SilkS', lw_slk, keepouts)
    if h_fabm > 0:
        addHDLineWithKeepout(kicad_modt, l_slkp, 3 * lw_slk, l_slkp + w_slkp, t_slkp - h_slkm, 'F.SilkS', lw_slk, keepouts)
        addVDLineWithKeepout(kicad_modt, l_slkp, t_slkp, 3 * lw_slk, t_slkp - h_slkm, 'F.SilkS', lw_slk, keepouts)
        addVDLineWithKeepout(kicad_modt, l_slkp + w_slkp, t_slkp, 3 * lw_slk, t_slkp - h_slkm, 'F.SilkS', lw_slk, keepouts)
    else:
        addHDLineWithKeepout(kicad_modt, l_slkp, 3 * lw_slk, l_slkp + w_slkp, t_slkp - h_slkp, 'F.SilkS', lw_slk, keepouts)
        addVDLineWithKeepout(kicad_modt, l_slkp, t_slkp, 3 * lw_slk, t_slkp - h_slkp, 'F.SilkS', lw_slk, keepouts)
        addVDLineWithKeepout(kicad_modt, l_slkp + w_slkp, t_slkp, 3 * lw_slk, t_slkp - h_slkp, 'F.SilkS', lw_slk, keepouts)

    x = 0
    for p in range(1, pck.pins + 1):
        addVDLineWithKeepout(kicad_modt, x, t_slkp, 3 * lw_slk, -(pck.pad[1]/2+slk_dist), 'F.SilkS', lw_slk, keepouts)
        x = x + pck.rm

    # create courtyard
    kicad_modt.append(
        RectLine(start=[roundCrt(l_crt), roundCrt(t_crt)], end=[roundCrt(l_crt + w_crt), roundCrt(t_crt + h_crt)],
                 layer='B.CrtYd', width=lw_crt))
    
    # create mounting hole
    if pck.mounting_hole_drill > 0:
        kicad_modt.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_OVAL, at=[l_mounth, t_mounth],
                             size=[pck.mounting_hole_drill, pck.mounting_hole_drill], drill=pck.mounting_hole_drill,
                             layers=['*.Cu', '*.Mask']))
    
    if len(pck.additional_pin_pad_size) > 0:
        kicad_modt.append(Pad(number=pck.pins + 1, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, at=[addpadx, addpady],
                             size=pck.additional_pin_pad_size, drill=0, layers=['B.Cu', 'F.Mask']))
    
    # create pads
    x = 0
    for p in range(1, pck.pins + 1):
        if (p == 1):
            kicad_modt.append(
                Pad(number=p, type=Pad.TYPE_THT, shape=Pad.SHAPE_RECT, at=[x, 0], size=pck.pad, drill=pck.drill,
                    layers=['*.Cu', '*.Mask']))
        else:
            kicad_modt.append(
                Pad(number=p, type=Pad.TYPE_THT, shape=Pad.SHAPE_OVAL, at=[x, 0], size=pck.pad, drill=pck.drill,
                    layers=['*.Cu', '*.Mask']))
        x = x + pck.rm
    
    # add model
    if (has3d):
        kicad_modt.append(
            Model(filename=lib_name + ".3dshapes/" + footprint_name + ".wrl", at=x_3d, scale=s_3d, rotate=[0, 0, 0]))
    
    # print render tree
    # print(kicad_mod.getRenderTree())
    # print(kicad_mod.getCompleteRenderTree())
    
    # write file
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile(footprint_name + '.kicad_mod')


# horizontal reversedsymbols for rectangular transistors
def makeHORREV(lib_name, pck, has3d=False, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], lptext="_LargePads"):
    l_fabp = -pck.pin_offset_x
    t_fabp = pck.pin_minlength
    w_fabp = pck.plastic[0]
    h_fabp = pck.plastic[1]
    
    w_fabm = pck.metal[0]
    h_fabm = pck.metal[1]
    
    l_slkp = l_fabp - slk_offset
    t_slkp = t_fabp - slk_offset
    w_slkp = w_fabp + 2 * slk_offset
    h_slkp = h_fabp + 2 * slk_offset
    w_slkm = w_fabm + 2 * slk_offset
    h_slkm = h_fabm + 2 * slk_offset

    l_crt = min(-pck.pad[0] / 2, l_slkp) - crt_offset
    t_crt = -pck.pad[1]/2- crt_offset
    w_crt = max(max(w_slkp, w_slkm), (pck.pins - 1) * pck.rm + pck.pad[0]) + 2 * crt_offset
    h_crt = -t_crt + t_slkp+max(h_slkp, h_slkm) + 2 * crt_offset
    
    l_mounth = l_fabp + pck.mounting_hole_pos[0]
    t_mounth = t_fabp + pck.mounting_hole_pos[1]
    
    txt_x = l_slkp + max(w_slkp, w_slkm) / 2
    txt_t = (t_slkp + max(h_slkm, h_slkp)) + txt_offset
    txt_b = -pck.pad[1] / 2 - txt_offset
    
    tag_items = ["Horizontal", "RM {0}mm".format(pck.rm)]
    
    footprint_name = pck.name
    footprint_name = footprint_name + "_Horizontal" + "_Reversed"
    for t in pck.fpnametags:
        footprint_name = footprint_name + "_" + t
    if pck.largepads:
        tag_items.append("large Pads")
        footprint_name = footprint_name + lptext
    print(footprint_name)
    
    description = pck.name
    tags = pck.name
    for t in tag_items:
        description = description + ", " + t
        tags = tags + " " + t
    for t in pck.tags:
        description = description + ", " + t
        tags = tags + " " + t
    
    # init kicad footprint
    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription(description)
    kicad_mod.setTags(tags)
    
    # set general values
    kicad_mod.append(Text(type='reference', text='REF**', at=[txt_x, txt_t], layer='F.SilkS'))
    kicad_mod.append(Text(type='value', text=footprint_name, at=[txt_x, txt_b], layer='F.Fab'))
    
    # create FAB-layer
    if (h_fabm > 0):
        kicad_mod.append(
            RectLine(start=[l_fabp, t_fabp], end=[l_fabp + w_fabm, t_fabp + h_fabm], layer='F.Fab', width=lw_fab))
    kicad_mod.append(RectLine(start=[l_fabp, t_fabp], end=[l_fabp + w_fabp, t_fabp + h_fabp], layer='F.Fab', width=lw_fab))
    kicad_mod.append(RectLine(start=[l_fabp, t_fabp], end=[l_fabp + w_fabp, t_fabp + h_fabp], layer='F.Fab', width=lw_fab))
    if pck.mounting_hole_diameter > 0:
        kicad_mod.append(Circle(center=[l_mounth, t_mounth], radius=pck.mounting_hole_diameter / 2, layer='F.Fab', width=lw_fab))
    x = 0
    for p in range(1, pck.pins + 1):
        kicad_mod.append(Line(start=[x, t_fabp], end=[x, 0], layer='F.Fab', width=lw_fab))
        x = x + pck.rm
    
    # create SILKSCREEN-layer
    keepouts = []
    x = 0
    for p in range(1, pck.pins + 1):
        if p==1:
            keepouts=keepouts+addKeepoutRect(x,0,pck.pad[0]+2*slk_dist,pck.pad[1]+2*slk_dist)
        else:
            keepouts=keepouts+addKeepoutRound(x,0,pck.pad[0]+2*slk_dist,pck.pad[1]+2*slk_dist)
        x = x + pck.rm
    
    addHLineWithKeepout(kicad_mod, l_slkp, l_slkp + w_slkp, t_slkp, 'F.SilkS', lw_slk, keepouts)
    addHLineWithKeepout(kicad_mod, l_slkp, l_slkp + w_slkp, t_slkp + h_slkp, 'F.SilkS', lw_slk, keepouts)
    addVLineWithKeepout(kicad_mod, l_slkp, t_slkp, t_slkp + h_slkp, 'F.SilkS', lw_slk, keepouts)
    addVLineWithKeepout(kicad_mod, l_slkp + w_slkp, t_slkp, t_slkp + h_slkp, 'F.SilkS', lw_slk, keepouts)
    if (h_fabm > 0):
        addHDLineWithKeepout(kicad_mod, l_slkp, 4*lw_slk, l_slkp + w_slkm, t_slkp + h_slkm, 'F.SilkS', lw_slk, keepouts)
        addVDLineWithKeepout(kicad_mod, l_slkp, t_slkp + h_slkp+lw_slk*2, 4 * lw_slk, t_slkp + h_slkm, 'F.SilkS', lw_slk, keepouts)
        addVDLineWithKeepout(kicad_mod, l_slkp + w_slkp, t_slkp + h_slkp+lw_slk*2, 4 * lw_slk, t_slkp + h_slkm, 'F.SilkS', lw_slk, keepouts)
    x = 0
    for p in range(1, pck.pins + 1):
        addVLineWithKeepout(kicad_mod, x, t_slkp, pck.pad[1]/2+slk_dist, 'F.SilkS', lw_slk, keepouts)
        x = x + pck.rm

    # create courtyard
    kicad_mod.append(
        RectLine(start=[roundCrt(l_crt), roundCrt(t_crt)], end=[roundCrt(l_crt + w_crt), roundCrt(t_crt + h_crt)],
                 layer='F.CrtYd', width=lw_crt))
    
    # create mounting hole
    if pck.mounting_hole_drill > 0:
        kicad_mod.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_OVAL, at=[l_mounth, t_mounth],
                         size=[pck.mounting_hole_drill, pck.mounting_hole_drill], drill=pck.mounting_hole_drill,
                         layers=['*.Cu', '*.Mask']))
    
    # create pads
    x = 0
    for p in range(1, pck.pins + 1):
        if (p==1):
            kicad_mod.append(Pad(number=p, type=Pad.TYPE_THT, shape=Pad.SHAPE_RECT, at=[x, 0], size=pck.pad, drill=pck.drill, layers=['*.Cu', '*.Mask']))
        else:
            kicad_mod.append(Pad(number=p, type=Pad.TYPE_THT, shape=Pad.SHAPE_OVAL, at=[x, 0], size=pck.pad, drill=pck.drill,layers=['*.Cu', '*.Mask']))
        x = x + pck.rm
    
    # add model
    if (has3d):
        kicad_mod.append(
            Model(filename=lib_name + ".3dshapes/" + footprint_name + ".wrl", at=x_3d, scale=s_3d, rotate=[0, 0, 0]))
    
    # print render tree
    # print(kicad_mod.getRenderTree())
    # print(kicad_mod.getCompleteRenderTree())
    
    # write file
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile(footprint_name + '.kicad_mod')


if __name__ == '__main__':
    packs=  ["SOT93",        "TO-264",       "TO-247",       "TO-218",       "TO-251",       "TO-126",       "TO-220",                            "TO-280",    "TO-262",    "SIPAC",    ]
    pins=   [[2,     3 ],    [2,     3 ],    [2,     3 ],    [2,     3    ], [2,     3    ], [2,     3    ], [2,        3,            4,     5],  [3     ],    [3     ],    [3     ],    ]
    rms=    [[0,     0 ],    [0,     0 ],    [0,     0 ],    [0,     0    ], [0,     0    ], [0,     0    ], [0,        0,         2.54,   1.7],  [0     ],    [0     ],    [0     ],    ]
    has3dv= [[False, False], [False, False], [False, False], [False, False], [False, False], [False, False], [True,     True,     False, False],  [False ],    [False ],    [False ],    ]
    has3dh= [[False, False], [False, False], [False, False], [False, False], [False, False], [False, False], [True,     True,     False, False],  [False ],    [False ],    [False ],    ]
    off3d=  [[[],    []],    [[],    []],    [[],    []],    [[],    []   ], [[],    []   ], [[],    []   ], [[0.1,0,0],[0.1,0,0],   [],    []],  [[]],        [[]],        [[]],        ]
    scale3d=[[[],    []],    [[],    []],    [[],    []],    [[],    []   ], [[],    []   ], [[],    []   ], [[],       [],          [],    []],  [[]],        [[]],        [[]],        ]
    for p in range(0,len(packs)):
        for pidx in range(0,len(pins[p])):
            o3d=[0,0,0]
            s3d=[1 / 2.54, 1 / 2.54, 1 / 2.54]
            if len(off3d[p][pidx])>0:
                o3d=off3d[p][pidx]
            if len(scale3d[p][pidx])>0:
                s3d=scale3d[p][pidx]
                
            pack_norm=pack(packs[p], pins[p][pidx], rms[p][pidx], False)
            libn="TO_SOT_Packages_THT"
            makeVERT(libn, pack_norm, has3dv[p][pidx], o3d, s3d)
            makeVERTLS(libn, pack_norm, has3dv[p][pidx], o3d, s3d)
            makeHOR(libn, pack_norm, has3dh[p][pidx], o3d, s3d)
            if (len(pack_norm.additional_pin_pad)<=0):
                makeHORLS(libn, pack_norm, has3dh[p][pidx], o3d, s3d)
                makeHORREV(libn, pack_norm, has3dh[p][pidx], o3d, s3d)



            #pack_largepins=pack(packs[p], pins[p][pidx], rms[p][pidx], True)
            #makeVERT("TO_SOT_Packages_THT", pack_largepins, has3dv[p][pidx], o3d, s3d)
            #makeHOR("TO_SOT_Packages_THT", pack_largepins, has3dh[p][pidx], o3d, s3d)
            #if (len(pack_largepins.additional_pin_pad) <= 0):
            #    makeHORREV("TO_SOT_Packages_THT", pack_largepins, has3dh[p][pidx], o3d, s3d)

