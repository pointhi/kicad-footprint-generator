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
def makeCrystal(footprint_name,rm,pad_size, ddrill,pack_width,pack_height,pack_offset,pack_rm, style="flat",package_pad=False,package_pad_add_holes=False,package_pad_offset=0, package_pad_size=[0,0],package_pad_drill_size=[1.2,1.2], package_pad_ddrill=0.8,description="Crystal THT", lib_name="Crystals",tags="",offset3d=[0,0,0],scale3d=[1,1,1],rotate3d=[0,0,0], name_addition=""):
        
        fpname=footprint_name
        fpname=fpname+name_addition
        
        pad=[pad_size,pad_size]
        
        pad3pos=[rm/2, package_pad_offset+package_pad_size[0]/2]
        pad3dril_xoffset=package_pad_size[1]/2+package_pad_ddrill/2

        h_fab=pack_width
        w_fab=pack_height
        l_fab=-(w_fab-rm)/2
        t_fab=pack_offset
        
        h_slk=h_fab+2*slk_offset
        w_slk=w_fab+2*slk_offset
        l_slk=l_fab-slk_offset
        t_slk=t_fab-slk_offset
        

        if package_pad:
            l_slk=min(l_slk,rm/2-package_pad_size[1]/2-slk_offset)
            w_slk = max(w_slk, package_pad_size[1]+2* slk_offset)
            h_slk = max(t_slk+h_slk,pad3pos[1]+package_pad_size[0]/2+ slk_offset)-t_slk
            if package_pad_add_holes:
                l_crt=pad3pos[0]-pad3dril_xoffset-package_pad_drill_size[0]/2-crt_offset

        t_crt = -pad[0] / 2 - crt_offset
        w_crt = max(pack_height,pad[0]+rm,w_slk) + 2 * crt_offset
        h_crt = max(t_slk+h_slk-t_crt,pack_width+pack_offset+pad[0]/2) + 2 * crt_offset
        l_crt = rm/2-w_crt/2

        if package_pad and package_pad_add_holes:
                l_crt=pad3pos[0]-pad3dril_xoffset-package_pad_drill_size[0]/2-crt_offset
                w_crt=pad3pos[0]+pad3dril_xoffset+package_pad_drill_size[0]/2+crt_offset-l_crt

        print(fpname)
        
        desc=description
        tag_s=tags

        # init kicad footprint
        kicad_mod = Footprint(fpname)
        kicad_mod.setDescription(desc)
        kicad_mod.setTags(tags)

        kicad_modg=kicad_mod

        # set general values
        kicad_modg.append(Text(type='reference', text='REF**', at=[l_slk-txt_offset, t_crt+h_crt/4], layer='F.SilkS', rotation=90))
        kicad_modg.append(Text(type='value', text=fpname, at=[l_slk+w_slk+txt_offset,t_crt+h_crt/4], layer='F.Fab', rotation=90))

        # create FAB-layer
        kicad_modg.append(RectLine(start=[l_fab, t_fab],
                               end=[l_fab + w_fab, t_fab + h_fab], layer='F.Fab', width=lw_fab))
        kicad_modg.append(Line(start=[l_fab+w_fab/2-pack_rm/2, t_fab],end=[0,0], layer='F.Fab', width=lw_fab))
        kicad_modg.append(Line(start=[l_fab+w_fab/2+pack_rm/2, t_fab],end=[rm,0], layer='F.Fab', width=lw_fab))
        if package_pad and package_pad_add_holes:
            kicad_modg.append(
                Line(start=[pad3pos[0]-pad3dril_xoffset,pad3pos[1]], end=[pad3pos[0]+pad3dril_xoffset,pad3pos[1]], layer='F.Fab', width=lw_fab))

        # create SILKSCREEN-layer
        if package_pad and package_pad_add_holes:
            kicad_modg.append(PolygoneLine(polygone=[[l_slk, pad3pos[1]-package_pad_drill_size[1]/2-slk_offset],
                                                     [l_slk , t_slk],
                                                     [l_slk + w_slk, t_slk],
                                                     [l_slk + w_slk, pad3pos[1]-package_pad_drill_size[1]/2-slk_offset]], layer='F.SilkS', width=lw_slk))
        else:
            kicad_modg.append(RectLine(start=[l_slk, t_slk],end=[l_slk + w_slk, t_slk + h_slk], layer='F.SilkS', width=lw_slk))
        kicad_modg.append(Line(start=[l_slk+w_slk/2-pack_rm/2, t_slk],end=[0,pad[1]/2+slk_offset], layer='F.SilkS', width=lw_slk))
        kicad_modg.append(Line(start=[l_slk+w_slk/2+pack_rm/2, t_slk],end=[rm,pad[1]/2+slk_offset], layer='F.SilkS', width=lw_slk))


        # create courtyard
        kicad_mod.append(RectLine(start=[roundCrt(l_crt), roundCrt(t_crt)], end=[roundCrt(l_crt+w_crt), roundCrt(t_crt+h_crt)], layer='F.CrtYd', width=lw_crt))

        # create pads
        pad_type = Pad.TYPE_THT
        pad_shape1=Pad.SHAPE_CIRCLE
        pad_layers = '*'
 
        kicad_modg.append(Pad(number=1, type=pad_type, shape=pad_shape1, at=[0, 0], size=pad, drill=ddrill, layers=[pad_layers+'.Cu', pad_layers+'.Mask']))
        kicad_modg.append(Pad(number=2, type=pad_type, shape=pad_shape1, at=[rm,0], size=pad, drill=ddrill,layers=[pad_layers + '.Cu', pad_layers + '.Mask']))

        if package_pad:
            kicad_modg.append(Pad(number=3, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, at=pad3pos, size=[package_pad_size[1],package_pad_size[0]], drill=0, layers=['F.Cu', 'F.Mask']))
            if package_pad_add_holes:
                kicad_modg.append(Pad(number=3, type=Pad.TYPE_THT, shape=Pad.SHAPE_RECT, at=[pad3pos[0]-pad3dril_xoffset,pad3pos[1]], size=package_pad_drill_size, drill=package_pad_ddrill,layers=[pad_layers + '.Cu', pad_layers + '.Mask']))
                kicad_modg.append(Pad(number=3, type=Pad.TYPE_THT, shape=Pad.SHAPE_RECT, at=[pad3pos[0]+pad3dril_xoffset,pad3pos[1]], size=package_pad_drill_size,drill=package_pad_ddrill, layers=[pad_layers + '.Cu', pad_layers + '.Mask']))
            
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
    makeCrystal(footprint_name="Crystal_Watch_C26-LF_l6.5mm_d2.1mm",
                rm=1.9, pad_size=1, ddrill=0.5, pack_width=6.5, pack_height=2.06, pack_rm=0.7, pack_offset=2,
                package_pad=False, package_pad_offset=2.5, package_pad_size=[0,0],
                style="flat", description="Crystal THT C26-LF 6.5mm length 2.06mm diameter", tags=["C26-LF"], lib_name="Crystals",
                offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeCrystal(footprint_name="Crystal_Watch_C26-LF_l6.5mm_d2.1mm_1EP_sytle1",
                rm=1.9, pad_size=1, ddrill=0.5, pack_width=6.5, pack_height=2.06, pack_rm=0.7, pack_offset=2,
                package_pad=True, package_pad_offset=2.5, package_pad_size=[6.5,2.2],
                style="flat", description="Crystal THT C26-LF 6.5mm length 2.06mm diameter", tags=["C26-LF"], lib_name="Crystals",
                offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeCrystal(footprint_name="Crystal_Watch_C26-LF_l6.5mm_d2.1mm_1EP_sytle2",
                rm=1.9, pad_size=1, ddrill=0.5, pack_width=6.5, pack_height=2.06, pack_rm=0.7, pack_offset=2,
                package_pad=True, package_pad_offset=2.5, package_pad_size=[6.5,2.2],
                package_pad_add_holes=True, package_pad_drill_size=[1.2, 1.2], package_pad_ddrill=0.8,
                style="flat", description="Crystal THT C26-LF 6.5mm length 2.06mm diameter", tags=["C26-LF"], lib_name="Crystals",
                offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeCrystal(footprint_name="Crystal_Watch_C38-LF_l8.0mm_d3.0mm",
                rm=1.9, pad_size=1, ddrill=0.5, pack_width=8, pack_height=3, pack_rm=1.09, pack_offset=2.5,
                package_pad=False, package_pad_offset=2.5, package_pad_size=[0, 0],
                style="flat", description="Crystal THT C38-LF 8.0mm length 3.0mm diameter", tags=["C38-LF"],
                lib_name="Crystals",
                offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeCrystal(footprint_name="Crystal_Watch_C38-LF_l8.0mm_d3.0mm_1EP_style1",
                rm=1.9, pad_size=1, ddrill=0.5, pack_width=8, pack_height=3, pack_rm=1.09, pack_offset=2.5,
                package_pad=True, package_pad_offset=3, package_pad_size=[8,3],
                package_pad_add_holes=False, package_pad_drill_size=[1.2, 1.2], package_pad_ddrill=0.8,
                style="flat", description="Crystal THT C38-LF 8.0mm length 3.0mm diameter", tags=["C38-LF"],
                lib_name="Crystals",
                offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeCrystal(footprint_name="Crystal_Watch_C38-LF_l8.0mm_d3.0mm_1EP_style2",
                rm=1.9, pad_size=1, ddrill=0.5, pack_width=8, pack_height=3, pack_rm=1.09, pack_offset=2.5,
                package_pad=True, package_pad_offset=3, package_pad_size=[8,3],
                package_pad_add_holes=True, package_pad_drill_size=[1.2, 1.2], package_pad_ddrill=0.8,
                style="flat", description="Crystal THT C38-LF 8.0mm length 3.0mm diameter", tags=["C38-LF"],
                lib_name="Crystals",
                offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeCrystal(footprint_name="Crystal_Watch_DS26_l6.0mm_d2.0mm",
                rm=1.9, pad_size=1, ddrill=0.5, pack_width=6, pack_height=2, pack_rm=0.7, pack_offset=2,
                package_pad=False, package_pad_offset=2.5, package_pad_size=[0, 0],
                style="flat", description="Crystal THT DS26 6.0mm length 2.0mm diameter http://www.microcrystal.com/images/_Product-Documentation/03_TF_metal_Packages/01_Datasheet/DS-Series.pdf",
                tags=["DS26"],lib_name="Crystals",
                offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeCrystal(footprint_name="Crystal_Watch_DS26_l6.0mm_d2.0mm_1EP_style1",
                rm=1.9, pad_size=1, ddrill=0.5, pack_width=6, pack_height=2, pack_rm=0.7, pack_offset=2,
                package_pad=True, package_pad_offset=2.5, package_pad_size=[6,2.5],
                package_pad_add_holes=False, package_pad_drill_size=[1.2, 1.2], package_pad_ddrill=0.8,
                style="flat", description="Crystal THT DS26 6.0mm length 2.0mm diameter http://www.microcrystal.com/images/_Product-Documentation/03_TF_metal_Packages/01_Datasheet/DS-Series.pdf",
                tags=["DS26"],lib_name="Crystals",
                offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeCrystal(footprint_name="Crystal_Watch_DS26_l6.0mm_d2.0mm_1EP_style2",
                rm=1.9, pad_size=1, ddrill=0.5, pack_width=6, pack_height=2, pack_rm=0.7, pack_offset=2,
                package_pad=True, package_pad_offset=2.5, package_pad_size=[6,2.5],
                package_pad_add_holes=True, package_pad_drill_size=[1.2, 1.2], package_pad_ddrill=0.8,
                style="flat", description="Crystal THT DS26 6.0mm length 2.0mm diameter http://www.microcrystal.com/images/_Product-Documentation/03_TF_metal_Packages/01_Datasheet/DS-Series.pdf",
                tags=["DS26"],lib_name="Crystals",
                offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeCrystal(footprint_name="Crystal_Watch_DS15_l5.0mm_d1.5mm",
                rm=1.7, pad_size=1, ddrill=0.5, pack_width=5, pack_height=1.5, pack_rm=0.5, pack_offset=1.5,
                package_pad=False, package_pad_offset=2.5, package_pad_size=[0, 0],
                style="flat",
                description="Crystal THT DS15 5.0mm length 1.5mm diameter http://www.microcrystal.com/images/_Product-Documentation/03_TF_metal_Packages/01_Datasheet/DS-Series.pdf",
                tags=["DS15"], lib_name="Crystals",
                offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeCrystal(footprint_name="Crystal_Watch_DS15_l5.0mm_d1.5mm_1EP_style1",
                rm=1.7, pad_size=1, ddrill=0.5, pack_width=5, pack_height=1.5, pack_rm=0.5, pack_offset=1.5,
                package_pad=True, package_pad_offset=2, package_pad_size=[5,2],
                package_pad_add_holes=False, package_pad_drill_size=[1.2, 1.2], package_pad_ddrill=0.8,
                style="flat",
                description="Crystal THT DS15 5.0mm length 1.5mm diameter http://www.microcrystal.com/images/_Product-Documentation/03_TF_metal_Packages/01_Datasheet/DS-Series.pdf",
                tags=["DS15"], lib_name="Crystals",
                offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeCrystal(footprint_name="Crystal_Watch_DS15_l5.0mm_d1.5mm_1EP_style2",
                rm=1.7, pad_size=1, ddrill=0.5, pack_width=5, pack_height=1.5, pack_rm=0.5, pack_offset=1.5,
                package_pad=True, package_pad_offset=2, package_pad_size=[5,2],
                package_pad_add_holes=True, package_pad_drill_size=[1.2, 1.2], package_pad_ddrill=0.8,
                style="flat",
                description="Crystal THT DS15 5.0mm length 1.5mm diameter http://www.microcrystal.com/images/_Product-Documentation/03_TF_metal_Packages/01_Datasheet/DS-Series.pdf",
                tags=["DS15"], lib_name="Crystals",
                offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeCrystal(footprint_name="Crystal_Watch_DS10_l4.3mm_d1.0mm",
                rm=1.5, pad_size=1, ddrill=0.5, pack_width=4.3, pack_height=1, pack_rm=0.3, pack_offset=1.5,
                package_pad=False, package_pad_offset=2.5, package_pad_size=[0, 0],
                style="flat",
                description="Crystal THT DS10 4.3mm length 1.0mm diameter http://www.microcrystal.com/images/_Product-Documentation/03_TF_metal_Packages/01_Datasheet/DS-Series.pdf",
                tags=["DS10"], lib_name="Crystals",
                offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeCrystal(footprint_name="Crystal_Watch_DS10_l4.3mm_d1.0mm_1EP_style1",
                rm=1.5, pad_size=1, ddrill=0.5, pack_width=4.3, pack_height=1, pack_rm=0.3, pack_offset=1.5,
                package_pad=True, package_pad_offset=2, package_pad_size=[4.3,1.5],
                package_pad_add_holes=False, package_pad_drill_size=[1.2, 1.2], package_pad_ddrill=0.8,
                style="flat",
                description="Crystal THT DS10 4.3mm length 1.0mm diameter http://www.microcrystal.com/images/_Product-Documentation/03_TF_metal_Packages/01_Datasheet/DS-Series.pdf",
                tags=["DS10"], lib_name="Crystals",
                offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeCrystal(footprint_name="Crystal_Watch_DS10_l4.3mm_d1.0mm_1EP_style2",
                rm=1.5, pad_size=1, ddrill=0.5, pack_width=4.3, pack_height=1, pack_rm=0.3, pack_offset=1.5,
                package_pad=True, package_pad_offset=2, package_pad_size=[4.3, 1.5],
                package_pad_add_holes=True, package_pad_drill_size=[1.2, 1.2], package_pad_ddrill=0.8,
                style="flat",
                description="Crystal THT DS10 4.3mm length 1.0mm diameter http://www.microcrystal.com/images/_Product-Documentation/03_TF_metal_Packages/01_Datasheet/DS-Series.pdf",
                tags=["DS10"], lib_name="Crystals",
                offset3d=[0, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeCrystal(footprint_name="Crystal_HC49-U_Horicontal",
                rm=4.9, pad_size=1.2, ddrill=0.8, pack_width=13.0, pack_height=10.9, pack_rm=4.9, pack_offset=2,
                package_pad=False, package_pad_offset=2.5, package_pad_size=[13.5, 11],
                package_pad_add_holes=False, package_pad_drill_size=[1.2, 1.2], package_pad_ddrill=0.8,
                style="flat",
                description="Crystal THT HC-49/U http://5hertz.com/pdfs/04404_D.pdf",
                lib_name="Crystals",
                offset3d=[2.4/25.4, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeCrystal(footprint_name="Crystal_HC49-U_Horicontal_1EP_style1",
                rm=4.9, pad_size=1.2, ddrill=0.8, pack_width=13.0, pack_height=10.9, pack_rm=4.9, pack_offset=2,
                package_pad=True, package_pad_offset=2.5, package_pad_size=[13.5, 11],
                package_pad_add_holes=False, package_pad_drill_size=[1.2, 1.2], package_pad_ddrill=0.8,
                style="flat",
                description="Crystal THT HC-49/U http://5hertz.com/pdfs/04404_D.pdf",
                lib_name="Crystals",
                offset3d=[2.4/25.4, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeCrystal(footprint_name="Crystal_HC49-U_Horicontal_1EP_style2",
                rm=4.9, pad_size=1.2, ddrill=0.8, pack_width=13.0, pack_height=10.9, pack_rm=4.9, pack_offset=2,
                package_pad=True, package_pad_offset=2.5, package_pad_size=[13.5, 11],
                package_pad_add_holes=True, package_pad_drill_size=[1.2, 1.2], package_pad_ddrill=0.8,
                style="flat",
                description="Crystal THT HC-49/U http://5hertz.com/pdfs/04404_D.pdf",
                lib_name="Crystals",
                offset3d=[2.4/25.4, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeCrystal(footprint_name="Crystal_HC18-U_Horicontal",
                rm=4.9, pad_size=1.2, ddrill=0.8, pack_width=13.0, pack_height=10.9, pack_rm=4.9, pack_offset=2,
                package_pad=False, package_pad_offset=2.5, package_pad_size=[13.5, 11],
                package_pad_add_holes=False, package_pad_drill_size=[1.2, 1.2], package_pad_ddrill=0.8,
                style="flat",
                description="Crystal THT HC-18/U http://5hertz.com/pdfs/04404_D.pdf",
                lib_name="Crystals",
                offset3d=[2.4/25.4, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeCrystal(footprint_name="Crystal_HC18-U_Horicontal_1EP_style1",
                rm=4.9, pad_size=1.2, ddrill=0.8, pack_width=13.0, pack_height=10.9, pack_rm=4.9, pack_offset=2,
                package_pad=True, package_pad_offset=2.5, package_pad_size=[13.5, 11],
                package_pad_add_holes=False, package_pad_drill_size=[1.2, 1.2], package_pad_ddrill=0.8,
                style="flat",
                description="Crystal THT HC-18/U http://5hertz.com/pdfs/04404_D.pdf",
                lib_name="Crystals",
                offset3d=[2.4/25.4, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeCrystal(footprint_name="Crystal_HC18-U_Horicontal_1EP_style2",
                rm=4.9, pad_size=1.2, ddrill=0.8, pack_width=13.0, pack_height=10.9, pack_rm=4.9, pack_offset=2,
                package_pad=True, package_pad_offset=2.5, package_pad_size=[13.5, 11],
                package_pad_add_holes=True, package_pad_drill_size=[1.2, 1.2], package_pad_ddrill=0.8,
                style="flat",
                description="Crystal THT HC-18/U http://5hertz.com/pdfs/04404_D.pdf",
                lib_name="Crystals",
                offset3d=[2.4/25.4, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeCrystal(footprint_name="Crystal_HC33-U_Horicontal",
                rm=12.34, pad_size=2.3, ddrill=1.7, pack_width=19.7, pack_height=19.23, pack_rm=12.34, pack_offset=2.5,
                package_pad=False, package_pad_offset=2.5, package_pad_size=[19.5, 13],
                package_pad_add_holes=False, package_pad_drill_size=[1.2, 1.2], package_pad_ddrill=0.8,
                style="flat",
                description="Crystal THT HC-33/U http://pdi.bentech-taiwan.com/PDI/GEN20SPEV20HC3320U.pdf",
                lib_name="Crystals",
                offset3d=[6.35 / 25.4, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeCrystal(footprint_name="Crystal_HC33-U_Horicontal_1EP_style1",
                rm=12.34, pad_size=2.3, ddrill=1.7, pack_width=19.7, pack_height=19.23, pack_rm=12.34, pack_offset=2.5,
                package_pad=True, package_pad_offset=2.5, package_pad_size=[19.5, 13],
                package_pad_add_holes=True, package_pad_drill_size=[1.2, 1.2], package_pad_ddrill=0.8,
                style="flat",
                description="Crystal THT HC-33/U http://pdi.bentech-taiwan.com/PDI/GEN20SPEV20HC3320U.pdf",
                lib_name="Crystals",
                offset3d=[6.35 / 25.4, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
    makeCrystal(footprint_name="Crystal_HC33-U_Horicontal_1EP_style2",
                rm=12.34, pad_size=2.3, ddrill=1.7, pack_width=19.7, pack_height=19.23, pack_rm=12.34, pack_offset=2.5,
                package_pad=True, package_pad_offset=2.5, package_pad_size=[19.5, 13],
                package_pad_add_holes=True, package_pad_drill_size=[1.2, 1.2], package_pad_ddrill=0.8,
                style="flat",
                description="Crystal THT HC-33/U http://pdi.bentech-taiwan.com/PDI/GEN20SPEV20HC3320U.pdf",
                lib_name="Crystals",
                offset3d=[6.35 / 25.4, 0, 0], scale3d=[1, 1, 1], rotate3d=[0, 0, 0])
