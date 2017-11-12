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
from math import sqrt

crt_offset = 0.5 # different for connectors

#
#  +----------------------------------------+                      ^                  
#  |       H           H           H        | ^                    |                  
#  |                                        | |                    |                  
#  |      OOO         OOO         OOO       | |secondHoleOffset    | package_height  
#  |     OOOOO       OOOOO       OOOOO      | v                    |                  ^
#  |      OOO         OOO         OOO       |                      |                  |
#  +----------------------------------------+ ^                    |                  | leftbottom_offset
#  |                                        | | bevel_height       |                  |
#  +----------------------------------------+ v                    v                  v
#          <--- rm ---->
#  <------>leftbottom_offset[0]     <------->leftbottom_offset[2] (or leftbottom_offset[0]  if len(leftbottom_offset)==2)
#
#
#
def makeTerminalBlockStd(footprint_name, pins, rm, package_height, leftbottom_offset, ddrill, pad, screw_diameter, bevel_height, slit_screw=True, screw_pin_offset=[0,0], secondHoleDiameter=0, secondHoleOffset=[0,0], thirdHoleDiameter=0, thirdHoleOffset=[0,0], fourthHoleDiameter=0, fourthHoleOffset=[0,0],secondDrillDiameter=0,secondDrillOffset=[0,0],secondDrillPad=[0,0],nibbleSize=[],nibblePos=[], fabref_offset=[0,0],
                        tags_additional=[], lib_name="${{KISYS3DMOD}}/Connectors_Terminal_Blocks", classname="Connectors_Terminal_Blocks", classname_description="terminal block", webpage="", script_generated_note=""):
                        
    package_size=[2*leftbottom_offset[0]+(pins-1)*rm, package_height];
    if len(leftbottom_offset)==3:
        package_size=[leftbottom_offset[0]+leftbottom_offset[2]+(pins-1)*rm, package_height];
    
    h_fab = package_size[1]
    w_fab = package_size[0]
    l_fab = -leftbottom_offset[0]
    t_fab = -(h_fab-leftbottom_offset[1])
    
    h_slk = h_fab + 2 * slk_offset
    w_slk = w_fab + 2 * slk_offset
    l_slk = l_fab - slk_offset
    t_slk = t_fab - slk_offset
    
    h_crt = h_fab + 2 * crt_offset
    w_crt = w_fab + 2 * crt_offset
    l_crt = l_fab - crt_offset
    t_crt = t_fab - crt_offset
    
    
    text_size = w_fab*0.6
    fab_text_size_max = 1.0
    if text_size < fab_text_size_min:
        text_size = fab_text_size_min
    elif text_size > fab_text_size_max:
        text_size = fab_text_size_max
    text_size = round(text_size, 2)
    text_size = [text_size,text_size]
    text_t = text_size[0] * 0.15
    
    
    description = "{2}, {0} pins, pitch {1:02}mm, size {3}x{4}mm^2, drill diamater {5}mm, pad diameter {6}mm, see {7}".format(pins, rm,classname_description, package_size[0], package_size[1], ddrill, max(pad), webpage)
    tags = "THT {2} pitch {1:02}mm size {3}x{4}mm^2 drill {5}mm pad {6}mm".format(pins, rm,classname_description, package_size[0], package_size[1], ddrill, max(pad))
    
    if len(script_generated_note)>0:
        description=description+", "+script_generated_note
    
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
    kicad_modg = Translation(offset[0], offset[1])
    kicad_mod.append(kicad_modg)
    
    # set general values
    kicad_modg.append(Text(type='reference', text='REF**', at=[l_fab+w_fab/2, t_slk - txt_offset], layer='F.SilkS'))
    if (type(fabref_offset) in (tuple, list)):
        kicad_modg.append(Text(type='user', text='%R', at=[l_fab+w_fab/2+fabref_offset[0], t_fab+h_fab/2+fabref_offset[1]], layer='F.Fab', size=text_size ,thickness=text_t))
    else:
        kicad_modg.append(Text(type='user', text='%R', at=[l_fab+w_fab/2,  t_slk - txt_offset], layer='F.Fab', size=text_size ,thickness=text_t))
    kicad_modg.append(Text(type='value', text=footprint_name, at=[l_fab+w_fab/2, t_slk + h_slk + txt_offset], layer='F.Fab'))
    
    
    # create pads
    p1 = int(1)
    x1 = 0
    y1 = 0 
     
    pad_type = Pad.TYPE_THT 
    extradrill1_type = Pad.TYPE_NPTH
    if secondDrillPad[0]>0:
        extradrill1_type = Pad.TYPE_THT
    pad_shape1 = Pad.SHAPE_RECT 
    pad_shapeother = Pad.SHAPE_CIRCLE 
    if secondDrillPad[0]!=secondDrillPad[1]:
        pad_shapeother = Pad.SHAPE_OVAL 
    pad_layers = Pad.LAYERS_THT
    keepouts=[];
    for p in range(1, pins + 1): 
        pextra=0
        if secondDrillPad[0]>0:
            pextra=p
        if p == 1: 
            kicad_modg.append(Pad(number=p, type=pad_type, shape=pad_shape1, at=[x1, y1], size=pad, drill=ddrill, layers=pad_layers)) 
            keepouts=keepouts+addKeepoutRect(x1, y1, pad[0]+8*slk_offset, pad[1]+8*slk_offset)
            if secondDrillDiameter>0:
                kicad_modg.append(Pad(number=p, type=extradrill1_type, shape=pad_shape1, at=[x1+secondDrillOffset[0], y1+secondDrillOffset[1]], size=secondDrillPad, drill=secondDrillDiameter, layers=pad_layers)) 
                keepouts=keepouts+addKeepoutRect(x1+secondDrillOffset[0], y1+secondDrillOffset[1], max(secondDrillPad[0],secondDrillDiameter)+8*slk_offset, max(secondDrillPad[0],secondDrillDiameter)+8*slk_offset)
        else:
            kicad_modg.append(Pad(number=p, type=pad_type, shape=pad_shapeother, at=[x1, y1], size=pad, drill=ddrill, layers=pad_layers))
            if secondDrillPad[0]!=secondDrillPad[1]:
                keepouts=keepouts+addKeepoutRect(x1, y1, pad[0]+8*slk_offset, pad[1]+8*slk_offset)
            else:
                keepouts=keepouts+addKeepoutRound(x1, y1, pad[0]+8*slk_offset, pad[0]+8*slk_offset)
            if secondDrillDiameter>0:
                kicad_modg.append(Pad(number=p, type=extradrill1_type, shape=pad_shapeother, at=[x1+secondDrillOffset[0], y1+secondDrillOffset[1]], size=secondDrillPad, drill=secondDrillDiameter, layers=pad_layers)) 
                keepouts=keepouts+addKeepoutRect(x1+secondDrillOffset[0], y1+secondDrillOffset[1], max(secondDrillPad[0],secondDrillDiameter)+8*slk_offset, max(secondDrillPad[0],secondDrillDiameter)+8*slk_offset)
        
        x1=x1+rm
    
    # create Body
    chamfer = min(h_fab/4, 2, bevel_height[0])
    bevelRectBL(kicad_modg,  [l_fab,t_fab], [w_fab,h_fab], 'F.Fab', lw_fab, bevel_size=chamfer)
    for bh in bevel_height:
        kicad_modg.append(Line(start=[l_fab, t_fab + h_fab-bh], end=[l_fab+w_fab, t_fab + h_fab-bh], layer='F.Fab', width=lw_fab))
        addHLineWithKeepout(kicad_modg,l_slk, l_slk+w_slk, t_fab + h_fab-bh, layer='F.SilkS', width=lw_slk, keepouts=keepouts)
    addRectWithKeepout(kicad_modg, l_slk, t_slk, w_slk, h_slk, layer='F.SilkS', width=lw_slk, keepouts=keepouts)
    # screws + other repeated features
    if screw_diameter>0:
        for p in range(1,pins+1):
            if screw_diameter>0:
                if slit_screw:
                    addSlitScrew(kicad_modg, (p-1)*rm+screw_pin_offset[0], 0+screw_pin_offset[1], screw_diameter/2, 'F.Fab', lw_fab, roun=0.001)
                    addSlitScrewWithKeepouts(kicad_modg, (p-1)*rm+screw_pin_offset[0], 0+screw_pin_offset[1], screw_diameter/2+3*slk_offset, 'F.SilkS', lw_slk, keepouts, roun=0.001)
                else:
                    addCrossScrew(kicad_modg, (p-1)*rm+screw_pin_offset[0], 0+screw_pin_offset[1], screw_diameter/2, 'F.Fab', lw_fab, roun=0.001)
                    addCrossScrewWithKeepouts(kicad_modg, (p-1)*rm+screw_pin_offset[0], 0+screw_pin_offset[1], screw_diameter/2+3*slk_offset, 'F.SilkS', lw_slk, keepouts, roun=0.001)
                
            if not (type(secondHoleDiameter) in (tuple, list)) and secondHoleDiameter>0 and (p-1)*rm+secondHoleOffset[0]<l_fab+w_fab:
                kicad_modg.append(Circle(center=[(p-1)*rm+secondHoleOffset[0], 0+secondHoleOffset[1]], radius=secondHoleDiameter/2, layer='F.Fab', width=lw_fab))
                addCircleWithKeepout(kicad_modg, (p-1)*rm+secondHoleOffset[0], 0+secondHoleOffset[1], secondHoleDiameter/2, 'F.SilkS', lw_slk, keepouts)
            if not (type(thirdHoleDiameter) in (tuple, list)) and thirdHoleDiameter>0 and (p-1)*rm+thirdHoleOffset[0]<l_fab+w_fab:
                kicad_modg.append(Circle(center=[(p-1)*rm+thirdHoleOffset[0], 0+thirdHoleOffset[1]], radius=thirdHoleDiameter/2, layer='F.Fab', width=lw_fab))
                addCircleWithKeepout(kicad_modg, (p-1)*rm+thirdHoleOffset[0], 0+thirdHoleOffset[1], thirdHoleDiameter/2, 'F.SilkS', lw_slk, keepouts)
            if not (type(fourthHoleDiameter) in (tuple, list)) and fourthHoleDiameter>0 and (p-1)*rm+fourthHoleOffset[0]<l_fab+w_fab:
                kicad_modg.append(Circle(center=[(p-1)*rm+fourthHoleOffset[0], 0+fourthHoleOffset[1]], radius=fourthHoleDiameter/2, layer='F.Fab', width=lw_fab))
                addCircleWithKeepout(kicad_modg, (p-1)*rm+fourthHoleOffset[0], 0+fourthHoleOffset[1], fourthHoleDiameter/2, 'F.SilkS', lw_slk, keepouts)
            if (type(secondHoleDiameter) in (tuple, list)) and (p-1)*rm+secondHoleOffset[0]<l_fab+w_fab:
                kicad_modg.append(RectLine(start=[(p-1)*rm+secondHoleOffset[0]-secondHoleDiameter[0]/2, 0+secondHoleOffset[1]-secondHoleDiameter[1]/2], end=[(p-1)*rm+secondHoleOffset[0]+secondHoleDiameter[0]/2, 0+secondHoleOffset[1]+secondHoleDiameter[1]/2], layer='F.Fab', width=lw_fab))
                addRectWithKeepout(kicad_modg, (p-1)*rm+secondHoleOffset[0]-secondHoleDiameter[0]/2, 0+secondHoleOffset[1]-secondHoleDiameter[1]/2, secondHoleDiameter[0],secondHoleDiameter[1], 'F.SilkS', lw_slk, keepouts)
            if (type(thirdHoleDiameter) in (tuple, list)) and (p-1)*rm+thirdHoleOffset[0]<l_fab+w_fab:
                kicad_modg.append(RectLine(start=[(p-1)*rm+thirdHoleOffset[0]-thirdHoleDiameter[0]/2, 0+thirdHoleOffset[1]-thirdHoleDiameter[1]/2], end=[(p-1)*rm+thirdHoleOffset[0]+thirdHoleDiameter[0]/2, 0+thirdHoleOffset[1]+thirdHoleDiameter[1]/2], layer='F.Fab', width=lw_fab))
                addRectWithKeepout(kicad_modg, (p-1)*rm+thirdHoleOffset[0]-thirdHoleDiameter[0]/2, 0+thirdHoleOffset[1]-thirdHoleDiameter[1]/2, thirdHoleDiameter[0],thirdHoleDiameter[1], 'F.SilkS', lw_slk, keepouts)
            if (type(fourthHoleDiameter) in (tuple, list)) and (p-1)*rm+fourthHoleOffset[0]<l_fab+w_fab:
                kicad_modg.append(RectLine(start=[(p-1)*rm+fourthHoleOffset[0]-fourthHoleDiameter[0]/2, 0+fourthHoleOffset[1]-fourthHoleDiameter[1]/2], end=[(p-1)*rm+fourthHoleOffset[0]+fourthHoleDiameter[0]/2, 0+fourthHoleOffset[1]+fourthHoleDiameter[1]/2], layer='F.Fab', width=lw_fab))
                addRectWithKeepout(kicad_modg, (p-1)*rm+fourthHoleOffset[0]-fourthHoleDiameter[0]/2, 0+fourthHoleOffset[1]-fourthHoleDiameter[1]/2, fourthHoleDiameter[0],fourthHoleDiameter[1], 'F.SilkS', lw_slk, keepouts)
    
    #nibble
    if len(nibbleSize)==2 and len(nibblePos)==2:
        kicad_modg.append(RectLine(start=[l_fab+nibblePos[0], t_fab+nibblePos[1]], end=[l_fab+nibblePos[0]+nibbleSize[0], t_fab+nibblePos[1]+nibbleSize[1]], layer='F.Fab', width=lw_fab))
        addRectWithKeepout(kicad_modg, l_fab+nibblePos[0]-slk_offset, t_fab+nibblePos[1]-slk_offset, nibbleSize[0],nibbleSize[1]+2*slk_offset, 'F.SilkS', lw_slk, keepouts)
        
                
                
    # create SILKSCREEN-pin1-marker
    kicad_modg.append(Line(start=[l_slk-2*lw_slk, t_slk + h_slk-chamfer], end=[l_slk-2*lw_slk, t_slk + h_slk+2*lw_slk], layer='F.SilkS', width=lw_slk))
    kicad_modg.append(Line(start=[l_slk-2*lw_slk, t_slk + h_slk+2*lw_slk], end=[l_slk-2*lw_slk+chamfer, t_slk + h_slk+2*lw_slk], layer='F.SilkS', width=lw_slk))
    
    # create courtyard
    kicad_mod.append(RectLine(start=[roundCrt(l_crt + offset[0]), roundCrt(t_crt + offset[1])],
                              end=[roundCrt(l_crt + offset[0] + w_crt), roundCrt(t_crt + offset[1] + h_crt)],
                              layer='F.CrtYd', width=lw_crt))
    
    
    # add model
    kicad_modg.append(
        Model(filename=lib_name + ".3dshapes/" + footprint_name + ".wrl", at=[0,0,0], scale=[1,1,1], rotate=[0,0,0]))
    
    #debug_draw_keepouts(kicad_modg,keepouts)
   
    # write file
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile(footprint_name + '.kicad_mod')


#
#  +----------------------------------------+                      ^                  
#  |       H           H           H        | ^                    |                  
#  |  -----------                           | |                    |                                       ^
#  |  |   OOO   |     OOO         OOO       | |secondHoleOffset    | package_height                        |
#  |  |  OOOOO  |    OOOOO       OOOOO      | v                    |                  ^                    | opening[1]
#  |  |   OOO   |     OOO         OOO       |                      |                  |                    |
#  +----------------------------------------+ ^                    |                  | leftbottom_offset  x
#  |                                        | | bevel_height       |                  |                    | opening_yoffset
#  +----------------------------------------+ v                    v                  v                    v
#          <--- rm ---->
#  <------>leftbottom_offset[0]     <------->leftbottom_offset[2] (or leftbottom_offset[0]  if len(leftbottom_offset)==2)
#     <---------> opening[0]
#
#
def makeTerminalBlockVertical(footprint_name, pins, rm, package_height, leftbottom_offset, ddrill, pad, opening, opening_yoffset, bevel_height, secondHoleDiameter=0, secondHoleOffset=[0,0], thirdHoleDiameter=0, thirdHoleOffset=[0,0], fourthHoleDiameter=0, fourthHoleOffset=[0,0],nibbleSize=[],nibblePos=[], fabref_offset=[0,0],
                        tags_additional=[], lib_name="${{KISYS3DMOD}}/Connectors_Terminal_Blocks", classname="Connectors_Terminal_Blocks", classname_description="terminal block", webpage="", script_generated_note=""):
                        
    package_size=[2*leftbottom_offset[0]+(pins-1)*rm, package_height];
    if len(leftbottom_offset)==3:
        package_size=[leftbottom_offset[0]+leftbottom_offset[2]+(pins-1)*rm, package_height];
    
    h_fab = package_size[1]
    w_fab = package_size[0]
    l_fab = -leftbottom_offset[0]
    t_fab = -(h_fab-leftbottom_offset[1])
    
    h_slk = h_fab + 2 * slk_offset
    w_slk = w_fab + 2 * slk_offset
    l_slk = l_fab - slk_offset
    t_slk = t_fab - slk_offset
    
    h_crt = h_fab + 2 * crt_offset
    w_crt = w_fab + 2 * crt_offset
    l_crt = l_fab - crt_offset
    t_crt = t_fab - crt_offset
    
    
    text_size = w_fab*0.6
    fab_text_size_max = 1.0
    if text_size < fab_text_size_min:
        text_size = fab_text_size_min
    elif text_size > fab_text_size_max:
        text_size = fab_text_size_max
    text_size = round(text_size, 2)
    text_size = [text_size,text_size]
    text_t = text_size[0] * 0.15
    
    
    description = "{2}, vertical (cable from top), {0} pins, pitch {1:02}mm, size {3}x{4}mm^2, drill diamater {5}mm, pad diameter {6}mm, see {7}, script-generated with ".format(pins, rm,classname_description, package_size[0], package_size[1], ddrill, max(pad), webpage)
    tags = "THT {2} vertical pitch {1:02}mm size {3}x{4}mm^2 drill {5}mm pad {6}mm".format(pins, rm,classname_description, package_size[0], package_size[1], ddrill, max(pad))
    
    if len(script_generated_note)>0:
        description=description+", "+script_generated_note
    
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
    kicad_modg = Translation(offset[0], offset[1])
    kicad_mod.append(kicad_modg)
    
    # set general values
    kicad_modg.append(Text(type='reference', text='REF**', at=[l_fab+w_fab/2, t_slk - txt_offset], layer='F.SilkS'))
    if (type(fabref_offset) in (tuple, list)):
        kicad_modg.append(Text(type='user', text='%R', at=[l_fab+w_fab/2+fabref_offset[0], t_fab+h_fab/2+fabref_offset[1]], layer='F.Fab', size=text_size ,thickness=text_t))
    else:
        kicad_modg.append(Text(type='user', text='%R', at=[l_fab+w_fab/2,  t_slk - txt_offset], layer='F.Fab', size=text_size ,thickness=text_t))
    kicad_modg.append(Text(type='value', text=footprint_name, at=[l_fab+w_fab/2, t_slk + h_slk + txt_offset], layer='F.Fab'))
    
    
    # create pads
    p1 = int(1)
    x1 = 0
    y1 = 0 
     
    pad_type = Pad.TYPE_THT 
    pad_shape1 = Pad.SHAPE_RECT 
    pad_shapeother = Pad.SHAPE_CIRCLE 
    pad_layers = Pad.LAYERS_THT
    keepouts=[];
    for p in range(1, pins + 1): 
         
        if p == 1: 
            kicad_modg.append(Pad(number=p, type=pad_type, shape=pad_shape1, at=[x1, y1], size=pad, drill=ddrill, layers=pad_layers)) 
            keepouts=keepouts+addKeepoutRect(x1, y1, pad[0]+8*slk_offset, pad[1]+8*slk_offset)
        else:
            kicad_modg.append(Pad(number=p, type=pad_type, shape=pad_shapeother, at=[x1, y1], size=pad, drill=ddrill, layers=pad_layers))
            keepouts=keepouts+addKeepoutRound(x1, y1, pad[0]+8*slk_offset, pad[0]+8*slk_offset)
        
        x1=x1+rm
    
    # create Body
    chamfer = min(h_fab/4, 2, bevel_height[0])
    bevelRectBL(kicad_modg,  [l_fab,t_fab], [w_fab,h_fab], 'F.Fab', lw_fab, bevel_size=chamfer)
    for bh in bevel_height:
        kicad_modg.append(Line(start=[l_fab, t_fab + h_fab-bh], end=[l_fab+w_fab, t_fab + h_fab-bh], layer='F.Fab', width=lw_fab))
        addHLineWithKeepout(kicad_modg,l_slk, l_slk+w_slk, t_fab + h_fab-bh, layer='F.SilkS', width=lw_slk, keepouts=keepouts)
    addRectWithKeepout(kicad_modg, l_slk, t_slk, w_slk, h_slk, layer='F.SilkS', width=lw_slk, keepouts=keepouts)
    
    # opening + other repeated features
    for p in range(1,pins+1):
        addRectWithKeepout(kicad_modg, (p-1)*rm-opening[0]/2, t_fab+h_fab-opening_yoffset-opening[1], opening[0], opening[1], 'F.SilkS', lw_slk, keepouts)
        addRectWith(kicad_modg, (p-1)*rm-opening[0]/2, t_fab+h_fab-opening_yoffset-opening[1], opening[0], opening[1], 'F.Fab', lw_fab)
        
        if not (type(secondHoleDiameter) in (tuple, list)) and secondHoleDiameter>0 and (p-1)*rm+secondHoleOffset[0]<l_fab+w_fab:
            kicad_modg.append(Circle(center=[(p-1)*rm+secondHoleOffset[0], 0+secondHoleOffset[1]], radius=secondHoleDiameter/2, layer='F.Fab', width=lw_fab))
            addCircleWithKeepout(kicad_modg, (p-1)*rm+secondHoleOffset[0], 0+secondHoleOffset[1], secondHoleDiameter/2, 'F.SilkS', lw_slk, keepouts)
        if not (type(thirdHoleDiameter) in (tuple, list)) and thirdHoleDiameter>0 and (p-1)*rm+thirdHoleOffset[0]<l_fab+w_fab:
            kicad_modg.append(Circle(center=[(p-1)*rm+thirdHoleOffset[0], 0+thirdHoleOffset[1]], radius=thirdHoleDiameter/2, layer='F.Fab', width=lw_fab))
            addCircleWithKeepout(kicad_modg, (p-1)*rm+thirdHoleOffset[0], 0+thirdHoleOffset[1], thirdHoleDiameter/2, 'F.SilkS', lw_slk, keepouts)
        if not (type(fourthHoleDiameter) in (tuple, list)) and fourthHoleDiameter>0 and (p-1)*rm+fourthHoleOffset[0]<l_fab+w_fab:
            kicad_modg.append(Circle(center=[(p-1)*rm+fourthHoleOffset[0], 0+fourthHoleOffset[1]], radius=fourthHoleDiameter/2, layer='F.Fab', width=lw_fab))
            addCircleWithKeepout(kicad_modg, (p-1)*rm+fourthHoleOffset[0], 0+fourthHoleOffset[1], fourthHoleDiameter/2, 'F.SilkS', lw_slk, keepouts)
        if (type(secondHoleDiameter) in (tuple, list)) and (p-1)*rm+secondHoleOffset[0]<l_fab+w_fab:
            kicad_modg.append(RectLine(start=[(p-1)*rm+secondHoleOffset[0]-secondHoleDiameter[0]/2, 0+secondHoleOffset[1]-secondHoleDiameter[1]/2], end=[(p-1)*rm+secondHoleOffset[0]+secondHoleDiameter[0]/2, 0+secondHoleOffset[1]+secondHoleDiameter[1]/2], layer='F.Fab', width=lw_fab))
            addRectWithKeepout(kicad_modg, (p-1)*rm+secondHoleOffset[0]-secondHoleDiameter[0]/2, 0+secondHoleOffset[1]-secondHoleDiameter[1]/2, secondHoleDiameter[0],secondHoleDiameter[1], 'F.SilkS', lw_slk, keepouts)
        if (type(thirdHoleDiameter) in (tuple, list)) and (p-1)*rm+thirdHoleOffset[0]<l_fab+w_fab:
            kicad_modg.append(RectLine(start=[(p-1)*rm+thirdHoleOffset[0]-thirdHoleDiameter[0]/2, 0+thirdHoleOffset[1]-thirdHoleDiameter[1]/2], end=[(p-1)*rm+thirdHoleOffset[0]+thirdHoleDiameter[0]/2, 0+thirdHoleOffset[1]+thirdHoleDiameter[1]/2], layer='F.Fab', width=lw_fab))
            addRectWithKeepout(kicad_modg, (p-1)*rm+thirdHoleOffset[0]-thirdHoleDiameter[0]/2, 0+thirdHoleOffset[1]-thirdHoleDiameter[1]/2, thirdHoleDiameter[0],thirdHoleDiameter[1], 'F.SilkS', lw_slk, keepouts)
        if (type(fourthHoleDiameter) in (tuple, list)) and (p-1)*rm+fourthHoleOffset[0]<l_fab+w_fab:
            kicad_modg.append(RectLine(start=[(p-1)*rm+fourthHoleOffset[0]-fourthHoleDiameter[0]/2, 0+fourthHoleOffset[1]-fourthHoleDiameter[1]/2], end=[(p-1)*rm+fourthHoleOffset[0]+fourthHoleDiameter[0]/2, 0+fourthHoleOffset[1]+fourthHoleDiameter[1]/2], layer='F.Fab', width=lw_fab))
            addRectWithKeepout(kicad_modg, (p-1)*rm+fourthHoleOffset[0]-fourthHoleDiameter[0]/2, 0+fourthHoleOffset[1]-fourthHoleDiameter[1]/2, fourthHoleDiameter[0],fourthHoleDiameter[1], 'F.SilkS', lw_slk, keepouts)

    #nibble
    if len(nibbleSize)==2 and len(nibblePos)==2:
        kicad_modg.append(RectLine(start=[l_fab+nibblePos[0], t_fab+nibblePos[1]], end=[l_fab+nibblePos[0]+nibbleSize[0], t_fab+nibblePos[1]+nibbleSize[1]], layer='F.Fab', width=lw_fab))
        addRectWithKeepout(kicad_modg, l_fab+nibblePos[0]-slk_offset, t_fab+nibblePos[1]-slk_offset, nibbleSize[0],nibbleSize[1]+2*slk_offset, 'F.SilkS', lw_slk, keepouts)
        
                
                
    # create SILKSCREEN-pin1-marker
    kicad_modg.append(Line(start=[l_slk-2*lw_slk, t_slk + h_slk-chamfer], end=[l_slk-2*lw_slk, t_slk + h_slk+2*lw_slk], layer='F.SilkS', width=lw_slk))
    kicad_modg.append(Line(start=[l_slk-2*lw_slk, t_slk + h_slk+2*lw_slk], end=[l_slk-2*lw_slk+chamfer, t_slk + h_slk+2*lw_slk], layer='F.SilkS', width=lw_slk))
    
    # create courtyard
    kicad_mod.append(RectLine(start=[roundCrt(l_crt + offset[0]), roundCrt(t_crt + offset[1])],
                              end=[roundCrt(l_crt + offset[0] + w_crt), roundCrt(t_crt + offset[1] + h_crt)],
                              layer='F.CrtYd', width=lw_crt))
    
    
    # add model
    kicad_modg.append(
        Model(filename=lib_name + ".3dshapes/" + footprint_name + ".wrl", at=[0,0,0], scale=[1,1,1], rotate=[0,0,0]))
    
    #debug_draw_keepouts(kicad_modg,keepouts)
   
    # write file
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile(footprint_name + '.kicad_mod')



    
    


#    <-----> vsegment_lines_offset
#  +-+------------+-----------+-------------+                      ^                  
#  | |     H      |    H      |    H        | ^                    |                  
#  | |----------- |           |             | |                    |                                       ^
#  | ||   OOO   | |   OOO     |   OOO       | |secondHoleOffset    | package_height                        |
#  | ||  OOOOO  | |  OOOOO    |  OOOOO      | v                    |                  ^                    | opening[1]
#  | ||   OOO   | |   OOO     |   OOO       |                      |                  |                    |
#  +-+------------+-----------+-------------+ ^                    |                  | leftbottom_offset  x
#  | |            |           |             | | bevel_height       |                  |                    | opening_yoffset
#  +-+------------+-----------+-------------+ v                    v                  v                    v
#          <--- rm ---->
#  <------>leftbottom_offset[0]     <------->leftbottom_offset[2] (or leftbottom_offset[0]  if len(leftbottom_offset)==2)
#     <---------> opening[0]
#
#
def makeTerminalBlock45Degree(footprint_name, pins, rm, package_height, leftbottom_offset, ddrill, pad, opening, opening_xoffset, opening_yoffset, opening_elliptic=False, bevel_height=[], vsegment_lines_offset=[], secondHoleDiameter=0, secondHoleOffset=[0,0], thirdHoleDiameter=0, thirdHoleOffset=[0,0], fourthHoleDiameter=0, fourthHoleOffset=[0,0], fifthHoleDiameter=0, fifthHoleOffset=[0,0],secondDrillDiameter=0,secondDrillOffset=[0,0],secondDrillPad=[0,0],nibbleSize=[],nibblePos=[], fabref_offset=[0,0],secondEllipseSize=[0,0],secondEllipseOffset=[0,0],
                        tags_additional=[], lib_name="${{KISYS3DMOD}}/Connectors_Terminal_Blocks", classname="Connectors_Terminal_Blocks", classname_description="terminal block", webpage="", script_generated_note=""):
                        
    package_size=[2*leftbottom_offset[0]+(pins-1)*rm, package_height];
    if len(leftbottom_offset)==3:
        package_size=[leftbottom_offset[0]+leftbottom_offset[2]+(pins-1)*rm, package_height];
    
    h_fab = package_size[1]
    w_fab = package_size[0]
    l_fab = -leftbottom_offset[0]
    t_fab = -(h_fab-leftbottom_offset[1])
    
    h_slk = h_fab + 2 * slk_offset
    w_slk = w_fab + 2 * slk_offset
    l_slk = l_fab - slk_offset
    t_slk = t_fab - slk_offset
    
    h_crt = h_fab + 2 * crt_offset
    w_crt = w_fab + 2 * crt_offset
    l_crt = l_fab - crt_offset
    t_crt = t_fab - crt_offset
    
    
    text_size = w_fab*0.6
    fab_text_size_max = 1.0
    if text_size < fab_text_size_min:
        text_size = fab_text_size_min
    elif text_size > fab_text_size_max:
        text_size = fab_text_size_max
    text_size = round(text_size, 2)
    text_size = [text_size,text_size]
    text_t = text_size[0] * 0.15
    
    
    description = "{2}, 45Degree (cable under 45degree), {0} pins, pitch {1:02}mm, size {3}x{4}mm^2, drill diamater {5}mm, pad diameter {6}mm, see {7}, script-generated with ".format(pins, rm,classname_description, package_size[0], package_size[1], ddrill, max(pad), webpage)
    tags = "THT {2} 45Degree pitch {1:02}mm size {3}x{4}mm^2 drill {5}mm pad {6}mm".format(pins, rm,classname_description, package_size[0], package_size[1], ddrill, max(pad))
    
    if len(script_generated_note)>0:
        description=description+", "+script_generated_note
    
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
    kicad_modg = Translation(offset[0], offset[1])
    kicad_mod.append(kicad_modg)
    
    # set general values
    kicad_modg.append(Text(type='reference', text='REF**', at=[l_fab+w_fab/2, t_slk - txt_offset], layer='F.SilkS'))
    if (type(fabref_offset) in (tuple, list)):
        kicad_modg.append(Text(type='user', text='%R', at=[l_fab+w_fab/2+fabref_offset[0], t_fab+h_fab/2+fabref_offset[1]], layer='F.Fab', size=text_size ,thickness=text_t))
    else:
        kicad_modg.append(Text(type='user', text='%R', at=[l_fab+w_fab/2,  t_slk - txt_offset], layer='F.Fab', size=text_size ,thickness=text_t))
    kicad_modg.append(Text(type='value', text=footprint_name, at=[l_fab+w_fab/2, t_slk + h_slk + txt_offset], layer='F.Fab'))
    
    
    # create pads
    p1 = int(1)
    x1 = 0
    y1 = 0 
     
    pad_type = Pad.TYPE_THT 
    pad_shape1 = Pad.SHAPE_RECT 
    pad_shapeother = Pad.SHAPE_CIRCLE 
    if secondDrillPad[0]!=secondDrillPad[1]:
        pad_shapeother = Pad.SHAPE_OVAL 
    pad_layers = Pad.LAYERS_THT
    if secondDrillPad[0]>0:
        extradrill1_type = Pad.TYPE_THT
    keepouts=[];
    for p in range(1, pins + 1): 
        pextra=0
        if secondDrillPad[0]>0:
            pextra=p
        if p == 1: 
            kicad_modg.append(Pad(number=p, type=pad_type, shape=pad_shape1, at=[x1, y1], size=pad, drill=ddrill, layers=pad_layers)) 
            keepouts=keepouts+addKeepoutRect(x1, y1, pad[0]+8*slk_offset, pad[1]+8*slk_offset)
            if secondDrillDiameter>0:
                kicad_modg.append(Pad(number=p, type=extradrill1_type, shape=pad_shape1, at=[x1+secondDrillOffset[0], y1+secondDrillOffset[1]], size=secondDrillPad, drill=secondDrillDiameter, layers=pad_layers)) 
                keepouts=keepouts+addKeepoutRect(x1+secondDrillOffset[0], y1+secondDrillOffset[1], max(secondDrillPad[0],secondDrillDiameter)+8*slk_offset, max(secondDrillPad[1],secondDrillDiameter)+8*slk_offset)
        else:
            kicad_modg.append(Pad(number=p, type=pad_type, shape=pad_shapeother, at=[x1, y1], size=pad, drill=ddrill, layers=pad_layers))
            if pad[0]!=pad[1]:
                keepouts=keepouts+addKeepoutRect(x1, y1, pad[0]+8*slk_offset, pad[1]+8*slk_offset)
            else:
                keepouts=keepouts+addKeepoutRound(x1, y1, pad[0]+8*slk_offset, pad[0]+8*slk_offset)
            if secondDrillDiameter>0:
                kicad_modg.append(Pad(number=p, type=extradrill1_type, shape=pad_shapeother, at=[x1+secondDrillOffset[0], y1+secondDrillOffset[1]], size=secondDrillPad, drill=secondDrillDiameter, layers=pad_layers)) 
                keepouts=keepouts+addKeepoutRect(x1+secondDrillOffset[0], y1+secondDrillOffset[1], max(secondDrillPad[0],secondDrillDiameter)+8*slk_offset, max(secondDrillPad[1],secondDrillDiameter)+8*slk_offset)
        
        x1=x1+rm
        
        

    # create Body
    if len(bevel_height)>0:
        chamfer = min(h_fab/4, 2, bevel_height[0])
    else:
        chamfer = min(h_fab/4, 2)
    bevelRectBL(kicad_modg,  [l_fab,t_fab], [w_fab,h_fab], 'F.Fab', lw_fab, bevel_size=chamfer)
    for bh in bevel_height:
        kicad_modg.append(Line(start=[l_fab, t_fab + h_fab-bh], end=[l_fab+w_fab, t_fab + h_fab-bh], layer='F.Fab', width=lw_fab))
        addHLineWithKeepout(kicad_modg,l_slk, l_slk+w_slk, t_fab + h_fab-bh, layer='F.SilkS', width=lw_slk, keepouts=keepouts)
    addRectWithKeepout(kicad_modg, l_slk, t_slk, w_slk, h_slk, layer='F.SilkS', width=lw_slk, keepouts=keepouts)
    
    # opening + other repeated features
    for p in range(1,pins+1):
        if opening[0]>0 and opening[1]>0:
            if opening_elliptic:
                addEllipse(kicad_modg, (p-1)*rm+opening_xoffset, t_fab+h_fab-opening_yoffset, opening[0], opening[1], layer='F.Fab', width=lw_fab)
                addEllipseWithKeepout(kicad_modg, (p-1)*rm+opening_xoffset, t_fab+h_fab-opening_yoffset, opening[0], opening[1], layer='F.SilkS', width=lw_slk, keepouts=keepouts)
            else:
                addRectWithKeepout(kicad_modg, (p-1)*rm-opening[0]/2+opening_xoffset, t_fab+h_fab-opening_yoffset-opening[1], opening[0], opening[1], 'F.SilkS', lw_slk, keepouts)
                addRectWith(kicad_modg, (p-1)*rm-opening[0]/2+opening_xoffset, t_fab+h_fab-opening_yoffset-opening[1], opening[0], opening[1], 'F.Fab', lw_fab)
        
        # vertical segment separation lines
        for seg_offset in vsegment_lines_offset:
            if seg_offset>=l_fab and seg_offset<=l_fab+w_fab:
                addVLineWithKeepout(kicad_modg, x=(p-1)*rm+seg_offset, y0=t_fab, y1=t_fab+h_fab, layer='F.Fab', width=lw_fab, keepouts=[])
                addVLineWithKeepout(kicad_modg, x=(p-1)*rm+seg_offset, y0=t_slk, y1=t_slk+h_slk, layer='F.SilkS', width=lw_slk, keepouts=keepouts)
            
        if not (type(secondHoleDiameter) in (tuple, list)) and secondHoleDiameter>0 and (p-1)*rm+secondHoleOffset[0]<l_fab+w_fab:
            kicad_modg.append(Circle(center=[(p-1)*rm+secondHoleOffset[0], 0+secondHoleOffset[1]], radius=secondHoleDiameter/2, layer='F.Fab', width=lw_fab))
            addCircleWithKeepout(kicad_modg, (p-1)*rm+secondHoleOffset[0], 0+secondHoleOffset[1], secondHoleDiameter/2, 'F.SilkS', lw_slk, keepouts)
        if not (type(thirdHoleDiameter) in (tuple, list)) and thirdHoleDiameter>0 and (p-1)*rm+thirdHoleOffset[0]<l_fab+w_fab:
            kicad_modg.append(Circle(center=[(p-1)*rm+thirdHoleOffset[0], 0+thirdHoleOffset[1]], radius=thirdHoleDiameter/2, layer='F.Fab', width=lw_fab))
            addCircleWithKeepout(kicad_modg, (p-1)*rm+thirdHoleOffset[0], 0+thirdHoleOffset[1], thirdHoleDiameter/2, 'F.SilkS', lw_slk, keepouts)
        if not (type(fourthHoleDiameter) in (tuple, list)) and fourthHoleDiameter>0 and (p-1)*rm+fourthHoleOffset[0]<l_fab+w_fab:
            kicad_modg.append(Circle(center=[(p-1)*rm+fourthHoleOffset[0], 0+fourthHoleOffset[1]], radius=fourthHoleDiameter/2, layer='F.Fab', width=lw_fab))
            addCircleWithKeepout(kicad_modg, (p-1)*rm+fourthHoleOffset[0], 0+fourthHoleOffset[1], fourthHoleDiameter/2, 'F.SilkS', lw_slk, keepouts)
        if not (type(fifthHoleDiameter) in (tuple, list)) and fifthHoleDiameter>0 and (p-1)*rm+fifthHoleOffset[0]<l_fab+w_fab:
            kicad_modg.append(Circle(center=[(p-1)*rm+fifthHoleOffset[0], 0+fifthHoleOffset[1]], radius=fifthHoleDiameter/2, layer='F.Fab', width=lw_fab))
            addCircleWithKeepout(kicad_modg, (p-1)*rm+fifthHoleOffset[0], 0+fifthHoleOffset[1], fifthHoleDiameter/2, 'F.SilkS', lw_slk, keepouts)
        if (type(secondHoleDiameter) in (tuple, list)) and (p-1)*rm+secondHoleOffset[0]<l_fab+w_fab:
            kicad_modg.append(RectLine(start=[(p-1)*rm+secondHoleOffset[0]-secondHoleDiameter[0]/2, 0+secondHoleOffset[1]-secondHoleDiameter[1]/2], end=[(p-1)*rm+secondHoleOffset[0]+secondHoleDiameter[0]/2, 0+secondHoleOffset[1]+secondHoleDiameter[1]/2], layer='F.Fab', width=lw_fab))
            addRectWithKeepout(kicad_modg, (p-1)*rm+secondHoleOffset[0]-secondHoleDiameter[0]/2, 0+secondHoleOffset[1]-secondHoleDiameter[1]/2, secondHoleDiameter[0],secondHoleDiameter[1], 'F.SilkS', lw_slk, keepouts)
        if (type(thirdHoleDiameter) in (tuple, list)) and (p-1)*rm+thirdHoleOffset[0]<l_fab+w_fab:
            kicad_modg.append(RectLine(start=[(p-1)*rm+thirdHoleOffset[0]-thirdHoleDiameter[0]/2, 0+thirdHoleOffset[1]-thirdHoleDiameter[1]/2], end=[(p-1)*rm+thirdHoleOffset[0]+thirdHoleDiameter[0]/2, 0+thirdHoleOffset[1]+thirdHoleDiameter[1]/2], layer='F.Fab', width=lw_fab))
            addRectWithKeepout(kicad_modg, (p-1)*rm+thirdHoleOffset[0]-thirdHoleDiameter[0]/2, 0+thirdHoleOffset[1]-thirdHoleDiameter[1]/2, thirdHoleDiameter[0],thirdHoleDiameter[1], 'F.SilkS', lw_slk, keepouts)
        if (type(fourthHoleDiameter) in (tuple, list)) and (p-1)*rm+fourthHoleOffset[0]<l_fab+w_fab:
            kicad_modg.append(RectLine(start=[(p-1)*rm+fourthHoleOffset[0]-fourthHoleDiameter[0]/2, 0+fourthHoleOffset[1]-fourthHoleDiameter[1]/2], end=[(p-1)*rm+fourthHoleOffset[0]+fourthHoleDiameter[0]/2, 0+fourthHoleOffset[1]+fourthHoleDiameter[1]/2], layer='F.Fab', width=lw_fab))
            addRectWithKeepout(kicad_modg, (p-1)*rm+fourthHoleOffset[0]-fourthHoleDiameter[0]/2, 0+fourthHoleOffset[1]-fourthHoleDiameter[1]/2, fourthHoleDiameter[0],fourthHoleDiameter[1], 'F.SilkS', lw_slk, keepouts)
        if (type(fifthHoleDiameter) in (tuple, list)) and (p-1)*rm+fifthHoleOffset[0]<l_fab+w_fab:
            kicad_modg.append(RectLine(start=[(p-1)*rm+fifthHoleOffset[0]-fifthHoleDiameter[0]/2, 0+fifthHoleOffset[1]-fifthHoleDiameter[1]/2], end=[(p-1)*rm+fifthHoleOffset[0]+fifthHoleDiameter[0]/2, 0+fifthHoleOffset[1]+fifthHoleDiameter[1]/2], layer='F.Fab', width=lw_fab))
            addRectWithKeepout(kicad_modg, (p-1)*rm+fifthHoleOffset[0]-fifthHoleDiameter[0]/2, 0+fifthHoleOffset[1]-fifthHoleDiameter[1]/2, fifthHoleDiameter[0],fifthHoleDiameter[1], 'F.SilkS', lw_slk, keepouts)
        if secondEllipseSize[0]>0 and secondEllipseSize[1]>0:
            addEllipse(kicad_modg, (p-1)*rm+secondEllipseOffset[0], 0+secondEllipseOffset[1], secondEllipseSize[0], secondEllipseSize[1], layer='F.Fab', width=lw_fab)
            addEllipseWithKeepout(kicad_modg, (p-1)*rm+secondEllipseOffset[0], 0+secondEllipseOffset[1], secondEllipseSize[0], secondEllipseSize[1], layer='F.SilkS', width=lw_slk, keepouts=keepouts)

    #nibble
    if len(nibbleSize)==2 and len(nibblePos)==2:
        kicad_modg.append(RectLine(start=[l_fab+nibblePos[0], t_fab+nibblePos[1]], end=[l_fab+nibblePos[0]+nibbleSize[0], t_fab+nibblePos[1]+nibbleSize[1]], layer='F.Fab', width=lw_fab))
        addRectWithKeepout(kicad_modg, l_fab+nibblePos[0]-slk_offset, t_fab+nibblePos[1]-slk_offset, nibbleSize[0],nibbleSize[1]+2*slk_offset, 'F.SilkS', lw_slk, keepouts)
        
                
                
    # create SILKSCREEN-pin1-marker
    kicad_modg.append(Line(start=[l_slk-2*lw_slk, t_slk + h_slk-chamfer], end=[l_slk-2*lw_slk, t_slk + h_slk+2*lw_slk], layer='F.SilkS', width=lw_slk))
    kicad_modg.append(Line(start=[l_slk-2*lw_slk, t_slk + h_slk+2*lw_slk], end=[l_slk-2*lw_slk+chamfer, t_slk + h_slk+2*lw_slk], layer='F.SilkS', width=lw_slk))
    
    # create courtyard
    kicad_mod.append(RectLine(start=[roundCrt(l_crt + offset[0]), roundCrt(t_crt + offset[1])],
                              end=[roundCrt(l_crt + offset[0] + w_crt), roundCrt(t_crt + offset[1] + h_crt)],
                              layer='F.CrtYd', width=lw_crt))
    
    
    # add model
    kicad_modg.append(
        Model(filename=lib_name + ".3dshapes/" + footprint_name + ".wrl", at=[0,0,0], scale=[1,1,1], rotate=[0,0,0]))
    
    #debug_draw_keepouts(kicad_modg,keepouts)
   
    # write file
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile(footprint_name + '.kicad_mod')


