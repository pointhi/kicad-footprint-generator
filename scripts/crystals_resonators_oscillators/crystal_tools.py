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

def roundG(x, g):
    if (x>0):
        return math.ceil(x/g)*g
    else:
        return math.floor(x/g)*g

 
def roundCrt(x):
    return roundG(x, 0.1)

def allBevelRect(model, x, size, layer, width, bevel_size=0.2):
    if bevel_size<=0:
        model.append(RectLine(start=x, end=[x[0]+size[0],x[1]+size[1]], layer=layer, width=width))
    else:
        model.append(PolygoneLine(polygone=[[x[0]+bevel_size,x[1]],
                                            [x[0]+size[0]-bevel_size, x[1]],
                                            [x[0]+size[0], x[1]+bevel_size],
                                            [x[0]+size[0], x[1]+size[1]-bevel_size],
                                            [x[0]+size[0]-bevel_size, x[1]+size[1]],
                                            [x[0]+bevel_size,x[1]+size[1]],
                                            [x[0],x[1]+size[1]-bevel_size],
                                            [x[0],x[1]+bevel_size],
                                            [x[0] + bevel_size, x[1]]], layer=layer, width=width))
            
def fillCircle(model, center, radius, layer, width):
    model.append(Circle(center=center, radius=radius, layer=layer, width=width))
    r = radius
    w=radius/3
    r=radius-w/2
    while r > w/2:
        if r - 0.9*w<=w/2:
            model.append(Circle(center=center, radius=r, layer=layer, width=r*2))
        else:
            model.append(Circle(center=center, radius=r, layer=layer, width=w))
        r = r - 0.9*w

def bevelRectTL(model, x, size, layer, width, bevel_size=1):
    model.append(PolygoneLine(polygone=[[x[0]+bevel_size,x[1]], [x[0]+size[0], x[1]], [x[0]+size[0], x[1]+size[1]], [x[0], x[1]+size[1]], [x[0], x[1]+bevel_size],[x[0]+bevel_size,x[1]]], layer=layer, width=width))

def bevelRectBL(model, x, size, layer, width, bevel_size=1):
    model.append(PolygoneLine(polygone=[[x[0],x[1]], [x[0]+size[0], x[1]], [x[0]+size[0], x[1]+size[1]], [x[0]+bevel_size, x[1]+size[1]], [x[0], x[1]+size[1]-bevel_size],[x[0],x[1]]], layer=layer, width=width))


def DIPRectT(model, x, size, layer, width, marker_size=2):
    model.append(PolygoneLine(polygone=[[x[0]+size[0]/2-marker_size/2,x[1]], [x[0], x[1]], [x[0], x[1]+size[1]], [x[0]+size[0], x[1]+size[1]], [x[0]+size[0], x[1]],[x[0]+size[0]/2+marker_size/2,x[1]]], layer=layer, width=width))
    model.append(Arc(center=[x[0]+size[0]/2,x[1]], start=[x[0]+size[0]/2-marker_size/2,x[1]], angle=-180, layer=layer, width=width))

def DIPRectL(model, x, size, layer, width, marker_size=2):
    model.append(PolygoneLine(polygone=[[x[0],x[1]+size[1]/2-marker_size/2],
                                        [x[0], x[1]],
                                        [x[0]+size[0], x[1]],
                                        [x[0]+size[0], x[1]+size[1]],
                                        [x[0],x[1]+size[1]],
                                        [x[0],x[1]+size[1]/2+marker_size/2]], layer=layer, width=width))
    model.append(Arc(center=[x[0],x[1]+size[1]/2], start=[x[0],x[1]+size[1]/2-marker_size/2], angle=180, layer=layer, width=width))

def DIPRectL_LeftOnly(model, x, size, layer, width, marker_size=2):
    model.append(Line(start=[x[0],x[1]+size[1]/2-marker_size/2], end=[x[0], x[1]], layer=layer, width=width))
    model.append(Line(start=[x[0],x[1]+size[1]], end=[x[0],x[1]+size[1]/2+marker_size/2], layer=layer, width=width))
    if size[0]>0:
        model.append(Line(start=[x[0], x[1]], end=[x[0]+size[0], x[1]], layer=layer, width=width))
        model.append(Line(start=[x[0], x[1] + size[1]], end=[x[0]+size[0], x[1] + size[1]], layer=layer, width=width))

    model.append(Arc(center=[x[0],x[1]+size[1]/2], start=[x[0],x[1]+size[1]/2-marker_size/2], angle=180, layer=layer, width=width))

def THTQuartzRect(model, x, size, inner_size, layer, width):
    model.append(RectLine(start=x, end=[x[0] + size[0], x[1] + size[1]], layer=layer, width=width))
    THTQuartz(model, [x[0]+(size[0]-inner_size[0])/2, x[1]+(size[1]-inner_size[1])/2], inner_size, layer, width)

def THTQuartz(model, x, size, layer, width):
    THTQuartzIncomplete(model, x, size, 180, layer, width)


def THTQuartzIncomplete(model, x, size, angle, layer, width):
    inner_size=size
    r=inner_size[1]/2
    xtl=[x[0] + size[0] / 2 - (inner_size[0] / 2 - r), x[1] + size[1] / 2 - inner_size[1] / 2]
    xtr=[x[0] + size[0] / 2 + (inner_size[0] / 2 - r), x[1] + size[1] / 2 - inner_size[1] / 2]
    xbl=[x[0] + size[0] / 2 - (inner_size[0] / 2 - r), x[1] + size[1] / 2 + inner_size[1] / 2]
    xbr=[x[0] + size[0] / 2 + (inner_size[0] / 2 - r), x[1] + size[1] / 2 + inner_size[1] / 2]
    cl=[x[0] + size[0] / 2 - (inner_size[0] / 2 - r), x[1] + size[1] / 2]
    cr=[x[0] + size[0] / 2 + (inner_size[0] / 2 - r), x[1] + size[1] / 2]
    model.append(Line(start=xtl, end=xtr, layer=layer, width=width))
    model.append(Line(start=xbl, end=xbr, layer=layer, width=width))
    if angle>=180:
        model.append(Arc(center=cl,start=xtl,angle=-angle, layer=layer, width=width))
        model.append(Arc(center=cr,start=xtr,angle=angle, layer=layer, width=width))
    else:
        model.append(Arc(center=cl, start=xtl, angle=-angle, layer=layer, width=width))
        model.append(Arc(center=cr, start=xtr, angle=angle, layer=layer, width=width))
        model.append(Arc(center=cl, start=xbl, angle=angle, layer=layer, width=width))
        model.append(Arc(center=cr, start=xbr, angle=-angle, layer=layer, width=width))

