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


#    overlen_top                           overlen_bottom
#  <--->                                 <------>
#       O          O          O          O                             ^
#       |          |          |          |                             |
#  +--------------------------------------------+    ^                 |
#  |                                            |    |                 |
#  +--+                                         |    |                 |
#     |                                         | package_width        |
#  +--+                                         |    |           pinrow_distance
#  |                                            |    |                 |
#  +--------------------------------------------+    v                 |
#       |          |          |          |                             |
#       O          O          O          O                             v
#
#       <----RM---->
def makeDIP(pins, rm, pinrow_distance_in, package_width, overlen_top, overlen_bottom, ddrill, pad, smd_pads=False,
            socket_width=0, socket_height=0, socket_pinrow_distance_offset=0, tags_additional=[],
            lib_name="Package_DIP", offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0], DIPName='DIP', DIPDescription='though-hole mounted DIP', DIPTags='THT DIP DIL PDIP', 
            prefix_name = "", skip_pin = [], skip_count = False, right_cnt_start = -1):

    pinrow_distance = pinrow_distance_in + socket_pinrow_distance_offset
    h_fab = (pins / 2 - 1) * rm + overlen_top + overlen_bottom
    w_fab = package_width
    l_fab = (pinrow_distance - w_fab) / 2
    t_fab = -overlen_top
    
    hasSocket = False
    if (socket_height > 0 and socket_width > 0):
        hasSocket = True
        h_fabs = socket_height
        w_fabs = socket_width
        l_fabs = (w_fabs - pinrow_distance) / 2
        t_fabs = (h_fabs - (pins / 2 - 1) * rm) / 2
    
    h_slk = h_fab + 2 * slk_offset
    w_slk = min(w_fab + 2 * slk_offset, pinrow_distance - pad[0] - 12 * slk_offset)
    l_slk = (pinrow_distance - w_slk) / 2
    t_slk = -overlen_top - slk_offset
    w_crt = max(package_width, pinrow_distance + pad[0]) + 2 * crt_offset
    h_crt = max(h_fab, (pins / 2 - 1) * rm + pad[1]) + 2 * crt_offset
    
    hasSocket = False
    if (socket_height > 0 and socket_width > 0):
        hasSocket = True
        h_fabs = max(socket_height,h_slk)
        w_fabs = socket_width
        l_fabs = (pinrow_distance - w_fabs) / 2
        t_fabs = ((pins / 2 - 1) * rm - h_fabs) / 2
        h_slks = h_fabs + 2 * slk_offset
        w_slks = max(w_fabs, pinrow_distance + pad[0] + 6 * slk_offset) + 2 * slk_offset
        l_slks = (pinrow_distance - w_slks) / 2
        t_slks = ((pins / 2 - 1) * rm - h_slks) / 2
        w_crt = max(w_crt, w_fabs + 2 * crt_offset)
        h_crt = max(h_crt, h_fabs + 2 * crt_offset)
    
    l_crt = pinrow_distance / 2 - w_crt / 2
    t_crt = (pins / 2 - 1) * rm / 2 - h_crt / 2
    
    footprint_name = DIPName+"-{0}_W{1}mm".format(pins, round(pinrow_distance, 2))
    if len(prefix_name) > 0:
        footprint_name = DIPName+'-'+prefix_name+"-{0}_W{1}mm".format(pins, round(pinrow_distance, 2))
    description = "{0}-lead {3} package, row spacing {1} mm ({2} mils)".format(pins, round(pinrow_distance, 2),
                                                                               int(pinrow_distance / 2.54 * 100),
																			   DIPDescription)
    tags = DIPTags+" {0}mm {1}mm {2}mil".format(rm, pinrow_distance, int(pinrow_distance / 2.54 * 100))
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
    if (smd_pads):
        offset = [-pinrow_distance / 2, -(pins / 2 - 1) * rm / 2]
        kicad_modg = Translation(offset[0], offset[1])
        kicad_mod.append(kicad_modg)
        kicad_mod.setAttribute('smd')
    else:
        kicad_modg = kicad_mod
    
    # set general values
    kicad_modg.append(
        Text(type='reference', text='REF**', at=[pinrow_distance / 2, t_slk - txt_offset], layer='F.SilkS'))
    kicad_modg.append(
        Text(type='user', text='%R', at=[pinrow_distance/2, t_fab + h_fab / 2], layer='F.Fab'))
    kicad_modg.append(
        Text(type='value', text=footprint_name, at=[pinrow_distance / 2, t_slk + h_slk + txt_offset], layer='F.Fab'))
    
    # create FAB-layer
    bevelRectTL(kicad_modg, [l_fab, t_fab], [w_fab, h_fab], 'F.Fab', lw_fab)
    if hasSocket:
        kicad_modg.append(
            RectLine(start=[l_fabs, t_fabs], end=[l_fabs + w_fabs, t_fabs + h_fabs], layer='F.Fab', width=lw_fab))
    
    # create SILKSCREEN-layer
    DIPRectT(kicad_modg, [l_slk, t_slk], [w_slk, h_slk], 'F.SilkS', lw_slk)
    if hasSocket:
        # if smd_pads:
        #    kicad_modg.append(Line(start=[l_slks, t_slks], end=[l_slks + w_slks, t_slks], layer='F.SilkS',width=lw_slk))
        #    kicad_modg.append(Line(start=[l_slks, t_slks+h_slks], end=[l_slks + w_slks, t_slks+h_slks], layer='F.SilkS',width=lw_slk))
        # else:
        #    kicad_modg.append(RectLine(start=[l_slks, t_slks], end=[l_slks+w_slks, t_slks+h_slks], layer='F.SilkS', width=lw_slk))
        kicad_modg.append(
            RectLine(start=[l_slks, t_slks], end=[l_slks + w_slks, t_slks + h_slks], layer='F.SilkS', width=lw_slk))
    
    # create courtyard
    kicad_mod.append(RectLine(start=[roundCrt(l_crt + offset[0]), roundCrt(t_crt + offset[1])],
                              end=[roundCrt(l_crt + offset[0] + w_crt), roundCrt(t_crt + offset[1] + h_crt)],
                              layer='F.CrtYd', width=lw_crt))
    
    # create pads
    p1 = int(1)
    x1 = 0
    y1 = 0
    p2 = int(pins / 2 + 1)
    if right_cnt_start >= 0:
        # The pins on the right side shall start with a specific value
        p2 = right_cnt_start

    x2 = pinrow_distance
    y2 = (pins / 2 - 1) * rm
    
    if smd_pads:
        pad_type = Pad.TYPE_SMT
        pad_shape1 = Pad.SHAPE_RECT
        pad_shapeother = Pad.SHAPE_RECT
        pad_layers = ['F.Cu', 'F.Mask', 'F.Paste']
    else:
        pad_type = Pad.TYPE_THT
        pad_shape1 = Pad.SHAPE_RECT
        pad_shapeother = Pad.SHAPE_OVAL
        pad_layers = ['*.Cu', '*.Mask']
    
    for p in range(1, int(pins / 2 + 1)):
        
        addpinL = True
        for sp in skip_pin:
            if sp == p:
                # The pin number is among those who should not be added
                addpinL = False

        if addpinL:
            if p == 1:
                kicad_modg.append(Pad(number=p1, type=pad_type, shape=pad_shape1, at=[x1, y1], size=pad, drill=ddrill,
                                      layers=pad_layers))
            else:
                kicad_modg.append(Pad(number=p1, type=pad_type, shape=pad_shapeother, at=[x1, y1], size=pad, drill=ddrill,
                                      layers=pad_layers))

        addpinR = True
        for sp in skip_pin:
            if sp == p + int(pins / 2):
                # The pin number is among those who should not be added
                addpinR = False

        if addpinR:
            kicad_modg.append(Pad(number=p2, type=pad_type, shape=pad_shapeother, at=[x2, y2], size=pad, drill=ddrill,
                              layers=pad_layers))

        # Do not increase the pin number if it should be skipped
        if not (skip_count and not addpinL):
            p1 = p1 + 1

        # Do not increase the pin number if it should be skipped
        if not (skip_count and not addpinR):
            p2 = p2 + 1

        y1 = y1 + rm
        y2 = y2 - rm

    # add model
    kicad_modg.append(
        Model(filename="${KISYS3DMOD}/" + lib_name + ".3dshapes/" + footprint_name + ".wrl", at=offset3d, scale=scale3d, rotate=rotate3d))
    
    # print render tree
    # print(kicad_mod.getRenderTree())
    # print(kicad_mod.getCompleteRenderTree())
    
    # write file
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile(footprint_name + '.kicad_mod')


#    overlen_top                           overlen_bottom
#  <--->                                 <------>
#       O          O          O          O                             ^
#       |          |          |          |                             |
#  +--------------------------------------------+    ^                 |
#  |  +---+  ^                                  |    |                 |
#  |  |   |  |                                  |    |                 |
#  |  +---+  switch_width                       | package_width        |
#  |  |   |  |                                  |    |           pinrow_distance
#  |  +---+  v                                  |    |                 |
#  +--------------------------------------------+    v                 |
#       |          |          |          |                             |
#       O          O          O          O                             v
#     <--->switch_height
#       <----RM---->
#
#  mode=Piano/Slide
#
def makeDIPSwitch(pins, rm, pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad, switch_width,
                  switch_height, mode='Piano', smd_pads=False, tags_additional=[],
                  lib_name="Button_Switch_THT", offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 90],
                  specialFPName="", SOICStyleSilk=False, cornerPads=[], cornerPadOffsetX=0, cornerPadOffsetY=0, webpage="", device_name="", switchtype="SPST"):
    switches = int(pins / 2)
    
    h_fab = (pins / 2 - 1) * rm + overlen_top + overlen_bottom
    w_fab = package_width
    l_fab = (pinrow_distance - w_fab) / 2
    t_fab = -overlen_top
    
    h_slk = h_fab + 2 * slk_offset
    w_slk = w_fab + 2 * slk_offset
    #if (package_width > pinrow_distance):
    #    w_slk = max(w_fab + 2 * slk_offset, pinrow_distance + pad[0] + 2 * slk_offset)
    #else:
    #    w_slk = min(w_fab + 2 * slk_offset, pinrow_distance - pad[0] - 4 * slk_offset)
    l_slk = (pinrow_distance - w_slk) / 2
    t_slk = -overlen_top - slk_offset
    
    if len(cornerPads) == 2:
        t_slk = t_fab + cornerPadOffsetY - cornerPads[1] / 2 - slk_offset
        h_slk = t_fab + h_fab - cornerPadOffsetY + cornerPads[1] / 2 + slk_offset - t_slk
    
    w_crt = max(package_width, pinrow_distance + pad[0]) + 2 * crt_offset
    h_crt = max(h_fab, (pins / 2 - 1) * rm + pad[1], h_slk) + 2 * crt_offset
    l_crt = pinrow_distance / 2 - w_crt / 2
    t_crt = min(t_slk - crt_offset, (pins / 2 - 1) * rm / 2 - h_crt / 2)
    
    if (mode == 'Piano'):
        l_crt = l_crt - switch_width
        w_crt = w_crt + switch_width
    
    smdtext=''
    smddescription=''
    if smd_pads:
        #smdtext='_SMD';
        smddescription='SMD '
    
    add_type=""
    bodysize="{0}x{1}mm".format(round(package_width,2), round(overlen_top+overlen_bottom+(pins/2-1)*rm,2))
    if len(device_name)>0:
        add_type="_"+device_name
        bodysize=""
    
    bodysizefp="";
    if len(bodysize)>0:
        bodysizefp=bodysize+"_"
    
    footprint_name = "SW_DIP_{6}x{0:02}_{4}{5}_{7}W{1}mm_P{2}mm{3}".format(switches, round(pinrow_distance, 2), round(rm, 2), smdtext, mode,add_type,switchtype,bodysizefp)
    description = "{4}{0}x-dip-switch {6} {5}, {3}, row spacing {1} mm ({2} mils), body size {7}".format(switches, round(pinrow_distance, 2),
                                                                               int(pinrow_distance / 2.54 * 100), mode,smddescription,device_name,switchtype,bodysize)

    if len(webpage)>0:
      description=description+" (see "+webpage+")"
    tags = "{3}DIP Switch {4} {0} {1}mm {2}mil".format(mode, pinrow_distance, int(pinrow_distance / 2.54 * 100),smddescription,switchtype)
    if (len(tags_additional) > 0):
        for t in tags_additional:
            if t != "SMD":  # suppress "SMD" in file name since this is already part of folder name
                footprint_name = footprint_name + "_" + t
            description = description + ", " + t
            tags = tags + " " + t
    
    if len(specialFPName) > 0:
        footprint_name = specialFPName
    
    print(footprint_name)
    
    # init kicad footprint
    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription(description)
    kicad_mod.setTags(tags)
    
    # anchor for SMD-symbols is in the center, for THT-sybols at pin1
    offset = [0, 0]
    if (smd_pads):
        offset = [-pinrow_distance / 2, -(pins / 2 - 1) * rm / 2]
        kicad_modg = Translation(offset[0], offset[1])
        kicad_mod.append(kicad_modg)
        kicad_mod.setAttribute('smd')
    else:
        kicad_modg = kicad_mod
    
    # add texts
    if pins == 2:
        fab_ref_size = [0.6, 0.6]
    else:
        ss=max(0.25, min((package_width-switch_width)*0.35, 0.8))
        fab_ref_size = [ss, ss]
        
    kicad_modg.append(Text(type='reference', text='REF**', at=[pinrow_distance / 2, t_slk - txt_offset], layer='F.SilkS'))
    kicad_modg.append(Text(type='value', text=footprint_name, at=[pinrow_distance / 2, t_slk + h_slk + txt_offset], layer='F.Fab'))
    if (mode == 'Piano'):
        kicad_modg.append(Text(type='user', text='%R', at=[pinrow_distance/2, t_fab + h_fab /2], size=fab_ref_size, layer='F.Fab', thickness=fab_ref_size[0]*0.15))
    else:
        kicad_modg.append(Text(type='user', text='%R', at=[pinrow_distance/2 + (package_width+switch_width)/4, t_fab + h_fab /2], rotation=90, size=fab_ref_size, layer='F.Fab', thickness=fab_ref_size[0]*0.15))
        kicad_modg.append(Text(type='user', text='on', at=[pinrow_distance/2 + (package_width+switch_width)/4-pinrow_distance/4, t_fab + (overlen_top-switch_height/2)/2], rotation=0, size=fab_ref_size, layer='F.Fab', thickness=fab_ref_size[0]*0.15))
        
    
    # create pads
    p1 = int(1)
    x1 = 0
    y1 = 0
    p2 = int(pins / 2 + 1)
    x2 = pinrow_distance
    y2 = (pins / 2 - 1) * rm
    keepouts=[];
    
    if smd_pads:
        pad_type = Pad.TYPE_SMT
        pad_shape1 = Pad.SHAPE_RECT
        pad_shapeother = Pad.SHAPE_RECT
        pad_layers = ['F.Cu', 'F.Mask', 'F.Paste']
    else:
        pad_type = Pad.TYPE_THT
        pad_shape1 = Pad.SHAPE_RECT
        pad_shapeother = Pad.SHAPE_OVAL
        pad_layers = ['*.Cu', '*.Mask']
    
    keepout_addsize=4*max(slk_offset, lw_slk)
    for p in range(1, int(pins / 2 + 1)):
        if p == 1:
            kicad_modg.append(Pad(number=p1, type=pad_type, shape=pad_shape1, at=[x1, y1], size=pad, drill=ddrill, layers=pad_layers))
            keepouts=keepouts+addKeepoutRect(x1, y1, pad[0]+keepout_addsize, pad[1]+keepout_addsize)
        else:
            kicad_modg.append(Pad(number=p1, type=pad_type, shape=pad_shapeother, at=[x1, y1], size=pad, drill=ddrill, layers=pad_layers))
            keepouts=keepouts+addKeepoutRound(x1, y1, pad[0]+keepout_addsize, pad[1]+keepout_addsize)
        
        kicad_modg.append(Pad(number=p2, type=pad_type, shape=pad_shapeother, at=[x2, y2], size=pad, drill=ddrill, layers=pad_layers))
        keepouts=keepouts+addKeepoutRound(x2, y2, pad[0]+keepout_addsize, pad[1]+keepout_addsize)
        
        p1 = p1 + 1
        p2 = p2 + 1
        y1 = y1 + rm
        y2 = y2 - rm
    
    if len(cornerPads) == 2:
        kicad_modg.append(Pad(number=pins + 1, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
                              at=[l_fab + cornerPadOffsetX, t_fab + cornerPadOffsetY], size=cornerPads, drill=0,
                              layers=pad_layers))
        keepouts=keepouts+addKeepoutRect(l_fab + cornerPadOffsetX, t_fab + cornerPadOffsetY, cornerPads[0]+keepout_addsize, cornerPads[1]+keepout_addsize)                              
        kicad_modg.append(Pad(number=pins + 1, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
                              at=[l_fab + w_fab - cornerPadOffsetX, t_fab + cornerPadOffsetY], size=cornerPads, drill=0,
                              layers=pad_layers))
        keepouts=keepouts+addKeepoutRect(l_fab + w_fab - cornerPadOffsetX, t_fab + cornerPadOffsetY, cornerPads[0]+keepout_addsize, cornerPads[1]+keepout_addsize)                              
        kicad_modg.append(Pad(number=pins + 1, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
                              at=[l_fab + cornerPadOffsetX, t_fab + h_fab - cornerPadOffsetY], size=cornerPads, drill=0,
                              layers=pad_layers))
        keepouts=keepouts+addKeepoutRect(l_fab + cornerPadOffsetX, t_fab + h_fab - cornerPadOffsetY, cornerPads[0]+keepout_addsize, cornerPads[1]+keepout_addsize)                              
        kicad_modg.append(Pad(number=pins + 1, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT,
                              at=[l_fab + w_fab - cornerPadOffsetX, t_fab + h_fab - cornerPadOffsetY], size=cornerPads,
                              drill=0, layers=pad_layers))        
        keepouts=keepouts+addKeepoutRect(l_fab + w_fab - cornerPadOffsetX, t_fab + h_fab - cornerPadOffsetY, cornerPads[0]+keepout_addsize, cornerPads[1]+keepout_addsize)                              
        
        

    # create FAB-layer
    bevelRectTL(kicad_modg, [l_fab, t_fab], [w_fab, h_fab], 'F.Fab', lw_fab)
    for sw in range(0, switches):
        x = pinrow_distance / 2
        y = sw * rm
        if (mode == 'Piano'):
            kicad_modg.append(
                RectLine(start=[l_fab, y - switch_height / 2], end=[l_fab - switch_width, y + switch_height / 2],
                         layer='F.Fab', width=lw_fab))
        else:
            kicad_modg.append(RectLine(start=[x - switch_width / 2, y - switch_height / 2],
                                       end=[x + switch_width / 2, y + switch_height / 2], layer='F.Fab', width=lw_fab))
            kicad_modg.append(RectFill(start=[x - switch_width / 2, y - switch_height / 2], end=[x - switch_width / 6, y + switch_height / 2], layer='F.Fab', width=lw_fab))
            kicad_modg.append(Line(start=[x - switch_width / 6, y - switch_height / 2], end=[x - switch_width / 6, y + switch_height / 2], layer='F.Fab', width=lw_fab))
    
    # create SILKSCREEN-layer
    if SOICStyleSilk and smd_pads:
        addHLineWithKeepout(kicad_modg, l_fab-slk_offset, l_fab + w_fab+slk_offset, t_slk + h_slk, layer='F.SilkS', width=lw_slk, keepouts=keepouts)
        if (overlen_top>0.5):
            addHLineWithKeepout(kicad_modg,-pad[0] / 2, l_fab-slk_offset, -pad[1] / 2-lw_slk-3*slk_offset, layer='F.SilkS', width=lw_slk, keepouts=keepouts)
            addVLineWithKeepout(kicad_modg, l_fab-slk_offset, t_slk, -pad[1] / 2-lw_slk-3*slk_offset, layer='F.SilkS', width=lw_slk, keepouts=keepouts)
            addHLineWithKeepout(kicad_modg, l_fab-slk_offset, l_fab + w_fab+slk_offset, t_slk, layer='F.SilkS', width=lw_slk, keepouts=keepouts)
            addVLineWithKeepout(kicad_modg, l_fab + w_fab+slk_offset, t_slk, t_slk+overlen_top, layer='F.SilkS', width=lw_slk, keepouts=keepouts)
        else:
            addHLineWithKeepout(kicad_modg, -pad[0] / 2, l_fab + w_fab+slk_offset, t_slk, layer='F.SilkS', width=lw_slk, keepouts=keepouts)
            
        if overlen_bottom>0.5:
            addVLineWithKeepout(kicad_modg, l_fab -slk_offset, t_slk+h_slk, t_slk+h_slk-overlen_bottom, layer='F.SilkS', width=lw_slk, keepouts=keepouts)
            addVLineWithKeepout(kicad_modg, l_fab + w_fab+slk_offset, t_slk+h_slk, t_slk+h_slk-overlen_bottom, layer='F.SilkS', width=lw_slk, keepouts=keepouts)
    else:
        addRectAndTLMarkWithKeepout(kicad_modg, l_slk, t_slk, w_slk, h_slk, min(max(0.5, pad[0]), rm*0.45), layer='F.SilkS', width=lw_slk, keepouts=keepouts)
        
        for sw in range(0, switches):
            x = pinrow_distance / 2
            y = sw * rm
            if (mode == 'Piano'):
                addRectWithKeepout(kicad_modg, l_slk - switch_width - slk_offset, y - switch_height / 2 - slk_offset, switch_width + slk_offset, switch_height+2*slk_offset, layer='F.SilkS', width=lw_slk)
            else:
                kicad_modg.append(RectLine(start=[x - switch_width / 2, y - switch_height / 2],
                                           end=[x + switch_width / 2, y + switch_height / 2], layer='F.SilkS',
                                           width=lw_slk))
                kicad_modg.append(
                    RectFill(start=[x - switch_width / 2, y - switch_height / 2], end=[x - switch_width / 6, y + switch_height / 2], layer='F.SilkS',
                         width=lw_slk))
                kicad_modg.append(
                    Line(start=[x - switch_width / 6, y - switch_height / 2], end=[x - switch_width / 6, y + switch_height / 2], layer='F.SilkS',
                         width=lw_slk))
    
    # create courtyard
    kicad_mod.append(RectLine(start=[roundCrt(l_crt + offset[0]), roundCrt(t_crt + offset[1])],
                              end=[roundCrt(l_crt + offset[0] + w_crt), roundCrt(t_crt + offset[1] + h_crt)],
                              layer='F.CrtYd', width=lw_crt))

    
    # add model
    kicad_modg.append(
        Model(filename="${KISYS3DMOD}/" + lib_name + ".3dshapes/" + footprint_name + ".wrl", at=offset3d, scale=scale3d, rotate=rotate3d))

    # print render tree
    # print(kicad_mod.getRenderTree())
    # print(kicad_mod.getCompleteRenderTree())
    
    # write file
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile(footprint_name + '.kicad_mod')
