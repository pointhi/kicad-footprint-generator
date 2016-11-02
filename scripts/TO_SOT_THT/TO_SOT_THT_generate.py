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

def roundG(x, g):
    if (x>0):
        return math.ceil(x/g)*g
    else:
        return math.floor(x/g)*g

def roundCrt(x):
    return roundG(x, 0.05)


#split a vertical line so it does not interfere with keepout areas defined as [[x0,x1,y0,y1], ...]
def addHLineWithKeepout(kicad_mod, x0, x1, y,layer, width, keepouts=[], roun=0.001):
    lines = [[x0, x1]]
    changes=True
    while (changes):
        changes=False
        for ko in keepouts:
            if (ko[2]<=y) & (y<=ko[3]):
                for li in reversed(range(0,len(lines))):
                    l=lines[li]
                    #print("H: ko=",ko,"  li=",li,"   l=",l,"   ls=",lines)
                    if (ko[0]<l[0]) & (l[1]<ko[1]) & (l[1]>ko[0]): # Line completely inside -> remove
                        lines.pop(li)
                        changes=True
                        break
                    elif (l[0]>ko[0]) & (l[1]<ko[1]) & (l[1] > ko[1]):  # Line starts inside, but ends outside -> remove and add shortened
                        lines.pop(li)
                        lines.append([ko[1], l[1]])
                        changes = True
                        break
                    elif (l[0]<ko[0] ) & (l[1] < ko[1])& (l[1] > ko[0]):  # Line starts outside, but ends inside -> remove and add shortened
                        lines.pop(li)
                        lines.append([l[0], ko[0]])
                        changes = True
                        break
                    elif (l[0]<ko[0]) & (l[1] > ko[1]):  # Line starts outside, and ends outside -> remove and add 2 shortened
                        lines.pop(li)
                        lines.append([l[0], ko[0]])
                        lines.append([ko[1], l[1]])
                        changes = True
                        break
                    if changes:
                        break
    for l in lines:
        kicad_mod.append(Line(start=[roundG(l[0], roun), roundG(y, roun)], end=[roundG(l[1], roun), roundG(y, roun)], layer=layer, width=width))



#split a vertical line so it does not interfere with keepout areas defined as [[x0,x1,y0,y1], ...]
def addVLineWithKeepout(kicad_mod, x, y0, y1,layer, width, keepouts=[], roun=0.001):
    lines = [[y0, y1]]
    changes=True
    while (changes):
        changes=False
        for ko in keepouts:
            if (ko[0]<=x) & (x<=ko[1]):
                for li in reversed(range(0,len(lines))):
                    l=lines[li]
                    #print("V: ko=",ko,"  li=",li,"   l=",l,"   ls=",lines)
                    if (ko[2]<l[0]) & (l[1]<ko[3]) & (l[1]>ko[2]): # Line completely inside -> remove
                        lines.pop(li)
                        changes=True
                        break
                    elif (l[0]>ko[2]) & (l[1]<ko[3]) & (l[1] > ko[3]):  # Line starts inside, but ends outside -> remove and add shortened
                        lines.pop(li)
                        lines.append([ko[3], l[1]])
                        changes = True
                        break
                    elif (l[0]<ko[2] ) & (l[1] < ko[3])& (l[1] > ko[2]):  # Line starts outside, but ends inside -> remove and add shortened
                        lines.pop(li)
                        lines.append([l[0], ko[2]])
                        changes = True
                        break
                    elif (l[0]<ko[2]) & (l[1] > ko[3]):  # Line starts outside, and ends outside -> remove and add 2 shortened
                        lines.pop(li)
                        lines.append([l[0], ko[2]])
                        lines.append([ko[3], l[1]])
                        changes = True
                        break
                    if changes:
                        break
    for l in lines:
        kicad_mod.append(Line(start=[roundG(x, roun), roundG(l[0], roun)], end=[roundG(x, roun), roundG(l[1], roun)], layer=layer, width=width))


class pack:
    #      metal_/plastic_                                        ^
    #  <--------width------>                                      |
    #  +-------------------+                 ^                    y
    #  |                   |                 |                    x---->
    #  |        OO         | mounting drill  |
    #  |                   |                 |
    #  |   METAL           |                 |
    #  +-------------------+ ^               metal_height
    #  |                   | |               |
    #  |                   | |               |
    #  |   PLASTIC         | plastic_height  |
    #  |                   | |               |
    #  |                   | |               |
    #  |                   | |               |
    #  0-------------------+ v  0= ref pos   v
    #     |      |      |  ^
    #     |      |      |  |
    #     |      |      |  pin_minlength
    #     |      |      |  |
    #     |      |      |  v
    #    PPP    PPP    PPP      PADs
    #     <--rm-->
    #   <->
    #    pin_offset_x
    #
    #  0-------------------+  0= ref pos    ^             ^                z
    #  |   METAL           |                metal_depth   |                |
    #  +-------------------+ ^              v             pin_offset_z     |
    #  |   PLASTIC         | plastic_depth                |                v
    #  | PPP    PPP    PPP | |                            v
    #  +-------------------+ v
    #
    def __init__(self):
        self.plastic = [0, 0, 0]  # width,heigth,depth of plastic package, starting at bottom-left
        self.metal = [0, 0, 0]  # width,heigth,thickness of metal plate, starting at metal_offset from bottom-left
        self.pins = 0  # number of pins
        self.rm = 0  # pin distance
        self.pad = [0, 0]  # width/height of pads
        self.drill = 0  # diameter of pad drills
        self.name = ""  # name of package
        self.mounting_hole_pos = [0, 0]  # position of mounting hole from bottom-left
        self.mounting_hole_diameter = 0  # diameter of mounting hole in package
        self.mounting_hole_drill = 0  # diameter of mounting hole drill
        self.pin_minlength = 0  # min. elongation of pins before 90° bend
        self.pinw = [0, 0];  # width,height of pins
        self.tags = []  # description/keywords
        self.pin_offset_x = 0
        self.pin_offset_z = 0

    def __init__(self,name,largepads=False):
        if (name=="SOT93") | (name=="SOT93_2pin"):
            self.plastic = [15.2, 12.7, 4.6]  # width,heigth,depth of plastic package, starting at bottom-left
            self.metal = [15.2, 21, 2]  # width,heigth,thickness of metal plate, starting at metal_offset from bottom-left
            self.pins = 3  # number of pins
            self.rm = 5.5  # pin distance
            if name=="SOT93_2pin":
                self.pins = 2
                self.rm = 2*self.rm
            self.pad = [2.5, 4.5]  # width/height of pads
            self.drill = 1.5  # diameter of pad drills
            self.name = name  # name of package
            self.mounting_hole_pos = [15.2/2, 21-4.4]  # position of mounting hole from bottom-left
            self.mounting_hole_diameter = 4.25  # diameter of mounting hole in package
            self.mounting_hole_drill = 4  # diameter of mounting hole drill
            self.pin_minlength = 5.08  # min. elongation of pins before 90° bend
            self.pinw = [1.15, 0.4];  # width,height of pins
            self.tags = []  # description/keywords
            self.pin_offset_x = (15.2-11)/2
            self.pin_offset_z = 4.6-1.6
            if largepads:
                self.tags.append("large pads")
                self.pad = [3.5, 5.5]
        elif (name == "TO-218") | (name=="TO-218_2pin"):
            self.plastic = [15.92, 12.7, 5.08]  # width,heigth,depth of plastic package, starting at bottom-left
            self.metal = [self.plastic[0], 20.72,1.27]  # width,heigth,thickness of metal plate, starting at metal_offset from bottom-left
            self.pins = 3  # number of pins
            self.rm = 5.47  # pin distance
            if name=="TO-218_2pin":
                self.pins = 2
                self.rm = 2*self.rm
            self.pad = [2.5, 4.5]  # width/height of pads
            self.drill = 1.5  # diameter of pad drills
            self.name = name  # name of package
            self.mounting_hole_pos = [15.2 / 2, 16.2]  # position of mounting hole from bottom-left
            self.mounting_hole_diameter = 4.23  # diameter of mounting hole in package
            self.mounting_hole_drill = 4  # diameter of mounting hole drill
            self.pin_minlength = 5.08  # min. elongation of pins before 90° bend
            self.pinw = [1.15, 0.4];  # width,height of pins
            self.tags = []  # description/keywords
            self.pin_offset_x = (self.plastic[0] - (self.pins-1)*self.rm) / 2
            self.pin_offset_z = 2.79
            if largepads:
                self.tags.append("large pads")
                self.pad = [3.5, 5.5]
        elif (name == "TO-220") | (name=="TO-220_2pin")| (name=="TO-220_5pin"):
            self.plastic = [10, 9.25, 4.4]  # width,heigth,depth of plastic package, starting at bottom-left
            self.metal = [self.plastic[0], 15.65,1.27]  # width,heigth,thickness of metal plate, starting at metal_offset from bottom-left
            self.pins = 3  # number of pins
            self.rm = 2.54  # pin distance
            self.pad = [1.5, 2.5]  # width/height of pads
            self.drill = 1  # diameter of pad drills
            self.name = name  # name of package
            self.mounting_hole_pos = [self.plastic[0] / 2, self.metal[1]-2.8]  # position of mounting hole from bottom-left
            self.mounting_hole_diameter = 3.7  # diameter of mounting hole in package
            self.mounting_hole_drill = 3.5  # diameter of mounting hole drill
            self.pin_minlength = 3.81  # min. elongation of pins before 90° bend
            self.pinw = [0.75, 0.5];  # width,height of pins
            self.tags = []  # description/keywords
            self.pin_offset_z = 2.4
            if largepads:
                self.tags.append("large pads")
                self.pad = [1.7, 3.5]
            if name == "TO-220_2pin":
                self.pins = 2
                self.rm = 2 * self.rm
            if name == "TO-220_5pin":
                self.pins = 5
                self.rm=1.7
                self.pad = [1.3,2]
            self.pin_offset_x = (self.plastic[0] - (self.pins - 1) * self.rm) / 2

        else:
            __init__()

crt_offset = 0.25
slk_offset = 0.2
slk_dist = 0.3
lw_fab = 0.1
lw_crt = 0.05
lw_slk = 0.15
txt_offset = 1

# vertical symbols for rectangular transistors
def makeVERT(lib_name, neutral, largepads, pck, has3d=False, x_3d=[0,0,0], s_3d=[1/2.54,1/2.54,1/2.54], vertfirst=True, lptext="_LargePads"):

    l_fabp = -pck.pin_offset_x
    t_fabp = -pck.pin_offset_z
    w_fabp = pck.plastic[0]
    h_fabp = pck.plastic[2]

    w_fabm = pck.metal[0]
    h_fabm = pck.metal[2]
    
    l_slkp=l_fabp-slk_offset
    t_slkp = t_fabp - slk_offset
    w_slkp=w_fabp+2*slk_offset
    h_slkp = h_fabp + 2*slk_offset
    w_slkm=w_fabm+2*slk_offset
    h_slkm = h_fabm + 2*slk_offset

    l_crt = min(-pck.pad[0]/2, l_slkp)-crt_offset
    t_crt = min(-pck.pad[1]/2, t_slkp) - crt_offset
    w_crt = max(max(w_slkp, w_slkm),(pck.pins-1)*pck.rm+pck.pad[0]) + 2*crt_offset
    h_crt = max(max(h_slkp, h_slkm),-t_crt+pck.pad[1]/2) + 2*crt_offset

    l_mounth=l_fabp+pck.mounting_hole_pos[0]

    txt_x=l_slkp+max(w_slkp, w_slkm)/2
    
    tag_items=["Vertical", "RM {0}mm".format(pck.rm)]

    footprint_name=pck.name
    if vertfirst:
        footprint_name=footprint_name+"_Vertical"
    if neutral:
        tag_items.append("Neutral")
        footprint_name=footprint_name+"_Neutral"
        for p in range(1,pck.pins+1):
            footprint_name = footprint_name + "{0}".format(p)
    if ~vertfirst:
        footprint_name=footprint_name+"_Vertical"
    if largepads:
        tag_items.append("large Pads")
        footprint_name=footprint_name+lptext

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
    kicad_mod.append(Text(type='reference', text='REF**', at=[txt_x, t_slkp-txt_offset], layer='F.SilkS'))
    kicad_mod.append(Text(type='value', text=footprint_name, at=[txt_x, t_slkp+max(h_slkm,h_slkp)+txt_offset], layer='F.Fab'))

    # create FAB-layer
    kicad_mod.append(RectLine(start=[l_fabp, t_fabp], end=[l_fabp+w_fabp, t_fabp+h_fabp], layer='F.Fab', width=lw_fab))
    if (h_fabm>0):
        kicad_mod.append(Line(start=[l_fabp, t_fabp+h_fabm], end=[l_fabp+w_fabp, t_fabp+h_fabm], layer='F.Fab', width=lw_fab))
        kicad_mod.append(Line(start=[l_mounth-pck.mounting_hole_diameter/2, t_fabp], end=[l_mounth-pck.mounting_hole_diameter/2, t_fabp+h_fabm], layer='F.Fab', width=lw_fab))
        kicad_mod.append(Line(start=[l_mounth+pck.mounting_hole_diameter/2, t_fabp], end=[l_mounth+pck.mounting_hole_diameter/2, t_fabp+h_fabm], layer='F.Fab', width=lw_fab))
    else:
        kicad_mod.append(Line(start=[l_mounth - pck.mounting_hole_diameter / 2, t_fabp],end=[l_mounth - pck.mounting_hole_diameter / 2, t_fabp + h_fabp], layer='F.Fab',width=lw_fab))
        kicad_mod.append(Line(start=[l_mounth + pck.mounting_hole_diameter / 2, t_fabp],end=[l_mounth + pck.mounting_hole_diameter / 2, t_fabp + h_fabp], layer='F.Fab',width=lw_fab))

    # create SILKSCREEN-layer
    keepouts=[]
    x = 0
    for p in range(1, pck.pins + 1):
        keepouts.append([x-pck.pad[0]/2-slk_dist, x+pck.pad[0]/2+slk_dist,-pck.pad[1]/2-slk_dist, pck.pad[1]/2+slk_dist])
        x = x + pck.rm
        
    addHLineWithKeepout(kicad_mod, l_slkp, l_slkp+w_slkp, t_slkp, 'F.SilkS', lw_slk, keepouts)
    addHLineWithKeepout(kicad_mod, l_slkp, l_slkp+w_slkp, t_slkp+h_slkp, 'F.SilkS', lw_slk, keepouts)
    addVLineWithKeepout(kicad_mod, l_slkp, t_slkp, t_slkp+h_slkp, 'F.SilkS', lw_slk, keepouts)
    addVLineWithKeepout(kicad_mod, l_slkp+w_slkp, t_slkp, t_slkp+h_slkp, 'F.SilkS', lw_slk, keepouts)
    if (h_slkm>0):
        addHLineWithKeepout(kicad_mod, l_slkp, l_slkp+w_slkp, t_slkp+h_slkm, 'F.SilkS', lw_slk, keepouts)
        addVLineWithKeepout(kicad_mod, l_mounth - pck.mounting_hole_diameter / 2, t_slkp, t_slkp + h_slkm, 'F.SilkS', lw_slk, keepouts)
        addVLineWithKeepout(kicad_mod, l_mounth + pck.mounting_hole_diameter / 2, t_slkp, t_slkp + h_slkm, 'F.SilkS', lw_slk, keepouts)
    else:
        addVLineWithKeepout(kicad_mod, l_mounth - pck.mounting_hole_diameter / 2, t_slkp, t_slkp + h_slkp, 'F.SilkS', lw_slk, keepouts)
        addVLineWithKeepout(kicad_mod, l_mounth + pck.mounting_hole_diameter / 2, t_slkp, t_slkp + h_slkp, 'F.SilkS', lw_slk, keepouts)

    # create courtyard
    kicad_mod.append(RectLine(start=[roundCrt(l_crt), roundCrt(t_crt)], end=[roundCrt(l_crt+w_crt), roundCrt(t_crt+h_crt)], layer='F.CrtYd', width=lw_crt))
    

    # create pads
    x=0
    for p in range(1,pck.pins+1):
        kicad_mod.append(Pad(number=p, type=Pad.TYPE_THT, shape=Pad.SHAPE_OVAL, at=[x, 0], size=pck.pad, drill=pck.drill, layers=['*.Cu', '*.Mask']))
        x=x+pck.rm

    # add model
    if (has3d):
        kicad_mod.append(Model(filename=lib_name + ".3dshapes/"+footprint_name+".wrl", at=x_3d, scale=s_3d, rotate=[0, 0, 0]))

    # print render tree
    # print(kicad_mod.getRenderTree())
    # print(kicad_mod.getCompleteRenderTree())

    # write file
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile(footprint_name+'.kicad_mod')


# vertical symbols for rectangular transistors
def makeHOR(lib_name, neutral, largepads, pck, has3d=False, x_3d=[0, 0, 0], s_3d=[1 / 2.54, 1 / 2.54, 1 / 2.54],horfirst=True, lptext="_LargePads"):

    
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
    t_crt = t_slkp- max(h_slkp,h_slkm) - crt_offset
    w_crt = max(max(w_slkp, w_slkm), (pck.pins - 1) * pck.rm + pck.pad[0]) + 2 * crt_offset
    h_crt = (-t_crt + pck.pad[1] / 2) + 2 * crt_offset
    
    l_mounth = l_fabp + pck.mounting_hole_pos[0]
    t_mounth = t_fabp - pck.mounting_hole_pos[1]

    txt_x = l_slkp + max(w_slkp, w_slkm) / 2
    txt_t = (t_slkp -max(h_slkm,h_slkp))-txt_offset
    txt_b = pck.pad[1] / 2+txt_offset

    tag_items = ["Horizontal", "RM {0}mm".format(pck.rm)]
    
    footprint_name = pck.name
    if horfirst:
        footprint_name=footprint_name+"_Horizontal"
    if neutral:
        tag_items.append("Neutral")
        footprint_name = footprint_name + "_Neutral"
        for p in range(1, pck.pins + 1):
            footprint_name = footprint_name + "{0}".format(p)
    if ~horfirst:
        footprint_name=footprint_name+"_Horizontal"
    if largepads:
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
        kicad_mod.append(RectLine(start=[l_fabp, t_fabp], end=[l_fabp + w_fabm, t_fabp - h_fabm], layer='F.Fab', width=lw_fab))
    kicad_mod.append(RectLine(start=[l_fabp, t_fabp], end=[l_fabp + w_fabp, t_fabp - h_fabp], layer='F.Fab', width=lw_fab))
    kicad_mod.append(RectLine(start=[l_fabp, t_fabp], end=[l_fabp + w_fabp, t_fabp - h_fabp], layer='F.Fab', width=lw_fab))
    kicad_mod.append(Circle(center=[l_mounth, t_mounth], radius=pck.mounting_hole_diameter/2, layer='F.Fab', width=lw_fab))
    x = 0
    for p in range(1, pck.pins + 1):
        kicad_mod.append(Line(start=[x, t_fabp], end=[x, 0], layer='F.Fab', width=lw_fab))
        x = x + pck.rm

    # create SILKSCREEN-layer
    keepouts = []
    x = 0
    for p in range(1, pck.pins + 1):
        keepouts.append([x - pck.pad[0] / 2 - slk_dist, x + pck.pad[0] / 2 + slk_dist, -pck.pad[1] / 2 - slk_dist,
                         pck.pad[1] / 2 + slk_dist])
        x = x + pck.rm
    
    addHLineWithKeepout(kicad_mod, l_slkp, l_slkp + w_slkp, t_slkp, 'F.SilkS', lw_slk, keepouts)
    addHLineWithKeepout(kicad_mod, l_slkp, l_slkp + w_slkp, t_slkp - h_slkm, 'F.SilkS', lw_slk, keepouts)
    addVLineWithKeepout(kicad_mod, l_slkp, t_slkp, t_slkp - h_slkm, 'F.SilkS', lw_slk, keepouts)
    addVLineWithKeepout(kicad_mod, l_slkp + w_slkp, t_slkp, t_slkp - h_slkm, 'F.SilkS', lw_slk, keepouts)
    
    # create courtyard
    kicad_mod.append(
        RectLine(start=[roundCrt(l_crt), roundCrt(t_crt)], end=[roundCrt(l_crt + w_crt), roundCrt(t_crt + h_crt)],
                 layer='F.CrtYd', width=lw_crt))
    
    # create mounting hole
    kicad_mod.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_OVAL, at=[l_mounth, t_mounth], size=[pck.mounting_hole_drill,pck.mounting_hole_drill], drill=pck.mounting_hole_drill, layers=['*.Cu', '*.Mask']))

    # create pads
    x = 0
    for p in range(1, pck.pins + 1):
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


if __name__ == '__main__':
    makeVERT("TO_SOT_Packages_THT", True, False, pack("SOT93"))
    makeVERT("TO_SOT_Packages_THT", True, True, pack("SOT93",True))
    makeHOR("TO_SOT_Packages_THT", True, False, pack("SOT93"))
    makeHOR("TO_SOT_Packages_THT", True, True, pack("SOT93", True))
    makeVERT("TO_SOT_Packages_THT", True, False, pack("SOT93_2pin"))
    makeVERT("TO_SOT_Packages_THT", True, True, pack("SOT93_2pin",True))
    makeHOR("TO_SOT_Packages_THT", True, False, pack("SOT93_2pin"))
    makeHOR("TO_SOT_Packages_THT", True, True, pack("SOT93_2pin", True))

    makeVERT("TO_SOT_Packages_THT", True, False, pack("TO-218"))
    makeVERT("TO_SOT_Packages_THT", True, True, pack("TO-218",True))
    makeHOR("TO_SOT_Packages_THT", True, False, pack("TO-218"))
    makeHOR("TO_SOT_Packages_THT", True, True, pack("TO-218", True))
    makeVERT("TO_SOT_Packages_THT", True, False, pack("TO-218_2pin"))
    makeVERT("TO_SOT_Packages_THT", True, True, pack("TO-218_2pin",True))
    makeHOR("TO_SOT_Packages_THT", True, False, pack("TO-218_2pin"))
    makeHOR("TO_SOT_Packages_THT", True, True, pack("TO-218_2pin", True))
    
    makeVERT("TO_SOT_Packages_THT", True, False, pack("TO-220"), True, [0.1, 0, 0], [1 / 2.54, 1 / 2.54, 1 / 2.54], False, "_largePads")
    makeVERT("TO_SOT_Packages_THT", True, True, pack("TO-220",True), True, [0.1, 0, 0], [1 / 2.54, 1 / 2.54, 1 / 2.54], False, "_largePads")
    makeHOR("TO_SOT_Packages_THT", True, False, pack("TO-220"), True, [0.1, 0, 0], [1 / 2.54, 1 / 2.54, 1 / 2.54], False, "_largePads")
    makeHOR("TO_SOT_Packages_THT", True, True, pack("TO-220", True), True, [0.1, 0, 0], [1 / 2.54, 1 / 2.54, 1 / 2.54], False, "_largePads")
    makeVERT("TO_SOT_Packages_THT", True, False, pack("TO-220_2pin"), True, [0.1, 0, 0], [1 / 2.54, 1 / 2.54, 1 / 2.54], False, "_largePads")
    makeVERT("TO_SOT_Packages_THT", True, True, pack("TO-220_2pin",True), True, [0.1, 0, 0], [1 / 2.54, 1 / 2.54, 1 / 2.54], False, "_largePads")
    makeHOR("TO_SOT_Packages_THT", True, False, pack("TO-220_2pin"), True, [0.1, 0, 0], [1 / 2.54, 1 / 2.54, 1 / 2.54], False, "_largePads")
    makeHOR("TO_SOT_Packages_THT", True, True, pack("TO-220_2pin", True), True, [0.1, 0, 0], [1 / 2.54, 1 / 2.54, 1 / 2.54], False, "_largePads")
    makeVERT("TO_SOT_Packages_THT", True, False, pack("TO-220_5pin"), False, [0.1, 0, 0], [1 / 2.54, 1 / 2.54, 1 / 2.54], False, "_largePads")
    makeHOR("TO_SOT_Packages_THT", True, False, pack("TO-220_5pin"), False, [0.1, 0, 0], [1 / 2.54, 1 / 2.54, 1 / 2.54], False, "_largePads")
