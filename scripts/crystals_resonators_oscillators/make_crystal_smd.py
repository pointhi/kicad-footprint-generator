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
from crystal_tools import *


lw_fab=0.1
lw_slk=0.12
lw_crt=0.05
crt_offset=0.25
slk_offset=0.2
txt_offset = 1


def makeSMDCrystalAndHand(footprint_name,addSizeFootprintName,pins,pad_sep_x,pad_sep_y,pad, pack_width,pack_height,pack_bevel,hasAdhesive=False,adhesivePos=[0,0],adhesiveSize=1, style="rect", description="Crystal SMD SMT", tags=[], lib_name="Crystals",offset3d=[0,0,0],scale3d=[1,1,1],rotate3d=[0,0,0]):
    makeSMDCrystal(footprint_name, addSizeFootprintName, pins, pad_sep_x, pad_sep_y, pad, pack_width,
                   pack_height, pack_bevel, hasAdhesive, adhesivePos, adhesiveSize, style,
                   description, tags, lib_name, offset3d,  scale3d, rotate3d)
    hsfactorx = 1.75
    hsfactory = 1
    if (pins==2 and pack_width>pad_sep_x+pad[0]):
        hsfactorx = 1
        hsfactory = 1.75
    elif (pins==4 and pack_width<pad_sep_x+pad[0] and pack_height<pad_sep_y+pad[1]):
        hsfactorx = 1.5
        hsfactory = 1.5
    elif (pins == 4 and pack_width > pad_sep_x + pad[0] and pack_height < pad_sep_y + pad[1]):
        hsfactorx = 1.1
        hsfactory = 1.5
    elif (pins==4 and pack_width<pad_sep_x+pad[0] and pack_height>pad_sep_y+pad[1]):
        hsfactorx = 1.5
        hsfactory = 1.1

    makeSMDCrystal(footprint_name, addSizeFootprintName, pins, pad_sep_x+pad[0]*(hsfactorx-1), pad_sep_y+pad[1]*(hsfactory-1), [pad[0]*hsfactorx,pad[1]*hsfactory], pack_width,
                   pack_height, pack_bevel, hasAdhesive, adhesivePos, adhesiveSize, style,
                   description+", hand-soldering", tags+" hand-soldering", lib_name, offset3d,  scale3d, rotate3d,name_addition="_HandSoldering")


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
def makeSMDCrystal(footprint_name,addSizeFootprintName,pins,pad_sep_x,pad_sep_y,pad, pack_width,pack_height,pack_bevel,hasAdhesive=False,adhesivePos=[0,0],adhesiveSize=1, style="rect",description="Crystal SMD SMT", tags=[], lib_name="Crystals",offset3d=[0,0,0],scale3d=[1,1,1],rotate3d=[0,0,0], name_addition=""):
        fpname=footprint_name
        if addSizeFootprintName:
            fpname+="_package{0:2.1f}x{1:2.1f}mm".format(pack_width,pack_height)
        fpname=fpname+name_addition
        
        overpad_height=pad_sep_y+pad[1]
        overpad_width = pad_sep_x + pad[0]
        if pins==3:
            overpad_height=pad_sep_y*2+pad[1]
            overpad_width = pad_sep_x*2 + pad[0]

        betweenpads_x_slk=pad_sep_x-pad[0]-2*slk_offset
        betweenpads_y_slk = pad_sep_y - pad[1] - 2 * slk_offset
        overpads_x_slk=pad_sep_x+pad[0]+2*slk_offset
        overpads_y_slk = pad_sep_y +pad[1] + 2 * slk_offset
        if pins==3:
            overpads_x_slk = pad_sep_x*2 + pad[0] + 2 * slk_offset
            overpads_y_slk = pad_sep_y*2 + pad[1] + 2 * slk_offset

        dip_size=1

        mark_size=1
        upright_mark=False
        while pack_height<2*mark_size or pack_width<2*mark_size:
            mark_size=mark_size/2

        if pack_bevel>0 and math.fabs(mark_size/pack_bevel)>0.7 and math.fabs(mark_size/pack_bevel)<1.3:
            upright_mark = True

        h_fab=pack_height
        w_fab=pack_width
        l_fab=-w_fab/2
        t_fab=-h_fab/2
        r_fab = pack_width / 10
        
        h_slk=h_fab+2*slk_offset
        w_slk=w_fab+2*slk_offset
        l_slk=l_fab-slk_offset
        t_slk=t_fab-slk_offset
        dip_size_slk=dip_size
        
        mark_l_slk=-overpads_x_slk / 2
        if math.fabs(l_slk-mark_l_slk)<2*lw_slk:
            mark_l_slk=l_slk-2*lw_slk
        mark_b_slk = overpads_y_slk / 2
        if math.fabs(t_slk+h_slk-mark_b_slk)<2*lw_slk:
            mark_b_slk=t_slk+h_slk+2*lw_slk

        w_crt=max(overpad_width,pack_width)+2*crt_offset
        h_crt = max(overpad_height,pack_height) + 2 * crt_offset
        l_crt = -w_crt/2
        t_crt=-h_crt/2
        
        print(fpname)
        
        desc=description+", {0:2.1f}x{1:2.1f}mm^2 package".format(pack_width,pack_height)
        tag_s=tags+" {0:2.1f}x{1:2.1f}mm^2 package".format(pack_width,pack_height)

        # init kicad footprint
        kicad_mod = Footprint(fpname)
        kicad_mod.setDescription(desc)
        kicad_mod.setTags(tags)

        # anchor for SMD-symbols is in the center, for THT-sybols at pin1
        kicad_mod.setAttribute('smd')
        offset=[0,0]
        kicad_modg=kicad_mod

        # set general values
        kicad_modg.append(Text(type='reference', text='REF**', at=[0, min(t_slk,-overpad_height/2,-pack_height/2)-txt_offset], layer='F.SilkS'))
        #kicad_modg.append(Text(type='user', text='%R', at=[0, min(t_slk,-overpad_height/2,-pack_height/2)-txt_offset], layer='F.Fab'))
        kicad_modg.append(Text(type='value', text=fpname, at=[0, max(t_slk+h_slk,overpad_height/2,pack_height/2)+txt_offset], layer='F.Fab'))

        # create FAB-layer
        if style=='hc49':
            THTQuartz(kicad_modg, [l_fab,t_fab], [w_fab,h_fab], [w_fab*0.9,h_fab*0.9], 'F.Fab', lw_fab)
        elif style=='dip':
            DIPRectL(kicad_modg, [l_fab,t_fab], [w_fab,h_fab], 'F.Fab', lw_fab, dip_size)
        else:
            allBevelRect(kicad_modg, [l_fab, t_fab], [w_fab, h_fab], 'F.Fab', lw_fab, pack_bevel)
            if upright_mark:
                kicad_modg.append(Line(start=[l_fab+max(mark_size,pack_bevel), t_fab], end=[l_fab+max(mark_size,pack_bevel), t_fab + h_fab],layer='F.Fab', width=lw_fab))
            else:
                kicad_modg.append(Line(start=[l_fab, t_fab + h_fab - mark_size], end=[l_fab + mark_size, t_fab + h_fab], layer='F.Fab',width=lw_fab))

        # create SILKSCREEN-layer
        if pins==2:
            if pack_height<pad[1]:
                kicad_modg.append(Line(start=[-betweenpads_x_slk/2, t_slk], end=[betweenpads_x_slk/2, t_slk], layer='F.SilkS', width=lw_slk))
                kicad_modg.append(Line(start=[-betweenpads_x_slk / 2, t_slk+h_slk], end=[betweenpads_x_slk / 2, t_slk+h_slk], layer='F.SilkS',width=lw_slk))
                # pin1 mark
                kicad_modg.append(Line(start=[min(l_slk,-overpads_x_slk / 2), -pad[1]/2], end=[min(l_slk,-overpads_x_slk / 2), pad[1]/2], layer='F.SilkS', width=lw_slk))
            else:
                kicad_modg.append(PolygoneLine(polygone=[[l_slk+w_slk,t_slk],
                                                         [-overpads_x_slk/2, t_slk],
                                                         [-overpads_x_slk / 2, t_slk+h_slk],
                                                         [l_slk + w_slk, t_slk+h_slk],], layer='F.SilkS',width=lw_slk))
        elif pins == 3:
            if (pack_height < overpad_height and pack_width > overpad_width):
                kicad_modg.append(PolygoneLine(polygone=[[overpads_x_slk / 2, t_slk],
                                                         [l_slk + w_slk, t_slk],
                                                         [l_slk + w_slk, t_slk + h_slk],
                                                         [overpads_x_slk / 2, t_slk + h_slk]], layer='F.SilkS',
                                               width=lw_slk))
                kicad_modg.append(Line(start=[l_slk -2*lw_slk, t_slk],
                                       end=[l_slk -2*lw_slk, t_slk+h_slk], layer='F.SilkS', width=lw_slk))

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
        elif pins == 4:
            if (betweenpads_y_slk<5*lw_slk or betweenpads_x_slk<5*lw_slk):
                kicad_modg.append(PolygoneLine(polygone=[[-overpads_x_slk/2,-overpads_y_slk/2],
                                                         [-overpads_x_slk / 2, overpads_y_slk / 2],
                                                         [overpads_x_slk / 2, overpads_y_slk / 2]], layer='F.SilkS', width=lw_slk))
            else:
                if (pack_height<overpad_height and pack_width<overpad_width):
                    kicad_modg.append(PolygoneLine(polygone=[[mark_l_slk, betweenpads_y_slk/2],
                                                             [l_slk, betweenpads_y_slk/2],
                                                             [l_slk, -betweenpads_y_slk/2]], layer='F.SilkS',width=lw_slk))
                    kicad_modg.append(PolygoneLine(polygone=[[l_slk+w_slk, -betweenpads_y_slk / 2],
                                                             [l_slk+w_slk, betweenpads_y_slk / 2]], layer='F.SilkS', width=lw_slk))
                    kicad_modg.append(PolygoneLine(polygone=[[-betweenpads_x_slk/2, t_slk],
                                                             [betweenpads_x_slk/2, t_slk]], layer='F.SilkS',width=lw_slk))
                    kicad_modg.append(PolygoneLine(polygone=[[betweenpads_x_slk / 2, t_slk+h_slk],
                                                             [-betweenpads_x_slk / 2, t_slk+h_slk],
                                                             [-betweenpads_x_slk / 2, mark_b_slk]], layer='F.SilkS', width=lw_slk))
                elif (pack_height < overpad_height and pack_width > overpad_width):
                    kicad_modg.append(PolygoneLine(polygone=[[overpads_x_slk / 2, t_slk],
                                                             [l_slk + w_slk, t_slk],
                                                             [l_slk + w_slk, t_slk + h_slk],
                                                             [overpads_x_slk / 2, t_slk + h_slk]], layer='F.SilkS',
                                                   width=lw_slk))
                    kicad_modg.append(PolygoneLine(polygone=[[-betweenpads_x_slk / 2, t_slk],
                                                             [betweenpads_x_slk / 2, t_slk]], layer='F.SilkS',
                                                   width=lw_slk))
                    if style == 'dip':
                        DIPRectL_LeftOnly(kicad_modg, [l_slk, t_slk], [(w_slk-overpads_x_slk) / 2, h_slk], 'F.SilkS', lw_slk, dip_size_slk)
                        kicad_modg.append(Line(start=[betweenpads_x_slk / 2, t_slk + h_slk], end=[-betweenpads_x_slk / 2, t_slk + h_slk], layer='F.SilkS',
                                                       width=lw_slk))
                    else:
                        kicad_modg.append(PolygoneLine(polygone=[[-overpads_x_slk / 2, mark_b_slk],
                                                                 [-overpads_x_slk / 2, t_slk + h_slk],
                                                                 [l_slk, t_slk + h_slk],
                                                                 [l_slk, t_slk],
                                                                 [-overpads_x_slk / 2, t_slk]], layer='F.SilkS',
                                                       width=lw_slk))
                        kicad_modg.append(PolygoneLine(polygone=[[betweenpads_x_slk / 2, t_slk + h_slk],
                                                                 [-betweenpads_x_slk / 2, t_slk + h_slk],
                                                                 [-betweenpads_x_slk / 2, mark_b_slk]], layer='F.SilkS',
                                                       width=lw_slk))
    
                elif (pack_height>overpad_height and pack_width<overpad_width):
                    kicad_modg.append(PolygoneLine(polygone=[[l_slk, -overpads_y_slk / 2],
                                                             [l_slk, t_slk],
                                                             [l_slk + w_slk, t_slk],
                                                             [l_slk + w_slk, -overpads_y_slk / 2]], layer='F.SilkS',width=lw_slk))
                    kicad_modg.append(PolygoneLine(polygone=[[mark_l_slk, overpads_y_slk / 2],
                                                             [l_slk, overpads_y_slk / 2],
                                                             [l_slk, t_slk + h_slk],
                                                             [l_slk + w_slk, t_slk + h_slk],
                                                             [l_slk + w_slk, overpads_y_slk / 2]], layer='F.SilkS',width=lw_slk))
                    kicad_modg.append(PolygoneLine(polygone=[[mark_l_slk, betweenpads_y_slk/2],
                                                             [l_slk, betweenpads_y_slk/2],
                                                             [l_slk, -betweenpads_y_slk/2]], layer='F.SilkS',width=lw_slk))
                    kicad_modg.append(PolygoneLine(polygone=[[l_slk + w_slk, -betweenpads_y_slk / 2],
                                                             [l_slk + w_slk, betweenpads_y_slk / 2]], layer='F.SilkS',width=lw_slk))

        # create courtyard
        kicad_mod.append(RectLine(start=[roundCrt(l_crt+offset[0]), roundCrt(t_crt+offset[1])], end=[roundCrt(l_crt+offset[0]+w_crt), roundCrt(t_crt+offset[1]+h_crt)], layer='F.CrtYd', width=lw_crt))

        # create pads
        pad_type = Pad.TYPE_SMT
        pad_shape1=Pad.SHAPE_RECT
        pad_layers = 'F'
        ddrill=0
 
        if (pins==2):
            kicad_modg.append(Pad(number=1, type=pad_type, shape=pad_shape1, at=[-pad_sep_x/2, 0], size=pad, drill=ddrill, layers=[pad_layers+'.Cu', pad_layers+'.Mask']))
            kicad_modg.append(Pad(number=2, type=pad_type, shape=pad_shape1, at=[pad_sep_x / 2, 0], size=pad, drill=ddrill,layers=[pad_layers + '.Cu', pad_layers + '.Mask']))
        elif (pins==3):
            kicad_modg.append(Pad(number=1, type=pad_type, shape=pad_shape1, at=[-pad_sep_x, 0], size=pad, drill=ddrill, layers=[pad_layers+'.Cu', pad_layers+'.Mask']))
            kicad_modg.append(Pad(number=2, type=pad_type, shape=pad_shape1, at=[0, 0], size=pad, drill=ddrill,layers=[pad_layers + '.Cu', pad_layers + '.Mask']))
            kicad_modg.append(Pad(number=3, type=pad_type, shape=pad_shape1, at=[pad_sep_x, 0], size=pad, drill=ddrill,layers=[pad_layers + '.Cu', pad_layers + '.Mask']))
        elif (pins==4):
            kicad_modg.append(Pad(number=1, type=pad_type, shape=pad_shape1, at=[-pad_sep_x/2, pad_sep_y/2], size=pad, drill=ddrill, layers=[pad_layers+'.Cu', pad_layers+'.Mask']))
            kicad_modg.append(Pad(number=2, type=pad_type, shape=pad_shape1, at=[pad_sep_x / 2, pad_sep_y/2], size=pad, drill=ddrill,layers=[pad_layers + '.Cu', pad_layers + '.Mask']))
            kicad_modg.append(Pad(number=3, type=pad_type, shape=pad_shape1, at=[pad_sep_x / 2, -pad_sep_y / 2], size=pad, drill=ddrill,layers=[pad_layers + '.Cu', pad_layers + '.Mask']))
            kicad_modg.append(Pad(number=4, type=pad_type, shape=pad_shape1, at=[-pad_sep_x / 2, -pad_sep_y / 2], size=pad, drill=ddrill,layers=[pad_layers + '.Cu', pad_layers + '.Mask']))

        if hasAdhesive:
            fillCircle(kicad_modg, center=adhesivePos, radius=adhesiveSize/2, width=0.1, layer='F.Adhes')

        # add model
        kicad_modg.append(Model(filename=lib_name + ".3dshapes/"+fpname+".wrl",at=offset3d, scale=scale3d, rotate=rotate3d))

        # print render tree
        # print(kicad_mod.getRenderTree())
        # print(kicad_mod.getCompleteRenderTree())

        # write file
        file_handler = KicadFileHandler(kicad_mod)
        file_handler.writeFile(fpname+'.kicad_mod')


if __name__ == '__main__':
    standardtags="SMD SMT crystal"
    standardtagsres="SMD SMT ceramic resonator"
    # common settings
    makeSMDCrystalAndHand(footprint_name="Crystal_SMD_Abracon_ABM3-2pin", addSizeFootprintName=True, pins=2, pad_sep_x=2.2+1.9, pad_sep_y=0, pad=[1.9,2.4], pack_width=5, pack_height=3.2, pack_bevel=0.2,
                   hasAdhesive=True, adhesivePos=[0, 0], adhesiveSize=1,
                   description="Abracon Miniature Ceramic Smd Crystal ABM3 http://www.abracon.com/Resonators/abm3.pdf", tags=standardtags+"",
                   lib_name="Crystals", offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeSMDCrystal(footprint_name="Crystal_SMD_Abracon_ABM3B-4pin", addSizeFootprintName=True, pins=4, pad_sep_x=4, pad_sep_y=2.4, pad=[1.8,1.2], pack_width=5, pack_height=3.2, pack_bevel=0.2,
                   hasAdhesive=True, adhesivePos=[0, 0], adhesiveSize=1,
                   description="Abracon Miniature Ceramic Smd Crystal ABM3B http://www.abracon.com/Resonators/abm3b.pdf", tags=standardtags+"",
                   lib_name="Crystals", offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeSMDCrystalAndHand(footprint_name="Crystal_SMD_SeikoEpson_FA238", addSizeFootprintName=True, pins=4, pad_sep_x=2.2, pad_sep_y=1.6, pad=[1.4, 1.2], pack_width=3.2,
                   pack_height=2.5, pack_bevel=0.1,
                   description="crystal Epson Toyocom FA-238 series http://www.mouser.com/ds/2/137/1721499-465440.pdf",
                   tags=standardtags + "",
                   lib_name="Crystals", offset3d=[0, 0, 0], scale3d=[0.24,0.24,0.24], rotate3d=[0, 0, 0])
    makeSMDCrystalAndHand(footprint_name="Crystal_SMD_SeikoEpson_FA238V", addSizeFootprintName=True, pins=4, pad_sep_x=2.4, pad_sep_y=1.9, pad=[1.4, 1.2], pack_width=3.2,
                   pack_height=2.5, pack_bevel=0.1,
                   description="crystal Epson Toyocom FA-238 series http://www.mouser.com/ds/2/137/1721499-465440.pdf",
                   tags=standardtags + "",
                   lib_name="Crystals", offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeSMDCrystalAndHand(footprint_name="Crystal_SMD_SeikoEpson_TSX3225", addSizeFootprintName=True, pins=4, pad_sep_x=2.2, pad_sep_y=1.6, pad=[1.4, 1.15], pack_width=3.2,
                   pack_height=2.5, pack_bevel=0.1,
                   description="crystal Epson Toyocom TSX-3225 series http://www.mouser.com/ds/2/137/1721499-465440.pdf",
                   tags=standardtags + "",
                   lib_name="Crystals", offset3d=[0, 0, 0], scale3d=[0.24,0.24,0.24], rotate3d=[0, 0, 0])
    makeSMDCrystalAndHand(footprint_name="Crystal_SMD_FOX_FE", addSizeFootprintName=True, pins=2, pad_sep_x=6.3, pad_sep_y=0, pad=[2.2, 2.4], pack_width=7.5,
                   pack_height=5, pack_bevel=0,hasAdhesive=True, adhesivePos=[0, 0], adhesiveSize=0.8,
                   description="crystal Ceramic Resin Sealed SMD http://www.foxonline.com/pdfs/fe.pdf",
                   tags=standardtags + "",
                   lib_name="Crystals", offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeSMDCrystalAndHand(footprint_name="Crystal_SMD_0603-2pin", addSizeFootprintName=True, pins=2, pad_sep_x=4.4, pad_sep_y=0,
                   pad=[1.9,2.5], pack_width=6,
                   pack_height=3.5, pack_bevel=0.1, hasAdhesive=True, adhesivePos=[0, 0], adhesiveSize=0.8,
                   description="SMD Crystal SERIES SMD0603/2 http://www.petermann-technik.de/fileadmin/petermann/pdf/SMD0603-2.pdf",
                   tags=standardtags + "",
                   lib_name="Crystals", offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeSMDCrystalAndHand(footprint_name="Crystal_SMD_0603-4pin", addSizeFootprintName=True, pins=4, pad_sep_x=4.4, pad_sep_y=2.4,
                   pad=[1.8, 1.4], pack_width=6, pack_height=3.5, pack_bevel=0.1, hasAdhesive=True, adhesivePos=[0, 0], adhesiveSize=0.8,
                   description="SMD Crystal SERIES SMD0603/4 http://www.petermann-technik.de/fileadmin/petermann/pdf/SMD0603-4.pdf",
                   tags=standardtags + "",
                   lib_name="Crystals", offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeSMDCrystalAndHand(footprint_name="Crystal_SMD_2012-2pin", addSizeFootprintName=True, pins=2, pad_sep_x=1.4, pad_sep_y=0,
                   pad=[0.6,1.1], pack_width=2, pack_height=1.2, pack_bevel=0, hasAdhesive=True, adhesivePos=[0, 0], adhesiveSize=0.4,
                   description="SMD Crystal 2012/2 http://txccrystal.com/images/pdf/9ht11.pdf",
                   tags=standardtags + "",
                   lib_name="Crystals", offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeSMDCrystalAndHand(footprint_name="Crystal_SMD_TXC_9HT11", addSizeFootprintName=True, pins=2, pad_sep_x=1.4, pad_sep_y=0,
                   pad=[0.6, 1.1], pack_width=2, pack_height=1.2, pack_bevel=0, hasAdhesive=True, adhesivePos=[0, 0],
                   adhesiveSize=0.4,
                   description="SMD Crystal TXC 9HT11 http://txccrystal.com/images/pdf/9ht11.pdf",
                   tags=standardtags + "",
                   lib_name="Crystals", offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeSMDCrystal(footprint_name="Crystal_SMD_2016-4pin", addSizeFootprintName=True, pins=4, pad_sep_x=1.4, pad_sep_y=1.1,
                   pad=[0.9,0.8], pack_width=2, pack_height=1.6, pack_bevel=0.1, hasAdhesive=False, adhesivePos=[0, 0],
                   adhesiveSize=0.8,
                   description="SMD Crystal SERIES SMD2016/4 http://www.q-crystal.com/upload/5/2015552223166229.pdf",
                   tags=standardtags + "",
                   lib_name="Crystals", offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeSMDCrystal(footprint_name="Crystal_SMD_2520-4pin", addSizeFootprintName=True, pins=4, pad_sep_x=1.75, pad_sep_y=1.4,
                   pad=[1.15,1], pack_width=2.5, pack_height=2, pack_bevel=0.1, hasAdhesive=False, adhesivePos=[0, 0],
                   adhesiveSize=0.8,
                   description="SMD Crystal SERIES SMD2520/4 http://www.newxtal.com/UploadFiles/Images/2012-11-12-09-29-09-776.pdf",
                   tags=standardtags + "",
                   lib_name="Crystals", offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeSMDCrystal(footprint_name="Crystal_SMD_2520-4pin", addSizeFootprintName=True, pins=4, pad_sep_x=1.75, pad_sep_y=1.4,
                   pad=[1.15, 1], pack_width=2.5, pack_height=2, pack_bevel=0.1, hasAdhesive=False, adhesivePos=[0, 0],
                   adhesiveSize=0.8,
                   description="SMD Crystal SERIES SMD2520/4 http://www.newxtal.com/UploadFiles/Images/2012-11-12-09-29-09-776.pdf",
                   tags=standardtags + "",
                   lib_name="Crystals", offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeSMDCrystal(footprint_name="Crystal_SMD_5032-4pin", addSizeFootprintName=True, pins=4, pad_sep_x=3.3, pad_sep_y=2.0,
                   pad=[1.6, 1.3], pack_width=5, pack_height=3.2, pack_bevel=0.2, hasAdhesive=False, adhesivePos=[0, 0],
                   adhesiveSize=0.8,
                   description="SMD Crystal SERIES SMD2520/4 http://www.icbase.com/File/PDF/HKC/HKC00061008.pdf",
                   tags=standardtags + "",
                   lib_name="Crystals", offset3d=[0, 0, 0], scale3d=[1/2.54,1/2.54,1/2.54], rotate3d=[0, 0, 0])
    makeSMDCrystalAndHand(footprint_name="Crystal_SMD_5032-2pin", addSizeFootprintName=True, pins=2, pad_sep_x=3.7, pad_sep_y=0,
                   pad=[2, 2.4], pack_width=5, pack_height=3.2, pack_bevel=0.2, hasAdhesive=True, adhesivePos=[0, 0],
                   adhesiveSize=0.8,
                   description="SMD Crystal SERIES SMD2520/2 http://www.icbase.com/File/PDF/HKC/HKC00061008.pdf",
                   tags=standardtags + "",
                   lib_name="Crystals", offset3d=[0, 0, 0], scale3d=[1/2.54,1/2.54,1/2.54], rotate3d=[0, 0, 0])
    makeSMDCrystal(footprint_name="Crystal_SMD_7050-4pin", addSizeFootprintName=True, pins=4, pad_sep_x=5.9, pad_sep_y=2.7,
                   pad=[2.1,1.7], pack_width=7, pack_height=5, pack_bevel=0.2, hasAdhesive=False, adhesivePos=[0, 0],
                   adhesiveSize=0.8,
                   description="SMD Crystal SERIES SMD7050/4 https://www.foxonline.com/pdfs/FQ7050.pdf",
                   tags=standardtags + "",
                   lib_name="Crystals", offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeSMDCrystalAndHand(footprint_name="Crystal_SMD_7050-2pin", addSizeFootprintName=True, pins=2, pad_sep_x=5.2,
                   pad_sep_y=0,
                   pad=[2.8, 3], pack_width=7, pack_height=5, pack_bevel=0.2, hasAdhesive=True, adhesivePos=[0, 0],
                   adhesiveSize=0.8,
                   description="SMD Crystal SERIES SMD7050/4 https://www.foxonline.com/pdfs/FQ7050.pdf",
                   tags=standardtags + "",
                   lib_name="Crystals", offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeSMDCrystal(footprint_name="Crystal_SMD_FOX_FQ7050-4pin", addSizeFootprintName=True, pins=4, pad_sep_x=5.9,
                   pad_sep_y=2.7,
                   pad=[2.1, 1.7], pack_width=7, pack_height=5, pack_bevel=0.2, hasAdhesive=False, adhesivePos=[0, 0],
                   adhesiveSize=0.8,
                   description="FOX SMD Crystal SERIES SMD7050/4 https://www.foxonline.com/pdfs/FQ7050.pdf",
                   tags=standardtags + "",
                   lib_name="Crystals", offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeSMDCrystalAndHand(footprint_name="Crystal_SMD_FOX_FQ7050-2pin", addSizeFootprintName=True, pins=2, pad_sep_x=5.2,
                          pad_sep_y=0,
                          pad=[2.8, 3], pack_width=7, pack_height=5, pack_bevel=0.2, hasAdhesive=True, adhesivePos=[0, 0],
                          adhesiveSize=0.8,
                          description="FOX SMD Crystal SERIES SMD7050/4 https://www.foxonline.com/pdfs/FQ7050.pdf",
                          tags=standardtags + "",
                          lib_name="Crystals", offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeSMDCrystalAndHand(footprint_name="Crystal_SMD_G8-2pin", addSizeFootprintName=True, pins=2, pad_sep_x=2.5,
                      pad_sep_y=0,
                      pad=[1,1.8], pack_width=3.2, pack_height=1.5, pack_bevel=0, hasAdhesive=True, adhesivePos=[0, 0],
                      adhesiveSize=0.5,
                      description="SMD Crystal G8",
                      tags=standardtags + "",
                      lib_name="Crystals", offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeSMDCrystalAndHand(footprint_name="Crystal_SMD_HC49-SD-2pin", addSizeFootprintName=False, pins=2, style="hc49",
                          pad_sep_x=8.5, pad_sep_y=0,
                          pad=[4.5,2], pack_width=11.4, pack_height=4.7, pack_bevel=0, hasAdhesive=False, adhesivePos=[0, 0],
                          adhesiveSize=0.5,
                          description="SMD Crystal HC-49-SD http://cdn-reichelt.de/documents/datenblatt/B400/xxx-HC49-SMD.pdf",
                          tags=standardtags + "",
                          lib_name="Crystals", offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeSMDCrystalAndHand(footprint_name="Crystal_SMD_SeikoEpson_MC156-4pin", addSizeFootprintName=False, pins=4, style="dip",
                          pad_sep_x=5.08, pad_sep_y=2.5,
                          pad=[1.2,1.5], pack_width=7.1, pack_height=2.5, pack_bevel=0, hasAdhesive=False,
                          adhesivePos=[0, 0],
                          adhesiveSize=0.5,
                          description="SMD Crystal Seiko Epson MC-156 https://support.epson.biz/td/api/doc_check.php?dl=brief_MC-156_en.pdf",
                          tags=standardtags + "",
                          lib_name="Crystals", offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeSMDCrystalAndHand(footprint_name="Crystal_SMD_SeikoEpson_MC146-4pin", addSizeFootprintName=False, pins=4,
                          style="rect",
                          pad_sep_x=6.3, pad_sep_y=0.9,
                          pad=[1.2,0.6], pack_width=6.7, pack_height=1.5, pack_bevel=0.4, hasAdhesive=False,
                          adhesivePos=[0, 0],
                          adhesiveSize=0.5,
                          description="SMD Crystal Seiko Epson MC-146 https://support.epson.biz/td/api/doc_check.php?dl=brief_MC-156_en.pdf",
                          tags=standardtags + "",
                          lib_name="Crystals", offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeSMDCrystalAndHand(footprint_name="Crystal_SMD_SeikoEpson_MC306-4pin", addSizeFootprintName=False, pins=4,
                          style="dip",
                          pad_sep_x=5.5, pad_sep_y=3.2,
                          pad=[1.3,1.9], pack_width=8, pack_height=3.2, pack_bevel=0, hasAdhesive=False,
                          adhesivePos=[0, 0],
                          adhesiveSize=0.5,
                          description="SMD Crystal Seiko Epson MC-306 https://support.epson.biz/td/api/doc_check.php?dl=brief_MC-306_en.pdf",
                          tags=standardtags + "",
                          lib_name="Crystals", offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeSMDCrystalAndHand(footprint_name="Crystal_SMD_SeikoEpson_MC405-2pin", addSizeFootprintName=False, pins=2,
                          style="rect",
                          pad_sep_x=8, pad_sep_y=0,
                          pad=[4.1,4.1], pack_width=9.6, pack_height=4.06, pack_bevel=0, hasAdhesive=False,
                          adhesivePos=[0, 0],
                          adhesiveSize=0.5,
                          description="SMD Crystal Seiko Epson MC-405 https://support.epson.biz/td/api/doc_check.php?dl=brief_MC-306_en.pdf",
                          tags=standardtags + "",
                          lib_name="Crystals", offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeSMDCrystalAndHand(footprint_name="Crystal_SMD_SeikoEpson_MC406-4pin", addSizeFootprintName=False, pins=4,
                          style="rect",
                          pad_sep_x=8, pad_sep_y=2.32,
                          pad=[4.1, 1.52], pack_width=9.6, pack_height=4.06, pack_bevel=0, hasAdhesive=False,
                          adhesivePos=[0, 0],
                          adhesiveSize=0.5,
                          description="SMD Crystal Seiko Epson MC-406 https://support.epson.biz/td/api/doc_check.php?dl=brief_MC-306_en.pdf",
                          tags=standardtags + "",
                          lib_name="Crystals", offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeSMDCrystalAndHand(footprint_name="Crystal_SMD_SeikoEpson_MA505-2pin", addSizeFootprintName=False, pins=2,
                          style="rect",
                          pad_sep_x=11.1, pad_sep_y=0,
                          pad=[4.1, 5.6], pack_width=12.7, pack_height=5.08, pack_bevel=0, hasAdhesive=False,
                          adhesivePos=[0, 0],
                          adhesiveSize=0.5,
                          description="SMD Crystal Seiko Epson MC-505 http://media.digikey.com/pdf/Data%20Sheets/Epson%20PDFs/MA-505,506.pdf",
                          tags=standardtags + "",
                          lib_name="Crystals", offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeSMDCrystalAndHand(footprint_name="Crystal_SMD_SeikoEpson_MA506-4pin", addSizeFootprintName=False, pins=4,
                          style="rect",
                          pad_sep_x=11.1, pad_sep_y=3.55,
                          pad=[4.1, 2.05], pack_width=12.7, pack_height=5.08, pack_bevel=0, hasAdhesive=False,
                          adhesivePos=[0, 0],
                          adhesiveSize=0.5,
                          description="SMD Crystal Seiko Epson MC-506 http://media.digikey.com/pdf/Data%20Sheets/Epson%20PDFs/MA-505,506.pdf",
                          tags=standardtags + "",
                          lib_name="Crystals", offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeSMDCrystalAndHand(footprint_name="Crystal_SMD_SeikoEpson_MA406-4pin", addSizeFootprintName=False, pins=4,
                          style="dip",
                          pad_sep_x=9.6, pad_sep_y=3.6,
                          pad=[1.8,1.9], pack_width=11.7, pack_height=4, pack_bevel=0, hasAdhesive=False,
                          adhesivePos=[0, 0],
                          adhesiveSize=0.5,
                          description="SMD Crystal Seiko Epson MC-506 http://media.digikey.com/pdf/Data%20Sheets/Epson%20PDFs/MA-505,506.pdf",
                          tags=standardtags + "",
                          lib_name="Crystals", offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeSMDCrystalAndHand(footprint_name="Crystal_SMD_EuroQuartz_MT-4pin", addSizeFootprintName=True, pins=4,
                          style="rect",
                          pad_sep_x=2.2, pad_sep_y=1.8,
                          pad=[1.3,1], pack_width=3.2, pack_height=2.5, pack_bevel=0.1, hasAdhesive=False,
                          adhesivePos=[0, 0],
                          adhesiveSize=0.5,
                          description="SMD Crystal EuroQuartz MT series http://cdn-reichelt.de/documents/datenblatt/B400/MT.pdf",
                          tags=standardtags + "",
                          lib_name="Crystals", offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeSMDCrystalAndHand(footprint_name="Crystal_SMD_EuroQuartz_X22-4pin", addSizeFootprintName=True, pins=4,
                      style="rect",
                      pad_sep_x=1.6, pad_sep_y=1.2,
                      pad=[1.2,1], pack_width=2.5, pack_height=2, pack_bevel=0.1, hasAdhesive=False,
                      adhesivePos=[0, 0],
                      adhesiveSize=0.5,
                      description="SMD Crystal EuroQuartz X22 series http://cdn-reichelt.de/documents/datenblatt/B400/DS_X22.pdf",
                      tags=standardtags + "",
                      lib_name="Crystals", offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeSMDCrystalAndHand(footprint_name="Crystal_SMD_EuroQuartz_MJ-4pin", addSizeFootprintName=True, pins=4,
                          style="rect",
                          pad_sep_x=3.7, pad_sep_y=2.3,
                          pad=[1.9, 1.1], pack_width=5, pack_height=3.2, pack_bevel=0.1, hasAdhesive=False,
                          adhesivePos=[0, 0],
                          adhesiveSize=0.5,
                          description="SMD Crystal EuroQuartz MJ series http://cdn-reichelt.de/documents/datenblatt/B400/MJ.pdf",
                          tags=standardtags + "",
                          lib_name="Crystals", offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeSMDCrystalAndHand(footprint_name="Crystal_SMD_EuroQuartz_MQ-4pin", addSizeFootprintName=True, pins=4,
                          style="rect",
                          pad_sep_x=6.3, pad_sep_y=2.5,
                          pad=[2.2,1.4], pack_width=7, pack_height=5, pack_bevel=0.1, hasAdhesive=False,
                          adhesivePos=[0, 0],
                          adhesiveSize=0.5,
                          description="SMD Crystal EuroQuartz MQ series http://cdn-reichelt.de/documents/datenblatt/B400/MQ.pdf",
                          tags=standardtags + "",
                          lib_name="Crystals", offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeSMDCrystalAndHand(footprint_name="Crystal_SMD_EuroQuartz_MQ2-2pin", addSizeFootprintName=True, pins=2,
                          style="rect",
                          pad_sep_x=6.3, pad_sep_y=0,
                          pad=[2.2,2.4], pack_width=7, pack_height=5, pack_bevel=0.1, hasAdhesive=False,
                          adhesivePos=[0, 0],
                          adhesiveSize=0.5,
                          description="SMD Crystal EuroQuartz MQ2 series http://cdn-reichelt.de/documents/datenblatt/B400/MQ.pdf",
                          tags=standardtags + "",
                          lib_name="Crystals", offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeSMDCrystalAndHand(footprint_name="Crystal_SMD_EuroQuartz_EQ161-2pin", addSizeFootprintName=True, pins=2,
                          style="rect",
                          pad_sep_x=2.5, pad_sep_y=0,
                          pad=[1,1.8], pack_width=3.2, pack_height=1.5, pack_bevel=0.1, hasAdhesive=False,
                          adhesivePos=[0, 0],
                          adhesiveSize=0.5,
                          description="SMD Crystal EuroQuartz EQ161 series http://cdn-reichelt.de/documents/datenblatt/B400/PG32768C.pdf",
                          tags=standardtags + "",
                          lib_name="Crystals", offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeSMDCrystalAndHand(footprint_name="Crystal_SMD_MicroCrystal_CC4V-T1A-2pin", addSizeFootprintName=True, pins=2,
                          style="rect",
                          pad_sep_x=4.2, pad_sep_y=0,
                          pad=[1.3, 2.2], pack_width=5, pack_height=1.9, pack_bevel=0, hasAdhesive=False,
                          adhesivePos=[0, 0],
                          adhesiveSize=0.5,
                          description="SMD Crystal MicroCrystal CC4V-T1A series http://cdn-reichelt.de/documents/datenblatt/B400/CC4V-T1A.pdf",
                          tags=standardtags + "",
                          lib_name="Crystals", offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeSMDCrystalAndHand(footprint_name="Crystal_SMD_MicroCrystal_CC5V-T1A-2pin", addSizeFootprintName=True, pins=2,
                          style="rect",
                          pad_sep_x=3.4, pad_sep_y=0,
                          pad=[1.1, 1.9], pack_width=4.1, pack_height=1.5, pack_bevel=0, hasAdhesive=False,
                          adhesivePos=[0, 0],
                          adhesiveSize=0.5,
                          description="SMD Crystal MicroCrystal CC5V-T1A series http://cdn-reichelt.de/documents/datenblatt/B400/CC5V-T1A.pdf",
                          tags=standardtags + "",
                          lib_name="Crystals", offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeSMDCrystalAndHand(footprint_name="Resonator_SMD_3pin", addSizeFootprintName=True, pins=3,
                          style="rect",
                          pad_sep_x=2.5, pad_sep_y=0,
                          pad=[1.4, 3.8], pack_width=7.2, pack_height=3, pack_bevel=0, hasAdhesive=False,
                          adhesivePos=[0, 0],
                          adhesiveSize=0.5,
                          description="SMD Resomator/Filter 7.2x3.0mm, Murata CSTCC8M00G53-R0; 8MHz resonator, SMD, Farnell (Element 14) #1170435, http://www.farnell.com/datasheets/19296.pdf?_ga=1.247244932.122297557.1475167906",
                          tags=standardtagsres + " filter",
                          lib_name="Crystals", offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeSMDCrystalAndHand(footprint_name="Resonator_SMD_muRata_SFECV-3pin", addSizeFootprintName=True, pins=3,
                          style="rect",
                          pad_sep_x=2.85, pad_sep_y=0,
                          pad=[1.2, 4], pack_width=6.9, pack_height=2.9, pack_bevel=0, hasAdhesive=False,
                          adhesivePos=[0, 0],
                          adhesiveSize=0.5,
                          description="SMD Resomator/Filter Murata SFECV, http://cdn-reichelt.de/documents/datenblatt/B400/SFECV-107.pdf",
                          tags=standardtagsres + " filter",
                          lib_name="Crystals", offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeSMDCrystalAndHand(footprint_name="Resonator_SMD_muRata_SFSKA-3pin", addSizeFootprintName=True, pins=3,
                          style="rect",
                          pad_sep_x=2.5, pad_sep_y=0,
                          pad=[1, 4.8], pack_width=7.9, pack_height=3.8, pack_bevel=0, hasAdhesive=False,
                          adhesivePos=[0, 0],
                          adhesiveSize=0.5,
                          description="SMD Resomator/Filter Murata SFSKA, http://cdn-reichelt.de/documents/datenblatt/B400/SFECV-107.pdf",
                          tags=standardtagsres + " filter",
                          lib_name="Crystals", offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeSMDCrystalAndHand(footprint_name="Resonator_SMD_muRata_TPSKA-3pin", addSizeFootprintName=True, pins=3,
                          style="rect",
                          pad_sep_x=2.5, pad_sep_y=0,
                          pad=[1, 4.8], pack_width=7.9, pack_height=3.8, pack_bevel=0, hasAdhesive=False,
                          adhesivePos=[0, 0],
                          adhesiveSize=0.5,
                          description="SMD Resomator/Filter Murata TPSKA, http://cdn-reichelt.de/documents/datenblatt/B400/SFECV-107.pdf",
                          tags=standardtagsres + " filter",
                          lib_name="Crystals", offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeSMDCrystalAndHand(footprint_name="Resonator_SMD_muRata_CDSCB-2pin", addSizeFootprintName=True, pins=2,
                              style="rect",
                              pad_sep_x=3, pad_sep_y=0,
                              pad=[1, 2.6], pack_width=4.5, pack_height=2, pack_bevel=0, hasAdhesive=False,
                              adhesivePos=[0, 0],
                              adhesiveSize=0.5,
                              description="SMD Resomator/Filter Murata CDSCB, http://cdn-reichelt.de/documents/datenblatt/B400/SFECV-107.pdf",
                              tags=standardtagsres + " filter",
                              lib_name="Crystals", offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])


