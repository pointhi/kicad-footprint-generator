#!/usr/bin/env python3

import sys
import os

# load parent path of KicadModTree
sys.path.append(os.path.join(sys.path[0], "..", ".."))

from KicadModTree import *

def rotary_coded_switch(args):
    footprint_name = args["name"]
    style = args["style"]
    datasheet = args["datasheet"]
    thru_hole = args["thru_hole"]
    pad_width = args["pad_width"]
    pad_height = args["pad_height"]
    pad_x_spacing = args["pad_x_spacing"]
    pad_y_spacing = args["pad_y_spacing"]
    gray = args["gray"]
    drill_size = args["drill_size"]
    pkg_width = args["pkg_width"]
    pkg_height = args["pkg_height"]

    f = Footprint(footprint_name)
    f.setDescription("4-bit rotary coded switch, " + style + ", " + datasheet)
    f.setTags("rotary switch bcd")
    if thru_hole:
        tech = "THT"
    else:
        tech = "SMD"
        f.setAttribute("smd")
    f.append(Model(filename="${KISYS3DMOD}/Buttons_Switches_" + tech + ".3dshapes/" + footprint_name + ".wrl", at=[0, 0, 0], scale=[1, 1, 1], rotate=[0.0, 0.0, 0.0]))

    wCrtYd = 0.05
    wFab = 0.1
    wSilkS = 0.12
    s = [1.0, 1.0]
    t = 0.15

    silk_clearance = 0.2
    crtYd = 0.25

    d = [drill_size, drill_size]
    p = [pad_width, pad_height]

    if thru_hole:
        rows = [0, pad_y_spacing, 2 * pad_y_spacing]
        columns = [0, pad_x_spacing]
    else:
        rows = [-pad_y_spacing, 0, pad_y_spacing]
        columns = [-pad_x_spacing / 2, pad_x_spacing / 2]

    if gray:
        pins = ["1", "8", "C", "X", "4", "2"]
    else:
        pins = ["1", "8", "C", "C", "4", "2"]

    xCenter = (columns[0] + columns[1]) / 2
    yCenter = rows[1]

    xLeft = xCenter - pkg_width / 2
    xRight = xCenter + pkg_width / 2
    yTop = yCenter - pkg_height / 2
    yBottom = yCenter + pkg_height / 2
    chamfer = 1.0

    yRef = yTop - 1.25
    yValue = yBottom + 1.25

    boundLeft = xCenter - (pad_x_spacing + pad_width) / 2
    boundRight = xCenter + (pad_x_spacing + pad_width) / 2

    r = (pad_x_spacing - pad_width) / 2 - silk_clearance

    # Text
    f.append(Text(type="reference", text="REF**", at=[xCenter, yRef],
                  layer="F.SilkS", size=s, thickness=t))
    f.append(Text(type="value", text=footprint_name, at=[xCenter, yValue],
                  layer="F.Fab", size=s, thickness=t))
    f.append(Text(type="user", text="%R", at=[xCenter, yCenter],
                  layer="F.Fab", size=s, thickness=t))

    # Fab
    f.append(PolygoneLine(polygone=[[xLeft + chamfer, yTop],
                                    [xRight, yTop],
                                    [xRight, yBottom],
                                    [xLeft, yBottom],
                                    [xLeft, yTop + chamfer],
                                    [xLeft + chamfer, yTop]],
                          layer="F.Fab",
                          width=wFab))

    def tb_silkscreen(yOuter, yInner):
        f.append(PolygoneLine(polygone=[[xLeft - wSilkS, yInner],
                                        [xLeft - wSilkS, yOuter],
                                        [xRight + wSilkS, yOuter],
                                        [xRight + wSilkS, yInner]],
                              layer="F.SilkS",
                              width=wSilkS))

    space = pad_height / 2 + silk_clearance

    tb_silkscreen(yTop - wSilkS, rows[0] - space)
    tb_silkscreen(yBottom + wSilkS, rows[2] + space)

    def compute_segment(row):
        return [rows[row] + space, rows[row + 1] - space]

    def lr_silkscreen(x, noMiddle):
        ys1 = compute_segment(0)
        ys2 = compute_segment(1)
        if noMiddle:
            ys = [[ys1[0], ys2[1]]]
        else:
            ys = [ys1, ys2]
        for seg in ys:
            f.append(Line(start=[x, seg[0]],
                          end=[x, seg[1]],
                          layer="F.SilkS",
                          width=wSilkS))

    lr_silkscreen(xLeft - wSilkS, False)
    lr_silkscreen(xRight + wSilkS, gray)

    margin = crtYd + wSilkS
    f.append(PolygoneLine(polygone=[[boundLeft - margin, yTop + chamfer],
                                    [boundLeft - margin, yTop - margin],
                                    [boundLeft + chamfer, yTop - margin]],
                          layer="F.SilkS",
                          width=wSilkS))

    if thru_hole:
        f.append(Circle(center=[xCenter, yCenter],
                        radius=r,
                        layer="F.SilkS",
                        width=wSilkS))
        f.append(Line(start=[xCenter, yCenter - r * 0.75],
                      end=[xCenter, yCenter + r * 0.75],
                      layer="F.SilkS",
                      width=wSilkS))
        f.append(PolygoneLine(polygone=[[xCenter - r * 0.5, yCenter - r * 0.25],
                                        [xCenter, yCenter - r * 0.75],
                                        [xCenter + r * 0.5, yCenter - r * 0.25]],
                              layer="F.SilkS",
                              width=wSilkS))

    # Courtyard
    f.append(RectLine(start=[boundLeft - crtYd, yTop - crtYd],
                      end=[boundRight + crtYd, yBottom + crtYd],
                      layer="F.CrtYd",
                      width=wCrtYd))

    # Pins
    for row in range(0, 3):
        for col in range(0, 2):
            pin = pins[row * 2 + col]
            if pin == "1":
                padShape=Pad.SHAPE_RECT
            else:
                padShape=Pad.SHAPE_OVAL
            if pin != "X":
                if thru_hole:
                    f.append(Pad(number=pin,
                                 type=Pad.TYPE_THT,
                                 shape=padShape,
                                 at=[columns[col], rows[row]],
                                 size=p,
                                 layers=Pad.LAYERS_THT,
                                 drill=d))
                else:
                    f.append(Pad(number=pin,
                                 type=Pad.TYPE_SMT,
                                 shape=Pad.SHAPE_RECT,
                                 at=[columns[col], rows[row]],
                                 size=p,
                                 layers=Pad.LAYERS_SMT))

    file_handler = KicadFileHandler(f)
    file_handler.writeFile(footprint_name + ".kicad_mod")


if __name__ == '__main__':
    parser = ModArgparser(rotary_coded_switch)
    # the root node of .yml files is parsed as name
    parser.add_parameter("name", type=str, required=True)
    parser.add_parameter("style", type=str, required=True)
    parser.add_parameter("datasheet", type=str, required=False, default="https://www.nidec-copal-electronics.com/e/catalog/switch/sh-7000.pdf")
    parser.add_parameter("thru_hole", type=bool, required=False, default=False)
    parser.add_parameter("pad_width", type=float, required=False, default=2.5)
    parser.add_parameter("pad_height", type=float, required=False, default=1.0)
    parser.add_parameter("pad_x_spacing", type=float, required=False, default=6.5)
    parser.add_parameter("pad_y_spacing", type=float, required=False, default=2.54)
    parser.add_parameter("gray", type=bool, required=False, default=False)
    parser.add_parameter("drill_size", type=float, required=False, default=1.0)
    parser.add_parameter("pkg_width", type=float, required=False, default=7.1)
    parser.add_parameter("pkg_height", type=float, required=False, default=7.3)

    # now run our script which handles the whole part of parsing the files
    parser.run()

