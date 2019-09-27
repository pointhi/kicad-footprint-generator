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

# tool function for generating 3D-scripts
def script3d_writevariable(file, line, varname, value):
    file.write("# {0}\nApp.ActiveDocument.Spreadsheet.set('A{1}', 'var {0} = '); App.ActiveDocument.Spreadsheet.set('B{1}', '{2}'); App.ActiveDocument.Spreadsheet.setAlias('B{1}', '{0}')\n".format(varname, line, value))


# round for grid g
def roundG(x, g):
    if (x > 0):
        return math.ceil(x / g) * g
    else:
        return math.floor(x / g) * g

# round for grid g
def sqr(x):
    return x*x


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
        Nrects = 16
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

# internal method for keepout-processing
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
                                l[1] > ko[
                                    xi + 1]):  # Line starts inside, but ends outside -> remove and add shortened
                        lines.pop(li)
                        lines.append([ko[xi + 1], l[1]])
                        # print("      H2: ko=", [ko[xi+0],ko[xi+1]], "  li=", li, "   l=", l, "): ", [ko[xi+1], l[1]])
                        changes = True
                    elif (l[0] < ko[xi + 0]) and (l[1] <= ko[xi + 1]) and (
                                l[1] >= ko[
                                    xi + 0]):  # Line starts outside, but ends inside -> remove and add shortened
                        lines.pop(li)
                        lines.append([l[0], ko[xi + 0]])
                        # print("      H3: ko=", [ko[xi+0],ko[xi+1]], "  li=", li, "   l=", l, "): ", [l[0], ko[xi+0]])
                        changes = True
                    elif (l[0] < ko[xi + 0]) and (
                                l[1] > ko[
                                    xi + 1]):  # Line starts outside, and ends outside -> remove and add 2 shortened
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

# gives True if the given point (x,y) is contained in any keepout
def containedInAnyKeepout(x,y, keepouts):
    for ko in keepouts:
        ko = [min(ko[0], ko[1]), max(ko[0], ko[1]), min(ko[2], ko[3]), max(ko[2], ko[3])]
        if x>=ko[0] and x<=ko[1] and y>=ko[2] and y<=ko[3]:
            #print("HIT!")
            return True
    #print("NO HIT ",x,y)
    return False

# draws the keepouts
def debug_draw_keepouts(kicad_modg, keepouts):
    for ko in keepouts:
        kicad_modg.append(RectLine(start=[ko[0],ko[2]],
                                  end=[ko[1],ko[3]],
                                  layer='F.Mask', width=0.01))

# split a horizontal line so it does not interfere with keepout areas defined as [[x0,x1,y0,y1], ...]
def addHLineWithKeepout(kicad_mod, x0, x1, y, layer, width, keepouts=[], roun=0.001, dashed=False):
    if dashed:
        addHDLineWithKeepout(kicad_mod, x0, x1, y, layer, width, keepouts, roun)
    else:
        # print("addHLineWithKeepout",y)
        linesout = applyKeepouts([[min(x0, x1), max(x0, x1)]], y, 0, 2, keepouts)
        for l in linesout:
            kicad_mod.append(
                Line(start=[roundG(l[0], roun), roundG(y, roun)], end=[roundG(l[1], roun), roundG(y, roun)], layer=layer,width=width))

# draw a circle minding the keepouts
def addCircleWithKeepout(kicad_mod, x, y, radius, layer, width, keepouts=[], roun=0.001):
    dalpha = 2 * 3.1415 / (360)
    a = 0
    start=0
    startx=x + radius * math.sin(0)
    starty=y + radius * math.cos(0)
    hasToDraw=False
    noneUsed=True
    while a < 2 * 3.1415:
        x1 = x + radius * math.sin(a)
        y1 = y + radius * math.cos(a)

        if containedInAnyKeepout(x1,y1, keepouts):
            if hasToDraw and math.fabs(a-start)>0:
                kicad_mod.append( Arc(center=[roundG(x, roun), roundG(y, roun)], start=[roundG(startx, roun), roundG(starty, roun)], angle=-1*(a - start)/3.1415*180, layer=layer, width=width))
            hasToDraw = False
            startx=x1; starty=y1; start=a
            noneUsed = False
        else:
            hasToDraw = True

        a = a + dalpha
    if noneUsed:
        kicad_mod.append(
            Circle(center=[roundG(x, roun), roundG(y, roun)], radius=radius, layer=layer, width=width))
    elif hasToDraw and math.fabs(a - start) > 0:
        kicad_mod.append( Arc(center=[roundG(x, roun), roundG(y, roun)], start=[roundG(startx, roun), roundG(starty, roun)], angle=-1*(a - start)/3.1415*180, layer=layer, width=width))

# draw an arc
def addArcByAngles(kicad_mod, x, y, radius, angle_start, angle_end, layer, width, roun=0.001):
    startx = x + radius * math.sin(angle_start/180*3.1415)
    starty = y + radius * math.cos(angle_start/180*3.1415)
    kicad_mod.append( Arc(center=[roundG(x, roun), roundG(y, roun)], start=[roundG(startx, roun), roundG(starty, roun)], angle=-(angle_end-angle_start), layer=layer, width=width))

# draw an arc minding the keepouts
def addArcByAnglesWithKeepout(kicad_mod, x, y, radius, angle_start, angle_end, layer, width, keepouts=[], roun=0.001):
    startx = x + radius * math.sin(angle_start/180*3.1415)
    starty = y + radius * math.cos(angle_start/180*3.1415)
    addArcWithKeepout(kicad_mod, x, y, startx, starty, -(angle_end-angle_start), layer, width, keepouts, roun)

# draw an arc minding the keepouts
def addArcWithKeepout(kicad_mod, x, y, startx, starty, angle, layer, width, keepouts=[], roun=0.001):
    dalpha = angle/180*3.1415 / (360)
    radius=math.sqrt(sqr(x-startx)+sqr(y-starty));
    a = math.asin((startx-x)/radius)
    if starty<0:
        a=a+3.1415/2
    astart=a;
    aend=astart+angle/180*3.1415
    start=astart
    #print(radius, astart/3.1415*180, aend/3.1415*180)
    istartx=x + radius * math.sin(a)
    istarty=y + radius * math.cos(a)
    hasToDraw=False
    noneUsed=True
    while a < aend:
        x1 = x + radius * math.sin(a)
        y1 = y + radius * math.cos(a)

        if containedInAnyKeepout(x1,y1, keepouts):
            if hasToDraw and math.fabs(a-start)>0:
                #print('DRAW ',x1,y1)
                kicad_mod.append( Arc(center=[roundG(x, roun), roundG(y, roun)], start=[roundG(istartx, roun), roundG(istarty, roun)], angle=-1*(a - start)/3.1415*180, layer=layer, width=width))
            hasToDraw = False
            istartx=x1; istarty=y1; start=a
            noneUsed = False
        else:
            hasToDraw = True
        #print(a, dalpha, hasToDraw, noneUsed)
        a = a + dalpha
    if noneUsed:
        kicad_mod.append(
            Arc(center=[roundG(x, roun), roundG(y, roun)], start=[roundG(startx, roun), roundG(starty, roun)], angle=angle, layer=layer, width=width))
    elif hasToDraw and math.fabs(a - start) > 0:
        kicad_mod.append( Arc(center=[roundG(x, roun), roundG(y, roun)], start=[roundG(istartx, roun), roundG(istarty, roun)], angle=-1*(a - start)/3.1415*180, layer=layer, width=width))

# draw an ellipse with one axis along x-axis and one axis along y-axis and given width/height
def addEllipse(kicad_mod, x, y, w, h, layer, width, roun=0.001):
    factor=h/w
    alpha=math.atan(h/w)*2
    radius=w/2/math.sin(alpha)
    addArcByAngles(kicad_mod=kicad_mod, x=x, y=y+radius*math.cos(alpha), radius=radius, angle_start=180-alpha/3.1415*180, angle_end=180+alpha/3.1415*180, layer=layer, width=width, roun=roun);
    addArcByAngles(kicad_mod=kicad_mod, x=x, y=y-radius*math.cos(alpha), radius=radius, angle_start=alpha/3.1415*180, angle_end=-alpha/3.1415*180, layer=layer, width=width, roun=roun);

# draw an ellipse with one axis along x-axis and one axis along y-axis and given width/height
def addEllipseWithKeepout(kicad_mod, x, y, w, h, layer, width, keepouts=[], roun=0.001):
    factor=h/w
    alpha=math.atan(h/w)*2
    radius=w/2/math.sin(alpha)
    addArcByAnglesWithKeepout(kicad_mod=kicad_mod, x=x, y=y+radius*math.cos(alpha), radius=radius, angle_start=180-alpha/3.1415*180, angle_end=180+alpha/3.1415*180, keepouts=keepouts, layer=layer, width=width, roun=roun);
    addArcByAnglesWithKeepout(kicad_mod=kicad_mod, x=x, y=y-radius*math.cos(alpha), radius=radius, angle_start=alpha/3.1415*180, angle_end=-alpha/3.1415*180, keepouts=keepouts, layer=layer, width=width, roun=roun);

# split a circle so it does not interfere with keepout areas defined as [[x0,x1,y0,y1], ...]
def addDCircleWithKeepout(kicad_mod, x, y, radius, layer, width, keepouts=[], roun=0.001):
    dalpha = 2 * 3.1415 / (2 * 3.1415 * radius / (6 * width))
    a = 0
    while a < 2 * 3.1415:
        x1 = x + radius * math.sin(a)
        y1 = y + radius * math.cos(a)
        x2 = x + radius * math.sin(a + dalpha / 2)
        y2 = y + radius * math.cos(a + dalpha / 2)
        ok=True
        aa=a
        while aa<a+dalpha and ok:
            xx = x + radius * math.sin(aa)
            yy = y + radius * math.cos(aa)
            if containedInAnyKeepout(xx, yy, keepouts):
                ok=False
            aa=aa+dalpha/20
        if ok: kicad_mod.append(Arc(center=[roundG(x, roun), roundG(y, roun)], start=[roundG(x1, roun), roundG(y1, roun)],
                             angle=-1*dalpha / 2 / 3.1415 * 180, layer=layer, width=width))
        a = a + dalpha

# split an arbitrary line so it does not interfere with keepout areas defined as [[x0,x1,y0,y1], ...]
def addLineWithKeepout(kicad_mod, x1, y1, x2,y2, layer, width, keepouts=[], roun=0.001):
    dx=(x2-x1)/200
    dy=(y2-y1)/200
    x=x1; y=y1
    xs=x1; ys=y1;
    hasToDraw=not containedInAnyKeepout(x, y, keepouts)
    didDrawAny=False
    for n in range(0,200):
        if containedInAnyKeepout(x+dx, y+dy, keepouts):
            if hasToDraw:
                didDrawAny=True
                kicad_mod.append(Line(start=[roundG(xs, roun), roundG(ys, roun)], end=[roundG(x, roun), roundG(y, roun)], layer=layer, width=width))
            xs=x+2*dx; ys=y+2*dy; hasToDraw=False
        else:
            hasToDraw = True

        x=x+dx; y=y+dy
    if hasToDraw and ((xs!=x2 or ys!=y2) or (not didDrawAny)):
        kicad_mod.append(Line(start=[roundG(xs, roun), roundG(ys, roun)], end=[roundG(x2, roun), roundG(y2, roun)], layer=layer, width=width))


# split an arbitrary line so it does not interfere with keepout areas defined as [[x0,x1,y0,y1], ...]
def addPolyLineWithKeepout(kicad_mod, poly, layer, width, keepouts=[], roun=0.001):
    if len(poly)>1:
        for p in range(0, len(poly)-1):
            addLineWithKeepout(kicad_mod, poly[p][0], poly[p][1], poly[p+1][0], poly[p+1][1], layer, width, keepouts, roun)



# add a dashed circle
def addDCircle(kicad_mod, x, y, radius, layer, width, roun=0.001):
    dalpha = 2 * 3.1415 / (2 * 3.1415 * radius / (6 * width))
    a = 0
    while a < 2 * 3.1415:
        x1 = x + radius * math.sin(a)
        y1 = y + radius * math.cos(a)
        x2 = x + radius * math.sin(a + dalpha / 2)
        y2 = y + radius * math.cos(a + dalpha / 2)
        kicad_mod.append(Arc(center=[roundG(x, roun), roundG(y, roun)], start=[roundG(x1, roun), roundG(y1, roun)],
                             angle=dalpha / 2 / 3.1415 + 180, layer=layer, width=width))
        a = a + dalpha

# draw a circle with a screw slit under 45 degrees
def addSlitScrew(kicad_mod, x, y, radius, layer, width, roun=0.001):
    kicad_mod.append(Circle(center=[roundG(x, roun), roundG(y, roun)], radius=radius, layer=layer, width=width))
    da = 5
    dx1 = 0.99 * radius * math.sin((135 - da) / 180 * 3.1415)
    dy1 = 0.99 * radius * math.cos((135 - da) / 180 * 3.1415)
    dx2 = 0.99 * radius * math.sin((135 + da) / 180 * 3.1415)
    dy2 = 0.99 * radius * math.cos((135 + da) / 180 * 3.1415)
    dx3 = 0.99 * radius * math.sin((315 - da) / 180 * 3.1415)
    dy3 = 0.99 * radius * math.cos((315 - da) / 180 * 3.1415)
    dx4 = 0.99 * radius * math.sin((315 + da) / 180 * 3.1415)
    dy4 = 0.99 * radius * math.cos((315 + da) / 180 * 3.1415)
    # print(x,y,dx1,dy1,dx4,dy4)
    kicad_mod.append(Line(start=[roundG(x + dx1, roun), roundG(y + dy1, roun)],
                          end=[roundG(x + dx4, roun), roundG(y + dy4, roun)], layer=layer, width=width))
    kicad_mod.append(Line(start=[roundG(x + dx2, roun), roundG(y + dy2, roun)],
                          end=[roundG(x + dx3, roun), roundG(y + dy3, roun)], layer=layer, width=width))

# draw a circle with a screw slit under 45 degrees
def addSlitScrewWithKeepouts(kicad_mod, x, y, radius, layer, width, keepouts, roun=0.001):
    addCircleWithKeepout(kicad_mod, x, y, radius, layer, width, keepouts, roun)
    da = 5
    dx1 = 0.99 * radius * math.sin((135 - da) / 180 * 3.1415)
    dy1 = 0.99 * radius * math.cos((135 - da) / 180 * 3.1415)
    dx2 = 0.99 * radius * math.sin((135 + da) / 180 * 3.1415)
    dy2 = 0.99 * radius * math.cos((135 + da) / 180 * 3.1415)
    dx3 = 0.99 * radius * math.sin((315 - da) / 180 * 3.1415)
    dy3 = 0.99 * radius * math.cos((315 - da) / 180 * 3.1415)
    dx4 = 0.99 * radius * math.sin((315 + da) / 180 * 3.1415)
    dy4 = 0.99 * radius * math.cos((315 + da) / 180 * 3.1415)
    # print(x,y,dx1,dy1,dx4,dy4)
    addLineWithKeepout(kicad_mod,x + dx1, y + dy1, x + dx4, y + dy4, layer, width, keepouts)
    addLineWithKeepout(kicad_mod, x + dx2, y + dy2, x + dx3, y + dy3, layer, width, keepouts)


# draw a circle with a cross-screw under 45 deg
def addCrossScrew(kicad_mod, x, y, radius, layer, width, roun=0.001):
    kicad_mod.append(Circle(center=[roundG(x, roun), roundG(y, roun)], radius=radius, layer=layer, width=width))

    kkt = Translation(x, y)
    kicad_mod.append(kkt)
    dd = radius * 0.1 / 2
    dw = 0.8 * radius
    kkt.append(PolygoneLine(polygone=[[roundG(-dw, roun), roundG(-dd, roun)],
                                      [roundG(-dd, roun), roundG(-dd, roun)],
                                      [roundG(-dd, roun), roundG(-dw, roun)],
                                      [roundG(+dd, roun), roundG(-dw, roun)],
                                      [roundG(+dd, roun), roundG(-dd, roun)],
                                      [roundG(+dw, roun), roundG(-dd, roun)],
                                      [roundG(+dw, roun), roundG(+dd, roun)],
                                      [roundG(+dd, roun), roundG(+dd, roun)],
                                      [roundG(+dd, roun), roundG(+dw, roun)],
                                      [roundG(-dd, roun), roundG(+dw, roun)],
                                      [roundG(-dd, roun), roundG(+dd, roun)],
                                      [roundG(-dw, roun), roundG(+dd, roun)],
                                      [roundG(-dw, roun), roundG(-dd, roun)]], layer=layer, width=width))


# draw a circle with a cross-screw under 45 deg
def addCrossScrewWithKeepouts(kicad_mod, x, y, radius, layer, width, keepouts=[], roun=0.001):
    addCircleWithKeepout(kicad_mod, x, y, radius, layer, width, keepouts, roun)

    kkt = Translation(x, y)
    kicad_mod.append(kkt)
    dd = radius * 0.1 / 2
    dw = 0.8 * radius
    polygone = [[roundG(-dw, roun), roundG(-dd, roun)],
                [roundG(-dd, roun), roundG(-dd, roun)],
                [roundG(-dd, roun), roundG(-dw, roun)],
                [roundG(+dd, roun), roundG(-dw, roun)],
                [roundG(+dd, roun), roundG(-dd, roun)],
                [roundG(+dw, roun), roundG(-dd, roun)],
                [roundG(+dw, roun), roundG(+dd, roun)],
                [roundG(+dd, roun), roundG(+dd, roun)],
                [roundG(+dd, roun), roundG(+dw, roun)],
                [roundG(-dd, roun), roundG(+dw, roun)],
                [roundG(-dd, roun), roundG(+dd, roun)],
                [roundG(-dw, roun), roundG(+dd, roun)],
                [roundG(-dw, roun), roundG(-dd, roun)]];
    addPolyLineWithKeepout(kicad_mod, polygone, layer, width, keepouts)


# split a vertical line so it does not interfere with keepout areas defined as [[x0,x1,y0,y1], ...]
def addVLineWithKeepout(kicad_mod, x, y0, y1, layer, width, keepouts=[], roun=0.001, dashed=False):
    if dashed:
        addVDLineWithKeepout(kicad_mod, x, y0, y1, layer, width, keepouts, roun)
    else:
        # print("addVLineWithKeepout",x)
        linesout = applyKeepouts([[min(y0, y1), max(y0, y1)]], x, 2, 0, keepouts)
        for l in linesout:
            kicad_mod.append(
                Line(start=[roundG(x, roun), roundG(l[0], roun)], end=[roundG(x, roun), roundG(l[1], roun)], layer=layer,
                     width=width))

# split a dashed horizontal line so it does not interfere with keepout areas defined as [[x0,x1,y0,y1], ...]
def addHDLineWithKeepout(kicad_mod, x0, x1, y, layer, width, keepouts=[], roun=0.001):
    dx=3*width
    x=min(x0,x1)
    while x<max(x0,x1):
        addHLineWithKeepout(kicad_mod, x,min(x+dx,x1), y, layer, width, keepouts, roun)
        x=x+dx*2

# split a dashed vertical line so it does not interfere with keepout areas defined as [[x0,x1,y0,y1], ...]
def addVDLineWithKeepout(kicad_mod, x, y0, y1, layer, width, keepouts=[], roun=0.001):
    dy = 3 * width
    y = min(y0, y1)
    while y < max(y0, y1):
        addVLineWithKeepout(kicad_mod, x, y, min(y1,y+dy), layer, width, keepouts, roun)
        y = y + dy * 2



# split a rectangle
def addRectWith(kicad_mod, x, y, w, h, layer, width, roun=0.001):
	kicad_mod.append(RectLine(start=[roundG(x, roun),roundG(y, roun)], end=[roundG(x+w, roun),roundG(y+h, roun)], layer=layer, width=width))


# split a rectangle so it does not interfere with keepout areas defined as [[x0,x1,y0,y1], ...]
def addRectWithKeepout(kicad_mod, x, y, w, h, layer, width, keepouts=[], roun=0.001):
    addHLineWithKeepout(kicad_mod, x, x+w, y, layer,width,keepouts,roun)
    addHLineWithKeepout(kicad_mod, x, x + w, y+h, layer, width, keepouts, roun)
    addVLineWithKeepout(kicad_mod, x, y, y+h, layer, width, keepouts, roun)
    addVLineWithKeepout(kicad_mod, x+w, y, y + h, layer, width, keepouts, roun)

# split a rectangle so it does not interfere with keepout areas defined as [[x0,x1,y0,y1], ...]
def addRectAndTLMarkWithKeepout(kicad_mod, x, y, w, h, mark_len, layer, width, keepouts=[], roun=0.001):
    addHLineWithKeepout(kicad_mod, x, x+w, y, layer,width,keepouts,roun)
    addHLineWithKeepout(kicad_mod, x, x + w, y+h, layer, width, keepouts, roun)
    addVLineWithKeepout(kicad_mod, x, y, y+h, layer, width, keepouts, roun)
    addVLineWithKeepout(kicad_mod, x+w, y, y + h, layer, width, keepouts, roun)
    addHLineWithKeepout(kicad_mod, x-2*width, x+mark_len, y-2*width, layer,width,keepouts,roun)
    addVLineWithKeepout(kicad_mod, x-2*width, y-2*width, y+mark_len, layer,width,keepouts,roun)


# split a dashed rectangle so it does not interfere with keepout areas defined as [[x0,x1,y0,y1], ...]
def addDRectWithKeepout(kicad_mod, x, y, w, h, layer, width, keepouts=[], roun=0.001):
    addHDLineWithKeepout(kicad_mod, x, x+w, y, layer,width,keepouts,roun)
    addHDLineWithKeepout(kicad_mod, x, x + w, y+h, layer, width, keepouts, roun)
    addVDLineWithKeepout(kicad_mod, x, y, y+h, layer, width, keepouts, roun)
    addVDLineWithKeepout(kicad_mod, x+w, y, y + h, layer, width, keepouts, roun)

# split a plus sign so it does not interfere with keepout areas defined as [[x0,x1,y0,y1], ...]
def addPlusWithKeepout(km, x, y, w, h, layer, width, keepouts=[], roun=0.001):
    addHLineWithKeepout(km, x, x+w, y+h/2, layer,width,keepouts,roun)
    addVLineWithKeepout(km, x+w/2, y, y+h, layer, width, keepouts, roun)

# draw a rectangle with bevel on all sides (e.g. for crystals), or a simple rectangle if bevel_size0=0)
#
#   /----\
#  /      \
# |        |
# |        |
# |        |
# |        |
# |        |
#  \      /
#   \----/
def allBevelRect(model, x, size, layer, width, bevel_size=0.2):
    if bevel_size <= 0:
        model.append(RectLine(start=x, end=[x[0] + size[0], x[1] + size[1]], layer=layer, width=width))
    else:
        model.append(PolygoneLine(polygone=[[x[0] + bevel_size, x[1]],
                                            [x[0] + size[0] - bevel_size, x[1]],
                                            [x[0] + size[0], x[1] + bevel_size],
                                            [x[0] + size[0], x[1] + size[1] - bevel_size],
                                            [x[0] + size[0] - bevel_size, x[1] + size[1]],
                                            [x[0] + bevel_size, x[1] + size[1]],
                                            [x[0], x[1] + size[1] - bevel_size],
                                            [x[0], x[1] + bevel_size],
                                            [x[0] + bevel_size, x[1]]], layer=layer, width=width))

# draw a trapezoid with a given angle of the vertical lines
#
# angle<0
#      /---------------------\     ^
#     /                       \    |
#    /                         \  size[1]
#   /                           \  |
#  /-----------------------------\ v
#  <------------size[0]---------->
def allTrapezoid(model, x, size, angle, layer, width):
    dx=size[1]*math.tan(math.fabs(angle)/180*math.pi)
    if angle == 0:
        model.append(RectLine(start=x, end=[x[0] + size[0], x[1] + size[1]], layer=layer, width=width))
    elif angle<0:
        model.append(PolygoneLine(polygone=[[x[0] + dx, x[1]],
                                            [x[0] + size[0] - dx, x[1]],
                                            [x[0] + size[0], x[1] + size[1]],
                                            [x[0], x[1] + size[1] ],
                                            [x[0] + dx, x[1]]], layer=layer, width=width))
    elif angle>0:
        model.append(PolygoneLine(polygone=[[x[0], x[1]],
                                            [x[0] + size[0], x[1]],
                                            [x[0] + size[0]-dx, x[1] + size[1]],
                                            [x[0] + dx, x[1] + size[1] ],
                                            [x[0] , x[1]]], layer=layer, width=width))

# draw a downward equal-sided triangle
def allEqualSidedDownTriangle(model, xcenter, side_length, layer, width):
    h=sqrt(3)/6*side_length
    model.append(PolygoneLine(polygone=[[xcenter[0]-side_length/2, xcenter[1]-h],
                                        [xcenter[0]+side_length/2, xcenter[1]-h],
                                        [xcenter[0], xcenter[1]+2*h],
                                        [xcenter[0]-side_length/2, xcenter[1]-h],
                                       ], layer=layer, width=width))

# draw a trapezoid with a given angle of the vertical lines and rounded corners
#
# angle<0
#      /---------------------\     ^
#     /                       \    |
#    /                         \  size[1]
#   /                           \  |
#  /-----------------------------\ v
#  <------------size[0]---------->
def allRoundedBevelRect(model, x, size, angle, corner_radius, layer, width):
    if corner_radius<=0:
        allTrapezoid(model,x,size,angle,layer,width)
    else:
        dx=size[1]*math.tan(math.fabs(angle)/180*math.pi)
        dx2=corner_radius*math.tan((90-math.fabs(angle))/2/180*math.pi)
        dx3=corner_radius/math.tan((90-math.fabs(angle))/2/180*math.pi)
        ds2=corner_radius*math.sin(math.fabs(angle)/180*math.pi)
        dc2=corner_radius*math.cos(math.fabs(angle)/180*math.pi)

        if angle == 0:
            addRoundedRect(model, x, size, corner_radius, layer, width=0.2)
        elif angle<0:
            ctl=[x[0] +dx+dx2, x[1]+corner_radius]
            ctr=[x[0] + size[0]-dx-dx2, x[1]+corner_radius]
            cbl=[x[0] +dx3, x[1]+size[1]-corner_radius]
            cbr=[x[0] + size[0]-dx3, x[1]+size[1]-corner_radius]
            model.append(Arc(center=ctl, start=[ctl[0], x[1]], angle=-(90-math.fabs(angle)),layer=layer, width=width))
            model.append(Arc(center=ctr, start=[ctr[0], x[1]], angle=(90-math.fabs(angle)),layer=layer, width=width))
            model.append(Arc(center=cbl, start=[cbl[0], x[1]+size[1]], angle=(90+math.fabs(angle)),layer=layer, width=width))
            model.append(Arc(center=cbr, start=[cbr[0], x[1]+size[1]], angle=-(90+math.fabs(angle)),layer=layer, width=width))
            model.append(Line(start=[ctl[0], x[1]], end=[ctr[0], x[1]], layer=layer, width=width))
            model.append(Line(start=[cbl[0], x[1]+size[1]], end=[cbr[0], x[1]+size[1]], layer=layer, width=width))
            model.append(Line(start=[ctr[0]+dc2,ctr[1]-ds2], end=[cbr[0]+dc2,cbr[1]-ds2], layer=layer, width=width))
            model.append(Line(start=[ctl[0]-dc2,ctl[1]-ds2], end=[cbl[0]-dc2,cbl[1]-ds2], layer=layer, width=width))
        elif angle>0:
            cbl=[x[0] +dx+dx2, x[1]+size[1]-corner_radius]
            cbr=[x[0] + size[0]-dx-dx2, x[1]+size[1]-corner_radius]
            ctl=[x[0] +dx3, x[1]+corner_radius]
            ctr=[x[0] + size[0]-dx3, x[1]+corner_radius]
            model.append(Arc(center=ctl, start=[ctl[0], x[1]], angle=-(90+math.fabs(angle)),layer=layer, width=width))
            model.append(Arc(center=ctr, start=[ctr[0], x[1]], angle=(90+math.fabs(angle)),layer=layer, width=width))
            model.append(Arc(center=cbl, start=[cbl[0], x[1]+size[1]], angle=(90-math.fabs(angle)),layer=layer, width=width))
            model.append(Arc(center=cbr, start=[cbr[0], x[1]+size[1]], angle=-(90-math.fabs(angle)),layer=layer, width=width))
            model.append(Line(start=[ctl[0], x[1]], end=[ctr[0], x[1]], layer=layer, width=width))
            model.append(Line(start=[cbl[0], x[1]+size[1]], end=[cbr[0], x[1]+size[1]], layer=layer, width=width))
            model.append(Line(start=[ctr[0]+dc2,ctr[1]+ds2], end=[cbr[0]+dc2,cbr[1]+ds2], layer=layer, width=width))
            model.append(Line(start=[ctl[0]-dc2,ctl[1]+ds2], end=[cbl[0]-dc2,cbl[1]+ds2], layer=layer, width=width))


# draw a rectangle with rounded corners on all sides (e.g. for crystals), or a simple rectangle if bevel_size0=0)
#
#   /----\
#  /      \
# |        |
# |        |
# |        |
# |        |
# |        |
#  \      /
#   \----/
def addRoundedRect(model, x, size, corner_radius, layer, width=0.2):
    if corner_radius <= 0:
        model.append(RectLine(start=x, end=[x[0] + size[0], x[1] + size[1]], layer=layer, width=width))
    else:
        model.append(Line(start=[x[0] + corner_radius, x[1]], end=[x[0] + size[0] - corner_radius, x[1]], layer=layer, width=width))
        model.append(Line(start=[x[0] + size[0], x[1] + corner_radius], end=[x[0] + size[0], x[1] + size[1] - corner_radius], layer=layer, width=width))
        model.append(Line(start=[x[0] + size[0] - corner_radius, x[1] + size[1]], end=[x[0] + corner_radius, x[1] + size[1]], layer=layer, width=width))
        model.append(Line(start=[x[0], x[1] + size[1] - corner_radius], end=[x[0], x[1] + corner_radius], layer=layer, width=width))
        model.append(Arc(center=[x[0]+corner_radius, x[1] +corner_radius], start=[x[0], x[1] +corner_radius], angle=90, layer=layer, width=width))
        model.append(Arc(center=[x[0]+ size[0]-corner_radius, x[1] +corner_radius], start=[x[0]+ size[0]-corner_radius, x[1]], angle=90, layer=layer, width=width))
        model.append(Arc(center=[x[0]+corner_radius, x[1] +size[1]-corner_radius], start=[x[0], x[1] +size[1]-corner_radius], angle=-90, layer=layer, width=width))
        model.append(Arc(center=[x[0]+ size[0]-corner_radius, x[1] +size[1]-corner_radius], start=[x[0]+ size[0], x[1] +size[1]-corner_radius], angle=90, layer=layer, width=width))



# draws a filled circle consisting of concentric circles of varying widths (e.g. for glue dots!)
def fillCircle(model, center, radius, layer, width):
    model.append(Circle(center=center, radius=radius, layer=layer, width=width))
    r = radius
    w = radius / 3
    r = radius - w / 2
    while r > w / 2:
        if r - 0.9 * w <= w / 2:
            model.append(Circle(center=center, radius=r, layer=layer, width=r * 2))
        else:
            model.append(Circle(center=center, radius=r, layer=layer, width=w))
        r = r - 0.9 * w



#     +------+
#    /       |
#   /        |
#   |        |
#   |        |
#   |        |
#   |        |
#   +--------+
#
#
def bevelRectTL(model, x, size, layer, width, bevel_size=1):
    model.append(PolygoneLine(
        polygone=[[x[0] + bevel_size, x[1]], [x[0] + size[0], x[1]], [x[0] + size[0], x[1] + size[1]],
                  [x[0], x[1] + size[1]], [x[0], x[1] + bevel_size], [x[0] + bevel_size, x[1]]], layer=layer,
        width=width))


#   +--------+
#   |        |
#   |        |
#   |        |
#   |        |
#   \        |
#    \       |
#     +------+
#
#
def bevelRectBL(model, x, size, layer, width, bevel_size=1):
    model.append(PolygoneLine(polygone=[[x[0], x[1]], [x[0] + size[0], x[1]], [x[0] + size[0], x[1] + size[1]],
                                        [x[0] + bevel_size, x[1] + size[1]], [x[0], x[1] + size[1] - bevel_size],
                                        [x[0], x[1]]], layer=layer, width=width))

# draws a DIP-package with half-circle at the top
#
# +----------+
# |   \  /   |
# |    ~~    |
# |          |
# |          |
# |          |
# |          |
# +----------+
def DIPRectT(model, x, size, layer, width, marker_size=2):
    model.append(PolygoneLine(
        polygone=[[x[0] + size[0] / 2 - marker_size / 2, x[1]], [x[0], x[1]], [x[0], x[1] + size[1]],
                  [x[0] + size[0], x[1] + size[1]], [x[0] + size[0], x[1]],
                  [x[0] + size[0] / 2 + marker_size / 2, x[1]]], layer=layer, width=width))
    model.append(Arc(center=[x[0] + size[0] / 2, x[1]], start=[x[0] + size[0] / 2 - marker_size / 2, x[1]], angle=-180,
                     layer=layer, width=width))


# draws a DIP-package with half-circle at the left
#
# +---------------+
# |-\             |
# |  |            |
# |-/             |
# +---------------+
def DIPRectL(model, x, size, layer, width, marker_size=2):
    model.append(PolygoneLine(polygone=[[x[0], x[1] + size[1] / 2 - marker_size / 2],
                                        [x[0], x[1]],
                                        [x[0] + size[0], x[1]],
                                        [x[0] + size[0], x[1] + size[1]],
                                        [x[0], x[1] + size[1]],
                                        [x[0], x[1] + size[1] / 2 + marker_size / 2]], layer=layer, width=width))
    model.append(Arc(center=[x[0], x[1] + size[1] / 2], start=[x[0], x[1] + size[1] / 2 - marker_size / 2], angle=180,
                     layer=layer, width=width))


# draws the left part of a DIP-package with half-circle at the left
#
# +--------
# |-\
# |  |
# |-/
# +--------
def DIPRectL_LeftOnly(model, x, size, layer, width, marker_size=2):
    model.append(Line(start=[x[0], x[1] + size[1] / 2 - marker_size / 2], end=[x[0], x[1]], layer=layer, width=width))
    model.append(
        Line(start=[x[0], x[1] + size[1]], end=[x[0], x[1] + size[1] / 2 + marker_size / 2], layer=layer, width=width))
    if size[0] > 0:
        model.append(Line(start=[x[0], x[1]], end=[x[0] + size[0], x[1]], layer=layer, width=width))
        model.append(Line(start=[x[0], x[1] + size[1]], end=[x[0] + size[0], x[1] + size[1]], layer=layer, width=width))

    model.append(Arc(center=[x[0], x[1] + size[1] / 2], start=[x[0], x[1] + size[1] / 2 - marker_size / 2], angle=180,
                     layer=layer, width=width))


# draws a THT quartz footprint (HC49) with a rect around it
#  +-------------------------+
#  |                         |
#  |   +----------------+    |
#  |  /                  \   |
#  |  \                  /   |
#  |   +----------------+    |
#  |                         |
#  +-------------------------+
def THTQuartzRect(model, x, size, inner_size, layer, width):
    model.append(RectLine(start=x, end=[x[0] + size[0], x[1] + size[1]], layer=layer, width=width))
    THTQuartz(model, [x[0] + (size[0] - inner_size[0]) / 2, x[1] + (size[1] - inner_size[1]) / 2], inner_size, layer,
              width)


# draws a THT quartz footprint (HC49)
#     +----------------+
#    /                  \
#    \                  /
#     +----------------+
def THTQuartz(model, x, size, layer, width):
    THTQuartzIncomplete(model, x, size, 180, layer, width)


# draws a THT quartz footprint (HC49)
#     +----------------+
#    /                  \
#    \                  /
#     +----------------+
def THTQuartzIncomplete(model, x, size, angle, layer, width):
    inner_size = size
    r = inner_size[1] / 2
    xtl = [x[0] + size[0] / 2 - (inner_size[0] / 2 - r), x[1] + size[1] / 2 - inner_size[1] / 2]
    xtr = [x[0] + size[0] / 2 + (inner_size[0] / 2 - r), x[1] + size[1] / 2 - inner_size[1] / 2]
    xbl = [x[0] + size[0] / 2 - (inner_size[0] / 2 - r), x[1] + size[1] / 2 + inner_size[1] / 2]
    xbr = [x[0] + size[0] / 2 + (inner_size[0] / 2 - r), x[1] + size[1] / 2 + inner_size[1] / 2]
    cl = [x[0] + size[0] / 2 - (inner_size[0] / 2 - r), x[1] + size[1] / 2]
    cr = [x[0] + size[0] / 2 + (inner_size[0] / 2 - r), x[1] + size[1] / 2]
    model.append(Line(start=xtl, end=xtr, layer=layer, width=width))
    model.append(Line(start=xbl, end=xbr, layer=layer, width=width))
    if angle >= 180:
        model.append(Arc(center=cl, start=xtl, angle=-angle, layer=layer, width=width))
        model.append(Arc(center=cr, start=xtr, angle=angle, layer=layer, width=width))
    else:
        model.append(Arc(center=cl, start=xtl, angle=-angle, layer=layer, width=width))
        model.append(Arc(center=cr, start=xtr, angle=angle, layer=layer, width=width))
        model.append(Arc(center=cl, start=xbl, angle=angle, layer=layer, width=width))
        model.append(Arc(center=cr, start=xbr, angle=-angle, layer=layer, width=width))

#
# This is an alternative to using silk keepout areas for simple cases.
# It calculates a new endpoint for a horizontal or vertical line such that
# the silk line has the correct minimal clearance. If the line is to short
# given the default clearance, the clearance is reduced and new points are
# calculated.
#
# Parameters:
#   - pad_size, pad_position, and pad_radius are the dimensions of the reference pad.
#     (pad that is expected to be intersected by the line)
#   - fixed_point: The fixed reference point
#   - moving_point: The point that will be moved (toward the fixed point)
#     if the line intersects the pads clearance area.
#   - silk_pad_offset: offset between edge of the pad and silk line center.
#   - min_lenght: minimum silk line length
#
# Returns a new point along the line or None if no valid point could be found
#
def nearestSilkPointOnOrthogonalLineSmallClerance(pad_size, pad_position, pad_radius, fixed_point, moving_point,
        silk_pad_offset_default, silk_pad_offset_reduced, min_lenght):
    if silk_pad_offset_reduced < silk_pad_offset_default:
        offset = (silk_pad_offset_default, silk_pad_offset_reduced)
    else:
        offset = (silk_pad_offset_default)

    for silk_pad_offset in (silk_pad_offset_default, silk_pad_offset_reduced):
        point = nearestSilkPointOnOrthogonalLine(
                pad_size, pad_position, pad_radius, fixed_point, moving_point,
                silk_pad_offset, min_lenght)
        if point is not None:
            return point
    return None

#
# This is an alternative to using silk keepout areas for simple cases.
# It calculates a new endpoint for a horizontal or vertical line such that
# the silk line has the correct minimal clearance.
#
# Parameters:
#   - pad_size, pad_position, and pad_radius are the dimensions of the reference pad.
#     (pad that is expected to be intersected by the line)
#   - fixed_point: The fixed reference point
#   - moving_point: The point that will be moved (toward the fixed point)
#     if the line intersects the pads clearance area.
#   - silk_pad_offset: offset between edge of the pad and silk line center.
#   - min_lenght: minimum silk line length
#
# Returns a new point along the line or None if no valid point could be found
#
def nearestSilkPointOnOrthogonalLine(pad_size, pad_position, pad_radius, fixed_point, moving_point,
        silk_pad_offset, min_lenght):
    if fixed_point[0] == moving_point[0]:
        normal_dir_idx = 0
    elif fixed_point[1] == moving_point[1]:
        normal_dir_idx = 1
    else:
        raise ValueError("nearestSilkPointOnOrthogonalLine only works for horizontal or vertical lines. \n"
                        "(Either x or y coordinate of the two reference points must be equal)")

    inline_dir_idx = (normal_dir_idx+1)%2

    line_pad_offset = fixed_point[normal_dir_idx] - pad_position[normal_dir_idx]

    rc_normal_dir = pad_size[normal_dir_idx]/2-pad_radius

    sign = 1 if pad_position[inline_dir_idx] - fixed_point[inline_dir_idx] > 0 else -1
    ep_new = Vector2D(moving_point)

    if rc_normal_dir < line_pad_offset:
        # the silk outline is in the area where the radius of the pad is.

        dr_normal_dir = line_pad_offset - rc_normal_dir

        r = pad_radius + silk_pad_offset

        # rounding to avoid floating point errors
        if round(dr_normal_dir, 6) >= round(r, 6):
            return moving_point

        dr_inline = sqrt(r**2 - dr_normal_dir**2)

        ep_new[inline_dir_idx] =  pad_position[inline_dir_idx] -\
            sign*(pad_size[inline_dir_idx]/2 - (pad_radius-dr_inline))
    else:
        ep_new[inline_dir_idx] =  pad_position[inline_dir_idx] -\
            sign*(pad_size[inline_dir_idx]/2 + silk_pad_offset)

    if sign*(ep_new[inline_dir_idx] - fixed_point[inline_dir_idx]) <  min_lenght:
        return None

    if abs(ep_new[inline_dir_idx] - fixed_point[inline_dir_idx]) > math.fabs(moving_point[inline_dir_idx] - fixed_point[inline_dir_idx]):
        return moving_point

    return ep_new
