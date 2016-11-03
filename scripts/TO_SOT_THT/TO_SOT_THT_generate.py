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

# split a vertical line into dashes, so it does not interfere with keepout areas defined as [[x0,x1,y0,y1], ...]
def addHDLineWithKeepout(kicad_mod, x0, dx, x1, y, layer, width, keepouts=[], roun=0.001):
    x=x0
    lines=[]
    while (x+dx)<x1:
        lines.append([x,x+dx])
        x=x+2*dx
    if len(lines)<=0:
        return
    changes = True
    while (changes):
        changes = False
        for ko in keepouts:
            if (ko[2] <= y) & (y <= ko[3]):
                for li in reversed(range(0, len(lines))):
                    l = lines[li]
                    # print("H: ko=",ko,"  li=",li,"   l=",l,"   ls=",lines)
                    if (ko[0] < l[0]) & (l[1] < ko[1]) & (l[1] > ko[0]):  # Line completely inside -> remove
                        lines.pop(li)
                        changes = True
                        break
                    elif (l[0] > ko[0]) & (l[1] < ko[1]) & (
                        l[1] > ko[1]):  # Line starts inside, but ends outside -> remove and add shortened
                        lines.pop(li)
                        lines.append([ko[1], l[1]])
                        changes = True
                        break
                    elif (l[0] < ko[0]) & (l[1] < ko[1]) & (
                        l[1] > ko[0]):  # Line starts outside, but ends inside -> remove and add shortened
                        lines.pop(li)
                        lines.append([l[0], ko[0]])
                        changes = True
                        break
                    elif (l[0] < ko[0]) & (
                        l[1] > ko[1]):  # Line starts outside, and ends outside -> remove and add 2 shortened
                        lines.pop(li)
                        lines.append([l[0], ko[0]])
                        lines.append([ko[1], l[1]])
                        changes = True
                        break
                    if changes:
                        break
    for l in lines:
        kicad_mod.append(Line(start=[roundG(l[0], roun), roundG(y, roun)], end=[roundG(l[1], roun), roundG(y, roun)],layer=layer, width=width))



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

# split a vertical line so it does not interfere with keepout areas defined as [[x0,x1,y0,y1], ...]
def addVDLineWithKeepout(kicad_mod, x, y0, dy, y1, layer, width, keepouts=[], roun=0.001):
    y=y0
    lines=[]
    while (y+dy)<y1:
        lines.append([y,y+dy])
        y=y+2*dy
    if len(lines)<=0:
        return
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
        self.largepads=False
        self.fpnametags=[]

    def __init__(self,name,pins=3,rm=0,largepads=False):
        self.largepads =largepads
        self.fpnametags = []
        if (name=="SOT93"):
            self.plastic = [15.2, 12.7, 4.6]  # width,heigth,depth of plastic package, starting at bottom-left
            self.metal = [15.2, 21, 2]  # width,heigth,thickness of metal plate, starting at metal_offset from bottom-left
            self.pins = 3  # number of pins
            self.rm = 5.5  # pin distance
            self.pad = [2.5, 4.5]  # width/height of pads
            self.drill = 1.5  # diameter of pad drills
            self.name = name  # name of package
            self.mounting_hole_pos = [15.2/2, 21-4.4]  # position of mounting hole from bottom-left
            self.mounting_hole_diameter = 4.25  # diameter of mounting hole in package
            self.mounting_hole_drill = 4  # diameter of mounting hole drill
            self.pin_minlength = 5.08  # min. elongation of pins before 90° bend
            self.pinw = [1.15, 0.4];  # width,height of pins
            self.tags = []  # description/keywords
            self.pin_offset_z = 4.6-1.6
            if largepads:
                self.pad = [3.5, 5.5]
                self.largepads =True
        elif (name == "TO-218"):
            self.plastic = [15.92, 12.7, 5.08]  # width,heigth,depth of plastic package, starting at bottom-left
            self.metal = [self.plastic[0], 20.72,1.27]  # width,heigth,thickness of metal plate, starting at metal_offset from bottom-left
            self.pins = 3  # number of pins
            self.rm = 5.47  # pin distance
            self.pad = [2.5, 4.5]  # width/height of pads
            self.drill = 1.5  # diameter of pad drills
            self.name = name  # name of package
            self.mounting_hole_pos = [15.2 / 2, 16.2]  # position of mounting hole from bottom-left
            self.mounting_hole_diameter = 4.23  # diameter of mounting hole in package
            self.mounting_hole_drill = 4  # diameter of mounting hole drill
            self.pin_minlength = 5.08  # min. elongation of pins before 90° bend
            self.pinw = [1.15, 0.4];  # width,height of pins
            self.tags = []  # description/keywords
            self.pin_offset_z = 2.79
            if largepads:
                self.pad = [3.5, 5.5]
                self.largepads = True
        elif (name == "TO-220"):
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
                self.largepads=True
        else:
            __init__()


        if rm > 0:
            self.rm = rm
        if pins != 3:
            self.name="{0}-{1}pin".format(self.name,pins)
            self.pins=pins
            if rm<=0:
                self.rm=2*self.rm/(pins-1)
            else:
                self.rm=rm;
        self.pin_offset_x = (self.plastic[0] - (self.pins - 1) * self.rm) / 2
        self.pad[0]=min(self.pad[0], 0.75*self.rm)
        if self.largepads:
            self.tags.append("large pads")
            

crt_offset = 0.25
slk_offset = 0.2
slk_dist = 0.3
lw_fab = 0.1
lw_crt = 0.05
lw_slk = 0.15
txt_offset = 1

# vertical symbols for rectangular transistors
def makeVERT(lib_name,  pck, has3d=False, x_3d=[0,0,0], s_3d=[1/2.54,1/2.54,1/2.54], lptext="_LargePads"):

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
    footprint_name=footprint_name+"_Vertical"
    for t in pck.fpnametags:
        footprint_name = footprint_name + "_" + t
    if pck.largepads:
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
    w_crt = max(max(w_slkp, w_slkm), (pck.pins - 1) * pck.rm + pck.pad[0]) + 2 * crt_offset
    h_crt = (-t_crt + pck.pad[1] / 2) + 2 * crt_offset
    
    l_mounth = l_fabp + pck.mounting_hole_pos[0]
    t_mounth = t_fabp - pck.mounting_hole_pos[1]
    
    txt_x = l_slkp + max(w_slkp, w_slkm) / 2
    txt_t = (t_slkp - max(h_slkm, h_slkp)) - txt_offset
    txt_b = pck.pad[1] / 2 + txt_offset
    
    tag_items = ["Horizontal", "RM {0}mm".format(pck.rm)]
    
    footprint_name = pck.name
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
        kicad_mod.append(
            RectLine(start=[l_fabp, t_fabp], end=[l_fabp + w_fabm, t_fabp - h_fabm], layer='F.Fab', width=lw_fab))
    kicad_mod.append(
        RectLine(start=[l_fabp, t_fabp], end=[l_fabp + w_fabp, t_fabp - h_fabp], layer='F.Fab', width=lw_fab))
    kicad_mod.append(
        RectLine(start=[l_fabp, t_fabp], end=[l_fabp + w_fabp, t_fabp - h_fabp], layer='F.Fab', width=lw_fab))
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
    kicad_mod.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_OVAL, at=[l_mounth, t_mounth],
                         size=[pck.mounting_hole_drill, pck.mounting_hole_drill], drill=pck.mounting_hole_drill,
                         layers=['*.Cu', '*.Mask']))
    
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
    t_crt = t_slkp + max(h_slkp, h_slkm) + crt_offset
    w_crt = max(max(w_slkp, w_slkm), (pck.pins - 1) * pck.rm + pck.pad[0]) + 2 * crt_offset
    h_crt = (-t_crt + pck.pad[1] / 2) + 2 * crt_offset
    
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
    kicad_mod.append(
        RectLine(start=[l_fabp, t_fabp], end=[l_fabp + w_fabp, t_fabp + h_fabp], layer='F.Fab', width=lw_fab))
    kicad_mod.append(
        RectLine(start=[l_fabp, t_fabp], end=[l_fabp + w_fabp, t_fabp + h_fabp], layer='F.Fab', width=lw_fab))
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
        keepouts.append([x - pck.pad[0] / 2 - slk_dist, x + pck.pad[0] / 2 + slk_dist, -pck.pad[1] / 2 - slk_dist,
                         pck.pad[1] / 2 + slk_dist])
        x = x + pck.rm
    
    addHLineWithKeepout(kicad_mod, l_slkp, l_slkp + w_slkp, t_slkp, 'F.SilkS', lw_slk, keepouts)
    addHLineWithKeepout(kicad_mod, l_slkp, l_slkp + w_slkp, t_slkp + h_slkp, 'F.SilkS', lw_slk, keepouts)
    addVLineWithKeepout(kicad_mod, l_slkp, t_slkp, t_slkp + h_slkp, 'F.SilkS', lw_slk, keepouts)
    addVLineWithKeepout(kicad_mod, l_slkp + w_slkp, t_slkp, t_slkp + h_slkp, 'F.SilkS', lw_slk, keepouts)
    if (h_fabm > 0):
        addHDLineWithKeepout(kicad_mod, l_slkp, 4*lw_slk, l_slkp + w_slkm, t_slkp + h_slkm, 'F.SilkS', lw_slk, keepouts)
        addVDLineWithKeepout(kicad_mod, l_slkp, t_slkp + h_slkp+lw_slk*2, 4 * lw_slk, t_slkp + h_slkm, 'F.SilkS', lw_slk, keepouts)
        addVDLineWithKeepout(kicad_mod, l_slkp + w_slkp, t_slkp + h_slkp+lw_slk*2, 4 * lw_slk, t_slkp + h_slkm, 'F.SilkS', lw_slk, keepouts)

    # create courtyard
    kicad_mod.append(
        RectLine(start=[roundCrt(l_crt), roundCrt(t_crt)], end=[roundCrt(l_crt + w_crt), roundCrt(t_crt + h_crt)],
                 layer='F.CrtYd', width=lw_crt))
    
    # create mounting hole
    kicad_mod.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_OVAL, at=[l_mounth, t_mounth],
                         size=[pck.mounting_hole_drill, pck.mounting_hole_drill], drill=pck.mounting_hole_drill,
                         layers=['*.Cu', '*.Mask']))
    
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
    packs=  ["SOT93",        "TO-218",       "TO-220"                          ]
    pins=   [[2,     3 ],    [2,     3    ],  [2,       3,         4,     5]   ]
    rms=    [[0,     0 ],    [0,     0    ],  [0,       0,      2.54,   1.7]   ]
    has3dv= [[False, False], [False, False], [True,  True,     False, False]   ]
    has3dh= [[False, False], [False, False], [True,  True,     False, False]   ]
    off3d=  [[[],    []],    [[],    []   ], [[0.1,0,0],[0.1,0,0],[],    []]   ]
    scale3d=[[[],    []],    [[],    []   ], [[],      [],        [],    []]   ]
    for p in range(0,len(packs)):
        for pidx in range(0,len(pins[p])):
            o3d=[0,0,0]
            s3d=[1 / 2.54, 1 / 2.54, 1 / 2.54]
            if len(off3d[p][pidx])>0:
                o3d=off3d[p][pidx]
            if len(scale3d[p][pidx])>0:
                s3d=scale3d[p][pidx]
            makeVERT("TO_SOT_Packages_THT", pack(packs[p], pins[p][pidx], rms[p][pidx], False), has3dv[p][pidx], o3d, s3d)
            makeVERT("TO_SOT_Packages_THT", pack(packs[p], pins[p][pidx], rms[p][pidx], True), has3dv[p][pidx], o3d, s3d)
            makeHOR("TO_SOT_Packages_THT", pack(packs[p], pins[p][pidx], rms[p][pidx], False), has3dh[p][pidx], o3d, s3d)
            makeHOR("TO_SOT_Packages_THT", pack(packs[p], pins[p][pidx], rms[p][pidx], True), has3dh[p][pidx], o3d, s3d)
            makeHORREV("TO_SOT_Packages_THT", pack(packs[p], pins[p][pidx], rms[p][pidx], False), has3dh[p][pidx], o3d, s3d)
            makeHORREV("TO_SOT_Packages_THT", pack(packs[p], pins[p][pidx], rms[p][pidx], True), has3dh[p][pidx], o3d, s3d)

