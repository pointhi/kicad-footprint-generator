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

def bevelRect(model, x, size, layer, width, bevel_size=1):
    model.append(PolygoneLine(polygone=[[x[0]+bevel_size,x[1]], [x[0]+size[0], x[1]], [x[0]+size[0], x[1]+size[1]], [x[0], x[1]+size[1]], [x[0], x[1]+bevel_size],[x[0]+bevel_size,x[1]]], layer=layer, width=width))
        

def DIPRect(model, x, size, layer, width, marker_size=2):
    model.append(PolygoneLine(polygone=[[x[0]+size[0]/2-marker_size/2,x[1]], [x[0], x[1]], [x[0], x[1]+size[1]], [x[0]+size[0], x[1]+size[1]], [x[0]+size[0], x[1]],[x[0]+size[0]/2+marker_size/2,x[1]]], layer=layer, width=width))
    model.append(Arc(center=[x[0]+size[0]/2,x[1]], start=[x[0]+size[0]/2-marker_size/2,x[1]], angle=-180, layer=layer, width=width))