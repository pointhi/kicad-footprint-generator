#!/usr/bin/env python

import sys
import os
import math
import time

# ensure that the kicad-footprint-generator directory is available
# sys.path.append(os.environ.get('KIFOOTPRINTGENERATOR'))  # enable package import from parent directory
# sys.path.append("D:\hardware\KiCAD\kicad-footprint-generator")  # enable package import from parent directory
sys.path.append(os.path.join(sys.path[0], "..", "..", "kicad_mod"))  # load kicad_mod path
sys.path.append(os.path.join(sys.path[0], "..", ".."))  # load kicad_mod path

from KicadModTree import *  # NOQA
from footprint_global_properties import *

# round for grid g
def roundG(x, g):
    if (x > 0):
        return math.ceil(x / g) * g
    else:
        return math.floor(x / g) * g


# round for courtyard grid
def roundCrt(x):
    return roundG(x, grid_crt)


# float-variant of range()
def frange(x, y, jump):
    while x < y:
        yield x
        x += jump


# inclusice float-variant of range()
def frangei(x, y, jump):
    while x <= y:
        yield x
        x += jump


# returns a list with a single rectangle around x,y with width and height w and h
def addKeepoutRect(x, y, w, h):
    return [[x - w / 2, x + w / 2, y - h / 2, y + h / 2]]


# returns a series of rectangle that lie around the circular pad around (x,y) with radius w=h
# if w!=h, addKeepoutRect() is called
def addKeepoutRound(x, y, w, h):
    if w != h:
        return addKeepoutRect(x, y, w, h)
    else:
        res = []
        Nrects = 4
        r = max(h, w) / 2
        yysum = 0
        for ya in frange(0, r, r / Nrects):
            a = math.fabs(math.asin(ya / r) / math.pi * 180)
            yy = math.fabs(r * math.sin(a / 180.0 * math.pi))
            xx = math.fabs(r * math.cos(a / 180.0 * math.pi))
            if (xx > 0):
                res.append([x - xx - 0.015, x + xx + 0.015, y - yy - r / Nrects - 0.015, y - yy + .015])
                res.append([x - xx - 0.015, x + xx + 0.015, y + yy - 0.015, y + yy + r / Nrects + 0.015])
            yysum = yysum + yy
        return res


def applyKeepouts(lines_in, y, xi, yi, keepouts):
    # print("  applyKeepouts(\n  lines_in=", lines_in, "  \n  y=", y, "   \n  xi=", xi, "   yi=", yi, "   \n  keepouts=", keepouts, ")")
    lines = lines_in
    changes = True
    while (changes):
        changes = False
        for ko in keepouts:
            ko = [min(ko[0], ko[1]), max(ko[0], ko[1]), min(ko[2], ko[3]), max(ko[2], ko[3])]
            if (ko[yi + 0] <= y) and (y <= ko[yi + 1]):
                # print("    INY: koy=", [ko[yi + 0], ko[yi + 1]], "  y=", y, "):             kox=", [ko[xi + 0], ko[xi + 1]])
                for li in reversed(range(0, len(lines))):
                    l = lines[li]
                    if (l[0] >= ko[xi + 0]) and (l[0] <= ko[xi + 1]) and (l[1] >= ko[xi + 0]) and (
                        l[1] <= ko[xi + 1]):  # Line completely inside -> remove
                        lines.pop(li)
                        # print("      H1: ko=", [ko[xi+0],ko[xi+1]], "  li=", li, "   l=", l, ")")
                        changes = True
                    elif (l[0] >= ko[xi + 0]) and (l[0] <= ko[xi + 1]) and (
                        l[1] > ko[xi + 1]):  # Line starts inside, but ends outside -> remove and add shortened
                        lines.pop(li)
                        lines.append([ko[xi + 1], l[1]])
                        # print("      H2: ko=", [ko[xi+0],ko[xi+1]], "  li=", li, "   l=", l, "): ", [ko[xi+1], l[1]])
                        changes = True
                    elif (l[0] < ko[xi + 0]) and (l[1] <= ko[xi + 1]) and (
                        l[1] >= ko[xi + 0]):  # Line starts outside, but ends inside -> remove and add shortened
                        lines.pop(li)
                        lines.append([l[0], ko[xi + 0]])
                        # print("      H3: ko=", [ko[xi+0],ko[xi+1]], "  li=", li, "   l=", l, "): ", [l[0], ko[xi+0]])
                        changes = True
                    elif (l[0] < ko[xi + 0]) and (
                        l[1] > ko[xi + 1]):  # Line starts outside, and ends outside -> remove and add 2 shortened
                        lines.pop(li)
                        lines.append([l[0], ko[xi + 0]])
                        lines.append([ko[xi + 1], l[1]])
                        # print("      H4: ko=", [ko[xi+0],ko[xi+1]], "  li=", li, "   l=", l, "): ", [l[0], ko[xi+0]], [ko[xi+1], l[1]])
                        changes = True
                        # else:
                        # print("      USE: ko=", [ko[xi+0],ko[xi+1]], "  li=", li, "   l=", l, "): ")
        if changes:
            break
    
    return lines


# split a vertical line so it does not interfere with keepout areas defined as [[x0,x1,y0,y1], ...]
def addHLineWithKeepout(kicad_mod, x0, x1, y, layer, width, keepouts=[], roun=0.001):
    # print("addHLineWithKeepout",y)
    linesout = applyKeepouts([[min(x0, x1), max(x0, x1)]], y, 0, 2, keepouts)
    for l in linesout:
        kicad_mod.append(
            Line(start=[roundG(l[0], roun), roundG(y, roun)], end=[roundG(l[1], roun), roundG(y, roun)], layer=layer,
                 width=width))



# split a vertical line so it does not interfere with keepout areas defined as [[x0,x1,y0,y1], ...]
def addVLineWithKeepout(kicad_mod, x, y0, y1, layer, width, keepouts=[], roun=0.001):
    # print("addVLineWithKeepout",x)
    linesout = applyKeepouts([[min(y0, y1), max(y0, y1)]], x, 2, 0, keepouts)
    for l in linesout:
        kicad_mod.append(
            Line(start=[roundG(x, roun), roundG(l[0], roun)], end=[roundG(x, roun), roundG(l[1], roun)], layer=layer,
                 width=width))


# split a rectangle so it does not interfere with keepout areas defined as [[x0,x1,y0,y1], ...]
def addRectWithKeepout(kicad_mod, x, y, w, h, layer, width, keepouts=[], roun=0.001):
    addHLineWithKeepout(kicad_mod, x, x+w, y, layer,width,keepouts,roun)
    addHLineWithKeepout(kicad_mod, x, x + w, y+h, layer, width, keepouts, roun)
    addVLineWithKeepout(kicad_mod, x, y, y+h, layer, width, keepouts, roun)
    addVLineWithKeepout(kicad_mod, x+w, y, y + h, layer, width, keepouts, roun)

# split a plus sign so it does not interfere with keepout areas defined as [[x0,x1,y0,y1], ...]
def addPlusWithKeepout(km, x, y, w, h, layer, width, keepouts=[], roun=0.001):
    addHLineWithKeepout(km, x, x+w, y+h/2, layer,width,keepouts,roun)
    addVLineWithKeepout(km, x+w/2, y, y+h, layer, width, keepouts, roun)
