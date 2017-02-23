#usr/bin/env python

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
def makeVERT(lib_name, pck, has3d=False, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], lptext="_LargePads", r_3d=[0, 0, 0]):
    padsize=pck.pad
    l_fabp = -pck.pin_offset_x
    t_fabp = -pck.pin_offset_z
    if pck.staggered_type >0:
        t_fabp=-pck.staggered_pin_offset_z
        
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
    
    l_mounth = l_fabp + pck.mounting_hole_pos[0]
    
    txt_x = l_slkp + max(w_slkp, w_slkm) / 2
    
    # calculate pad positions
    pads=[]
    yshift=0
    y1=0
    y2=0
    maxpiny=0
    if pck.staggered_type == 1:
        y1 = pck.staggered_rm[0]
        yshift = -pck.staggered_rm[0]
        y2 = 0
        maxpiny = pck.staggered_rm[0]
        if len(pck.staggered_pad)>0:
            padsize=pck.staggered_pad
    elif pck.staggered_type == 2:
        y1 = 0
        yshift = 0
        y2=pck.staggered_rm[0]
        maxpiny = pck.staggered_rm[0]
        if len(pck.staggered_pad) > 0:
            padsize = pck.staggered_pad

    pinwid = (pck.pins - 1) * pck.rm
    if len(pck.rm_list) > 0:
        pinwid = 0
        for rm in pck.rm_list:
            pinwid = pinwid + rm

    l_crt = min(-padsize[0] / 2, l_fabp) - crt_offset
    t_crt = min(-padsize[1] / 2, t_fabp) - crt_offset
    w_crt = max(max(w_fabp, w_fabm), pinwid + padsize[0]) + 2 * crt_offset
    h_crt = max(t_fabp+max(h_fabp, h_fabm)+ crt_offset-t_crt, -t_crt + maxpiny + padsize[1] / 2 + crt_offset)

    y=y1
    x = 0
    for p in range(1, pck.pins + 1):
        if (p % 2) == 1:
            y = y1
        else:
            y = y2
        pads.append([x, y])
        if len(pck.rm_list)>0 and p<=len(pck.rm_list):
            x = x + pck.rm_list[p-1]
        else:
            x = x + pck.rm
            

    tag_items = ["Vertical", "RM {0}mm".format(pck.rm)]
    
    footprint_name = pck.name
    for t in pck.more_packnames:
        footprint_name = footprint_name + "_" + t
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

    kicad_modt = Translation(0, yshift)
    kicad_mod.append(kicad_modt)

    # set general values
    kicad_modt.append(Text(type='reference', text='REF**', at=[txt_x, t_slkp - txt_offset], layer='F.SilkS'))
    kicad_modt.append(Text(type='user', text='%R', at=[txt_x, t_slkp - txt_offset], layer='F.Fab'))
    kicad_modt.append(
        Text(type='value', text=footprint_name, at=[txt_x, t_slkp + max(h_slkm, h_slkp, h_slkp+maxpiny + padsize[1] / 2) + txt_offset], layer='F.Fab'))
    
    # create FAB-layer
    kicad_modt.append(
        RectLine(start=[l_fabp, t_fabp], end=[l_fabp + w_fabp, t_fabp + h_fabp], layer='F.Fab', width=lw_fab))
    if (pck.metal[2] > 0):
        kicad_modt.append(
            Line(start=[l_fabp, t_fabp + h_fabm], end=[l_fabp + w_fabp, t_fabp + h_fabm], layer='F.Fab', width=lw_fab))
        if pck.mounting_hole_diameter > 0:
            kicad_modt.append(Line(start=[l_mounth - pck.mounting_hole_diameter / 2, t_fabp],
                                  end=[l_mounth - pck.mounting_hole_diameter / 2, t_fabp + h_fabm], layer='F.Fab',
                                  width=lw_fab))
            kicad_modt.append(Line(start=[l_mounth + pck.mounting_hole_diameter / 2, t_fabp],
                                  end=[l_mounth + pck.mounting_hole_diameter / 2, t_fabp + h_fabm], layer='F.Fab',
                                  width=lw_fab))
    else:
        if pck.mounting_hole_diameter > 0:
            kicad_modt.append(Line(start=[l_mounth - pck.mounting_hole_diameter / 2, t_fabp],
                                  end=[l_mounth - pck.mounting_hole_diameter / 2, t_fabp + h_fabp], layer='F.Fab',
                                  width=lw_fab))
            kicad_modt.append(Line(start=[l_mounth + pck.mounting_hole_diameter / 2, t_fabp],
                                  end=[l_mounth + pck.mounting_hole_diameter / 2, t_fabp + h_fabp], layer='F.Fab',
                                  width=lw_fab))
    for p in range(0, len(pads)):
        yl1=t_fabp + h_fabp
        yl2=pads[p][1]
        if yl2>yl1:
            kicad_modt.append(Line(start=[pads[p][0], yl1], end=[pads[p][0], yl2], layer='F.Fab', width=lw_fab))
    
    # create SILKSCREEN-layer
    keepouts = []
    for p in range(0,len(pads)):
        if p==0:
            keepouts=keepouts+addKeepoutRect(pads[p][0],pads[p][1],padsize[0]+2*slk_dist,padsize[1]+2*slk_dist)
        else:
            keepouts=keepouts+addKeepoutRound(pads[p][0],pads[p][1],padsize[0]+2*slk_dist,padsize[1]+2*slk_dist)
    
    #for ko in keepouts:
    #    kicad_modt.append(
    #        RectLine(start=[ko[0],ko[2]], end=[ko[1],ko[3]], layer='B.Fab', width=lw_fab))
    
    addHLineWithKeepout(kicad_modt, l_slkp, l_slkp + w_slkp, t_slkp, 'F.SilkS', lw_slk, keepouts)
    addHLineWithKeepout(kicad_modt, l_slkp, l_slkp + w_slkp, t_slkp + h_slkp, 'F.SilkS', lw_slk, keepouts)
    addVLineWithKeepout(kicad_modt, l_slkp, t_slkp, t_slkp + h_slkp, 'F.SilkS', lw_slk, keepouts)
    addVLineWithKeepout(kicad_modt, l_slkp + w_slkp, t_slkp, t_slkp + h_slkp, 'F.SilkS', lw_slk, keepouts)
    if (pck.metal[2] > 0):
        addHLineWithKeepout(kicad_modt, l_slkp, l_slkp + w_slkp, t_slkp + h_slkm, 'F.SilkS', lw_slk, keepouts)
        if pck.mounting_hole_diameter > 0:
            addVLineWithKeepout(kicad_modt, l_mounth - pck.mounting_hole_diameter / 2, t_slkp, t_slkp + h_slkm,
                                'F.SilkS', lw_slk, keepouts)
            addVLineWithKeepout(kicad_modt, l_mounth + pck.mounting_hole_diameter / 2, t_slkp, t_slkp + h_slkm,
                                'F.SilkS', lw_slk, keepouts)
    else:
        if pck.mounting_hole_diameter > 0:
            addVLineWithKeepout(kicad_modt, l_mounth - pck.mounting_hole_diameter / 2, t_slkp, t_slkp + h_slkp,
                                'F.SilkS', lw_slk, keepouts)
            addVLineWithKeepout(kicad_modt, l_mounth + pck.mounting_hole_diameter / 2, t_slkp, t_slkp + h_slkp,
                                'F.SilkS', lw_slk, keepouts)
    for p in range(0, len(pads)):
        yl1 = t_slkp + h_slkp
        yl2 = pads[p][1]
        if yl2>yl1:
            addVLineWithKeepout(kicad_modt,pads[p][0], yl1, yl2, 'F.SilkS', lw_slk, keepouts)

    # create courtyard
    kicad_mod.append(
        RectLine(start=[roundCrt(l_crt), roundCrt(t_crt+yshift)], end=[roundCrt(l_crt + w_crt), roundCrt(t_crt + h_crt+yshift)],
                 layer='F.CrtYd', width=lw_crt))
    
    # create pads
    for p in range(0,len(pads)):
        if p==0:
            kicad_modt.append(
                Pad(number=p+1, type=Pad.TYPE_THT, shape=Pad.SHAPE_RECT, at=pads[p], size=padsize, drill=pck.drill,
                    layers=['*.Cu', '*.Mask']))
        else:
            kicad_modt.append(
                Pad(number=p+1, type=Pad.TYPE_THT, shape=Pad.SHAPE_OVAL, at=pads[p], size=padsize, drill=pck.drill,
                    layers=['*.Cu', '*.Mask']))

    
    # add model
    if (has3d):
        kicad_modt.append(
            Model(filename=lib_name + ".3dshapes/" + footprint_name + ".wrl", at=x_3d, scale=s_3d, rotate=r_3d))
    
    # print render tree
    # print(kicad_mod.getRenderTree())
    # print(kicad_mod.getCompleteRenderTree())
    
    # write file
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile(footprint_name + '.kicad_mod')



# horizontal symbols for rectangular transistors
def makeHOR(lib_name, pck, has3d=False, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], lptext="_LargePads", r_3d=[0, 0, 0]):
    padsize = pck.pad
    l_fabp = -pck.pin_offset_x
    t_fabp = -pck.pin_minlength
    if pck.staggered_type >0:
        t_fabp=-pck.staggered_pin_minlength
    w_fabp = pck.plastic[0]
    h_fabp = pck.plastic[1]
    
    w_fabm = pck.metal[0]
    h_fabm = pck.metal[1]
    
    l_mounth = l_fabp + pck.mounting_hole_pos[0]
    t_mounth = t_fabp - pck.mounting_hole_pos[1]

    # calculate pad positions
    pads = []
    yshift = 0
    y1 = 0
    y2 = 0
    maxpiny = 0
    if pck.staggered_type == 1:
        y1 = pck.staggered_rm[1]
        yshift = -pck.staggered_rm[1]
        y2 = 0
        maxpiny = pck.staggered_rm[1]
        if len(pck.staggered_pad) > 0:
            padsize = pck.staggered_pad
    elif pck.staggered_type == 2:
        y1 = 0
        yshift = 0
        y2 = pck.staggered_rm[1]
        maxpiny = pck.staggered_rm[1]
        if len(pck.staggered_pad) > 0:
            padsize = pck.staggered_pad

    y=y1
    x = 0
    for p in range(1, pck.pins + 1):
        if (p % 2) == 1:
            y = y1
        else:
            y = y2
        pads.append([x, y])
        if len(pck.rm_list)>0 and p<=len(pck.rm_list):
            x = x + pck.rm_list[p-1]
        else:
            x = x + pck.rm

    pinwid = (pck.pins - 1) * pck.rm
    if len(pck.rm_list) > 0:
        pinwid = 0
        for rm in pck.rm_list:
            pinwid = pinwid + rm

    l_slkp = l_fabp - slk_offset
    t_slkp = t_fabp + slk_offset
    w_slkp = w_fabp + 2 * slk_offset
    h_slkp = h_fabp + 2 * slk_offset
    w_slkm = w_fabm + 2 * slk_offset
    h_slkm = h_fabm + 2 * slk_offset
    addpad = 0
    l_crt = min(-padsize[0] / 2, l_fabp) - crt_offset
    t_crt = t_fabp - max(h_fabp, h_fabm) - crt_offset
    h_crt = (-t_crt + maxpiny+padsize[1] / 2) + crt_offset
    if len(pck.additional_pin_pad_size) > 0:
        h_crt = h_crt + (pck.additional_pin_pad[1] + pck.additional_pin_pad_size[1] / 2 - h_fabm)
        t_crt = t_crt - (pck.additional_pin_pad[1] + pck.additional_pin_pad_size[1] / 2 - h_fabm)
        addpad = pck.additional_pin_pad_size[0]
        addpadx = l_fabp + pck.additional_pin_pad[0]
        addpady = t_fabp - pck.additional_pin_pad[1]
    w_crt = max(max(max(w_fabp, w_fabm), pinwid + padsize[0]), addpad) + 2 * crt_offset


    txt_x = l_slkp + max(w_slkp, w_slkm) / 2
    txt_t = (t_slkp - max(h_slkm, h_slkp)) - txt_offset
    txt_b = maxpiny+padsize[1] / 2 + txt_offset
    if len(pck.additional_pin_pad_size) > 0:
        txt_t = txt_t - (pck.additional_pin_pad[1] + pck.additional_pin_pad_size[1] / 2 - h_fabm)
    tag_items = ["Horizontal", "RM {0}mm".format(pck.rm)]
    
    footprint_name = pck.name
    if len(pck.additional_pin_pad_size) > 0:
        footprint_name = footprint_name + "-1EP"
    for t in pck.more_packnames:
        footprint_name = footprint_name + "_" + t
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

    kicad_modt = Translation(0, yshift)
    kicad_mod.append(kicad_modt)

    # set general values
    kicad_modt.append(Text(type='reference', text='REF**', at=[txt_x, txt_t], layer='F.SilkS'))
    kicad_modt.append(Text(type='user', text='%R', at=[txt_x, txt_t], layer='F.Fab'))
    kicad_modt.append(Text(type='value', text=footprint_name, at=[txt_x, txt_b], layer='F.Fab'))
    
    # create FAB-layer
    if (h_fabm > 0):
        if len(pck.plastic_angled)>0:
            if len(pck.metal_angled) > 0:
                addRectAngledTopNoBottom(kicad_modt, [l_fabp + pck.metal_offset_x, t_fabp - h_fabp+pck.plastic_angled[1]],
                                 [l_fabp + pck.metal_offset_x + w_fabm, t_fabp - h_fabm], pck.metal_angled, 'F.Fab',
                                 lw_fab)
            else:
                kicad_modt.append(RectLine(start=[l_fabp + pck.metal_offset_x, t_fabp - h_fabp-pck.plastic_angled[1]],
                                           end=[l_fabp + pck.metal_offset_x + w_fabm, t_fabp - h_fabm], layer='F.Fab',
                                           width=lw_fab))
        else:
            if len(pck.metal_angled)>0:
                addRectAngledTop(kicad_modt, [l_fabp + pck.metal_offset_x, t_fabp - h_fabp], [l_fabp + pck.metal_offset_x + w_fabm, t_fabp - h_fabm], pck.metal_angled, 'F.Fab', lw_fab)
            else:
                kicad_modt.append(RectLine(start=[l_fabp + pck.metal_offset_x, t_fabp - h_fabp],
                                      end=[l_fabp + pck.metal_offset_x + w_fabm, t_fabp - h_fabm], layer='F.Fab',
                                      width=lw_fab))
            
    if len(pck.plastic_angled)>0:
         addRectAngledTop(kicad_modt, [l_fabp, t_fabp],
                         [l_fabp + w_fabp, t_fabp - h_fabp], pck.plastic_angled, 'F.Fab', lw_fab)
    else:
        kicad_modt.append(
            RectLine(start=[l_fabp, t_fabp], end=[l_fabp + w_fabp, t_fabp - h_fabp], layer='F.Fab', width=lw_fab))
    if pck.mounting_hole_diameter > 0:
        kicad_modt.append(
            Circle(center=[l_mounth, t_mounth], radius=pck.mounting_hole_diameter / 2, layer='F.Fab', width=lw_fab))
   
    for p in range(0, len(pads)):
        kicad_modt.append(Line(start=[pads[p][0], t_fabp], end=[pads[p][0], pads[p][1]], layer='F.Fab', width=lw_fab))
    
    # create SILKSCREEN-layer
    keepouts = []
    for p in range(0,len(pads)):
        if p==0:
            keepouts=keepouts+addKeepoutRect(pads[p][0],pads[p][1],padsize[0]+2*slk_dist,padsize[1]+2*slk_dist)
        else:
            keepouts=keepouts+addKeepoutRound(pads[p][0],pads[p][1],padsize[0]+2*slk_dist,padsize[1]+2*slk_dist)
    
    if len(pck.additional_pin_pad_size) > 0:
        keepouts.append([addpadx - pck.additional_pin_pad_size[0] / 2 - slk_dist,
                         addpadx + pck.additional_pin_pad_size[0] / 2 + slk_dist,
                         addpady - pck.additional_pin_pad_size[1] / 2 - slk_dist,
                         addpady + pck.additional_pin_pad_size[1] / 2 + slk_dist])
    
    addHLineWithKeepout(kicad_modt, l_slkp, l_slkp + w_slkp, t_slkp, 'F.SilkS', lw_slk, keepouts)
    if h_fabm > 0:
        addHLineWithKeepout(kicad_modt, l_slkp, l_slkp + w_slkp, t_slkp - h_slkm, 'F.SilkS', lw_slk, keepouts)
        addVLineWithKeepout(kicad_modt, l_slkp, t_slkp, t_slkp - h_slkm, 'F.SilkS', lw_slk, keepouts)
        addVLineWithKeepout(kicad_modt, l_slkp + w_slkp, t_slkp, t_slkp - h_slkm, 'F.SilkS', lw_slk, keepouts)
    else:
        addHLineWithKeepout(kicad_modt, l_slkp, l_slkp + w_slkp, t_slkp - h_slkp, 'F.SilkS', lw_slk, keepouts)
        addVLineWithKeepout(kicad_modt, l_slkp, t_slkp, t_slkp - h_slkp, 'F.SilkS', lw_slk, keepouts)
        addVLineWithKeepout(kicad_modt, l_slkp + w_slkp, t_slkp, t_slkp - h_slkp, 'F.SilkS', lw_slk, keepouts)



    for p in range(0, len(pads)):
        addVLineWithKeepout(kicad_modt, pads[p][0], t_slkp, pads[p][1], 'F.SilkS', lw_slk, keepouts)

    # create courtyard
    kicad_mod.append(
        RectLine(start=[roundCrt(l_crt), roundCrt(t_crt+yshift)], end=[roundCrt(l_crt + w_crt), roundCrt(t_crt + h_crt+yshift)],
                 layer='F.CrtYd', width=lw_crt))
    
    # create mounting hole
    if pck.mounting_hole_drill > 0:
        kicad_modt.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_OVAL, at=[l_mounth, t_mounth],
                             size=[pck.mounting_hole_drill, pck.mounting_hole_drill], drill=pck.mounting_hole_drill,
                             layers=['*.Cu', '*.Mask']))
    
    if len(pck.additional_pin_pad_size) > 0:
        kicad_modt.append(Pad(number=pck.pins + 1, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, at=[addpadx, addpady],
                             size=pck.additional_pin_pad_size, drill=0, layers=['F.Cu', 'F.Mask']))
    
    # create pads
    for p in range(0,len(pads)):
        if p==0:
            kicad_modt.append(
                Pad(number=p+1, type=Pad.TYPE_THT, shape=Pad.SHAPE_RECT, at=pads[p], size=padsize, drill=pck.drill,
                    layers=['*.Cu', '*.Mask']))
        else:
            kicad_modt.append(
                Pad(number=p+1, type=Pad.TYPE_THT, shape=Pad.SHAPE_OVAL, at=pads[p], size=padsize, drill=pck.drill,
                    layers=['*.Cu', '*.Mask']))

    
    # add model
    if (has3d):
        kicad_modt.append(
            Model(filename=lib_name + ".3dshapes/" + footprint_name + ".wrl", at=x_3d, scale=s_3d, rotate=r_3d))
    
    # print render tree
    # print(kicad_mod.getRenderTree())
    # print(kicad_mod.getCompleteRenderTree())
    
    # write file
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile(footprint_name + '.kicad_mod')


# vertical, mounted-from-Lowerside symbols for rectangular transistors
def makeVERTLS(lib_name, pck, has3d=False, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], lptext="_LargePads", r_3d=[0, 0, 0]):
    l_fabp = -pck.pin_offset_x
    t_fabp = -pck.pin_offset_z
    w_fabp = pck.plastic[0]
    h_fabp = pck.plastic[2]
    
    w_fabm = pck.metal[0]
    h_fabm = pck.metal[2]
    
    pinwid=(pck.pins - 1) * pck.rm
    if len(pck.rm_list)>0:
        pinwid=0
        for rm in pck.rm_list:
            pinwid=pinwid+rm
    
    l_slkp = l_fabp - slk_offset
    t_slkp = t_fabp - slk_offset
    w_slkp = w_fabp + 2 * slk_offset
    h_slkp = h_fabp + 2 * slk_offset
    w_slkm = w_fabm + 2 * slk_offset
    h_slkm = h_fabm + 2 * slk_offset
    
    l_crt = min(-pck.pad[0] / 2, l_fabp) - crt_offset
    t_crt = min(-pck.pad[1] / 2, t_fabp) - crt_offset
    w_crt = max(max(w_fabp, w_fabm), pinwid + pck.pad[0]) + 2 * crt_offset
    h_crt = max(t_fabp+max(h_fabp, h_fabm) +  crt_offset-t_crt, -t_crt + pck.pad[1] / 2+crt_offset)
    
    l_mounth = l_fabp + pck.mounting_hole_pos[0]
    
    txt_x = l_slkp + max(w_slkp, w_slkm) / 2
    
    tag_items = ["Vertical", "RM {0}mm".format(pck.rm), "mount on lower-side of PCB"]
    
    footprint_name = pck.name
    for t in pck.more_packnames:
        footprint_name = footprint_name + "_" + t
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
    
    kicad_modt = Translation(-pinwid, 0)
    kicad_mod.append(kicad_modt)
    
    # set general values
    kicad_modt.append(Text(type='reference', text='REF**', at=[txt_x, t_slkp - txt_offset], layer='F.SilkS'))
    kicad_modt.append(Text(type='user', text='%R', at=[txt_x, t_slkp - txt_offset], layer='B.Fab'))
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
    x = pinwid
    
    for p in range(1, pck.pins + 1):
        if p == 1:
            keepouts = keepouts + addKeepoutRect(x, 0, pck.pad[0] + 2 * slk_dist, pck.pad[1] + 2 * slk_dist)
        else:
            keepouts = keepouts + addKeepoutRound(x, 0, pck.pad[0] + 2 * slk_dist, pck.pad[1] + 2 * slk_dist)
        if len(pck.rm_list)>0 and p<=len(pck.rm_list):
            x = x - pck.rm_list[p-1]
        else:
            x = x - pck.rm

    
    #for ko in keepouts:
    #    kicad_modt.append(
    #        RectLine(start=[ko[0], ko[2]],
    #                 end=[ko[1], ko[3]],
    #                 layer='F.CrtYd', width=0.01))
    
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
    kicad_mod.append(
        RectLine(start=[roundCrt(l_crt-pinwid), roundCrt(t_crt)], end=[roundCrt(l_crt + w_crt-pinwid), roundCrt(t_crt + h_crt)],
                 layer='B.CrtYd', width=lw_crt))
    
    # create pads
    x = pinwid
    for p in range(1, pck.pins + 1):
        if (p == 1):
            kicad_modt.append(
                Pad(number=p, type=Pad.TYPE_THT, shape=Pad.SHAPE_RECT, at=[x, 0], size=pck.pad, drill=pck.drill,
                    layers=['*.Cu', '*.Mask']))
        else:
            kicad_modt.append(
                Pad(number=p, type=Pad.TYPE_THT, shape=Pad.SHAPE_OVAL, at=[x, 0], size=pck.pad, drill=pck.drill,
                    layers=['*.Cu', '*.Mask']))
        if len(pck.rm_list)>0 and p<=len(pck.rm_list):
            x = x - pck.rm_list[p-1]
        else:
            x = x - pck.rm

    
    # add model
    if (has3d):
        kicad_modt.append(
            Model(filename=lib_name + ".3dshapes/" + footprint_name + ".wrl", at=x_3d, scale=s_3d, rotate=r_3d))
    
    # print render tree
    # print(kicad_mod.getRenderTree())
    # print(kicad_mod.getCompleteRenderTree())
    
    # write file
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile(footprint_name + '.kicad_mod')


# horizontal, mounted-from-Lowerside symbols for rectangular transistors
def makeHORLS(lib_name, pck, has3d=False, x_3d=[0, 0, -2], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], lptext="_LargePads", r_3d=[0, 0, 0]):
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

    pinwid = (pck.pins - 1) * pck.rm
    if len(pck.rm_list) > 0:
        pinwid = 0
        for rm in pck.rm_list:
            pinwid = pinwid + rm
    
    l_crt = min(-pck.pad[0] / 2, l_fabp) - crt_offset
    t_crt = t_fabp - max(h_fabp, h_fabm) - crt_offset
    h_crt = (-t_crt + pck.pad[1] / 2) + crt_offset
    addpad = 0
    if len(pck.additional_pin_pad_size) > 0:
        h_crt = h_crt + (pck.additional_pin_pad[1] + pck.additional_pin_pad_size[1] / 2 - h_fabm)
        t_crt = t_crt - (pck.additional_pin_pad[1] + pck.additional_pin_pad_size[1] / 2 - h_fabm)
        addpad = pck.additional_pin_pad_size[0]
        addpadx = l_fabp + pck.additional_pin_pad[0]
        addpady = t_fabp - pck.additional_pin_pad[1]
    w_crt = max(max(max(w_fabp, w_fabm), pinwid + pck.pad[0]), addpad) + 2 * crt_offset
    
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
    for t in pck.more_packnames:
        footprint_name = footprint_name + "_" + t
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

    kicad_modt=Translation(0,0)#-(pck.pins - 1) * pck.rm,0)
    kicad_mod.append(kicad_modt)

    # set general values
    kicad_modt.append(Text(type='reference', text='REF**', at=[txt_x, txt_t], layer='F.SilkS'))
    kicad_modt.append(Text(type='user', text='%R', at=[txt_x, txt_t], layer='B.Fab'))
    kicad_modt.append(Text(type='value', text=footprint_name, at=[txt_x, txt_b], layer='B.Fab'))
    
    # create FAB-layer

    if (h_fabm > 0):
        if len(pck.metal_angled) > 0:
            addRectAngledTop(kicad_modt, [l_fabp + pck.metal_offset_x, t_fabp - h_fabp],
                             [l_fabp + pck.metal_offset_x + w_fabm, t_fabp - h_fabm], pck.metal_angled, 'B.Fab', lw_fab)
        else:
            kicad_modt.append(RectLine(start=[l_fabp + pck.metal_offset_x, t_fabp - h_fabp],
                                       end=[l_fabp + pck.metal_offset_x + w_fabm, t_fabp - h_fabm], layer='B.Fab',
                                       width=lw_fab))

    if len(pck.plastic_angled) > 0:
        addRectAngledTop(kicad_modt, [l_fabp, t_fabp],
                         [l_fabp + w_fabp, t_fabp - h_fabp], pck.plastic_angled, 'B.Fab', lw_fab)
    else:
        kicad_modt.append(
            RectLine(start=[l_fabp, t_fabp], end=[l_fabp + w_fabp, t_fabp - h_fabp], layer='B.Fab', width=lw_fab))

#    if (h_fabm > 0):
#        kicad_modt.append(RectLine(start=[l_fabp + pck.metal_offset_x, t_fabp - h_fabp],
#                                  end=[l_fabp + pck.metal_offset_x + w_fabm, t_fabp - h_fabm], layer='B.Fab',
#                                  width=lw_fab))
#    kicad_modt.append(
#        RectLine(start=[l_fabp, t_fabp], end=[l_fabp + w_fabp, t_fabp - h_fabp], layer='B.Fab', width=lw_fab))
#    kicad_modt.append(
#        RectLine(start=[l_fabp, t_fabp], end=[l_fabp + w_fabp, t_fabp - h_fabp], layer='B.Fab', width=lw_fab))
    if pck.mounting_hole_diameter > 0:
        kicad_modt.append(
            Circle(center=[l_mounth, t_mounth], radius=pck.mounting_hole_diameter / 2, layer='B.Fab', width=lw_fab))
    x = 0
    for p in range(1, pck.pins + 1):
        kicad_modt.append(Line(start=[x, t_fabp], end=[x, 0], layer='B.Fab', width=lw_fab))
        if len(pck.rm_list)>0 and p<=len(pck.rm_list):
            x = x + pck.rm_list[p-1]
        else:
            x = x + pck.rm

    
    # create SILKSCREEN-layer
    keepouts = []
    x = 0
    for p in range(1, pck.pins + 1):
        if p == 1:
            keepouts = keepouts + addKeepoutRect(x, 0, pck.pad[0] + 2 * slk_dist, pck.pad[1] + 2 * slk_dist)
        else:
            keepouts = keepouts + addKeepoutRound(x, 0, pck.pad[0] + 2 * slk_dist, pck.pad[1] + 2 * slk_dist)
        if len(pck.rm_list)>0 and p<=len(pck.rm_list):
            x = x + pck.rm_list[p-1]
        else:
            x = x + pck.rm

    
    if len(pck.additional_pin_pad_size) > 0:
        keepouts.append([addpadx - pck.additional_pin_pad_size[0] / 2 - slk_dist,
                         addpadx + pck.additional_pin_pad_size[0] / 2 + slk_dist,
                         addpady - pck.additional_pin_pad_size[1] / 2 - slk_dist,
                         addpady + pck.additional_pin_pad_size[1] / 2 + slk_dist])
    
    addHDLineWithKeepout(kicad_modt, l_slkp, 3 * lw_slk, l_slkp + w_slkp, t_slkp, 'F.SilkS', lw_slk, keepouts)
    if h_fabm > 0:
        addHDLineWithKeepout(kicad_modt, l_slkp, 3 * lw_slk, l_slkp + w_slkp, t_slkp - h_slkm, 'F.SilkS', lw_slk, keepouts)
        addHDLineWithKeepout(kicad_modt, l_slkp, 3 * lw_slk, l_slkp + w_slkp, t_fabp - h_fabp, 'F.SilkS', lw_slk, keepouts)
        addVDLineWithKeepout(kicad_modt, l_slkp, t_slkp, 3 * lw_slk, t_slkp - h_slkm, 'F.SilkS', lw_slk, keepouts)
        addVDLineWithKeepout(kicad_modt, l_slkp + w_slkp, t_slkp, 3 * lw_slk, t_slkp - h_slkm, 'F.SilkS', lw_slk, keepouts)
    else:
        addHDLineWithKeepout(kicad_modt, l_slkp, 3 * lw_slk, l_slkp + w_slkp, t_slkp - h_slkp, 'F.SilkS', lw_slk, keepouts)
        addVDLineWithKeepout(kicad_modt, l_slkp, t_slkp, 3 * lw_slk, t_slkp - h_slkp, 'F.SilkS', lw_slk, keepouts)
        addVDLineWithKeepout(kicad_modt, l_slkp + w_slkp, t_slkp, 3 * lw_slk, t_slkp - h_slkp, 'F.SilkS', lw_slk, keepouts)

    x = 0
    for p in range(1, pck.pins + 1):
        addVDLineWithKeepout(kicad_modt, x, t_slkp, 3 * lw_slk, -(pck.pad[1]/2+slk_dist), 'F.SilkS', lw_slk, keepouts)
        if len(pck.rm_list)>0 and p<=len(pck.rm_list):
            x = x + pck.rm_list[p-1]
        else:
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
        if len(pck.rm_list)>0 and p<=len(pck.rm_list):
            x = x + pck.rm_list[p-1]
        else:
            x = x + pck.rm
    
    # add model
    if (has3d):
        kicad_modt.append(
            Model(filename=lib_name + ".3dshapes/" + footprint_name + ".wrl", at=x_3d, scale=s_3d, rotate=r_3d))
    
    # print render tree
    # print(kicad_mod.getRenderTree())
    # print(kicad_mod.getCompleteRenderTree())
    
    # write file
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile(footprint_name + '.kicad_mod')


# horizontal reversed symbols for rectangular transistors
def makeHORREV(lib_name, pck, has3d=False, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], lptext="_LargePads", r_3d=[0, 0, 0]):
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

    pinwid = (pck.pins - 1) * pck.rm
    if len(pck.rm_list) > 0:
        pinwid = 0
        for rm in pck.rm_list:
            pinwid = pinwid + rm

    l_crt = min(-pck.pad[0] / 2, l_fabp) - crt_offset
    t_crt = -pck.pad[1]/2- crt_offset
    w_crt = max(max(w_fabp, w_fabm), pinwid + pck.pad[0]) + 2 * crt_offset
    h_crt = -t_crt + t_fabp+max(h_fabp, h_fabm) +  crt_offset
    
    l_mounth = l_fabp + pck.mounting_hole_pos[0]
    t_mounth = t_fabp + pck.mounting_hole_pos[1]
    
    txt_x = l_slkp + max(w_slkp, w_slkm) / 2
    txt_t = (t_slkp + max(h_slkm, h_slkp)) + txt_offset
    txt_b = -pck.pad[1] / 2 - txt_offset
    
    tag_items = ["Horizontal", "RM {0}mm".format(pck.rm)]
    
    footprint_name = pck.name
    for t in pck.more_packnames:
        footprint_name = footprint_name + "_" + t
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
    kicad_mod.append(Text(type='user', text='%R', at=[txt_x, txt_t], layer='F.Fab'))
    kicad_mod.append(Text(type='value', text=footprint_name, at=[txt_x, txt_b], layer='F.Fab'))
    

    if (h_fabm > 0):
        if len(pck.metal_angled) > 0:
            addRectAngledBottom(kicad_mod, [l_fabp + pck.metal_offset_x, t_fabp + h_fabp],
                                [l_fabp + pck.metal_offset_x + w_fabm, t_fabp + h_fabm], pck.metal_angled, 'F.Fab', lw_fab)
        else:
            kicad_mod.append(RectLine(start=[l_fabp + pck.metal_offset_x, t_fabp + h_fabp],
                                       end=[l_fabp + pck.metal_offset_x + w_fabm, t_fabp + h_fabm], layer='F.Fab',
                                       width=lw_fab))

    if len(pck.plastic_angled) > 0:
        addRectAngledBottom(kicad_mod, [l_fabp, t_fabp],
                            [l_fabp + w_fabp, t_fabp + h_fabp], pck.plastic_angled, 'F.Fab', lw_fab)
    else:
        kicad_mod.append(
            RectLine(start=[l_fabp, t_fabp], end=[l_fabp + w_fabp, t_fabp + h_fabp], layer='F.Fab', width=lw_fab))
 
    if pck.mounting_hole_diameter > 0:
        kicad_mod.append(Circle(center=[l_mounth, t_mounth], radius=pck.mounting_hole_diameter / 2, layer='F.Fab', width=lw_fab))
    x = 0
    for p in range(1, pck.pins + 1):
        kicad_mod.append(Line(start=[x, t_fabp], end=[x, 0], layer='F.Fab', width=lw_fab))
        if len(pck.rm_list)>0 and p<=len(pck.rm_list):
            x = x + pck.rm_list[p-1]
        else:
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
        addHDLineWithKeepout(kicad_mod, l_slkp + pck.metal_offset_x, 10*lw_slk, l_slkp + pck.metal_offset_x + w_slkm, t_slkp + h_slkm, 'F.SilkS', lw_slk, keepouts)
        addVDLineWithKeepout(kicad_mod, l_slkp + pck.metal_offset_x, t_slkp + h_slkp+lw_slk*2, 10 * lw_slk, t_slkp + h_slkm, 'F.SilkS', lw_slk, keepouts)
        addVDLineWithKeepout(kicad_mod, l_slkp + pck.metal_offset_x + w_slkm, t_slkp + h_slkp+lw_slk*2, 10 * lw_slk, t_slkp + h_slkm, 'F.SilkS', lw_slk, keepouts)
    x = 0
    for p in range(1, pck.pins + 1):
        addVLineWithKeepout(kicad_mod, x, t_slkp, pck.pad[1]/2+slk_dist, 'F.SilkS', lw_slk, keepouts)
        if len(pck.rm_list)>0 and p<=len(pck.rm_list):
            x = x + pck.rm_list[p-1]
        else:
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
        if len(pck.rm_list)>0 and p<=len(pck.rm_list):
            x = x + pck.rm_list[p-1]
        else:
            x = x + pck.rm

    
    # add model
    if (has3d):
        kicad_mod.append(
            Model(filename=lib_name + ".3dshapes/" + footprint_name + ".wrl", at=x_3d, scale=s_3d, rotate=r_3d))
    
    # print render tree
    # print(kicad_mod.getRenderTree())
    # print(kicad_mod.getCompleteRenderTree())
    
    # write file
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile(footprint_name + '.kicad_mod')


# horizontal symbols for rectangular transistors
def makeTORound(lib_name, pck, has3d=False, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54], lptext="_LargePads"):
    padsize = pck.pad
    d_fab=pck.diameter_outer
    d_slk=pck.diameter_outer+2*slk_offset

    # calculate pad positions
    pads = []
    yshift = 0
    xshift = 0
    a=pck.pin1_angle
    firstPin=True
    for p in range(1, pck.pins + 1):
        x=pck.pin_circle_diameter/2*math.cos(a/180*math.pi)
        y=pck.pin_circle_diameter/2*math.sin(a/180*math.pi)
        a = a + pck.pin_dangle
        if (len(pck.used_pins)<=0) or ((p-1) in pck.used_pins):
            pads.append([x, y])
            if firstPin:
                xshift=-x
                yshift=-y
                firstPin=False
                

    txt_t = -d_slk/2 - txt_offset
    txt_b = d_slk/2 + txt_offset
    tag_items = []
    
    footprint_name = pck.name
    for t in pck.more_packnames:
        footprint_name = footprint_name + "_" + t
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
    
    kicad_modt = Translation(xshift, yshift)
    kicad_mod.append(kicad_modt)
    
    # set general values
    kicad_modt.append(Text(type='reference', text='REF**', at=[0, txt_t], layer='F.SilkS'))
    kicad_modt.append(Text(type='user', text='%R', at=[0, txt_t], layer='F.Fab'))
    kicad_modt.append(Text(type='value', text=footprint_name, at=[0, txt_b], layer='F.Fab'))
    
    # create FAB-layer
    kicad_modt.append(Circle(center=[0, 0], radius=pck.diameter_inner / 2, layer='F.Fab', width=lw_fab))
    if pck.mark_width > 0 and pck.mark_len > 0:
        a=pck.mark_angle
        da=math.asin(pck.mark_width/d_fab)/math.pi*180
        a1=a+da
        a2=a-da
        x1 = [(pck.diameter_outer / 2) * math.cos(a1 / 180 * math.pi), (pck.diameter_outer / 2) * math.sin(a1 / 180 * math.pi)]
        x3 = [(pck.diameter_outer / 2) * math.cos(a2 / 180 * math.pi), (pck.diameter_outer / 2) * math.sin(a2 / 180 * math.pi)]
        dx1=  (pck.mark_len) * math.cos(a / 180 * math.pi)
        dx2 = (pck.mark_len) * math.sin(a / 180 * math.pi)
        x2 = [x1[0] + dx1, x1[1] + dx2]
        x4 = [x3[0] + dx1, x3[1] + dx2]
        minx=min(x2[0],x4[0])
        miny=min(x2[1],x4[1])
        kicad_modt.append(Arc(center=[0, 0], start=x1, angle=(360-2*da), layer='F.Fab', width=lw_fab))
        kicad_modt.append(Line(start=x1, end=x2, angle=0, layer='F.Fab', width=lw_fab))
        kicad_modt.append(Line(start=x2, end=x4, angle=0, layer='F.Fab', width=lw_fab))
        kicad_modt.append(Line(start=x4, end=x3, angle=0, layer='F.Fab', width=lw_fab))
    else:
        kicad_modt.append(Circle(center=[0, 0], radius=pck.diameter_outer / 2, layer='F.Fab', width=lw_fab))
    if pck.window_diameter>0:
        addCircleLF(kicad_modt, [0,0], pck.window_diameter/2, 'F.Fab', lw_fab, 4*lw_fab)

    
    # create SILKSCREEN-layer
    if pck.mark_width>0 and pck.mark_len>0:
        a=pck.mark_angle
        da=math.asin((pck.mark_width+2*slk_offset)/d_slk)/math.pi*180
        a1=a+da
        a2=a-da
        x1 = [(d_slk / 2) * math.cos(a1 / 180 * math.pi), (d_slk / 2) * math.sin(a1 / 180 * math.pi)]
        x3 = [(d_slk / 2) * math.cos(a2 / 180 * math.pi), (d_slk / 2) * math.sin(a2 / 180 * math.pi)]
        dx1=  (pck.mark_len+slk_offset) * math.cos(a / 180 * math.pi)
        dx2 = (pck.mark_len+slk_offset) * math.sin(a / 180 * math.pi)
        x2 = [x1[0] + dx1, x1[1] + dx2]
        x4 = [x3[0] + dx1, x3[1] + dx2]
        #minx=min(x2[0],x4[0])
        #miny=min(x2[1],x4[1])
        kicad_modt.append(Arc(center=[0, 0], start=x1, angle=(360-2*da), layer='F.SilkS', width=lw_slk))
        kicad_modt.append(Line(start=x1, end=x2, angle=0, layer='F.SilkS', width=lw_slk))
        kicad_modt.append(Line(start=x2, end=x4, angle=0, layer='F.SilkS', width=lw_slk))
        kicad_modt.append(Line(start=x4, end=x3, angle=0, layer='F.SilkS', width=lw_slk))
    else:
        kicad_modt.append(Circle(center=[0, 0], radius=d_slk/2, layer='F.SilkS', width=lw_slk))

    

    if pck.mark_width > 0 and pck.mark_len > 0:
        kicad_mod.append(
            RectLine(start=[roundCrt(xshift+min(minx-crt_offset,-d_fab/2-crt_offset)), roundCrt(yshift+min(miny-crt_offset,-d_fab/2-crt_offset))], end=[roundCrt(xshift+d_fab/2+crt_offset), roundCrt(yshift+d_fab/2+crt_offset)],
                     layer='F.CrtYd', width=lw_crt))
    else:
        kicad_mod.append(Circle(center=[roundCrt(xshift), roundCrt(yshift)], radius=roundCrt(d_fab / 2+crt_offset), layer='F.CrtYd', width=lw_crt))

        
    # create pads
    for p in range(0, len(pads)):
        if p == 0:
            kicad_modt.append(
                Pad(number=p + 1, type=Pad.TYPE_THT, shape=Pad.SHAPE_OVAL, at=pads[p], size=[roundG(padsize[0]*1.3,0.1),padsize[1]], drill=pck.drill,
                    layers=['*.Cu', '*.Mask']))
        else:
            kicad_modt.append(
                Pad(number=p + 1, type=Pad.TYPE_THT, shape=Pad.SHAPE_OVAL, at=pads[p], size=padsize, drill=pck.drill,
                    layers=['*.Cu', '*.Mask']))
    
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


if __name__ == '__main__':
    # make standard packages
    packs = ["TO-264", "TO-247", "TO-218", "TO-251", "TO-126", "TO-220", "TO-280", "TO-262", "SIPAK","TO-3PB"]
    pins = [[2, 3,5], [2, 3,4,5], [2, 3], [2, 3], [2, 3], [2, 3, 4,5], [3], [3], [3],  [3]]
    rms = [ [0, 0,3.81], [0, 0,2.54,2.54], [0, 0], [0, 0], [0, 0], [0, 0, 2.54,1.7], [0], [0], [0],  [0]]
    has3dv = [[True, True, True], [True, True, True, True], [True, True], [True, True], [True, True],
              [True, True, True, True], [True], [True], [True], [True], ]
    has3dh = [ [True, True, True], [True, True, True, True], [True, True], [True, True], [True, True],
              [True, True, True, True], [True], [True], [True], [True], ]
    off3d = [ [[], [], []], [[5.4/25.4,0,0], [5.4/25.4,0,0], [], []], [[5.2/25.4,0,0], [5.2/25.4,0,0]], [[], []], [[], [0.1,0,0]], [[0.1, 0, 0], [0.1, 0, 0], [], [0,0,0]], [[]], [[]], [[]], [[]], ]
    off3dh = [ [[], [], []], [[5.4/25.4,0,0], [5.4/25.4,0,0], [], []], [[5.2/25.4,0,0], [5.2/25.4,0,0]], [[], []], [[0.1,0.2,0], [0.1,0.2,0]], [[0.1, 0, 0], [0.1, 0, 0], [], [0,0,0]], [[]], [[]], [[]], [[]], ]
    off3dls = [[[], [], []], [[], [], [], []], [[], []], [[], []], [[], []], [[0.1, 0, -4 / 25.4], [0.1, 0, -4 / 25.4], [], [0, 0, -4 / 25.4]],
             [[]], [[]], [[]], [[]], ]
    off3dvls = [[[], [], []], [[], [], [], []], [[], []], [[], []], [[], []], [[-0.1, 0, -2 / 25.4], [-0.1, 0, -2 / 25.4], [], [-0, 0, -2 / 25.4]],
             [[]], [[]], [[]], [[]], ]

    scale3d = [ [[], [], []], [[], [1,1,1], [], []], [[], [1,1,1]], [[], []], [[], [1,1,1]], [[], [], [], []], [[]], [[]], [[]], [[]],  ]
    
    #makeVERTLS("TO_SOT_Packages_THT", pack("SOT93", 2, 0, 0, False),False, [0, 0, 0], [0, 0, 0])
    #exit()
    for p in range(0, len(packs)):
        for pidx in range(0, len(pins[p])):
            o3d = [0, 0, 0]
            o3dh = [0, 0, 0]
            o3dls = [0, 0, 0]
            o3dvls = [0, 0, 0]
            s3d = [1 / 2.54, 1 / 2.54, 1 / 2.54]
            r3d=[0,0,0]
            if len(off3d[p][pidx]) > 0:
                o3d = off3d[p][pidx]
            if len(off3dh[p][pidx]) > 0:
                o3dh = off3dh[p][pidx]
                print(o3dh)
            if len(off3dls[p][pidx]) > 0:
                o3dls = off3dls[p][pidx]
            if len(off3dvls[p][pidx]) > 0:
                o3dvls = off3dvls[p][pidx]
            if len(scale3d[p][pidx]) > 0:
                s3d = scale3d[p][pidx]
            r3dr=r3d
            if packs[p]=="TO-220":
                r3dr = [0, 0, 180]
            
            pack_norm = pack(packs[p], pins[p][pidx], rms[p][pidx], 0, False)
            libn = "TO_SOT_Packages_THT"
            makeVERT(libn, pack_norm, has3dv[p][pidx], o3d, s3d, "_LargePads", r3d)
            makeVERTLS(libn, pack_norm, has3dv[p][pidx], o3dvls, s3d, "_LargePads", r3d)
            makeHOR(libn, pack_norm, has3dh[p][pidx], o3dh, s3d, "_LargePads", r3d)
            if (len(pack_norm.additional_pin_pad) <= 0):
                makeHORLS(libn, pack_norm, has3dh[p][pidx], o3dls, s3d, "_LargePads", r3d)
                makeHORREV(libn, pack_norm, has3dh[p][pidx], o3d, s3d, "_LargePads", r3dr)
            

    # make staggered packages
    packs =   [ "TO-220",                 "Multiwatt"]
    pins =    [ [5      ,     7,     9 ], [11,       15,    ]]
    rms =     [ [1.7    ,  1.27,  0.97 ], [1.7,    1.27,    ]]
    has3dv =  [ [True   , True, True ], [False,  True,    ]]
    has3dh =  [ [True   , True, True ], [False,  True,    ]]
    off3d =   [ [[]     , []   , []    ], [[],       [],    ]]
    scale3d = [ [[]     , []   , []    ], [[],  [1,1,1],    ]]
    for p in range(0, len(packs)):
        for pidx in range(0, len(pins[p])):
            o3d = [0, 0, 0]
            s3d = [1 / 2.54, 1 / 2.54, 1 / 2.54]
            if len(off3d[p][pidx]) > 0:
                o3d = off3d[p][pidx]
            if len(scale3d[p][pidx]) > 0:
                s3d = scale3d[p][pidx]

            pack_norm1 = pack(packs[p], pins[p][pidx], rms[p][pidx], 1, False)
            pack_norm2 = pack(packs[p], pins[p][pidx], rms[p][pidx], 2, False)
            libn = "TO_SOT_Packages_THT"
            makeVERT(libn, pack_norm1, has3dv[p][pidx], o3d, s3d)
            makeVERT(libn, pack_norm2, has3dv[p][pidx], o3d, s3d)
            makeHOR(libn, pack_norm1, has3dh[p][pidx], o3d, s3d)
            makeHOR(libn, pack_norm2, has3dh[p][pidx], o3d, s3d)

            
            
                            #pack_largepins=pack(packs[p], pins[p][pidx], rms[p][pidx], True)
            #makeVERT("TO_SOT_Packages_THT", pack_largepins, has3dv[p][pidx], o3d, s3d)
            #makeHOR("TO_SOT_Packages_THT", pack_largepins, has3dh[p][pidx], o3d, s3d)
            #if (len(pack_largepins.additional_pin_pad) <= 0):
            #    makeHORREV("TO_SOT_Packages_THT", pack_largepins, has3dh[p][pidx], o3d, s3d)

    # make round packages
    packs=[]
    modifiers=[]
    pins=[]
    has3d=[]
    off3d=[]
    scale3d=[]

    packs.append("TO-5")
    modifiers.append(["", "Window"])
    pins.append([2, 3, 4, 6, 8, 10])
    has3d.append([True, True, True, True, True, True])
    off3d.append([])
    scale3d.append([])

    packs.append("TO-5_PD5.08")
    modifiers.append(["", "Window"])
    pins.append([8])
    has3d.append([True])
    off3d.append([])
    scale3d.append([])

    packs.append("TO-8")
    modifiers.append(["", "Window"])
    pins.append([2, 3])
    has3d.append([True, True])
    off3d.append([])
    scale3d.append([])

    packs.append("TO-11")
    modifiers.append(["", "Window"])
    pins.append([2, 3])
    has3d.append([True, True])
    off3d.append([])
    scale3d.append([])

    packs.append("TO-12")
    modifiers.append(["", "Window"])
    pins.append([4])
    has3d.append([True])
    off3d.append([[]])
    scale3d.append([[]])

    packs.append("TO-17")
    modifiers.append(["", "Window"])
    pins.append([4])
    has3d.append([True])
    off3d.append([[]])
    scale3d.append([[]])

    packs.append("TO-18")
    modifiers.append(["", "Window", "Lens"])
    pins.append([2, 3, 4])
    has3d.append([True, True, True])
    off3d.append([])
    scale3d.append([])

    packs.append("TO-33")
    modifiers.append(["", "Window"])
    pins.append([4])
    has3d.append([True])
    off3d.append([[]])
    scale3d.append([[]])

    packs.append("TO-38")
    modifiers.append(["", "Window"])
    pins.append([2, 3])
    has3d.append([True, True])
    off3d.append([])
    scale3d.append([])

    packs.append("TO-39")
    modifiers.append(["", "Window"])
    pins.append([2, 3, 4, 6, 8, 10])
    has3d.append([True, True, True, True, True, True])
    off3d.append([])
    scale3d.append([])

    packs.append("TO-46")
    modifiers.append(["", "Window"])
    pins.append([2, 3, 4])
    has3d.append([True, True, True])
    off3d.append([])
    scale3d.append([])

    packs.append("TO-52")
    modifiers.append(["", "Window"])
    pins.append([2, 3])
    has3d.append([True, True])
    off3d.append([])
    scale3d.append([])

    packs.append("TO-72")
    modifiers.append(["", "Window"])
    pins.append([4])
    has3d.append([True])
    off3d.append([[]])
    scale3d.append([[]])

    packs.append("TO-78")
    modifiers.append(["", "Window"])
    pins.append([6, 8, 10])
    has3d.append([True, True, True])
    off3d.append([])
    scale3d.append([])

    packs.append("TO-99")
    modifiers.append(["", "Window"])
    pins.append([6,8])
    has3d.append([True,True])
    off3d.append([])
    scale3d.append([])



    for p in range(0, len(packs)):
        mi=0
        for m in modifiers[p]:
            for pidx in range(0, len(pins[p])):

                o3d = [0, 0, 0]
                s3d = [1 / 2.54, 1 / 2.54, 1 / 2.54]
                if len(off3d[p])>0:
                    if len(off3d[p][pidx]) > 0:
                        o3d = off3d[p][pidx]
                if len(scale3d[p])>0:
                    if len(scale3d[p][pidx]) > 0:
                        s3d = scale3d[p][pidx]
                
                pack = pack_round(packs[p], pins[p][pidx], m, False)
                libn = "TO_SOT_Packages_THT"
                makeTORound(libn, pack, has3d[p][pidx], o3d, s3d)
            mi=mi+1
