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


def makeSMDCrystalAndHand(footprint_name, addSizeFootprintName, pins, pad_sep_x, pad_sep_y, pad, pack_width,
                          pack_height, pack_bevel, hasAdhesive=False, adhesivePos=[0, 0], adhesiveSize=1, style="rect",
                          description="Crystal SMD SMT", tags=[], lib_name="Crystals", offset3d=[0, 0, 0],
                          scale3d=[1, 1, 1], rotate3d=[0, 0, 0]):
    makeSMDCrystal(footprint_name, addSizeFootprintName, pins, pad_sep_x, pad_sep_y, pad, pack_width,
                   pack_height, pack_bevel, hasAdhesive, adhesivePos, adhesiveSize, style,
                   description, tags, lib_name, offset3d, scale3d, rotate3d)
    hsfactorx = 1.75
    hsfactory = 1
    if (pins == 2 and pack_width > pad_sep_x + pad[0]):
        hsfactorx = 1
        hsfactory = 1.75
    elif (pins == 4 and pack_width < pad_sep_x + pad[0] and pack_height < pad_sep_y + pad[1]):
        hsfactorx = 1.5
        hsfactory = 1.5
    elif (pins == 4 and pack_width > pad_sep_x + pad[0] and pack_height < pad_sep_y + pad[1]):
        hsfactorx = 1.1
        hsfactory = 1.5
    elif (pins == 4 and pack_width < pad_sep_x + pad[0] and pack_height > pad_sep_y + pad[1]):
        hsfactorx = 1.5
        hsfactory = 1.1
    
    makeSMDCrystal(footprint_name, addSizeFootprintName, pins, pad_sep_x + pad[0] * (hsfactorx - 1),
                   pad_sep_y + pad[1] * (hsfactory - 1), [pad[0] * hsfactorx, pad[1] * hsfactory], pack_width,
                   pack_height, pack_bevel, hasAdhesive, adhesivePos, adhesiveSize, style,
                   description + ", hand-soldering", tags + " hand-soldering", lib_name, offset3d, scale3d, rotate3d,
                   name_addition="_HandSoldering")


#
#          <----------pad_sep_x------------->
#        <----------pack_width-------------->
#  #=============#                   #=============#
#  |   4         |                   |         3   |
#  |     +----------------------------------+      |    ^            ^
#  |     |       |                   |      |      |    |            |
#  #=============#                   #=============#    |            |
#        |                                  |           |            |
#        |                                  |           pack_height  |
#        |                                  |           |            pad_sep_y
#        |                                  |           |            |
#  #=============#                   #=============#    |  ^         |
#  |     |       |                   |      |      |    |  |         |
#  |     +----------------------------------+      |    v  |         v
#  |   1         |                   |         2   |       pad[1]
#  #=============#                   #=============#       v
#                                    <---pad[0]---->
#
#
# pins=2,4
# style="rect"/"hc49"/"dip"
def makeSMDCrystal(footprint_name, addSizeFootprintName, pins, pad_sep_x, pad_sep_y, pad, pack_width, pack_height,
                   pack_bevel, hasAdhesive=False, adhesivePos=[0, 0], adhesiveSize=1, style="rect",
                   description="Crystal SMD SMT", tags=[], lib_name="Crystals", offset3d=[0, 0, 0], scale3d=[1, 1, 1],
                   rotate3d=[0, 0, 0], name_addition=""):
    fpname = footprint_name
    if addSizeFootprintName:
        fpname += "-{2}pin_{0:2.1f}x{1:2.1f}mm".format(pack_width, pack_height, pins)
    fpname = fpname + name_addition
    
    overpad_height = pad_sep_y + pad[1]
    overpad_width = pad_sep_x + pad[0]
    if pins == 3:
        overpad_height = pad_sep_y * 2 + pad[1]
        overpad_width = pad_sep_x * 2 + pad[0]
    
    betweenpads_x_slk = pad_sep_x - pad[0] - 2 * slk_offset
    betweenpads_y_slk = pad_sep_y - pad[1] - 2 * slk_offset
    overpads_x_slk = pad_sep_x + pad[0] + 2 * slk_offset
    overpads_y_slk = pad_sep_y + pad[1] + 2 * slk_offset
    if pins == 3:
        overpads_x_slk = pad_sep_x * 2 + pad[0] + 2 * slk_offset
        overpads_y_slk = pad_sep_y * 2 + pad[1] + 2 * slk_offset
    elif pins == 6:
        overpads_x_slk = pad_sep_x * 2 + pad[0] + 2 * slk_offset

    dip_size = 1
    
    mark_size = max(1.5*pack_bevel,1)
    upright_mark = False
    while pack_height < 2 * mark_size or pack_width < 2 * mark_size:
        mark_size = mark_size / 2
    
    if pack_bevel > 0 and math.fabs(mark_size / pack_bevel) > 0.7 and math.fabs(mark_size / pack_bevel) < 1.3:
        upright_mark = True
    
    h_fab = pack_height
    w_fab = pack_width
    l_fab = -w_fab / 2
    t_fab = -h_fab / 2
    r_fab = pack_width / 10
    
    h_slk = h_fab + 2 * slk_offset
    w_slk = w_fab + 2 * slk_offset
    l_slk = l_fab - slk_offset
    t_slk = t_fab - slk_offset
    dip_size_slk = dip_size
    
    mark_l_slk = -overpads_x_slk / 2
    if math.fabs(l_slk - mark_l_slk) < 2 * lw_slk:
        mark_l_slk = l_slk - 2 * lw_slk
    mark_b_slk = overpads_y_slk / 2
    if math.fabs(t_slk + h_slk - mark_b_slk) < 2 * lw_slk:
        mark_b_slk = t_slk + h_slk + 2 * lw_slk
    
    w_crt = max(overpad_width, pack_width) + 2 * crt_offset
    h_crt = max(overpad_height, pack_height) + 2 * crt_offset
    l_crt = -w_crt / 2
    t_crt = -h_crt / 2
    
    print(fpname)
    
    desc = description + ", {0:2.1f}x{1:2.1f}mm^2 package".format(pack_width, pack_height)
    tag_s = tags + " {0:2.1f}x{1:2.1f}mm^2 package".format(pack_width, pack_height)
    
    # init kicad footprint
    kicad_mod = Footprint(fpname)
    kicad_mod.setDescription(desc)
    kicad_mod.setTags(tags)
    
    # anchor for SMD-symbols is in the center, for THT-sybols at pin1
    kicad_mod.setAttribute('smd')
    offset = [0, 0]
    kicad_modg = kicad_mod
    
    # set general values
    kicad_modg.append(
        Text(type='reference', text='REF**', at=[0, min(t_slk, -overpad_height / 2, -pack_height / 2) - txt_offset],
             layer='F.SilkS'))
    # kicad_modg.append(Text(type='user', text='%R', at=[0, min(t_slk,-overpad_height/2,-pack_height/2)-txt_offset], layer='F.Fab'))
    kicad_modg.append(
        Text(type='value', text=fpname, at=[0, max(t_slk + h_slk, overpad_height / 2, pack_height / 2) + txt_offset],
             layer='F.Fab'))
    
    # create FAB-layer
    if style == 'hc49':
        THTQuartzRect(kicad_modg, [l_fab, t_fab], [w_fab, h_fab], [w_fab * 0.9, h_fab * 0.9], 'F.Fab', lw_fab)
    elif style == 'dip':
        DIPRectL(kicad_modg, [l_fab, t_fab], [w_fab, h_fab], 'F.Fab', lw_fab, dip_size)
    elif style == 'rect1bevel':
        bevelRectBL(kicad_modg, [l_fab, t_fab], [w_fab, h_fab], 'F.Fab', lw_fab, dip_size)
    else:
        allBevelRect(kicad_modg, [l_fab, t_fab], [w_fab, h_fab], 'F.Fab', lw_fab, pack_bevel)
        if upright_mark:
            kicad_modg.append(Line(start=[l_fab + max(mark_size, pack_bevel), t_fab],
                                   end=[l_fab + max(mark_size, pack_bevel), t_fab + h_fab], layer='F.Fab',
                                   width=lw_fab))
        else:
            kicad_modg.append(
                Line(start=[l_fab, t_fab + h_fab - mark_size], end=[l_fab + mark_size, t_fab + h_fab], layer='F.Fab',
                     width=lw_fab))
    
    # create SILKSCREEN-layer
    if pins == 2:
        if pack_height < pad[1]:
            kicad_modg.append(
                Line(start=[-betweenpads_x_slk / 2, t_slk], end=[betweenpads_x_slk / 2, t_slk], layer='F.SilkS',
                     width=lw_slk))
            kicad_modg.append(
                Line(start=[-betweenpads_x_slk / 2, t_slk + h_slk], end=[betweenpads_x_slk / 2, t_slk + h_slk],
                     layer='F.SilkS', width=lw_slk))
            # pin1 mark
            kicad_modg.append(Line(start=[min(l_slk, -overpads_x_slk / 2), -pad[1] / 2],
                                   end=[min(l_slk, -overpads_x_slk / 2), pad[1] / 2], layer='F.SilkS', width=lw_slk))
        else:
            kicad_modg.append(PolygoneLine(polygone=[[l_slk + w_slk, t_slk],
                                                     [-overpads_x_slk / 2, t_slk],
                                                     [-overpads_x_slk / 2, t_slk + h_slk],
                                                     [l_slk + w_slk, t_slk + h_slk], ], layer='F.SilkS', width=lw_slk))
    elif pins == 3:
        if (pack_height < overpad_height and pack_width > overpad_width):
            kicad_modg.append(PolygoneLine(polygone=[[overpads_x_slk / 2, t_slk],
                                                     [l_slk + w_slk, t_slk],
                                                     [l_slk + w_slk, t_slk + h_slk],
                                                     [overpads_x_slk / 2, t_slk + h_slk]], layer='F.SilkS',
                                           width=lw_slk))
            kicad_modg.append(Line(start=[l_slk - 2 * lw_slk, t_slk],
                                   end=[l_slk - 2 * lw_slk, t_slk + h_slk], layer='F.SilkS', width=lw_slk))
            
            kicad_modg.append(PolygoneLine(polygone=[[-overpads_x_slk / 2, mark_b_slk],
                                                     [-overpads_x_slk / 2, t_slk + h_slk],
                                                     [l_slk, t_slk + h_slk],
                                                     [l_slk, t_slk],
                                                     [-overpads_x_slk / 2, t_slk]], layer='F.SilkS',
                                           width=lw_slk))
        
        else:
            kicad_modg.append(PolygoneLine(polygone=[[-overpads_x_slk / 2, -overpads_y_slk / 2],
                                                     [-overpads_x_slk / 2, overpads_y_slk / 2],
                                                     [overpads_x_slk / 2, overpads_y_slk / 2]], layer='F.SilkS',
                                           width=lw_slk))
    elif pins >= 4:
        if (betweenpads_y_slk < 5 * lw_slk or betweenpads_x_slk < 5 * lw_slk) and (pack_height < overpad_height and pack_width < overpad_width):
            kicad_modg.append(PolygoneLine(polygone=[[-overpads_x_slk / 2, -overpads_y_slk / 2],
                                                     [-overpads_x_slk / 2, overpads_y_slk / 2],
                                                     [overpads_x_slk / 2, overpads_y_slk / 2]], layer='F.SilkS',
                                           width=lw_slk))
        else:
            if (pack_height < overpad_height and pack_width < overpad_width):
                
                kicad_modg.append(PolygoneLine(polygone=[[mark_l_slk, betweenpads_y_slk / 2],
                                                         [l_slk, betweenpads_y_slk / 2],
                                                         [l_slk, -betweenpads_y_slk / 2]], layer='F.SilkS',
                                               width=lw_slk))
                kicad_modg.append(PolygoneLine(polygone=[[l_slk + w_slk, -betweenpads_y_slk / 2],
                                                         [l_slk + w_slk, betweenpads_y_slk / 2]], layer='F.SilkS',
                                               width=lw_slk))
                if pins == 4:
                    kicad_modg.append(PolygoneLine(polygone=[[-betweenpads_x_slk / 2, t_slk],
                                                         [betweenpads_x_slk / 2, t_slk]], layer='F.SilkS',
                                               width=lw_slk))
                    kicad_modg.append(PolygoneLine(polygone=[[betweenpads_x_slk / 2, t_slk + h_slk],
                                                         [-betweenpads_x_slk / 2, t_slk + h_slk],
                                                         [-betweenpads_x_slk / 2, mark_b_slk]], layer='F.SilkS',
                                               width=lw_slk))
            elif (pack_height < overpad_height and pack_width > overpad_width):
                kicad_modg.append(PolygoneLine(polygone=[[overpads_x_slk / 2, t_slk],
                                                         [l_slk + w_slk, t_slk],
                                                         [l_slk + w_slk, t_slk + h_slk],
                                                         [overpads_x_slk / 2, t_slk + h_slk]], layer='F.SilkS',
                                               width=lw_slk))
                if pins == 4:
                    kicad_modg.append(PolygoneLine(polygone=[[-betweenpads_x_slk / 2, t_slk],
                                                         [betweenpads_x_slk / 2, t_slk]], layer='F.SilkS',
                                               width=lw_slk))
                if style == 'dip':
                    DIPRectL_LeftOnly(kicad_modg, [l_slk, t_slk], [(w_slk - overpads_x_slk) / 2, h_slk], 'F.SilkS',
                                      lw_slk, dip_size_slk)
                    kicad_modg.append(
                        Line(start=[betweenpads_x_slk / 2, t_slk + h_slk], end=[-betweenpads_x_slk / 2, t_slk + h_slk],
                             layer='F.SilkS',
                             width=lw_slk))
                else:
                    kicad_modg.append(PolygoneLine(polygone=[[-overpads_x_slk / 2, mark_b_slk],
                                                             [-overpads_x_slk / 2, t_slk + h_slk],
                                                             [l_slk, t_slk + h_slk],
                                                             [l_slk, t_slk],
                                                             [-overpads_x_slk / 2, t_slk]], layer='F.SilkS',
                                                   width=lw_slk))
                    if pins==4:
                        kicad_modg.append(PolygoneLine(polygone=[[betweenpads_x_slk / 2, t_slk + h_slk],
                                                             [-betweenpads_x_slk / 2, t_slk + h_slk],
                                                             [-betweenpads_x_slk / 2, mark_b_slk]], layer='F.SilkS',
                                                   width=lw_slk))
            
            elif (pack_height > overpad_height and pack_width < overpad_width):
                kicad_modg.append(PolygoneLine(polygone=[[l_slk, -overpads_y_slk / 2],
                                                         [l_slk, t_slk],
                                                         [l_slk + w_slk, t_slk],
                                                         [l_slk + w_slk, -overpads_y_slk / 2]], layer='F.SilkS',
                                               width=lw_slk))
                kicad_modg.append(PolygoneLine(polygone=[[mark_l_slk, overpads_y_slk / 2],
                                                         [l_slk, overpads_y_slk / 2],
                                                         [l_slk, t_slk + h_slk],
                                                         [l_slk + w_slk, t_slk + h_slk],
                                                         [l_slk + w_slk, overpads_y_slk / 2]], layer='F.SilkS',
                                               width=lw_slk))
                if pins == 4:
                    kicad_modg.append(PolygoneLine(polygone=[[mark_l_slk, betweenpads_y_slk / 2],
                                                             [l_slk, betweenpads_y_slk / 2],
                                                             [l_slk, -betweenpads_y_slk / 2]], layer='F.SilkS',
                                                   width=lw_slk))
                    kicad_modg.append(PolygoneLine(polygone=[[l_slk + w_slk, -betweenpads_y_slk / 2],
                                                             [l_slk + w_slk, betweenpads_y_slk / 2]], layer='F.SilkS',
                                                   width=lw_slk))
    
    # create courtyard
    kicad_mod.append(RectLine(start=[roundCrt(l_crt + offset[0]), roundCrt(t_crt + offset[1])],
                              end=[roundCrt(l_crt + offset[0] + w_crt), roundCrt(t_crt + offset[1] + h_crt)],
                              layer='F.CrtYd', width=lw_crt))
    
    # create pads
    pad_type = Pad.TYPE_SMT
    pad_shape1 = Pad.SHAPE_RECT
    pad_layers = 'F'
    ddrill = 0
    
    if (pins == 2):
        kicad_modg.append(Pad(number=1, type=pad_type, shape=pad_shape1, at=[-pad_sep_x / 2, 0], size=pad, drill=ddrill,
                              layers=[pad_layers + '.Cu', pad_layers + '.Mask']))
        kicad_modg.append(Pad(number=2, type=pad_type, shape=pad_shape1, at=[pad_sep_x / 2, 0], size=pad, drill=ddrill,
                              layers=[pad_layers + '.Cu', pad_layers + '.Mask']))
    elif (pins == 3):
        kicad_modg.append(Pad(number=1, type=pad_type, shape=pad_shape1, at=[-pad_sep_x, 0], size=pad, drill=ddrill,
                              layers=[pad_layers + '.Cu', pad_layers + '.Mask']))
        kicad_modg.append(Pad(number=2, type=pad_type, shape=pad_shape1, at=[0, 0], size=pad, drill=ddrill,
                              layers=[pad_layers + '.Cu', pad_layers + '.Mask']))
        kicad_modg.append(Pad(number=3, type=pad_type, shape=pad_shape1, at=[pad_sep_x, 0], size=pad, drill=ddrill,
                              layers=[pad_layers + '.Cu', pad_layers + '.Mask']))
    elif (pins == 4):
        kicad_modg.append(
            Pad(number=1, type=pad_type, shape=pad_shape1, at=[-pad_sep_x / 2, pad_sep_y / 2], size=pad, drill=ddrill,
                layers=[pad_layers + '.Cu', pad_layers + '.Mask']))
        kicad_modg.append(
            Pad(number=2, type=pad_type, shape=pad_shape1, at=[pad_sep_x / 2, pad_sep_y / 2], size=pad, drill=ddrill,
                layers=[pad_layers + '.Cu', pad_layers + '.Mask']))
        kicad_modg.append(
            Pad(number=3, type=pad_type, shape=pad_shape1, at=[pad_sep_x / 2, -pad_sep_y / 2], size=pad, drill=ddrill,
                layers=[pad_layers + '.Cu', pad_layers + '.Mask']))
        kicad_modg.append(
            Pad(number=4, type=pad_type, shape=pad_shape1, at=[-pad_sep_x / 2, -pad_sep_y / 2], size=pad, drill=ddrill,
                layers=[pad_layers + '.Cu', pad_layers + '.Mask']))

    elif (pins == 6):
        kicad_modg.append(
            Pad(number=1, type=pad_type, shape=pad_shape1, at=[-pad_sep_x , pad_sep_y / 2], size=pad, drill=ddrill,
                layers=[pad_layers + '.Cu', pad_layers + '.Mask']))
        kicad_modg.append(
            Pad(number=2, type=pad_type, shape=pad_shape1, at=[0, pad_sep_y / 2], size=pad, drill=ddrill,
                layers=[pad_layers + '.Cu', pad_layers + '.Mask']))
        kicad_modg.append(
            Pad(number=3, type=pad_type, shape=pad_shape1, at=[pad_sep_x , pad_sep_y / 2], size=pad, drill=ddrill,
                layers=[pad_layers + '.Cu', pad_layers + '.Mask']))
        kicad_modg.append(
            Pad(number=4, type=pad_type, shape=pad_shape1, at=[pad_sep_x , -pad_sep_y / 2], size=pad, drill=ddrill,
                layers=[pad_layers + '.Cu', pad_layers + '.Mask']))
        kicad_modg.append(
            Pad(number=5, type=pad_type, shape=pad_shape1, at=[0, -pad_sep_y / 2], size=pad, drill=ddrill,
                layers=[pad_layers + '.Cu', pad_layers + '.Mask']))
        kicad_modg.append(
            Pad(number=6, type=pad_type, shape=pad_shape1, at=[-pad_sep_x, -pad_sep_y / 2], size=pad, drill=ddrill,
                layers=[pad_layers + '.Cu', pad_layers + '.Mask']))

    if hasAdhesive:
        fillCircle(kicad_modg, center=adhesivePos, radius=adhesiveSize / 2, width=0.1, layer='F.Adhes')
    
    # add model
    kicad_modg.append(
        Model(filename=lib_name + ".3dshapes/" + fpname + ".wrl", at=offset3d, scale=scale3d, rotate=rotate3d))
    
    # print render tree
    # print(kicad_mod.getRenderTree())
    # print(kicad_mod.getCompleteRenderTree())
    
    # write file
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile(fpname + '.kicad_mod')


def makeCrystalAll(footprint_name, rm, pad_size, ddrill, pack_width, pack_height, pack_offset, pack_rm, style="flat",
                   package_pad=False, package_pad_add_holes=False, package_pad_offset=0, package_pad_size=[0, 0],
                   package_pad_drill_size=[1.2, 1.2], package_pad_ddrill=0.8, description="Crystal THT",
                   lib_name="Crystals", tags="", offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0],
                   name_addition="", pad_style="tht", script3d="", height3d=4.65, iheight3d=4):
    makeCrystal(footprint_name, rm, pad_size, ddrill, pack_width, pack_height, pack_offset, pack_rm, style,
                False, False, package_pad_offset, package_pad_size,
                package_pad_drill_size, package_pad_ddrill, description,
                lib_name, tags, offset3d, scale3d, rotate3d,
                name_addition, pad_style, script3d, height3d, iheight3d)
    if package_pad:
        makeCrystal(footprint_name, rm, pad_size, ddrill, pack_width, pack_height, pack_offset, pack_rm, style,
                    True, False, package_pad_offset, package_pad_size,
                    package_pad_drill_size, package_pad_ddrill, description,
                    lib_name, tags, offset3d, scale3d, rotate3d,
                    name_addition + "_1EP_style1", pad_style, script3d, height3d, iheight3d)
    if package_pad_add_holes and package_pad:
        makeCrystal(footprint_name, rm, pad_size, ddrill, pack_width, pack_height, pack_offset, pack_rm, style,
                    True, True, package_pad_offset, package_pad_size,
                    package_pad_drill_size, package_pad_ddrill, description,
                    lib_name, tags, offset3d, scale3d, rotate3d,
                    name_addition + "_1EP_style2", pad_style, script3d, height3d, iheight3d)


#                    +---------------------------------------------------------------+   ^
#   OOOOO            |                                                               |   |
#   OO1OO----^---    |                                                               |   |
#   OOOOO    |   ----+ ^                                                             |   |
#            |       | |                                                             |   |
#           rm       | pack_rm                                                       |   pack_height
#            |       | |                                                             |   |
#   OOOOO    |   ----+ v                                                             |   |
#   OO2OO ---v---    |                                                               |   |
#   OOOOO            |                                                               |   |
#                    +---------------------------------------------------------------+   v
#                    <-----------------pack_width------------------------------------>
#     <------------->pack_offset
#
#
# pins=2,3
# style="flat"/"hc49"
# pad_style=tht/smd for pin 1/2
def makeCrystal(footprint_name, rm, pad_size, ddrill, pack_width, pack_height, pack_offset, pack_rm, style="flat",
                package_pad=False, package_pad_add_holes=False, package_pad_offset=0, package_pad_size=[0, 0],
                package_pad_drill_size=[1.2, 1.2], package_pad_ddrill=0.8, description="Crystal THT",
                lib_name="Crystals", tags="", offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0],
                name_addition="", pad_style="tht", script3d="", height3d=4.65, iheight3d=4):
    fpname = footprint_name
    fpname = fpname + name_addition
    
    if type(pad_size) is list:
        pad=[pad_size[1],pad_size[0]]
    else:
        pad = [pad_size, pad_size]
    
    pad3pos = [rm / 2, package_pad_offset + package_pad_size[0] / 2]
    pad3dril_xoffset = package_pad_size[1] / 2 + package_pad_ddrill / 2
    
    
    h_fab = pack_width
    w_fab = pack_height
    l_fab = -(w_fab - rm) / 2
    t_fab = pack_offset
    
    h_slk = h_fab + 2 * slk_offset
    w_slk = w_fab + 2 * slk_offset
    l_slk = l_fab - slk_offset
    t_slk = t_fab - slk_offset
    
    bev = 0
    if style == "hc49":
        bev = min(0.35, max(2 * lw_slk, w_slk / 7))
    
    slk_u_line=False
    if package_pad:
        if (package_pad_size[1] < pack_width / 2):
            h_slk=math.fabs((pad3pos[1]-package_pad_size[0]/2-slk_offset)-t_slk)
            slk_u_line = True
        else:
            h_slk = max(t_slk + h_slk, pad3pos[1] + package_pad_size[0] / 2 + slk_offset) - t_slk
        l_slk = min(l_slk, rm / 2 - package_pad_size[1] / 2 - slk_offset)
        w_slk = max(l_slk+w_slk, rm / 2 + package_pad_size[1] / 2 + slk_offset)-l_slk
        if package_pad_add_holes:
            l_crt = pad3pos[0] - pad3dril_xoffset - package_pad_drill_size[0] / 2 - crt_offset
            
    
    
    extra_textoffset = 0
    if (l_slk>-(pad[0]/2+slk_offset+lw_slk)):
        extra_textoffset=pad[0]/2+slk_offset+lw_slk-0.5
    
    t_crt = -pad[1] / 2 - crt_offset
    w_crt = max(pack_height + 2 * bev + 4 * crt_offset, pad[0] + rm, w_slk) + 2 * crt_offset
    h_crt = max(t_slk + h_slk - t_crt, pad3pos[1] + package_pad_size[0] / 2-t_crt-crt_offset,pack_width + pack_offset+pad[1]/2) + 2 * crt_offset
    l_crt = rm / 2 - w_crt / 2
    
    if package_pad and package_pad_add_holes and (pad[1]<pack_width/2):
        l_crt = min(l_crt, pad3pos[0] - pad3dril_xoffset - package_pad_drill_size[0] / 2 - crt_offset)
        w_crt = max(w_crt, pad3pos[0] + pad3dril_xoffset + package_pad_drill_size[0] / 2 + crt_offset - l_crt)
    
    print(fpname)
    
    

    if script3d!="":
        with open(script3d, "a") as myfile:
            myfile.write("\n\n # {0}\n".format(footprint_name))
            myfile.write("import FreeCAD\n")
            myfile.write("import os\n")
            myfile.write("import os.path\n\n")
            myfile.write("# d_wire\nApp.ActiveDocument.Spreadsheet.set('B5', '0.02')\n")
            myfile.write("App.ActiveDocument.recompute()\n")
            myfile.write("# W\nApp.ActiveDocument.Spreadsheet.set('B1', '{0}')\n".format(pack_width) )
            myfile.write("# Wi\nApp.ActiveDocument.Spreadsheet.set('C1', '{0}')\n".format(int(pack_width*0.96)) )
            myfile.write("# H\nApp.ActiveDocument.Spreadsheet.set('B2', '{0}')\n".format(pack_height))
            myfile.write("# Hi\nApp.ActiveDocument.Spreadsheet.set('C2', '{0}')\n".format(int(pack_height*0.96)))
            myfile.write("# height3d\nApp.ActiveDocument.Spreadsheet.set('B3', '{0}')\n".format(height3d))
            myfile.write("# iheight3d\nApp.ActiveDocument.Spreadsheet.set('C3', '{0}')\n".format(iheight3d))
            myfile.write("# RM\nApp.ActiveDocument.Spreadsheet.set('B4', '{0}')\n".format(rm))
            myfile.write("# d_wire\nApp.ActiveDocument.Spreadsheet.set('B5', '{0}')\n".format(ddrill-0.3))
            myfile.write("# pack_offset\nApp.ActiveDocument.Spreadsheet.set('B6', '{0}')\n".format(pack_offset))
            myfile.write("# pack_rm\nApp.ActiveDocument.Spreadsheet.set('B7', '{0}')\n".format(pack_rm))
            myfile.write("App.ActiveDocument.recompute()\n")
            myfile.write("doc = FreeCAD.activeDocument()\n")
            myfile.write("__objs__=[]\n")
            myfile.write("for obj in doc.Objects:	\n")
            myfile.write("    if obj.ViewObject.Visibility:\n")
            myfile.write("        __objs__.append(obj)\n")
            myfile.write("\nFreeCADGui.export(__objs__,os.path.split(doc.FileName)[0]+os.sep+\"{0}.wrl\")\n".format(fpname))
            myfile.write("doc.saveCopy(os.path.split(doc.FileName)[0]+os.sep+\"{0}.FCStd\")\n".format(fpname))
            myfile.write("print(\"created {0}\")\n".format(fpname))
    
    desc = description
    tag_s = tags
    
    # init kicad footprint
    kicad_mod = Footprint(fpname)
    kicad_mod.setDescription(desc)
    kicad_mod.setTags(tags)
    
    offset = [0, 0]
    if pad_style == "smd":
        offset = [-rm / 2, -pad3pos[1]/2];
        kicad_mod.setAttribute('smd')
        kicad_modg = Translation(offset[0], offset[1])
        kicad_mod.append(kicad_modg)
    else:
        kicad_modg = kicad_mod
    
    # set general values
    kicad_modg.append(
        Text(type='reference', text='REF**', at=[l_slk - bev / 2 - txt_offset-extra_textoffset, t_crt + h_crt / 4], layer='F.SilkS',
             rotation=90))
    kicad_modg.append(
        Text(type='value', text=fpname, at=[l_slk + w_slk + txt_offset+extra_textoffset + bev / 2, t_crt + h_crt / 4], layer='F.Fab',
             rotation=90))
    
    # create FAB-layer
    kicad_modg.append(RectLine(start=[l_fab, t_fab],
                                   end=[l_fab + w_fab, t_fab + h_fab], layer='F.Fab', width=lw_fab))
    kicad_modg.append(PolygoneLine(polygone=[[l_fab + w_fab / 2 - pack_rm / 2, t_fab],
                                             [0, t_fab/2],
                                             [0, 0]], layer='F.Fab', width=lw_fab))
    kicad_modg.append(PolygoneLine(polygone=[[l_fab + w_fab / 2 + pack_rm / 2, t_fab],
                                             [rm, t_fab/2],
                                             [rm, 0]], layer='F.Fab', width=lw_fab))
    if package_pad and package_pad_add_holes:
        kicad_modg.append(
            Line(start=[pad3pos[0] - pad3dril_xoffset, pad3pos[1]], end=[pad3pos[0] + pad3dril_xoffset, pad3pos[1]],
                 layer='F.Fab', width=lw_fab))
    if style == "hc49":
        kicad_modg.append(RectLine(start=[l_fab - bev, t_fab], end=[l_fab + w_fab + bev, t_fab - lw_fab], layer='F.Fab',
                                   width=lw_fab))
    # create SILKSCREEN-layer
    if package_pad and package_pad_add_holes:
        kicad_modg.append(PolygoneLine(polygone=[[l_slk, pad3pos[1] - package_pad_drill_size[1] / 2 - slk_offset],
                                                 [l_slk, t_slk],
                                                 [l_slk + w_slk, t_slk],
                                                 [l_slk + w_slk,
                                                  pad3pos[1] - package_pad_drill_size[1] / 2 - slk_offset]],
                                       layer='F.SilkS', width=lw_slk))
    else:
        if slk_u_line:
            kicad_modg.append(PolygoneLine(polygone=[[l_slk, t_slk + h_slk],
                                                     [l_slk, t_slk],
                                                     [l_slk + w_slk, t_slk],
                                                     [l_slk + w_slk, t_slk + h_slk]], layer='F.SilkS', width=lw_slk))
        else:
            kicad_modg.append(
                RectLine(start=[l_slk, t_slk], end=[l_slk + w_slk, t_slk + h_slk], layer='F.SilkS', width=lw_slk))
    kicad_modg.append(PolygoneLine(polygone=[[l_slk + w_slk / 2 - pack_rm / 2, t_slk], [0, max(t_slk/2,pad[1] / 2 + slk_offset)], [0, pad[1] / 2 + slk_offset]], layer='F.SilkS',width=lw_slk))
    kicad_modg.append(PolygoneLine(polygone=[[l_slk + w_slk / 2 + pack_rm / 2, t_slk], [rm, max(t_slk/2,pad[1] / 2 + slk_offset)], [rm, pad[1] / 2 + slk_offset]], layer='F.SilkS',width=lw_slk))
    if style == "hc49":
        kicad_modg.append(
            RectLine(start=[l_slk - bev, t_slk], end=[l_slk + w_slk + bev, t_slk - lw_slk], layer='F.SilkS',
                     width=lw_slk))
    
    # create courtyard
    kicad_mod.append(RectLine(start=[roundCrt(l_crt + offset[0]), roundCrt(t_crt + offset[1])],
                              end=[roundCrt(l_crt + w_crt + offset[0]), roundCrt(t_crt + h_crt + offset[1])],
                              layer='F.CrtYd', width=lw_crt))
    
    # create pads
    pad_type = Pad.TYPE_THT
    pad_shape1 = Pad.SHAPE_CIRCLE
    pad_layers = '*'
    if pad_style == "smd":
        kicad_modg.append(Pad(number=1, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, at=[0, 0], size=pad, drill=0,
                              layers=['F.Cu', 'F.Mask']))
        kicad_modg.append(Pad(number=2, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, at=[rm, 0], size=pad, drill=0,
                              layers=['F.Cu', 'F.Mask']))
    else:
        kicad_modg.append(Pad(number=1, type=pad_type, shape=pad_shape1, at=[0, 0], size=pad, drill=ddrill,
                              layers=[pad_layers + '.Cu', pad_layers + '.Mask']))
        kicad_modg.append(Pad(number=2, type=pad_type, shape=pad_shape1, at=[rm, 0], size=pad, drill=ddrill,
                              layers=[pad_layers + '.Cu', pad_layers + '.Mask']))
    
    if package_pad:
        kicad_modg.append(Pad(number=3, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, at=pad3pos,
                              size=[package_pad_size[1], package_pad_size[0]], drill=0, layers=['F.Cu', 'F.Mask']))
        if package_pad_add_holes:
            kicad_modg.append(
                Pad(number=3, type=Pad.TYPE_THT, shape=Pad.SHAPE_RECT, at=[pad3pos[0] - pad3dril_xoffset, pad3pos[1]],
                    size=package_pad_drill_size, drill=package_pad_ddrill,
                    layers=[pad_layers + '.Cu', pad_layers + '.Mask']))
            kicad_modg.append(
                Pad(number=3, type=Pad.TYPE_THT, shape=Pad.SHAPE_RECT, at=[pad3pos[0] + pad3dril_xoffset, pad3pos[1]],
                    size=package_pad_drill_size, drill=package_pad_ddrill,
                    layers=[pad_layers + '.Cu', pad_layers + '.Mask']))
    
    # add model
    kicad_modg.append(
        Model(filename=lib_name + ".3dshapes/" + fpname + ".wrl", at=offset3d, scale=scale3d, rotate=rotate3d))
    
    # print render tree
    # print(kicad_mod.getRenderTree())
    # print(kicad_mod.getCompleteRenderTree())
    
    # write file
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile(fpname + '.kicad_mod')


#      +----------------------------------------------------+       ^
#    /                                                       \      |
#   /       OOOOO                              OOOOO          \     |
#  |        OOOOO                              OOOOO          |     pack_height
#   \       OOOOO                              OOOOO         /      |
#    \                                                      /       |
#      +----------------------------------------------------+       v
#  <-------------------------pack_width----------------------->
#              <-------------rm------------------>
#
#
# pins=2,3
def makeCrystalHC49Vert(footprint_name, pins, rm, pad_size, ddrill, pack_width, pack_height, innerpack_width, innerpack_height,
                description="Crystal THT", lib_name="Crystals", tags="", offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0], addSizeFootprintName=False,
                        script3d="", height3d=10):
    fpname = footprint_name
    desc = description
    tag_s = tags

    if addSizeFootprintName:
        fpname += "-{2}pin_w{0:2.1f}mm_h{1:2.1f}mm".format(pack_width, pack_height, pins)
        desc = description + ", length*width={0:2.1f}x{1:2.1f}mm^2 package, package length={0:2.1f}mm, package width={1:2.1f}mm, {2} pins".format(pack_width, pack_height,pins)
        tag_s = tags + " {0:2.1f}x{1:2.1f}mm^2 package length {0:2.1f}mm width {1:2.1f}mm {2} pins".format(pack_width, pack_height,pins)
    
    if type(pad_size) is list:
        pad = [pad_size[1], pad_size[0]]
    else:
        pad = [pad_size, pad_size]
        
    centerpos=[rm/2,0]
    pin1pos=[0,0]
    pin2pos=[rm,0]
    pin3pos = [rm / 2, 0]
    if (pins==3):
        pin2pos = [rm/2, 0]
        pin3pos = [rm, 0]
        
        

    w_fab = pack_width
    h_fab = pack_height
    l_fab = -(w_fab - rm) / 2
    t_fab = -h_fab/2
    iw_fab = innerpack_width
    ih_fab = innerpack_height
    il_fab = -(iw_fab - rm) / 2
    it_fab = -ih_fab/2


    incomplete_slk=False
    h_slk = h_fab + 2 * slk_offset
    w_slk = w_fab + 2 * slk_offset
    l_slk = l_fab - slk_offset
    t_slk = t_fab - slk_offset
    
    l_crt=l_slk-crt_offset
    t_crt=t_slk-crt_offset
    w_crt=w_slk+2*crt_offset
    h_crt = h_slk + 2 * crt_offset
    
    if pack_width<rm+pad[0]:
        l_crt = min(-pad[0]/2, l_fab) - crt_offset
        w_crt = max(rm+pad[0], w_fab)+2*slk_offset
        incomplete_slk = True
        angle_slk=math.acos((pad[1]/2+slk_offset)/(h_slk/2))/3.1415*180
    
    print(fpname)
    

    if script3d!="":
        with open(script3d, "a") as myfile:
            myfile.write("\n\n # {0}\n".format(footprint_name))
            myfile.write("import FreeCAD\n")
            myfile.write("import os\n")
            myfile.write("import os.path\n\n")
            myfile.write("# d_wire\nApp.ActiveDocument.Spreadsheet.set('B5', '0.02')\n")
            myfile.write("App.ActiveDocument.recompute()\n")
            myfile.write("# W\nApp.ActiveDocument.Spreadsheet.set('B1', '{0}')\n".format(pack_width) )
            myfile.write("# Wi\nApp.ActiveDocument.Spreadsheet.set('C1', '{0}')\n".format(innerpack_width) )
            myfile.write("# H\nApp.ActiveDocument.Spreadsheet.set('B2', '{0}')\n".format(pack_height))
            myfile.write("# Hi\nApp.ActiveDocument.Spreadsheet.set('C2', '{0}')\n".format(innerpack_height))
            myfile.write("# height3d\nApp.ActiveDocument.Spreadsheet.set('B3', '{0}')\n".format(height3d))
            myfile.write("# RM\nApp.ActiveDocument.Spreadsheet.set('B4', '{0}')\n".format(rm))
            myfile.write("# d_wire\nApp.ActiveDocument.Spreadsheet.set('B5', '{0}')\n".format(ddrill-0.3))
            myfile.write("App.ActiveDocument.recompute()\n")
            myfile.write("doc = FreeCAD.activeDocument()\n")
            myfile.write("__objs__=[]\n")
            myfile.write("for obj in doc.Objects:	\n")
            myfile.write("    if obj.ViewObject.Visibility:\n")
            myfile.write("        __objs__.append(obj)\n")
            myfile.write("\nFreeCADGui.export(__objs__,os.path.split(doc.FileName)[0]+os.sep+\"{0}.wrl\")\n".format(fpname))
            myfile.write("doc.saveCopy(os.path.split(doc.FileName)[0]+os.sep+\"{0}.FCStd\")\n".format(fpname))
            myfile.write("print(\"created {0}\")\n".format(fpname))

    
    # init kicad footprint
    kicad_mod = Footprint(fpname)
    kicad_mod.setDescription(desc)
    kicad_mod.setTags(tags)
    
    offset = [0, 0]
    kicad_modg = kicad_mod
    
    # set general values
    kicad_modg.append(Text(type='reference', text='REF**', at=[centerpos[0], t_slk-txt_offset], layer='F.SilkS'))
    kicad_modg.append(Text(type='value', text=fpname, at=[centerpos[0], t_slk+h_slk+txt_offset], layer='F.Fab'))
    
    # create FAB-layer
    THTQuartz(kicad_modg, [l_fab,t_fab], [w_fab,h_fab], 'F.Fab', lw_fab)
    THTQuartz(kicad_modg, [il_fab,it_fab], [iw_fab,ih_fab], 'F.Fab', lw_fab)


    # create SILKSCREEN-layer
    if incomplete_slk:
        THTQuartzIncomplete(kicad_modg, [l_slk, t_slk], [w_slk, h_slk], angle_slk, 'F.SilkS', lw_slk)
    else:
        THTQuartz(kicad_modg, [l_slk,t_slk], [w_slk,h_slk], 'F.SilkS', lw_slk)
    
    # create courtyard
    kicad_mod.append(RectLine(start=[roundCrt(l_crt + offset[0]), roundCrt(t_crt + offset[1])],
                              end=[roundCrt(l_crt + w_crt + offset[0]), roundCrt(t_crt + h_crt + offset[1])],
                              layer='F.CrtYd', width=lw_crt))
    
    # create pads
    pad_type = Pad.TYPE_THT
    pad_shape1 = Pad.SHAPE_CIRCLE
    pad_layers = '*'

    kicad_modg.append(Pad(number=1, type=pad_type, shape=pad_shape1, at=pin1pos, size=pad, drill=ddrill,
                          layers=[pad_layers + '.Cu', pad_layers + '.Mask']))
    kicad_modg.append(Pad(number=2, type=pad_type, shape=pad_shape1, at=pin2pos, size=pad, drill=ddrill,
                          layers=[pad_layers + '.Cu', pad_layers + '.Mask']))
    if pins==3:
        kicad_modg.append(Pad(number=3, type=pad_type, shape=pad_shape1, at=pin3pos, size=pad, drill=ddrill,
                              layers=[pad_layers + '.Cu', pad_layers + '.Mask']))
    
    # add model
    kicad_modg.append(
        Model(filename=lib_name + ".3dshapes/" + fpname + ".wrl", at=offset3d, scale=scale3d, rotate=rotate3d))
    
    # print render tree
    # print(kicad_mod.getRenderTree())
    # print(kicad_mod.getCompleteRenderTree())
    
    # write file
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile(fpname + '.kicad_mod')


#       +---------------------------------------+       
#      /                                         \      
#     /                                           \      
#    /                                             \      
#   /       OOOOO                    OOOOO          \     
#  |        OOOOO                    OOOOO          |     
#   \       OOOOO                    OOOOO         /      
#    \                                            /       
#     \                                          /       
#      \                                        /       
#       +--------------------------------------+       
#  <-----------------pack_diameter------------------>
#              <-------------rm-------->
#
#
# pins=2,3
def makeCrystalRoundVert(footprint_name, rm, pad_size, ddrill, pack_diameter,
                         description="Crystal THT", lib_name="Crystals", tags="", offset3d=[0, 0, 0], scale3d=[1, 1, 1],
                         rotate3d=[0, 0, 0]):
    fpname = footprint_name
    
    if type(pad_size) is list:
        pad = [pad_size[1], pad_size[0]]
    else:
        pad = [pad_size, pad_size]
    
    centerpos = [rm / 2, 0]
    pin1pos = [0, 0]
    pin2pos = [rm, 0]
    
    d_fab = pack_diameter
    cl_fab = rm / 2
    ct_fab = 0
    
    d_slk = d_fab + 2 * slk_offset
    cl_slk = cl_fab
    ct_slk = ct_fab
    sl_slk = 0
    if d_fab >= rm + pad[0]:
        st_slk = 0
        sl_slk = min(-(d_fab - rm) / 2, - pad[0] / 2) - slk_offset
        alpha_slk = 180
    elif d_slk * d_slk / 4 >= rm * rm / 4:
        st_slk = -max(math.sqrt(d_slk * d_slk / 4 - rm * rm / 4), pad[1] / 2 + slk_offset)
        alpha_slk = 2 * (
        90 - math.fabs(180 / 3.1415 * math.atan(math.fabs(st_slk - centerpos[1]) / math.fabs(sl_slk - centerpos[0]))))
    else:
        st_slk = -pad[1] / 2 - slk_offset
        alpha_slk = 2 * (
        90 - math.fabs(180 / 3.1415 * math.atan(math.fabs(st_slk - centerpos[1]) / math.fabs(sl_slk - centerpos[0]))))
    
    d_crt = max(rm + pad[0], d_slk) + 2 * crt_offset
    cl_crt = cl_fab
    ct_crt = ct_fab
    
    print(fpname)
    
    desc = description
    tag_s = tags
    
    # init kicad footprint
    kicad_mod = Footprint(fpname)
    kicad_mod.setDescription(desc)
    kicad_mod.setTags(tags)
    
    offset = [0, 0]
    kicad_modg = kicad_mod
    
    # set general values
    kicad_modg.append(
        Text(type='reference', text='REF**', at=[centerpos[0], ct_slk - d_slk / 2 - txt_offset], layer='F.SilkS'))
    kicad_modg.append(
        Text(type='value', text=fpname, at=[centerpos[0], ct_slk + d_slk / 2 + txt_offset], layer='F.Fab'))
    
    # create FAB-layer
    kicad_mod.append(Circle(center=[cl_fab, ct_fab], radius=d_fab / 2, layer='F.Fab', width=lw_fab))
    
    # create SILKSCREEN-layer
    kicad_mod.append(
        Arc(center=[cl_slk, ct_slk], start=[sl_slk, st_slk], angle=alpha_slk, layer='F.SilkS', width=lw_slk))
    kicad_mod.append(
        Arc(center=[cl_slk, ct_slk], start=[sl_slk, -st_slk], angle=-alpha_slk, layer='F.SilkS', width=lw_slk))
    
    # create courtyard
    kicad_mod.append(Circle(center=[cl_crt, ct_crt], radius=d_crt / 2, layer='F.CrtYd', width=lw_crt))
    
    # create pads
    pad_type = Pad.TYPE_THT
    pad_shape1 = Pad.SHAPE_CIRCLE
    pad_layers = '*'
    
    kicad_modg.append(Pad(number=1, type=pad_type, shape=pad_shape1, at=pin1pos, size=pad, drill=ddrill,
                          layers=[pad_layers + '.Cu', pad_layers + '.Mask']))
    kicad_modg.append(Pad(number=2, type=pad_type, shape=pad_shape1, at=pin2pos, size=pad, drill=ddrill,
                          layers=[pad_layers + '.Cu', pad_layers + '.Mask']))
    
    # add model
    kicad_modg.append(
        Model(filename=lib_name + ".3dshapes/" + fpname + ".wrl", at=offset3d, scale=scale3d, rotate=rotate3d))
    
    # print render tree
    # print(kicad_mod.getRenderTree())
    # print(kicad_mod.getCompleteRenderTree())
    
    # write file
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile(fpname + '.kicad_mod')


