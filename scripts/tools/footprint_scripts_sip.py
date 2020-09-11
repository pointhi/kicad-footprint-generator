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


def makeSIPVertical(pins, rm, ddrill, pad, package_size, left_offset, top_offset, footprint_name, description, tags, lib_name, missing_pins=[]):
    padx=pad[0]
    pady=pad[1]
    
    w_fab=package_size[0]
    h_fab=package_size[1]
    l_fab=-left_offset
    t_fab=-top_offset
    
    h_slk = h_fab + 2 * slk_offset
    w_slk = w_fab + 2 * slk_offset
    l_slk = l_fab - slk_offset
    t_slk = t_fab - slk_offset
    w_crt = w_fab + 2 * crt_offset
    h_crt = h_fab + 2 * crt_offset
    l_crt = min(l_fab, -padx / 2) - crt_offset
    t_crt = t_fab  - crt_offset
    if (-pady/2<t_fab):
        t_crt=-(pady / 2) - crt_offset
        h_crt=h_fab+(pady/2-math.fabs(t_fab))+2*crt_offset
    if (pady/2>t_fab+h_fab):
        t_crt = t_fab  - crt_offset
        h_crt=h_fab+(pady/2-math.fabs(t_fab))+2*crt_offset
    
    
    print(footprint_name)
    
    # init kicad footprint
    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription(description)
    kicad_mod.setTags(tags)
   
    # create pads
    keepout=[]
    if not 1 in missing_pins:
        kicad_mod.append(Pad(number=1, type=Pad.TYPE_THT, shape=Pad.SHAPE_RECT, at=[0, 0], size=pad, drill=ddrill,
                             layers=['*.Cu', '*.Mask']))
        keepout=keepout+addKeepoutRect(0,0,pad[0]+2*min_pad_distance+2*lw_slk, pad[1]+2*min_pad_distance+2*lw_slk)
    for x in range(2, pins + 1):
        if not x in missing_pins:
            kicad_mod.append(Pad(number=x, type=Pad.TYPE_THT, shape=Pad.SHAPE_OVAL, at=[(x - 1) * rm, 0], size=pad,
                                 drill=ddrill, layers=['*.Cu', '*.Mask']))
            if (padx/pady)<1.05 and (padx/pady)>.95:
                keepout=keepout+addKeepoutRect((x - 1) * rm,0,pad[0]+2*min_pad_distance+2*lw_slk, pad[1]+2*min_pad_distance+2*lw_slk)
            else:
                keepout=keepout+addKeepoutRound((x - 1) * rm,0,pad[0]+2*min_pad_distance+2*lw_slk, pad[1]+2*min_pad_distance+2*lw_slk)
    # set general values
    kicad_mod.append(Text(type='reference', text='REF**', at=[(pins-1) / 2 * rm, min(-pady/2,t_slk) - txt_offset], layer='F.SilkS'))
    kicad_mod.append(Text(type='user', text='%R', at=[(pins-1) / 2 * rm, t_fab +h_fab/2], layer='F.Fab'))
    kicad_mod.append(Text(type='value', text=footprint_name, at=[(pins-1) / 2 * rm, t_fab+h_fab + txt_offset], layer='F.Fab'))
    
    # create FAB-layer
    pin1TL=True
    pin1size=min(1, h_fab/2)
    if top_offset>h_fab/2:
        bevelRectBL(kicad_mod, x=[l_fab, t_fab], size=[w_fab, h_fab], bevel_size=pin1size, layer='F.Fab', width=lw_fab)
        pin1TL=False
    else:
        bevelRectTL(kicad_mod, x=[l_fab, t_fab], size=[w_fab, h_fab], bevel_size=pin1size, layer='F.Fab', width=lw_fab)
        pin1TL=True
    
    # create SILKSCREEN-layer
    addRectWithKeepout(kicad_mod, l_slk, t_slk, w_slk, h_slk, keepouts=keepout, layer='F.SilkS', width=lw_slk)
    if pin1TL:
        addPolyLineWithKeepout(kicad_mod, [
                                            [l_slk-2*lw_slk, t_slk+pin1size], 
                                            [l_slk-2*lw_slk, t_slk-2*lw_slk], 
                                            [l_slk+pin1size, t_slk-2*lw_slk], 
                                            ], keepouts=keepout, layer='F.SilkS', width=lw_slk)
    else:
        addPolyLineWithKeepout(kicad_mod, [
                                            [l_slk-2*lw_slk, t_slk+h_slk-pin1size], 
                                            [l_slk-2*lw_slk, t_slk+h_slk+2*lw_slk], 
                                            [l_slk+pin1size, t_slk+h_slk+2*lw_slk], 
                                            ], keepouts=keepout, layer='F.SilkS', width=lw_slk)
    
    # create courtyard
    kicad_mod.append(
        RectLine(start=[roundCrt(l_crt), roundCrt(t_crt)], end=[roundCrt(l_crt + w_crt), roundCrt(t_crt + h_crt)],
                 layer='F.CrtYd', width=lw_crt))
     
    # add model
    kicad_mod.append(Model(filename="${KISYS3DMOD}/"+lib_name + ".3dshapes/" + footprint_name + ".wrl",
                           at=[0, 0, 0], scale=[1,1,1], rotate=[0, 0, 0]))
    
    # write file
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile(footprint_name + '.kicad_mod')

    


def makeSIPHorizontal(pins, rm, ddrill, pad, package_size, left_offset, pin_bottom_offset, footprint_name, description, tags, lib_name, missing_pins=[]):
    padx=pad[0]
    pady=pad[1]
    
    w_fab=package_size[0]
    h_fab=package_size[2]
    l_fab=-left_offset
    t_fab=-pin_bottom_offset-h_fab
    
    h_slk = h_fab + 2 * slk_offset
    w_slk = w_fab + 2 * slk_offset
    l_slk = l_fab - slk_offset
    t_slk = t_fab-slk_offset
    
    w_crt = w_fab + 2 * crt_offset
    h_crt = h_fab+pin_bottom_offset+pad[1]/2 + 2 * crt_offset
    l_crt = min(l_fab, -padx / 2) - crt_offset
    t_crt = t_fab  - crt_offset

    # Pin 1 maker
    l_pin1 = l_slk + left_offset - padx / 2 - 2 * lw_slk
    h_pin1 = pin_bottom_offset + pady / 2 - lw_slk
    
    print(footprint_name)
    
    # init kicad footprint
    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription(description)
    kicad_mod.setTags(tags)
   
    # create pads
    keepout=[]
    if not 1 in missing_pins:
        kicad_mod.append(Pad(number=1, type=Pad.TYPE_THT, shape=Pad.SHAPE_RECT, at=[0, 0], size=pad, drill=ddrill,
                             layers=['*.Cu', '*.Mask']))
        keepout=keepout+addKeepoutRect(0,0,pad[0]+2*min_pad_distance+2*lw_slk, pad[1]+2*min_pad_distance+2*lw_slk)
        kicad_mod.append(Line(start=[-lw_fab/2, 0], end=[-lw_fab/2,-pin_bottom_offset], layer='F.Fab', width=lw_fab))
        kicad_mod.append(Line(start=[lw_fab/2, 0], end=[lw_fab/2,-pin_bottom_offset], layer='F.Fab', width=lw_fab))
    for x in range(2, pins + 1):
        if not x in missing_pins:
            kicad_mod.append(Pad(number=x, type=Pad.TYPE_THT, shape=Pad.SHAPE_OVAL, at=[(x - 1) * rm, 0], size=pad,
                                 drill=ddrill, layers=['*.Cu', '*.Mask']))
            kicad_mod.append(Line(start=[(x - 1) * rm-lw_fab/2, 0], end=[(x - 1) * rm-lw_fab/2,-pin_bottom_offset], layer='F.Fab', width=lw_fab))
            kicad_mod.append(Line(start=[(x - 1) * rm+lw_fab/2, 0], end=[(x - 1) * rm+lw_fab/2,-pin_bottom_offset], layer='F.Fab', width=lw_fab))
            if (padx/pady)<1.05 and (padx/pady)>.95:
                keepout=keepout+addKeepoutRect((x - 1) * rm,0,pad[0]+2*min_pad_distance+2*lw_slk, pad[1]+2*min_pad_distance+2*lw_slk)
            else:
                keepout=keepout+addKeepoutRound((x - 1) * rm,0,pad[0]+2*min_pad_distance+2*lw_slk, pad[1]+2*min_pad_distance+2*lw_slk)
    # set general values
    kicad_mod.append(Text(type='reference', text='REF**', at=[(pins-1) / 2 * rm, min(-pady/2,t_slk) - txt_offset], layer='F.SilkS'))
    kicad_mod.append(Text(type='user', text='%R', at=[(pins-1) / 2 * rm, t_fab +h_fab/2], layer='F.Fab'))
    kicad_mod.append(Text(type='value', text=footprint_name, at=[(pins-1) / 2 * rm, pady/2 + txt_offset], layer='F.Fab'))
    
    # create FAB-layer
    pin1size=min(1, h_fab/2)
    bevelRectBL(kicad_mod, x=[l_fab, t_fab], size=[w_fab, h_fab], bevel_size=pin1size, layer='F.Fab', width=lw_fab)
    
    # create SILKSCREEN-layer
    addRectWithKeepout(kicad_mod, l_slk, t_slk, w_slk, h_slk, keepouts=keepout, layer='F.SilkS', width=lw_slk)
    addPolyLineWithKeepout(kicad_mod, [
                                        [l_pin1, t_slk + h_slk],
                                        [l_pin1, t_slk + h_slk + h_pin1]
                                        ], layer='F.SilkS', width=lw_slk)

    # create courtyard
    kicad_mod.append(
        RectLine(start=[roundCrt(l_crt), roundCrt(t_crt)], end=[roundCrt(l_crt + w_crt), roundCrt(t_crt + h_crt)],
                 layer='F.CrtYd', width=lw_crt))
     
    # add model
    kicad_mod.append(Model(filename="${KISYS3DMOD}/"+lib_name + ".3dshapes/" + footprint_name + ".wrl",
                           at=[0, 0, 0], scale=[1,1,1], rotate=[0, 0, 0]))
    
    # write file
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile(footprint_name + '.kicad_mod')


def makeResistorSIP(pins, footprint_name, description):
    rm = 2.54
    h = 2.5
    leftw = 1.29
    ddrill = 0.8
    padx = 1.6
    pady = 1.6
    
    w = (pins - 1) * rm + 2 * leftw
    left = -leftw
    top = -h / 2
    h_slk = max(h, pady) + 2 * slk_offset
    w_slk = w + 2 * slk_offset
    l_slk = -leftw - slk_offset
    r_slk = l_slk + w_slk
    t_slk = -h_slk / 2
    w_crt = w_slk + 2 * crt_offset
    h_crt = max(h_slk, pady) + 2 * crt_offset
    l_crt = min(l_slk, -padx / 2) - crt_offset
    t_crt = min(t_slk, -pady / 2) - crt_offset
    
    lib_name = "Resistors_ThroughHole"
    
    print(footprint_name)
    
    # init kicad footprint
    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription(description)
    kicad_mod.setTags("R")
    
    # set general values
    kicad_mod.append(Text(type='reference', text='REF**', at=[pins / 2 * rm, t_slk - txt_offset], layer='F.SilkS'))
    kicad_mod.append(Text(type='value', text=footprint_name, at=[pins / 2 * rm, h_slk / 2 + txt_offset], layer='F.Fab'))
    
    # create FAB-layer
    kicad_mod.append(RectLine(start=[left, top], end=[left + w, top + h], layer='F.Fab', width=lw_fab))
    kicad_mod.append(Line(start=[0.5 * rm, top], end=[0.5 * rm, top + h], layer='F.Fab', width=lw_fab))
    
    # create SILKSCREEN-layer
    kicad_mod.append(RectLine(start=[l_slk, t_slk], end=[l_slk + w_slk, t_slk + h_slk], layer='F.SilkS'))
    kicad_mod.append(Line(start=[0.5 * rm, t_slk], end=[0.5 * rm, t_slk + h_slk], layer='F.SilkS'))
    
    # create courtyard
    kicad_mod.append(
        RectLine(start=[roundCrt(l_crt), roundCrt(t_crt)], end=[roundCrt(l_crt + w_crt), roundCrt(t_crt + h_crt)],
                 layer='F.CrtYd', width=lw_crt))
    
    # create pads
    kicad_mod.append(Pad(number=1, type=Pad.TYPE_THT, shape=Pad.SHAPE_RECT, at=[0, 0], size=[padx, pady], drill=ddrill,
                         layers=['*.Cu', '*.Mask']))
    for x in range(2, pins + 1):
        kicad_mod.append(Pad(number=x, type=Pad.TYPE_THT, shape=Pad.SHAPE_OVAL, at=[(x - 1) * rm, 0], size=[padx, pady],
                             drill=ddrill, layers=['*.Cu', '*.Mask']))
    
    # add model
    kicad_mod.append(Model(filename="${KISYS3DMOD}/"+lib_name + ".3dshapes/" + footprint_name + ".wrl",
                           at=[0, 0, 0], scale=[1 / 2.54, 1 / 2.54, 1 / 2.54], rotate=[0, 0, 0]))
    
    # print render tree
    # print(kicad_mod.getRenderTree())
    # print(kicad_mod.getCompleteRenderTree())
    
    # write file
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile(footprint_name + '.kicad_mod')
