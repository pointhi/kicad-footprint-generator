#!/usr/bin/env python3

import sys

import os

# load parent path of KicadModTree
sys.path.append(os.path.join(sys.path[0], "..", ".."))
sys.path.append(os.path.join(sys.path[0], "..", "tools"))

from KicadModTree import *
from drawing_tools import *

def slide_pot(args):
    footprint_name = args["name"]
    dimA = args["dimA"]
    dimC = args["dimC"]
    dimD = args["dimD"]
    dimE = args["dimE"]
    travel = args["travel"]

    f = Footprint(footprint_name)
    f.setDescription("Bourns single-gang slide potentiometer, " + str(travel) + "mm travel")
    f.setTags("Bourns single-gang slide potentiometer " + str(travel) + "mm")
    f.append(Model(filename="${KISYS3DMOD}/Potentiometer_THT.3dshapes/" + footprint_name + ".wrl", at=[0.0, 0.0, 0.0], scale=[1.0, 1.0, 1.0], rotate=[0.0, 0.0, 0.0]))

    dPin = [1.2, 1.2]
    dMP = [1.7, 1.7]

    pPin = [2.2, 2.2]
    pMP = [2.7, 2.7]

    s = [1.0, 1.0]
    t = 0.15

    wCrtYd = 0.05
    wFab = 0.1
    wSilkS = 0.12

    silk = wSilkS
    silkGap = 2 * wSilkS
    silk_ko = 0.3
    crtYd = 0.5

    xCenter = dimE / 2
    yCenter = 3.5 / 2

    xPin1 = 0.0
    yPin1 = 0.0
    xPin2 = 0.0
    yPin2 = 3.5
    xPin3 = dimE
    yPin3 = 0.0

    mountingPins = []

    for row in [[-1, dimC], [1, dimD]]:
        y = yCenter + 8.4 / 2 * row[0]
        half = row[1] / 2
        mountingPins.append([xCenter - half, y])
        mountingPins.append([xCenter + half, y])

    halfWidth = dimA / 2
    halfHeight = 9.0 / 2

    xLeftFab = xCenter - halfWidth
    xRightFab = xCenter + halfWidth
    yTopFab = yCenter - halfHeight
    yBottomFab = yCenter + halfHeight

    xLeftSilk = xLeftFab - silk
    xRightSilk = xRightFab + silk
    yTopSilk = yTopFab - silk
    yBottomSilk = yBottomFab + silk

    xLeftCrtYd = xLeftFab - crtYd
    xRightCrtYd = xRightFab + crtYd
    yTopCrtYd = yTopFab - crtYd
    yBottomCrtYd = yBottomFab + crtYd

    yRef = yTopFab - 1.25
    yValue = yBottomFab + 1.25
    yFabRef = yCenter

    keepouts = []

    # Pins
    for pin in [["1", [xPin1, yPin1], Pad.SHAPE_RECT],
                ["2", [xPin2, yPin2], Pad.SHAPE_CIRCLE],
                ["3", [xPin3, yPin3], Pad.SHAPE_CIRCLE]]:
        f.append(Pad(number=pin[0], type=Pad.TYPE_THT, shape=pin[2], at=pin[1],
                     size=pPin, layers=Pad.LAYERS_THT, drill=dPin))
        x = pin[1][0]
        y = pin[1][1]
        d = pPin[0] + 2 * silk_ko
        if pin[0] == "1":
            keepouts = keepouts + addKeepoutRect(x, y, d, d)
        else:
            keepouts = keepouts + addKeepoutRound(x, y, d, d)

    for mp in mountingPins:
        f.append(Pad(number="MP", type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
                     at=mp, size=pMP, layers=Pad.LAYERS_THT, drill=dMP))
        d = pMP[0] + 2 * silk_ko
        keepouts = keepouts + addKeepoutRound(mp[0], mp[1], d, d)

    # Text
    f.append(Text(type="reference", text="REF**", at=[xCenter, yRef], layer="F.SilkS", size=s, thickness=t))
    f.append(Text(type="value", text=footprint_name, at=[xCenter, yValue], layer="F.Fab", size=s, thickness=t))
    f.append(Text(type="user", text="%R", at=[xCenter, yFabRef], layer="F.Fab", size=s, thickness=t))

    # Fab
    f.append(PolygoneLine(polygone=[[xLeftFab + 1, yTopFab],
                                    [xRightFab, yTopFab],
                                    [xRightFab, yBottomFab],
                                    [xLeftFab, yBottomFab],
                                    [xLeftFab, yTopFab + 1],
                                    [xLeftFab + 1, yTopFab]],
                          layer="F.Fab",
                          width=wFab))

    # Silk
    addRectWithKeepout(f, xLeftSilk, yTopSilk,
                       xRightSilk - xLeftSilk, yBottomSilk - yTopSilk,
                       "F.SilkS", wSilkS, keepouts)
    f.append(PolygoneLine(polygone=[[xLeftSilk - silkGap, yTopSilk + 1],
                                    [xLeftSilk - silkGap, yTopSilk - silkGap],
                                    [xLeftSilk + 1, yTopSilk - silkGap]],
                          layer="F.SilkS",
                          width=wSilkS))

    # CrtYd
    f.append(RectLine(start=[xLeftCrtYd, yTopCrtYd],
                      end=[xRightCrtYd, yBottomCrtYd],
                      layer="F.CrtYd",
                      width=wCrtYd))

    file_handler = KicadFileHandler(f)
    file_handler.writeFile(footprint_name + ".kicad_mod")


if __name__ == '__main__':
    parser = ModArgparser(slide_pot)
    # the root node of .yml files is parsed as name
    parser.add_parameter("name", type=str, required=True)
    parser.add_parameter("dimA", type=float, required=True)
    parser.add_parameter("dimC", type=float, required=True)
    parser.add_parameter("dimD", type=float, required=True)
    parser.add_parameter("dimE", type=float, required=True)
    parser.add_parameter("travel", type=float, required=True)

    # now run our script which handles the whole part of parsing the files
    parser.run()
