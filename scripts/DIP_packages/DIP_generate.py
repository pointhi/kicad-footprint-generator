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
from DIP_tools import *


lw_fab=0.1
lw_slk=0.12
lw_crt=0.05
crt_offset=0.25
slk_offset=0.12
txt_offset = 1


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
def makeDIP(pins, rm, pinrow_distance_in, package_width, overlen_top, overlen_bottom, ddrill, pad, smd_pads=False, socket_width=0,socket_height=0,socket_pinrow_distance_offset=0, tags_additional=[], lib_name="Housings_DIP",offset3d=[0,0,0],scale3d=[1,1,1],rotate3d=[0,0,0]):
        pinrow_distance=pinrow_distance_in+socket_pinrow_distance_offset
        h_fab=(pins/2-1)*rm+overlen_top+overlen_bottom
        w_fab=package_width
        l_fab=(pinrow_distance-w_fab)/2
        t_fab=-overlen_top
        
        hasSocket=False
        if (socket_height>0 and socket_width>0):
            hasSocket=True
            h_fabs=socket_height
            w_fabs=socket_width
            l_fabs=(w_fabs-pinrow_distance)/2
            t_fabs=(h_fabs-(pins/2-1)*rm)/2
        
        
        h_slk=h_fab+2*slk_offset
        w_slk=min(w_fab+2*slk_offset,pinrow_distance-pad[0]-4*slk_offset)
        l_slk=(pinrow_distance-w_slk)/2
        t_slk=-overlen_top-slk_offset
        w_crt=max(package_width, pinrow_distance+pad[0])+2*crt_offset
        h_crt=max(h_fab, (pins/2-1)*rm+pad[1])+2*crt_offset
        
        hasSocket = False
        if (socket_height > 0 and socket_width > 0):
            hasSocket = True
            h_fabs = socket_height
            w_fabs = socket_width
            l_fabs = (pinrow_distance-w_fabs) / 2
            t_fabs = ((pins / 2 - 1) * rm-h_fabs) / 2
            h_slks = socket_height+2*slk_offset
            w_slks = max(socket_width, pinrow_distance+pad[0])+2*slk_offset
            l_slks = (pinrow_distance-w_slks) / 2
            t_slks = ((pins / 2 - 1) * rm-h_slks) / 2
            w_crt = max(w_crt, w_slks+2*crt_offset)
            h_crt = max(h_crt, h_slks+2*crt_offset)
            
        l_crt = pinrow_distance / 2 - w_crt / 2
        t_crt = (pins / 2 - 1) * rm / 2 - h_crt / 2

        footprint_name="DIP-{0}_W{1}mm".format(pins, round(pinrow_distance,2))
        description="{0}-lead dip package, row spacing {1} mm ({2} mils)".format(pins,round(pinrow_distance,2),int(pinrow_distance/2.54*100))
        tags="DIL DIP PDIP {0}mm {1}mm {2}mil".format(rm,pinrow_distance,int(pinrow_distance/2.54*100))
        if (len(tags_additional)>0):
            for t in tags_additional:
                footprint_name=footprint_name+"_"+t
                description=description+", "+t
                tags=tags+" "+t

        print(footprint_name)

        # init kicad footprint
        kicad_mod = Footprint(footprint_name)
        kicad_mod.setDescription(description)
        kicad_mod.setTags(tags)

        offset=[0,0]
        if (smd_pads):
            offset=[-pinrow_distance/2,-(pins/2-1)*rm/2]
            kicad_modg = Translation(offset[0],offset[1])
            kicad_mod.append(kicad_modg)
            kicad_mod.setAttribute('smd')
        else:
            kicad_modg = kicad_mod

        # set general values
        kicad_modg.append(Text(type='reference', text='REF**', at=[pinrow_distance/2, t_slk-txt_offset], layer='F.SilkS'))
        kicad_modg.append(Text(type='value', text=footprint_name, at=[pinrow_distance/2, t_slk+h_slk+txt_offset], layer='F.Fab'))

        # create FAB-layer
        bevelRect(kicad_modg, [l_fab,t_fab], [w_fab,h_fab], 'F.Fab', lw_fab)
        if hasSocket:
            kicad_modg.append(RectLine(start=[l_fabs,t_fabs], end=[l_fabs+w_fabs,t_fabs+h_fabs], layer='F.Fab', width=lw_fab))

        # create SILKSCREEN-layer
        DIPRect(kicad_modg, [l_slk,t_slk], [w_slk,h_slk], 'F.SilkS', lw_slk)
        if hasSocket:
            #if smd_pads:
            #    kicad_modg.append(Line(start=[l_slks, t_slks], end=[l_slks + w_slks, t_slks], layer='F.SilkS',width=lw_slk))
            #    kicad_modg.append(Line(start=[l_slks, t_slks+h_slks], end=[l_slks + w_slks, t_slks+h_slks], layer='F.SilkS',width=lw_slk))
            #else:
            #    kicad_modg.append(RectLine(start=[l_slks, t_slks], end=[l_slks+w_slks, t_slks+h_slks], layer='F.SilkS', width=lw_slk))
            kicad_modg.append(RectLine(start=[l_slks, t_slks], end=[l_slks + w_slks, t_slks + h_slks], layer='F.SilkS', width=lw_slk))

        # create courtyard
        kicad_mod.append(RectLine(start=[roundCrt(l_crt+offset[0]), roundCrt(t_crt+offset[1])], end=[roundCrt(l_crt+offset[0]+w_crt), roundCrt(t_crt+offset[1]+h_crt)], layer='F.CrtYd', width=lw_crt))

        # create pads
        p1=int(1)
        x1=0
        y1=0
        p2=int(pins/2+1)
        x2=pinrow_distance
        y2=(pins/2-1)*rm
        
        if smd_pads:
            pad_type = Pad.TYPE_SMT
            pad_shape1=Pad.SHAPE_RECT
            pad_shapeother=Pad.SHAPE_RECT
            pad_layers = 'F'
        else:
            pad_type = Pad.TYPE_THT
            pad_shape1 = Pad.SHAPE_RECT
            pad_shapeother = Pad.SHAPE_OVAL
            pad_layers = '*'

        for p in range(1,int(pins/2+1)):
            if p==1:
                kicad_modg.append(Pad(number=p1, type=pad_type, shape=pad_shape1, at=[x1, y1], size=pad, drill=ddrill, layers=[pad_layers+'.Cu', pad_layers+'.Mask']))
            else:
                kicad_modg.append(Pad(number=p1, type=pad_type, shape=pad_shapeother, at=[x1, y1], size=pad, drill=ddrill, layers=[pad_layers+'.Cu', pad_layers+'.Mask']))
            
            kicad_modg.append(Pad(number=p2, type=pad_type, shape=pad_shapeother, at=[x2,y2], size=pad, drill=ddrill, layers=[pad_layers+'.Cu', pad_layers+'.Mask']))
            
            p1=p1+1
            p2=p2+1
            y1=y1+rm
            y2=y2-rm

        # add model
        kicad_modg.append(Model(filename=lib_name + ".3dshapes/"+footprint_name+".wrl",at=offset3d, scale=scale3d, rotate=rotate3d))

        # print render tree
        # print(kicad_mod.getRenderTree())
        # print(kicad_mod.getCompleteRenderTree())

        # write file
        file_handler = KicadFileHandler(kicad_mod)
        file_handler.writeFile(footprint_name+'.kicad_mod')


if __name__ == '__main__':
    # common settings
    overlen_top=1.27
    overlen_bottom=1.27
    rm=2.54
    ddrill=0.8
    pad=[1.6,1.6]
    pad_large=[2.4,1.6]
    pad_smdsocket=[3.1,1.6]
    pad_smdsocket_small=[1.6,1.6]

    # narrow 7.62 DIPs
    pins=[4,6,8,10,12,14,16,18,20,22,24,28]
    pinrow_distance=7.62
    package_width=6.35
    socket_width=pinrow_distance+2.54
    for p in pins:
        makeDIP(p,rm,pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad,False,0,0,0)
        makeDIP(p, rm, pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad_large, False, 0,0,0, ["LongPads"])
        socket_height = (p / 2 - 1) * rm + 2.54
        makeDIP(p, rm, pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad, False, socket_width,socket_height,0, ["Socket"])
        makeDIP(p, rm, pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad_large, False, socket_width,socket_height,0,  ["Socket","LongPads"])
        makeDIP(p, rm, pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad_smdsocket, True, socket_width,socket_height,1.27, ["SMDSocket","LongPads"])
        makeDIP(p, rm, pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad_smdsocket_small, True,socket_width, socket_height, 0, ["SMDSocket", "SmallPads"])

    # mid 10.16 DIPs
    pins=[22,24]
    pinrow_distance=10.16
    package_width=9.14
    socket_width=pinrow_distance+2.54
    for p in pins:
        makeDIP(p,rm,pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad,False,0,0,0)
        makeDIP(p, rm, pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad_large, False, 0,0,0, ["LongPads"])
        socket_height = (p / 2 - 1) * rm + 2.54
        makeDIP(p, rm, pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad, False, socket_width,socket_height,0, ["Socket"])
        makeDIP(p, rm, pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad_large, False, socket_width,socket_height,0,  ["Socket","LongPads"])
        makeDIP(p, rm, pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad_smdsocket, True,
            socket_width, socket_height, 1.27, ["SMDSocket", "LongPads"])
        makeDIP(p, rm, pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad_smdsocket_small, True,
            socket_width, socket_height, 0, ["SMDSocket", "SmallPads"])

    # mid 15.24 DIPs
    pins=[24,28,32,40,42,48,64]
    pinrow_distance=15.24
    package_width=14.73
    socket_width=pinrow_distance+2.54
    for p in pins:
        makeDIP(p,rm,pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad,False,0,0,0)
        makeDIP(p, rm, pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad_large, False, 0,0,0, ["LongPads"])
        socket_height = (p / 2 - 1) * rm + 2.54
        makeDIP(p, rm, pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad, False, socket_width,socket_height,0, ["Socket"])
        makeDIP(p, rm, pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad_large, False, socket_width,socket_height,0,  ["Socket","LongPads"])
        makeDIP(p, rm, pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad_smdsocket, True,
            socket_width, socket_height, 1.27, ["SMDSocket", "LongPads"])
        makeDIP(p, rm, pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad_smdsocket_small, True,
            socket_width, socket_height, 0, ["SMDSocket", "SmallPads"])

    # large 22.86 DIPs
    pins=[64]
    pinrow_distance=22.86
    package_width=22.35
    socket_width=pinrow_distance+2.54
    for p in pins:
        makeDIP(p,rm,pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad,False,0,0,0)
        makeDIP(p, rm, pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad_large, False, 0,0,0, ["LongPads"])
        socket_height = (p / 2 - 1) * rm + 2.54
        makeDIP(p, rm, pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad, False, socket_width,socket_height,0, ["Socket"])
        makeDIP(p, rm, pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad_large, False, socket_width,socket_height,0,  ["Socket","LongPads"])
        makeDIP(p, rm, pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad_smdsocket, True,
            socket_width, socket_height, 1.27, ["SMDSocket", "LongPads"])
        makeDIP(p, rm, pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad_smdsocket_small, True,
            socket_width, socket_height, 0, ["SMDSocket", "SmallPads"])

    # large 25.4 DIPs
    pins=[40,64]
    pinrow_distance=25.4
    package_width=24.89
    socket_width=pinrow_distance+2.54
    for p in pins:
        makeDIP(p,rm,pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad,False,0,0,0)
        makeDIP(p, rm, pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad_large, False, 0,0,0, ["LongPads"])
        socket_height = (p / 2 - 1) * rm + 2.54
        makeDIP(p, rm, pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad, False, socket_width,socket_height,0, ["Socket"])
        makeDIP(p, rm, pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad_large, False, socket_width,socket_height,0,  ["Socket","LongPads"])
        makeDIP(p, rm, pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad_smdsocket, True,
            socket_width, socket_height, 1.27, ["SMDSocket", "LongPads"])
        makeDIP(p, rm, pinrow_distance, package_width, overlen_top, overlen_bottom, ddrill, pad_smdsocket_small, True,
            socket_width, socket_height, 0, ["SMDSocket", "SmallPads"])

    # special SMD footprints
    smd_pins=[4,6,8,10,14,16]
    pad_smd = [2, 1.78]
    smd_pinrow_distances=[7.62, 9.53, 11.48]
    package_width=6.35
    for p in smd_pins:
        for prd in smd_pinrow_distances:
            makeDIP(p, rm, prd, package_width, overlen_top, overlen_bottom, ddrill, pad_smd, True,  0,0,0, ["SMD"])

